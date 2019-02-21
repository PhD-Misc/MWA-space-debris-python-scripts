from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import astropy
from astropy.wcs import WCS


for i in range(116):
	i+= 1
	hud1 = fits.open('1102604896-2m-t00' + str(i).zfill(2) + '-image.fits')
	hud2 = fits.open('1102604896-2m-t00' + str(i+1).zfill(2) + '-image.fits')
	data1 = np.array(hud1[0].data[0,0,:,:])
	data2 = np.array(hud2[0].data[0,0,:,:])
	mean1 = np.mean(data1)
	mean2 = np.mean(data2)
	np.true_divide(data1, mean1)
	np.true_divide(data2, mean2)
	date = hud2[0].header[43]
	wcs = WCS(hud2[0].header, naxis=2)
	dataDiff = data2 - data1
	plt.figure().add_subplot(1,1,1, projection = wcs)
	plt.imshow(dataDiff, cmap=plt.cm.viridis, vmin=-1, vmax=1)
	plt.xlabel('x-pixels (RA)')
	plt.ylabel('y-pixels (Dec)')
	plt.title(date)
	plt.colorbar()
	plt.savefig('imageDiff' + str(i) + '.png')



