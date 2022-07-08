#!/bin/bash -l
#
# allocate 2 node (8 Cores) for 48 hours
#PBS -l nodes=2:ppn=8,walltime=48:00:00
#
# job name 
#PBS -N GenesFRF1
#
# first non-empty non-comment line ends PBS options

#load required modules (compiler, ...)

module load r/4.0.2-mro

# jobs always start in $HOME - 
# change to work directory
cd  /home/woody/iwbn/iwbn001h/GenesFRF/All

 
# run 
Rscript Genie3.R



