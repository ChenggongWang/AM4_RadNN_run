#!/bin/bash

###################################################################
#Script Name : auto_test.sh
#Description : compile AM4 and run dev test
#Args        :
#Author      : Chenggong Wang
#Email       : c.wang@princeton.edu
###################################################################
set -e #end with any error
#set -x #expands variables and prints a little + sign before the line
dev=/scratch/gpfs/cw55/AM4_NN/AM4_RadNN_run/test_dev
exec=/scratch/gpfs/cw55/AM4_NN/exec

cd $exec
pwd
source /scratch/gpfs/cw55/AM4_NN/exec/set_env.sh 
make
cd $dev
pwd
rm -rf work/*
sbatch run_AM4_CTL1990s_radnn
echo end
exit 

