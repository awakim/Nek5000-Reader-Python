#=============================================================================#                                                               #
#                                                                             #
# Authors: WAKIM ARNOLD                                                       #
# Contact: arnold.wakim(at)gmail.com(at)                                      #
#=============================================================================#


import numpy as np
import matplotlib.pyplot as plt
import time

def readheader(fname):
    try:
        infile = open(fname, 'rb')
    except IOError as e:
        print('I/O error ({0}): {1}'.format(e.errno, e.strerror))
        return -1
    header=infile.read(132).split()
    infile.close()
    return header



def readelmap(fname,header):
    """ Reads element map for Nek5000 binary files *0.f* """
    nelf=int(header[6])   # number of elements in the file

    try:
        infile = open(fname, 'rb')
    except IOError as e:
        print('I/O error ({0}): {1}'.format(e.errno, e.strerror))
        return -1
    #locating element map of the field
    headersize=132
    endiansize=4
    infile.seek(headersize+endiansize) # go to first bit of element map
    #READ ELEMENT MAP IN FILE USING BINARY READER NP.FROMFILE
    elmap=list(np.fromfile(infile,count=nelf,dtype=np.int32)) # read element map as list of np.int32 integers

    infile.close()
    return elmap


def readgeo(fname,header,elmap):
    """ Reads geomtry mesh for Nek5000 binary files *0.f*    """
    nelf=len(elmap) # number of elements to read where elmap is the list of elems to read

    # FIND IF MESH IS PRESENT IN THE FILE#######################################
    variables = header[11].decode('utf-8')
    thereisgeo = False
    for v in variables:
        if (v == 'X'):
			thereisgeo = True
    ############################################################################

    if (thereisgeo):

        try:
            infile = open(fname, 'rb')
        except IOError as e:
            print('I/O error ({0}): {1}'.format(e.errno, e.strerror))
            return -1

        #INITIALIZE GEOMETRY AS LIST OF NUMPY ARRAYS
        lr1 = [int(header[2]),int(header[3]),int(header[4])]
        ndim = 2 + (lr1[2]>1)
        geo=[np.zeros( (ndim, lr1[2], lr1[1], lr1[0]) ) for i in range(nelf)]

        #locating GEOMETRY field
        headersize=132
        endiansize=4
        elmapsize=nelf*4
        initgeo=headersize+endiansize+elmapsize
        infile.seek(initgeo) #go to first bit of geometry field

        #READ GEOMETRY USING BINARY READER NP.FROMFILE
        dtgeo= np.dtype([('xyz', np.float32,   (ndim,lr1[2], lr1[1], lr1[0]) )]) # INITIALIZE DATA TYPE
        for iel in elmap:
            fi=np.fromfile(infile,count=1,dtype=dtgeo)
            for dim in range(ndim):
                 geo[iel-1][dim]=fi[0][0][dim]
        infile.close()
        return geo
    else:
        print("### You cannot read geometry ###")
        print("### Mesh is not available in this file ###")
        return -1


def readvel(fname,header,elmap):
    """ Reads velocity field for Nek5000 binary files *0.f*    """
    nelf=len(elmap) # number of elements to read where elmap is the list of elems to read

    # FIND IF VELOCITY IS PRESENT IN THE FILE###################################
    variables = header[11].decode('utf-8')
    thereisvel = False
    for v in variables:
        if (v == 'U'):
			thereisvel = True
    ############################################################################

    if (thereisvel):

        try:
    		infile = open(fname, 'rb')
    	except IOError as e:
    		print('I/O error ({0}): {1}'.format(e.errno, e.strerror))
    		return -1

        #INITIALIZE GEOMETRY AS LIST OF NUMPY ARRAYS
        lr1 = [int(header[2]),int(header[3]),int(header[4])]
        ndim = 2 + (lr1[2]>1)
        vel=[np.zeros( (ndim, lr1[2], lr1[1], lr1[0]) ) for i in range(nelf)]

        #locating GEOMETRY field
        headersize=132
        endiansize=4
        elmapsize=nelf*4
        npel=lr1[0]*lr1[1]*lr1[2]
        wdsz = int(header[1])
        geosize=max(elmap)*ndim*npel*wdsz
        initvel=headersize+endiansize+elmapsize+geosize  #go to first bit of velocity field
        infile.seek(initvel) #go to first bit of geometry field

        #READ GEOMETRY USING BINARY READER NP.FROMFILE
        dtvel= np.dtype([('xyz', np.float32,   (ndim,lr1[2], lr1[1], lr1[0]) )]) # INITIALIZE DATA TYPE FOR NP.FROMFILE
        for iel in elmap:
            fi=np.fromfile(infile,count=1,dtype=dtvel)
            for dim in range(ndim):
                 vel[iel-1][dim]=fi[0][0][dim]
        infile.close()
        return vel
    else:
        print("### You cannot read velocity ###")
        print("### velocity is not available in this file ###")
        return -1


def readpres(fname,header,elmap):
    """ Reads pressure field for Nek5000 binary files *0.f*    """
    nelf=len(elmap) # number of elements to read where elmap is the list of elems to read

    # FIND IF PRESSURE IS PRESENT IN THE FILE###################################
    variables = header[11].decode('utf-8')
    thereisvel = False
    for v in variables:
        if (v == 'P'):
			thereispres = True
    ############################################################################

    if (thereispres):

        try:
    		infile = open(fname, 'rb')
    	except IOError as e:
    		print('I/O error ({0}): {1}'.format(e.errno, e.strerror))
    		return -1

        #INITIALIZE GEOMETRY AS LIST OF NUMPY ARRAYS
        lr1 = [int(header[2]),int(header[3]),int(header[4])]
        ndim = 2 + (lr1[2]>1)
        pres=[np.zeros( (ndim, lr1[2], lr1[1], lr1[0]) ) for i in range(nelf)]

        #locating GEOMETRY field
        headersize=132
        endiansize=4
        elmapsize=nelf*4
        npel=lr1[0]*lr1[1]*lr1[2]
        wdsz = int(header[1])
        geosize=max(elmap)*ndim*npel*wdsz
        velsize=max(elmap)*ndim*npel*wdsz
        initpres=headersize+endiansize+elmapsize+geosize+velsize  #go to first bit of velocity field
        infile.seek(initpres) #go to first bit of geometry field

        #READ GEOMETRY USING BINARY READER NP.FROMFILE
        dtpres= np.dtype([('xyz', np.float32,   (1,lr1[2], lr1[1], lr1[0]) )]) # INITIALIZE DATA TYPE FOR NP.FROMFILE
        for iel in elmap:
            fi=np.fromfile(infile,count=1,dtype=dtpres)
            for dim in range(ndim):
                 pres[iel-1][0]=fi[0][0]
        infile.close()
        return pres
    else:
        print("### You cannot read pressure ###")
        print("### pressure is not available in this file ###")
        return -1


    return pres

def gather
