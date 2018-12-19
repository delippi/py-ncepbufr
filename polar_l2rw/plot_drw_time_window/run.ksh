#!/bin/ksh

#This script runs everything


STAIDS="KGRK KSJT KDYX KFDR KTLX KINX KCRP"
STAIDS="KGRK KVNX KTLX KRTX KFDR" 
anel0=0.5
del_time=0.125

for STAID in $STAIDS; do
    echo $STAID
    mkdir -p $STAID
    cd $STAID

    cp ../templates/plot_radar_polar_timew_template.py     ./plot_radar_polar_timew_${STAID}.py
    cp ../templates/plot_radar_polar_timew_std_template.py ./plot_radar_polar_timew_std_${STAID}.py
    cp ../templates/run_timew_template.ksh                 ./run_timew_${STAID}.ksh
    cp ../templates/run_timew_std_template.ksh             ./run_timew_std_${STAID}.ksh

    sed -i "s/@STAID@/${STAID}/g"       ./plot_radar_polar_timew_${STAID}.py
    sed -i "s/@anel0@/${anel0}/g"       ./plot_radar_polar_timew_${STAID}.py
    sed -i "s/@del_time@/${del_time}/g" ./plot_radar_polar_timew_${STAID}.py

    sed -i "s/@STAID@/${STAID}/g"       ./plot_radar_polar_timew_std_${STAID}.py
    sed -i "s/@anel0@/${anel0}/g"       ./plot_radar_polar_timew_std_${STAID}.py
    sed -i "s/@del_time@/${del_time}/g" ./plot_radar_polar_timew_std_${STAID}.py

    sed -i "s/@STAID@/${STAID}/g"       ./run_timew_${STAID}.ksh
    sed -i "s/@STAID@/${STAID}/g"       ./run_timew_std_${STAID}.ksh

    qsub ./run_timew_${STAID}.ksh
    qsub ./run_timew_std_${STAID}.ksh

    cd ..

done

