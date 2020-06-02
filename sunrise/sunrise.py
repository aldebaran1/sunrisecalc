#!/usr/bin/env python
"""
PyEphem does not take altitude of observer into account for sunrise/sunset, and doesn't plan to:
https://github.com/brandon-rhodes/pyephem/issues/102#issuecomment-225047734

This spherical earth computation works around that issue.
For more accuracy consider astropy.get_sun

python sunrise.py 40 -100 100.

@author: Sebastijan Mrak <smrak@bu.edu>
"""

from math import cos, radians, acos, degrees
import ephem
import datetime
from dateutil.parser import parse

def getsunriseTimeUTC(lat=40, lon=-80, alt=0, 
                      date=None, verbose = False,
                      pressure=None, horizon=None):
    """
    By default horizon == 0, namely we compute a sunrise time NOT dawn.
    'alt' argument must be set in kilometers.
    'pressure' argument is in milibars [mBar]
    """
    L = ephem.Observer()
    L.lon = str(lon)
    L.lat = str(lat)
    if pressure is not None: L.pressure = pressure
    if horizon is not None: L.horizon = str(horizon)

    if date is None:
        date = datetime.date.today()
    elif isinstance(date, str):
        date = parse(date)
    elif isinstance(date,datetime.datetime):
        pass
    else:
        raise TypeError('time must be datetime object')

    L.date = date.strftime('%Y/%m/%d')
# %% compute
    sunrise1 = L.previous_rising(ephem.Sun()).datetime()
    sunrise2 = L.next_rising(ephem.Sun()).datetime()

    d1 = sunrise1.isoformat()
#    d2 = sunrise2.strftime('%d')
    d = date.isoformat()
    if d == d1:
        sunrise = sunrise1
    else:
        sunrise = sunrise2
    if verbose:
        print('Sunrise time at ground level UTC:', sunrise.isoformat()[:-7])
# %% Geometry: Spherical Earth approximation
# CAUTION: This is a sloppy approximantion. It assumes geoid=sphere and rotation
# of the Earth = 15deg/hour
    Re = 6378.0 # km
    h = alt # km
    theta = degrees(acos(Re/(Re+h)))
# %% Earth rotation 15 deg/hour
    dt = (theta / 15.0) * 60 * 60 / cos(radians(lat))

    tsunrise = sunrise - datetime.timedelta(seconds=dt)

    return tsunrise


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('lat',type=float)
    p.add_argument('lon',type=float)
    p.add_argument('alt_km',help=' altitude (km)',type=float)
    p.add_argument('date', nargs='?')
    p.add_argument('-p', '--pressure')
    p.add_argument('--horizon')
    p = p.parse_args()

    tsr = getsunriseTimeUTC(p.lat, p.lon, p.alt_km, p.date, p.pressure, p.horizon)

    print('Sunrise at', p.alt_km,'km altitude UTC:',tsr.isoformat()[:-7])