#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import sys


def fasta(filename):
    with open(filename, 'r') as file:
        sequence, chrom = '', ''
        for line in file:
            line = line.strip()
            if line.startswith('>') and sequence:
                # base case for additional entries
                yield chrom, sequence
                chrom = line.split(' ')[0]
                sequence = ''
            elif line.startswith('>'):
                # base case for first entry in fasta file
                chrom = line.split(' ')[0]
            else:
                # concatenate multi-line sequences
                sequence += line
        else:
            yield chrom, sequence


def main():
	file = sys.argv[1]
	for chrom, seq in fasta(file):
		print(chrom, seq)


if __name__ == '__main__':
	main()