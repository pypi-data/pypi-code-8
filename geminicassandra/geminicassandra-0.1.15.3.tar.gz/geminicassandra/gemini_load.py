#!/usr/bin/env python

# native Python imports
import os.path
import sys

import annotations
import subprocess
#from cluster_helper.cluster import cluster_view
from gemini_load_chunk import GeminiLoader
import time
from cluster_helper.cluster import cluster_view


def load(parser, args):
    #if (args.db is None or args.vcf is None):
    if args.vcf is None:
        parser.print_help()
        exit("ERROR: load needs both a VCF file\n")
    
    start_time = time.time()
    annos = annotations.get_anno_files( args )
    # force skipping CADD and GERP if the data files have not been installed
    if args.skip_cadd is False:
        if 'cadd_score' not in annos:
            sys.stderr.write("\nCADD scores are not being loaded because the"
            " annotation file could not be found.\n"
            "`Run geminicassandra update --dataonly --extra cadd_score`"
            " to install the annotation file.\n\n")
            args.skip_cadd = True
        else:
            sys.stderr.write("CADD scores are being loaded (to skip use:--skip-cadd).\n")
    if args.skip_gerp_bp is False:
        if 'gerp_bp' not in annos:
            sys.stderr.write("\nGERP per bp is not being loaded because the annotation file"
                        " could not be found.\n    Run `geminicassandra update --dataonly --extra gerp_bp`"
                        " to install the annotation file.\n\n")
            args.skip_gerp_bp = True
        else:
            sys.stderr.write("GERP per bp is being loaded (to skip use:--skip-gerp-bp).\n")
    # collect of the the add'l annotation files
    annotations.load_annos( args )
    
    gemini_loader = GeminiLoader(args)
    gemini_loader.setup_db()
    time_2 = time.time()
    gemini_loader.single_core_stuff()
    time_3 = time.time()
    
    if args.scheduler:
        #load_ipython(args)
        sys.stdout.write("Just testing, no fancy scheduler stuff available yet")
    elif args.cores > 1:
        load_multicore(args)
    else:
        load_singlecore(args)
    end_time = time.time()
    total_time = str(end_time - start_time)
    db_creation_time = str(time_2 - start_time)
    single_core_time = str(time_3 - time_2)
    parallel_time = str(end_time - time_3)
    print "Finished loading in %s s" % total_time
    if args.timing_log != None:
        with open(args.timing_log, "a") as myfile:
            myfile.write(",".join([args.exp_id, total_time, db_creation_time, single_core_time, parallel_time]) + "\n")        

def load_singlecore(args):
    # create a new geminicassandra loader and populate
    # the geminicassandra db and files from the VCF
    gemini_loader = GeminiLoader(args)
    gemini_loader.connect_to_db()
    if not args.no_genotypes and not args.no_load_genotypes:
        gemini_loader._init_sample_gt_counts()
        
    gemini_loader.populate_from_vcf()


    '''if not args.skip_gene_tables and not args.test_mode:
        gemini_loader.update_gene_table()'''
    
    if not args.no_genotypes and not args.no_load_genotypes:
        gemini_loader.store_sample_gt_counts()
    if not args.test_mode:
        gemini_loader.disconnect()
        
    #geminicassandra.add_extras(args.db, [args.db])

def load_multicore(args):
    grabix_file = bgzip(args.vcf)
    load_chunks_multicore(grabix_file, args)
    # geminicassandra.add_extras(args.db, chunks)


def load_ipython(args):
    grabix_file = bgzip(args.vcf)
    with cluster_view(*get_ipython_args(args)) as view:
        chunks = load_chunks_ipython(grabix_file, args, view)
    # geminicassandra.add_extras(args.db, chunks)


def get_chunk_name(chunk):
    return "--chunkdb " + chunk

def load_chunks_multicore(grabix_file, args):
    cores = args.cores

    # specify the PED file if given one
    ped_file = ""
    if args.ped_file is not None:
        ped_file = "-p " + args.ped_file

    # specify the annotation type if given one
    anno_type = ""
    if args.anno_type is not None:
        anno_type = "-t " + args.anno_type

    no_genotypes = ""
    if args.no_genotypes is True:
        no_genotypes = "--no-genotypes"

    no_load_genotypes = ""
    if args.no_load_genotypes is True:
        no_load_genotypes = "--no-load-genotypes"

    skip_gerp_bp = ""
    if args.skip_gerp_bp is True:
        skip_gerp_bp = "--skip-gerp-bp"

    skip_gene_tables = ""
    if args.skip_gene_tables is True:
        skip_gene_tables = "--skip-gene-tables"

    skip_cadd = ""
    if args.skip_cadd is True:
        skip_cadd = "--skip-cadd"
    
    test_mode = ""
    if args.test_mode is True:
        test_mode = "--test-mode"

    passonly = ""
    if args.passonly is True:
        passonly = "--passonly"

    skip_info_string = ""
    if args.skip_info_string is True:
        skip_info_string = "--skip-info-string"
        
    contact_points = "-db " + args.contact_points 
    keyspace = "-ks " + args.keyspace
    buffer_size = "--buffer-size " + str(args.buffer_size)
    max_queue = "--max_queue " + str(args.max_queue)
    
    submit_command = "{cmd}"
    vcf, _ = os.path.splitext(grabix_file)
    chunk_steps = get_chunk_steps(grabix_file, args)
    chunk_vcfs = []
    procs = []

    for chunk_num, chunk in chunk_steps:
        start, stop = chunk
        gemini_load = gemini_pipe_load_cmd().format(**locals())
        procs.append(subprocess.Popen(submit_command.format(cmd=gemini_load),
                                      shell=True))

        chunk_vcf = vcf + ".chunk" + str(chunk_num)
        chunk_vcfs.append(chunk_vcf)

    wait_until_finished(procs)
    print "Done loading {0} variants in {1} chunks.".format(stop, chunk_num+1)

def load_chunks_ipython(grabix_file, args, view):
    # specify the PED file if given one
    ped_file = ""
    if args.ped_file is not None:
        ped_file = "-p " + args.ped_file

    # specify the annotation type if given one
    anno_type = ""
    if args.anno_type is not None:
        anno_type = "-t " + args.anno_type

    no_genotypes = ""
    if args.no_genotypes is True:
        no_genotypes = "--no-genotypes"

    no_load_genotypes = ""
    if args.no_load_genotypes is True:
        no_load_genotypes = "--no-load-genotypes"

    skip_gerp_bp = ""
    if args.skip_gerp_bp is True:
        skip_gerp_bp = "--skip-gerp-bp"

    skip_gene_tables = ""
    if args.skip_gene_tables is True:
        skip_gene_tables = "--skip-gene-tables"
    
    skip_cadd = ""
    if args.skip_cadd is True:
        skip_cadd = "--skip-cadd"
    
    test_mode = ""
    if args.test_mode is True:
        test_mode = "--test-mode"

    passonly = ""
    if args.passonly is True:
        passonly = "--passonly"
        
    contact_points = "-db \"" + args.contact_points + "\""
    keyspace = "-ks \"" + args.keyspace + "\""
    buffer_size = "--buffer-size " + args.buffer_size 

    skip_info_string = ""
    if args.skip_info_string is True:
        skip_info_string = "--skip-info-string"


    vcf, _ = os.path.splitext(grabix_file)
    chunk_steps = get_chunk_steps(grabix_file, args)
    total_chunks = len(chunk_steps)
    scheduler, queue, cores = get_ipython_args(args)
    load_args = {"ped_file": ped_file,
                 "anno_type": anno_type,
                 "vcf": vcf,
                 "grabix_file": grabix_file,
                 "no_genotypes": no_genotypes,
                 "no_load_genotypes": no_load_genotypes,
                 "skip_gerp_bp": skip_gerp_bp,
                 "skip_gene_tables": skip_gene_tables,
                 "skip_cadd": skip_cadd,
                 "test_mode": test_mode,
                 "passonly": passonly,
                 "skip_info_string": skip_info_string,
                 "contact_points": contact_points,
                 "keyspace": keyspace}    
    chunk_dbs = view.map(load_chunk, chunk_steps, [load_args] * total_chunks)

    print "Done loading variants in {0} chunks.".format(total_chunks)
    return chunk_dbs

def load_chunk(chunk_step, kwargs):
    chunk_num, chunk = chunk_step
    start, stop = chunk
    args = combine_dicts(locals(), kwargs)
    gemini_load = gemini_pipe_load_cmd().format(**args)
    subprocess.check_call(gemini_load, shell=True)
    chunk_db = args["vcf"] + ".chunk" + str(chunk_num) + ".db"
    return chunk_db

def wait_until_finished(procs):
    [p.wait() for p in procs]

def gemini_pipe_load_cmd():
    grabix_cmd = "grabix grab {grabix_file} {start} {stop}"
    gemini_load_cmd = ("geminicassandra load_chunk -v - {anno_type} {ped_file}"
                       " {no_genotypes} {no_load_genotypes} {no_genotypes}"
                       " {skip_gerp_bp} {skip_gene_tables} {skip_cadd}"
                       " {passonly} {skip_info_string} {test_mode}"
                       " -o {start} {contact_points} {keyspace} {buffer_size} {max_queue}")
    return " | ".join([grabix_cmd, gemini_load_cmd])

def get_chunk_steps(grabix_file, args):
    index_file = grabix_index(grabix_file)
    num_lines = get_num_lines(index_file)
    print "Importing %d variants." % num_lines
    chunk_size = int(num_lines) / int(args.cores)
    print "Breaking {0} into {1} chunks.".format(grabix_file, args.cores)

    starts = []
    stops = []
    for chunk in range(0, int(args.cores)):
        start = (chunk * chunk_size) + 1
        stop  = start + chunk_size - 1
        # make sure the last chunk covers the remaining lines
        if chunk >= (args.cores - 1) and stop < num_lines:
            stop = num_lines
        starts.append(start)
        stops.append(stop)
    return list(enumerate(zip(starts, stops)))

def get_num_lines(index_file):
    with open(index_file) as index_handle:
        index_handle.next()
        num_lines = int(index_handle.next().strip())
    print "Loading %d variants." % (num_lines)
    return num_lines

def grabix_index(fname):
    if not which("grabix"):
        print_cmd_not_found_and_exit("grabix")
    index_file = fname + ".gbi"
    if file_exists(index_file):
        return index_file
    print "Indexing {0} with grabix.".format(fname)
    subprocess.check_call("grabix index {fname}".format(fname=fname), shell=True)
    return index_file

def bgzip(fname):

    if not which("bgzip"):
        print_cmd_not_found_and_exit("bgzip")

    if is_gz_file(fname):
        return fname

    vcf_time = os.path.getmtime(fname)
    bgzip_file = fname + ".gz"

    if not file_exists(bgzip_file) or \
       (file_exists(bgzip_file) and os.path.getmtime(bgzip_file) < vcf_time):
        print "Bgzipping {0} into {1}.".format(fname, fname + ".gz")
        subprocess.check_call("bgzip -c {fname} > \
                              {fname}.gz".format(fname=fname),
                              shell=True)
    elif file_exists(bgzip_file) and os.path.getmtime(bgzip_file) > vcf_time:
        print "Loading with existing bgzip ({0}) version of {1}.".format(fname + ".gz", fname)

    return bgzip_file


def is_gz_file(fname):
    _, ext = os.path.splitext(fname)
    if ext == ".gz":
        return True
    else:
        return False

def get_submit_command(args):
    return "{cmd}"


def file_exists(fname):
    """Check if a file exists and is non-empty.
    """
    return os.path.exists(fname) and os.path.getsize(fname) > 0

def which(program):
    """ returns the path to an executable or None if it can't be found
     http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
     """

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def combine_dicts(d1, d2):
    return dict(d1.items() + d2.items())

def get_ipython_args(args):
    return (args.scheduler, args.queue, args.cores)

def print_cmd_not_found_and_exit(cmd):
    sys.stderr.write("Cannot find {cmd}, install it or put it in your "
                     "path.".format(cmd=cmd))
    exit(1)

def use_scheduler(args):
    return bool(args.scheduler)
