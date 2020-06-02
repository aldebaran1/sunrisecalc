# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:21:20 2019

@author: smrak@bu.edu
"""
import ephem
import numpy as np
from datetime import datetime
import concurrent.futures
from skimage import measure

def get_sza(time, glon, glat, horizon=None, alt_km=None):
    if horizon is None:
        if alt_km is None:
            alt_km = 0
        re = 6371
        horizon = -np.degrees(np.arccos(re/(re + alt_km)))
    
    def _sza(x, y):
        
        obs = ephem.Observer()
        obs.lat = np.deg2rad(y)
        obs.lon = np.deg2rad(x)
        obs.date = ephem.Date(time)
        
        sun = ephem.Sun()
        sun.compute(obs)
        sza = 90 - np.degrees(sun.alt) + horizon
        return sza
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
        sza_worker = np.asarray([ex.submit(_sza, glon.ravel()[i], glat.ravel()[i]) for i in range(glon.size)])

    sza = np.nan*np.ones(glon.ravel().size)
    for i in range(sza_worker.size):
        sza[i] = sza_worker[i].result()
    sza = sza.reshape(glon.shape)
    
    return sza

def get_terminator(time, alt_km=0,
                   glon=None, glat=None,
                   return_sza=False):
    
    if glon is None and glat is None:
        glon, glat = np.meshgrid(np.arange(-180,180,1), np.arange(-90, 90.1, 1))
    
    if time is None:
        time = datetime.now()
    else:
        assert isinstance(time, datetime)

    sza_2d = get_sza(time, glon, glat, alt_km=alt_km) - 90
    terminator = np.squeeze(np.array(measure.find_contours(sza_2d, 0)))
    try:
        if len(terminator.shape) == 2:
            x = terminator[:,1] - 180
            y = terminator[:,0] - 90
        elif (len(terminator.shape) == 1) and (terminator.shape[0] > 1): 
            x = []
            y = []
            for i, t in enumerate(terminator):
                x.append(t[:,1] - 180)
                y.append(t[:,0] - 90)
    except:
        x = None
        y = None
    if return_sza:
        return sza_2d
    else:
        return x, y
