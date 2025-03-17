#!/bin/bash
#SBATCH --nodes=1 # node count
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1     # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=200G
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
echo $(date +%y%m%d%H%M)
#python -u nn_ratio_p0.5k.py
echo $(date +%y%m%d%H%M)
python -u nn_ratio.py
echo $(date +%y%m%d%H%M)
echo END
