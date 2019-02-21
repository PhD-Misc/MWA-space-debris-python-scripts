import astropy
from astropy.io import fits
from astropy.wcs import WCS
import ephem
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta

#the below is the satellite tle data
line1 = "DUCHAFAT 1"
line2 = "1 40021U 14033M   14348.10384436  .00004745  00000-0  54091-3 0  9999"
line3 = "2 40021 097.9694 243.1318 0015413 071.7045 288.5857 14.86534944 26293"
sat = ephem.readtle(line1, line2, line3)


#the below sets the observation from MWA
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level


for i in range(100):
	
	i+=1 #This increment is done cos the first file is full of zeroes
	
	#the below section reads the fits files for image difference
	hdu1 = fits.open('1102603216-2m-t00' + str(i).zfill(2) + '-image.fits')
	hdu2 = fits.open('1102603216-2m-t00' + str(i+1).zfill(2) + '-image.fits')
	data1 = np.array(hdu1[0].data[0,0,:,:])
	data2 = np.array(hdu2[0].data[0,0,:,:])
        mean1 = np.mean(data1)
        mean2 = np.mean(data2)
        np.true_divide(data1, mean1)
        np.true_divide(data2, mean2)
	
	#The below code reads the time from the second header file
	header = hdu2[0].header
	wcs = WCS(header, naxis=2)
	UTCtime = datetime.strptime(header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S')

	#The below code plots the difference data
	dataDiff = data2 - data1
	plt.figure().add_subplot(1,1,1, projection = wcs)
	plt.imshow(dataDiff, cmap=plt.cm.viridis, vmin =-2, vmax=2) #vmin and vmax can be added here
	plt.xlabel('x (RA)')
	plt.ylabel('y (Dec)')
	plt.title(UTCtime)
	plt.colorbar()
	

	#The below code calculates the pixel of satellite
	mwa.date = UTCtime
	sat.compute(mwa)
	x, y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
	
	#The below plots the sat pixel if within frame
	if (0 <= x < 240) and (0 <= y < 240):
		plt.plot(x, y, marker='o', color='b')
		

	#The below code can be replaced with plt.show() or plt.savefig()
	plt.savefig('testSat' + str(i) + '.png')
	





