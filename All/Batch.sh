#!/bin/bash -l
#
# allocate 1 node (4 Cores) for 96 hours
#PBS -l nodes=1:ppn=4,walltime=96:00:00
#
# job name 
#PBS -N GenesFRF1
#
# first non-empty non-comment line ends PBS options

#load required modules (compiler, ...)
module load python
module load r/4.0.2-mro

# jobs always start in $HOME - 
# change to work directory
cd  /home/woody/iwbn/iwbn001h/GenesFRF/All

 
# run 
python evaluation.py

