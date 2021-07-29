#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function, division
from utils import err
from math import ceil
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


def truncate(sequence, index, upstream=30, downstream=None):
    """Truncates a given amino acid sequence at a given index up to X characters upstream 
    and Y characters downstream. If a stop codon is found downstream prior to reaching 
    the Y-th character, it will truncate the sequenece automatically. If a downstream
    value is not provided, it will return the remaining sequence downstream of the index
    or the sequence up to the first terminating stop codon.

    Sequence: index=5, upstream=2, downstream=3
        1  2  3  4  5  6  7  8  9
        M  I  T  N  S  D  L  P  *
                    ^
              +  +  !  +  +  +
      2 bp upstream | 3 bp downstream
    Result:
        1  2  3  4  5  6
        T  N  S  D  L  P
    @param sequence <str>:
        Amino acid sequence to truncate
    @param index <int>:
        Seed or reference point index in sequence where upstream and downstream characters
        will be derived from to truncate the sequence
    @param upstream <int>:
        Extract N character upstream of the index the sequence
    @param upstream <int>:
        Extract N character downstream of the index the sequence
    @returns subsequence <str>:
        Truncated amino acid sequence 
    """
    # Get index upstream with respect to string length
    # and convert 1-based to 0-based coordinate system
    left_index = max(0, index-abs(upstream)-1)  
    # Default right index to capture end of the sequence
    right_index = len(sequence)
    # If downstream is not given, it will truncate the sequenece 
    # until a stop codon ('*') is reached or until the end of the 
    # sequence is reached. Try to find index of the first stop 
    # codon in downstream sequence.
    downstream_sequence = sequence[index:right_index]
    for i in range(len(downstream_sequence)):
        if downstream_sequence[i] == '*':
            right_index = index + i + 1 # convert 0-based to 1-based coordinate system
            break  # only consider first stop codon occurence

    if downstream:
        # Get downstream with respect to string length
        # Find the downstream cut off as the minimum between:
        # A. Index + Upstream Sequence Length
        # B. right_index where the right_index could be
        #     I.  the length of the sequence
        #     II. the position of the first stop codon (if found) 
        right_index = min(index+abs(downstream), right_index)

    subsequence = "{}{}".format(
        sequence[left_index:index],  # Extracts left sub string AND index seed
        sequence[index:right_index]  # Extracts right substring only 
    )

    return subsequence


def convert_aa_cooridate(coordinate):
    """Converts DNA sequence coordinates into Amino acid coordinates.
    Assumes the coordiante system of the DNA sequence starts at 1, 
    and the provided coordinate is a non-negative integer.
    
    @param coord <int>:
        DNA coordinate to convert into an Amino acid coordinate
    @returns converted <int>:
        Converted Amino acid coordinate
    """
    coordinate = int(coordinate)
    # Finds coordinate in Amino acid space
    converted = int(ceil(coordinate/3))

    return converted


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
    
    # Convert DNA coordinates to AA coordinates
    print("DNA to AA coordinates: {} -> {}".format(1, convert_aa_cooridate(1)))
    print("DNA to AA coordinates: {} -> {}".format(5, convert_aa_cooridate(5)))
    print("DNA to AA coordinates: {} -> {}".format(9, convert_aa_cooridate(9)))

    # Truncate amino acid sequence 
    print("Truncating sequence where i=5,l=2,r=3: {} -> {}".format('MITNSDLP*', truncate('MITNSDLP*', 5,2,3)))
    print("Truncating sequence where i=5,l=2,r=999: {} -> {}".format('MITNSDLP*', truncate('MITNSDLP*', 5,2,999)))
    print("Truncating sequence where i=1,l=-66,r=1: {} -> {}".format('MITNSDLP*', truncate('MITNSDLP*', 1,66,1)))
    print("Truncating sequence where i=9,l=2,r=66: {} -> {}".format('MITNSDLP*', truncate('MITNSDLP*', 9,2,66)))
    print("Truncating sequence with terminating stop codon where i=5,l=2,r=None: {} -> {}".format(
        'MITNSD*LP*', truncate('MITNSD*LP*', 5, 2)))

if __name__ == '__main__':
    main()