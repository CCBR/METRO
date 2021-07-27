#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
from utils import err
import re

"""
ABOUT: A standard variant description has the format “prefix.position(s)_change”.

Depending on the change found, the description of the variant can have many different formats. 
Here we will list and briefly explain, the major variant types for Coding DNA reference sequences.

In a human diagnostic setting the most frequently used reference is a 'coding DNA reference sequence' 
(description starting with 'c.', e.g. NM_004006.3:c.4375C>T). Variant descriptions based on this format 
are very popular because they directly link to the encoded protein. In protein coding DNA reference 
sequences numbering starts with 1 at the first position of the protein coding region, the A of the 
translation initiating ATG triplet. Numbering ends at the last position of the ending triplet, the last 
position of the translation stop codon (TAA, TAG or TGA). When you divide the position number from a 'c.' 
description by three you get the affected amino acid residue from the protein sequence (description 
starting with 'p.'); for NM_004006.3:c.4375C>T (with predicted consequence on protein level 
p.(Arg1459*)), i.e. 4375 divided by three gives amino acid 1459. NOTE: positions in front of the 
protein coding sequence get a minus sign (e.g. 'c.-26'), those after the translation stop an asterisk 
(e.g. 'c.*85'). Numbering in intronic sequences has a format like c.530+6 or c.531-23. For details see 
'Reference Sequences'. The most frequently used coding DNA reference sequences are the NM’s (RefSeq gene 
transcript sequences, e.g. NM_004006.2) and LRG’s (Locus Genomic Reference sequences, e.g. LRG_199t1).

NOTE: mutations occuring in intronic or UTR regions (non-CDS regions) will not be evaulated, and 
will be passed over and will raise a non-terminating warning message to standard error.
"""

def mutate(sequence, hgvs):
    """Wrapper to each supported mutatation type: substitution, deletion, duplication, insertion, indel.
    Mutate takes in a reference sequence and a HGVS term and returns a mutated sequence. Only coding DNA
    reference sequences are supported (starts with 'c.') and mutations occuring in intronic or UTR regions 
    (non-CDS regions or genomic regions) will NOT be evaulated, and will be passed over and will raise a 
    non-terminating warning message to standard error.
    See https://varnomen.hgvs.org/bg-material/simple/ for more information about the HGVS specification.
    @param sequence <str>:
        Coding DNA reference sequence to mutate (transcript sequence)
    @param hgvs <str>:
        HGVS term describing the mutation
    @return mutation
        Mutated coding DNA sequence, unsupported HGVS types raise UnsupportedVariantTypeError()
    """

    # Check for mutations encoded in non-CDS regions like introns and 5'/3' UTR regions 
    if '-' in hgvs or '+' in hgvs or '*' in hgvs or '?' in hgvs:
        raise NonCodingVariantError(hgvs)

    # Check the variant type
    # Ideally a user would provide a coding DNA sequence and a coding DNA HGVS variant
    if not hgvs.startswith('c.'):
        err("WARNING: HGVS variant '{}' may not be a coding DNA variant and may not be supported!".format(hgvs))

    # Handler of each major variant types for Coding DNA reference sequences
    if '>' in hgvs:
        return substitution(sequence, hgvs)
    elif 'delins' in hgvs:
        return indel(sequence, hgvs)
    elif 'del' in hgvs:
        return deletion(sequence, hgvs)
    elif 'dup' in hgvs:
        duplication()
    elif 'ins' in hgvs:
        return insertion(sequence, hgvs)
    else:
        raise UnsupportedVariantTypeError(hgvs, "HGVS variant '{}' is an unsupported variant type!")


def tokenize(regex, tokens, hgvs, variant_type):
    """Breaks up a given HGVS term into meaningful tokens or components.
    Takes a regular expression, a list of named tokens representing required named 
    groups within the regular expression to check against, and a HGVS term to impose 
    the regular expression upon. A list of parse tokens are returned.
    @param regex <str>:
        Regular expression to tokenize HGVS term
    @param tokens list[<str>]:
        List of require named tokens/groups to check after imposing the regex
    @param hgvs <str>:
        HGVS term to parse with the regex param
    @param variant_type <str>:
        Variant type or parsing method
    @returns parsed list[<str>]:
        Parsed values for each named group in the regular expression
    """
    # List of parsed named group values to return
    parsed = []
    hgvs = hgvs.strip()
    matched = re.search(regex,hgvs) 

    if not matched: raise VariantParsingError(hgvs, variant_type)

    for token in tokens:
        parsed.append(matched.group(token))

    return parsed



def substitution(seq, hgvs):
    """One letter (nucleotide) of the DNA code is replaced (substituted) by one other letter. 
    On DNA and RNA level a substitution is indicated using '>' character.
    Example:
        c.4375C>T
    where the C nucleotide at position c.4375 changed to a T
    
    @param seq <str>:
        Coding DNA reference sequence to mutate (transcript sequence)
    @param hgvs <str>:
        HGVS term describing the mutation
    @return mutated
        Mutated coding DNA sequence
    """
    # Regular expression to tokenize HGVS subsitution term
    # See examples below
    # c.2413G>T
    # c.1249C>G
    # c.10732A>C
    # c.35G>T
    # c1.1.1249C>G
    regex = '(?P<id>^.+)\.(?P<position>\d+)(?P<ref>[A,C,G,T,N,a,c,g,t,n])(?P<type>>)(?P<alt>[A,C,G,T,N,a,c,g,t,n]$)'
    tokens = tokenize(regex, ['id', 'position', 'ref', 'type', 'alt'], hgvs, 'substitution')
    tid, mutation_position, ref, mtype, alt = tokens

    # Generate mutated sequence
    mutated = ''
    for i in range(len(seq)):
        bp = seq[i]
        # Transcript coordinates start at 1 (i.e. not zero based)
        transcript_index = i + 1
        # Find subsitution location defined by the HGVS term
        if transcript_index == int(mutation_position):
            # Sanity check to verify that the ref bp defined by HGSV is the same
            # as the transcript's base pair at the defined position
            if bp != ref:
                # Reference bp does NOT match HGVS!
                raise NonMatchingReferenceBases(hgvs)
            bp = alt
        mutated += bp

    return mutated


def deletion(seq, hgvs):
    """One or more letters of the DNA code are missing (deleted). 
    A deletion is indicated using 'del' sub string.
    Example:
        c.4375_4379del
    where the nucleotides from position c.4375 to c.4379 (CGATT) are missing (deleted). 
    Also reported as c.4375_4379delCGATT.

    @param seq <str>:
        Coding DNA reference sequence to mutate (transcript sequence)
    @param hgvs <str>:
        HGVS term describing the mutation
    @return mutated
        Mutated coding DNA sequence
    """
    # Regular expression to tokenize HGVS deletion term
    # See examples below
    # c.448del
    # c.333_666del
    # c.8054_8058delATTA
    # c.862+26delA
    # c.695-6del
    # c.460-9_460-8del
    regex = '(?P<id>^.+)\.(?P<start>[0-9+-?*]+)_{0,1}(?P<stop>[0-9+-?*]+){0,1}(?P<type>del)(?P<seq>[A,C,G,T,a,c,g,t,N,n]+){0,1}'
    tokens = tokenize(regex, ['id', 'start', 'stop', 'type', 'seq'], hgvs, 'deletion')
    tid, start, stop, mtype, del_seq = tokens
    start = int(start)
    deleted_range = [start]  # point deletion

    if stop:
        # Deletion occuring over a range of base pairs
        stop = int(stop)
        deleted_range = range(start, stop + 1)  # Range and string index end position is not inclusive

    # Generate mutated sequence
    mutated = ''
    for i in range(len(seq)):
        bp = seq[i]
        # Transcript coordinates start at 1 (i.e. not zero based)
        transcript_index = i + 1
        if transcript_index in deleted_range:
            continue  # do not concatenate bp (i.e. delete bp)
        mutated += bp

    return mutated


def duplication():
    """One or more letters of the DNA code are present twice (doubled, duplicated). 
    A duplication is indicated using 'dup' sub string.
    Example:
        c.4375_4385dup
    where the nucleotides from position c.4375 to c.4385 (CGATTATTCCA) are present twice 
    (duplicated). Often reported as c.4375_4385dupCGATTATTCCA or c.4385_4386insCGATTATTCCA
    (not a correct HGVS description).
    """
    pass



def insertion(seq, hgvs):
    """One or more letters in the DNA code are new (inserted).
    An insertion is indicated using 'ins' sub string.
    Example:
        c.4375_4376insACCT
    where the new sequence 'ACCT' was found inserted between positions c.4375 and c.4376.
    NOTE: A stop position is required by the HGVS specification.

    Point of insertion or insertion break point should contain two flanking nucleotides,
    e.g. (123 and 124) but NOT (123 and 125)
    Example:
        c.2_3insCCCCC
        1  2   3  4
        A  A   T  T
             ^
         C C C C C
    Result:
        1  2  3  4  5  6  7  8  9
        A  A  C  C  C  C  C  A  A

    @param seq <str>:
        Coding DNA reference sequence to mutate (transcript sequence)
    @param hgvs <str>:
        HGVS term describing the mutation
    @return mutated
        Mutated coding DNA sequence
    """
    # Regular expression to tokenize HGVS deletion term
    # See examples below
    # c.4375_4376insACCT
    # c.1597_1598insC
    # c.432-15_432-14insGGGG
    # c.579+1_579+2insAAGAAGAGGAAGA
    # c.738_738+1insAAAAAGAAAGAAGAGG
    regex = '(?P<id>^.+)\.(?P<start>[0-9+-?*]+)_{1}(?P<stop>[0-9+-?*]+){1}(?P<type>ins)(?P<seq>[A,C,G,T,a,c,g,t,N,n]+){1}'
    tokens = tokenize(regex, ['id', 'start', 'stop', 'type', 'seq'], hgvs, 'insertion')
    tid, start, stop, mtype, ins_seq = tokens
    start = int(start)

    # Point of insertion or insertion break point
    insert_point = start  # Insertion is added directly after concatenating start bp

    # Generate mutated sequence
    mutated = ''
    for i in range(len(seq)):
        bp = seq[i]
        # Transcript coordinates start at 1 (i.e. not zero based)
        transcript_index = i + 1
        if transcript_index == insert_point:
            # Insertion MUST be added after concatenating insert point (or start) bp
            mutated += bp
            mutated += ins_seq
            continue # goto next bp position
        mutated += bp

    return mutated


def indel(seq, hgvs):
    """One or more letters in the DNA code are missing and replaced by several new letters. 
    A deletion/insertion is indicated using 'delins' sub string.
    Example:
        c.4375_4376delinsAGTT
    the nucleotides from position c.4375 to c.4376 (CG) are missing (deleted) and replaced by 
    the new sequence 'AGTT'. Also reported as c.4375_4376delCGinsAGTT.
    Example:
        c.2_3insCCCCC
        1  2   3  4
        A  T   T  A
           - - -
             ^
         C C C C C
    Result:
        1  2  3  4  5  6  7
        A  C  C  C  C  C  A
    """
    # Regular expression to tokenize HGVS deletion term
    # See examples below
    # c.32386323delinsGA
    # c.6775_6777delinsC
    # c.145_147delinsTGG (p.Arg49Trp)
    # c.9002_9009delinsTTT
    # LRG_199t1:c.850_901delinsTTCCTCGATGCCTG
    regex = '(?P<id>^.+)\.(?P<start>[0-9+-?*]+)_{0,1}(?P<stop>[0-9+-?*]+){0,1}(?P<type>delins)(?P<seq>[A,C,G,T,a,c,g,t,N,n]+){1}'
    tokens = tokenize(regex, ['id', 'start', 'stop', 'type', 'seq'], hgvs, 'indel')
    tid, start, stop, mtype, ins_seq = tokens
    start = int(start)
    deleted_range = [start]

    if stop:
        # Deletion occuring over a range of base pairs
        stop = int(stop)
        deleted_range = range(start, stop + 1)  # Range and string index end position is not inclusive

    # Generate mutated sequence
    mutated = ''
    inserted = False  # tracks whether the insertion has been added
    for i in range(len(seq)):
        bp = seq[i]
        # Transcript coordinates start at 1 (i.e. not zero based)
        transcript_index = i + 1
        if transcript_index in deleted_range:
            if not inserted:
                mutated += ins_seq
                inserted = True # add insertion sequence only once
            continue  # do not concatenate bp (i.e. delete bp)
        mutated += bp

    return mutated





class NonCodingVariantError(Exception):
    """Raised when a user provides a coding DNA HGVS term with a non-coding DNA variant.
    Requires the genomic sequence to be provided. Mutated sequence cannot be inferred from the 
    transcript sequence.
    @attributes:
        hgvs -- input hgvs term which caused the error
    """
    def __init__(self, hgvs):
        self.hgvs = hgvs
        self.message = """Error: HGVS coding DNA mutation '{}' in non-coding region!
            └── Mutated sequence cannot be inferred from the transcript sequence and requires 
                genomic reference sequence.""".format(self.hgvs)
        super(Exception, self).__init__(self.message)

    def __str__(self):
        return "{} -> {}".format(self.hgvs, self.message)


class UnsupportedVariantTypeError(Exception):
    """Raised when a user provides an unsupported HGVS variant type.
    Each major variant type for coding DNA sequences are supported.
    Unsupported genomic DNA variants include inversion ('inv'), alleles (';'),
    repeated sequences ([N]), complex ('pter' OR 'cen' OR 'qter' OR 'sub' or '::'),
    other ('=').
    @attributes:
        hgvs -- input hgvs term which caused the error
    """
    def __init__(self, hgvs):
        self.hgvs = hgvs
        self.message = """Error: Unsupported HGVS mutation type '{}' provided!
            └── Only coding DNA reference sequences are supported. 
                Not all genomic reference sequence HGVS mutations are not supported.""".format(self.hgvs)
        super(Exception, self).__init__(self.message)

    def __str__(self):
        return "{} -> {}".format(self.hgvs, self.message)


class VariantParsingError(Exception):
    """Raised when a HGVS variant cannot be parsed.
    Each major variant type for coding DNA sequences are supported.
    Unsupported genomic DNA variants include inversion ('inv'), alleles (';'),
    repeated sequences ([N]), complex ('pter' OR 'cen' OR 'qter' OR 'sub' or '::'),
    other ('=').
    @attributes:
        hgvs -- input hgvs term which caused the error
        method -- regular expression type for variant class (sub, del, indel, dup)
    """
    def __init__(self, hgvs, method):
        self.hgvs = hgvs
        self.method = method
        self.message = """Error: Failed to parse HGVS mutation '{}' using {} parser!
            └── Only coding DNA reference sequences are supported. 
                Not all genomic reference sequence HGVS mutations are not supported.""".format(self.hgvs, self.method)
        super(Exception, self).__init__(self.message)

    def __str__(self):
        return "{} -> {}".format(self.hgvs, self.message)



class NonMatchingReferenceBases(Exception):
    """Raised when a base pair or range of base pairs defined by a HGVS term
    does not match the base pair or range of basepairs in the provided reference
    transcriptome.

    @attributes:
        hgvs -- input hgvs term which caused the error
    """
    def __init__(self, hgvs, method):
        self.hgvs = hgvs
        self.method = method
        self.message = """Error: Non-matching bases in HGVS '{}' mutation and reference sequence!
            └── Please verify the correct reference file is provided!""".format(self.hgvs, self.method)
        super(Exception, self).__init__(self.message)

    def __str__(self):
        return "{} -> {}".format(self.hgvs, self.message)


def main():
    """
    Pseudo main method that runs when program is directly invoked.
    """
    # TODO: add tests for each HGVS variant class
    # All variants given are in the DMD gene and reported in relation 
    # to coding DNA reference sequence LRG_199t1 (NM_004006.3).
    # https://varnomen.hgvs.org/bg-material/simple/
    
    # Check for variants in non-CDS regions
    try:
        mutate(sequence='TTTTAC', hgvs='c.1-1_1insCAA')
    except NonCodingVariantError:
        err("WARNING: Skipping over non-coding DNA HGVS variant '{}'!".format('c.1-1_1insCAA'))
    
    # Check for variants in genomic dna
    try:
        mutate(sequence='TTTTAC', hgvs='g.1_1insCAA')
    except UnsupportedVariantTypeError:
        err("WARNING: Skipping over genomic DNA HGVS variant '{}'!".format('g.1_1insCAA'))

    # Tokenize different HGVS terms
    try:
        # Induce substitution parsing failure
        tokenize('(?P<id>^.+)\.(?P<position>\d+)(?P<ref>[A,C,G,T,N,a,c,g,t,n])(?P<type>>)(?P<alt>[A,C,G,T,N,a,c,g,t,n]$)', 
            ['id', 'position', 'ref', 'type', 'alt'], 
            'g.1_1insCAA', 'substitution'
        )
    except VariantParsingError:
        err('WARNING: Failed to parse {} using {} parser!'.format('g.1_1insCAA', 'substitution'))

    # Check deletion tokenization
    regex = '(?P<id>^.+)\.(?P<start>[0-9+-?*]+)_{0,1}(?P<stop>[0-9+-?*]+){0,1}(?P<type>del)(?P<seq>[A,C,G,T,a,c,g,t,N,n]+){0,1}'
    tokens = tokenize(regex, ['id', 'start', 'stop', 'type', 'seq'], 'c.8054delG', 'deletion')
    print('Tokenization of c.8054_8058delATTA -> {}'.format(tokens))

    # Induce a deletion
    print('Induced deletion of c.1_2delAA: AATCC -> {}'.format(deletion('AATCC', 'c.1_2delAA')))

    # Induce an insertion mutation
    print('Induced insertion of c.2_3insAA: AATT -> {}'.format(insertion('AATT', 'c.2_3insCCccGGgg')))

    # Induce an indel
    print('Induced indel of c.2_4delinsgGGGaCCCc: ATTTA -> {}'.format(indel('ATTTA', 'c.2_4delinsgGGGaCCCc')))
    print('Induced indel of c.2delinsgGGGaCCCc: ACA -> {}'.format(indel('ACA', 'c.2delinsgGGGaCCCc')))


if __name__ == '__main__':
    main()