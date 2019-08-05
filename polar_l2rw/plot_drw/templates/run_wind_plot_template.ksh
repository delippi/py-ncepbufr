#!/bin/ksh --login

#SBATCH -J radar_@STAID@_wind 
#SBATCH -t @walltime@
#SBATCH -n 10
#SBATCH -q @queue@
#SBATCH -A fv3-cpu
#SBATCH -o radar_wind.log 
#
#run the executable
set -x

module load intel
module load anaconda/2.3.0

cd /home/Donald.E.Lippi/plotting/python/py-ncepbufr/polar_l2rw/plot_drw/@STAID@
# Set up experiment
ANAL_TIME=@ANAL_TIME@
OBS_PATH=/scratch4/NCEPDEV/meso/save/Donald.E.Lippi/gsi/data/obsfiles/$ANAL_TIME/

staid="@STAID@"
anel0=@anel0@
hh=`echo $ANAL_TIME | cut -c9-10`

#OBS_FILE=${OBS_PATH}/rap.t${hh}z.nexrad.tm00.bufr_d
OBS_FILE=${OBS_PATH}/nam.t${hh}z.nexrad.tm00.bufr_d
#OBS_FILE=${OBS_PATH}/rap.t${hh}z.nexrad.tm00.bufr_d
if [[ $hh -ge 00 && $hh -le 09 ]]; then
   (( num=6010+$hh )) 
   msg_type=NC00$num #Ex: NC006012 if for 02z and NC006013 is for 03z.
elif [[ $hh -ge 10 && $hh -le 19 ]]; then
   (( num=6010+$hh )) 
   msg_type=NC00$num #Ex: NC006022 if for 12z and NC006023 is for 13z.
elif [[ $hh -ge 20 && $hh -le 23 ]]; then
   (( num=6010+$hh )) 
   msg_type=NC00$num #Ex: NC006032 if for 22z and NC006033 is for 23z.
fi


# Sets PYTHONPATH correctly for running python in the q.
PYTHONPATH=/contrib/anaconda/EXT/2.3.0/lib/python2.7/site-packages:/scratch4/NCEPDEV/meso/save/Jacob.Carley/python/lib64/python:/scratch4/NCEPDEV/meso/save/Donald.E.Lippi/python/lib64/python


# Run Python Script
/contrib/anaconda/2.3.0/bin/python ./plot_radar_polar_@STAID@.py ${OBS_FILE} ${msg_type} ${ANAL_TIME} ${staid} ${anel0}

echo 'done'


