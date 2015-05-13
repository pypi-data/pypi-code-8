"""Command line interface for ifalg"""
from ifalg.linux import STRATEGY_HEURISTIC, STRATEGY_SENDMSG, STRATEGY_SPLICE, ALG_TYPE_SKCIPHER, ALG_TYPE_HASH
import argparse
import sys

ALG_CHOICES = [
    ALG_TYPE_SKCIPHER,
    ALG_TYPE_HASH
]

STRATEGY_CHOICES = {
    'heuristic': STRATEGY_HEURISTIC,
    'sendmsg': STRATEGY_SENDMSG,
    'splice': STRATEGY_SPLICE
}

def die(msg, status=1):
    print("ERROR: %s"%msg, file=sys.stderr)
    sys.exit(status)

def main():
    argparser = argparse.ArgumentParser(description="Command Line interface with the Linux kernel crypto API")
    argparser.add_argument('-k', '--key',
                           action = 'store',
                           help = 'Symetric cipher key / HMAC key, in hex format')
    argparser.add_argument('-i', '--iv',
                           action = 'store',
                           help = 'IV used for operation, in hex format')
    argparser.add_argument('-t', '--type',
                           action = 'store',
                           required = True,
                           choices = ALG_CHOICES,
                           help = 'Algorthm type')
    argparser.add_argument('-a', '--algo',
                           action = 'store',
                           required = True,
                           help = 'Algorithm name')
    argparser.add_argument('-s', '--strategy',
                           action = 'store',
                           choices = STRATEGY_CHOICES.keys(),
                           default = 'heuristic',
                           help = 'Strategy used for oneshot operations')
    argparser.add_argument('--in',
                           action = 'store',
                           help = 'Input data, for oneshot operations')
    argparser.add_argument('--in-file',
                           action = 'store',
                           help = "Input file, if no '--in' nor '--in-file' is specified then read from STDIN")
    argparser.add_argument('--out-file',
                           action = 'store',
                           help = "Output file, if omited the output is send to STDOUT")
    argparser.add_argument('-f', '--format',
                           action = 'store',
                           choices = ['binary', 'hex'],
                           help = "Output format, if omited it depends of '--out-file', bynary for files and hex for STDOUT")
    
    
    args = argparser.parse_args()
    print("arguments: %r"%(args,))
    try:
        iv = None if args.iv is None else bytes.fromhex(args.iv.lower())
    except ValueError:
        die("IV must be an hex string")

    try:
        key = None if args.key is None else bytes.fromhex(args.key.lower())
    except ValueError:
        die("Key must be an hex string")

if __name__ == '__main__':
    main()
