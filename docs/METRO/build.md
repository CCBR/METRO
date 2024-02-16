# 3. Build Synposis

The `./metro` executable is composed of several inter-related sub commands. Please see `./metro -h` for all available options. The synopsis for the sub command `build` shows its parameters and their usage. Optional parameters are shown in square brackets.

```
$ ./metro build [-h] --ref-fa REF_FA \
                --ref-gtf REF_GTF \
                --output  OUTPUT 
```

This part of the documentation describes options and concepts for the `./metro build` sub command in more detail. With minimal configuration, the build sub command enables you to build reference file. In its most basic form, `./metro build` only has _three required inputs_.

## 3.1. Required Arguments

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

## 3.3 Optional Arguments
Each of the following arguments are optional and do not need to be provided. 

`-h, --help`            
> **Display Help.**  
> *type: boolean*
> 
> Shows command's synopsis, help message, and an example command
> 
> ***Example:*** 
> `--help`

## 3.3 Example
Build reference files for the run sub comamnd. Follow the setup in [Getting Started](https://ccbr.github.io/METRO/METRO/getting-started/) before this step.

```bash
# login and load interactive session, as described in Getting Started

# download reference files, as needed
wget -P /output/dir/ http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M39/GRCm39.primary_assembly.genome.fa
gunzip /scratch/$USER/METRO/refs/GRCm39.primary_assembly.genome.fa.gz

wget -P /output/dir/ http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M39/gencode.vM36.annotation.gtf
gunzip /scratch/$USER/METRO/refs/gencode.vM36.annotation.gtf.gz

# Build METRO reference files
## Github
module purge
module load cufflinks samtools singularity

## Docker
singularity shell --bind /data/$USER docker://nciccbr/ccbr_metro_v1.4 nciccbr/ccbr_metro_v1.4

## Command
./metro build \
            --ref-fa /scratch/$USER/METRO/GRCm39.primary_assembly.genome.fa \
            --ref-gtf /scratch/$USER/METRO/gencode.vM36.annotation.gtf \
            --output /scratch/$USER/METRO
```