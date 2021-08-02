# AAsap

[![GitHub releases](https://img.shields.io/github/release/CCBR/AAsap)](https://github.com/CCBR/AAsap/releases)  [![GitHub issues](https://img.shields.io/github/issues/CCBR/AAsap)](https://github.com/CCBR/AAsap/issues) [![GitHub license](https://img.shields.io/github/license/CCBR/AAsap)](https://github.com/CCBR/AAsap/blob/master/LICENSE)  

### 1. Introduction  

**A**mino **A**cid **s**equence **a**nalysis **p**ipeline, as known as `AAsap`, is a pipeline to characterize the effect of a mutation on an amino acid sequence. 

AAsap takes a MAF-like file containing HGVS terms describing a given mutation and a FASTA file containing transcript sequences to determine the consequence of a mutation on a protein product. The `build` sub command can be used to generate a FASTA file containing CDS sequence of each transcript. The `run` sub command will parse and tokenize HGVS terms describing coding DNA mutations. AAsap supports each major class of HGVS terms encoding for coding DNA mutations: substitution, deletion, insertions, duplications, and INDELS. AAsap _does not_ support HGVS tokenization of terms describing mutations in non-exonic (or non-CDS) regions like introns, 3'-UTR or 5'-UTR. AAsap will mutate a given coding DNA sequence based on the provided HGVS term and will translate that sequence into an amino acid sequence. AAsap will also truncate a given amino acid sequence +/- N amino acids relativve to a given mutation start site.

### 2. System Requirements

`aasap` executable is composed of several inter-related sub commands. The `build` sub command requires that `samtools`, `gffread` from the cufflinks, and `python` are installed on the target system. A virtual environment containing the required python packages to run aasap can be built from our `requirements.txt`. aasap compatiable with `python>=2.7` and `python>=3.5` (with preference to the latter).

If you are on biowulf, these dependencies can be met by running the following command:
```bash
# Grab an interactive node
# Do not run aasap on the head node!
srun -N 1 -n 1 --time=12:00:00 -p interactive --mem=8gb  --cpus-per-task=4 --pty bash
module purge
module load cuffdiff samtools python/3.5
```

### 3. Build Resources

AAsap has a `build` sub command to create any required reference files for the `run` sub command. The `build` sub command will generate a reference file containing the transcriptome (i.e. CDS region of each transcript) in FASTA format from a genomic FASTA file and an annotation in GTF format. The sequence of each transcript annotated in the GTF file will be reported in this transcripts FASTA file. This file can then be provided to the `--transcripts` option of the `run` sub command. When the `build` sub command is executed, the transcripts FASTA file (named _transcripts.fa_) will be generated in the defined output directory. 

It is important to note that when building reference files for AAsap, you should used the same genomic FASTA file and GTF file that was used to call and annotate your variants. If a transcript is reported in the MAF file but cannot be found in the provided GTF file, a warning message will be produced to standard error. This warning message may indicate that the genomic FASTA and/or the GTF file you provided is not correct.

#### 3.1 Build Synposis

The `./aasap` executable is composed of several inter-related sub commands. Please see `./aasap -h` for all available options. The synopsis for the `build` sub command   shows its parameters and their usage. Optional parameters are shown in square brackets.

```
$ ./aasap build [-h] --ref-fa REF_FA \
                --ref-gtf REF_GTF \
                --output  OUTPUT 
```

This part of the documentation describes options and concepts for the `./aasap build` sub command in more detail. With minimal configuration, the build sub command enables you to build reference file for the `./aasap run` sub command. Buidling refernce file for the run sub command is fast and easy! In its most basic form, `./aasap build` only has _three required inputs_.

#### 3.2 Required Build Arguments

Each of the following arguments are required. Failure to provide a required argument will result in a non-zero exit-code.


  `--ref-fa REF_FA`  
> **Genomic FASTA file of the reference genome.**  
> *type: file*
> 
> This file represents the genome sequence of the reference assembly in FASTA format. This input file should not be compressed. Sequence identifers in this file must match with sequence identifers in the GTF file provided to `--ref-gtf`.  
> 
> ***Example:***
> `--ref-fa GRCh38.primary_assembly.genome.fa`

--- 
  `--ref-gtf REF_GTF`  
> **Gene annotation or GTF file for the reference genome.**  
> *type: file*
> 
> This file represents the reference genome's gene annotation in GTF format. This input file should not be compressed. Sequence identifers (column 1) in this file must match with sequence identifers in the FASTA file provided to `--ref-fa`.  
> 
> ***Example:***  
> `--ref-gtf gencode.v36.primary_assembly.annotation.gtf`
  
--- 
  `--output OUTPUT`
> **Output directory where reference files will be generated.**  
> *type: path*
>   
> This location is where the build pipeline will create all of its output files. If the user-provided path does not exist, it will be created automatically.
> 
> ***Example:*** 
> `--output /scratch/$USER/refs/hg38_v36/`

#### 3.3 Build Options

Each of the following arguments are optional and do not need to be provided. 

  `-h, --help`            
> **Display Help.**  
> *type: boolean*
> 
> Shows command's synopsis, help message, and an example command
> 
> ***Example:*** 
> `--help`

#### 3.4 Build Example

Build reference files for the run sub comamnd.

```bash 
# Step 0.) Grab an interactive node
# Do not run on head node!
srun -N 1 -n 1 --time=12:00:00 -p interactive --mem=8gb  --cpus-per-task=4 --pty bash
module purge
module load cuffdiff samtools

# Step 1.) Build AASAP reference files
aasap build --ref-fa GRCm39.primary_assembly.genome.fa \
            --ref-gtf gencode.vM26.annotation.gtf \
            --output /scratch/$USER/AASAP/refs/
```

### 4. Run AAsap

AAsap has a `run` sub command to generate a mutated amino acid sequence described by an HGVS term. AAsap takes a MAF-like file containing HGVS terms describing a given mutation and a FASTA file containing transcript sequences to determine the mutated amino acid sequence. The build sub command can be used to generate a FASTA file containing CDS sequence of each transcript. 

AAsap supports each major class of HGVS terms encoding for mutations in coding DNA sequences: substitution, deletion, insertions, duplications, and INDELS. AAsap does not support HGVS tokenization of terms describing mutations in non-exonic (or non-CDS) regions like intronic or UTR regions.

AAsap will also truncate a given amino acid sequence +/- N amino acids relativve to a given mutation start site. This feature can be controlled via the '--subset' option.

#### 4.1 Run Synopsis

The `./aasap` executable is composed of several inter-related sub commands. Please see `./aasap -h` for all available options. The synopsis for the run sub command shows its parameters and their usage. Optional parameters are shown in square brackets.

```
$ ./aasap run [-h] [--subset SUBSET] \
                   --input INPUT [INPUT ...] \
                   --transcripts TRANSCRIPTS \
                   --output OUTPUT 
```

This part of the documentation describes options and concepts for `./aasap run` sub command in more detail. With minimal configuration, the `run` sub command enables you to start running aasap pipeline.

Setting up the aasap is fast and easy! In its most basic form, `./aasap run` only has _three required inputs_.

#### 4.2 Required Run Arguments

Each of the following arguments are required. Failure to provide a required argument will result in a non-zero exit-code.


  `--input INPUT [INPUT ...]`  
> **Input MAF-like file(s) to process.**  
> *type: file*  
> 
> One or more MAF-like files can be provided. From the command-line, each input file should seperated by a space. Globbing is also supported! This makes selecting input files easier. Input MAF-like input files should be in an excel-like, CSV, or TSV format. For each input file a new output file will be generated in the specified output directory. Each file will end with the following extension: `.aasap.tsv`.
> 
> ***Example:*** 
> `--input data/*.xls*`

---  
  `--output OUTPUT`
> **Path to an output directory.**   
> *type: path*
>   
> This location is where the aasap will create all of its output files, also known as the pipeline's working directory. If the provided output directory does not exist, it will be created automatically.
> 
> ***Example:*** 
> `--output /scratch/$USER/RNA_hg38`

---  
  `--transcripts TRANSCRIPTS`
> **Transcriptomic FASTA file.**   
> *type: file*
>   
> This reference file contains the sequence of each transcript in the reference genome. The file can be generated by running the build sub command, (i.e. /path/to/build/output/transcripts.fa). When creating this reference file, it is very important to use the same genomic FASTA and annotation file to call and annotate variants. Failure to use the correct reference file may result in multiple warnings and/or errors. 
> 
> ***Example:*** 
> ` --transcripts transcripts.fa`

#### 4.3 Run Options

Each of the following arguments are optional and do not need to be provided. 

  `-h, --help`            
> **Display Help.**  
> *type: boolean*
> 
> Shows command's synopsis, help message, and an example command
> 
> ***Example:*** 
> `--help`

---  
  `--subset SUBSET`            
> **Subset resulting mutated amino acid sequences.**  
> *type: int*
> 
> If defined, this option will obtain the mutated amino acid sequence (AAS) +/- N amino acids of the mutation start site. By default, the first 30 upstream and downstream amino acids from the mutation site are recorded for non-frame shift mutations. Amino acids downstream of a frame shit mutation will be reported until the end of the amino acids sequence for the variants transcript or until the first reported terminating stop codon is found.
>
> ***Example:*** 
> `--subset 30`

#### 4.4 Run Example

Run aasap with the references files generated in the build example.

```bash 
# Step 0.) Grab an interactive node
# Do not run on head node!
srun -N 1 -n 1 --time=12:00:00 -p interactive --mem=8gb  --cpus-per-task=4 --pty bash
module purge
module load python/3.5

 # Step 1.) Run AASAP to find mutated protein products
 ./aasap run --input  data/*.xlsx \
             --output /scratch/$USER/AASAP \
             --transcripts /scratch/$USER/AASAP/refs/transcripts.fa \
             --subset 30
```
