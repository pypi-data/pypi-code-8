import subprocess
import sys
import textwrap
import time
import shutil
import os
import glob
import platform

import numpy as np

from itertools import izip

import parabam
import pysam
import argparse

import simulator

######################################################################
##
##      Create a length estimate given a telbam or group of telbams.
##
##      Author: jhrf
##
######################################################################

class ReadLogic(object):
    #These methods are used in various places
    #notably merecat-tools simulate and split

    def get_read_type(self,read1,read2):
        comps = map( lambda alig: alig.cigar == [(0,len(alig.seq))] , (read1,read2) )
        if all(comps):
            #Reads both completely mapped to reference are true telomere
            return "F1"
        elif any(comps):
            #One read not complete, test if it's on the telomere boundary
            return self.__check_orientation__(*self.__order_reads_by_strand__(read1,read2))
        else:
            return "F3"

    def __check_orientation__(self,pos_strand_read,neg_strand_read):
        #This function is only called when at least one read was 
        #completely mapped to the telomeric reference
        if neg_strand_read.cigar == [(0,len(neg_strand_read.seq))]:
            #Wrong end is complete! This is a TTAGGG read (originally), 
            #We know that this read originated from an ITS region or
            #malformed proximal telomere
            return "F4"
        else:
            #This read may be on the boundary, or could be the opposite
            #side of an interestitial read.
            return "F2"

    def __order_reads_by_strand__(self,read1,read2):
        #This function requires at least one mapped read
        unclassified = None
        operation = None
        ordered = []
        for read in (read1,read2):
            if read.is_unmapped:
                unclassified = read
            else:
                if read.is_reverse:
                    operation = "append"
                    ordered.append(read)
                else:
                    operation = "insert"
                    ordered.insert(0,read)
        
        if unclassified:
            if operation == "append":
                ordered.insert(0,unclassified)
            else:
                ordered.append(unclassified)

        return tuple(ordered)


class Interface(parabam.core.Interface):
    def __init__(self,temp_dir):
        super(Interface,self).__init__(temp_dir)
        self._compliments = {"A":"T","T":"A","C":"G","G":"C","N":"N"}

    def run_cmd(self,parser):
        cmd_args = parser.parse_args()
        self.run(input_paths = cmd_args.input,
            total_procs = cmd_args.p,
            task_size = cmd_args.s,
            reader_n = cmd_args.f,
            verbose = cmd_args.v,
            keep = cmd_args.k,
            output = cmd_args.out,
            announce=True)

    def run(self,input_paths,total_procs,task_size,verbose,output,reader_n,
        keep=False,alig_params=None,announce=False):
        
        if not verbose:
            announce = False
        self.verbose = verbose
        program_name = "telomerecat telbam2length"
        self.__introduce__(program_name,announce)

        names = map(lambda b: self.__get_basename__(b),input_paths)
        names = map(lambda nm: nm.replace("_telbam",""),names)
        
        output_csv_path = self.__create_output_file__(output)

        for sample_path,sample_name in izip(input_paths,names):
            length_counts = self.__run_length_estimation__(sample_path,
                                           sample_name,
                                           total_procs,
                                           task_size,
                                           reader_n,
                                           keep)
            self.__write_to_csv__(length_counts,output_csv_path,sample_name)

        self.__goodbye__(program_name,announce)
        self.__copy_out_of_temp__([output_csv_path])

    def __run_length_estimation__(self,sample_path,sample_name,total_procs,task_size,reader_n,keep):
        self.__output__("[Status] Starting Length Estimatation process for %s\n" % (sample_name))
            
        self.__output__("[Status] Generating FASTQ from Telbam\n")
        fastq_paths = self.__bam_to_fastq__(sample_path)
        
        self.__output__("[Status] Aligning reads to telomeric reference\n")
        telref_path_sam = self.__get_telref_path__(sample_path,".sam")
        
        self.__run_telref_aligner__(telref_path_sam,fastq_paths,total_procs)         
        
        telref_path_bam = self.__get_telref_path__(sample_path,".bam")
        self.__sam_to_bam__(telref_path_sam,telref_path_bam,sample_path)
        os.remove(telref_path_sam)

        self.__output__("[Status] Analysing results of alignment to telref\n")
        length_counts = self.__get_length_counts__(telref_path_bam,task_size,total_procs,reader_n)

        self.__output__("[Status] Using simulation approach to estimate length\n")
        self.__output__("\n")

        simulation_results = self.__run_simulation__(sample_path,length_counts,total_procs)
        length_counts.update(simulation_results)

        if keep:
            self.__copy_out_of_temp__([telref_path_bam,fastq_paths[0],fastq_paths[1]])
        else:
            map( lambda path: os.remove(path), fastq_paths )
            os.remove(telref_path_bam)

        return length_counts

    def __create_output_file__(self,output):
        if output:
            unqiue_file_ID = output
        else:
            unqiue_file_ID = "telomerecat_length_%d.csv" % (time.time(),)

        output_csv_path = os.path.join(self._temp_dir,unqiue_file_ID)
        with open(output_csv_path,"w") as total:
            header = "Sample,F1,F2,F4,Uncertainty,Insert_mean,Insert_sd,Length\n"
            total.write(header)
        return output_csv_path

    def __output__(self,outstr):
        if self.verbose:
            sys.stdout.write(outstr)
            sys.stdout.flush()

    def __write_to_csv__(self,length_counts,output_csv_path,name):
        with open(output_csv_path,"a") as counts:
            counts.write("%s,%d,%d,%d,%.3f,%.3f,%.3f,%d\n" %\
                (name,
                length_counts["F1"],
                length_counts["F2"],
                length_counts["F4"],
                length_counts["uncertainty"],
                length_counts["insert_mean"],
                length_counts["insert_sd"],
                length_counts["length"]))

    def __sam_to_bam__(self,sam_path,bam_path,template_path):
        sam_file = pysam.AlignmentFile(sam_path,"r")

        master = pysam.AlignmentFile(template_path,"rb")
        bam_file = pysam.AlignmentFile(bam_path,"wb",template=master)
        master.close()

        for read in sam_file.fetch(until_eof=True):
            bam_file.write(read)

        sam_file.close()
        bam_file.close()

    def __run_simulation__(self,telbam_path,length_counts,total_procs):
        total_F2 = length_counts["F2"]
        total_f1 = length_counts["F1"]
        read_length = length_counts["read_length"]

        insert_mean,insert_sd = self.__insert_size_from_header__(telbam_path)

        len_mean,len_std = simulator.run_simulator_par(insert_mean,insert_sd,
                                                       total_f1,total_F2,
                                                       total_procs,read_length,N=16)
        len_mean = int(len_mean)

        return {"insert_mean":insert_mean,
                "insert_sd":insert_sd,
                "length":len_mean,
                "uncertainty":len_std}
        
    def __insert_size_from_header__(self,telbam_path):
        telbam_object = pysam.Samfile(telbam_path,"rb")
        header = telbam_object.header
        telbam_object.close()
        try:
            for comment in header["CO"]:
                comment_part = comment.partition(":")
                if comment_part[0] == "insert_mean,insert_sd":
                    comment_subpart = comment_part[2].partition(",")
                    insert_mean,insert_sd = (float(comment_subpart[0]),float(comment_subpart[2]))
                    return insert_mean,insert_sd
        except KeyError:
            #We couldn't find a header entry specifying insert_size
            pass
        sys.stderr.write("[Warning] TELBAM header malformed.\n\t"\
            "Using default mean and sd insert size for estimation algorithm.\n")
        return (325,20)

    def __get_length_counts__(self,telref_path,task_size,total_procs,reader_n):

        def engine(reads,constants,parent):
            read_logic = constants["read_logic"]
            read_type = read_logic.get_read_type(*reads)

            readlen_max = max( [ len(read.seq) for read in reads ]  )

            return {read_type:{"result":1},
                    "readlen_max":{"result":readlen_max}}

        constants = {"read_logic":ReadLogic()}
        structures = {"F1":{"data":0,"store_method":"cumu"},
                      "F2":{"data":0,"store_method":"cumu"},
                      "F4":{"data":0,"store_method":"cumu"},
                      "F3":{"data":0,"store_method":"cumu"},
                      "readlen_max":{"data":0,"store_method":"max"}
                      }


        interface = parabam.command.stat.Interface(self._temp_dir)
        output_files = interface.run(input_bams=[telref_path],
                            total_procs = total_procs,
                            reader_n = reader_n,
                            task_size = task_size,
                            user_constants = constants,
                            user_engine = engine,
                            user_struc_blueprint = structures,
                            keep_in_temp = True,#TODO: insert csv not staying in temp
                            pair_process = True)

        return self.__parabam_results_to_dict__(output_files["global"][0])

    def __parabam_results_to_dict__(self,csv_path):
        results_array = np.genfromtxt(csv_path,
                                    delimiter=",",
                                    names=True,
                                    dtype=("S256",float,float,float,float,float))

        called_F2 = results_array["F2"].tolist()
        called_F4 = results_array["F4"].tolist()

        total_F1 = results_array["F1"].tolist()
        total_F2 = called_F2 - called_F4 #Half the called_F2s actually
                                         #came from F4 regions. Normalise
                                         #by subtracting F4 

        total_F4 = called_F4 * 2 #Inflate F4 reads to 
                                 #adjust for F4s wrongly
                                 #called F2 reads.

        read_length = results_array["readlen_max"]

        return {"F1":int(total_F1),"F4":int(total_F4),
                "F2":int(total_F2),
                "called_F2":int(called_F2),
                "read_length":read_length}

    def __copy_out_of_temp__(self,file_nms,copy_path="."):
        map(lambda fil: shutil.copy(fil,copy_path),file_nms)

    def __get_telref_path__(self,path,path_ext=".bam"):
        root,filename = os.path.split(path)
        head,ext = os.path.splitext(filename)
        head = head.replace("_telbam","")
        return os.path.join(self._temp_dir,"%s_telref%s" % (head,path_ext,))

    def __pysam_read_fq__(self,read):
        read_num = 1 if read.is_read1 else 2
        seq = read.seq
        qual = read.qual
        if read.is_reverse:
            seq,qual = self.__flip_and_compliment__(read)
        fqStr = ("@%s/%d\n" % (read.qname,read_num) +
                "%s\n" % (seq,)+
                "+\n" + 
                "%s\n" % (qual,)
                )
        return (read_num,fqStr)

    def __flip_and_compliment__(self,read):
        seq_compliment = map(lambda base: self._compliments[base],read.seq)
        seq_compliment = "".join(seq_compliment)
        return(seq_compliment[::-1],read.qual[::-1])

    def __bam_to_fastq__(self,master_file_path):
        fastq_paths = self.__get_fastq_paths__(master_file_path,self._temp_dir)
        output_paths = [open(fastq_paths[0],"w"),open(fastq_paths[1],"w")]
        master = pysam.Samfile(master_file_path,"rb")
        
        loners = {}

        for i,alig in enumerate(master.fetch(until_eof=True)):
            if alig.qname in loners:
                if not alig.is_secondary:
                    mate = loners[alig.qname]

                    if mate.is_read1 == alig.is_read1:
                        continue

                    fastqised = map(self.__pysam_read_fq__,(alig,mate))
                    for (read_num,read) in fastqised:
                        output_paths[read_num-1].write(read)
                        output_paths[read_num-1].flush()
                    del loners[alig.qname]
            else:
                if not alig.is_secondary:
                    loners[alig.qname] = alig

        del loners
        
        map(lambda o: o.close(),output_paths)
        return (fastq_paths)

    def __get_fastq_paths__(self,bam_path,temp_dir="."):
        template = os.path.basename(bam_path)
        template = template.replace(".bam","")
        return ["%s/%s-%d.fq" % (temp_dir,template,i+1,) for i in range(2)]

    #Here we align the fastq files against a telomeric referene
    def __run_telref_aligner__(self,tel_ref_path,fastq_paths,proc):
        bowtie2 = self.__get_bowtie2_binary_path__()
        reference_path = self.__get_telomere_ref_path__()
        call_string = "--mp 17 -p %d -x %s -1 %s -2 %s -S %s" %\
            (proc,reference_path,fastq_paths[0],fastq_paths[1],tel_ref_path)
        
        return_code = subprocess.call([bowtie2,call_string],stderr=open(os.devnull, 'wb'))
        return return_code

    def __get_telomerecat_dir__(self):
        if hasattr(sys,"_MEIPASS"):
            #find the correct bath when bundeled by pyinstaller
            return sys._MEIPASS
        else:
            return os.path.dirname(__file__)

    def __get_bowtie2_dir__(self,telomerecat_dir):
        if platform.system() == "Darwin":
            sys_tag = "macos"
        elif platform.system() == "Linux":
            sys_tag = "linux"

        bowtie_search = "bowtie2*%s*" % (sys_tag,)
        return glob.glob(os.path.join(telomerecat_dir,bowtie_search))[0]

    def __get_bowtie2_binary_path__(self):

        bowtie2_dir = self.__get_bowtie2_dir__(self.__get_telomerecat_dir__())
        return os.path.join(bowtie2_dir,"bowtie2")

    def __get_telomere_ref_path__(self):
        telomerecat_dir = self.__get_telomerecat_dir__()
        return os.path.join(telomerecat_dir,"telomere_reference","telomere.fa")

    def get_parser(self):
        parser = self.default_parser()
        parser.description = textwrap.dedent(
        '''\
        telomerecat telbam2length
        ----------------------------------------------------------------------

            The telbam2length command allows the user to genereate a telomere
            length estimate from a previously generated TELBAM file.

            Example useage:

            telomerecat telbam2length /path/to/some_telbam.bam

            This will generate a .csv file with an telomere length estimate
            for the `some_telbam.bam` file.

        ----------------------------------------------------------------------
        ''')

        parser.add_argument('input',metavar='TELBAM(S)', nargs='+',
            help="The telbam(s) that we wish to analyse")
        parser.add_argument('--out',metavar='CSV',nargs='?',type=str,default="",
            help="Specify the name of the .csv output file")
        parser.add_argument('-k',action="store_true",default=False
            ,help="Retain fastq and telref files created by analysis")
        parser.add_argument('-v',choices=[0,1,2],default=0,type=int,
            help="Verbosity. The amount of information output by the program:\n"\
            "\t0: Silent [Default]\n"\
            "\t1: Output\n"\
            "\t2: Detailed Output")

        return parser

if __name__ == "__main__":
    print "Do not run this script directly. Type `telomerecat` for help."
