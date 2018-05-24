#!/bin/bash

#loop through deforestation scales, coupling strength regions, ensemble members                                                                                                                             

for def in 242GP allAMZ CTL
#001GP 009GP 025GP 081GP 121GP                                                                                                                                                                   




do echo $def                                                                                                                                                                                                

#for def2 in CTL
#242GP allAMZ CTL                                                                                                                                                                                           
#do echo $def2

#for coup in sc wc                                                                                                                                                                                         
#do echo $coup                                                                                                                                                                                              

#for ens in {0..4}
#do echo $ens

exp=$def$coup'_E'$ens
#$def$coup'_E'$ens
members=$def$coup
#$coup                                                                                                                                                                                                      
echo $exp

#Set control experiment as Ensemble mean                                                                                                                                                                    

#for indice in hfls hfss rss
#do echo $indice
indice=txx

#Select wc and sc regions
infile='/g/data3/w97/dc8106/AMZ_def_EXPs/'$exp'/'$indice'_MON_AMZDEF_'$exp'_1978-2011.nc'
infile2='/g/data3/w97/dc8106/AMZ_def_EXPs/'$exp'/'$indice'_MON_AMZDEF_'$exp'_1978-2011-clean.nc'
#.daily_tasmin.'$indice'.pr.1978_2011_'$exp'.nc'
ofile='/g/data3/w97/dc8106/AMZ_def_EXPs/'$exp'/'$indice'_MON_sc-only_1978-2011_'$exp'.nc'

sc=-59.375,-39.375,-13.75,-1.25

#cdo selvar,txx $infile $infile2
#rm $infile
#cdo sellonlatbox,$sc $infile2 $ofile

#Seasonal cycle
climatology='/g/data3/w97/dc8106/AMZ_def_EXPs/'$exp'/'$indice'_climatology_sc-only_1978-2011_'$exp'.nc'

#cdo ymonmean $ofile $climatology 

#cp $climatology /g/data3/w97/dc8106/AMZ_def_EXPs/analysis/ensmean/ensemble_members

ensmean='/g/data3/w97/dc8106/AMZ_def_EXPs/analysis/ensmean/'$indice'_climatology_sc-only_1978-2011_'$members'_ensmean.nc'
cdo ensmean `find /g/data3/w97/dc8106/AMZ_def_EXPs/analysis/ensmean/ensemble_members -name $indice'_climatology_sc-only_1978-2011_*'$members'*.nc' -print` $ensmean

done
done
done