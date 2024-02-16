# 2. Example Usage
A workflow script is provided to allow users the ability to run locally or to submit to Biowulf SLURM.

## 2.1 Runmodes
There are several “flags” which have been created to run the commands. These are `build`, `prepare`, `find`, `predict`
```
bash metro_script.sh build echo
```

## 2.2 Handling Runmodes
There are several options for handing the above runmodes. These include:

1.	echo: this will print the SH file location
2.	cat: this will print the contents of the SH file
3.	sh: this will run the SH file locally
4.	submit_batch: this will run the SH file on the SLURM cluster (use HPC dashboard to monitor)
5.	submit_batch_large: this will run the SH file on the SLURM cluster with “larger” resources 

## 2.3 Examples to run the workflow:
Example printing out the workflow commands to the command line:
```
bash metro_script.sh build cat
bash metro_script.sh prepare cat
bash metro_script.sh find cat
bash metro_script.sh predict cat
```

Example submitting to SLURM:
```
bash metro_script.sh build submit_batch
bash metro_script.sh prepare submit_batch
bash metro_script.sh find submit_batch
bash metro_script.sh predict submit_batch_large
```