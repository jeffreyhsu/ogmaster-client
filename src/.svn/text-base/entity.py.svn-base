# -*- coding: utf-8 -*-

__author__="jeffrey"
__date__ ="$Mar 9, 2009 9:49:17 PM$"

import re
import datetime

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.orm.properties import CompositeProperty
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

from common import *
from utils import *

#s = 'postgres://postgres:lefx8233@127.0.0.1:5432/ogame'
engine = create_engine('%s://%s:%s@%s/%s?charset=utf8' % ('mysql', 'root', '', 'localhost', 'ogame'), echo=False)

db = scoped_session(sessionmaker(autoflush=True, bind=engine))

class Model(object):

    def __init__(self, **kw):
        for k, v in kw.iteritems():
            setattr(self, k, v)

    def __repr__(self):
        attrs = []
        for key in self.__dict__:
            if not key.startswith('_'):
                attrs.append((key, getattr(self, key)))
        return self.__class__.__name__ + '(' + ', '.join(x[0] + '=' +
                                            repr(x[1]) for x in attrs) + ')'

    def __copy__(self, d):
        for k in d:
            setattr(self, k, d[k])

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def format(self, dt):
        return format(dt)

Base = declarative_base(bind=engine, cls=Model)
metadata = Base.metadata

class Alliance(Base):
    __tablename__ = 'alliance'

    ogameid = Column(Integer, autoincrement=False, primary_key=True)
    name = Column(Unicode(20))
    fullname = Column(Unicode(100))
    _prev_names = Column(Unicode(200), default='[]')
    
    def _get_prev_names(self):
        return eval(self._prev_names)

    def _set_prev_names(self, value):
        self._prev_names = repr(value)

    prev_names = synonym('_prev_names', descriptor=property(_get_prev_names,
                                                        _set_prev_names))
    rank = Column(Integer)

    updated = Column(DateTime)

class Player(Base):
    __tablename__ = 'player'

    ogameid = Column(Integer, autoincrement=False, primary_key=True)
    name = Column(Unicode(20))
    
    rank = Column(Integer)
    points = Column(Integer)

    _prev_names = Column(Unicode(200), default='[]')

    alliance_id = Column(Integer, ForeignKey('alliance.ogameid'))

    alliance = relation(Alliance, backref=backref('players', lazy='dynamic'))

    _status = Column(String(20))

    def _get_status(self):
        return eval(self._status)

    def _set_status(self, status):
        self._status = repr(status)

    status = synonym('_status', descriptor=property(_get_status,
                                                        _set_status))

    def _get_prev_names(self):
        return eval(self._prev_names)

    def _set_prev_names(self, value):
        self._prev_names = repr(value)

    prev_names = synonym('_prev_names', descriptor=property(_get_prev_names,
                                                        _set_prev_names))

    def can_attack(self):
        return not bool(set(['v', 'n', 's']) & self.status)

    def is_normal(self):
        return not bool(self.status)
    def is_inactive(self):
        return 'i' in self.status or 'I' in self.status
    def is_noob(self):
        return 'n' in self.status
    def is_strong(self):
        return 's' in self.status
    def is_banned(self):
        return 'b' in self.status

    updated = Column(DateTime)

class PlayerRecord(Base):
    __tablename__ = 'stat_player'

    id = Column(Integer, autoincrement=True, primary_key=True)
    player_name = Column(Unicode(50))
    ogameid = Column(Integer)
    rank = Column(Integer)
    points = Column(Integer)
    fleet_rank = Column(Integer)
    fleet_points = Column(Integer)
    research_rank = Column(Integer)
    research_points = Column(Integer)
    ally = Column(Unicode(50))

    updated = Column(DateTime)

class AllianceRecord(Base):
    __tablename__ = 'stat_alliance'

    id = Column(Integer, autoincrement=True, primary_key=True)
    alliance_id = Column(Integer, ForeignKey('alliance.ogameid'))
    rank = Column(Integer)
    points = Column(Integer)

    updated = Column(DateTime)

class Planet(Base):
    __tablename__ = 'planet'

    id = Column(Integer, autoincrement=True, primary_key=True)

    name = Column(Unicode(20))
    _prev_names = Column(String(200), default='[]')

    galaxy = Column(Integer)
    system = Column(Integer)
    position = Column(Integer)

    _coord = Column(String(20))

    def _get_coord(self):
        return Coord(self.galaxy, self.system, self.position)

    def _set_coord(self, value):
        self.galaxy = value.galaxy
        self.system = value.system
        self.position = value.position
        self._coord = value.to_string()

    coord = synonym('_coords', descriptor=property(_get_coord, _set_coord))

    has_moon = Column(Boolean, default=False)
    debris_amount = Column(Integer)
    debris_metal = Column(Integer)
    debris_crystal = Column(Integer)
    
    _player_status = Column(String(20))

    status = Column(String(20))

    player_name = Column(Unicode(20))
    player_id = Column(Integer, ForeignKey('player.ogameid'))

    def _get_prev_names(self):
        return eval(self._prev_names)

    def _set_prev_names(self, value):
        self._prev_names = repr(value)

    prev_names = synonym('_prev_names', descriptor=property(_get_prev_names,
                                                        _set_prev_names))

    def _get_player_status(self):
        return eval(self._status)

    def _set_player_status(self, status):
        self._status = repr(status)

    player_status = synonym('_player_status', descriptor=property(_get_player_status, _set_player_status))

    updated = Column(DateTime)

    player = relation(Player, backref=backref('planets', lazy='dynamic'))

    def can_attack(self):
        status = self.player_status
        s = set(['v', 'n', 's'])
        return not bool(s & status)

class OgameEvent(Base):
    __tablename__ = 'ogame_event'

    id = Column(Integer, autoincrement=True, primary_key=True)

    type = Column(String(20))
    data = Column(String(20))

    owner_planet_id = Column(String(36), ForeignKey('planet.id'))
    owner_id = Column(Integer, ForeignKey('player.ogameid'))

    target_planet_id = Column(String(36), ForeignKey('planet.id'))
    target_id = Column(Integer, ForeignKey('player.ogameid'))

    online_index = Column(Integer, default=1)

    owner_planet = relation(Planet, primaryjoin=owner_planet_id==Planet.id, backref=backref('events', lazy='dynamic'))
    owner = relation(Player, primaryjoin=owner_id==Player.ogameid, backref=backref('events', lazy='dynamic'))

    target_planet = relation(Planet, primaryjoin=target_planet_id==Planet.id, backref=backref('target_events', lazy='dynamic'))
    target = relation(Player, primaryjoin=target_id==Player.ogameid, backref=backref('target_events', lazy='dynamic'))

    updated = Column(DateTime)

class Coord(object):
    """Coordinate object

    >>> Coord('2:382:9')
    [2:382:9]
    >>> Coord('2:382')
    [2:382:0]
    >>> c = Coord(4,109,6)
    >>> c
    [4:109:6]
    >>> c.tuple()
    (4, 109, 6)
    >>> c.type
    1
    >>> c1 = Coord(2,169,5)
    >>> c2 = Coord(2,169,10)
    >>> c1.distance_to(c2)
    1025
    """

    class Types(Enum):
        unknown = 0
        planet  = 1
        debris  = 2
        moon = 3

    PLANETS_PER_SYSTEM = 15
    REGEXP_coord    = re.compile(r"([0-9]{1,3}):([0-9]{1,3}):?([0-9]{1,2})?")

    def __init__(self, galaxy, system=0, position=0, type=Types.planet):
        '''
            First parameter can be a string to be parsed e.g: [1:259:12] or the galaxy.
            If it's the galaxy, system and planet must also be supplied.
        '''
        self.type = type
        try: self.parse(galaxy)
        except Exception:
            self.galaxy = galaxy
            self.system = system
            self.position = position
            self.convert_to_ints()

    def is_moon(self):
        return self.type == self.Types.moon

    def parse(self, newcoord):
        match = self.REGEXP_coord.search(newcoord)
        if not match:
            raise Exception("Error parsing coord: " + newcoord)
        self.galaxy, self.system, self.position = match.groups()
        self.position = self.position if self.position else 0
        if 'moon' in newcoord: self.type = self.Types.moon
        self.convert_to_ints()

    def tuple(self):
        return self.galaxy, self.system, self.position

    def convert_to_ints(self):
        self.galaxy, self.system, self.position = int(self.galaxy), int(self.system), int(self.position)

    def __repr__(self):
        repr = "[%s:%s:%s]" % (self.galaxy, self.system, self.position)
        if not self.type == self.Types.planet:
            repr += " " + self.Types.toStr(self.type)
        return  repr

    def __eq__(self, othercoord):
        return self.tuple() == othercoord.tuple() and self.type == othercoord.type

    def __ne__(self, othercoord):
        return not self.__eq__(othercoord)

    def __lt__(self,othercoord):
        if self.galaxy < othercoord.galaxy:
            return True
        elif self.galaxy == othercoord.galaxy:
            if self.system < othercoord.system:
                return True
            elif self.system == othercoord.system:
                if self.position < othercoord.position:
                    return True
        return False

    def to_string(self):
        return "%s:%s:%s" % (self.galaxy, self.system, self.position)

    def distance_to(self, coord):

        distance = 0
        if   coord.galaxy - self.galaxy != 0:
            distance = abs(coord.galaxy - self.galaxy) * 20000
        elif coord.system - self.system != 0:
            distance = abs(coord.system - self.system) * 5 * 19 + 2700
        elif coord.position - self.position != 0:
            distance = abs(coord.position - self.position) * 5 + 1000
        else:
            distance = 5
        return distance

    def flightTimeTo(self, coord, speed, speedPercentage=100):
        seconds = 350000.0/speedPercentage * math.sqrt(self.distanceTo(coord) * 10.0 / float(speed)) + 10.0
        return datetime.timedelta(seconds=int(seconds))

class BasePlanet(object):
    def __init__(self, coord, name=""):
        self.coord = coord
        self.name = name
        
    def __repr__(self):
        return 'Planet[%s]' % (self.name + "," + str(self.coord))


class OwnPlanet(BasePlanet):
    """
    >>> p = OwnPlanet(Coord('2:291:4'), 'MJ_II', '1234567')
    >>> p
    Planet[MJ_II,[2:291:4]]
    """
    def __init__(self, coord, name="", code=0):
        super(OwnPlanet, self).__init__(coord, name)
        self.code = code

class Message(object):

    def __init__(self, type, subject, servertime, content, ogameid=None, sender='system'):
        self.type = type
        self.subject = subject
        self.servertime = servertime
        self.content = content
        self.sender = sender
        self.ogameid = ogameid

    def __repr__(self):
        return 'Msg[%s,%s,%s]' % (self.type, self.sender, self.subject)

if __name__ == "__main__":
    import doctest
    doctest.testmod()