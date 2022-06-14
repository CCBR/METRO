# 5. Predict Synopsis
The `./metro` executable is composed of several inter-related sub commands. Please see `./metro -h` for all available options. The synopsis for the sub command `predict` shows its parameters and their usage. Optional parameters are shown in square brackets.

```
$ ./ metro predict [-h] --mutationFile MUTATIONFILE \
                              --alleleList ALLELELIST \
                              --outputdir OUTPUTDIR \
                              --outprefix OUTPREFIX \
                              [--kmerLength KMERLENGTH] \
                              [--peptideLength PEPTIDELENGTH] \
                              [--highbind HIGHBIND] \
                              [--lowbind LOWBIND]
```

This part of the documentation describes options and concepts for `./metro input` sub command in more detail. With minimal configuration, the `predict` sub command enables you to generate prediction files for each mutated sequence identified in the metro `run` sub command.

## 5.1 Required Arguments
Each of the following arguments are required. Failure to provide a required argument will result in a non-zero exit-code.

`--mutationFile MUTATIONFILE [MUTATIONFILE ...]`  
> **Input TSV mutation file to process.**  
> *type: file*  
> 
> Input file in tsv format. This can be the output of the METRO run command
> 
> ***Example:*** 
> `--mutationFile data/test_Variant.metro.tsv`
>
> ***Required headers:***
> Required header (in any order):
> - Variant_Classification
> - Hugo_Symbol	
> - Transcript_ID
> - WT_Subset_AA_Sequence
> - Mutated_Subset_AA_Sequence
---  
  `--outputdir OUTPUTDIR`
> **Path to an output directory.**   
> *type: path*
>   
> This location is where the metro will create all of its output files, also known as the pipeline's working directory. If the provided output directory does not exist, it will be created automatically.
> 
> ***Example:*** 
> `--outputdir /scratch/$USER/RNA_hg38`
---  
  `--outputprefix OUTPUTPREFIX`
> **Output file prefix.**   
> *type: prefix*
>   
> Prefix for sample output files.
> 
> ***Example:*** 
> `--outputprefix test`
---  
  `--alleleList ALLELELIST`
> **List of Alleles for netMHCpan input.**   
> *type: list*
>   
> Allele name(s) to input into netMHCpan. If this is a list, each allele is separated by commas and without spaces (max 20 per submission). For full list of alleles is available on netMHC's [website](https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/MHC_allele_names.txt)
> 
> ***Example:*** 
> `--alleleList H-2-Ld,H-2-Dd,H-2-Kb`

## 5.2 Optional Arguments
Each of the following arguments are optional and do not need to be provided. Default values listed in each example will be used, if value not provided.

  `-h, --help`            
> **Display Help.**  
> *type: boolean*
> 
> Shows command's synopsis, help message, and an example command
> 
> ***Example:*** 
> `--help`
---  
  `--kmerLength KMERLENGTH`
> **Length of kmer for netMHC input.**   
> *type: numeric*
>   
> Single value, or list, of the length of peptide sequence used for prediction analysis. If this is a list, each length is separated by a comma and without spaces.
> 
> ***Example:*** 
> `--peptideLength 8,9,10,11`
---
  `--highbind HIGHBIND`
> **Threshold for identifying STRONG affinity.**   
> *type: numeric*
>   
> Threshold to define binding affinity as "STRONG" for netHMC output. Must be an integer that is lower than `--lowbind`.
> 
> ***Example:*** 
> `--highbind 0.5`
---
  `--lowbind LOWBIND`
> **Filter for IMPACT values.**   
> *type: numeric*
>   
> Threshold to define binding affinity as "WEAK" for netHMC output. Must be an integer that is higher than `--highbind`.
> 
> ***Example:*** 
> `--lowbind 2`

## 5.3 Example
Predict the binding of peptides to any MHC molecule of known sequence using artificial neural networks (ANNs) and perform filtering of output based on user-provided parameters.

```bash 
# Step 0.) Grab an interactive node
# Do not run on head node!
srun -N 1 -n 1 --time=12:00:00 -p interactive --mem=8gb  --cpus-per-task=4 --pty bash
module purge
module load python/3.5

 # Step 1.) Run METRO predict to find the binding of peptides to any MHC molecule
 ./metro predict \
                --mutationFile /scratch/$USER/METRO/test_Variant.asap.tsv \
                --allelList H-2-Ld,H-2-Dd,H-2-Kb \
                --peptideLength 8,9,10,11 \
                --kmerLength 21 \
                --outputdir /scratch/$USER/METRO/ \
                --outprefix test
```
