#!/bin/ksh

#This script loops over the specified radars (from station ids list) and
#computes the mean, standard deviation, and variance from the bufr ob file.

STAIDS="KFDR KFWS KGLD KGRK KICT KINX KLNX KRTX KTLX KVNX" #What radars would you like to process? 
#STAIDS="KGRK" #What radars would you like to process? 
anel0=0.5  #and at what elevation angle?
walltime=00:20:00
queue="batch"

#Loop over radars
for STAID in $STAIDS; do
       echo $STAID
       mkdir -p $STAID #make a directory for each station id.
       cd $STAID       #move into the newly created directory.

       #copy the template files to the corresponding directory and rename for the station id.
       #cp ../templates/run_l2rw_plot_template.ksh.qsub        ./run_l2rw_plot_${STAID}.ksh.qsub
       cp ../templates/run_wind_plot_template.ksh             ./run_wind_plot_${STAID}.ksh
       cp ../templates/run_refl_plot_template.ksh             ./run_refl_plot_${STAID}.ksh
       cp ../templates/plot_radar_polar_ref_template.py       ./plot_radar_polar_ref_${STAID}.py
       cp ../templates/plot_radar_polar_template.py           ./plot_radar_polar_${STAID}.py


       #modifiy the variables in the template copies escaped by "@" on either side of the variable.
       sed -i "s/@STAID@/${STAID}/g"       ./plot_radar_polar_${STAID}.py

       sed -i "s/@STAID@/${STAID}/g"       ./plot_radar_polar_ref_${STAID}.py

       sed -i "s/@STAID@/${STAID}/g"       ./run_wind_plot_${STAID}.ksh
       sed -i "s/@walltime@/${walltime}/g" ./run_wind_plot_${STAID}.ksh
       sed -i "s/@queue@/${queue}/g"       ./run_wind_plot_${STAID}.ksh
       sed -i "s/@anel0@/${anel0}/g"       ./run_wind_plot_${STAID}.ksh

       sed -i "s/@STAID@/${STAID}/g"       ./run_refl_plot_${STAID}.ksh
       sed -i "s/@walltime@/${walltime}/g" ./run_refl_plot_${STAID}.ksh
       sed -i "s/@queue@/${queue}/g"       ./run_refl_plot_${STAID}.ksh
       sed -i "s/@anel0@/${anel0}/g"       ./run_refl_plot_${STAID}.ksh

       #submit the job to the queue to make the mean and std 2d wind plots.
       #qsub ./run_l2rw_plot_${STAID}.ksh.qsub
       qsub ./run_wind_plot_${STAID}.ksh
       qsub ./run_refl_plot_${STAID}.ksh


       #move up one directory to process the next radar
       cd ..
done


