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
pre=nr.readpres(fname,header,elmap)
te= time.time()
print "time elapsed for full file :: ", te-ts



X=np.array([])
Y=np.array([])
Z=np.array([])

# for i in range(111):
#     for j in range(111):
#         for iy in range(6):
#             X+=list(geo[111+i+222*j][0,0,iy,:])
#             Y+=list(geo[111+i+222*j][1,0,iy,:])
#             Z+=list(pres[111+i+222*j][0,0,iy,:])

for i in range(60):
    for j in range(60):
        X=np.append(X,geo[111+i+222*j][0,0,:,:])
        Y=np.append(Y,geo[111+i+222*j][1,0,:,:])
        Z=np.append(Z,pre[111+i+222*j][0,0,:,:])

print X,len(X)

v=np.linspace(-1.,1.,16)
plt.tricontourf(X,Y,Z,v,cmap=plt.cm.bwr,extend='both')
plt.show()
#do not mind the ugly plot as it is just an example of what can be done
