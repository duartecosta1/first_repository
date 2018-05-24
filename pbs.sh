#!/bin/bash                                                                                                                                                                                                 

#PBS -m ae                                                                                                                                                                                                  
#PBS -P w97                                                                                                                                                                                                
#PBS -l walltime=1:30:00                                                                                                                                                                                    
#PBS -l mem=32GB                                                                                                                                                                                            
#PBS -l ncpus=4                                                                                                                                                                                             
#PBS -j oe                                                                                                                                                                                                 
#PBS -q express                                                                                                                                                                                            
#PBS -l wd                                                                                                                                                                                                 

module use /g/data3/hh5/public/modules  
module load conda/analysis27-18.01
python pdfplot.py
