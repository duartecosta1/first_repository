#!/bin/bash                                                                                                                                                                                                 

#PBS -m ae                                                                                                                                                                                                   
#PBS -P w97                                                                                                                                                                                                  
#PBS -l walltime=1:30:00                                                                                                                                                                                     
#PBS -l mem=32GB                                                                                                                                                                                             
#PBS -l ncpus=4                                                                                                                                                                                              
#PBS -j oe                                                                                                                                                                                                   
#PBS -q express                                                                                                                                                                                              
#PBS -l wd                                                                                                                                                                                                   
#PBS -l other=gdata3                                                                                                                                                                                         
#Run LIS                                                                                                                                                                                                     
#Analysis of Climate extreme indices

#loop through deforestation scales, coupling strength regions, ensemble members

#for def in 001GP 009GP 025GP 081GP 121GP 
#do echo $def

for def2 in 242GP allAMZ 
#001GP 009GP 025GP 081GP 121GP
#
#CTL
#
do echo $def2

#for coup in sc wc
#do echo $coup
#for ens in {0..4}
#do echo $ens

exp=$def2$coup'_E'$ens
members=$def2$coup
#$coup
echo $exp

#Set control experiment as Ensemble mean

#for indice in 
#hfls hfss rss
#do echo $indice
indice=tasmax
#CTL=/g/data3/w97/dc8106/AMZ_def_EXPs/$exp2/$indice'_ANN_AMZDEF_'$exp2'_1978-2011.nc'

CTLensmean=/g/data3/w97/dc8106/AMZ_def_EXPs/analysis/ensmean/$indice/$indice'_MYseasm_AMZDEF_CTL_ensmean_1978-2011.nc'

#Set indice, clean up double time-bounds, set multi-year mean and calculate anomalies
 
#index=/g/data3/w97/dc8106/AMZ_def_EXPs/$exp/$indice'_ANN_AMZDEF_'$exp'_1978-2011.nc'
#index2=/g/data3/w97/dc8106/AMZ_def_EXPs/$exp/$indice'_MYm_AMZDEF_'$exp'_1978-2011_clean.nc'
diff=/g/data3/w97/dc8106/AMZ_def_EXPs/analysis/ensmean/$indice/$indice'_MYseasm_AMZDEF_'$members'_1978-2011_diff_to_CTL.nc'

#cdo timmean -selvar,$indice $index $index2

#Calculate ensemble mean of 'anomalies' files

#indexensmean=/g/data3/w97/dc8106/AMZ_def_EXPs/analysis/ensmean/$indice'_MYm_AMZDEF_'$def$coup'_ensmean_1978-2011_clean.nc'

#echo $def$coup

#ls `find . -name 'txx_MYm_AMZDEF_*'$def$coup'*' -print`
#cd /g/data3/w97/dc8106/AMZ_def_EXPs/analysis/
#cdo ensmean `find . -name 'txx_MYm_AMZDEF_*'$def$coup'*' -print` $indexensmean

#echo -wholename $indexensmean

#Seasonal mean

input=/g/data3/w97/dc8106/AMZ_def_EXPs/$exp/'AMZDEF.daily_tasmin.tasmax.pr.1978_2011_'$exp'.nc'

yseas=/g/data3/w97/dc8106/AMZ_def_EXPs/$exp/$indice'_MYseasm_AMZDEF_'$exp'_1978-2011.nc'

#mon=/g/data3/w97/dc8106/AMZ_def_EXPs/$exp2/$indice'_MON_AMZDEF_'$exp2'_1978-2011.nc'                                                                                                                       #yseas=/g/data3/w97/dc8106/AMZ_def_EXPs/$exp2/$indice'_MYseasm_AMZDEF_'$exp2'_1978-2011.nc'   

#cdo yseasmean -selvar,$indice $input $yseas
#cp $yseas /g/data3/w97/dc8106/AMZ_def_EXPs/analysis/seasonal

#Calculate ensemble mean of seasonal means                                                                                                                                                                

seasensmean=/g/data3/w97/dc8106/AMZ_def_EXPs/analysis/ensmean/$indice/$indice'_MYseasm_AMZDEF_'$members'_ensmean_1978-2011.nc'

#echo $exp

#ls `find . -name 'txx_MYm_AMZDEF_*'$def$coup'*' -print`                                                                                                                                                    

#cd /g/data3/w97/dc8106/AMZ_def_EXPs/analysis/seasonal/                                                                                                                                                  

cdo ensmean `find /g/data3/w97/dc8106/AMZ_def_EXPs/analysis/seasonal/ -name $indice'_MYseasm_AMZDEF_*'$members'*_1978-2011.nc' -print` $seasensmean

#echo -wholename $indexensmean          

#Calculate difference                                                                                                                                                                                       

cdo sub $seasensmean $CTLensmean $diff


done
done
done
#done