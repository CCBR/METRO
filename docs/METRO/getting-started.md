# 1. Getting Started

## 1.1 Introduction
METRO takes a VCF file(s) and performs filtering and pre-processing for the pipeline input. Then, an MAF-like file containing HGVS terms describing a given mutation and a FASTA file containing transcript sequences are used to determine the consequence of a mutation on a protein product. The *build* sub command can be used to generate a FASTA file containing CDS sequence of each transcript. The *input* sub command will merge and filter MAF files based on user-provided parameters. The *run* sub command will parse and tokenize HGVS terms describing coding DNA mutations. METRO supports each major class of HGVS terms encoding for coding DNA mutations: substitution, deletion, insertions, duplications, and INDELS. METRO _does not_ support HGVS tokenization of terms describing mutations in non-exonic (or non-CDS) regions like introns, 3'-UTR or 5'-UTR. METRO will mutate a given coding DNA sequence based on the provided HGVS term and will translate that sequence into an amino acid sequence. METRO will also truncate a given amino acid sequence +/- N amino acids relativve to a given mutation start site. The *predict* sub command will take the output of the *run* sub command and utilize [netMHCpan](https://services.healthtech.dtu.dk/service.php?NetMHCpan-4.1) to make predictions related to the mutations identified. In addition, it will filter and prepare outputs based on user-provided parameters.

The following are sub-commands used within METRO:

    - build: build reference files
    - prepare: prepare input VAF files
    - find: find mutated protein products
    - predict: predict the binding of peptides to any MHC molecule 

## 1.2 Setup Dependencies

METRO has two dependencies: PYTHON and netMHCpan. These dependencies can be installed by a sysadmin. Before running the pipeline or any of the commands below, please ensure PYTHON and netMHCHPan are in your $PATH. 

    In addition, the following PYTHON modules are required:
    - argparse
    - pandas
    - xlrd
    - numpy

CUFFLINKS

SAMTOOLS


### 1.3 Login to cluster
```
# ssh into cluster's head node
ssh -Y $USER@biowulf.nih.gov
```

### 1.4 Prepare an interactive node
```
# Grab an interactive node first
sinteractive

# Add PYTHON executables to $PATH 
# NOTE: If you do not have a bashrc file, create one first

# Add netMHCpan executables to $PATH
# NOTE: If you do not have a bashrc file, create one first
export PATH=$PATH:/data/CCBR_Pipeliner/bin/netMHC/netMHCpan-4.1
```

## 1.5 Setup METRO through either GitHub or Docker
The tool is available on both [GitHub](https://github.com/CCBR/METRO) or on [DockerHub](https://hub.docker.com/r/nciccbr/ccbr_metro_v1.4).

### 1.5.1 Clone the METRO repository from Github
```
git clone https://github.com/CCBR/METRO.git
export PATH=${PWD}/METRO:${PATH}
# run subcommands
```

### 1.5.2 Pull Docker Image
# Review subcommands before loading singularity, as other dependencies may need to be included.
```
module load singularity
singularity shell --bind /data/$USER docker://nciccbr/ccbr_metro_v1.4 nciccbr/ccbr_metro_v1.4
# run subcommand
```