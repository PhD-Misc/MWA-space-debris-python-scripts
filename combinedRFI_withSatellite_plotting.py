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
import matplotlib.pyplot as plt

mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level


globalData = np.zeros((2000,2000))
LeoData = np.zeros((2000,2000))
MeoData = np.zeros((2000,2000))
HeoData = np.zeros((2000,2000))

def trunc(values, decs=0):
    return np.trunc(values*10**decs)/(10**decs)

for i in range(149):


    sat_id_array = []
    try:
        hdu = fits.open("1244057704/7SigmaRFIBinaryMap-withFreq-t" + str(i).zfill(4) + ".fits")
    except:
        continue
    globalData += hdu[0].data
    print(i)
    if i==75:

        header = hdu[0].header


globalData = globalData*100.0
globalData = globalData.astype(int)
#flat = np.reshape(globalData, (1,400000))
temp = np.around(globalData,decimals=3)
#temp = globalData
temp = np.unique(temp)
temp = temp.astype(int)
temp = [k for k in temp if 8100 <k<11500]
print(len(temp))

globalData = np.ma.masked_where(globalData< 81 , globalData)
cmap=plt.cm.tab20
#cmap = plt.cm.Greys
cmap.set_bad(color='white')
plt.imshow(globalData,cmap=cmap, origin='lower', vmin='8100', vmax=11500)
plt.colorbar()
plt.show()

Points1 = np.asarray(np.where(globalData>0))
#x.scatter(Points1[1,:], Points1[0,:],marker='o',c='red', s=1)



