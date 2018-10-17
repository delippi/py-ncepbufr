#!/bin/ksh
#PBS -N radar
#PBS -l walltime=00:30:00
#PBS -l procs=10 
#PBS -q debug
#PBS -A fv3-cpu
#PBS -o radar.log
#PBS -j oe

cd /home/Donald.E.Lippi/plotting/python/py-ncepbufr/polar_l2rw

#python /home/Donald.E.Lippi/plotting/python/py-ncepbufr/polar_l2rw/read_bufr.py 
python /home/Donald.E.Lippi/plotting/python/py-ncepbufr/polar_l2rw/plot_radar_polar_timew.py 
