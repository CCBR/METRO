#!/bin/sh

###############################################################
# INPUT ARGS
###############################################################
# command line argument for flag
## should be build, prepare, find, predict
flag=$1
## how to handle the flag
## echo: will print the SH file location
## cat: will print the SH file contents
## sh: will run the SH file locally
## submit_batch: will run the SH file on the SLURM cluster
## submit_batch_large: will run the SH file on the SLURM cluster with large settings
calltype=$2
###############################################################
# USER PARAMS
###############################################################
# Update directory paths
METRO_LOC="/data/CCBR_Pipeliner/Pipelines/METRO/metro-dev-sevillas2"
REF_FA="http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M29/GRCm39.primary_assembly.genome.fa.gz"
REF_FA_SHORT="GRCm39.primary_assembly.genome.fa"
REF_GTF="http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M29/gencode.vM29.annotation.gtf.gz"
REF_GTF_SHORT="gencode.vM29.annotation.gtf"
OUTPUT_DIR="/data/sevillas2/metro_fulltest"
INPUT_MAF_FILES="/data/CCBR_Pipeliner/Pipelines/METRO/metro-dev-sevillas2/data/*.maf"

# set variables
prefix="test"
vafFilter="0.2"
passFilter="2"
impactFilter="2"
subsetFilter="30"
alleleList="H-2-Ld,H-2-Dd,H-2-Kb"
peptideLength="8,9,10,11"
kmerLength="21"

###############################################################
# DIRECTORIES
###############################################################
if [[ ! -d $OUTPUT_DIR ]]; then mkdir $OUTPUT_DIR; fi

# set logdir
LOG_DIR="$OUTPUT_DIR/logs"

# set sh dir for logs
sh_dir="$LOG_DIR/sh"
if [[ ! -d $sh_dir ]]; then mkdir -p $sh_dir; fi

# set other dirs
BUILD_DIR=$OUTPUT_DIR/build
if [[ ! -d $BUILD_DIR ]]; then mkdir -p $BUILD_DIR; fi
PREPARE_DIR=$OUTPUT_DIR/prepare
if [[ ! -d $PREPARE_DIR ]]; then mkdir -p $PREPARE_DIR; fi
FIND_DIR=$OUTPUT_DIR/find
if [[ ! -d $FIND_DIR ]]; then mkdir -p $FIND_DIR; fi
PREDICT_DIR=$OUTPUT_DIR/predict
if [[ ! -d $PREDICT_DIR ]]; then mkdir -p $PREDICT_DIR; fi

# prep sh file
sh=$sh_dir/$flag.sh
if [[ -f $sh ]]; then rm $sh; fi
touch $sh

###############################################################
# FUNCTIONS
###############################################################
submit_batch(){
	sbatch --cpus-per-task=16 --verbose \
	--output=$LOG_DIR/%j.out \
	--mem=200g --gres=lscratch:200 --time 02:30:00 \
	--error=$LOG_DIR/%j.err $sh
}

submit_batch_large(){
	sbatch --cpus-per-task=56 --verbose \
	--output=$LOG_DIR/%j.out \
	--mem=200g --gres=lscratch:200 --time 02:30:00 \
	--error=$LOG_DIR/%j.err $sh
}

###############################################################
# COMMANDS
###############################################################
if [[ $flag == "build" ]]; then
    echo "----------------------------"
    echo "--building"

    echo "#!/bin/sh
    export PATH=$PATH:/data/CCBR_Pipeliner/bin/netMHC/netMHCpan-4.1
    module load samtools cufflinks

    if [[ ! -f $BUILD_DIR/$REF_FA_SHORT ]]; then
        if [[ ! -f $BUILD_DIR/$REF_FA_SHORT.gz ]]; then
            echo "----download FA file"
            wget -P $BUILD_DIR $REF_FA
        fi
        echo "----unzip FA file"
        gunzip $BUILD_DIR/$REF_FA_SHORT
    fi

    if [[ ! -f $BUILD_DIR/$REF_GTF_SHORT ]]; then
        if [[ ! -f $BUILD_DIR/$REF_GTF_SHORT.gz ]]; then
            echo "----download GTF file"
            wget -P $BUILD_DIR $REF_GTF
        fi
        echo "----unzip GTF file"
        gunzip $BUILD_DIR/$REF_GTF_SHORT
    fi

    $METRO_LOC/./metro build \
        --ref-fa $BUILD_DIR/$REF_FA_SHORT \
        --ref-gtf $BUILD_DIR/$REF_GTF_SHORT \
        --output $BUILD_DIR" > $sh
    $calltype $sh
fi

if [[ $flag == "prepare" ]]; then
    echo "----------------------------"
    echo "--prepare"

    echo "#!/bin/sh
    export PATH=$PATH:/data/CCBR_Pipeliner/bin/netMHC/netMHCpan-4.1
    $METRO_LOC/./metro prepare \
        --mafFiles $INPUT_MAF_FILES \
        --outputDir $PREPARE_DIR \
        --outprefix $prefix \
        --vafFilter $vafFilter \
        --passFilter $passFilter \
        --impactFilter $impactFilter" > $sh
    $calltype $sh
fi

if [[ $flag == "find" ]]; then
    echo "----------------------------"
    echo "--find"

    # set VAF shorthand
    VAF=`echo $vafFilter | cut -f2 -d"."`
    
    echo "#!/bin/sh
    export PATH=$PATH:/data/CCBR_Pipeliner/bin/netMHC/netMHCpan-4.1
    module load python/3.8
    $METRO_LOC/./metro find \
        --input $PREPARE_DIR/${prefix}_VAF${VAF}0_Variant.csv \
        --output $FIND_DIR \
        --transcripts $BUILD_DIR/transcripts.fa \
        --subset $subsetFilter" > $sh
    $calltype $sh
fi

if [[ $flag == "predict" ]]; then
    echo "----------------------------"
    echo "--predict"

    # set VAF shorthand
    VAF=`echo $vafFilter | cut -f2 -d"."`
    
    # Reads lines and put them in array
    readarray -t array2 <<< "$(sed "s/,/\n/g" <<< "$alleleList")"

    # runs every allele element
    for a in "${array2[@]}"; do
        if [[ ! -d $$PREDICT_DIR/$a ]]; then mkdir $PREDICT_DIR/$a; fi
        predict_log=$PREDICT_DIR/$a/${prefix}_output_netmhc_log_${a}.tsv
        if [[ -f $predict_log ]]; then rm $predict_log; fi
        sh=$sh_dir/${flag}_${a}.sh

        echo "#!/bin/sh
            export PATH=$PATH:/data/CCBR_Pipeliner/bin/netMHC/netMHCpan-4.1
            module load python/3.8

            cd $METRO_LOC
            $METRO_LOC/./metro predict \
                --mutationFile $FIND_DIR/${prefix}_VAF${VAF}0_Variant.metro.tsv \
                --alleleList $a \
                --peptideLength $peptideLength \
                --kmerLength $kmerLength \
                --outputDir $PREDICT_DIR/$a \
                --outprefix $prefix" > $sh
        $calltype $sh
    done
fi