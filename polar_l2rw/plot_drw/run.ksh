#!/bin/ksh

#This script loops over the specified radars from STAIDS list and performs one of the follwoing tasks:
# 1) creates a plot of the radar observations (either reflectivity or radial winds) and also computes
#    some statistics for the observations.
# 2) creates a histogram plot of the radar observations (radial wind only). 

#Requirements: 
#  https://github.com/JacobCarley-NOAA/NCEPy
#  https://github.com/JCSDA/py-ncepbufr

######    U S E R   I N P U T    #####################################################################
STAIDS="KFDR KFWS KGLD KGRK KICT KINX KLNX KRTX KTLX KVNX" #What radars would you like to process?   # 
STAIDS="KOHX"        #(input) What radars would you like to process? (can be a list)                 #
anel0=0.5            #(input) and at what elevation angle? (+/-0.25) 0.5 0.9 1.3 1.8 2.4 3.4...      #
refl="NO"            #(input) plot reflectivity                                                      #
drws="YES"           #(input) plot doppler radial winds                                              #
walltime=00:20:00    #(input) batch job walltime (SBATCH)                                            #
queue="batch"        #(input) the batch queue                                                        #
debug="NO"           #(input) don't run a batch job                                                  #
ANAL_TIME=2019120100 #(input) date of the observation file                                           #
histogram=".false."  #(input) true=makes histogram plot; false=plots observations                    #
obspath="/scratch1/NCEPDEV/stmp2/Donald.E.Lippi/" #(input) the nexrad bufr files are located here.   #
work="/scratch2/NCEPDEV/fv3-cam/Donald.E.Lippi/py-ncepl2bufr/polar_l2rw/plot_drw/" #(input) workspace#
######################################################################################################
set -x
base=`pwd`
#Loop over radars
for STAID in $STAIDS; do
       cd $base #start from the base directory
       echo $STAID
       mkdir -p $STAID #make a directory for each station id.
       cd $STAID       #move into the newly created directory.

       if [[ $histogram == ".true." ]]; then
          #copy the template files to the corresponding directory and rename for the station id.
          cp ../templates/plot_radar_polar_hist_template.py      ./plot_radar_polar_hist_${STAID}.py
          cp ../templates/run_wind_plot_hist_template.ksh        ./run_wind_plot_hist_${STAID}.ksh
          #stream edit the template files for the corresponding variables.
          sed -i "s/@STAID@/${STAID}/g"         ./plot_radar_polar_hist_${STAID}.py
          sed -i "s/@ANAL_TIME@/${ANAL_TIME}/g" ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s/@STAID@/${STAID}/g"         ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s/@walltime@/${walltime}/g"   ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s/@queue@/${queue}/g"         ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s/@anel0@/${anel0}/g"         ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s/@histogram@/${histogram}/g" ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s#@obspath@#${obspath}#g"     ./run_wind_plot_hist_${STAID}.ksh
          sed -i "s#@work@#${work}#g"           ./run_wind_plot_hist_${STAID}.ksh
          if [[ $debug == "NO" ]]; then; sbatch ./run_wind_plot_hist_${STAID}.ksh; fi
          if [[ $debug =="YES" ]]; then;    ksh ./run_wind_plot_hist_${STAID}.ksh; fi

       else
          if [[ $drws == "YES" ]]; then
             #copy the template files to the corresponding directory and rename for the station id.
             cp ../templates/run_wind_plot_template.ksh             ./run_wind_plot_${STAID}.ksh
             cp ../templates/plot_radar_polar_wind_template.py      ./plot_radar_polar_wind_${STAID}.py
             #stream edit the template files for the corresponding variables.
             sed -i "s/@STAID@/${STAID}/g"         ./plot_radar_polar_wind_${STAID}.py
             sed -i "s/@ANAL_TIME@/${ANAL_TIME}/g" ./run_wind_plot_${STAID}.ksh
             sed -i "s/@STAID@/${STAID}/g"         ./run_wind_plot_${STAID}.ksh
             sed -i "s/@walltime@/${walltime}/g"   ./run_wind_plot_${STAID}.ksh
             sed -i "s/@queue@/${queue}/g"         ./run_wind_plot_${STAID}.ksh
             sed -i "s/@anel0@/${anel0}/g"         ./run_wind_plot_${STAID}.ksh
             sed -i "s/@histogram@/${histogram}/g" ./run_wind_plot_${STAID}.ksh
             sed -i "s#@obspath@#${obspath}#g"     ./run_wind_plot_${STAID}.ksh 
             sed -i "s#@work@#${work}#g"           ./run_wind_plot_${STAID}.ksh 
             if [[ $debug == "NO" ]]; then; sbatch ./run_wind_plot_${STAID}.ksh; fi
             if [[ $debug =="YES" ]]; then;    ksh ./run_wind_plot_${STAID}.ksh; fi
          fi

          if [[ $refl == "YES" ]]; then
             #copy the template files to the corresponding directory and rename for the station id.
             cp ../templates/run_refl_plot_template.ksh             ./run_refl_plot_${STAID}.ksh
             cp ../templates/plot_radar_polar_refl_template.py      ./plot_radar_polar_refl_${STAID}.py
             #stream edit the template files for the corresponding variables.
             sed -i "s/@STAID@/${STAID}/g"         ./plot_radar_polar_refl_${STAID}.py
             sed -i "s/@ANAL_TIME@/${ANAL_TIME}/g" ./run_refl_plot_${STAID}.ksh
             sed -i "s/@STAID@/${STAID}/g"         ./run_refl_plot_${STAID}.ksh
             sed -i "s/@walltime@/${walltime}/g"   ./run_refl_plot_${STAID}.ksh
             sed -i "s/@queue@/${queue}/g"         ./run_refl_plot_${STAID}.ksh
             sed -i "s/@anel0@/${anel0}/g"         ./run_refl_plot_${STAID}.ksh
             sed -i "s#@obspath@#${obspath}#g"     ./run_refl_plot_${STAID}.ksh 
             sed -i "s#@work@#${work}#g"           ./run_refl_plot_${STAID}.ksh 
             if [[ $debug == "NO" ]]; then; sbatch ./run_refl_plot_${STAID}.ksh; fi
             if [[ $debug =="YES" ]]; then;    ksh ./run_refl_plot_${STAID}.ksh; fi
          fi
       fi
done
