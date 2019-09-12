from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.wcs import WCS
from datetime import datetime, timedelta
from astropy.coordinates import AltAz, SkyCoord, EarthLocation
import astropy.units as u
import math

hfont = {'fontname':'Helvetica', 'size':18}

def getVal(val):
    return val

def radec_to_altaz(ra, dec, time, pos):
    coord = SkyCoord(ra, dec, unit=(u.deg, u.deg))
    coord.time = time + timedelta(hours=pos.lon.hourangle)
    coord = coord.transform_to(AltAz(obstime=time, location=pos))
    return np.degrees(coord.alt.rad), np.degrees(coord.az.rad)

globalData = np.zeros((2000,2000))
altaz = np.zeros((900,3600))
altazI = np.zeros((900,3600))
pos = EarthLocation(lon=116.67083333*u.deg, lat=-26.70331941*u.deg, height=377.827*u.m)

for i in range(150):
    altaz = np.zeros((900,3600))
    altazI = np.zeros((900,3600))

    try:
        hdu = fits.open("8SigmaRFIBinaryMap-withFreq-t" + str(i).zfill(4) + ".fits")
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
        hduInt = fits.open("8SigmaintensitybinaryMap-" + str(i).zfill(4) + ".fits")
        dataI = hduInt[0].data
        print(world.shape)
        for p in range(len(world[:,0])):
            alt, az = radec_to_altaz(world[p,0], world[p,1], UTC, pos)
            if math.isnan(alt) or math.isnan(az):
                continue
            alt = int(round(alt*10))
            az = int(round(az*10))
            
            val = data[Points1[0,p], Points1[1,p]]
            val = getVal(val)
            #print("The value is " + str(val))
            altaz[alt,az] = val
            altaz[alt+1,az] = val
            altaz[alt,az+1] = val
            altaz[alt-1,az] = val
            altaz[alt,az-1] = val

            INT = dataI[Points1[0,p], Points1[1,p]]
            altazI[alt,az] = INT
            altazI[alt+1,az] = INT
            altazI[alt,az+1] = INT
            altazI[alt-1,az] = INT
            altazI[alt,az-1] = INT



    scale = plt.cm.Purples(np.linspace(0,1,100))
    altaz = np.ma.masked_where(altaz ==0, altaz)
    cmap = plt.cm.Set3
    cmap.set_bad(color=scale[10])
    plt.subplot(2,1,1)
    plt.title(UTC)
    plt.imshow(altaz, cmap=plt.cm.Set3, origin="lower", interpolation='nearest', aspect='auto', extent=[0,360,0,90], vmin=81, vmax=112)
    plt.colorbar()
    plt.xlabel("Azimuth (Degrees)",**hfont)
    plt.ylabel("Elevation (Degrees)",**hfont)
    plt.grid()


    plt.subplot(2,1,2)
    altazI = np.ma.masked_where(altazI ==0, altazI)
    cmap2 = plt.cm.inferno
    cmap2.set_bad(color=scale[10])
    plt.imshow(altazI, cmap=cmap2, origin="lower", interpolation='nearest', aspect='auto', extent=[0,360,0,90])
    plt.colorbar()
    plt.xlabel("Azimuth (Degrees)",**hfont)
    plt.ylabel("Elevation (Degrees)",**hfont)
    plt.grid()

    if len(Points1[1,:]) > 0:
        plt.show()
        plt.savefig('img' + str(i) + '.png')
    plt.clf()
