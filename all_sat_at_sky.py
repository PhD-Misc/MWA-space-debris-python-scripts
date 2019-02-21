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


number_of_lines_in_tle = sum(1 for line in open('tle.txt'))

number_of_satellites = number_of_lines_in_tle/2


print('The tle file has ' + str(number_of_lines_in_tle) + ' lines and ' + str(number_of_satellites) + ' satellites')


with open('tle.txt') as f:

	for i in range(116):
		i+=1
		hud1 = fits.open('1102603216-2m-t00' + str(i).zfill(2) + '-dirty.fits')
	        hud2 = fits.open('1102603216-2m-t00' + str(i+1).zfill(2) + '-dirty.fits')
	        header = hud2[0].header
	        wcs = WCS(header, naxis=2)
	        UTCtime = datetime.strptime(header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S') +timedelta(seconds=7)
	        mwa.date = UTCtime

		tleLineNo = 0
		tleLine1 = 'sat'
	
		for SatNo in range(number_of_satellites):
			line2 = f.read().split('\n')[tleLineNo]
			tleLineNo += 1
			line3 = f.read().split('\n')[tleLineNo]
			tleLineNo += 1
			
			sat.emphem.readtle(line1, line2, line3)
			sat.compute(mwa)
			x, y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]

			if (0 <= x < 10000) and (0 <= y < 10000):
				plt.plot(x,y, marker='+', color'b')
				print('sat' + str(SatNo) + ' is in the image ')
			else:
				print('sat' + str(SatNo) + 'is NOT in the image')

		plt.savefig('all_sat_diff_image' + str(i) + '.png')
		print('saving image ' + str(i) + '...')




