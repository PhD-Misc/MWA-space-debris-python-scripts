from astropy.io import fits
import matplotlib.pyplot as plt

for i in range(29):
	data1 = {}
	data2 = {}
	temp1 = fits.open('1102603216-2m-t00' + str(i).zfill(2) + '-image.fits')
	temp2 = fits.open('1102603216-2m-t00' + str(i).zfill(2) + '-image.fits')
	data1 = temp1[0].data
	data2 = temp2[0].data
	data1Modified = data1[0,0,:,:]
	data2Modified = data2[0,0,:,:]
	dataDiff = data2Modified-data1Modified
	plt.imshow(dataDiff, cmap=plt.cm.viridis)
	plt.xlabel('x-pixels (RA)')
	plt.ylabel('y-pixels (Dec)')
	plt.colorbar()
	plt.savefig('image' + str(i) + '.png')

