# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jeffrey"
__date__ ="$Oct 28, 2009 5:52:06 PM$"

import datetime
from time import strptime

import pytz

import app
from entity import *

def parse_coord(value):
#    return [int(s) for s in value.split(':')]
    v = value.split(':')
    return Coord(v[0], v[1], v[2])

def format_coord(coord):
    return ':'.join([str(c) for c in coord])

def parse_decimal(decimal):
    return int(decimal.replace('.', ''))

def parse_time(time_str):
    """
    >>> parse_time('11.12.2009 11:45:02')
    datetime.datetime(2009, 12, 11, 11, 45, 2)
    """
    return datetime.datetime(*strptime(time_str,"%d.%m.%Y %H:%M:%S")[0:6])

def get_servertime_now():
    s = '%Y-%m-%d %H:%M:%S'
    local_tz = pytz.timezone(app.config['timezone'])
    local_now = local_tz.localize(datetime.datetime.now())
    server_tz = pytz.timezone(pytz.country_timezones['de'][0])
    dt = local_now.astimezone(server_tz)
    return datetime.datetime.strptime(dt.strftime(s), s)

def parse_coords_exp(exp):
    """
    >>> parse_coords_exp('2:309:6,1:308:3')
    [[2:309:6], [1:308:3]]
    >>> parse_coords_exp('2:200,3:400,5:500')
    [[2:200:0], [3:400:0], [5:500:0]]
    >>> parse_coords_exp('2:1-10')
    [[2:1:0], [2:2:0], [2:3:0], [2:4:0], [2:5:0], [2:6:0], [2:7:0], [2:8:0], [2:9:0], [2:10:0]]
    >>> parse_coords_exp('2:1-3,3:4-6')
    [[2:1:0], [2:2:0], [2:3:0], [3:4:0], [3:5:0], [3:6:0]]
    >>> parse_coords_exp('2:1-2,5:400,6:321-322')
    [[2:1:0], [2:2:0], [5:400:0], [6:321:0], [6:322:0]]
    """
    coords = []
    exp_list = exp.split(',')
    for e in exp_list:
        if '-' in e:
            m = re.compile(r'([1-9]):(\d+)-(\d+)').search(e)
            (g, r1, r2) = m.groups()
            for i in range(int(r1), int(r2)+1):
                coords.append(Coord(int(g), int(i), 0))
        else:
            coords.append(Coord(e))
    return coords

if __name__ == '__main__':

    import doctest
    doctest.testmod()