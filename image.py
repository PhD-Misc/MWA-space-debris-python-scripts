from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import astropy
from astropy.wcs import WCS


for i in range(116):
	hud = fits.open('1102604896-2m-t00' + str(i).zfill(2) + '-image.fits')
	data = hud[0].data[0,0,:,:]
	date = hud[0].header[43]
	wcs = WCS(hud[0].header, naxis=2)
	dataNumpy = np.array(data)
	plt.figure().add_subplot(1,1,1, projection = wcs)
	plt.imshow(dataNumpy, cmap=plt.cm.viridis)
	plt.xlabel('x-pixels (RA)')
	plt.ylabel('y-pixels (Dec)')
	plt.title(date)
	plt.colorbar()
	plt.savefig('image' + str(i) + '.png')


