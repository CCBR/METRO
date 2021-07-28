#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
from utils import err
import re


def translate(sequence):
    """Translates a coding DNA reference sequence into an amino acid sequence.
    @param sequence <str>:
        Coding DNA reference sequence to translate (transcript sequence or CDS sequence)
    @returns aminoacid <str>:
        Translated amino acid sequence
    """
    # Clean sequence prior to conversion
    sequence = sequence.strip().upper()
    # Translates codons to amino acids 
    codontable = {
        'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
        'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
        'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
        'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
        'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
        'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
        'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
        'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
        'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
        'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
        'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
        'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*',
        'TGC': 'C', 'TGT': 'C', 'TGA': '*', 'TGG': 'W'
    }

    # Translate DNA sequence to amino acids 
    aminoacid = ""
    for i in range(0, len(sequence)-2, 3):
        codon = sequence[i:i+3]
        try:
            aminoacid += codontable[codon]
        except KeyError:
            raise InvalidCodonError(sequence, codon)

    return aminoacid


class InvalidCodonError(Exception):
    """Raised when a trinucleotide sequence cannot be mapped to a known amino acid.
    This may occur when the provided sequence contains N's or unknown basepairs.
    In this scenario, the corresponding amino acid cannot be determined.

    @attributes:
        sequence -- input DNA sequence which caused the error
        codon    -- the exact codon or trinucleotide sequence that cannot be mapped.
    """
    def __init__(self, sequence, codon):
        self.sequence = sequence
        self.codon = codon
        self.message = """Error: Invalid trinucleotide sequence, '{}', within coding DNA sequence to translate!
            └── Please view the provided reference file and the provided DNA sequence to translate:
                > {}""".format(self.codon, self.sequence)
        super(Exception, self).__init__(self.message)

    def __str__(self):
        return "{} -> {}".format(self.codon, self.message)


def main():
    """
    Pseudo main method that runs when program is directly invoked.
    """

    # Translate DNA sequence to AA sequence
    print('Translated {} -> {}'.format('ATGATAACAAACAGCCTACCATGA',translate('ATGATAACAAACAGCCTACCATGA')))
    assert(translate('ATGATAACAAACAGCCTACCATGA') == 'MITNSLP*'), 'Error DNA sequence translation incorrect!'

    # Induce a translation failure
    try:
        translate('ATGATAACnAACAGCCTACCATGA')
    except InvalidCodonError as e:
        err('WARNING: Unable to translate DNA sequence!\n{}'.format(e))

if __name__ == '__main__':
    main()