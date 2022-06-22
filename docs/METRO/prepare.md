# 3. Prepare Synopsis
The `./metro` executable is composed of several inter-related sub commands. Please see `./metro -h` for all available options. The synopsis for the sub command `prepare` shows its parameters and their usage. Optional parameters are shown in square brackets.

```
$ ./metro prepare [-h] --mafFiles MAFFILES \
                      --outputdir OUTPUTdir \
                      --outputprefix OUTPUTprefix \
                      [--vafFilter VAFFILTER] \
                      [--passFilter PASSFILTER] \
                      [--impactFilter IMPACTFILTER]
```

This part of the documentation describes options and concepts for `./metro prepare` sub command in more detail. With minimal configuration, the `prepare` sub command enables you to create filtered MAF files for the metro `run` pipeline.

## 3.1 Required Arguments
Each of the following arguments are required. Failure to provide a required argument will result in a non-zero exit-code.
`--mafFiles MAFFILES [MAFFILES ...]`  
> **Input MAF-like file(s) to process.**  
> *type: file*  
> 
> Input VCF file(s) in MAF format. Provide a minimum of two files, separated by a comma.
> 
> ***Example:*** 
> `--mafFiles data/test1.maf,data/test2.maf`
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
> ` --outputprefix test`

## 3.2 Optional Arguments
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
  `--vafFilter VAFFilter`
> **Filter for VAF values.**   
> *type: numeric*
>   
> Minimum value for average VAF, calculated as t_alt_count/t_depth, to be included.
> 
> ***Example:*** 
> `--vafFilter 0.2`
---
  `--passFilter PASSFILTER`
> **Filter for PASS values.**   
> *type: numeric*
>   
> Minimum number of input files with a filter rating of "PASS", to be included.
> 
> ***Example:*** 
> `--passFilter 2`
---
  `--impactFilter IMPACTFILTER`
> **Filter for IMPACT values.**   
> *type: numeric*
>   
> Minimum number of input files with an IMPACT rating of "MODERATE" or "HIGH", to be included.
> 
> ***Example:*** 
> `--impactFilter 2`

## 3.3 Example
Filter MAF files in preparation of metro run.

```bash 
# Step 0.) Grab an interactive node
# Do not run on head node!
srun -N 1 -n 1 --time=12:00:00 -p interactive --mem=8gb  --cpus-per-task=4 --pty bash
module purge
module load python/3.5

 # Step 1.) Run METRO subcommand PREPARE to prepare files for processing
 ./metro prepare \
            --mafFiles /data/*.maf \
            --outputDir /scratch/$USER/METRO \
            --outprefix test \
            --vafFilter 0.2 \
            --passFilter 2 \
            --impactFilter 2
```
