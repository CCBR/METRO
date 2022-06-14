# 2. Build Synposis

The `./metro` executable is composed of several inter-related sub commands. Please see `./metro -h` for all available options. The synopsis for the sub command `build` shows its parameters and their usage. Optional parameters are shown in square brackets.

```
$ ./metro build [-h] --ref-fa REF_FA \
                --ref-gtf REF_GTF \
                --output  OUTPUT 
```

This part of the documentation describes options and concepts for the `./metro build` sub command in more detail. With minimal configuration, the build sub command enables you to build reference file. In its most basic form, `./metro build` only has _three required inputs_.

## 2.1. Required Arguments

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

## 2.2 Optional Arguments
Each of the following arguments are optional and do not need to be provided. 

`-h, --help`            
> **Display Help.**  
> *type: boolean*
> 
> Shows command's synopsis, help message, and an example command
> 
> ***Example:*** 
> `--help`

## 2.3 Example
Build reference files for the run sub comamnd.

```bash 
# Step 0.) Grab an interactive node
# Do not run on head node!
srun -N 1 -n 1 --time=12:00:00 -p interactive --mem=8gb  --cpus-per-task=4 --pty bash
module purge
module load cufflinks samtools

# Step 1.) Build METRO reference files
metro build --ref-fa GRCm39.primary_assembly.genome.fa \
            --ref-gtf gencode.vM26.annotation.gtf \
            --output /scratch/$USER/METRO/refs/
```
