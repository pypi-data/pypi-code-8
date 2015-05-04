#!/usr/bin/env python

# native Python imports
import os.path
import sys
import numpy as np
import json

# third-party imports
import cyvcf as vcf

# geminicassandra modules
import version
from ped import load_ped_file
import gene_table
import infotag
from database_cassandra import insert, batch_insert, create_tables
import annotations
import func_impact
import severe_impact
import popgen
import structural_variants as svs
from geminicassandra.gemini_constants import HET, HOM_ALT, HOM_REF, UNKNOWN
from compression import pack_blob
from geminicassandra.config import read_gemini_config
from cassandra.cluster import Cluster
from blist import blist
from itertools import repeat
from geminicassandra.ped import get_ped_fields
import time
from string import strip
from random import randint
from geminicassandra.table_schemes import get_column_names
from cassandra.query import BatchStatement, BatchType
import Queue
from cassandra.concurrent import execute_concurrent_with_args
from cassandra.policies import RetryPolicy
from cassandra import ConsistencyLevel

class GeminiLoader(object):
    """
    Object for creating and populating a geminicassandra
    database and auxillary data files.
    """
    def __init__(self, args):
        self.args = args
        
        # create a reader for the VCF file
        self.vcf_reader = self._get_vcf_reader()
        
        self.buffer_size = args.buffer_size
        self.queue_length = args.max_queue
        self._get_anno_version()
        self.contact_points = map(strip, args.contact_points.split(','))
        self.keyspace = args.keyspace
        self.replication_factor = args.replication
        
        self.typed_gt_column_names = []
        self.gt_column_names = []
        
        if not self.args.no_genotypes:
            self.samples = self.vcf_reader.samples
            self.gt_column_names, self.typed_gt_column_names = self._get_typed_gt_column_names()
            
        NUM_BUILT_IN = 6
        self.extra_sample_columns = get_ped_fields(args.ped_file)[NUM_BUILT_IN:]        

        if self.args.anno_type == "VEP":
            self._effect_fields = self._get_vep_csq(self.vcf_reader)
        else:
            self._effect_fields = []
            
    def single_core_stuff(self):
        
        self.store_vcf_header()
        self.store_resources()
        self.store_version()
        if not self.args.no_genotypes and not self.args.no_load_genotypes:
                # load the sample info from the VCF file.
            self._prepare_samples()
                # initialize genotype counts for each sample
            self.num_samples = len(self.samples)
        else:
            self.num_samples = 0
            
        if not self.args.skip_gene_tables:
            self._get_gene_detailed()
            self._get_gene_summary()

    def store_vcf_header(self):
        """Store the raw VCF header.
        """
        insert(self.session, 'vcf_header', get_column_names('vcf_header'), [self.vcf_reader.raw_header])

    def store_resources(self):
        """Create table of annotation resources used in this geminicassandra database.
        """
        batch_insert(self.session, 'resources', get_column_names('resources'), annotations.get_resources( self.args ))

    def store_version(self):
        """Create table documenting which geminicassandra version was used for this db.
        """
        insert(self.session, 'version', get_column_names('version'), [version.__version__])
    
    def _get_typed_gt_column_names(self):
            
        gt_cols = [('gts', 'text'),
                   ('gt_types', 'int'),
                   ('gt_phases', 'int'),
                   ('gt_depths', 'int'),
                   ('gt_ref_depths', 'int'),
                   ('gt_alt_depths', 'int'),
                   ('gt_quals', 'float'),
                   ('gt_copy_numbers', 'float')]
        
        column_names = concat(map(lambda x: map(lambda y: x[0] + '_' + y, self.samples), gt_cols))
        typed_column_names = concat(map(lambda x: map(lambda y: x[0] + '_' + y + ' ' + x[1], self.samples), gt_cols))
        
        return (column_names, typed_column_names)
    
    def _get_vid(self):
        if hasattr(self.args, 'offset'):
            v_id = int(self.args.offset)
        else:
            v_id = 1
        return v_id
    
    def prepare_insert_queries(self):
        
        basic_query = 'INSERT INTO %s ( %s ) VALUES ( %s  )'
        
        from time import sleep
        
        nap = 20*randint(0,6)
        sleep(nap)
        
        start_time = time.time()
        
        self.insert_variants_query = self.session.prepare(basic_query % \
                             ('variants', ','.join(get_column_names('variants') + self.gt_column_names), ','.join(list(repeat("?",len(get_column_names('variants') + self.gt_column_names))))))
        self.insert_variants_samples_gt_types_query = self.session.prepare(basic_query % \
                             ('variants_by_samples_gt_types', "variant_id, sample_name, gt_types", ','.join(list(repeat("?",3)))))
        self.insert_samples_variants_gt_types_query = self.session.prepare(basic_query % \
                             ('samples_by_variants_gt_type', "variant_id, sample_name, gt_type", ','.join(list(repeat("?",3)))))
        self.insert_variants_samples_gt_depths_query = self.session.prepare(basic_query % \
                             ('variants_by_samples_gt_depths', "variant_id, sample_name, gt_depths", ','.join(list(repeat("?",3)))))
        self.insert_variants_samples_gts_query = self.session.prepare(basic_query % \
                             ('variants_by_samples_gts', "variant_id, sample_name, gts", ','.join(list(repeat("?",3))))) 
        self.insert_variant_impacts_query = self.session.prepare(basic_query % \
                             ('variant_impacts', ','.join(get_column_names('variant_impacts')), ','.join(list(repeat("?", len(get_column_names('variant_impacts')))))))
        self.insert_variant_stcr_query = self.session.prepare(basic_query % \
                             ('variants_by_sub_type_call_rate', ','.join(get_column_names('variants_by_sub_type_call_rate')), ','.join(list(repeat("?", 3)))))
        self.insert_variant_gene_query = self.session.prepare(basic_query % \
                             ('variants_by_gene', 'variant_id, gene', ','.join(list(repeat("?", 2)))))
        self.insert_variant_chrom_start_query = self.session.prepare(basic_query % \
                             ('variants_by_chrom_start', 'variant_id, chrom, start', ','.join(list(repeat("?", 3)))))
                       
        end_time = time.time()
        
        print("preparing statements took %.2f s." % (end_time - start_time))
                                                 
    def populate_from_vcf(self):
        """
        """
        self.v_id = self._get_vid()
        self.var_buffer = blist([])
        self.var_impacts_buffer = blist([])
        self.var_subtypes_buffer = blist([])
        self.var_gene_buffer = blist([])
        self.var_chrom_start_buffer = blist([])
        self.prepare_insert_queries()
        buffer_count = 0
        self.skipped = 0
        #extra_file, extraheader_file = geminicassandra.get_extra_files(self.args.db)
        #extra_headers = {}
        self.counter = 0
        start_time = time.time()
        interval_start = time.time()
        variants_gts_timer = 0
        log_file = open("loading_logs/%s.csv" % str(os.getpid()), "w")
        sys.err = open("loading_logs/%s.err" % str(os.getpid()), "w")
        #with open(extra_file, "w") as extra_handle:
            # process and load each variant in the VCF file
        vars_inserted = 0
        for var in self.vcf_reader:
            if self.args.passonly and (var.FILTER is not None and var.FILTER != "."):
                self.skipped += 1
                continue
            (variant, variant_impacts, sample_info, extra_fields) = self._prepare_variation(var)
            # add the core variant info to the variant buffer
            self.var_buffer.append(variant)
            self.var_subtypes_buffer.append([self.v_id, variant[11], variant[12]])
            if variant[55] != None:
                self.var_gene_buffer.append([self.v_id, variant[55]])
            self.var_chrom_start_buffer.append([self.v_id, variant[0], variant[1]])
        
            var_sample_gt_types_buffer = blist([])
            var_sample_gt_depths_buffer = blist([])
            var_sample_gt_buffer = blist([])
                
            for sample in sample_info:
                if sample[1] != None:
                    var_sample_gt_depths_buffer.append([self.v_id, sample[0], sample[2]])
                    var_sample_gt_types_buffer.append([self.v_id, sample[0], sample[1]])
                    var_sample_gt_buffer.append([self.v_id, sample[0], sample[3]])        
                             
            stime = time.time()                       
            self.prepared_batch_insert(self.session, var_sample_gt_types_buffer, var_sample_gt_depths_buffer, var_sample_gt_buffer, 30)
            variants_gts_timer += (time.time() - stime)
            
                # add each of the impact for this variant (1 per gene/transcript)
            for var_impact in variant_impacts:
                self.var_impacts_buffer.append(var_impact)

            buffer_count += 1
                # buffer full - start to insert into DB
            if buffer_count >= self.buffer_size:
                startt = time.time()
                execute_concurrent_with_args(self.session, self.insert_variants_query, self.var_buffer,30)
                execute_concurrent_with_args(self.session, self.insert_variant_impacts_query, self.var_impacts_buffer)
                execute_concurrent_with_args(self.session, self.insert_variant_stcr_query, self.var_subtypes_buffer)
                execute_concurrent_with_args(self.session, self.insert_variant_gene_query, self.var_gene_buffer)
                execute_concurrent_with_args(self.session, self.insert_variant_chrom_start_query, self.var_chrom_start_buffer)
                endt = time.time()
                    # binary.genotypes.append(var_buffer)
                    # reset for the next batch
                self.var_buffer = blist([])
                self.var_subtypes_buffer = blist([])
                self.var_impacts_buffer = blist([])
                self.var_gene_buffer = blist([])
                self.var_chrom_start_buffer = blist([])
                vars_inserted += self.buffer_size   
                if(self.args.offset == '1'):                   
                    print "%s vars done; last %s took %.2f s; var tables %.2f s; var_gt_tables %.2f s" % (vars_inserted, self.buffer_size, endt - interval_start, endt - startt, variants_gts_timer) 
                log_file.write("%s;%.2f;%.2f;%.2f\n" % (self.buffer_size, endt - interval_start, endt - startt, variants_gts_timer)) 
                log_file.flush()       
                buffer_count = 0
                interval_start = time.time()
                variants_gts_timer = 0
            self.v_id += 1
            self.counter += 1
        '''if extra_headers:
            with open(extraheader_file, "w") as out_handle:
                out_handle.write(json.dumps(extra_headers))
        else:
            os.remove(extra_file)'''
        # final load to the database
        self.v_id -= 1
        
        startt = time.time()
        execute_concurrent_with_args(self.session, self.insert_variants_query, self.var_buffer)
        execute_concurrent_with_args(self.session, self.insert_variant_impacts_query, self.var_impacts_buffer)
        execute_concurrent_with_args(self.session, self.insert_variant_stcr_query, self.var_subtypes_buffer)
        execute_concurrent_with_args(self.session, self.insert_variant_gene_query, self.var_gene_buffer,self)
        execute_concurrent_with_args(self.session, self.insert_variant_chrom_start_query, self.var_chrom_start_buffer)
        
        end_time = time.time()
        vars_inserted += self.buffer_size   
        log_file.write("%s;%.2f;%.2f;%.2f\n" % (self.buffer_size, end_time - interval_start, end_time - startt, variants_gts_timer))        
        log_file.close()        
        elapsed_time = end_time - start_time            
        sys.stderr.write("pid " + str(os.getpid()) + ": " +
                         str(self.counter) + " variants processed in %s s.\n" % elapsed_time)
        if self.args.passonly:
            sys.stderr.write("pid " + str(os.getpid()) + ": " +
                             str(self.skipped) + " skipped due to having the "
                             "FILTER field set.\n")
            
    def prepared_batch_insert(self, session, types_buf, depth_buf, gt_buffer, queue_length=30):
        """
        Populate the given table with the given values
        """
        
        class custom_retry_policy(RetryPolicy):
            
            def on_read_timeout(self, *args, **kwargs):
                return (self.RETHROW, None)

            def on_write_timeout(self, *args, **kwargs):
                return (self.RETRY, ConsistencyLevel.ONE)
        
            def on_unavailable(self, *args, **kwargs):
                return (self.RETHROW, None)
        
        futures = Queue.Queue(maxsize=queue_length+1)
        for i in range(len(types_buf)):
            if i >= queue_length:
                old_future = futures.get_nowait()
                old_future.result()
            
            batch = BatchStatement(batch_type=BatchType.UNLOGGED, retry_policy=custom_retry_policy)
            batch.add(self.insert_samples_variants_gt_types_query, types_buf[i])
            batch.add(self.insert_variants_samples_gt_types_query, types_buf[i])
            batch.add(self.insert_variants_samples_gt_depths_query, depth_buf[i])
            batch.add(self.insert_variants_samples_gts_query, gt_buffer[i])
            future = session.execute_async(batch)
            futures.put_nowait(future)

    def _update_extra_headers(self, headers, cur_fields):
        """Update header information for extra fields.
        """
        for field, val in cur_fields.items():
            headers[field] = self._get_field_type(val, headers.get(field, "integer"))
        return headers

    def _get_field_type(self, val, cur_type):
        start_checking = False
        for name, check_fn in [("integer", int), ("float", float), ("text", str)]:
            if name == cur_type:
                start_checking = True
            if start_checking:
                try:
                    check_fn(val)
                    break
                except:
                    continue
        return name

    def disconnect(self):
        """
        Create the db table indices and close up
        db connection
        """
        # index our tables for speed
        # commit data and close up
        self.session.shutdown()

    def _get_vcf_reader(self):
        # the VCF is a proper file
        if self.args.vcf != "-":
            if self.args.vcf.endswith(".gz"):
                return vcf.VCFReader(open(self.args.vcf), 'rb', compressed=True)
            else:
                return vcf.VCFReader(open(self.args.vcf), 'rb')
        # the VCF is being passed in via STDIN
        else:
            return vcf.VCFReader(sys.stdin, 'rb')

    def _get_anno_version(self):
        """
        Extract the snpEff or VEP version used
        to annotate the VCF
        """
        # default to unknown version
        self.args.version = None

        if self.args.anno_type == "snpEff":
            try:
                version_string = self.vcf_reader.metadata['SnpEffVersion']
            except KeyError:
                error = ("\nWARNING: VCF is not annotated with snpEff, check documentation at:\n"\
                "http://geminicassandra.readthedocs.org/en/latest/content/functional_annotation.html#stepwise-installation-and-usage-of-snpeff\n")
                sys.exit(error)

            # e.g., "SnpEff 3.0a (build 2012-07-08), by Pablo Cingolani"
            # or "3.3c (build XXXX), by Pablo Cingolani"

            version_string = version_string.replace('"', '')  # No quotes

            toks = version_string.split()

            if "SnpEff" in toks[0]:
                self.args.raw_version = toks[1]  # SnpEff *version*, etc
            else:
                self.args.raw_version = toks[0]  # *version*, etc
            # e.g., 3.0a -> 3
            self.args.maj_version = int(self.args.raw_version.split('.')[0])

        elif self.args.anno_type == "VEP":
            pass

    def _get_vep_csq(self, reader):
        """
        Test whether the VCF header meets expectations for
        proper execution of VEP for use with Gemini.
        """
        required = ["Consequence"]
        expected = "Consequence|Codons|Amino_acids|Gene|SYMBOL|Feature|EXON|PolyPhen|SIFT|Protein_position|BIOTYPE".upper()  # @UnusedVariable
        if 'CSQ' in reader.infos:
            parts = str(reader.infos["CSQ"].desc).split("Format: ")[-1].split("|")
            all_found = True
            for check in required:
                if check not in parts:
                    all_found = False
                    break
            if all_found:
                return parts
        # Did not find expected fields
        error = "\nERROR: Check geminicassandra docs for the recommended VCF annotation with VEP"\
                "\nhttp://geminicassandra.readthedocs.org/en/latest/content/functional_annotation.html#stepwise-installation-and-usage-of-vep"
        sys.exit(error)

    def setup_db(self):
        """
        Create keyspace named 'gemini_keyspace' and all tables. (IF NOT EXISTS)
        """
        self.cluster = Cluster(self.contact_points)
        self.session = self.cluster.connect()
        query = "CREATE KEYSPACE IF NOT EXISTS %s WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : %d}" % (self.keyspace, self.replication_factor)
        self.session.execute(query)
        self.session.set_keyspace(self.keyspace)
        # create the geminicassandra database tables for the new DB
        create_tables(self.session, self.typed_gt_column_names, self.extra_sample_columns)
        
    def connect_to_db(self):
        
        self.cluster = Cluster(self.contact_points)
        self.session = self.cluster.connect(self.keyspace)        

    def _prepare_variation(self, var):
        """private method to collect metrics for a single variant (var) in a VCF file.

        Extracts variant information, variant impacts and extra fields for annotation.
        """
        extra_fields = {}
        # these metrics require that genotypes are present in the file
        call_rate = None
        hwe_p_value = None
        pi_hat = None
        inbreeding_coeff = None
        hom_ref = het = hom_alt = unknown = None

        # only compute certain metrics if genotypes are available
        if not self.args.no_genotypes and not self.args.no_load_genotypes:
            hom_ref = var.num_hom_ref
            hom_alt = var.num_hom_alt
            het = var.num_het
            unknown = var.num_unknown
            
            try:
                call_rate = var.call_rate
            except ValueError:  #TODO: catch error instead of bogus value
                call_rate = -43.0
            aaf = var.aaf
            hwe_p_value, inbreeding_coeff = \
                popgen.get_hwe_likelihood(hom_ref, het, hom_alt, aaf)
            pi_hat = var.nucl_diversity
        else:
            aaf = infotag.extract_aaf(var)

        ############################################################
        # collect annotations from geminicassandra's custom annotation files
        # but only if the size of the variant is <= 50kb
        ############################################################
        if var.end - var.POS < 50000:
            pfam_domain = annotations.get_pfamA_domains(var)
            cyto_band = annotations.get_cyto_info(var)
            rs_ids = annotations.get_dbsnp_info(var)
            clinvar_info = annotations.get_clinvar_info(var)
            in_dbsnp = 0 if rs_ids is None else 1
            rmsk_hits = annotations.get_rmsk_info(var)
            in_cpg = annotations.get_cpg_island_info(var)
            in_segdup = annotations.get_segdup_info(var)
            is_conserved = annotations.get_conservation_info(var)
            esp = annotations.get_esp_info(var)
            thousandG = annotations.get_1000G_info(var)
            recomb_rate = annotations.get_recomb_info(var)
            gms = annotations.get_gms(var)
            grc = annotations.get_grc(var)
            in_cse = annotations.get_cse(var)
            encode_tfbs = annotations.get_encode_tfbs(var)
            encode_dnaseI = annotations.get_encode_dnase_clusters(var)
            encode_cons_seg = annotations.get_encode_consensus_segs(var)
            gerp_el = annotations.get_gerp_elements(var)
            vista_enhancers = annotations.get_vista_enhancers(var)
            cosmic_ids = annotations.get_cosmic_info(var)
            fitcons = annotations.get_fitcons(var)
            Exac = annotations.get_exac_info(var)

            #load CADD scores by default
            if self.args.skip_cadd is False:
                (cadd_raw, cadd_scaled) = annotations.get_cadd_scores(var)
            else:
                (cadd_raw, cadd_scaled) = (None, None)

            # load the GERP score for this variant by default.
            gerp_bp = None
            if self.args.skip_gerp_bp is False:
                gerp_bp = annotations.get_gerp_bp(var)
        # the variant is too big to annotate
        else:
            pfam_domain = None
            cyto_band = None
            rs_ids = None
            clinvar_info = annotations.ClinVarInfo()
            in_dbsnp = None
            rmsk_hits = None
            in_cpg = None
            in_segdup = None
            is_conserved = None
            esp = annotations.ESPInfo(None, None, None, None, None)
            thousandG = annotations.ThousandGInfo(None, None, None, None, None, None, None)
            Exac = annotations.ExacInfo(None, None, None, None, None, None, None, None, None, None)
            recomb_rate = None
            gms = annotations.GmsTechs(None, None, None)
            grc = None
            in_cse = None
            encode_tfbs = None
            encode_dnaseI = annotations.ENCODEDnaseIClusters(None, None)
            encode_cons_seg = annotations.ENCODESegInfo(None, None, None, None, None, None)
            gerp_el = None
            vista_enhancers = None
            cosmic_ids = None
            fitcons = None                
            cadd_raw = None
            cadd_scaled = None
            gerp_bp = None

        # impact is a list of impacts for this variant
        impacts = None
        severe_impacts = None
        # impact terms initialized to None for handling unannotated vcf's
        # anno_id in variants is for the trans. with the most severe impact term
        gene = transcript = exon = codon_change = aa_change = aa_length = \
            biotype = consequence = consequence_so = effect_severity = None
        is_coding = is_exonic = is_lof = None
        polyphen_pred = polyphen_score = sift_pred = sift_score = anno_id = None

        if self.args.anno_type is not None:
            impacts = func_impact.interpret_impact(self.args, var, self._effect_fields)
            severe_impacts = \
                severe_impact.interpret_severe_impact(self.args, var, self._effect_fields)
            if severe_impacts:
                extra_fields.update(severe_impacts.extra_fields)
                gene = severe_impacts.gene
                transcript = severe_impacts.transcript
                exon = severe_impacts.exon
                codon_change = severe_impacts.codon_change
                aa_change = severe_impacts.aa_change
                aa_length = severe_impacts.aa_length
                biotype = severe_impacts.biotype
                consequence = severe_impacts.consequence
                effect_severity = severe_impacts.effect_severity
                polyphen_pred = severe_impacts.polyphen_pred
                polyphen_score = severe_impacts.polyphen_score
                sift_pred = severe_impacts.sift_pred
                sift_score = severe_impacts.sift_score
                anno_id = severe_impacts.anno_id
                is_exonic = severe_impacts.is_exonic
                is_coding = severe_impacts.is_coding
                is_lof = severe_impacts.is_lof
                consequence_so = severe_impacts.so

        # construct the var_filter string
        var_filter = None
        if var.FILTER is not None and var.FILTER != ".":
            if isinstance(var.FILTER, list):
                var_filter = ";".join(var.FILTER)
            else:
                var_filter = var.FILTER

        #TODO: sensible value
        vcf_id = None
        if var.ID is not None and var.ID != ".":
            vcf_id = var.ID

        # build up numpy arrays for the genotype information.
        sample_info = blist([])
        if not self.args.no_genotypes and not self.args.no_load_genotypes:
            gt_bases = var.gt_bases  # 'A/G', './.'
            gt_types = var.gt_types  # -1, 0, 1, 2
            gt_phases = var.gt_phases  # T F F
            gt_depths = var.gt_depths  # 10 37 0
            gt_ref_depths = var.gt_ref_depths  # 2 21 0 -1
            gt_alt_depths = var.gt_alt_depths  # 8 16 0 -1
            gt_quals = var.gt_quals  # 10.78 22 99 -1
            gt_copy_numbers = var.gt_copy_numbers  # 1.0 2.0 2.1 -1
            gt_columns = concat([gt_bases, gt_types, gt_phases, gt_depths, gt_ref_depths, gt_alt_depths, gt_quals, gt_copy_numbers])

            for entry in var.samples:
                sample_info.append((entry.sample, entry.gt_type, entry.gt_depth, entry.gt_bases))

            # tally the genotypes            
            self._update_sample_gt_counts(np.array(var.gt_types, np.int8))
            
        else:
            gt_columns= []            
        
        if self.args.skip_info_string is False:
            info = var.INFO
        else:
            info = None

        # were functional impacts predicted by SnpEFF or VEP?
        # if so, build up a row for each of the impacts / transcript
        variant_impacts = []
        if impacts is not None:
            for idx, impact in enumerate(impacts):
                var_impact = [self.v_id, (idx + 1), impact.gene,
                              impact.transcript, impact.is_exonic,
                              impact.is_coding, impact.is_lof,
                              impact.exon, impact.codon_change,
                              impact.aa_change, impact.aa_length,
                              impact.biotype, impact.consequence,
                              impact.so, impact.effect_severity,
                              impact.polyphen_pred, impact.polyphen_score,
                              impact.sift_pred, impact.sift_score]
                variant_impacts.append(var_impact)

        # extract structural variants
        sv = svs.StructuralVariant(var)
        ci_left = sv.get_ci_left()
        ci_right = sv.get_ci_right()

        # construct the core variant record.
        # 1 row per variant to VARIANTS table
        if extra_fields:
            extra_fields.update({"chrom": var.CHROM, "start": var.start, "end": var.end})
        chrom = var.CHROM if var.CHROM.startswith("chr") else "chr" + var.CHROM
        variant = [chrom, var.start, var.end,
                   vcf_id, self.v_id, anno_id, var.REF, ','.join(var.ALT),
                   var.QUAL, var_filter, var.var_type,
                   var.var_subtype,
                   call_rate, in_dbsnp,
                   rs_ids,
                   ci_left[0],
                   ci_left[1], 
                   ci_right[0],
                   ci_right[1],
                   sv.get_length(), 
                   sv.is_precise(),
                   sv.get_sv_tool(),
                   sv.get_evidence_type(),
                   sv.get_event_id(),
                   sv.get_mate_id(),
                   sv.get_strand(),
                   clinvar_info.clinvar_in_omim,
                   clinvar_info.clinvar_sig,
                   clinvar_info.clinvar_disease_name,
                   clinvar_info.clinvar_dbsource,
                   clinvar_info.clinvar_dbsource_id,
                   clinvar_info.clinvar_origin,
                   clinvar_info.clinvar_dsdb,
                   clinvar_info.clinvar_dsdbid,
                   clinvar_info.clinvar_disease_acc,
                   clinvar_info.clinvar_in_locus_spec_db,
                   clinvar_info.clinvar_on_diag_assay,
                   clinvar_info.clinvar_causal_allele,
                   pfam_domain, cyto_band, rmsk_hits, in_cpg,
                   in_segdup, is_conserved, gerp_bp, parse_float(gerp_el),
                   hom_ref, het, hom_alt, unknown,
                   aaf, hwe_p_value, inbreeding_coeff, pi_hat,
                   recomb_rate, gene, transcript, is_exonic,
                   is_coding, is_lof, exon, codon_change, aa_change,
                   aa_length, biotype, consequence, consequence_so, effect_severity,
                   polyphen_pred, polyphen_score, sift_pred, sift_score,
                   infotag.get_ancestral_allele(var), infotag.get_rms_bq(var),
                   infotag.get_cigar(var),
                   infotag.get_depth(var), infotag.get_strand_bias(var),
                   infotag.get_rms_map_qual(var), infotag.get_homopol_run(var),
                   infotag.get_map_qual_zero(var),
                   infotag.get_num_of_alleles(var),
                   infotag.get_frac_dels(var),
                   infotag.get_haplotype_score(var),
                   infotag.get_quality_by_depth(var),
                   infotag.get_allele_count(var), infotag.get_allele_bal(var),
                   infotag.in_hm2(var), infotag.in_hm3(var),
                   infotag.is_somatic(var),
                   infotag.get_somatic_score(var),
                   esp.found, esp.aaf_EA,
                   esp.aaf_AA, esp.aaf_ALL,
                   esp.exome_chip, thousandG.found,
                   parse_float(thousandG.aaf_AMR), parse_float(thousandG.aaf_EAS), 
                   parse_float(thousandG.aaf_SAS), parse_float(thousandG.aaf_AFR), 
                   parse_float(thousandG.aaf_EUR), parse_float(thousandG.aaf_ALL), grc,
                   parse_float(gms.illumina), parse_float(gms.solid),
                   parse_float(gms.iontorrent), in_cse,
                   encode_tfbs,
                   parse_int(encode_dnaseI.cell_count),
                   encode_dnaseI.cell_list,
                   encode_cons_seg.gm12878,
                   encode_cons_seg.h1hesc,
                   encode_cons_seg.helas3,
                   encode_cons_seg.hepg2,
                   encode_cons_seg.huvec,
                   encode_cons_seg.k562,
                   vista_enhancers,
                   cosmic_ids,
                   pack_blob(info),
                   cadd_raw,
                   cadd_scaled,
                   fitcons,
                   Exac.found,
                   parse_float(Exac.aaf_ALL),
                   Exac.adj_aaf_ALL,
                   Exac.aaf_AFR, Exac.aaf_AMR,
                   Exac.aaf_EAS, Exac.aaf_FIN,
                   Exac.aaf_NFE, Exac.aaf_OTH,
                   Exac.aaf_SAS] + gt_columns
                   
        
            
        return variant, variant_impacts, sample_info, extra_fields
    
    
    def _prepare_samples(self):
        """
        private method to load sample information
        """
        if not self.args.no_genotypes:
            self.sample_to_id = {}
            for idx, sample in enumerate(self.samples):
                self.sample_to_id[sample] = idx + 1

        self.ped_hash = {}
        if self.args.ped_file is not None:
            self.ped_hash = load_ped_file(self.args.ped_file)
       
        samples_buffer = blist([])
        buffer_counter = 0
        for sample in self.samples:
            sample_list = []
            i = self.sample_to_id[sample]
            if sample in self.ped_hash:
                fields = self.ped_hash[sample]
                sample_list = [i] + fields
            elif len(self.ped_hash) > 0:
                sys.exit("EXITING: sample %s found in the VCF but "
                                 "not in the PED file.\n" % (sample))
            else:
                # if there is no ped file given, just fill in the name and
                # sample_id and set random value for sex & phenotype
                sample_list = [i, '0', sample, '0', '0', str(randint(1,2)), str(randint(1,2))]
                
            samples_buffer.append(sample_list)
            buffer_counter += 1
            
            if buffer_counter >= self.buffer_size:
                batch_insert(self.session, 'samples', get_column_names('samples') + self.extra_sample_columns, samples_buffer)
                buffer_counter = 0
                samples_buffer = blist([])
        
        column_names = get_column_names('samples') + self.extra_sample_columns  
        batch_insert(self.session, 'samples', column_names, samples_buffer)
        batch_insert(self.session, 'samples_by_phenotype', column_names, samples_buffer)
        batch_insert(self.session, 'samples_by_sex', column_names, samples_buffer)        
        
    def _get_gene_detailed(self):
        """
        define a gene detailed table
        """
        #unique identifier for each entry
        i = 0
        detailed_list = []
        gene_buffer = blist([])
        buffer_count = 0
        
        config = read_gemini_config( args = self.args )
        path_dirname = config["annotation_dir"]
        file_handle = os.path.join(path_dirname, 'detailed_gene_table_v75')
        for line in open(file_handle, 'r'):
            field = line.strip().split("\t")
            if not field[0].startswith("Chromosome"):
                i += 1
                table = gene_table.gene_detailed(field)
                detailed_list = [i,table.chrom,table.gene,table.is_hgnc,
                                 table.ensembl_gene_id,table.ensembl_trans_id, 
                                 table.biotype,table.trans_status,table.ccds_id, 
                                 table.hgnc_id,table.entrez,table.cds_length,table.protein_length, 
                                 table.transcript_start,table.transcript_end,
                                 table.strand,table.synonym,table.rvis,table.mam_phenotype]
                gene_buffer.append(detailed_list)
                buffer_count += 1
            #TODO: buffer size same as for variants?
            if buffer_count >= self.buffer_size / 2:
                batch_insert(self.session, 'gene_detailed', get_column_names('gene_detailed'), gene_buffer)
                buffer_count = 0
                gene_buffer = blist([])
                
        batch_insert(self.session, 'gene_detailed', get_column_names('gene_detailed'), gene_buffer)
        
    def _get_gene_summary(self):
        """
        define a gene summary table
        """
        #unique identifier for each entry
        i = 0
        summary_list = []
        gene_buffer = blist([])
        buffer_count = 0
        
        config = read_gemini_config( args = self.args )
        path_dirname = config["annotation_dir"]
        file_path = os.path.join(path_dirname, 'summary_gene_table_v75')
        print 'gene file path = %s' % file_path
        for line in open(file_path, 'r'):
            col = line.strip().split("\t")
            if not col[0].startswith("Chromosome"):
                i += 1
                table = gene_table.gene_summary(col)
                # defaul cosmic census to False
                cosmic_census = 0
                summary_list = [i,table.chrom,table.gene,table.is_hgnc,
                                table.ensembl_gene_id,table.hgnc_id,
                                table.transcript_min_start,
                                table.transcript_max_end,table.strand,
                                table.synonym,table.rvis,table.mam_phenotype,
                                cosmic_census]
                gene_buffer.append(summary_list)
                buffer_count += 1
                
            if buffer_count >= self.buffer_size / 2:
                batch_insert(self.session, 'gene_summary', get_column_names("gene_summary"), gene_buffer)
                buffer_count = 0
                gene_buffer = blist([])
                
        batch_insert(self.session, 'gene_summary', get_column_names("gene_summary"), gene_buffer)

    def update_gene_table(self):
        """
        """
        gene_table.update_cosmic_census_genes(self.session, self.args)

    def _init_sample_gt_counts(self):
        """
        Initialize a 2D array of counts for tabulating
        the count of each genotype type for each sample.

        The first dimension is one bucket for each sample.
        The second dimension (size=4) is a count for each gt type.
           Index 0 == # of hom_ref genotypes for the sample
           Index 1 == # of het genotypes for the sample
           Index 2 == # of missing genotypes for the sample
           Index 3 == # of hom_alt genotypes for the sample
        """
        self.sample_gt_counts = np.array(np.zeros((len(self.samples), 4)),
                                         dtype='uint32')

    def _update_sample_gt_counts(self, gt_types):
        """
        Update the count of each gt type for each sample
        """
        for idx, gt_type in enumerate(gt_types):
            self.sample_gt_counts[idx][gt_type] += 1

    def store_sample_gt_counts(self):
        """
        Update the count of each gt type for each sample
        """
        samples_buffer = blist([])
        buffer_count = 0
        for idx, gt_counts in enumerate(self.sample_gt_counts):
            if buffer_count < 10000:
                samples_buffer.append([int(gt_counts[HOM_REF]),  # hom_ref
                                int(gt_counts[HET]),  # het
                                int(gt_counts[HOM_ALT]),  # hom_alt
                                int(gt_counts[UNKNOWN]), #missing
                                idx])
                buffer_count += 1
            else:
                self.batch_insert_gt_counts(samples_buffer)
                samples_buffer = blist([])
                buffer_count = 0
        self.batch_insert_gt_counts(samples_buffer)   
            
    def batch_insert_gt_counts(self, contents):
        
        update_query = self.session.prepare('''UPDATE sample_genotype_counts    \
                                               SET num_hom_ref = ?,\
                                               num_het = ?,            \
                                               num_hom_alt = ?,    \
                                               num_unknown = ?,    \
                                               version = ?   \
                                               WHERE sample_id = ? \
                                               IF version = ?''')
        
        create_query = self.session.prepare('''INSERT INTO sample_genotype_counts \
                                               (num_hom_ref,\
                                               num_het,            \
                                               num_hom_alt,    \
                                               num_unknown,    \
                                               sample_id, \
                                               version)    \
                                               VALUES (?,?,?,?,?,?) IF NOT EXISTS''')
        
        get_query = self.session.prepare("SELECT * FROM sample_genotype_counts WHERE sample_id = ?")
        
        def get_version(sample_id):
            res = self.session.execute(get_query, [sample_id])
            if len(res) > 0:
                return res[0]
            else:
                return []
        
        retries = []
        for entry in contents:
            vals = get_version(entry[4])
            versioned_entry = entry
            if vals == []:
                versioned_entry.append(0)
                res = self.session.execute(create_query, versioned_entry)
            else:
                updated_contents = [entry[0]+vals.num_hom_ref, entry[1]+vals.num_het, entry[2]+vals.num_hom_alt,\
                                    entry[3]+vals.num_unknown, vals.version + 1, entry[4],  vals.version]
                res = self.session.execute(update_query, updated_contents)
            if not res[0].applied:
                retries.append(entry)  
                
        if len(retries) > 0:
            self.batch_insert_gt_counts(retries)   
            
def concat(l):
        return reduce(lambda x, y: x + y, l, [])
    
def concat_key_value(samples_dict):
        return blist(map(lambda x: blist([x]) + samples_dict[x], samples_dict.keys()))

def parse_float(s):
    try:
        return float(s)
    except ValueError:
        return None
    except TypeError:
        return None
    
def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return -42
    except TypeError:
        return -43

def load(parser, args):
    if args.vcf is None:
        parser.print_help()
        exit("ERROR: load needs both a VCF file and a database file\n")
    if args.anno_type not in ['snpEff', 'VEP', None]:
        parser.print_help()
        exit("\nERROR: Unsupported selection for -t\n")

    # collect of the the add'l annotation files
    annotations.load_annos( args )

    # create a new geminicassandra loader and populate
    # the geminicassandra db and files from the VCF
    gemini_loader = GeminiLoader(args)
    gemini_loader.connect_to_db()
    if not args.no_genotypes and not args.no_load_genotypes:
        gemini_loader._init_sample_gt_counts()

    gemini_loader.populate_from_vcf()
    #gemini_loader.update_gene_table()
    
    if not args.no_genotypes and not args.no_load_genotypes:
        gemini_loader.store_sample_gt_counts()
        
    gemini_loader.disconnect()
