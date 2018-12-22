#!/bin/ksh --login
#PBS -N radar_@STAID@_@del_time@
#PBS -l walltime=@walltime@
#PBS -l procs=10 
#PBS -q @queue@
#PBS -A fv3-cpu
#PBS -o radar_@del_time@.log
#PBS -j oe

module load intel
module load anaconda/2.3.0

# Sets PYTHONPATH correctly for running python in the q.
PYTHONPATH=/contrib/anaconda/EXT/2.3.0/lib/python2.7/site-packages:/scratch4/NCEPDEV/meso/save/Jacob.Carley/python/lib64/python:/scratch4/NCEPDEV/meso/save/Donald.E.Lippi/python/lib64/python

PATH="/home/Donald.E.Lippi/plotting/python/py-ncepbufr/polar_l2rw/plot_drw_time_window/@STAID@"
cd $PATH
/contrib/anaconda/2.3.0/bin/python ./plot_radar_polar_timew_@STAID@_@del_time@.py 
