#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:46:10 2018

@author: Sebastijan Mrak <smrak@bu.edu>
"""

from numpy import cos, deg2rad, arccos, rad2deg
import ephem
import datetime

def getsunriseTimeUTC(lat=40,lon=-100, alt=0, date=0,pressure=0,horizon=0):
    loc = ephem.Observer()
    loc.lon = str(lon)
    loc.lat = str(lat)
    loc.pressure = pressure
    loc.horizon = str(horizon)

    if date == 0:
        date=datetime.datetime.now()
    if isinstance(date, datetime.datetime):
        loc.date = date.strftime('%Y/%m/%d')
    else:
        print ('Argument date musti be dateimte.datetime object')
    loc.date = '2017/08/21'
    sunrise1 = loc.previous_rising(ephem.Sun()).datetime()
    sunrise2 = loc.next_rising(ephem.Sun()).datetime()
    d1 = sunrise1.strftime('%d')
    d2 = sunrise2.strftime('%d')
    d = date.strftime('%d')
    if d == d1:
        sunrise = sunrise1
    else:
        sunrise = sunrise2

    # Geometry: Spherical Earth approximation
    Re = 6378.0 # km
    h = alt # km
    theta = rad2deg(arccos(Re/(Re+h)))
    # Earth rotation 15deg per hour
    dt = (theta / 15.0) * 60 * 60 / cos(deg2rad(lat))
    sunrise_alt = sunrise - datetime.timedelta(seconds=dt)
    return sunrise_alt

if __name__ == '__main__':
    print (getsunriseTimeUTC(date=datetime.datetime(2017,8,21,0,0,0), alt=100))