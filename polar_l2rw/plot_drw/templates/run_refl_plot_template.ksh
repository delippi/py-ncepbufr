#!/bin/ksh --login

#SBATCH -J radar_@STAID@_refl 
#SBATCH -t @walltime@
#SBATCH -n 10
#SBATCH -q @queue@
#SBATCH -A fv3-cpu
#SBATCH -o radar_refl.log 
#
#run the executable
set -x

module load intel
module load anaconda/2.3.0

staid="@STAID@"
cd @work@/$staid
# Set up experiment
ANAL_TIME=@ANAL_TIME@
OBS_PATH="@obspath@"

anel0=@anel0@
hh=`echo $ANAL_TIME | cut -c9-10`

OBS_FILE=${OBS_PATH}/nam.t${hh}z.nexrad.tm00.bufr_d
#OBS_FILE=${OBS_PATH}/rap.t${hh}z.nexrad.tm00.bufr_d
cp -p $OBS_FILE ${OBS_FILE}_cpy #make a copy (it helps)

if [[ $hh -ge 00 && $hh -le 09 ]]; then
   (( num=6040+$hh ))
   msg_type=NC00$num #Ex: NC006042 if for 02z and NC006043 is for 03z.
elif [[ $hh -ge 10 && $hh -le 19 ]]; then
   (( num=6040+$hh ))
   msg_type=NC00$num #Ex: NC006052 if for 12z and NC006053 is for 13z.
elif [[ $hh -ge 20 && $hh -le 23 ]]; then
   (( num=6040+$hh ))
   msg_type=NC00$num #Ex: NC006062 if for 22z and NC006063 is for 23z.
fi

# Sets PYTHONPATH correctly for running python in the q.
PYTHONPATH=/contrib/anaconda/EXT/2.3.0/lib/python2.7/site-packages:/scratch2/NCEPDEV/fv3-cam/Jacob.Carley/python/lib64/python

# Run Python Script
/contrib/anaconda/2.3.0/bin/python ./plot_radar_polar_refl_@STAID@.py ${OBS_FILE} ${msg_type} ${ANAL_TIME} ${staid} ${anel0}
echo 'done'

