#!/bin/ksh --login
#PBS -N radar_@STAID@_@del_time@
#PBS -l walltime=@walltime@
#PBS -l procs=10 
#PBS -q @queue@
#PBS -A fv3-cpu
#PBS -o radar_@del_time@.log
#PBS -j oe

. /usr/Modules/3.2.10/init/ksh
. /etc/profile
. /etc/profile.d/modules.sh
module load intel
module load anaconda


PATH="/home/Donald.E.Lippi/plotting/python/py-ncepbufr/polar_l2rw/plot_drw_time_window/@STAID@"
cd $PATH
/contrib/anaconda/2.3.0/bin/python ./plot_radar_polar_timew_@STAID@_@del_time@.py 
