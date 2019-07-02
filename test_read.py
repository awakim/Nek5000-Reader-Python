import nekreader as nr
import time as time

fname='basvortex0.f00001'
ts= time.time()
header=nr.readheader(fname)
elmap=nr.readelmap(fname,header)
geo=nr.readgeo(fname,header,elmap)
vel=nr.readvel(fname,header,elmap)
pres=nr.readpres(fname,header,elmap)
te= time.time()
print "time elapsed for full file :: ", te-ts
