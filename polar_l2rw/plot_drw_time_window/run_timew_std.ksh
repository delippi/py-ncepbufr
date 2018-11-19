#!/bin/ksh
#PBS -N radar
#PBS -l walltime=00:30:00
#PBS -l procs=10 
#PBS -q debug
#PBS -A fv3-cpu
#PBS -o radar_std.log
#PBS -j oe


PATH="/home/Donald.E.Lippi/plotting/python/py-ncepbufr/polar_l2rw/plot_drw_time_window/"
cd $PATH
/contrib/anaconda/2.3.0/bin/python ./plot_radar_polar_timew_std.py 
