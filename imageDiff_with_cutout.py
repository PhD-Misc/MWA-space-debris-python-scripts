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
from astropy.nddata import Cutout2D

#The below is the satellite TLe data
line1 = "ISS"
line2 = "1 25544U 98067A   16078.18872957  .00011987  00000-0  18767-3 0  9997"
line3 = "2 25544  51.6438 151.8661 0001598 315.1341 138.1171 15.54181702990822"
sat = ephem.readtle(line1, line2, line3)


#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level


for i in range(200):
	hud1 = fits.open('2sInt-t00' + str(i).zfill(2) + '-dirty.fits')
	hud2 = fits.open('2sInt-t00' + str(i+1).zfill(2) + '-dirty.fits')

        header = hud2[0].header
        wcs = WCS(header, naxis=2)
        UTCTime = datetime.strptime(header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S') + timedelta(seconds=1)

        mwa.date = UTCTime
        sat.compute(mwa)
        xy = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]

        x = int(np.floor(xy[0]))
        y = int(np.floor(xy[1]))

    
        data1 = np.array(hud1[0].data[0,0,:,:])
	data2 = np.array(hud2[0].data[0,0,:,:])
	mean1 = np.mean(data1)
	mean2 = np.mean(data2)
	np.true_divide(data1, mean1)
	np.true_divide(data2, mean2)
	date = hud2[0].header[43]
	dataDiff = data2 - data1
	
        #position = (x , y)
        #size = (1500, 1500)
        
        #cutout = Cutout2D(dataDiff, position, size)

        plt.figure().add_subplot(1,1,1, projection = wcs)
	plt.imshow(dataDiff, cmap=plt.cm.viridis, vmin=-2, vmax=2)
        plt.plot(x, y, marker = '+', color='b')
        plt.xlabel('x-pixels (RA)')
	plt.ylabel('y-pixels (Dec)')
        plt.grid(color='white', ls='solid')
	plt.title(date)
	plt.colorbar()
	plt.savefig('imageDiff' + str(i) + '.png')


