from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.wcs import WCS
from datetime import datetime, timedelta
from astropy.coordinates import AltAz, SkyCoord, EarthLocation
import astropy.units as u
import math

hfont = {'fontname':'Helvetica', 'size':18}

#perthChannels = [90.5,92.1,92.9,93.7,94.5,95.3,96.1,96.9,97.7,98.5,99.1,100.1,100.9,101.7,103.3,104.9]
#perthChannels = [94.9,96.5,98.1,98.9,99.7,101.3]
perthChannels = [98.1]

def getVal(val):
    newVal = val
    #minFreq = val - 20.0*1000.0/1000000.0
    #maxFreq = val + 20.0*1000.0/1000000.0
    #print("the min value is " + str(minFreq))
    #print("the max value is " + str(maxFreq))
    #FMChannel = [m for m in perthChannels if m>=minFreq and m<=maxFreq]
    #print(FMChannel)
    #if len(FMChannel) == 0:
    #    newVal = 110
    #else:
    #    newVal = 95
    ##print('The new value is ' + str(newVal))
    return newVal


def radec_to_altaz(ra, dec, time, pos):
    coord = SkyCoord(ra, dec, unit=(u.deg, u.deg))
    coord.time = time + timedelta(hours=pos.lon.hourangle)
    coord = coord.transform_to(AltAz(obstime=time, location=pos))
    return np.degrees(coord.alt.rad), np.degrees(coord.az.rad)

globalData = np.zeros((2000,2000))
altaz = np.zeros((900,3600))
pos = EarthLocation(lon=116.67083333*u.deg, lat=-26.70331941*u.deg, height=377.827*u.m)

for i in range(150):
    try:
        hdu = fits.open("1244057704/8SigmaintensitybinaryMap-" + str(i).zfill(4) + ".fits")
    except:
        continue
    data = hdu[0].data
    wcs = WCS(hdu[0].header, naxis=2)
    UTC = datetime.strptime(hdu[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
    globalData += hdu[0].data
    Points1 = np.asarray(np.where(data>0))
    pixcrd = np.array((Points1[1,:], Points1[0,:]),dtype=np.float64).T
    print(i)
    if len(Points1[1,:]) > 0:
        world = wcs.wcs_pix2world(pixcrd,0)
        print(world.shape)
        for p in range(len(world[:,0])):
            alt, az = radec_to_altaz(world[p,0], world[p,1], UTC, pos)
            if math.isnan(alt) or math.isnan(az):
                continue
            alt = int(round(alt*10))
            az = int(round(az*10))
            #altaz[alt,az] = 1
            #altaz[alt+1,az] = 1
            #altaz[alt,az+1] = 1
            #altaz[alt-1,az] = 1
            #altaz[alt,az-1] = 1
            
            val = data[Points1[0,p], Points1[1,p]]
            val = getVal(val)
            #print("The value is " + str(val))
            altaz[alt,az] = val
            altaz[alt+1,az] = val
            altaz[alt,az+1] = val
            altaz[alt-1,az] = val
            altaz[alt,az-1] = val

for i in range(150):
    try:
        hdu = fits.open("1244057408/8SigmaintensitybinaryMap-" + str(i).zfill(4) + ".fits")
    except:
        continue
    data = hdu[0].data
    wcs = WCS(hdu[0].header, naxis=2)
    UTC = datetime.strptime(hdu[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
    globalData += hdu[0].data
    Points1 = np.asarray(np.where(data>0))
    pixcrd = np.array((Points1[1,:], Points1[0,:]),dtype=np.float64).T
    print(i)
    if len(Points1[1,:]) > 0:
        world = wcs.wcs_pix2world(pixcrd,0)
        print(world.shape)
        for p in range(len(world[:,0])):
            alt, az = radec_to_altaz(world[p,0], world[p,1], UTC, pos)
            if math.isnan(alt) or math.isnan(az):
                continue
            alt = int(round(alt*10))
            az = int(round(az*10))
            #altaz[alt,az] = 1
            #altaz[alt+1,az] = 1
            #altaz[alt,az+1] = 1
            #altaz[alt-1,az] = 1
            #altaz[alt,az-1] = 1

            val = data[Points1[0,p], Points1[1,p]]
            val = getVal(val)
            #print("The value is " + str(val))
            altaz[alt,az] = val
            altaz[alt+1,az] = val
            altaz[alt,az+1] = val
            altaz[alt-1,az] = val
            altaz[alt,az-1] = val

for i in range(150):
    try:
        hdu = fits.open("1244057112/8SigmaintensitybinaryMap-" + str(i).zfill(4) + ".fits")
    except:
        continue
    data = hdu[0].data
    wcs = WCS(hdu[0].header, naxis=2)
    UTC = datetime.strptime(hdu[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
    globalData += hdu[0].data
    Points1 = np.asarray(np.where(data>0))
    pixcrd = np.array((Points1[1,:], Points1[0,:]),dtype=np.float64).T
    print(i)
    if len(Points1[1,:]) > 0:
        world = wcs.wcs_pix2world(pixcrd,0)
        print(world.shape)
        for p in range(len(world[:,0])):
            alt, az = radec_to_altaz(world[p,0], world[p,1], UTC, pos)
            if math.isnan(alt) or math.isnan(az):
                continue
            alt = int(round(alt*10))
            az = int(round(az*10))
            #altaz[alt,az] = 1
            #altaz[alt+1,az] = 1
            #altaz[alt,az+1] = 1
            #altaz[alt-1,az] = 1
            #altaz[alt,az-1] = 1

            val = data[Points1[0,p], Points1[1,p]]
            val = getVal(val)
            #print("The value is " + str(val))
            altaz[alt,az] = val
            altaz[alt+1,az] = val
            altaz[alt,az+1] = val
            altaz[alt-1,az] = val
            altaz[alt,az-1] = val

for i in range(150):
    try:
        hdu = fits.open("1244056816/8SigmaintensitybinaryMap-" + str(i).zfill(4) + ".fits")
    except:
        continue
    data = hdu[0].data
    wcs = WCS(hdu[0].header, naxis=2)
    UTC = datetime.strptime(hdu[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
    globalData += hdu[0].data
    Points1 = np.asarray(np.where(data>0))
    pixcrd = np.array((Points1[1,:], Points1[0,:]),dtype=np.float64).T
    print(i)
    if len(Points1[1,:]) > 0:
        world = wcs.wcs_pix2world(pixcrd,0)
        print(world.shape)
        for p in range(len(world[:,0])):
            alt, az = radec_to_altaz(world[p,0], world[p,1], UTC, pos)
            if math.isnan(alt) or math.isnan(az):
                continue
            alt = int(round(alt*10))
            az = int(round(az*10))
            #altaz[alt,az] = 1
            #altaz[alt+1,az] = 1
            #altaz[alt,az+1] = 1
            #altaz[alt-1,az] = 1
            #altaz[alt,az-1] = 1

            val = data[Points1[0,p], Points1[1,p]]
            val = getVal(val)
            #print("The value is " + str(val))
            altaz[alt,az] = val
            altaz[alt+1,az] = val
            altaz[alt,az+1] = val
            altaz[alt-1,az] = val
            altaz[alt,az-1] = val

for i in range(150):
    try:
        hdu = fits.open("1244056520/8SigmaintensitybinaryMap-" + str(i).zfill(4) + ".fits")
    except:
        continue
    data = hdu[0].data
    wcs = WCS(hdu[0].header, naxis=2)
    UTC = datetime.strptime(hdu[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
    globalData += hdu[0].data
    Points1 = np.asarray(np.where(data>0))
    pixcrd = np.array((Points1[1,:], Points1[0,:]),dtype=np.float64).T
    print(i)
    if len(Points1[1,:]) > 0:
        world = wcs.wcs_pix2world(pixcrd,0)
        print(world.shape)
        for p in range(len(world[:,0])):
            alt, az = radec_to_altaz(world[p,0], world[p,1], UTC, pos)
            if math.isnan(alt) or math.isnan(az):
                continue
            alt = int(round(alt*10))
            az = int(round(az*10))
            #altaz[alt,az] = 1
            #altaz[alt+1,az] = 1
            #altaz[alt,az+1] = 1
            #altaz[alt-1,az] = 1
            #altaz[alt,az-1] = 1

            val = data[Points1[0,p], Points1[1,p]]
            val = getVal(val)
            #print("The value is " + str(val))
            altaz[alt,az] = val
            altaz[alt+1,az] = val
            altaz[alt,az+1] = val
            altaz[alt-1,az] = val
            altaz[alt,az-1] = val

for i in range(150):
    try:
        hdu = fits.open("1244056224/8SigmaintensitybinaryMap-" + str(i).zfill(4) + ".fits")
    except:
        continue
    data = hdu[0].data
    wcs = WCS(hdu[0].header, naxis=2)
    UTC = datetime.strptime(hdu[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
    globalData += hdu[0].data
    Points1 = np.asarray(np.where(data>0))
    pixcrd = np.array((Points1[1,:], Points1[0,:]),dtype=np.float64).T
    print(i)
    if len(Points1[1,:]) > 0:
        world = wcs.wcs_pix2world(pixcrd,0)
        print(world.shape)
        for p in range(len(world[:,0])):
            alt, az = radec_to_altaz(world[p,0], world[p,1], UTC, pos)
            if math.isnan(alt) or math.isnan(az):
                continue
            alt = int(round(alt*10))
            az = int(round(az*10))
            #altaz[alt,az] = 1
            #altaz[alt+1,az] = 1
            #altaz[alt,az+1] = 1
            #altaz[alt-1,az] = 1
            #altaz[alt,az-1] = 1

            val = data[Points1[0,p], Points1[1,p]]
            val = getVal(val)
            #print("The value is " + str(val))
            altaz[alt,az] = val
            altaz[alt+1,az] = val
            altaz[alt,az+1] = val
            altaz[alt-1,az] = val
            altaz[alt,az-1] = val


#for i in range(150):
#    try:
#        hdu = fits.open("1244057408/8SigmaRFIBinaryMap-withFreq-t" + str(i).zfill(4) + ".fits")
#    except:
#        continue
#    data = hdu[0].data
#    wcs = WCS(hdu[0].header, naxis=2)
#    UTC = datetime.strptime(hdu[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
#    globalData += hdu[0].data
#    Points1 = np.asarray(np.where(data>0))
#    pixcrd = np.array((Points1[1,:], Points1[0,:]),dtype=np.float64).T
#    print(i)
#    if len(Points1[1,:]) > 0:
#        world = wcs.wcs_pix2world(pixcrd,0)
#        print(world.shape)
#        for p in range(len(world[:,0])):
#            alt, az = radec_to_altaz(world[p,0], world[p,1], UTC, pos)
#            if math.isnan(alt) or math.isnan(az):
#                continue
#            alt = int(round(alt*10))
#            az = int(round(az*10))
#            #altaz[alt,az] = 1
#            #altaz[alt+1,az] = 1
#            #altaz[alt,az+1] = 1
#            #altaz[alt-1,az] = 1
#            #altaz[alt,az-1] = 1

#            val = data[Points1[0,p], Points1[1,p]]
#            val = getVal(val)
#            #print("The value is " + str(val))
#            altaz[alt,az] = val
#            altaz[alt+1,az] = val
#            altaz[alt,az+1] = val
#            altaz[alt-1,az] = val
#            altaz[alt,az-1] = val

#for i in range(150):




scale = plt.cm.Purples(np.linspace(0,1,100))
altaz = np.ma.masked_where(altaz ==0, altaz)
cmap = plt.cm.Set3
cmap.set_bad(color=scale[40])
plt.imshow(altaz, cmap=plt.cm.inferno, origin="lower", interpolation='nearest', aspect='auto', extent=[0,360,0,90], vmax=350)
plt.colorbar()
plt.xlabel("Azimuth (Degrees)",**hfont)
plt.ylabel("Elevation (Degrees)",**hfont)
plt.grid()
plt.show()
