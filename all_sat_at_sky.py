from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import astropy
from astropy.wcs import WCS
import ephem
import time
from datetime import datetime, timedelta
from array import *
import os.path

mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level

hdu1 = fits.open("test1-0553-image.fits")
hdu2 = fits.open("test2-0553-image.fits")
header = hdu2[0].header
wcs = WCS(header, naxis=2)
UTCtime = datetime.strptime(header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S') +timedelta(seconds=0)
mwa.date = UTCtime
line1 = 'ALOS'

diff = hdu2[0].data[0,0,:,:] - hdu1[0].data[0,0,:,:]
print(diff.shape)

#plt.figure().add_subplot(1,1,1, projection=wcs)
plt.imshow(diff)

f = open('tle.txt')
line = f.readline()
counter = 1
while line:
    #print(line)
    
    if counter%2 == 1:
        line2 = line
        #line2 = line2.replace("+", "")
        #line2 = line2.replace("-", "")
    else:
        line3 = line
        #line3 = line3.replace("+", "")
        #line3 = line3.replace("-", "")
        print(line1)
        print(line2)
        print(line3)
        sat=ephem.readtle(str(line1), str(line2),str(line3))
        sat.compute(mwa)
        x, y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
        if (0 <= x < diff.shape[0]) and (0 <= y < diff.shape[1]):
            plt.plot(x,y, marker='+', color='black')
    print(counter)
    counter+=1
    line = f.readline()
print(diff.shape)
plt.show()
