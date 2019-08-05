#!/bin/ksh

#This script loops over the specified radars (from station ids list) and
#computes the mean, standard deviation, and variance from the bufr ob file.

STAIDS="KFDR KFWS KGLD KGRK KICT KINX KLNX KRTX KTLX KVNX" #What radars would you like to process? 
STAIDS="KGRK" #What radars would you like to process? 
STAIDS="KPOE_KSHV_KSRX" #What radars would you like to process? 
STAIDS="KSHV" #What radars would you like to process? 
#STAIDS="KTWX" #What radars would you like to process? 
#STAIDS="KGRK" #What radars would you like to process? 
#0.5 0.9 1.3 1.8 2.4 3.4...
anel0=0.5  #and at what elevation angle?
walltime=00:20:00
queue="batch"
#ANAL_TIME=2015103018
#ANAL_TIME=2015103110
ANAL_TIME=2019051906
histogram=".false."
set -x
#Loop over radars
for STAID in $STAIDS; do
       echo $STAID
       mkdir -p $STAID #make a directory for each station id.
       cd $STAID       #move into the newly created directory.

       #copy the template files to the corresponding directory and rename for the station id.
       #cp ../templates/run_l2rw_plot_template.ksh.qsub        ./run_l2rw_plot_${STAID}.ksh.qsub
       if [[ $histogram == ".true." ]]; then
          cp ../templates/plot_radar_polar_hist_template.py      ./plot_radar_polar_hist_${STAID}.py
          cp ../templates/run_wind_plot_hist_template.ksh        ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s/@STAID@/${STAID}/g"       ./plot_radar_polar_hist_${STAID}.py
          sed -i "s/@ANAL_TIME@/${ANAL_TIME}/g" ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s/@STAID@/${STAID}/g"         ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s/@walltime@/${walltime}/g"   ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s/@queue@/${queue}/g"         ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s/@anel0@/${anel0}/g"         ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s/@histogram@/${histogram}/g" ./run_wind_plot_hist_${STAID}.ksh
          #sbatch ./run_wind_plot_hist_${STAID}.ksh
          ksh ./run_wind_plot_hist_${STAID}.ksh

       else
          cp ../templates/run_wind_plot_template.ksh             ./run_wind_plot_${STAID}.ksh
          cp ../templates/plot_radar_polar_template.py           ./plot_radar_polar_${STAID}.py
          sed -i "s/@STAID@/${STAID}/g"       ./plot_radar_polar_${STAID}.py
          sed -i "s/@ANAL_TIME@/${ANAL_TIME}/g" ./run_wind_plot_${STAID}.ksh
          sed -i "s/@STAID@/${STAID}/g"         ./run_wind_plot_${STAID}.ksh
          sed -i "s/@walltime@/${walltime}/g"   ./run_wind_plot_${STAID}.ksh
          sed -i "s/@queue@/${queue}/g"         ./run_wind_plot_${STAID}.ksh
          sed -i "s/@anel0@/${anel0}/g"         ./run_wind_plot_${STAID}.ksh
          sed -i "s/@histogram@/${histogram}/g" ./run_wind_plot_${STAID}.ksh

          cp ../templates/run_refl_plot_template.ksh             ./run_refl_plot_${STAID}.ksh
          cp ../templates/plot_radar_polar_ref_template.py       ./plot_radar_polar_ref_${STAID}.py
          sed -i "s/@STAID@/${STAID}/g"       ./plot_radar_polar_ref_${STAID}.py
          sed -i "s/@ANAL_TIME@/${ANAL_TIME}/g" ./run_refl_plot_${STAID}.ksh
          sed -i "s/@STAID@/${STAID}/g"         ./run_refl_plot_${STAID}.ksh
          sed -i "s/@walltime@/${walltime}/g"   ./run_refl_plot_${STAID}.ksh
          sed -i "s/@queue@/${queue}/g"         ./run_refl_plot_${STAID}.ksh
          sed -i "s/@anel0@/${anel0}/g"         ./run_refl_plot_${STAID}.ksh
          #submit the job to the queue to make the mean and std 2d wind plots.
          sbatch ./run_wind_plot_${STAID}.ksh
          sbatch ./run_refl_plot_${STAID}.ksh
       fi

       #move up one directory to process the next radar
       cd ..
done


