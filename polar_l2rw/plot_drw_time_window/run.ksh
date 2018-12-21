#!/bin/ksh

#This script loops over the specified radars (from station ids list) and
#computes the mean, standard deviation, and variance from the bufr ob file.

STAIDS="KFDR KFWS KGLD KGRK KICT KINX KLNX KRTX KTLX KVNX" #What radars would you like to process? 
anel0=0.5  #and at what elevation angle?
del_times="0.5 0.125" #and at what temporal time window? 0.125 == +/-7.5 (15min window)
queue="batch"

#Loop over radars
for STAID in $STAIDS; do
    for del_time in $del_times; do
       if   [[ $del_time  == "0.5"  ]]; then
          walltime=00:45:00 #walltime for hour window jobs
       elif [[ $del_time == "0.125" ]]; then
          walltime=00:30:00 #walltime for 15min window jobs
       fi
       echo $STAID $del_time
       mkdir -p $STAID #make a directory for each station id.
       cd $STAID       #move into the newly created directory.

       #copy the template files to the corresponding directory and rename for the station id.
       cp ../templates/plot_radar_polar_timew_template.py     ./plot_radar_polar_timew_${STAID}_${del_time}.py
       cp ../templates/plot_radar_polar_timew_std_template.py ./plot_radar_polar_timew_std_${STAID}_${del_time}.py
       cp ../templates/run_timew_template.ksh                 ./run_timew_${STAID}_${del_time}.ksh
       cp ../templates/run_timew_std_template.ksh             ./run_timew_std_${STAID}_${del_time}.ksh

       #modifiy the variables in the template copies escaped by "@" on either side of the variable.
       sed -i "s/@STAID@/${STAID}/g"       ./plot_radar_polar_timew_${STAID}_${del_time}.py
       sed -i "s/@anel0@/${anel0}/g"       ./plot_radar_polar_timew_${STAID}_${del_time}.py
       sed -i "s/@del_time@/${del_time}/g" ./plot_radar_polar_timew_${STAID}_${del_time}.py
   
       sed -i "s/@STAID@/${STAID}/g"       ./plot_radar_polar_timew_std_${STAID}_${del_time}.py
       sed -i "s/@anel0@/${anel0}/g"       ./plot_radar_polar_timew_std_${STAID}_${del_time}.py
       sed -i "s/@del_time@/${del_time}/g" ./plot_radar_polar_timew_std_${STAID}_${del_time}.py

       sed -i "s/@STAID@/${STAID}/g"       ./run_timew_${STAID}_${del_time}.ksh
       sed -i "s/@del_time@/${del_time}/g" ./run_timew_${STAID}_${del_time}.ksh
       sed -i "s/@walltime@/${walltime}/g" ./run_timew_${STAID}_${del_time}.ksh
       sed -i "s/@queue@/${queue}/g"       ./run_timew_${STAID}_${del_time}.ksh

       sed -i "s/@STAID@/${STAID}/g"       ./run_timew_std_${STAID}_${del_time}.ksh
       sed -i "s/@del_time@/${del_time}/g" ./run_timew_std_${STAID}_${del_time}.ksh
       sed -i "s/@walltime@/${walltime}/g" ./run_timew_std_${STAID}_${del_time}.ksh
       sed -i "s/@queue@/${queue}/g"       ./run_timew_std_${STAID}_${del_time}.ksh

       #submit the job to the queue to make the mean and std 2d wind plots.
       qsub ./run_timew_${STAID}_${del_time}.ksh
       qsub ./run_timew_std_${STAID}_${del_time}.ksh


       #move up one directory to process the next radar
       cd ..
   done
done

