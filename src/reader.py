#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import pandas as pd
import sys, os


def fasta(filename):
    """
    Reads in a FASTA file and yields each of its entries.
    The generator yields each sequence identifier and its 
    corresponding sequence to ensure a low memory profile. 
    If a sequence occurs over multiple lines, the yielded 
    sequence is concatenated.
     @param filename <str>:
        Path of FASTA file to read and parse
    @yield chrom, sequence <str>, <str>:
        Yields each seq id and seq in the FASTA file
    """
    with open(filename, 'r') as file:
        sequence, chrom = '', ''
        for line in file:
            line = line.strip()
            if line.startswith('>') and sequence:
                # base case for additional entries
                yield chrom, sequence
                chrom = line[1:] # remove the > symbol
                sequence = ''
            elif line.startswith('>'):
                # base case for first entry in fasta file
                chrom = line[1:] # remove the > symbol
            else:
                # concatenate multi-line sequences
                sequence += line
        else:
            yield chrom, sequence


def maf(filename, subset=[], skip='#', **kwargs):
    """Reads in an MAF-like file as a dataframe. Determines the 
    correct handler for reading in a given MAF file. Supports reading
    in TSV files (.tsv, .txt, .text, .vcf, or .maf), CSV files (.csv), 
    and excel files (.xls, .xlsx, .xlsm, .xlsb, .odf, .ods, .odt ). 
    The subset option allows a users to only select a few columns 
    given a list of column names.
    @param filename <str>:
        Path of an MAF-like file to read and parse
    @param subset list[<str>]:
        List of column names which can be used to subset the df
    @param skip <str>:
        Skips over line starting with this character
    @params kwargs <read_excel()>
        Key words to modify pandas.read_excel() function behavior
    @return <pandas dataframe>:
        dataframe with spreadsheet contents
    """
    # Get file extension
    extension = os.path.splitext(filename)[-1].lower()

    # Assign a handler to read in the file
    if extension in ['.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt']:
        # Read in as an excel file
        return excel(filename, subset, skip, **kwargs)
    elif extension in ['.csv']:
        # Read in as an CSV file
        return csv(filename, subset, skip, **kwargs)
    else:
        # Default to reading in as an TSV file
        # Tab is the normal delimeter for MAF or VCF files
        # MAF files usually have one of the following
        # extensions: '.tsv', '.txt', '.text', '.vcf', '.maf'
        return tsv(filename, subset, skip, **kwargs)


def excel(filename, subset=[], skip='#', **kwargs):
    """Reads in an excel file as a dataframe. The subset option
    allows a users to only select a few columns given a list of 
    column names.
    @param filename <str>:
        Path of an EXCEL file to read and parse
    @param subset list[<str>]:
        List of column names which can be used to subset the df
    @param skip <str>:
        Skips over line starting with this character
    @params kwargs <read_excel()>
        Key words to modify pandas.read_excel() function behavior
    @return <pandas dataframe>:
        dataframe with spreadsheet contents
    """
    if subset: 
        # 'Transcript_ID','HGVSc','Hugo_Symbol', 'Gene'
        return pd.read_excel(filename, comment=skip, **kwargs)[subset]
    
    return pd.read_excel(filename, comment=skip, **kwargs)


def tsv(filename, subset=[], skip='#', **kwargs):
    """Reads in an TSV file as a dataframe. The subset option
    allows a users to only select a few columns given a list of 
    column names.
    @param filename <str>:
        Path of an TSV file to read and parse
    @param subset list[<str>]:
        List of column names which can be used to subset the df
    @param skip <str>:
        Skips over line starting with this character
    @params kwargs <read_excel()>
        Key words to modify pandas.read_excel() function behavior
    @return <pandas dataframe>:
        dataframe with spreadsheet contents
    """
    if subset: 
        # 'Transcript_ID','HGVSc','Hugo_Symbol', 'Gene'
        return pd.read_table(filename, comment=skip, **kwargs)[subset]
    
    return pd.read_table(filename, comment=skip, **kwargs)


def csv(filename, subset=[], skip='#', **kwargs):
    """Reads in an CSV file as a dataframe. The subset option
    allows a users to only select a few columns given a list of 
    column names.
    @param filename <str>:
        Path of an CSV file to read and parse
    @param subset list[<str>]:
        List of column names which can be used to subset the df
    @param skip <str>:
        Skips over line starting with this character
    @params kwargs <read_excel()>
        Key words to modify pandas.read_excel() function behavior
    @return <pandas dataframe>:
        dataframe with spreadsheet contents
    """
    if subset: 
        # 'Transcript_ID','HGVSc','Hugo_Symbol', 'Gene'
        return pd.read_csv(filename, comment=skip, **kwargs)[subset]
    
    return pd.read_csv(filename, comment=skip, **kwargs)


def main():
    """
    Pseudo main method that runs when program is directly invoked.
    """
    file = sys.argv[1]
    for chrom, seq in fasta(file):
	    print("{}\t{}".format(chrom, seq))


if __name__ == '__main__':
    main()