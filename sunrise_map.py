# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 10:33:38 2019

@author: smrak@bu.edu
"""

import numpy as np
from sunrise import terminator as ter
from datetime import datetime
import matplotlib.pyplot as plt
from skimage import measure
from cartomap import geogmap as gm

def get_terminator(time, alt_km=0,
                   glon=None, glat=None,
                   return_sza=False):
    
    if glon is None and glat is None:
        glon, glat = np.meshgrid(np.arange(-180,180,1), np.arange(-90,91,.2))
    
    if time is None:
        time = datetime.now()
    else:
        assert isinstance(time, datetime)

    sza_2d = ter.get_sza(time, glon, glat, alt_km=alt_km) - 90
    terminator = np.squeeze(np.array(measure.find_contours(sza_2d, 0)))
    if len(terminator.shape) == 2:
        x = terminator[:,1] - 180
        y = terminator[:,0] - 90
    
    elif (len(terminator.shape) == 1) and (terminator.shape[0] > 1): 
        x = []
        y = []
        for i, t in enumerate(terminator):
            x.append(t[:,1] - 180)
            y.append(t[:,0] - 90)
    
    if return_sza:
        return sza_2d
    else:
        return x, y

date = datetime(2017,8,21,23)
alt_km = 0
glon, glat = np.meshgrid(np.arange(-180, 180.1, 1),
                         np.arange(-90, 90.1, 1))
sza = get_terminator(time=date, alt_km = alt_km, glon=glon, glat = glat, return_sza=True)
terminator = np.squeeze(np.array(measure.find_contours(sza, 0)))
x,y = get_terminator(time=date, alt_km = alt_km, glon=glon, glat = glat)
if isinstance(x, list):
    plt.figure()
    im = plt.pcolormesh(glon, glat, sza, cmap='bwr', vmin=-80, vmax=80)
    for i in range(len(x)):
        plt.plot(x[i], y[i], '--g', lw=4)
    plt.colorbar(im)
else:
    plt.figure()
    im = plt.pcolormesh(glon, glat, sza, cmap='bwr', vmin=-80, vmax=80)
    plt.plot(x, y, '--g', lw=4)
    plt.colorbar(im)
    
fig, ax = gm.plotCartoMap(projection='plate',lon0=-50,
                          title="{}, Terminators H=[0,150] km".format(date),
                          lonlim=[-140,0], latlim=[-90,90],
                          meridians = np.arange(-180,180.1,40),
                          parallels = np.arange(-80,80.1,20),
                          date=date,
                          terminator=True, terminator_altkm=[0,150])
