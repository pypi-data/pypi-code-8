#!/usr/bin/env python

__author__ = 'chris'
import argparse
import sys

parser = argparse.ArgumentParser(description="https://projecteuler.net/problem=6 -- Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.")
parser.add_argument('--cutoff', help='The number to find the sum of squares below.', type=int, default=1)

def main():
    args = parser.parse_args()
    cutoff = args.cutoff
    if cutoff < 0:
        sys.stderr.write('Numbers must be positive.')
        return -1
    cutoff = 1000 if cutoff > 1000 else cutoff+1
    answer = sum(xrange(cutoff))**2-sum([i**2 for i in xrange(cutoff)])
    sys.stdout.write('The difference of the sum of squares and the square of sums below {} is {}'.format(cutoff-1, answer))

if __name__ == "__main__":
    sys.exit(main())
