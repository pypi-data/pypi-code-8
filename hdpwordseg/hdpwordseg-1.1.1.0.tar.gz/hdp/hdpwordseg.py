#!/usr/bin/env pypy
#-*- coding: utf-8 -*-

import os, sys
import re
import tempfile
import ConfigParser

from prob import *
from ngram import *
from topicngram import *
from argparse import ArgumentParser

############################################################

def version():
    return '1.1.1.0'

############################################################

def readconfig(fname):
    config = ConfigParser.ConfigParser()
    config.read(fname)
    return config

def builddefaults(args):
    defaults = {}
    defaults['word-gram'] = args.n
    defaults['char-gram'] = args.cn
    defaults['max-word-len'] = str(args.maxwordlen)
    defaults['iters'] = str(args.maxiters)
    defaults['output'] = args.output
    defaults['delim'] = args.delim
    defaults['space'] = args.space
    defaults['burnin'] = args.burnin
    defaults['max-temp'] = str(args.maxtemp)
    defaults['topics'] = args.topics
    defaults['LDA'] = 'on' if args.lda else 'off'
    defaults['word-dict'] = args.dictfname
    defaults['atom-dict'] = args.atomfname
    defaults['alpha'] = str(args.alpha)
    defaults['theta'] = str(args.theta)
    defaults['pstop'] = args.pstop
    defaults['fwdbwd'] = 'on' if args.fwdbwd else 'off'
    defaults['hparamsmp'] = 'on' if args.hparamsmp else 'off'
    defaults['poisson'] = 'on' if args.poisson else 'off'
    defaults['verbose'] = 'off' if not args.verbose else 'on'
    defaults['debug'] = 'off' if not args.debug else 'on'
    defaults['cache'] = 'off' if not args.cache else 'on'
    defaults['beamsize'] = str(args.beamsize)
    return defaults

def configdict(cfgfname, args):
    defaults = builddefaults(args)
    cfgdict = {}
    if cfgfname is not None:
        config = ConfigParser.ConfigParser(defaults)
        config.read(cfgfname)
        cfgdict['n'] = config.getint('Model', 'word-gram')
        cfgdict['cn'] = config.getint('Model', 'char-gram')
        cfgdict['maxwordlen'] = config.getint('Content', 'max-word-len')
        cfgdict['maxiters'] = config.getint('Experiment', 'iters')
        cfgdict['output'] = config.get('Output', 'output')
        cfgdict['delim'] = config.get('Content', 'delim')
        if cfgdict['delim'] in ['no', 'false', 'off']:
            cfgdict['delim'] = ''
        else:
            cfgdict['delim'] = cfgdict['delim'][1:-1]
        cfgdict['space'] = config.get('Content', 'space')
        if cfgdict['space'] is not None:
            cfgdict['space'] = cfgdict['space'][1:-1]
        cfgdict['burnin'] = config.get('Experiment', 'burnin')
        if cfgdict['burnin'] is not None:
            cfgdict['burnin'] = int(cfgdict['burnin'])
        cfgdict['maxtemp'] = config.getfloat('Experiment', 'max-temp')
        cfgdict['topics'] = config.get('Model', 'topics')
        if cfgdict['topics'] is not None:
            cfgdict['topics'] = int(cfgdict['topics'])
        cfgdict['lda'] = config.getboolean('Model', 'LDA')
        cfgdict['dictfname'] = config.get('Content', 'word-dict')
        cfgdict['atomfname'] = config.get('Content', 'atom-dict')
        cfgdict['alpha'] = config.get('Hyperparameters', 'alpha')
        if cfgdict['alpha'] is not None:
            cfgdict['alpha'] = float(cfgdict['alpha'])
        cfgdict['theta'] = config.get('Hyperparameters', 'theta')
        if cfgdict['theta'] is not None:
            cfgdict['theta'] = float(cfgdict['theta'])
        cfgdict['pstop'] = config.get('Hyperparameters', 'pstop')
        if cfgdict['pstop'] is not None:
            cfgdict['pstop'] = float(cfgdict['pstop'])
        cfgdict['fwdbwd'] = config.getboolean('Experiment', 'fwdbwd')
        cfgdict['hparamsmp'] = config.getboolean('Experiment', 'hparamsmp')
        cfgdict['poisson'] = config.getboolean('Experiment', 'poisson')
        cfgdict['beamsize'] = config.get('Experiment', 'beamsize')
        if cfgdict['beamsize'] is not None:
            cfgdict['beamsize'] = int(cfgdict['beamsize'])
        cfgdict['verbose'] = config.getboolean('Experiment', 'verbose')
        cfgdict['debug'] = config.getboolean('Experiment', 'debug')
        cfgdict['cache'] = config.getboolean('Experiment', 'cache')
    else:
        cfgdict['n'] = defaults['word-gram']
        cfgdict['cn'] = defaults['char-gram']
        cfgdict['maxwordlen'] = defaults['max-word-len']
        cfgdict['maxiters'] = defaults['iters']
        cfgdict['output'] = defaults['output']
        cfgdict['delim'] = defaults['delim']
        cfgdict['space'] = defaults['space']
        cfgdict['burnin'] = defaults['burnin']
        cfgdict['maxtemp'] = defaults['max-temp']
        cfgdict['topics'] = defaults['topics']
        cfgdict['lda'] = (defaults['LDA'] == 'on')
        cfgdict['dictfname'] = defaults['word-dict']
        cfgdict['atomfname'] = defaults['atom-dict']
        cfgdict['alpha'] = float(defaults['alpha'])
        cfgdict['theta'] = float(defaults['theta'])
        cfgdict['pstop'] = float(defaults['pstop'])
        cfgdict['fwdbwd'] = (defaults['fwdbwd'] == 'on')
        cfgdict['hparamsmp'] = (defaults['hparamsmp'] == 'on')
        cfgdict['poisson'] = (defaults['poisson'] == 'on')
        cfgdict['verbose'] = (defaults['verbose'] == 'on')
        cfgdict['debug'] = (defaults['debug'] == 'on')
        cfgdict['cache'] = (defaults['cache'] == 'on')
        cfgdict['beamsize'] = defaults['beamsize']
    return cfgdict

############################################################

def replacemacros(macrotbl, line):
    result = line
    for m in macrotbl:
        result = result.replace(
            m, '(%s)' % '|'.join(macrotbl[m])
        )
    return result

def loadregex(fname):
    macrotbl = {}
    entries = []
    fhdl = open(fname)
    for line in fhdl:
        line = line.strip().decode('utf-8')
        if len(line) == 0: continue
        elif line.startswith('#'): continue
        elif line.startswith('@define'):
            toks = line.split(maxsplit=2)
            if len(toks) != 3: continue
            (m, pattern) = (toks[1], toks[2])
            if m not in macrotbl: macrotbl[m] = []
            macrotbl[m].append(pattern)
        else:
            entries.append(replacemacros(macrotbl, line))
    fhdl.close()
    expr = '^(' + '|'.join(entries) + ')$'
    regexp = re.compile(expr, re.UNICODE)
    return regexp

def loaddict(fname):
    if fname is not None:
        regexp = loadregex(fname)
        return lambda w: regexp.match(w) is not None
    else:
        return None

############################################################

def loadtext(ifnames, delim, space):
    texts = []
    structure = []
    size = 0
    idx = 0
    for ifname in ifnames:
        fhdl = open(ifname)
        for line in fhdl:
            line = line.strip().decode('utf-8')
            if len(line) == 0:
                structure.append('\n')
                continue
            if space is None: sents = line.split()
            else: sents = line.split(space)
            for sent in sents:
                if len(sent) == 0: continue
                if len(delim) > 0:
                    toks = [s for s in sent.split(delim) if len(s) > 0]
                else: toks = sent
                texts.append(toks)
                size += len(toks)
                structure.append(idx)
                idx += 1
            structure.append('\n')
    return (texts, structure, size)

def writetext(wordseg, structure, ofhdl, space, delim):
    L = len(structure)
    for i in xrange(L):
        x = structure[i]
        if type(x) is int:
            lattice = wordseg[x]
            sent = lattice.getsent()
            q = delim.join(sent).encode('utf-8') + delim
            ofhdl.write(q)
            if i < L - 1 and type(structure[i + 1]) is int:
                ofhdl.write(space + delim)
        elif type(x) is str:
            ofhdl.write(x)

############################################################

parser = ArgumentParser(
    description='Word segmentation module based on Hierarchical \
    Dirichlet Processes (Goldwater\'s PhD thesis, 2007; \
    Mochihashi et al., ACL 2009) version %s.' % version(),
    epilog='This implementation is developed by Prachya Boonkwan, \
    National Electronics and Computer Technology Center (NECTEC), \
    Thailand. (C) April 2015. All right reserved.'
)
parser.add_argument(
    'ifnames', metavar='ifname', type=str, nargs='+',
    help='Each input text file. If word delimiters are present in \
    the file, they must be specified by option --delimiter.'
)
parser.add_argument(
    '--config', dest='config', action='store',
    help='Read arguments from the specified configuration file',
    default=None
)
parser.add_argument(
    '-n', '--ngram', dest='n', action='store', type=int,
    help='The number of word-level contextual grams (e.g. -n 2 = \
    bigram) [either 1 or 2 or 3; default=3]',
    default=3
)
parser.add_argument(
    '-c', '--charngram', dest='cn', action='store', type=int,
    help='The number of character-level contextual grams (e.g. -c 3 \
    = trigram) [at least 1; default=n]',
    default=None
)
parser.add_argument(
    '-l', '--maxwordlen', dest='maxwordlen', action='store', 
    type=int, help='Maximum word length [default=20]', default=20
)
parser.add_argument(
    '-i', '--maxiters', dest='maxiters', action='store', type=int,
    help='Maximum number of corpus-level loop iterations \
    [default=100]',
    default=100
)
parser.add_argument(
    '-o', '--output', dest='output', action='store', type=str,
    help='Output file [default=stdout]'
)
parser.add_argument(
    '--delim', dest='delim', action='store', type=str,
    help='Word delimiter of the input files [default=\'\'; no \
    delimiters].', default=''
)
parser.add_argument(
    '--space', dest='space', action='store', type=str,
    help='Blank space [default=\' \']', default=None
)
parser.add_argument(
    '-b', '--burnin', dest='burnin', action='store', type=int,
    help='Number of corpus-level burn-in iterations (0 = burn-in \
    disabled) [default=disabled]',
    default=None
)
parser.add_argument(
    '-t', '--maxtemp', dest='maxtemp', action='store', type=float,
    help='Maximum temperature for simulated annealing (0 = disable) \
    [default=5]',
    default=5.0
)
parser.add_argument(
    '--topics', dest='topics', action='store', type=int,
    help='Number of topics (0 and 1 = disable) [default=disabled]',
    default=None
)
parser.add_argument(
    '--lda', dest='lda', action='store_true',
    help='Enable Latent Dirichlet Allocation for topics \
    [default=disabled]', default=False
)
parser.add_argument(
    '-d', '--dict', dest='dictfname', action='store', type=str,
    help='Dictionary file (cf. README.md for information) \
    [default=None]'
)
parser.add_argument(
    '-a', '--atompat', dest='atomfname', action='store', type=str, 
    help='Atom pattern file (cf. README.md for information) \
    [default=None]'
)
parser.add_argument(
    '--alpha', dest='alpha', action='store', type=float,
    help='The deduction parameter of Pitman-Yor Process for the \
    language model [default=0.0]',
    default=0.0
)
parser.add_argument(
    '--theta', dest='theta', action='store', type=float,
    help='The strength parameter of Pitman-Yor Process for the \
    language model [default=1.0]',
    default=1.0
)
parser.add_argument(
    '--pstop', dest='pstop', action='store', type=float,
    help='The stopping probability of word generation \
    [default=None; disabled]',
    default=None
)
parser.add_argument(
    '-F', '--nofwdbwd', dest='fwdbwd', action='store_false',
    help='Disable forward filtering and backward sampling \
    [default=enabled]',
    default=True
)
parser.add_argument(
    '-S', '--nohparamsmp', dest='hparamsmp', action='store_false',
    help='Disable hyper-parameter resampling [default=enabled]',
    default=True
)
parser.add_argument(
    '-R', '--nopoisson', dest='poisson', action='store_false',
    help='Disable the Poisson regulator for word lengths \
    [default=enabled]',
    default=True
)
parser.add_argument(
    '-v', '--verbose', dest='verbose', action='store_true',
    help='Verbose mode', default=False
)
parser.add_argument(
    '--debug', dest='debug', action='store_true',
    help='Debug mode', default=False
)
parser.add_argument(
    '--cache', dest='cache', action='store_true',
    help='Enable the usage of cache', default=False
)
parser.add_argument(
    '--beamsize', dest='beamsize', action='store', type=int,
    help='Set the beam size for search space sampling [default=10]',
    default=10
)

############################################################

def main():
    tmp = tempfile.mktemp()
    args = parser.parse_args()
    cfgdict = configdict(args.config, args)

    if cfgdict['n'] < 1 or cfgdict['n'] > 3:
        parser.print_help()
        sys.stderr.write('\n>> Only word-leveled unigram, bigram, and trigram are allowed.\n')
        sys.exit(1)

    if cfgdict['cn'] is None: cfgdict['cn'] = cfgdict['n']

    if cfgdict['cn'] < 1:
        parser.print_help()
        sys.stderr.write('\n>> Character-based n-gram cannot be less than 1.\n')
        sys.exit(1)

    wordfn = loaddict(cfgdict['dictfname'])
    atomfn = loaddict(cfgdict['atomfname'])
    (texts, structure, size) \
        = loadtext(args.ifnames, cfgdict['delim'], cfgdict['space'])

    if cfgdict['verbose']:
        sys.stderr.write(
            '>> Loaded %d text chunks (%d tokens) into memory\n' % (
                len(texts), size
            )
        )
    
    if len(cfgdict['delim']) == 0: cfgdict['delim'] = '|'
    if cfgdict['space'] is None: cfgdict['space'] = ' '

    # if size > 10000:
    #     cfgdict['cache'] = True
    disk = tmp if cfgdict['cache'] else None

    if cfgdict['verbose'] and cfgdict['cache']:
        sys.stderr.write('>> Cache: %s\n' % tmp)

    ProbWordLattice.setbeam(cfgdict['beamsize'])

    if cfgdict['topics'] in [0, 1, None]:
        wordseg = Wordseg(
            cfgdict['n'], cfgdict['cn'], texts,
            atomfn=atomfn, wordfn=wordfn, 
            maxwordlen=cfgdict['maxwordlen'],
            fwdbwd=cfgdict['fwdbwd'], hparamsmp=cfgdict['hparamsmp'],
            maxiters=cfgdict['maxiters'], burnin=cfgdict['burnin'],
            maxtemp=cfgdict['maxtemp'], p_stop=cfgdict['pstop'],
            poisson=cfgdict['poisson'],
            alpha_char=cfgdict['alpha'], alpha_uni=cfgdict['alpha'],
            alpha_bi=cfgdict['alpha'], alpha_tri=cfgdict['alpha'],
            theta_char=cfgdict['theta'], theta_uni=cfgdict['theta'],
            theta_bi=cfgdict['theta'], theta_tri=cfgdict['theta'],
            disk=disk
        )
    else:
        unidist = None
        topicdist = None
        if disk is not None:
            disk_uni = disk + '_unigram'
        else: disk_uni = None
        if args.lda:
            unidist = CRP(cfgdict['alpha'], cfgdict['theta'], disk=disk_uni)
            topicdist = TopicLDA(
                cfgdict['topics'], cfgdict['alpha'],
                cfgdict['theta'], unidist
            )
        wordseg = TopicWordseg(
            cfgdict['n'], cfgdict['cn'], texts,
            atomfn=atomfn, wordfn=wordfn, 
            maxwordlen=cfgdict['maxwordlen'],
            fwdbwd=cfgdict['fwdbwd'], hparamsmp=cfgdict['hparamsmp'],
            maxiters=cfgdict['maxiters'], burnin=cfgdict['burnin'],
            maxtemp=cfgdict['maxtemp'],
            p_stop=cfgdict['pstop'], poisson=cfgdict['poisson'],
            alpha_char=cfgdict['alpha'], alpha_uni=cfgdict['alpha'],
            alpha_bi=cfgdict['alpha'], alpha_tri=cfgdict['alpha'],
            alpha_topic=cfgdict['alpha'],
            theta_char=cfgdict['theta'], theta_uni=cfgdict['theta'], 
            theta_bi=cfgdict['theta'], theta_tri=cfgdict['theta'],
            theta_topic=cfgdict['theta'], disk=disk,
            maxtopics=cfgdict['topics'],
            unidist=unidist, topicdist=topicdist
        )

    if cfgdict['verbose']: wordseg.set_verbose()
    if cfgdict['debug']: 
        wordseg.set_debug()
        wordseg.set_verbose(False)

    try:
        wordseg.build()
        wordseg.run()
        
        if cfgdict['output'] is not None:
            ofhdl = open(cfgdict['output'], 'w')
        else:
            ofhdl = sys.stdout
    
        writetext(
            wordseg, structure, ofhdl, cfgdict['space'], cfgdict['delim']
        )

        if cfgdict['output'] is not None:
            ofhdl.close()
    except KeyboardInterrupt, e:
        sys.stderr.write('\nHDP word segmentation has terminated.\n')
    finally:
        wordseg.close()

############################################################

if __name__ == '__main__':
    main()
