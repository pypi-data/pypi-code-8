#!/usr/bin/env python

__author__ = 'chris'
import argparse
import sys

parser = argparse.ArgumentParser(description="https://projecteuler.net/problem=16 -- What is the sum of the digits of the number 2^1000?")
parser.add_argument('--exponent', help='The exponent to find digits below.', type=int, default=1)

def main():
    args = parser.parse_args()
    exponent = args.exponent
    if exponent  < 0:
        sys.stderr.write('Exponents must be positive.')
        return -1
    exponent = 5000 if exponent  > 1000 else exponent
    answer = sum(map(int, list(str(2**exponent))))
    sys.stdout.write('The sum of digits for 2^{} is {}'.format(exponent, answer))

if __name__ == "__main__":
    sys.exit(main())
