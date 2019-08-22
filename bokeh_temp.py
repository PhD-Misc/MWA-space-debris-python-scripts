from bokeh.plotting import figure, show, output_file, ColumnDataSource
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from collections import Counter

hfont = {'fontname':'Helvetica', 'size':18}


altaz = np.zeros((900, 3600))
df = pd.read_csv('RFI.csv')
az = df['az']
alt = df['alt']
freq = df['freq']
temp = np.unique(freq)
print(temp)
c = Counter(freq)
plt.bar(c.keys(), c.values(), width=0.01)
plt.show()

#print(temp)
#for f in temp:
for i in range(len(az)):
    if math.isnan(alt[i]) or math.isnan(az[i]) or math.isnan(freq[i]):
        continue
    altaz[int(round(alt[i]*10.0)),int(round(az[i]*10.0))] = freq[i]
    altaz[int(round(alt[i]*10.0))+1,int(round(az[i]*10.0))] = freq[i]
    altaz[int(round(alt[i]*10.0)),int(round(az[i]*10.0))+1] = freq[i]
    altaz[int(round(alt[i]*10.0)),int(round(az[i]*10.0))-1] = freq[i]
    altaz[int(round(alt[i]*10.0))-1,int(round(az[i]*10.0))] = freq[i]
altaz = np.ma.masked_where(altaz==0, altaz)
cmap = plt.cm.Set3
cmap.set_bad(color='white')
plt.imshow(altaz, origin='lower', cmap=cmap,aspect='auto',interpolation='nearest',extent=[0,360,0,90], vmin=81, vmax=112)
plt.colorbar()
plt.xlabel("Azimuth (Degrees)",**hfont)
plt.ylabel("Elevation (Degrees)",**hfont)
plt.grid()
plt.vlines(185.4, colors='r', ymin=0, ymax=90)
plt.vlines(108.7, colors='m', ymin=0, ymax=90)
plt.vlines(250.5, colors='g', ymin=0, ymax=90)

plt.show()


#p = figure()
#p.image(image=[altaz], x=0, y=0,dw=3600, dh=900,palette="Spectral11")
#output_file("image.html", title="image.py example")
#show(p)  # open a browser


