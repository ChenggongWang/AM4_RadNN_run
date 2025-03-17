#!/bin/bash
#SBATCH --nodes=1 # node count
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=120G
#SBATCH -t 06:30:00
# Sends mail when process begins, and when it ends. 
# Make sure you define your email
#SBATCH --mail-type=all
#SBATCH --mail-user=cw55@princeton.edu

###################################################################
#Script Name : run_notebook_analysis
#Description : run and save the notebook via slurm
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
date_v=$(date +%y%m%d%H%M)
#exec=rad_GCM_nn_dev
#echo $(date +%y%m%d%H%M)
#jupyter nbconvert --to notebook --execute $exec --output $exec.$date_v
#exec=diag_GCM_nn_y2000
#echo $(date +%y%m%d%H%M)
#jupyter nbconvert --to notebook --execute $exec --output $exec.$date_v
# exec=diag_GCM_nn_clm
# echo $(date +%y%m%d%H%M)
# jupyter nbconvert --to notebook --execute $exec --output $exec.$date_v
# echo $(date +%y%m%d%H%M)

exec=diag_GCM_nn_on_test2000s
echo $(date +%y%m%d%H%M)
jupyter nbconvert --to notebook --execute $exec --output $exec.$date_v
echo $(date +%y%m%d%H%M)

echo END
