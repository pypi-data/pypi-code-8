#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

"""Download genome data from UCSC genome ftp site to local file system.

This is a module for downloading genome data from UCSC ftp site. The genome 
data can be specific assembly or most used reference (if available), the file 
can be in .2bit or .fa.gz format. The chromosome data can be in seperated .fa.
gz file for each chromosome or in a single tar.gz or .zip file contains all 
chromosomes (if available). 

This module can be considered a sample and excellent tool for downloading 
genomes data. It can be used both as a python module and a terminal tool.

For further information please look into the file README.txt or README.html!
If you have any questions or suggestions, please feel free to contact me:
email: fyuan4@uh.edu
GitHub: https://github.com/TinyNecessaryTools/Biology.git
"""

import os
import sys
import ftplib
import socket
import subprocess
import getopt

__version__ = "0.1.0"
__license__ = "MIT"
__author__ = "FEI YUAN"
__contact__ = "fyuan4@uh.edu"
__date__ = "2015-07-07"


host = 'hgdownload.cse.ucsc.edu'

TAXA_MAP = {  
    # common_name : (abbreviation, scientific_name)
    # Mammals
    "alpaca": ("vicPac", "Vicugna_pacos"),
    "armadillo": ("dasNov", "Dasypus_novemcinctus"),
    "baboon": ("papAnu", "Papio_anubis"),
    "bushbaby": ("otoGar", "Otolemur_garnettii"),
    "cat": ("felCat", "Felis_catus"),
    "chimp": ("panTro", "Pan_troglodytes"),
    "chinese hamster": ("criGri", "Cricetulus_griseus"),
    "cow": ("bosTau", "Bos_taurus"),
    "dog": ("canFam", "Canis_familiaris"),
    "dolphin": ("turTru", "Tursiops_truncatus"),
    "elephant": ("loxAfr", "Loxodonta_africana"),
    "ferret": ("musFur", "Mustela_putorius_furo"),
    "gibbon": ("nomLeu", "Nomascus_leucogenys"),
    "gorilla": ("gorGor", "Gorilla_gorilla_gorilla"),
    "guinea pig": ("cavPor", "Cavia_porcellus"),
    "hedgehog": ("eriEur", "Erinaceus_europaeus"),
    "horse": ("equCab", "Equus_caballus"),
    "human": ("hg", "Homo_sapiens"),
    "kangaroo rat": ("dipOrd", "Dipodomys_ordii"),
    "manatee": ("triMan", "Trichechus_manatus_latirostris"),
    "marmoset": ("calJac", "Callithrix_jacchus"),
    "megabat": ("pteVam", "Pteropus_vampyrus"),
    "microbat": ("myoLuc", "Myotis_lucifugus"),
    "minke whale": ("balAcu", "Balaenoptera_acutorostrata_scammoni"),
    "mouse": ("mm", "Mus_musculus"),
    "mouse lemur": ("micMur", "Microcebus_murinus"),
    "naked mole-rat": ("hetGla", "Heterocephalus_glaber"),
    "opossum": ("monDom", "Monodelphis_domestica"),
    "orangutan": ("ponAbe", "Pongo_abelii"),
    "panda": ("ailMel", "Ailuropoda_melanoleuca"),
    "pig": ("susScr", "Sus_scrofa"),
    "pika": ("ochPri", "Ochotona_princeps"),
    "platypus": ("ornAna", "Ornithorhynchus_anatinus"),
    "rabbit": ("oryCun", "Oryctolagus_cuniculus"),
    "rat": ("rn", "Rattus_norvegicus"),
    "rhesus": ("rheMac", "Rhesus_macaque"),
    "rock hyrax": ("proCap", "Procavia_capensis"),
    "sheep": ("oviAri", "Ovis_aries"),
    "shrew": ("sorAra", "Sorex_araneus"),
    "sloth": ("choHof", "Choloepus_hoffmanni"),
    "squirrel": ("speTri", "Spermophilus_tridecemlineatus"),
    "squirrel monkey": ("saiBol", "Saimiri_boliviensis"),
    "tarsier": ("tarSyr", "Tarsius_syrichta"),
    "tasmanian devil": ("sarHar", "Sarcophilus_harrisii"),
    "tenrec": ("echTel", "Echinops_telfairi"),
    "tree shrew": ("tupBel", "Tupaia_belangeri"),
    "wallaby": ("macEug", "Macropus_eugenii"),
    "white rhinoceros": ("cerSim", "Ceratotherium_simum"),
    # Vertebrates
    "american alligator": ("allMis", "Alligator_mississippiensis"),
    "atlantic cod": ("gadMor", "Gadus_morhua"),
    "budgerigar": ("melUnd", "Melopsittacus_undulatus"),
    "chicken": ("galGal", "Gallus_gallus"),
    "coelacanth": ("latCha", "Latimeria_chalumnae"),
    "elephant shark": ("calMil", "Callorhinchus_milii"),
    "fugu": ("fr", "Fugu_rubripes"),
    "lamprey": ("petMar", "Petromyzon_marinus"),
    "lizard": ("anoCar", "Anolis_carolinensis"),
    "medaka": ("oryLat", "Oryzias_latipes"),
    "medium ground finch": ("geoFor", "Geospiza_fortis"),
    "nile tilapia": ("oreNil", "Oreochromis_niloticus"),
    "painted turtle": ("chrPic", "Chrysemys_picta_bellii"),
    "stickleback": ("gasAcu", "Gasterosteus_aculeatus"),
    "tetraodon": ("tetNig", "Tetraodon_nigroviridis"),
    "turkey": ("melGal", "Meleagris_gallopavo"),
    "X. tropicalis": ("xenTro", "Xenopus_tropicalis"),
    "zebra finch": ("taeGut", "Taeniopygia_guttata"),
    "zebrafish": ("danRer", "Danio_rerio"),
    # Insects
    "A. gambiae": ("anoGam", "Anopheles_gambiae"),
    "A. mellifera": ("apiMel", "Apis_mellifera"),
    "D. ananassae": ("droAna", "Drosophila_ananassae"),
    "D. erecta": ("droEre", "Drosophila_erecta"),
    "D. grimshawi": ("droGri", "Drosophila_grimshawi"),
    "D. melanogaster": ("dm", "Drosophila_melanogaster"),
    "D. mojavensis": ("droMoj", "Drosophila_mojavensis"),
    "D. persimilis": ("droPer", "Drosophila_persimilis"),
    "D. pseudoobscura": ("dp", "Drosophila_pseudoobscura"),
    "D. sechellia": ("droSec", "Drosophila_sechellia"),
    "D. simulans": ("droSim", "Drosophila_simulans"),
    "D. virilis": ("droVir", "Drosophila_virilis"),
    "D. willistoni": ("droWil", "Drosophila_villistoni"),
    "D. yakuba": ("droYak", "Drosophila_yakuba"),
    "T. castaneum": ("triCas", "Tribolium_castaneum"),
    # Deuterostomes,
    "C. intestinalis": ("ci", "Ciona_intestinalis"),
    "lancelet": ("braFlo", "Branchiostoma_floridae"),
    "sea urchin": ("strPur", "Strongylocentrotus_purpuratus"),
    # Nematodes
    "C. brenneri": ("caePb", "Caenorhabditis_brenneri"),
    "C. briggsae": ("cb", "Caenorhabditis_briggsae"),
    "C. elegans": ("ce", "Caenorhabditis_elegans"),
    "C. japonica": ("caeJap", "Caenorhabditis_japonica"),
    "C. remanei": ("caeRem", "Caenorhabditis_remanei"),
    "P. pacificus": ("priPac", "Pristionchus_pacificus"),
    # Yeast and sea hare
    "yeast": ("sacCer", "Saccharomyces_cerevisiae"),
    "sea hare": ("aplCal", "Aplysia_californica"),
    # Viruses
    "ebola virus": ("eboVir", "Ebola_virus")
}

GROUP_MAP = {  
    # Mammals
    "Mammals": ("human", "mouse", "alpaca", "armadillo", "baboon", "bushbaby", "cat", "chimp", "chinese hamster", "cow", "dog", "dolphin", "elephant", "ferret", "gibbon", "gorilla", "guinea pig", "hedgehog", "horse", "kangaroo rat", "manatee", "marmoset", "megabat", "microbat", "minke whale", "mouse lemur", "naked mole-rat", "opossum", "orangutan", "panda", "pig", "pika", "platypus", "rabbit", "rat", "rhesus", "rock hyrax", "sheep", "shrew", "sloth", "squirrel", "squirrel monkey", "tarsier", "tasmanian devil", "tenrec", "tree shrew", "wallaby", "white rhinoceros"),

    # Vertebrates
    "Vertebrates": ("american alligator",  "atlantic cod",  "budgerigar",  "chicken",  "coelacanth",  "elephant shark",  "fugu",  "lamprey",  "lizard",  "medaka",  "medium ground finch",  "nile tilapia",  "painted turtle",  "stickleback",  "tetraodon",  "turkey",  "X. tropicalis",  "zebra finch",  "zebrafish"),

    # Insects
    "Insects": ("A. gambiae", "D. pseudoobscura", "A. mellifera", "D. sechellia", "D. ananassae", "D. simulans", "D. erecta", "D. virilis", "D. grimshawi", "D. willistoni", "D. melanogaster", "D. yakuba", "D. mojavensis", "T. castaneum", "D. persimilis"),

    # Nematodes
    "Nematodes": ("C. brenneri", "C. briggsae", "C. elegans", "C. japonica", "C. remanei", "P. pacificus"),

    # Deuterostomes,
    "Deuterostomes": ("C. intestinalis", "lancelet", "sea urchin"),

    # Yeast and others
    "Yeast": ("yeast", "sea hare"),

    # Viruses
    "Virus": ["ebola virus"]
}


def ftp_connection(host='', taxa='', genomedir='', email='', timeout=60*60):
    "Connect to a ftp site, change to assigned directory, if necessary"

    try:
        ftp = ftplib.FTP(host)
    except socket.gaierror:
        print('Can not reach to {0}, please chech the site or your internet connection!'.format(host))
        return

    if email:
        try:
            ftp.login('anonymous', email)
        except ftplib.error_perm:
            print 'Can not login anonymously'
            ftp.quit()
            return
    else:
        ftp.login()

    if genomedir and taxa:
        try:
            ftp.cwd(genomedir)
        except ftplib.error_perm:
            print('Wrong option\nYou may input a wrong taxa name: {0}\nOr UCSC ftp does not have genome for your taxa: {0}\n\nPlease consider the following ways:\n1) Please check your spell carefully\n2) Please check available genomes via "-g 1".\n'.format(taxa))
            ftp.quit()
            return
    return ftp


def taxa_convert(taxa='', assembly=''):
    """Convert taxa name and assembly name to required forms for the downstream call.

    Taxa can be common name, scientific name and assembly name.

    e.g. 
        common name: human, dog, cat, yeast, ...
        scientific name: Homo sapiens, Canis familiaris, ...
        assembly name: hg19, hg38, sacCer3, rehMac, bosTau, ...
    """

    if taxa:
        common_name = TAXA_MAP.keys()
        abbrevs = [v[0] for v in TAXA_MAP.values()]
        sci_name = [v[1].replace('_', ' ') for v in TAXA_MAP.values()]

        if assembly:
            if taxa in common_name:
                return (TAXA_MAP[taxa][0], True)
            elif taxa.strip('0123456789') in abbrevs:
                print('You already specified the genome assembly with {0}, the assembly argument will be ignored!'.format(taxa))
                return (taxa, True)
            elif taxa in sci_name:
                taxa = [v[0]
                        for v in TAXA_MAP.values() if taxa == v[1].replace('_', ' ')]
                return (taxa[0], True)
            else:
                print('Wrong taxa: {0}\n\nYou can consider the following ways:\n1) Please check you spell carefully!\n2) Please check available genomes via "-g 1".\n'.format(taxa))
                return ('', False)
        else:
            if taxa in common_name:
                return (TAXA_MAP[taxa][1], False)
            elif taxa.strip('0123456789') in abbrevs:
                return (taxa, True)
            elif taxa in sci_name:
                return (taxa.replace(' ', '_'), False)
            else:
                print('Wrong taxa: {0}\n\nYou can consider the following ways:\n1) Please check you spell carefully!\n2) Please check available genomes via "-g 1".\n'.format(taxa))
                return ('', False)
    else:
        return ('', False)


def genomes_available(group=''):
    """Prints out all available taxa or a group of available taxa.

    Group are supposed to be 1 (all available taxa), Mammals, Vertebrates, 
    Deuterostomes, Insects, Nematodes, Yeast, and Virus.

    When try to use group at the very beginning, you can assign part of them,
    (e.g. mam, inse, ver, deu, nem, yea, vir). It will match the according 
    group name and it's case insensitivity.

    However, once you made a mistake, it will show you a available list and 
    prompt you to input a group name, you should use the exact full name.
    """

    if not group:
        return

    groups = ['Mammals', 'Vertebrates', 'Deuterostomes',
              'Insects',  'Nematodes', 'Yeast', 'Virus']
    header = '|{0}|{1}|'.format(
        'Common Name'.center(20), 'Scientific Name'.center(36))
    if group == '1':
        title = 'UCSC genomes ({0})'.format(len(TAXA_MAP.values()))
        content = TAXA_MAP.keys()
    else:
        group = [i for i in groups if group.title() in i]
        if len(group) == 1:
            group = group[0]
        else:
            print('Wrong option!\nGroup only accept the following names:\n{0}'.format(
                '\n'.join(groups)))
            group = raw_input('Input q to quit or a group name to ccontinue: ')
            if group == 'q':
                return
            else:
                while group not in groups:
                    group = raw_input('Wrong choice! Please input q to quit or a name to continue: ')
                    if group == 'q':
                        return

        title = '{0} ({1} taxa available)'.format(group, len(GROUP_MAP[group]))
        content = GROUP_MAP[group]

    print('{0}'.format(59*'-'))
    print('| {0} |'.format(title.center(55)))
    print('{0}{1}{0}{2}{0}'.format('+', 20*'-', 36*'-', '+'))
    print(header)
    print('{0}{1}{0}{2}{0}'.format('+', 20*'-', 36*'-', '+'))
    for i in sorted(content):
        print('|{0}|{1}|'.format(
            i.center(20), TAXA_MAP[i][1].replace('_', ' ').center(36)))
        print('{0}{1}{0}{2}{0}'.format('+', 20*'-', 36*'-', '+'))


def genomes_assembly(taxa='', assembly=''):
    """Based on taxa name and assembly status, return available assembly's 
    path on ftp site"""

    if not taxa:
        return ('', '')

    genomedir = ''
    if assembly:
        if taxa[-1].isdigit():
            genomedir = '/'.join(['goldenPath', taxa, 'bigZips'])
            return (taxa, genomedir)
        else:
            ftp = ftp_connection(host, taxa)
            ftp.cwd('goldenPath')
            try:
                otus = ftp.nlst()
                ftp.quit()
            except Exception:
                return ('', genomedir)

            otus = [i for i in otus if i.startswith(taxa.strip('0123456789'))]
            if otus:
                print('Found {0} available genome assembly(s):\n{1}'.format(
                    len(otus), 79*'='))
                print('\n'.join(otus))
                print(79*'=')
                taxa = raw_input('Input q to quit or an assembly name to ccontinue: ')
                if taxa == 'q':
                    print('Goodbye!')
                    return ('', '')
                else:
                    genomedir = '/'.join(['goldenPath', taxa, 'bigZips'])
                    while taxa not in otus:
                        taxa = raw_input('Wrong choice! Please input q to quit or an assembly name to continue: ')
                        if taxa == 'q':
                            print('Goodbye!')
                            return ('', '')
                    genomedir = '/'.join(['goldenPath', taxa, 'bigZips'])
                return (taxa, genomedir)
            else:
                return ('', genomedir)
    else:
        genomedir = '/'.join(['goldenPath/currentGenomes', taxa.replace(' ', '_'), 'bigZips'])
        taxa = [v[0]
                for v in TAXA_MAP.values() if taxa == v[1].replace(' ', '_')]
        if taxa:
            taxa = taxa[0]

    return (taxa, genomedir)


def ftp_files(host, taxa, genomedir, email='', chrs='', formats=''):
    "Get and return available data's path on ftp site"

    if not taxa:
        return

    ftp = ftp_connection(host, taxa, genomedir, email)

    if not ftp:
        return

    if chrs:
        if str(chrs) == '1' or chrs == 1:
            try:
                ftp.cwd('../chromosomes')
            except Exception:
                print('The genome you request does not have this kind of file format!\nYou can try to download all chromosomes data were packed in a single tar.gz or zip file.\nIf you want to give a try, please assign chrs to 2 (-c 2).')
                return
            pwd = '/'.join(ftp.pwd().split('/')[3:])
            try:
                files = ftp.nlst('chr*.fa.gz')
            except Exception:
                print('The genome you request does not have this kind of file format!\nYou can try to download all chromosomes data were packed in a single tar.gz or zip file.\nIf you want to give a try, please assign chrs to 2 (-c 2).')
                return
            files = ['/'.join([pwd, i]) for i in files]
            ftp.quit()
        elif str(chrs) == '2' or chrs == 2:
            try:
                files = ftp.nlst('chromFa.*')
            except Exception:
                print('The genome you request does not have this kind of file format!\nYou can try to download chromosomes data were stored in sepreated files, each chromosome was stored in one single fa.gz file.\nIf you want to give a try, please assign chrs to 1 (-c 1).')
                return
            files = ['/'.join([genomedir, i]) for i in files]
            ftp.quit()
        else:
            files = ''
            print('You plan to download chromosome data, the possible formats only can be one of the following two:\n1) "1" - Seperated files, each chromosome in one fa.gz file;\n2) "2" - All chromosomes are packed in one single tar.gz or zip file.\nPlease assign chrs to either 1 or 2 (-c 1 or -c 2).')
    else:
        if formats:
            formats = formats
        else:
            formats = '2bit'
            try:
                files = ftp.nlst(taxa + '*.' + formats)
            except Exception:
                print('The genome you request does not have this kind of file format, try to download genome in fa.gz format(-f fa.gz)!')
                formats = 'fa.gz'
                try:
                    files = ftp.nlst(taxa + '*.' + formats)
                except Exception:
                    print('Very regret!\nCan not find any available genome for you, ucsc may not have genome for this taxa.\nRecommend you go to ucsc ftp site and double check!')
                    return
        try:
            files = ftp.nlst(taxa + '*.' + formats)
        except Exception:
            print('The genome you request does not have this kind of file format!\nIf you do not mind file format, please remove format option (-f) and try again.\nWe will do our best to find any available genomes for you!')
            return
        pwd = '/'.join(ftp.pwd().split('/')[3:])
        files = ['/'.join([pwd, i]) for i in files]
        ftp.quit()

    return files


def dirs(outdir):
    "Verify outdir or just set it to current directory"

    if not outdir:
        outdir = os.getcwd()

    if not os.path.exists(outdir):
        outdir = os.getcwd()
        print('The outdir you assigned does not exist, files will be stored to {0}'.format(outdir))
    return outdir

def cmds(method, taxa, files='', outdir=''):
    "Create commands for download functions"

    if not files:
        return
    
    prefix = {
        'rsync' : ('rsync://hgdownload.cse.ucsc.edu', 'rsync -P'),
        'wget' : ('ftp://hgdownload.cse.ucsc.edu', 'wget - O'),
        'ftp' : ('', 'RETR')
    }
    url = ['/'.join([prefix[method][0], i]) for i in files]
    fname = [os.path.basename(i) if os.path.basename(i).startswith(
        taxa.strip('0123456789')) else ''.join([taxa, os.path.basename(i)]) for i in url]
    outfiles = [os.path.join(dirs(outdir), i) for i in fname]
    if method == 'ftp':
        cmd = [' '.join([prefix[method][1], files[i]]) for i in range(len(files))]
        return (cmd, outfiles)
    else:
        cmd = [' '.join([prefix[method][1], url[i], outfiles[i]]) for i in range(len(url))]
        cmd = [i.split(' ') for i in cmd]
        return cmd

def rsync_download(host, taxa, files='', outdir=''):
    "Download data use rsync"
    cmd = cmds('rsync', taxa, files, outdir)
    if not cmd:
        return
    map(subprocess.call, cmd)
    print('\nDownload successfully! File(s) was stored in {0}'.format(dirs(outdir)))


def wget_download(host, taxa, files='', outdir=''):
    "Download data use wget"
    cmd = cmds('rsync', taxa, files, outdir)
    if not cmd:
        return
    map(subprocess.call, cmds('wget', taxa, files, outdir))
    print('\nDownload successfully! File(s) was stored in {0}'.format(dirs(outdir)))


def ftp_download(host, taxa, files='', outdir='', email=''):
    "Download data use ftplib"

    cmd, outfiles = cmds('ftp', taxa, files, outdir)

    if cmd:
        ftp = ftp_connection(host, taxa, email)
        ftp.sendcmd('TYPE i')
        size = [ftp.size(i) for i in files]

    class CallBack(object): 
        def __init__(self, size, f): 
            self.size = size 
            self.f = f 
            self.received = 0

        def __call__(self, data): 
            self.f.write(data) 
            self.received += len(data)
            percent = self.received/float(self.size)
            mark = '=' * int(round(100 * percent/2))
            sys.stdout.write('\r{0} [{1:50s}] {2:.2%} '.format(os.path.basename(self.f.name), mark, percent))
            sys.stdout.flush()

    [ftp.retrbinary(cmd[i], CallBack(size[i], open(outfiles[i], 'wb'))) for i in range(len(files))]
    ftp.quit()
    print('\nDownload successfully! File(s) was stored in {0}'.format(dirs(outdir)))


def genomes(group='', taxa='', assembly='', chrs='',  formats='', outdir='', email=''):
    """Very Import! Only this function can be safely used external!
    If you want to use this module in your script, this is the only function 
    you can directly and safely use via import pygenomes, you should avoid use 
    other functions.
    """
    
    genomes_available(group)
    if not taxa:
        return

    if taxa == '1':
        genomes_available(taxa)
    else:
        taxa, assembly = taxa_convert(taxa, assembly)

    taxa, genomedir = genomes_assembly(taxa, assembly)
    files = ftp_files(host, taxa, genomedir, email, chrs, formats)
    try:
        rsync_download(host, taxa, files, outdir)
    except OSError:
        try:
            wget_download(host, taxa, files, outdir)
        except OSError:
            try:
                ftp_download(host, taxa, files, outdir, email)
            except Exception:
                return


# command-line usage stuff

def show_version():
     "Print version message and terminate"

     program = 'pygenomes'
     print('{0} {1}'.format(program, __version__))
     sys.exit()


def shwo_usage():
    "Print usage message and terminate"

    program = 'pygenomes'
    copyrightYear = "2015"
    args = (program, __version__, __author__, __contact__, copyrightYear, __license__)
    print("\n{0} v.{1}, Copyleft by {2} ({3}), {4} ({5})".format(program, __version__, __author__, __contact__, copyrightYear, __license__))
    print("\nDownload genome data from UCSC genome ftp site to local file system")
    print("\nUSAGE: {0} [-hvgtacfoe]".format(program))
    print("""\
\nOPTIONS:

  -h --help         Prints this usage message and exits.

  -v --version      Prints version number and exists.

  -g --group        Prints available taxa by group name
                        1 - prints all available taxa 
                        group name - e.g. Mammals, Insects, Vertebrates.

  -t --taxa         Name of interested taxa 
                        1 - will show available taxa list
                        commmon name - e.g. human, yeast, cow;
                        scientific name - e.g. Homo sapiens;
                        genome assembly - e.g. hg19, hg38, sacCer3. 

  -a --assembly     Invoke specific genome assembly choose
                        0 - do not invoke genome assembly choose, default;
                        1 - interactive mode, will give a list and ask user 
                            to input a specific genome assembly.

  -c --chrs         Download chromosome data rather than genome data
                        0 - do not invoke chromosome data download, default;
                        1 - download chrosome data, each chromosome in a 
                            single fa.gz file, if available;
                        2 - download chromose data, all chromosomes data 
                            were packed in one .tar.gz or .zip file.

  -f --formats      Download genome data in specific format
                        2bit - default, if not available will try fa.gz;
                        fa.gz - optional format, if available.

  -o --outdir       Set output directory, absolute path; if not set, 
                    file(s) will be stored in current directory.

  -e --email        Set ftp login email, if rsync and wget download methods  
                    failed, download via ftp will be invoke, it will be 
                    courtesy if you provide your email.
EXAMPLE:

Check available taxa list and download genome data

  {0} -g 1                          # show all available taxa 

  {0} -g Mammals                    # show available taxa of mammals

  {0} -t human                      # use common name 

  {0} -t Homo sapiens -a 1          # use scientific name interactive mode

  {0} -t hg38 -f fa.gz              # use assmebly name fa.gz format file 

  {0} -t cow -a 1 -f fa.gz -o /tmp  # interactive mode, output directory

Download chromosome data in different formats (if available)

  {0} -t human -c 1       # common name, chromosome data, default file format

  {0} -t yeast -a 1 -c 2  # interactive mode, chromosome data, set file format 
""".format(program))
    sys.exit()


def main():
    "Main function for command-line usage"

    try:
        longopts = "help version group= taxa= assembly= chrs= formats= outdir= email=".split()
        opts, args = getopt.getopt(sys.argv[1:], "hvg:t:a:c:f:o:e:", longopts)
    except getopt.GetoptError:
        print("ERROR")
        shwo_usage()


    group, taxa, assembly, chrs, formats, outdir, email = '', '', '', '', '', '', ''
    for key, value in opts:
        if key in ("-h", "--help"):
            shwo_usage()
        elif key in ("-v", "--version"):
            show_version()
        elif key in ("-g", "--group"):
            group = value
        elif key in ("-t", '--taxa'):
            if value == '1':
                genomes(group='1')
            else:
                taxa = value
        elif key in ("-a", "--assembly"):
            if value == '0':
                assembly = False
            elif value == '1':
                assembly = True
            else:
                print('Wrong option! -a or --assmbly only accept 0 or 1')
                return
        elif key in ("-c", '--chrs'):
            if value == '0':
                chrs = False
            else:
                chrs = value
        elif key in ("-f", "--formats"):
            formats = value
        elif key in ("-o", '--outdir'):
            outdir = value
        elif key in ("-e", "--email"):
            email = value

    if not opts:
        shwo_usage()

    genomes(group, taxa, assembly, chrs, formats, outdir, email)



if __name__ == "__main__":
    main()
