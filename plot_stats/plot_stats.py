#!/bin/python

import numpy as np
import os
import matplotlib.pyplot as plt

import subprocess

STAIDS=["KFDR","KFWS","KGLD","KGRK","KICT","KINX","KLNX","KRTX","KTLX","KVNX"]
strn=" -e STDEV -e MEAN -e VAR "
strn_std=" STDEV "
strn_mean=" MEAN "
strn_var=" VAR "
cut=" | cut -f 2 -d '='"

VARS=["STDEV","MEAN"]

stdev=np.zeros(shape=(len(STAIDS),7),dtype=float)
mean=np.zeros(shape=(len(STAIDS),7),dtype=float)
var=np.zeros(shape=(len(STAIDS),7),dtype=float)


i=0
for STAID in STAIDS:
#    print STAID

    l2rw_timewindow="../polar_l2rw/plot_drw_time_window/"+STAID+"/"
    l2rw="../polar_l2rw/plot_drw/"+STAID+"/"
    supob="../polar_supob/"+STAID+"/"

#STANDARD DEVIATION
    stdev[i,0]=subprocess.check_output("grep"+strn_std+l2rw+STAID+"stats2015103018"+cut,shell=True)
    stdev[i,1]=subprocess.check_output("grep"+strn_std+l2rw_timewindow+STAID+"_0.5_2015103018_0.125.txt"+cut,shell=True)
    stdev[i,2]=subprocess.check_output("grep"+strn_std+l2rw_timewindow+STAID+"_0.5_2015103018_0.5.txt"+cut,shell=True)
    stdev[i,3]=subprocess.check_output("grep"+strn_std+supob+STAID+"stats2015103018tuned"+cut,shell=True)
    stdev[i,4]=subprocess.check_output("grep"+strn_std+supob+STAID+"stats2015103018default_7pt5min"+cut,shell=True)
    stdev[i,5]=subprocess.check_output("grep"+strn_std+supob+STAID+"stats2015103018tuned_30min"+cut,shell=True)
    stdev[i,6]=subprocess.check_output("grep"+strn_std+supob+STAID+"stats2015103018default"+cut,shell=True)
#MEAN
    mean[i,0]=subprocess.check_output("grep"+strn_mean+l2rw+STAID+"stats2015103018"+cut,shell=True)
    mean[i,1]=subprocess.check_output("grep"+strn_mean+l2rw_timewindow+STAID+"_0.5_2015103018_0.125.txt"+cut,shell=True)
    mean[i,2]=subprocess.check_output("grep"+strn_mean+l2rw_timewindow+STAID+"_0.5_2015103018_0.5.txt"+cut,shell=True)
    mean[i,3]=subprocess.check_output("grep"+strn_mean+supob+STAID+"stats2015103018tuned"+cut,shell=True)
    mean[i,4]=subprocess.check_output("grep"+strn_mean+supob+STAID+"stats2015103018default_7pt5min"+cut,shell=True)
    mean[i,5]=subprocess.check_output("grep"+strn_mean+supob+STAID+"stats2015103018tuned_30min"+cut,shell=True)
    mean[i,6]=subprocess.check_output("grep"+strn_mean+supob+STAID+"stats2015103018default"+cut,shell=True)
#VARIANCE
    var[i,0]=subprocess.check_output("grep"+strn_var+l2rw+STAID+"stats2015103018"+cut,shell=True)
    var[i,1]=subprocess.check_output("grep"+strn_var+l2rw_timewindow+STAID+"_0.5_2015103018_0.125.txt"+cut,shell=True)
    var[i,2]=subprocess.check_output("grep"+strn_var+l2rw_timewindow+STAID+"_0.5_2015103018_0.5.txt"+cut,shell=True)
    var[i,3]=subprocess.check_output("grep"+strn_var+supob+STAID+"stats2015103018tuned"+cut,shell=True)
    var[i,4]=subprocess.check_output("grep"+strn_var+supob+STAID+"stats2015103018default_7pt5min"+cut,shell=True)
    var[i,5]=subprocess.check_output("grep"+strn_var+supob+STAID+"stats2015103018tuned_30min"+cut,shell=True)
    var[i,6]=subprocess.check_output("grep"+strn_var+supob+STAID+"stats2015103018default"+cut,shell=True)


    txt1=" > "+STAID+".txt"
    txt2=" >> "+STAID+".txt"
    subprocess.check_output("grep"+strn+l2rw+STAID+"stats2015103018"+txt1,shell=True);                             subprocess.check_output("echo ''"+txt2,shell=True)
    subprocess.check_output("grep"+strn+l2rw_timewindow+STAID+"_0.5_2015103018_0.125.txt"+txt2,shell=True);        subprocess.check_output("echo ''"+txt2,shell=True)
    subprocess.check_output("grep"+strn+l2rw_timewindow+STAID+"_0.5_2015103018_0.5.txt"+txt2,shell=True);          subprocess.check_output("echo ''"+txt2,shell=True)
    subprocess.check_output("grep"+strn+supob+STAID+"stats2015103018default"+txt2,shell=True);          subprocess.check_output("echo ''"+txt2,shell=True)
    subprocess.check_output("grep"+strn+supob+STAID+"stats2015103018tuned_30min"+txt2,shell=True);      subprocess.check_output("echo ''"+txt2,shell=True)
    subprocess.check_output("grep"+strn+supob+STAID+"stats2015103018default_7pt5min"+txt2,shell=True);  subprocess.check_output("echo ''"+txt2,shell=True)
    subprocess.check_output("grep"+strn+supob+STAID+"stats2015103018tuned"+txt2,shell=True)

    i+=1

#print stdev
#print ""
#print mean
#print ""
#print var


###################################
xy_label_fontsize=18              #
tick_label_fontsize=18            #
legend_fontsize=16                #
fig_title_fontsize=20             #
dot_size=50                       #
l_dot_size=7                      #
linewidth=3                       #
###################################

levels = ['L2 \n +/-0min',
 'L2 \n +/-7.5min',
 'L2 \n +/-30min',
 'SO \n 3-km \n +/-7.5min',
 'SO \n 5-km \n +/-7.5min',
 'SO \n 3-km \n +/-30min',
 'SO \n 5-km \n +/-30min'
]

levels_int=np.arange(0,7,1)



colors=["#000000","#ff0044","#55ff00","#00aaff","#8800ff"]
colors=["#000000","#ff0044","#55ff00","#00aaff","#8800ff","#000000","#ff0044","#55ff00","#00aaff","#8800ff"]
colors=["#000000","#ff0044","#55ff00","#00aaff","#8800ff","#ff6600","#33cccc","#ff99ff","#99ccff","#339933"]
linestyles=["-","-","-","-","-","-","-","-","-","-"]
for VAR in VARS:
   fig = plt.figure(1,figsize=(10,6))
   ax1 = fig.add_subplot(111)
   i=0
   for STAID in STAIDS:
      print(VAR,STAID)
      if(VAR == "STDEV"):
         ax1.plot(stdev[i,:],color=colors[i],marker='o',markersize=l_dot_size,label=STAID,    linewidth=linewidth,linestyle=linestyles[i])
         ylabel="Standard Deviation (m/s)"
         figname="RadialWindStats_std"
      if(VAR == "MEAN"):
         ax1.plot(mean[i,:],color=colors[i],marker='o',markersize=l_dot_size,label=STAID,    linewidth=linewidth,linestyle=linestyles[i])
         ylabel="Mean (m/s)"
         figname="RadialWindStats_mean"
      if(VAR == "VAR"):
         ax1.plot(var[i,:],color=colors[i],marker='o',markersize=l_dot_size,label=STAID,    linewidth=linewidth,linestyle=linestyles[i])
         ylabel="Variance (m/s)"
         figname="RadialWindStats_var"
      i+=1

   ax1.set_xticklabels(levels)
   ax1.grid('on')
   leg=ax1.legend(fontsize=legend_fontsize,ncol=5,scatterpoints=1,loc='upper center',bbox_to_anchor=(0.,-0.3,1.,.102))
   leg.get_frame().set_alpha(0.9)
   title=plt.suptitle('Radar winds single value statistics',fontsize=fig_title_fontsize,x=0.5,y=1.00)
   plt.xlabel('Method of processing radial winds',fontsize=xy_label_fontsize)
   plt.ylabel(ylabel,fontsize=xy_label_fontsize)
   plt.savefig('./'+figname+'.png',bbox_extra_artists=(leg,title),bbox_inches='tight')
   plt.close()
