#!/bin/bash
#SBATCH --nodes=1 # node count
#SBATCH --sockets-per-node=1
#SBATCH --cores-per-socket=4
#SBATCH --threads-per-core=1
#SBATCH --mem-per-cpu=100G
#SBATCH -t 00:30:00
# Sends mail when process begins, and when it ends. 
# Make sure you define your email
#SBATCH --mail-type=all
#SBATCH --mail-user=cw55@princeton.edu

###################################################################
#Script Name : run_notebook_analysis
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
module load anaconda3/2022.5

source /usr/licensed/anaconda3/2022.5/etc/profile.d/conda.sh
conda activate cg310
which python
date_v=$(date +%y%m%d%H%M)
exec=rad_GCM_nn_dev
jupyter nbconvert --to notebook --execute $exec --output $exec.$date_v
exec=diag_GCM_nn_y2000
jupyter nbconvert --to notebook --execute $exec --output $exec.$date_v
exec=diag_GCM_nn_clm
jupyter nbconvert --to notebook --execute $exec --output $exec.$date_v
