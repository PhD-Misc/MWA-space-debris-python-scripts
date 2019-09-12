import sys
sys.path.append("/home/steve/Downloads/analysis_scripts")
import analysisUtils as au
import numpy as np
import random
from datetime import datetime
random.seed(datetime.now())


baselines = np.asarray(au.getBaselineLengths('0200.ms',sort=True))
currentBaselines = []

for b in baselines:
    if float(b[1])> 200 and float(b[1]) <= 400:
        currentBaselines.append(np.asarray(b))


num2flag=len(currentBaselines)-100
currentBaselines = np.asarray(currentBaselines)
selectedBaseline = np.random.choice(currentBaselines[:,0],size=100,replace=False)


config=""
for i in range(len(selectedBaseline)):
    a,b = selectedBaseline[i].split("-")
    config = str(config) + str(a) + "&" + str(b)
    if i < (len(selectedBaseline)-1):
        config = config + ";"
split(vis='1244056224.ms/',outputvis='test.ms',antenna=config)








