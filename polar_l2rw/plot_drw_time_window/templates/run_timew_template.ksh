#!/bin/ksh
#PBS -N radar
#PBS -l walltime=00:50:00
#PBS -l procs=10 
#PBS -q batch
#PBS -A fv3-cpu
#PBS -o radar.log
#PBS -j oe

import intel
import anaconda/2.3.0

PATH="/home/Donald.E.Lippi/plotting/python/py-ncepbufr/polar_l2rw/plot_drw_time_window/@STAID@"
cd $PATH
/contrib/anaconda/2.3.0/bin/python ./plot_radar_polar_timew_@STAID@.py 
