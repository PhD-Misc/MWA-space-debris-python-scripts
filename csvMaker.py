from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.wcs import WCS
from datetime import datetime, timedelta
from astropy.coordinates import AltAz, SkyCoord, EarthLocation
import astropy.units as u
import math
import csv
hfont = {'fontname':'Helvetica', 'size':18}

#perthChannels = [90.5,92.1,92.9,93.7,94.5,95.3,96.1,96.9,97.7,98.5,99.1,100.1,100.9,101.7,103.3,104.9]
perthChannels = [96.9,97.7,99.3]

def getVal(val):
    minFreq = val - 20.0*1000.0/1000000.0
    maxFreq = val + 20.0*1000.0/1000000.0
    #print("the min value is " + str(minFreq))
    #print("the max value is " + str(maxFreq))
    FMChannel = [m for m in perthChannels if m>=minFreq and m<=maxFreq]
    #print(FMChannel)
    if len(FMChannel) == 0:
        newVal = 110
    else:
        newVal = 95
    #print('The new value is ' + str(newVal))
    return newVal


def radec_to_altaz(ra, dec, time, pos):
    coord = SkyCoord(ra, dec, unit=(u.deg, u.deg))
    coord.time = time + timedelta(hours=pos.lon.hourangle)
    coord = coord.transform_to(AltAz(obstime=time, location=pos))
    return np.degrees(coord.alt.rad), np.degrees(coord.az.rad)

globalData = np.zeros((2000,2000))
altaz = np.zeros((900,3600))
pos = EarthLocation(lon=116.67083333*u.deg, lat=-26.70331941*u.deg, height=377.827*u.m)


with open('RFI.csv','w') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['az','alt','UTC','freq','numFreq','ra','dec'])


    obsID = [1244057704,1244057408,1244057112,1244056816,1244056520,1244056224]

    for ID in obsID:
        for i in range(150):
            try:
                hdu = fits.open(str(ID) + '/8SigmaRFIBinaryMap-withFreq-t' + str(i).zfill(4) + '.fits')
                hdu2= fits.open(str(ID) + '/8SigmanofreqbinaryMap-' + str(i).zfill(4) + '.fits')
            except:
                continue
            data = hdu[0].data
            data2 = hdu2[0].data
            wcs = WCS(hdu[0].header, naxis=2)
            UTC = datetime.strptime(hdu[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
            Points1 = np.asarray(np.where(data>0))
            pixcrd = np.array((Points1[1,:], Points1[0,:]),dtype=np.float64).T
            print(i)
            if len(Points1[1,:]) > 0:
                world = wcs.wcs_pix2world(pixcrd,0)
                for p in range(len(world[:,0])):
                    alt,az = radec_to_altaz(world[p,0], world[p,1], UTC, pos)
                    freq = data[Points1[0,p], Points1[1,p]]
                    numFreq = data2[Points1[0,p], Points1[1,p]]
                    ra = world[p,0]
                    dec = world[p,1]
                    line = [az,alt,UTC,freq,numFreq,ra,dec]
                    thewriter.writerow(line)



