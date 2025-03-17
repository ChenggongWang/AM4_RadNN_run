#!/bin/bash
#SBATCH --nodes=1 # node count
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1     # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=100G
#SBATCH -t 24:00:00
# Sends mail when process begins, and when it ends. 
# Make sure you define your email
#SBATCH --mail-type=all
#SBATCH --mail-user=cw55@princeton.edu

###################################################################
#Script Name : run_nn_ratio.sh
#Description : ~
#Args        :
#Author      : Chenggong Wang
#Email       : c.wang@princeton.edu
###################################################################

set -e #end with any error
#set -x #expands variables and prints a little + sign before the line
# load modules or conda environments here
source /usr/share/Modules/init/bash

module purge
module load anaconda3/2023.3

source /usr/licensed/anaconda3/2023.3/etc/profile.d/conda.sh
conda activate cg310
which python
echo "Date:"
echo $(date +%y%m%d%H%M)
ROOT=$PWD
echo "Current dir:"
echo $ROOT
for f in $ROOT/*8xdaily*.nc
do 
    echo "$f"
    new_f="$f.monavg_error.nc"
    if test -f "$new_f"; then
        echo "$new_f exists."
    else
        # echo "$new_f not exists."
        # cdo monavg "$f" "$new_f"
        python -u monthavg_erorr_file.py --filename "$f"
    fi

done
python -u regrid_monthave_error.py --input_directory "$ROOT"
echo $(date +%y%m%d%H%M)
echo END
