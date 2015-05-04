#!/usr/bin/env python

from itertools import repeat

from cassandra.query import BatchStatement, SimpleStatement
import Queue
from cassandra.concurrent import execute_concurrent_with_args

def drop_tables(session):
    session.execute("DROP TABLE IF EXISTS variants")
    session.execute("DROP TABLE IF EXISTS variant_impacts")
    session.execute("DROP TABLE IF EXISTS resources")
    session.execute("DROP TABLE IF EXISTS version")
    session.execute("DROP TABLE IF EXISTS gene_detailed")
    session.execute("DROP TABLE IF EXISTS gene_summary")

def create_tables(session, gt_column_names, extra_sample_columns):
    """
    Create our master DB tables
    """
        
    session.execute(SimpleStatement('''CREATE TABLE if not exists variant_impacts  (   \
                    variant_id int,                               \
                    anno_id int,                                  \
                    gene text,                                        \
                    transcript text,                                  \
                    is_exonic int,                                   \
                    is_coding int,                                   \
                    is_lof int,                                      \
                    exon text,                                        \
                    codon_change text,                                \
                    aa_change text,                                   \
                    aa_length text,                                   \
                    biotype text,                                     \
                    impact text,                                      \
                    impact_so text,                                   \
                    impact_severity text,                             \
                    polyphen_pred text,                               \
                    polyphen_score float,                             \
                    sift_pred text,                                   \
                    sift_score float,                                 \
                    PRIMARY KEY((variant_id, anno_id)))'''))

    session.execute(SimpleStatement('''CREATE TABLE if not exists resources ( \
                     name text PRIMARY KEY,                  \
                     resource text)'''))

    session.execute(SimpleStatement('''CREATE TABLE if not exists version ( \
                     version text PRIMARY KEY)'''))
    
    session.execute(SimpleStatement('''CREATE TABLE if not exists gene_detailed (       \
                   uid int PRIMARY KEY,                                \
                   chrom text,                                         \
                   gene text,                                          \
                   is_hgnc int,                                        \
                   ensembl_gene_id text,                               \
                   transcript text,                                    \
                   biotype text,                                       \
                   transcript_status text,                             \
                   ccds_id text,                                       \
                   hgnc_id text,                                       \
                   entrez_id text,                                     \
                   cds_length text,                                    \
                   protein_length text,                                \
                   transcript_start text,                              \
                   transcript_end text,                                \
                   strand text,                                        \
                   synonym text,                                       \
                   rvis_pct float,                                     \
                   mam_phenotype_id text)'''))
    
    session.execute(SimpleStatement('''CREATE TABLE if not exists gene_summary (     \
                    uid int PRIMARY KEY,                         \
                    chrom text,                                     \
                    gene text,                                      \
                    is_hgnc int,                                   \
                    ensembl_gene_id text,                           \
                    hgnc_id text,                                   \
                    transcript_min_start text,                      \
                    transcript_max_end text,                        \
                    strand text,                                    \
                    synonym text,                                   \
                    rvis_pct float,                                 \
                    mam_phenotype_id text,                          \
                    in_cosmic_census int)'''))
    
    session.execute(SimpleStatement('''CREATE TABLE if not exists variants_by_samples_gt_types ( \
                        sample_name text, \
                        gt_types int, \
                        variant_id int, \
                        primary key (sample_name, gt_types, variant_id))'''))
    
    session.execute(SimpleStatement('''CREATE TABLE if not exists variants_by_samples_gt_depths ( \
                        sample_name text, \
                        gt_depths int, \
                        variant_id int, \
                        primary key (sample_name, gt_depths, variant_id))''')) 
     
    session.execute(SimpleStatement('''CREATE TABLE if not exists variants_by_samples_gts ( \
                        sample_name text, \
                        gts text, \
                        variant_id int, \
                        primary key (sample_name, gts, variant_id))'''))
    
    session.execute(SimpleStatement('''CREATE TABLE IF NOT EXISTS samples_by_variants_gt_type ( \
                    variant_id int, \
                    gt_type int, \
                    sample_name text, \
                    PRIMARY KEY (variant_id, gt_type, sample_name))'''))
    
    session.execute(SimpleStatement('''CREATE TABLE if not exists vcf_header (vcf_header text PRIMARY KEY)'''))
    
    session.execute(SimpleStatement('''CREATE TABLE if not exists variants_by_sub_type_call_rate ( \
                        variant_id int, \
                        sub_type text, \
                        call_rate float, \
                        PRIMARY KEY (sub_type, call_rate, variant_id))'''))
     
    session.execute(SimpleStatement('''CREATE TABLE if not exists variants_by_chrom_start( \
                        chrom text,
                        start int,
                        variant_id int, \
                        primary key (chrom, start, variant_id))'''))     
    
    session.execute(SimpleStatement('''CREATE TABLE if not exists variants_by_gene ( \
                        variant_id int, \
                        gene text,
                        PRIMARY KEY (gene, variant_id))'''))
    
    session.execute(SimpleStatement('''CREATE TABLE if not exists sample_genotype_counts ( \
                     sample_id int PRIMARY KEY, \
                     version int,                                   \
                     num_hom_ref int,                                 \
                     num_het int,                                     \
                     num_hom_alt int,                                 \
                     num_unknown int)'''))
     
    
    session.execute(create_variants_table(gt_column_names))
    
    for stmt in create_samples_tables(extra_sample_columns):
        session.execute(stmt)

def create_variants_table(gt_column_names):

    #TODO: line 230 was hwe decimal(9,7) in sqlite and info was BYTEA
    #Also changed real -> float and numeric to float
    placeholders = ",".join(list(repeat("%s",len(gt_column_names))))
    creation =      '''CREATE TABLE if not exists variants  (   \
                    chrom text,                                 \
                    start int,                                  \
                    \"end\" int,                                \
                    vcf_id text,                                \
                    variant_id int PRIMARY KEY,            \
                    anno_id int,                                \
                    ref text,                                   \
                    alt text,                                   \
                    qual float,                                 \
                    filter text,                                \
                    type text,                                  \
                    sub_type text,                              \
                    call_rate float,                            \
                    in_dbsnp int,                               \
                    rs_ids text ,                               \
                    sv_cipos_start_left int,                    \
                    sv_cipos_end_left int,                      \
                    sv_cipos_start_right int,                   \
                    sv_cipos_end_right int,                     \
                    sv_length int,                              \
                    sv_is_precise boolean,                      \
                    sv_tool text,                               \
                    sv_evidence_type text,                      \
                    sv_event_id text,                           \
                    sv_mate_id text,                            \
                    sv_strand text,                             \
                    in_omim int,                                \
                    clinvar_sig text,                           \
                    clinvar_disease_name text,                  \
                    clinvar_dbsource text,                      \
                    clinvar_dbsource_id text,                   \
                    clinvar_origin text,                        \
                    clinvar_dsdb text,                          \
                    clinvar_dsdbid text,                        \
                    clinvar_disease_acc text,                   \
                    clinvar_in_locus_spec_db int,               \
                    clinvar_on_diag_assay int,                  \
                    clinvar_causal_allele text,                 \
                    pfam_domain text,                           \
                    cyto_band text,                             \
                    rmsk text,                                  \
                    in_cpg_island boolean,                      \
                    in_segdup boolean,                          \
                    is_conserved boolean,                       \
                    gerp_bp_score float,                        \
                    gerp_element_pval float,                    \
                    num_hom_ref int,                            \
                    num_het int,                                \
                    num_hom_alt int,                            \
                    num_unknown int,                            \
                    aaf float,                                \
                    hwe float,                                \
                    inbreeding_coeff float,                     \
                    pi float,                                   \
                    recomb_rate float,                          \
                    gene text,                                  \
                    transcript text,                            \
                    is_exonic int,                              \
                    is_coding int,                              \
                    is_lof int,                                 \
                    exon text,                                  \
                    codon_change text,                          \
                    aa_change text,                             \
                    aa_length text,                             \
                    biotype text,                               \
                    impact text,                                \
                    impact_so text,                             \
                    impact_severity text,                       \
                    polyphen_pred text,                         \
                    polyphen_score float,                       \
                    sift_pred text,                             \
                    sift_score float,                           \
                    anc_allele text,                            \
                    rms_bq float,                               \
                    cigar text,                                 \
                    depth int,                                  \
                    strand_bias float,                          \
                    rms_map_qual float,                         \
                    in_hom_run int,                             \
                    num_mapq_zero int,                          \
                    num_alleles int,                            \
                    num_reads_w_dels float,                     \
                    haplotype_score float,                      \
                    qual_depth float,                           \
                    allele_count int,                           \
                    allele_bal float,                           \
                    in_hm2 int,                                 \
                    in_hm3 int,                                 \
                    is_somatic int,                             \
                    somatic_score float,                        \
                    in_esp boolean,                             \
                    aaf_esp_ea float,                           \
                    aaf_esp_aa float,                           \
                    aaf_esp_all float,                          \
                    exome_chip boolean,                         \
                    in_1kg boolean,                             \
                    aaf_1kg_amr float,                          \
                    aaf_1kg_eas float,                          \
                    aaf_1kg_sas float,                          \
                    aaf_1kg_afr float,                          \
                    aaf_1kg_eur float,                          \
                    aaf_1kg_all float,                          \
                    grc text,                                   \
                    gms_illumina float,                         \
                    gms_solid float,                            \
                    gms_iontorrent float,                       \
                    in_cse boolean,                             \
                    encode_tfbs text,                           \
                    encode_dnaseI_cell_count int,               \
                    encode_dnaseI_cell_list text,               \
                    encode_consensus_gm12878 text,              \
                    encode_consensus_h1hesc text,               \
                    encode_consensus_helas3 text,               \
                    encode_consensus_hepg2 text,                \
                    encode_consensus_huvec text,                \
                    encode_consensus_k562 text,                 \
                    vista_enhancers text,                       \
                    cosmic_ids text,                            \
                    info blob,                                  \
                    cadd_raw float,                             \
                    cadd_scaled float,                          \
                    fitcons float,                              \
                    in_exac boolean,                            \
                    aaf_exac_all float,                       \
                    aaf_adj_exac_all float,                   \
                    aaf_adj_exac_afr float,                   \
                    aaf_adj_exac_amr float,                   \
                    aaf_adj_exac_eas float,                   \
                    aaf_adj_exac_fin float,                   \
                    aaf_adj_exac_nfe float,                   \
                    aaf_adj_exac_oth float,                   \
                    aaf_adj_exac_sas float, {0})'''
    stmt = creation.format(placeholders) % tuple(gt_column_names)
    return SimpleStatement(stmt)

def create_samples_tables(extra_columns):
    creation = '''CREATE TABLE if not exists samples{0}(          \
                     sample_id int,                 \
                     family_id text,                             \
                     name text,                                 \
                     paternal_id text,                           \
                     maternal_id text,                           \
                     sex text,                                  \
                     phenotype text, {1})'''
    optional = " text,".join(extra_columns + ['PRIMARY KEY{0}'])
    
    creation_samples = creation.format("", optional.format('(name, sample_id)'))
    creation_samples_by_phenotype = creation.format("_by_phenotype", optional.format('(phenotype, name)'))
    creation_samples_by_sex = creation.format("_by_sex", optional.format('(sex, name)'))
    
    return [SimpleStatement(creation_samples), SimpleStatement(creation_samples_by_phenotype), SimpleStatement(creation_samples_by_sex)]
    
def batch_insert(session, table, columns, contents, queue_length=120):
    """
    Populate the given table with the given values
    """
    column_names = ','.join(columns)
    question_marks = ','.join(list(repeat("?",len(columns))))
    insert_query = session.prepare('INSERT INTO ' + table + ' (' + column_names + ') VALUES (' + question_marks + ')')
    
    execute_concurrent_with_args(session, insert_query, contents)
    
def insert(session, table, columns, contents):
    column_names = ','.join(columns)
    placeholders = ','.join(list(repeat("%s",len(columns))))
    insert_query = 'INSERT INTO ' + table + ' (' + column_names + ') VALUES (' + placeholders + ')'
    session.execute(insert_query, contents)

def update_gene_summary_w_cancer_census(session, genes):
    update_qry = "UPDATE gene_summary SET in_cosmic_census = ? "
    update_qry += " WHERE gene = ? and chrom = ?"
    query = session.prepare(update_qry)
    batch = BatchStatement()
    for gene in genes:
        batch.add(query, gene)
    session.execute(batch)

# @contextlib.contextmanager
# def database_transaction(db):
#     conn = sqlite3.connect(db)
#     conn.isolation_level = None
#     session = conn.session()
#     session.execute('PRAGMA synchronous = OFF')
#     session.execute('PRAGMA journal_mode=MEMORY')
#     yield session
#     conn.commit
#     session.close()
