from astropy.io import fits
import numpy as np
import os.path
from argparse import ArgumentParser
import sys
sys.path.append("/home/steve/Downloads/analysis_scripts")
import analysisUtils as au

baselines = np.asarray(au.getBaselineLengths('1244056224.ms/',sort=True))
currentBaselines=[]
for b in baselines:
    if float(b[1])> 0 and float(b[1]) <= 500:
        currentBaselines.append(np.asarray(b))
    
print(len(currentBaselines))
hdu = fits.open('1244056224.metafits')
position = []
for b in currentBaselines:
    tile1, tile2 = b[0].split('-')
    tile1Index = np.where(hdu[1].data['TileName']==tile1)
    tile1pos = hdu[1].data['North'][tile1Index[0][0]]
    tile2Index = np.where(hdu[1].data['TileName']==tile2)
    tile2pos = hdu[1].data['North'][tile2Index[0][0]]
    centerPoint = (float(tile1pos) + float(tile2pos)) /2.0
    position.append(centerPoint)

maxposition = np.asarray(position)
eastArray = []
westArray = []

maxArrayIndex = []
for i in range(250):
    index = np.where(maxposition == max(maxposition))
    maxArrayIndex.append(int(index[0]))
    maxposition[index] = -1000
    eastArray.append(currentBaselines[int(index[0])])


positionE = []
positionN = []
for b in eastArray:
    tile1,tile2 = b[0].split("-")
    tile1Index = np.where(hdu[1].data['TileName']==tile1)
    tile1posE = hdu[1].data['East'][tile1Index[0][0]]
    tile1posN = hdu[1].data['North'][tile1Index[0][0]]
    tile2Index = np.where(hdu[1].data['TileName']==tile2)
    tile2posE = hdu[1].data['East'][tile2Index[0][0]]
    tile2posN = hdu[1].data['North'][tile2Index[0][0]]
    centerPointE = (float(tile1posE) + float(tile2posE)) /2.0
    centerPointN = (float(tile1posN) + float(tile2posN)) /2.0
    positionE.append(centerPointE)
    positionN.append(centerPointN)
E = np.mean(positionE)
N = np.mean(positionN)
print("center of north array E " + str(E) + " and N " + str(N))



minposition = np.asarray(position)
minArrayIndex = []
for i in range(250):
    index = np.where(minposition == min(minposition))
    minArrayIndex.append(int(index[0]))
    minposition[index] = 1000
    westArray.append(currentBaselines[int(index[0])])


positionE = []
positionN = []
for b in westArray:
    tile1,tile2 = b[0].split("-")
    tile1Index = np.where(hdu[1].data['TileName']==tile1)
    tile1posE = hdu[1].data['East'][tile1Index[0][0]]
    tile1posN = hdu[1].data['North'][tile1Index[0][0]]
    tile2Index = np.where(hdu[1].data['TileName']==tile2)
    tile2posE = hdu[1].data['East'][tile2Index[0][0]]
    tile2posN = hdu[1].data['North'][tile2Index[0][0]]
    centerPointE = (float(tile1posE) + float(tile2posE)) /2.0
    centerPointN = (float(tile1posN) + float(tile2posN)) /2.0
    positionE.append(centerPointE)
    positionN.append(centerPointN)
E = np.mean(positionE)
N = np.mean(positionN)
print("center of south array E " + str(E) + " and N " + str(N))




eastconfig = ""
westconfig = ""
counter = 0
for b in westArray:
    currentBaseline = b[0]
    tile1, tile2 = currentBaseline.split("-")
    westconfig = str(westconfig) + str(tile1) + "&" + str(tile2)
    if counter < 249:
        westconfig = westconfig + ";"
    counter += 1

counter = 0
for b in eastArray:
    currentBaseline = b[0]
    tile1, tile2 = currentBaseline.split("-")
    eastconfig = str(eastconfig) + str(tile1) + "&" + str(tile2)
    if counter < 249:
        eastconfig = eastconfig + ";"
    counter += 1






split(vis='1244056224.ms/',datacolumn='corrected',outputvis='eastArray.ms',antenna=eastconfig)
split(vis='1244056224.ms/',datacolumn='corrected',outputvis='westArray.ms',antenna=westconfig)








