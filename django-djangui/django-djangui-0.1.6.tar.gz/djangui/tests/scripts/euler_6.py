#!/usr/bin/env python

__author__ = 'chris'
import argparse
import sys

parser = argparse.ArgumentParser(description="https://projecteuler.net/problem=6 -- Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.")
parser.add_argument('--cutoff', help='The number to find the sum of squares below.', type=int, default=1)

def main():
    args = parser.parse_args()
    start = args.start
    if start < 0:
        sys.stderr.write('Numbers must be positive.')
        return -1
    start = 1000 if start > 1000 else start+1
    answer = sum(xrange(start))**2-sum([i**2 for i in xrange(start)])
    sys.stdout.write('The difference of the sum of squares and the square of sums below {} is {}'.format(start, answer))

if __name__ == "__main__":
    sys.exit(main())
