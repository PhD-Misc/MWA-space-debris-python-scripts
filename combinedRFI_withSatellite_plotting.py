from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.wcs import WCS
from astropy.nddata import Cutout2D
import os.path
from argparse import ArgumentParser
import ephem
import time
from datetime import datetime, timedelta
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level


globalData = np.zeros((900,900))
LeoData = np.zeros((900,900))
MeoData = np.zeros((900,900))
HeoData = np.zeros((900,900))








for i in range(150):

    sat_id_array = []
    hdu = fits.open("7SigmaSigmaRFIBinaryMap-t" + str(i).zfill(4) + ".fits")
    globalData += hdu[0].data
    #print("Working on timestep " + str(i))

    wcs = WCS(hdu[0].header, naxis=2)
    if i ==1 or i==148:
        print(wcs)
    #if i ==0:
    #    #plt.gcf().set_size_inches(8, 8)
    #    ax = plt.subplot(111, projection=wcs)
    #    #plt.gcf().set_size_inches(8, 8)
    #if i == 75:
    #    wcs = WCS(hdu[0].header, naxis=2)
    #    UTCtime = datetime.strptime(hdu[0].header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S')
    #UTCtime = datetime.strptime(hdu[0].header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S')
    #mwa.date = UTCtime


timeArray = np.linspace(-200,200, 200)

hdu = fits.open("7SigmaSigmaRFIBinaryMap-t" + str(75).zfill(4) + ".fits")
wcs = WCS(hdu[0].header, naxis=2)
UTCtime = datetime.strptime(hdu[0].header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S')
ax = plt.subplot(111, projection=wcs)

for t in timeArray:
    sat_id_array = []
    mwa.date = UTCtime + timedelta(seconds=t) 
    print(t)
    f = open("LEOtle.txt")
    line = f.readline()
    counter = 1
    line1 = "starlink"
    while line:
        if counter%2 ==1:
            line2 = line
        else:
            line3 = line
            satID = int(line2[2] + line2[3] + line2[4] + line2[5] + line2[6] )
            #print(satID)
            if satID not in sat_id_array:
                sat_id_array.append(satID)
                #print("appended")
                sat = ephem.readtle(str(line1), str(line2), str(line3)) 
                sat.compute(mwa)
                x, y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
                #except:
                #    print("could not calculate")
                #    counter +=1
                #    line = f.readline()
                #    continue
                #print("could calculate tle")
                if (5 <= x <= 1995) and (5<= y < 1995):
                    #print("plotting trail...")
                    #plt.plot(x,y,marker='+',color='blue',markersize='0.25')
                    LeoData[int(y),int(x)] =1
                    LeoData[int(y+1),int(x)] =1
                    LeoData[int(y),int(x+1)] =1
                    LeoData[int(y-1),int(x)] =1
                    LeoData[int(y),int(x-1)] =1
            else:
                counter +=1
                line = f.readline()
                continue

        counter +=1
        line = f.readline()




    #f = open("starlinkTLE.txt")
    #line = f.readline()
    #counter = 1
    #line1 = "starlink"
    #while line:
    #    if counter%2 ==1:
    #        line2 = line
    #    else:
    #        line3 = line
    #        satID = int(line2[2] + line2[3] + line2[4] + line2[5] + line2[6] )
    #        #print(satID)
    #        if satID not in sat_id_array:
    #            sat_id_array.append(satID)
    #            #print("appended")
    #            sat = ephem.readtle(str(line1), str(line2), str(line3))
    #            sat.compute(mwa)
    #            x, y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    #            #except:
    #            #    print("could not calculate")
    #            #    counter +=1
    #            #    line = f.readline()
    #            #    continue
    #            #print("could calculate tle")
    #            if (5 <= x <= 1995) and (5<= y < 1995):
    #                #print("plotting trail...")
    #                #plt.plot(x,y,marker='+',color='blue',markersize='0.25')
    #                LeoData[int(y),int(x)] =1
    #                LeoData[int(y),int(x)] =1
    #                LeoData[int(y+1),int(x)] =1
    #                LeoData[int(y),int(x+1)] =1
    #                LeoData[int(y-1),int(x)] =1
    #                LeoData[int(y),int(x-1)] =1
    #
    #        else:
    #            counter +=1
    #            line = f.readline()
    #            continue
    #
    #    counter +=1
    #    line = f.readline()



    



    f = open("MEOtle.txt")
    line = f.readline()
    counter = 1
    line1 = "starlink"
    while line:
        if counter%2 ==1:
            line2 = line
        else:
            line3 = line
            satID = int(line2[2] + line2[3] + line2[4] + line2[5] + line2[6] )
            #print(satID)
            if satID not in sat_id_array:
                sat_id_array.append(satID)
                #print("appended")
                sat = ephem.readtle(str(line1), str(line2), str(line3))
                sat.compute(mwa)
                x, y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
                #except:
                #    print("could not calculate")
                #    counter +=1
                #    line = f.readline()
                #    continue
                #print("could calculate tle")
                if (5 <= x <= 1995) and (5<= y < 1995):
                    #print("plotting trail...")
                    #plt.plot(x,y,marker='+',color='green',markersize='0.25')
                    LeoData[int(y),int(x)] =1
                    LeoData[int(y+1),int(x)] =1
                    LeoData[int(y),int(x+1)] =1
                    LeoData[int(y-1),int(x)] =1
                    LeoData[int(y),int(x-1)] =1

                    LeoData[int(x),int(y)] =1
            else:
                counter +=1
                line = f.readline()
                continue

        counter +=1
        line = f.readline()

    f = open("starlinkTLE.txt")
    line = f.readline()
    counter = 1
    line1 = "starlink"
    while line:
        if counter%2 ==1:
            line2 = line
        else:
            line3 = line
            satID = int(line2[2] + line2[3] + line2[4] + line2[5] + line2[6] )
            #print(satID)
            if satID not in sat_id_array:
                sat_id_array.append(satID)
                #print("appended")
                sat = ephem.readtle(str(line1), str(line2), str(line3))
                sat.compute(mwa)
                x, y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
                #except:
                #    print("could not calculate")
                #    counter +=1
                #    line = f.readline()
                #    continue
                #print("could calculate tle")
                if (5 <= x <= 1995) and (5<= y < 1995):
                    #print("plotting trail...")
                    #plt.plot(x,y,marker='+',color='black',markersize='0.25')
                    LeoData[int(y),int(x)] =1
                    LeoData[int(y+1),int(x)] =1
                    LeoData[int(y),int(x+1)] =1
                    LeoData[int(y-1),int(x)] =1
                    LeoData[int(y),int(x-1)] =1
                    LeoData[int(y),int(x)] =1
            else:
                counter +=1
                line = f.readline()
                continue

        counter +=1
        line = f.readline()




    f = open("HEOtle.txt")
    line = f.readline()
    counter = 1
    line1 = "starlink"
    while line:
        if counter%2 ==1:
            line2 = line
        else:
            line3 = line
            satID = int(line2[2] + line2[3] + line2[4] + line2[5] + line2[6] )
            #print(satID)
            if satID not in sat_id_array:
                sat_id_array.append(satID)
                #print("appended")
                sat = ephem.readtle(str(line1), str(line2), str(line3))
                sat.compute(mwa)
                x, y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
                #except:
                #    print("could not calculate")
                #    counter +=1
                #    line = f.readline()
                #    continue
                #print("could calculate tle")
                if (5 <= x <= 1995) and (5<= y < 1995):
                    #print("plotting trail...")
                    #plt.plot(x,y,marker='+',color='black',markersize='0.25')
                    LeoData[int(y),int(x)] =1
                    LeoData[int(y+1),int(x)] =1
                    LeoData[int(y),int(x+1)] =1
                    LeoData[int(y-1),int(x)] =1
                    LeoData[int(y),int(x-1)] =1
                    LeoData[int(y),int(x)] =1
            else:
                counter +=1
                line = f.readline()
                continue

        counter +=1
        line = f.readline()






globalData = np.where(globalData==0,-8,globalData) 

globalData = np.ma.masked_where(globalData >0, globalData)
cmap = plt.cm.Purples
cmap.set_bad(color='red')


Points1 = np.asarray(np.where(globalData>0))
#ax.scatter(Points1[1,:], Points1[0,:],marker='o',c='red', s=1)


PointsLEO = np.asarray(np.where(LeoData ==1))
PointsMEO = np.asarray(np.where(MeoData ==1))
PointsHEO = np.asarray(np.where(HeoData ==1))


#plt.show()


#plt.plot(PointsLEO[1,:], PointsLEO[0,:],marker='+',c='blue', markersize='0.25')
#plt.plot(PointsMEO[1,:], PointsMEO[0,:],marker='+',c='green', markersize='0.25')
#plt.plot(PointsHEO[1,:], PointsHEO[0,:],marker='+',c='black', markersize='0.25')

plt.imshow(LeoData, cmap=cmap, origin='lower')

ax.scatter(Points1[1,:], Points1[0,:],marker='o',c='red', s=1)



#ax = plt.subplot(1,1,1, projection=wcs)
#plt.imshow(globalData, cmap=cmap, origin='lower',vmin=-8, vmax=1)
#plt.imshow(LeoData, cmap=cmap, origin='lower')
plt.grid(color='blue',linestyle='-',linewidth='1')
plt.xlabel("RA (Degrees)")
plt.ylabel("Dec (Degrees)")
#plt.colorbar()

plt.show()
