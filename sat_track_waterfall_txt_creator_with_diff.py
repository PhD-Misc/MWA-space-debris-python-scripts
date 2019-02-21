 
import astropy
from astropy.io import fits
from astropy.wcs import WCS
import ephem
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta
from array import *
import os.path


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

waterfall = []
waterfall = np.array(waterfall)
l = 0

i=127 #This increment is done cos the first file is full of zeroes
	
#The below section reads the fits files for image difference
hdu = fits.open('1102603216-2m-' + str(i) + '-0000-dirty.fits')
#data = np.array(hdu[0].data[0,0,:,:]) # This line is redundant
	
#The below code reads the time from the header file
header = hdu[0].header
wcs = WCS(header, naxis=2)
UTCtime = datetime.strptime(header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S') + timedelta(seconds=4)
	
#The below code calculates the pixel of the satellite
mwa.date = UTCtime
sat.compute(mwa)
xy = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
x = int(np.floor(xy[0]))
y = int(np.floor(xy[1]))
#print("The value of x is " + str(x) + " and the value of y is " + str(y))
#print("The value of i is " +str(i))

hdu.close()		
	
	
#The below code gets executed only if the satellite is within the image frame
if (0 <= x < 5000) and (0 <= y < 5000):
	freq_array=[]
	end="false"
	#print("The value of l is " + str(l))
	save_counter=0
	for n in range(1700):
		dataDiff=[]
		print("The value of n is " + str(n))
		if (os.path.isfile('1102603216-2m-' + str(i) + '-' + str(n).zfill(4) + '-dirty.fits')):
			hdutemp1 = fits.open('1102603216-2m-' + str(i) + '-' + str(n).zfill(4) + '-dirty.fits')

			#dataDiff = datatemp1 #note that this line has been changed
			waterfall = np.hstack((waterfall, hdutemp1[0].data[0,0,x,y]))
			#print("Hello world")
			hdutemp1.close()	
		else:
			end="true"
			break
		l=l+1
		#np.absolute(freq_array_modified)
#		if (n%100 == 0) and (n!=0):
	np.savetxt("waterfall-data" + str(i)+ "-"+ str(n) + ".txt", waterfall )
	save_counter += 1
	waterfall = []
	print("The last frequency channel is n " + str(n))
#		if (end == "true"):
#			np.savetxt("waterfall-data" + str(i) + "-" + str(save_counter) + ".txt", waterfall)
#			print("The last frequency channel is " + str(n))
		
