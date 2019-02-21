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
from astropy.nddata import Cutout2D
import math
import matplotlib.patches as patches


#The below section is the TLE date of the satellite
line1 = "ISS"
line2 = "1 25544U 98067A   16078.18872957  .00011987  00000-0  18767-3 0  9997"
line3 = "2 25544  51.6438 151.8661 0001598 315.1341 138.1171 15.54181702990822"
sat = ephem.readtle(line1, line2, line3)

#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level


head_rms_array = [None]*99
tail_rms_array = [None]*99
rms_rms_array = [None]*99
snr_array = [None]*99

#The real game starts from here
for i in range(116):
    hud1 = fits.open('test-t00' + str(i).zfill(2) + "-image.fits")
    hud2 = fits.open('test-t00' + str(i+1).zfill(2) + "-image.fits")

    header1 = hud1[0].header
    header2 = hud2[0].header

    wcs1 = WCS(header1, naxis=2)
    wcs2 = WCS(header2, naxis=2)

    UTCTime1 = datetime.strptime(header1['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=-0.5)
    UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=0)


    #The below section calculates the position of the satellite in the bottom image in the coordinate system of the top image
    mwa.date = UTCTime1
    sat.compute(mwa)
    xy1 = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    x1 = int(np.floor(xy1[0]))
    y1 = int(np.floor(xy1[1]))
    

    #The below section calculates the position of the satellite in the top image in the coordinate system of the top image
    mwa.date = UTCTime2
    sat.compute(mwa)
    xy2 = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    x2 = int(np.floor(xy2[0]))
    y2 = int(np.floor(xy2[1]))


    #The below section calculates the diff image 2D array
    data1 = np.array(hud1[0].data[0,0,:,:])
    data2 = np.array(hud2[0].data[0,0,:,:])
    dataDiff = data2 - data1

    #The below code does the cutout of the section showing the strek. This will be centered at the pixel location of the satellite given by the top image
    position = (x2, y2)
    shape = (200, 200)

    cutout = Cutout2D(dataDiff, position, shape, wcs=wcs2)
    
    #The below code calculates the position of the satellite in the wcs of the cutout
    wcs_cutout = cutout.wcs
    #The sat position in top image in cutout
    mwa.date =  UTCTime2
    sat.compute(mwa)
    xy_cutout2 = wcs_cutout.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    x_cutout2 = int(np.floor(xy_cutout2[0]))
    y_cutout2 = int(np.floor(xy_cutout2[1]))

    #The sat position in bottom image in cutout
    mwa.date =  UTCTime1
    sat.compute(mwa)
    xy_cutout1 = wcs_cutout.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    x_cutout1 = int(np.floor(xy_cutout1[0]))
    y_cutout1 = int(np.floor(xy_cutout1[1]))

    #The below calculates the number of pixels between the head and the tail positions
    dist = int(np.floor(((x_cutout1-x_cutout2)**(2) + (y_cutout1-y_cutout2)**(2))**(0.5)))
    size_of_box = int(np.floor((0.3 * dist)))
    print("The size of the box is " + str(size_of_box))
    if size_of_box < 2:
        size_of_box = 2
    displacement = int(np.floor(size_of_box/2))


    #The below code isolates the head and the tail patches of the streak
    head = Cutout2D(cutout.data, (x_cutout2, y_cutout2), (size_of_box, size_of_box), wcs=cutout.wcs)
    tail = Cutout2D(cutout.data, (x_cutout1, y_cutout1), (size_of_box, size_of_box), wcs=cutout.wcs)
    head_rms = np.sum(head.data)
    tail_rms = np.sum(tail.data)
    print("The rms of head is " + str(head_rms) + " and the rms of the tail is "  + str(tail_rms) + " and the value of i is " + str(i) + " and the size of the box is " + str(size_of_box))
    head_mean = np.mean(head.data)
    tail_mean = np.mean(tail.data)
    print("The avg value of head is " + str(head_mean) + " and the avg value of tail is " + str(tail_mean))
    

    #The final ploting magic happens here
    ax = plt.subplot(2,3,1, projection = cutout.wcs)
    plt.imshow(cutout.data, cmap= plt.cm.viridis,  origin='lower')
    
    #plt.plot(x_cutout1,y_cutout1, 'o', mfc='none', color='white')
    #plt.plot(x_cutout2,y_cutout2, 'o', mfc='none', color='black')
    rect_head = patches.Rectangle((x_cutout2-displacement, y_cutout2-displacement), size_of_box, size_of_box, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect_head)
    rect_tail = patches.Rectangle((x_cutout1-displacement, y_cutout1-displacement), size_of_box, size_of_box, linewidth=1, edgecolor='blue', facecolor='none')
    ax.add_patch(rect_tail)
    #plt.xlabel('RA')
    #plt.ylabel('DEC')
    plt.grid(color='white', linestyle='-', linewidth='1')
    #plt.title(UTCTime2)
    #plt.colorbar()
    #plt.savefig('imageDiff' + str(str(i).zfill(3) + '.png'))



    #The below below section is for ploting rms value of head with time
    plt.subplot(2,3,4)
    #plt.axis([0, 98, 0, 3])
    #plt.plot(i, head_rms, '.', markerfacecolor='white', markeredgecolor='white')    
    head_rms_array[i]=head_rms
    i_array = np.linspace(0, 98, 99)
    plt.title("Head_rms")
    plt.plot(i_array, head_rms_array, 'r')



    #The below section if for plotting rms value of tail with time
    plt.subplot(2,3,5)
    #plt.axis([0, 98, 0, 3])
    tail_rms_array[i]=tail_rms
    i_array = np.linspace(0, 98, 99)
    plt.title("Tail_rms")
    plt.plot(i_array, tail_rms_array, 'blue')


    #The below section is for plotting the rms section of the diff images
    position_rms = (x2, y2)
    shape_rms = (800, 800)
    cutout_rms = Cutout2D(dataDiff, position_rms, shape_rms, wcs=wcs2)
    
    mwa.date = UTCTime2
    sat.compute(mwa)
    
    wcs_cutout_rms = cutout_rms.wcs
    xy_cutout_rms = wcs_cutout.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    x_cutout_rms = int(np.floor(xy_cutout_rms[0]))
    y_cutout_rms = int(np.floor(xy_cutout_rms[1]))


    mwa.date = UTCTime2 + timedelta(seconds=-20)
    sat.compute(mwa)
    
    wcs_cutout_rms = cutout_rms.wcs
    xy_cutout_rms_box = wcs_cutout.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    x_cutout_rms_box = int(np.floor(xy_cutout_rms_box[0]))
    y_cutout_rms_box = int(np.floor(xy_cutout_rms_box[1]))
    
    ax=plt.subplot(2,3,2, projection=wcs_cutout_rms)
    plt.imshow(cutout_rms.data, cmap= plt.cm.viridis, origin='lower')
    rect_rms = patches.Rectangle((x_cutout_rms_box+400, y_cutout_rms_box+400), 800, 800, linewidth=1, edgecolor='m', facecolor='none')
    ax.add_patch(rect_rms)
    #plt.plot(1500, 1500, 'o', markerfacecolor='none', markeredgecolor='black')
    plt.grid(color='white', linestyle='-', linewidth='1')
    
    
    cutout_rms_2 = Cutout2D(dataDiff, (x_cutout_rms_box, y_cutout_rms_box), (1000, 1000), wcs=wcs2)

    #The below section if for plotting the variation of rms with time
    #rms_rms = np.sqrt(np.mean(cutout_rms_2.data**2))
    rms_rms= np.sqrt(np.mean(dataDiff**2))
    rms_rms_array[i] = rms_rms
    
    plt.subplot(2,3,3)
    #plt.axis([0, 98, 0, 3])
    i_array = np.linspace(0, 98, 99)
    plt.title("Noise_rms")
    plt.plot(i_array, rms_rms_array, 'm')
    
    #The below section if for plotting the snr with time

    plt.subplot(2,3,6)
    #plt.axis([0, 98, 0, 10])
    plt.title("Head_rms*Tail_rms/Noise_rms")
    i_array = np.linspace(0, 98, 99)
    snr_array[i] = (head_rms-tail_rms)/rms_rms 
    #snr_array[i] = (head_rms + tail_rms)/rms_rms
    plt.plot(i_array, snr_array, 'black')
    #plt.show()
    plt.savefig('imageDiff' + str(str(i).zfill(3) + '.png'))


