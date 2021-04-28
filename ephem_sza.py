# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:21:20 2019

@author: smrak@bu.edu
"""
import ephem
import numpy as np
from datetime import datetime
import concurrent.futures
import matplotlib.pyplot as plt

def get_sza(glon, glat):
    global t, horizon
    obs = ephem.Observer()
    obs.lat = np.deg2rad(glat)
    obs.lon = np.deg2rad(glon)
    obs.date = ephem.Date(t)
    
    sun = ephem.Sun()
    sun.compute(obs)
#    sun_azm = np.degrees(sun.ra)
    sza = 90 - np.degrees(sun.alt) + horizon
    
    return sza

glon, glat = np.meshgrid(np.arange(-180,181,2), np.arange(-90,91,1))
galt = 0
re = 6371
horizon = -np.degrees(np.arccos(re/(re + galt)))
t = datetime(2017,9,7,23,30)

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
    sza_worker = np.asarray([ex.submit(get_sza, glon.ravel()[i], glat.ravel()[i]) for i in range(glon.size)])

sza = np.nan*np.ones(glon.ravel().size)
for i in range(sza_worker.size):
    sza[i] = sza_worker[i].result()
sza = sza.reshape(glon.shape)

night_ravel = (sza.ravel() >= 90)
night = night_ravel.reshape(glon.shape)
sza_day = sza
sza_day[night] = np.nan

terminator = (sza > 90-.2) & (sza < 90+.2)
terminator_mask = np.zeros(glon.shape)
terminator_mask[terminator] = 1
plt.figure()
plt.pcolormesh(glon, glat, sza_day)
plt.pcolormesh(glon, glat, terminator_mask)

#sun = ephem.Sun()
#obs = ephem.Observer()
#obs.lat = np.deg2rad(glat)
#obs.lon = np.deg2rad(glon)
#obs.date = ephem.Date(t)
#sun.compute(obs)
#sr = sun.radius
#sun_azm = np.degrees(sun.ra)
#sun_elv = np.degrees(sun.alt) - horizon
#
#print (sun_azm, sun_elv)