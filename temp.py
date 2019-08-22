from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.wcs import WCS
from datetime import datetime, timedelta
from astropy.coordinates import AltAz, SkyCoord, EarthLocation
import astropy.units as u
import math

hfont = {'fontname':'Helvetica', 'size':18}


def radec_to_altaz(ra, dec, time, pos):
    coord = SkyCoord(ra, dec, unit=(u.deg, u.deg))
    coord.time = time + timedelta(hours=pos.lon.hourangle)
    coord = coord.transform_to(AltAz(obstime=time, location=pos))
    return np.degrees(coord.alt.rad), np.degrees(coord.az.rad)


globalData = np.zeros((2000,2000))
altaz = np.zeros((900,3600))
pos = EarthLocation(lon=116.67083333*u.deg, lat=-26.70331941*u.deg, height=377.827*u.m)


hdu = fits.open("cleaned-image.fits")
header = hdu[0].header
#print(header)
data = hdu[0].data[0,0,:,:]
wcs = WCS(hdu[0].header, naxis=2)
UTC = datetime.strptime(hdu[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
Points1 = np.asarray(np.where(data>=1))

print(Points1)
pixcrd = np.array((Points1[1,:], Points1[0,:]),dtype=np.float64).T
world = wcs.wcs_pix2world(pixcrd,0)
#print(pixcrd)
for p in range(len(world[:,0])):
    
    #print(world[p,0])
    #print(world[p,1])
    alt, az = radec_to_altaz(world[p,0], world[p,1], UTC, pos)
    if math.isnan(alt) or math.isnan(az):
        continue
    alt = int(round(alt*10))
    az = int(round(az*10))
    print(p)
    val = data[Points1[0,p], Points1[1,p]]
    altaz[alt,az] += val*100
    altaz[alt+1,az] += val*100
    altaz[alt,az+1] += val*100
    altaz[alt-1,az] += val*100
    altaz[alt,az-1] += val*100
altaz = np.ma.masked_where(altaz ==0, altaz)
cmap = plt.cm.inferno
cmap.set_bad(color='white')

plt.imshow(altaz, cmap=cmap, origin="lower", interpolation='nearest', aspect='auto', extent=[0,360,0,90])
#plt.plot(Points1[1,:], Points1[0,:], marker='+')
plt.colorbar()
plt.xlabel("Azimuth (Degrees)",**hfont)
plt.ylabel("Elevation (Degrees)",**hfont)
plt.grid()
plt.show()


