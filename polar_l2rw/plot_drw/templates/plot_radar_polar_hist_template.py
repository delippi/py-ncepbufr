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
    obstr= 'DIST125M DMVR DVSW' #NL2RW--level 2 radial wind.
    #obstr2='STDM SUPLON SUPLAT HEIT RWND RWAZ RSTD' #RWSOB--radial wind super ob.

    #1. INITIALIZING SOME BASIC LISTS AND GETTING INPUT DATA.
    i=0; sids=[]; lons=[]; lats=[]; l2rw=[]; anel=[]; anaz=[]; dist125m=[]; ymdhm=[]; radii=[]; PRF=[]
    OBS_FILE=sys.argv[1]; message_type=sys.argv[2]; date=sys.argv[3]; STAID=sys.argv[4]
    OBS_FILECPY=OBS_FILE+"_cpy"

    anel0=float(sys.argv[5])
    del_anel=0.25
    maxanaz=0
     
    #2. READ PREPBUFR FILE.
    b='false' # used for breaking the loop.
    bufr = ncepbufr.open(OBS_FILE) # bufr file for reading.
    bufrcpy=ncepbufr.open(OBS_FILECPY) # bufr file for reading ahead and determining maxanaz.
    bufr.dump_table('l2rwbufr.table') # dump table to file.
    while bufr.advance() == 0: # loop over messages.
       #bufr has been advanced, now if reading concurrently, bufrcpy should be behind by one. But sometimes
       #bufrcpy could be ahead of where we need it (but only by one step) since we read it forward. 
       #We don't want to advance it in that case.
       if( (bufr.msg_counter-bufrcpy.msg_counter)==1): bufrcpy.advance()
       print(bufr.msg_counter, bufr.msg_type, bufr.msg_date)
       if(bufr.msg_type == message_type):
            while bufr.load_subset() == 0: # loop over subsets in message.
                hdr = bufr.read_subset(hdstr).squeeze() # parse hdstr='SSTN CLON ... etc.'
                station_id = hdr[0].tostring() # convert SSTN to string.
                station_id=station_id.strip()  # remove white space from SSTN.
                #*********************
                bufrcpy.load_subset()#**********************
                hdrcpy=bufrcpy.read_subset(hdstr).squeeze()#
                #*******************************************
                if(station_id == STAID): # comes from input. used for picking a single SSTN.
                    if(hdr[4] >= anel0-del_anel and hdr[4] <= anel0+del_anel): # read an elevation angle.
                        obs = bufr.read_subset(obstr).squeeze() # parse obstr='DIST125M DMVR DVSW'
                        #*******************************************
                        obscpy=bufrcpy.read_subset(obstr).squeeze()#
                        #*******************************************
                        print(bufr.msg_counter,'SSTN,CLON,CLAT,ANAL,ANAZ : ',station_id,hdr[1],hdr[2],hdr[4],hdr[11])
                        i=i+1  #number of observations counter.
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
                               maxanaz=max(maxanaz,int(np.ceil(hdrcpy[11]))) #need hdrcpy[11] rounded up.
                           tries=0
                           while tries < 10 and bufrcpy.advance() == 0: # look no. tries messages ahead.
                              tries+=1
                              while bufrcpy.load_subset() == 0:
                                  if(bufrcpy.msg_type == message_type):
                                     station_id = hdrcpy[0].tostring() # convert SSTN to string.
                                     station_id=station_id.strip()  # remove white space from SSTN.
                                     if(station_id == STAID):
                                        if(hdrcpy[4] >= anel0-del_anel and hdrcpy[4] <= anel0+del_anel):
                                           hdrcpy= bufrcpy.read_subset(hdstr).squeeze()
                                           maxanaz=max(maxanaz,int(np.ceil(hdrcpy[11])))
                                           print(bufrcpy.msg_counter,'cpySSTN,DATE/TIME : ',station_id,hdrcpy[5:10],hdrcpy[4],hdrcpy[11],len(anaz))
                              print(maxanaz)
                        if(len(anaz) >= 355): print(len(anaz),maxanaz)
#***********************************************************************************************************
                        if(len(anaz) == maxanaz and len(anaz)> 355):
                           while(len(anaz) < 360): #fill in some missing data points
                              l2rw.append(obs[1]*0 + -999.)
                              anel.append(anel[-1])
                              anaz.append(anaz[-1]+1)
                              radii.append(radii[-1])
                              ymdhm.append(ymdhm[-1])
                           while(len(anaz) < 361): # fill in the final beam with nan mean between 1st and 359th
                              l2rw.append(l2rw[0])
                              anel.append(anel[0])
                              anaz.append(anaz[-1]+1)
                              radii.append(radii[0])
                              ymdhm.append(ymdhm[0])
                           b='true'
       if(b == 'true'): break # stop reading after all anaz's read.
    bufr.close()
    print("number of obs: ",i)
    MM=str(ymdhm[-1])
    print(np.min(anel),np.max(anel))
    print(np.min(ymdhm),np.max(ymdhm))
    toc = time.clock() # check how long reading the data in took.
    sec = str(toc-tic)
    print('time it took to run: '+sec+' seconds.')

    #3. FIND THE MAX/MIN VALUES OF THE DIST125M AND THETA ARRAYS.
    maxRadii=100000 # set max of max distances to about 100 mi.
    minRadii=0 # min of min distances.

    #4. INITIALIZE THE POLAR PLOT AS ALL MISSING DATA (-999).
    fig = plt.figure(figsize=(8,8)) # 8" x 8" seems plenty large.
    ax = fig.add_subplot(111)
#    ax = fig.add_subplot(111,polar=True) # we would like it to be a polar plot.
#    ax.set_theta_zero_location("N") # set theta zero location to point North.
#    ax.set_theta_direction(-1) # set theta to increase clockwise (-1).
    theta,r = np.meshgrid(anaz,np.arange(minRadii,maxRadii,250.)) # create meshgrid
    theta=deg2rad(theta) # convert theta from degrees to radians.
    rw = np.zeros(shape=(len(theta),len(r[0]))) # initialize the polar plot with all 0's.
    rw.fill(-999) # change all values to missing data (-999).
    #PRF_new=np.zeros(shape=(len(theta),len(r[0])))
    #PRF_new.fill(-999)
    r=r.T; rw=rw.T#; PRF_new.T # transpose r and rw for later manipulation.
    
    #5. POPULATE THE EMPTY RW ARRAY WITH ACTUAL VALUES.
    for i in range(len(anaz)): # for every azimuth angle ...
        sys.stdout.write('\r'+str(i)+'/'+str(len(anaz)))
        sys.stdout.flush()
        for j in range(len(radii[i])): # ... loop over every observation distance from radar ...
            for k in range(len(r[i])): # ... and loop over an equally 125m spaced array ...
                if(radii[i][j] == r[i][k]): # ... if the observation dist = dist125m ...
                    rw[i][k]=l2rw[i][j] # ... assign the value of the observation to that index.
                    #PRF_new[i][k]=PRF[i][j]
                    break # speeds things up by about 50-60%.
    rw[np.isnan(rw)] = -999 # the masked values are converted to nan. set nan to -999.
    print(np.max(rw)) # check that it is not nan.

    ax.hist(rw[rw!=-999.],bins=41)

    plt.title('Doppler Velocity \n Station ID: '+STAID\
              +'  Scan Angle: '+str(anel[0])\
              +'  Date: '+date+MM.zfill(2),fontsize=15,y=1.12) # add a useful title.
    plt.xlabel('velocity (m/s)')
    plt.ylabel('number of obs')
    ax.grid(True)
    plt.show() # make the plot.
    plt.savefig('./'+STAID+'_'+str(anel[0])+'_'+date+MM.zfill(2)+'_hist.png'\
                ,bbox_inches='tight') # save figure.

    #7. CALCULATE SOME STATS
    toc = time.clock() # check to see how long it took to run.
    sec = str(toc-tic)
    print('time it took to run: '+sec+' seconds.')

if __name__ == "__main__":
    main()
