from __future__ import print_function
import ncepbufr
import matplotlib
matplotlib.use('Agg')
import ncepy, sys
import numpy as np
import matplotlib.pyplot as plt
import time
import fortranfile as F
import os
import matplotlib.colors as mcolors

def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)


def deg2rad(theta):
    theta = (theta)*3.141592/180.
    return(theta)

def main():
    tic = time.clock()

    #1. DECLARE THE SUPEROB PARAMETERS USED FROM THE GSI NAMELIST.
    anal_time=str(sys.argv[1])
    station_id=sys.argv[2]
    del_azimuth=float(sys.argv[3])#5.
    del_elev=float(sys.argv[4])
    del_range=float(sys.argv[5])#5000.
    range_max=100000.
    del_time=float(sys.argv[6])#0.125
    minnum=int(sys.argv[7])#50

    #2. SET SOME VALUES WHICH CHANGE BASED ON THE SUPEROB PARAMETERS.
    max_angle_az=360. 
    rows_az=int(max_angle_az/del_azimuth)
    cols_rw=range_max/del_range
    dr2=del_range/2.
    half_del_az=del_azimuth/2.
 
    #3. INITIALIZE SOME BASIC LISTS.
    staid=[]; stalat=[]; stalon=[]; stahgt=[]; dattime=[]; lat=[]; lon=[]; hgt=[]; vr=[]
    corrected_azimuth=[]; err=[]; corrected_tilt=[]; gamma=[]
    stalats=[]; stalons=[]; anel=[]; anaz=[]; radii=[]; l2rw=[]; tilt=[]; azimuth=[]; rad=[]; l2=[]

    #4. GET THE INPUT FILE CONTAINING THE SUPER OBSERVATIONS.
    fileds=[stalat,stalon,stahgt,dattime,hgt,vr,corrected_azimuth,err,corrected_tilt,gamma]
    os.system('./exec/read_radar.exe')
    fname='./output.bin'
    f=F.FortranFile(fname,endian='>')

    #5. GET THE NUMBER OF SUPEROB BOXES READ BY READ_RADAR.
    #os.system('./read_radar.exe')
    fname_num_supob_boxes='./num_supob_boxes.bin'
    fnsb=F.FortranFile(fname_num_supob_boxes,endian='>')
    num_supob_boxes=fnsb.readInts('i')
    #num_supob_boxes=1

    #6. READ THE SUPEROB FILE AND STORE DATA IN 1-D RAD AND L2 ARRAYS.
    for i in range(num_supob_boxes):
       fields=f.readReals('d')
       vr                 =fields[5]
       corrected_azimuth  =fields[6] 
       corrected_tilt     =fields[8]
       gamma              =fields[9]
       azimuth.append(corrected_azimuth)
       tilt.append(corrected_tilt)
       rad.append(int(gamma))
       l2.append(vr)

    #7. INITIALIZE RADIUS AND L2RW DATA ARRAYS WITH ALL ZEROS.
    radii = np.zeros((rows_az,cols_rw))
    l2rw  = np.zeros((rows_az,cols_rw))

    #8. INITIALIZE ANAZ WITH MID-POINT ANGLES.
    start_az=0.; end_az=360.
    anaz = np.linspace(start_az,end_az,360./del_azimuth)
    print("\n \nYou are using the following settings:")
    print("del_azimuth    :",del_azimuth)
    print("start_az       :",start_az)
    print("end_az         :",end_az)
    print("number of rows (azimuths) (",max_angle_az,"/",del_azimuth,") :",rows_az)
    
    #9. PUT RADIUS AND L2RW VALUES IN 2-D ARRAY ACCORDING TO AZIMUTHS.
    j=0; daz=del_azimuth-0.2; gates_beam=int(range_max/del_range)
    print("range_max      :",range_max)
    print("del_range      :",del_range)
    print("gates per beam :",gates_beam)
    print("number of columns (rw) (",range_max,"/",del_range,") :",cols_rw)
    print("giving the shape of",np.shape(radii),"\n \n")
    for i in range(num_supob_boxes):
       ai=int(azimuth[i]/del_azimuth)
       aim1=int(azimuth[i-1]/del_azimuth)
       if(i != 0 and np.abs(ai - aim1) > 0.8): j=0
       if(i != 0 and np.abs(ai - aim1) < 0.8): j=j+1
       if(j == gates_beam):
           print('Error Raised at azimuth angle: ',azimuth[i]*180/3.141592)
           print('np.abs(ai - aim1) = ',np.abs(ai - aim1))
           print('ai =',ai)
           print('aim1 =',aim1)
       for k in range(gates_beam):
           if(rad[i] > del_range*k and rad[i] <= del_range*(k+1)):
               radii[ai-1][j] = dr2 + del_range*k
           l2rw[ai-1][j] = l2[i]

    #10. INITIALIZE THE POLAR PLOT AS ALL MISSING DATA (-999).
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111,polar=True)
    #ax.set_theta_zero_location("N"); ax.set_theta_direction(-1) # DO NOT USE THESE!!!!
    theta,r = np.meshgrid(anaz,np.linspace(0.,range_max,range_max/del_range))
    theta=deg2rad(theta)
    rw = np.zeros(shape=(len(theta),len(r[0])))
    rw.fill(-999) 
    r=r.T; rw=rw.T 

    print('Max value should be...',np.max(l2rw))
    #11. POPULATE THE EMPTY RW ARRAY WITH ACTUAL VALUES.
    if(np.max(radii)==0.0): print('Make sure gamma is written out by GSI!')
    l=0
    for i in range(len(anaz)):
        for j in range(len(radii[i])): 
            for k in range(len(r[i])):
                if((radii[i][j]-r[i][k]) <= del_range/2.): 
                    rw[i][k]=l2rw[i][j]
                    l=l+1
                    break 
    #### print the index of the single observatios ###
    #print(np.argmax(rw))
    #print(rw[0])
    #print(np.shape(rw))
    #print(np.shape(radii))
    #print(rw[np.argmax(rw)/39][:])
    #print(r[np.argmax(rw)/39][:])
    ##################################################
    #if(del_range == 5000):
    #  so_type="default"
    #if(del_range == 3000):
    #  so_type="tuned"
    calc_variance=True
    if(calc_variance):
       if(del_time == 0.5 and del_range == 5000):
          f1=open('./'+str(station_id)+'stats'+str(anal_time)+"default",'w+')
       if(del_time != 0.5 and del_range == 5000):
          f1=open('./'+str(station_id)+'stats'+str(anal_time)+"default_7pt5min",'w+')
       if(del_time != 0.5 and del_range == 3000):
          f1=open('./'+str(station_id)+'stats'+str(anal_time)+"tuned",'w+')
       if(del_time == 0.5 and del_range == 3000):
          f1=open('./'+str(station_id)+'stats'+str(anal_time)+"tuned_30min",'w+')
       rw_stdev=rw[rw>-999].std()
       rw_mean =rw[rw>-999].mean()
       rw_var  =rw[rw>-999].var()
       f1.write("The output here describes some statistics for the radial wind obs \n")
       f1.write("Obs file={} \n".format("./output.bin"))
       f1.write("date    ={} \n".format(anal_time))
       f1.write("Station ={} \n".format(station_id))
       f1.write("DELAZ   ={} \n".format(del_azimuth))
       f1.write("DELELV  ={} \n".format(del_elev))
       f1.write("DELRNG  ={} \n".format(del_range))
       f1.write("RMAX    ={} \n".format(range_max))
       f1.write("DELTIME ={} \n".format(del_time))
       f1.write("MINNUM  ={} \n".format(minnum))
       f1.write("STDEV   ={} \n".format(rw_stdev))
       f1.write("MEAN    ={} \n".format(rw_mean))
       f1.write("VAR     ={} \n".format(rw_var))
       f1.close()

    print('The max rw value is: ',np.max(rw))
    if(np.max(rw) == -999):
       print('There is an error reading in the data.')
       exit() 
    print(l,' out of ',num_supob_boxes,' super ob boxes read')

    #12. FINISH MAKING THE POLAR PLOT.
    if(False):
       cmap = plt.cm.jet
       cmap.set_under('white')
    else:
       c = mcolors.ColorConverter().to_rgb
       cmap = make_colormap(
             [c('deepskyblue'),c('navy')    ,0.20, # light blue to dark blue
              c('#02ff02')    ,c('#003500') ,0.47, # bright green to dark green
              c('#809e80')    ,c('white')   ,0.50, # gray with green tint to white
              c('white')      ,c('#9e8080') ,0.53, # white to gray with red tint
              c('#350000')    ,c('#ff0000') ,0.80, # dark red to bright red
              c('salmon')     ,c('yellow')])       # salmon to yellow
       #plt.register_cmap(name=gwr.name, cmap=gwr); cmap= plt.set_cmap(gwr)
       cmap.set_under('#999999')
       cmap.set_over('purple')
    mesh = ax.pcolormesh(theta,r.T,rw.T,shading='flat',cmap=cmap,vmin=-40,vmax=40)
    cbar = fig.colorbar(mesh,shrink=0.85,pad=0.10,ax=ax)
    cbar.set_label('$m/s$')
    lLaTeX=True
    if(lLaTeX):
     fig.suptitle('Doppler Velocity Super-Observations  '+station_id
              +'\n $\Delta$r: '+str(int(del_range))+'-m, '\
              +'  $\Delta \\theta$: '+str(del_azimuth)+' deg, '\
              +'\n $\Delta$t: +/-'+str(del_time*60)+' min, '\
              +'  N: '+str(minnum), fontsize=15,x=0.42,y=0.95)
    if(not lLaTeX):
     fig.suptitle('Doppler Velocity Super-Observations  '+station_id
              +'\n del_range: '+str(int(del_range))+'-m, '\
              +'  del_azimuth: '+str(del_azimuth)+' deg, '\
              +'\n del_time: +/-'+str(del_time*60)+' min, '\
              +'  minnum: '+str(minnum), fontsize=15,x=0.42,y=0.95)
    ax.grid(True)
    plt.show()
    plt.savefig('./'+station_id+'_'+anal_time+'_'\
                +str(int(del_range))+'-'+str(del_azimuth)+'-'\
                +str("%0.3f" % del_time)+'-'+str(int(minnum))+'.png'\
                ,bbox_inches='tight')

    #13. CALCULATE SOME TIMING STATS.
    toc = time.clock() # check to see how long it took to run.
    sec = str(toc-tic)
    print('time it took to run: '+sec+' seconds.')


if __name__ == "__main__":
    main()
