#!/usr/bin/env python

__author__ = 'chris'
import argparse
import sys
import itertools

parser = argparse.ArgumentParser(description="https://projecteuler.net/problem=1 -- Find the sum of all the multiples of 3 or 5 below a number.")
parser.add_argument('--below', help='The number to find the sum of multiples below.', type=int, default=1000)

def main():
    args = parser.parse_args()
    below = args.below
    below = 100000 if below > 100000 else below
    total = sum(set([i for i in itertools.chain(xrange(3, below, 3), xrange(5,below,5))]))
    sys.stdout.write('The sum of numbers below {} is {}'.format(below, total))

if __name__ == "__main__":
    sys.exit(main())
