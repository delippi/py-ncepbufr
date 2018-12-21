#!/bin/python
#PBS -N radar
#PBS -l walltime=00:20:00
#PBS -l nodes=1:ppn=8 
#PBS -q batch
#PBS -A fv3-cpu
#PBS -o radar.log
#PBS -j oe


from __future__ import print_function
import matplotlib
matplotlib.use('Agg')
import ncepbufr
import ncepy, sys
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import time
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
    theta = theta*3.141592/180.
    return(theta)

def main():
    tic = time.clock()
    # Mnemonics for getting data from the bufr file.
    hdstr= 'SSTN CLON CLAT SELV ANEL YEAR MNTH DAYS HOUR MINU QCRW ANAZ' #PRFR' # MGPT'
    obstr= 'DIST125M DMVR DVSW' # PRFR'                     #NL2RW--level 2 radial wind.
    obstr2='STDM SUPLON SUPLAT HEIT RWND RWAZ RSTD' #RWSOB--radial wind super ob.

    #1. INITIALIZING SOME BASIC LISTS AND GETTING INPUT DATA.
    sids=[]; lons=[]; lats=[]; l2rw=[]; anel=[]; anaz=[]; dist125m=[]; ymdhm=[]; radii=[]; PRF=[]
    #3. FIND THE MAX/MIN VALUES OF THE DIST125M AND THETA ARRAYS.
    maxRadii=100000 # set max of max distances to about 100 mi.
    minRadii=0 # min of min distances.

    #4. INITIALIZE THE POLAR PLOT AS ALL MISSING DATA (-999).
    theta,r = np.meshgrid(anaz,np.arange(minRadii,maxRadii,250.)) # create meshgrid
    theta=deg2rad(theta) # convert theta from degrees to radians.
    l2rwX = np.zeros(shape=(1,361,400))*np.nan #init first dim to 1. we'll inc this later 

    #INPUT PARAMS ###############
   #OBS_FILE='/scratch4/NCEPDEV/meso/save/Donald.E.Lippi/gsi/data/obsfiles/2015103018/rap.t18z.nexrad.tm00.bufr_d'
    OBS_FILE='/scratch4/NCEPDEV/meso/save/Donald.E.Lippi/gsi/data/obsfiles/2015103018/nam.t18z.nexrad.tm00.bufr_d'
    OBS_FILECPY=OBS_FILE+"_cpy"
    message_type1='NC006027' #6010 + 17z = 6027
    message_type2='NC006028' #6010 + 18z = 6028
    date=2015103018
    STAID="@STAID@"
    anel0=@anel0@
    del_anel=0.25
    del_time=@del_time@
    #############################
    time_check_1=(60. - del_time*60.)
    time_check_2=(      del_time*60.)
    print("Average obs with time window of {} minutes".format(del_time*60.))
    n=-1
     
    #2. READ PREPBUFR FILE.
    brk=False # used for breaking the loop.
    bufr = ncepbufr.open(OBS_FILE) # bufr file for reading.
    bufrcpy=ncepbufr.open(OBS_FILECPY) # bufr file for reading ahead and determining maxanaz.
    bufr.dump_table('l2rwbufr.table') # dump table to file.
    while bufr.advance() == 0: # loop over messages.
       #bufr has been advanced, now if reading concurrently, bufrcpy should be behind by one. But sometimes
       #bufrcpy could be ahead of where we need it (but only by one step) since we read it forward. 
       #We don't want to advance it in that case.
       if( (bufr.msg_counter-bufrcpy.msg_counter)==1): bufrcpy.advance()
       if(bufr.msg_type == message_type1 or bufr.msg_type == message_type2):
            print(bufr.msg_counter, bufr.msg_type, bufr.msg_date,time_check_1,time_check_2)
            while bufr.load_subset() == 0: # loop over subsets in message.
                hdr = bufr.read_subset(hdstr).squeeze() # parse hdstr='SSTN CLON ... etc.'
                bufr_minu=hdr[9]
                #*********************
                bufrcpy.load_subset()#**********************
                hdrcpy=bufrcpy.read_subset(hdstr).squeeze()#
                bufrcpy_minu=hdrcpy[9]#*********************
                #**********************
                good=False
                if(bufr.msg_type == message_type1 and bufr_minu >= time_check_1): good=True
                if(bufr.msg_type == message_type2 and bufr_minu <= time_check_2): good=True
                if(good): #looking for next minute to process
                   station_id = hdr[0].tostring() # convert SSTN to string.
                   station_id=station_id.strip()  # remove white space from SSTN.
                   if(station_id == STAID): # comes from input. used for picking a single SSTN.
                       if(hdr[4] >= anel0-del_anel and hdr[4] <= anel0+del_anel): # read an elevation angle.
                           if(hdr[11] >= 0 and hdr[11] <= 1): # increment n on first azimuth only
                              n=n+1
                              maxanaz=0 #initialize/reset. This gets updates around azm 355
                           obs = bufr.read_subset(obstr).squeeze() # parse obstr='DIST125M DMVR DVSW'
                           #*******************************************
                           obscpy=bufrcpy.read_subset(obstr).squeeze()#
                           #*******************************************
                           print(bufr.msg_counter,'SSTN,DATE/TIME : ',station_id,hdr[5:10],hdr[4],hdr[11],n,len(anaz))
                           sids.append(station_id) # station ids
                           l2rw.append(obs[1]) # level 2 radial winds
                           anel.append(hdr[4]) # elevation angles
                           anaz.append(hdr[11]) # azimuthal angles
                           radii.append(obs[0]*125) #distances in units of 1 m
                           ymdhm.append(int(hdr[9]))
                           #It is not sufficient to check for len(anaz) == 360. Sometimes, it is missing. 
#***********************************************************************************************************
                           if(len(anaz) == 355): #pause to read ahead. 
                              while bufrcpy.load_subset() == 0: # read ahead with bufrcpy
                                  hdrcpy=bufrcpy.read_subset(hdstr).squeeze()
                                  bufrcpy_minu=hdrcpy[9]
                                  maxanaz=max(maxanaz,int(np.ceil(hdrcpy[11]))) #need hdrcpy[11] rounded up.
                              tries=0
                              while tries < 10 and bufrcpy.advance() == 0: # look no. tries messages ahead.
                                 tries+=1
                                 while bufrcpy.load_subset() == 0:
                                     bufrcpy_minu=hdrcpy[9]
                                     good=False
                                     if(bufrcpy.msg_type == message_type1 and bufrcpy_minu >= time_check_1): 
                                        good=True
                                     if(bufrcpy.msg_type == message_type2 and bufrcpy_minu <= time_check_2):
                                        good=True
                                     if(good): #looking for next minute to process
                                        station_id = hdrcpy[0].tostring() # convert SSTN to string.
                                        station_id=station_id.strip()  # remove white space from SSTN.
                                        if(station_id == STAID):
                                           if(hdrcpy[4] >= anel0-del_anel and hdrcpy[4] <= anel0+del_anel):
                                              hdrcpy= bufrcpy.read_subset(hdstr).squeeze()
                                              maxanaz=max(maxanaz,int(np.ceil(hdrcpy[11])))
                                              print(bufrcpy.msg_counter,'cpySSTN,DATE/TIME : ',station_id,hdrcpy[5:10],hdrcpy[4],hdrcpy[11],n,len(anaz))
                              print(maxanaz)
                           if(len(anaz) >= 355): print(len(anaz),maxanaz)
#***********************************************************************************************************
                           #if(len(anaz) >= 355 and we've reached the end of the subset with anaz = 355)
                           if(len(anaz) == maxanaz and len(anaz)> 355):
                              while(len(anaz) < 360): #fill in some missing data points
                                 l2rw.append(obs[1]*0 + -999.)
                                 anel.append(anel[-1])
                                 anaz.append(anaz[-1]+1)
                                 radii.append(radii[-1])
                                 ymdhm.append(ymdhm[-1])
                              while(len(anaz) < 361): # fill in the final beam with nan mean between 1st and 359th
                                 #l2rw_first_last=l2rw[0],l2rw[-1]
                                 #l2rw.append(np.nanmean(np.dstack(l2rw_first_last),axis=2).flatten().tolist())
                                 l2rw.append(l2rw[0])
                                 anel.append(anel[0])
                                 anaz.append(anaz[-1]+1)
                                 radii.append(radii[0])
                                 ymdhm.append(ymdhm[0])
                              MM=str(ymdhm[-1])
                              print("max/min el. angle:  ",np.max(anel),np.min(anel))
                              print("max/min minute:     ",np.max(ymdhm),np.min(ymdhm))
                              theta,r = np.meshgrid(anaz,np.arange(minRadii,maxRadii,250.)) # create meshgrid
                              theta=deg2rad(theta)
                              rw = np.zeros(shape=(len(theta),len(r[0])))# initialize the polar plot with all 0's
                              rw.fill(-999) # change all values to missing data (-999).
                              r=r.T; rw=rw.T#; PRF_new.T # transpose r and rw for later manipulation.
                              #5. POPULATE THE EMPTY RW ARRAY WITH ACTUAL VALUES.
                              for i in range(360): # for every azimuth angle ...
                                  print(str(i+1)+'/'+str(360))
                                  for j in range(len(radii[i])): # loop over every observation distance from radar
                                      for k in range(len(r[i])): # and loop over an equally 125m spaced array
                                          if(radii[i][j] == r[i][k]): # if the observation dist = dist125m
                                              rw[i][k]=l2rw[i][j] # assign the value of the obsrvtn to that index.
                                              break # speeds things up by about 50-60%.
                              if(n>0):
                                 newrow=rw*np.nan
                                 l2rwX = np.concatenate((l2rwX,[newrow]),axis=0) 
                              rw[rw==-999.]=np.nan #set -999 to nans
                              l2rwX[n,:,:]=rw
                              sids=[]; lons=[]; lats=[]; l2rw=[]; anel=[]; anaz=[]
                              dist125m=[]; ymdhm=[]; radii=[]; PRF=[]
    bufr.close()
    rw_mean = np.nanmean(np.dstack(l2rwX),axis=2)#average element wise over time series
    print("shape of l2rwX is" +str(np.shape(l2rwX)))
    print("type=",type(l2rwX))
    rw=rw_mean # overwrite rw with the rw_mean for further processing
    rw[np.isnan(rw)] = -999. # the masked values are converted to nan. set nan to -999.
    print("shape of rw is" +str(np.shape(rw)))
    toc = time.clock() # check how long reading the data in took.
    sec = str(toc-tic)
    print('time it took to run: '+sec+' seconds.')


    #4. INITIALIZE THE POLAR PLOT
    fig = plt.figure(figsize=(8,8)) # 8" x 8" seems plenty large.
    ax = fig.add_subplot(111,polar=True) # we would like it to be a polar plot.
    ax.set_theta_zero_location("N") # set theta zero location to point North.
    ax.set_theta_direction(-1) # set theta to increase clockwise (-1).


    calc_variance=True
    figname='./'+STAID+'_'+str(anel0)+'_'+str(date)+'_'+str(del_time)
    if(calc_variance):
       f1=open(figname+'.txt','w+')
       rw_stdev=rw[rw!=-999.].std()
       rw_mean =rw[rw!=-999.].mean()
       rw_var  =rw[rw!=-999.].var()
       f1.write("The output here describes some statistics for the radial wind obs \n")
       f1.write("Obs file={} \n".format(OBS_FILE))
       f1.write("date    ={} \n".format(date))
       f1.write("Station ={} \n".format(STAID))
       f1.write("STDEV   ={} \n".format(rw_stdev))
       f1.write("MEAN    ={} \n".format(rw_mean))
       f1.write("VAR     ={} \n".format(rw_var))
       f1.close()
        

    #6. FINISH MAKING THE POLAR PLOT WITH THE FILLED IN VALUES.
    if(False):
       cmap = plt.cm.jet # use the jet colormap.
       cmap.set_under('white') # set the -999 values to white.
    else:
       c = mcolors.ColorConverter().to_rgb
       cmap = make_colormap(
             [c('deepskyblue'),c('navy')    ,0.20, # light blue to dark blue
              c('#02ff02')    ,c('#003500') ,0.47, # bright green to dark green
              c('#809e80')    ,c('white')   ,0.50, # gray with green tint to white
              c('white')      ,c('#9e8080') ,0.53, # white to gray with red tint
              c('#350000')    ,c('#ff0000') ,0.80, # dark red to bright red
              c('salmon')     ,c('yellow')])       # salmon to yellow
       cmap.set_under('#999999')
       cmap.set_over('purple')
    mesh = ax.pcolormesh(theta,r.T,rw.T,shading='flat',cmap=cmap,vmin=-40,vmax=40) # plot the data.
    cbar = fig.colorbar(mesh,shrink=0.85,pad=0.10,ax=ax) # add a colorbar.
    cbar.set_label('$m/s$') # radial wind data is in units of meters per second.
    plt.title('Doppler Velocity \n Station ID: '+STAID\
              +'  Scan Angle: '+str(anel0)\
              +'  Date: '+str(date),fontsize=15,y=1.12) # add a useful title.
    ax.grid(True)
    plt.show() # make the plot.
    plt.savefig(figname+'.png',bbox_inches='tight') # save figure.

    #7. CALCULATE SOME STATS
    toc = time.clock() # check to see how long it took to run.
    sec = str(toc-tic)
    print('time it took to run: '+sec+' seconds.')

if __name__ == "__main__":
    main()
