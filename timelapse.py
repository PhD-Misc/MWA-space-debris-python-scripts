from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.wcs import WCS
from datetime import datetime

background = plt.cm.Purples(np.linspace(0,1,13))
c = plt.cm.Greys(np.linspace(0,1,13))
globalMap = np.zeros((900,900))
for i in range(150):
    print(i)
    
    try:
        hdu1 = fits.open("7SigmaSigmaRFIBinaryMap-t" + str(i).zfill(4) + ".fits")
        data1 = hdu1[0].data
        points1 = np.asarray(np.where(data1!=0))
        wcs = WCS(hdu1[0].header, naxis=2)
        UTCTime = datetime.strptime(hdu1[0].header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S')
        ax = plt.subplot(111, projection=wcs)
        globalMap = np.ma.masked_where(globalMap==0, globalMap)
        cmap = plt.cm.inferno
        cmap.set_bad(color=background[2])
        plt.imshow(globalMap, cmap=cmap, origin='lower')
        plt.xlabel('RA (Degrees)')
        plt.ylabel('DEC (Degrees)')
        plt.title(str(UTCTime) + " TimeStep " + str(i+1) + "/150")
    except:
        plt.grid()
        plt.savefig("Timelapse" + str(i).zfill(4) + ".png", facecolor=c[2])
        continue

    try:
        hdu2 = fits.open("7SigmaSigmaRFIBinaryMap-t" + str(i-1).zfill(4) + ".fits")
        data2 = hdu2[0].data
        points2 = np.asarray(np.where(data2!=0))
    except:
        ax.scatter(points1[1,:], points1[0,:],marker='o',c=c[12], s=1)
        plt.grid()
        plt.title(str(UTCTime) + " TimeStep " + str(i+1) + "/150")
        plt.savefig("Timelapse" + str(i).zfill(4) + ".png",facecolor=c[2])
        continue
    
    try:
        hdu3 = fits.open("7SigmaSigmaRFIBinaryMap-t" + str(i-2).zfill(4) + ".fits")
        data3 = hdu3[0].data
        points3 = np.asarray(np.where(data3!=0))
    except:
        ax.scatter(points2[1,:], points2[0,:],marker='o',c=c[6], s=1)
        ax.scatter(points1[1,:], points1[0,:],marker='o',c=c[12], s=1)
        plt.grid()
        plt.title(str(UTCTime) + " TimeStep " + str(i+1) + "/150")
        plt.savefig("Timelapse" + str(i).zfill(4) + ".png",facecolor=c[2])
        continue
    
    try:
        hdu4 = fits.open("7SigmaSigmaRFIBinaryMap-t" + str(i-3).zfill(4) + ".fits")
        data4 = hdu4[0].data
        points4 = np.asarray(np.where(data4!=0))
    except:
        ax.scatter(points3[1,:], points3[0,:],marker='o',c=c[4], s=1)
        ax.scatter(points2[1,:], points2[0,:],marker='o',c=c[6], s=1)
        ax.scatter(points1[1,:], points1[0,:],marker='o',c=c[12], s=1)
        plt.grid()
        plt.title(str(UTCTime) + " TimeStep " + str(i+1) + "/150")
        plt.savefig("Timelapse" + str(i).zfill(4) + ".png",facecolor=c[2])
        continue

    ax.scatter(points4[1,:], points4[0,:],marker='o',c=c[2], s=1)
    ax.scatter(points3[1,:], points3[0,:],marker='o',c=c[4], s=1)
    ax.scatter(points2[1,:], points2[0,:],marker='o',c=c[6], s=1)
    ax.scatter(points1[1,:], points1[0,:],marker='o',c=c[12], s=1)
    plt.grid()
    plt.title(str(UTCTime) + " TimeStep " + str(i+1) + "/150")
    plt.savefig("Timelapse" + str(i).zfill(4) + ".png",facecolor=c[2])



