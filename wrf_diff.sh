#!/bin/bash

runame='CONUS-RRTM_1hourly'
label='1day-only'
'SAmerica_CORDEX_Noah-MP'
'SAmerica_CORDEX_land_default'
#"TROPICAL"
#"SAmerica_CORDEX_Noah-MP"

#'SAmerica_CORDEX'

inpath='/g/data3/w97/dc8106/WRF_runs/Era-Interim/WRF_outputs/runs'

wrfout='wrfout_d01_2012-09-11_00:00:00'

#Extract 
echo $wrfout
#cp '/short/w97/dc8106/WRF/WRFV3/run/'$wrfout $inpath'/'$runame'_'$wrfout'.nc'
#'/short/w97/dc8106/WRF/WRFV3/run/wrfout_d01_2012-08-27_00:00:00' $inpath'/'$runame'_wrfout_d01_2012-08-27.nc'

for var in SST T2 PSFC
do 
echo $var
outpath='/g/data3/w97/dc8106/WRF_runs/Era-Interim/VALIDATION/'$var
echo $outpath

wrf=$inpath'/'$runame'_'$wrfout'.nc'

#forc2='/g/data3/w97/dc8106/WRF_runs/Era-Interim/VALIDATION/Erai-variables/'$var'_'$forcing'_remapnn_sept2012.nc'
#metgrid='/g/data3/w97/dc8106/WRF_runs/Era-Interim/VALIDATION/Erai-variables/'$var_'metgrid_sept2012.nc'

field=$outpath'/'$runame'_'$var'_'$label'.nc'
field2=$outpath'/'$runame'_'$var'_'$label'_remapnn.nc'

cdo selvar,$var $wrf $field
#-seldate,2012-09-01T00:00:00,2012-09-30T18:00:00 


if [ "$var" == "T2" ]
then
	#Interpolate by the nearest neighbour the finer dataset (WRF) to coarser one (ERAI)
	forcing='erai'
	echo $forcing $var
	forc='/g/data3/w97/dc8106/WRF_runs/Era-Interim/VALIDATION/Erai-variables/'$var'_'$forcing'_sept2012_SAmerica.nc'
	cdo remapnn,$forc $field $field2
	diff=$outpath'/'$runame'_'$var'_DIFF_TO_'$forcing'_'$label'.nc'
	cdo sub -seldate,2012-09-11T00:00:00,2012-09-12T00:00:00 $field2 $forc $diff

else 
	[ "$forcing"="metgrid"]

#rm $forc
cdo sub -seldate,2012-09-11T00:00:00,2012-09-12T00:00:00 $field $forc $diff

fi
done
