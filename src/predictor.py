#!/usr/bin/env python3

"""predictor.py: runs netMHC prediction jobs in parallel for each allele provided.
USAGE:
  python3 predictor.py alleleList inputFile peptideLength im_prefix output_file
  --alleleList: list of alleles for netMHC separated by commas [H-2-Ld,H-2-Dd]
  --inputFile: filtered file obtained from predict sub-command
  --peptideLength: passed sys.arg of peptide lengths separated by commas [8,9]
  --im_prefix: path and prefix of intermediate netMHC output file [/path/to/output/netmhc_]
  --output_file: path and prefix of the raw netMHC, merged, output file [/path/to/output/output_netmhc_raw.tsv]
"""

from __future__ import print_function
import sys, os, subprocess
import ray

def bash(cmd, interpreter='/bin/bash', strict=True, **kwargs):
    """
    Interface to run a process or bash command. Using subprocess.call_check()
    due to portability across most python versions. It was introduced in python 2.5
    and it is also interoperabie across all python 3 versions. 
    @param cmd <str>:
        Shell command to run
    @param interpreter <str>:
        Interpreter for command to run [default: bash]
    @pararm strict <bool>:
        Prefixes any command with 'set -euo pipefail' to ensure process fail with
        the expected exit-code  
    @params kwargs <check_call()>:
        Keyword arguments to modify subprocess.check_call() behavior
    @return exitcode <int>:
        Returns the exit code of the run command, failures return non-zero exit codes
    """
    # Changes behavior of default shell
    prefix = ''
    # set -e: exit immediately upon error
    # set -u: treats unset variables as an error
    # set -o pipefail: exits if a error occurs in any point of a pipeline
    if strict: prefix = 'set -euo pipefail; '

    exitcode = subprocess.check_call(prefix + cmd, shell = True, executable = interpreter, **kwargs)

    if exitcode != 0: 
        fatal("""\n\tFatal: Failed to run '{}' command!
        └── Command returned a non-zero exitcode of '{}'.
        """.format(process, exitcode)
        )

    return exitcode

# run netMHCpan on individual allele with RAY parallelizing jobs
@ray.remote 
def run_netMHC(alleleid, netMHC_input, peptideLength, netmhc_intermed): 
    print("RUNNING " + alleleid)
    
    # set output intermed file names
    netmhc_raw=str(netmhc_intermed+"raw_"+alleleid+".tsv")
    netmhc_log=str(netmhc_intermed+"log_"+alleleid+".tsv")
    
    # Run NETMHCPAN
    # netHMC -f $file -a alleleList -l pepetidelength
    # -xls -xlsfile /ouput/dir/outprefix_output_netmhc_raw.tsv > outprefix_netmhc_log.tsv
    process = "{} -f {} -a {} -l {} -BA -xls -xlsfile {} > {}".format(
        "netMHCpan", 
        netMHC_input,
        alleleid,
        peptideLength,
        netmhc_raw,
        netmhc_log
    )
    
    print("--Running: " + process)
    exitcode = bash(process)

    return netmhc_raw

if __name__ == '__main__':

    # List of alleles to process
    list_in=sys.argv[1]
    alleleList=list_in.split(",")

    # Number of concurrent tasks
    # or remote workers.
    try: threads = int(sys.argv[5])
    except ValueError: threads = 4

    # Initialize a ray cluster
    # with X remote workers
    ray.init(num_cpus = threads)

    # set args
    netMHC_input=sys.argv[2]
    peptideLength=sys.argv[3]
    netmhc_intermed=sys.argv[4]

    # run netMHC in parallel
    result_ids = [run_netMHC.remote(id, netMHC_input, peptideLength, netmhc_intermed) for id in alleleList] 