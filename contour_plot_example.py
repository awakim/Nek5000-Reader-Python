import nekreader as nr
import time as time
import matplotlib.pyplot as plt
import numpy as np

fname='basvortex0.f00001' # Edit file name as wanted (I had a file named that way)
ts= time.time()
header=nr.readheader(fname)
elmap=nr.readelmap(fname,header)
geo=nr.readgeo(fname,header,elmap)
vel=nr.readvel(fname,header,elmap)
pres=nr.readpres(fname,header,elmap)
te= time.time()
print "time elapsed for full file :: ", te-ts



X=[]
Y=[]
Z=[]

for i in range(222):
    for j in range(111):
        for iy in range(6):
            X+=list(geo[i+222*j][0,0,iy,:])
            Y+=list(geo[i+222*j][1,0,iy,:])
            Z+=list(pres[i+222*j][0,0,iy,:])



v=np.linspace(-1.,1.,16)
plt.tricontourf(X,Y,Z,v,cmap=plt.cm.bwr,extend='both')
plt.show()
#do not mind the ugly plot as it is just an example of what can be done
