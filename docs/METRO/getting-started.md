# 1. Getting Started

## 1.1 Introduction
METRO takes a VCF file(s) and performs filtering and pre-processing for the pipeline input. Then, an MAF-like file containing HGVS terms describing a given mutation and a FASTA file containing transcript sequences are used to determine the consequence of a mutation on a protein product. The *build* sub command can be used to generate a FASTA file containing CDS sequence of each transcript. The *input* sub command will merge and filter MAF files based on user-provided parameters. The *run* sub command will parse and tokenize HGVS terms describing coding DNA mutations. METRO supports each major class of HGVS terms encoding for coding DNA mutations: substitution, deletion, insertions, duplications, and INDELS. METRO _does not_ support HGVS tokenization of terms describing mutations in non-exonic (or non-CDS) regions like introns, 3'-UTR or 5'-UTR. METRO will mutate a given coding DNA sequence based on the provided HGVS term and will translate that sequence into an amino acid sequence. METRO will also truncate a given amino acid sequence +/- N amino acids relativve to a given mutation start site. The *predict* sub command will take the output of the *run* sub command and utilize [netMHCpan](https://services.healthtech.dtu.dk/service.php?NetMHCpan-4.1) to make predictions related to the mutations identified. In addition, it will filter and prepare outputs based on user-provided parameters.

The following are sub-commands used within METRO:

    - build: build reference files
    - prepare: prepare input VAF files
    - find: find mutated protein products
    - predict: predict the binding of peptides to any MHC molecule 

## 1.2 Setup METRO

METRO has two dependencies: PYTHON and netMHCpan. These dependencies can be installed by a sysadmin. Before running the pipeline or any of the commands below, please ensure PYTHON and netMHCHPan are in your $PATH. 

    In addition, the following PYTHON modules are required:
    - argparse
    - pandas
    - xlrd
    - numpy

    Please see follow the instructions below for getting started with the METRO pipeline.

### 1.2.1 Login to cluster

```
# Setup Step 0.) ssh into cluster's head node
# example below for Biowulf cluster
ssh -Y $USER@biowulf.nih.gov
```

### 1.2.2 Grab an interactive node
```
# Setup Step 1.) Please do not run METRO on the head node!
# Grab an interactive node first
srun -N 1 -n 1 --time=12:00:00 -p interactive --mem=8gb  --cpus-per-task=4 --pty bash
```

### 1.2.3 Load dependecies
```
# Setup Step 2.) Add PYTHON executables to $PATH
module purge
module load METRO

# Setup Step 3.) Add netMHCpan executables to $PATH
# NOTE: If you do not have a bashrc file, create one first
[TODO add netMHC pan path here]

# Setup Step 4.) Download METRO and add to $PATH
# Clone the METRO repository from Github
git clone https://github.com/CCBR/METRO.git
export PATH=${PWD}/METRO:${PATH}
```