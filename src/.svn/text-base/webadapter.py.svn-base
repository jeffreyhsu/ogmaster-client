
__author__ = "jeffrey"
__date__ = "$Mar 13, 2009 8:52:56 PM$"

# python standard libs
import sys
import os
from Queue import *
import StringIO
import app
import cPickle
import cookielib
import copy
import httplib
import locale
import logging
import random
import re
import socket
import threading
import types
import urllib
import urllib2
from utils import *
import warnings

from BeautifulSoup import BeautifulSoup

import common
from entity import *
from worker import WorkQueue
from common import my_sleep
from modules import galaxy, message, statistic

class WebAdapter(object):

    def __init__(self, master):
        self.logger = logging.getLogger('WebAdapter')

        self.master = master
        self.account = self.master.account
        self.config = self.master.config

        self.last_fetched_url = ''
        self._mutex = threading.RLock()

        # setup http clients
        self.agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5"
        socket.setdefaulttimeout(30.0)
        
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

        headers = [
            ('User-agent', self.agent),
            ('Keep-Alive', "300")]
        self.opener.addheaders = headers

        self.generate_regexps()

        self.current_planet = None

        self.do_login()

        self.generate_base_urls()

        self.logger.debug(self.base_urls['overview'])


    def setSession(self, value):
        self._session = value

    def getSession(self):
        return self._session

    session = property(getSession, setSession)

    def fs(self):

        request = urllib2.Request(self.base_urls['movement'],
                                  urllib.urlencode({
                                  'am203':3, 'am205':60, 'am209':1,
                                  'expeditiontime':1,
                                  'galaxy':2, 'system':356, 'position':12, 'type':2, 'speed':10, 'union2':0, 'expeditiontime':0,
                                  'holdingOrExpTime': 0, 'holdingtime': 1, 'mission': 8,
                                  'resource1':5000, 'resource2':20000, 'resource3':19000}))
        req = 'http://draco.ogame.org/game/index.php?page=movement&session=%s&am203=3&expeditiontime=1&galaxy=2&holdingOrExpTime=0&holdingtime=1&mission=1&position=12&resource1=0&resource2=0&resource3=0&speed=10&system=356&type=1&union2=0' % self.session
        response = self.fetch_valid_response(req)

    def crawl(self, request):
        response = self.fetch_valid_response(request)
        page = response.read()
        return {'url':request.get_full_url(), 'params':request.get_data(), 'page':page}

    def do_login(self):
        page = self.fetch_valid_response('http://%s.ogame.org/game/reg/login2.php?v=2&login=%s&pass=%s' % (self.account.universe, self.account.username, self.account.password)).read()
        
        result = re.findall(self.REGEXP_SESSION_STR, page)
        if result:
            self.session = result[0]
            self.logger.info('%s login successful' % (self.account.username))
        else:
            self.logger.error('%s loging failed!')
            raise WebError()

        self.generate_base_urls()

        # load player planets
#        
        self.planets = {}
        colonies = self.REGEXPS['planets'].findall(page)
        # if there are colony
        if colonies:
            self.go_to_planet(code=colonies[0][0])
            (code, home_name, home_coord) = self.REGEXPS['planets'].findall(self.last_fetched_page)[0]
            home_planet = OwnPlanet(Coord(home_coord), home_name, code)
            self.planets[home_name] = home_planet
            for code, name, coord in colonies:
                self.planets[name] = OwnPlanet(Coord(coord), name, code)
            # back to the home planet
            self.go_to_planet(name=home_name)
            self.home = home_planet
        # if there is only a home planet
        else:
            (home_name, home_coord) = self.REGEXPS['home'].findall(page)[0]
            home_planet = OwnPlanet(Coord(home_coord), home_name)
            self.planets[home_name] = home_planet
            self.current_planet = home_planet
            self.home = home_planet


    def fetch_page(self, php, ** params):
        url = "%s&%s" % (self.base_urls[php], urllib.urlencode(params))
        return self.fetch_valid_response(url)

    def fetch_valid_response(self, request, skip_validate_check=False):
        self._mutex.acquire()

        if isinstance(request, str):
            request = urllib2.Request(request)
        if self.last_fetched_url:
            request.add_header('Referer', self.last_fetched_url)

        valid = False
        while not valid:
            valid = True
            try:
                response = self.opener.open(request)
                self.last_fetched_url = response.geturl()
                
                cached_response = StringIO.StringIO(response.read())
                
                p = cached_response.getvalue()
                cached_response.seek(0)

                self.last_fetched_page = p

#                if skip_validate_check:
#                    return cached_response
#                elif 'You attempted to log in' in p:
#                    raise BotFatalError("Invalid username and/or password.")
#                elif not p or 'errorcode=8' in self.last_fetched_url:
#                    valid = False
#		#NOTE \ FIX THIS if this fails then just comment it ???
                if 'DB problem' in p:
                    my_sleep(120)
                    old_session = self.session
                    self.do_login()
                    print self.session
                    print request.get_full_url()
                    url = request.get_full_url().replace(old_session, self.session)
                    data = request.get_data()
                    if data: data = data.replace(old_session, self.session)
                    request = urllib2.Request(url, data)
                    valid = False
            except urllib2.HTTPError, e:
                if e.code == 302: # happens once in a while when user and bot are playing simultaneusly.
                    raise BotError()
                else: raise e
            except (urllib2.URLError, httplib.IncompleteRead, httplib.BadStatusLine), e:
                valid = False
            except Exception, e:
                if "timed out" in str(e):
                    valid = False
                else: raise e
            if not valid:
                my_sleep(120)

        self._mutex.release()
        return cached_response

    def generate_base_urls(self):
        self.base_urls = {
            'overview': 'http://%s.ogame.org/game/index.php?page=overview&session=%s&lgn=1' % (self.account.universe, self.session),
            'resource': 'http://%s.ogame.org/game/index.php?page=resources&session=%s' % (self.account.universe, self.session),
            'station': 'http://%s.ogame.org/game/index.php?page=station&session=%s' % (self.account.universe, self.session),
            'fleet': 'http://%s.ogame.org/game/index.php?page=fleet1&session=%s' % (self.account.universe, self.session),
            'galaxy': 'http://%s.ogame.org/game/index.php?page=galaxyContent&session=%s&ajax=1' % (self.account.universe, self.session),
            'message': 'http://%s.ogame.org/game/index.php?page=messages&session=%s' % (self.account.universe, self.session),
            'msg' : 'http://%s.ogame.org/game/index.php?page=showmessage&session=%s&ajax=1' % (self.account.universe, self.session),
            'espionage': 'http://%s.ogame.org/game/index.php?page=minifleet&session=%s&ajax=1' % (self.account.universe, self.session),
            'movement': 'http://%s.ogame.org/game/index.php?page=movement&session=%s' % (self.account.universe, self.session),
            'statistic' : 'http://%s.ogame.org/game/index.php?page=statistics&session=%s' % (self.account.universe, self.session),
            'statistic_content' : 'http://%s.ogame.org/game/index.php?page=statisticsContent&session=%s&ajax=1' % (self.account.universe, self.session),
            'logout' : 'http://%s.ogame.org/game/index.php?page=logout&session=%s' % (self.account.universe, self.session),
            'events' : 'http://%s.ogame.org/game/index.php?page=fetchEventbox&session=%s&ajax=1' % (self.account.universe, self.session),
        }

    def generate_regexps(self):

        self.REGEXP_COORDS_STR  = r"([1-9]{1,3}):([0-9]{1,3}):([0-9]{1,2})"
        self.REGEXP_SESSION_STR = r"[0-9A-Fa-f]{12}"

        self.REGEXPS = {
            'home' : re.compile(r'<span class="planet-name">(.+?)</span>\s*?<span class="planet-koords">\[(.+?)\]</span>', re.DOTALL),
            'planets' : re.compile(r'cp=([\d\w]+)".+?<span class="planet-name">(.+?)</span>\s*?<span class="planet-koords">\[(.+?)\]</span>', re.DOTALL),
            'token': re.compile(r"'token' value='(.*)' />"),
            'fleet_slots':re.compile(r"<span>fleets:</span> (\d+/\d+)                        </div>.*?<span>Expeditions:</span> (\d+/\d+)            </div>", re.DOTALL),
        }

    def relogin(self):

        self.fetch_page('logout')
        self.do_login()

    def go_to_planet(self, name=None, code=None):
        if not code:
            planet = self.planets.get(name)
            code = planet.code
            self.current_planet = planet
        request = urllib2.Request(self.base_urls['overview'], urllib.urlencode({'cp':code}))

        self.fetch_valid_response(request)

    def building(self, planet, build, wait=False, timeout=10):
        def post_request(url):
            page = self.fetch_valid_response(url).read()
            token = self.REGEXPS['token'].search(page)

            token = token.group(1)

            if '<li id="%s" class="on">' % (build_entry['slot']) in page:
                params = {'modus': '1', 'token': token, 'type':build_entry['type']}
                if planet.code:
                    params['cp'] = planet.code
                if build_entry.get('build_params'):
                        params.update(build_entry.get('build_params'))
                request = urllib2.Request(url, urllib.urlencode(params))
                resp = self.fetch_valid_response(request)
                self.logger.info('Upgrading %s on %s%s' % (build_entry['name'], planet.name, planet.coord))
                my_sleep(2)
                return True
            else:
                return False

        build_entry = self.master.config.building[build]
        url = self.base_urls[build_entry['section']]

        if planet.code:
            url = url + '&cp=%s' % planet.code

        if wait:
            while not post_request(url):
                my_sleep(10)
        else:
            return post_request(url)

    def spy(self, target):

        while not (self.get_free_fleet_slots > 0):
            my_sleep(2)

        request = urllib2.Request(self.base_urls['espionage'],
                                  urllib.urlencode({'galaxy':target[0], 'system':target[1], 'position':target[2], 'shipCount':3, 'type':1, 'mission':6}))
        resp = self.fetch_valid_response(request)
        result = resp.read()
        if result.endswith("[%s]" % format_coord(target)):
            return True
        else:
            return False

    def get_messages(self, all=False):

        next_page = 1
        messages = []

        while next_page:
            request = urllib2.Request(self.base_urls['message'],
            urllib.urlencode({'ajax': 1, 'displayCategory' : 9, 'displayPage' : next_page, 'siteType':'undefined'}))
            page = self.fetch_valid_response(request).read()
            print next_page
            (msgs, next_page) = message.parse_messages(page, all)
            messages = messages + msgs

        for m in msgs:
            self.read_message(m)
        
        return messages

    def read_message(self, msg):

        request = urllib2.Request(self.base_urls['msg'],
            urllib.urlencode({'msg_id':msg.ogameid}))
        page = self.fetch_valid_response(request).read()

        result = {'SpyReport':message.parse_spy_report}[msg.type](page)

        msg.content = result

        return msg


    def statistic(self):
        self.fetch_page('statistic')
        my_sleep(2)
        request = urllib2.Request(self.base_urls['statistic_content'],
                    urllib.urlencode({'sort_per_member':0, 'start_at':-1, 'type':'ressources', 'who':'player'}))
        self.fetch_page('events')

        page = self.fetch_valid_response(request).read()

        soup = BeautifulSoup(page)

        values = [int(op['value']) for op in soup.find("select").findAll("option")[1:]]

        count = 0
        records = []
        for v in values:
            records = records + self.get_statistic(v)
            count = count + 1
            print v
            if count % 10 == 0:
                print 'relogin'
                my_sleep(120)
                self.relogin()
        return records


    def get_statistic(self, start=1):
        request = urllib2.Request(self.base_urls['statistic_content'],
            urllib.urlencode({'sort_per_member':0, 'start':start, 'start_at':start, 'type':'ressources', 'who':'player'}))

        page = self.fetch_valid_response(request).read()
        return statistic.parse_player_stat(page)

    def get_fleet_slots(self):

        resp = self.fetch_valid_response(self.base_urls['fleet'])

        slots = self.REGEXPS['fleet_slots'].findall(resp.read())[0]

        return [[int(s) for s in slot.split('/')] for slot in slots]
#        return slots

    def get_free_fleet_slots(self):
        slots = self.get_fleet_slots()
        return slots[0][1] - slots[0][0]

    def scan_solar_systems(self, solar_systems):
        from progressbar import *

        self.logger.info('Start scaning galaxy: %s' % solar_systems)

        urls = []

        scan_widgets = ['Scaning: ', Percentage(), ' ', Bar('>'), ' ', ETA()]
        scan_bar = ProgressBar(widgets=scan_widgets, maxval=len(solar_systems)).start()

        for c in solar_systems:
            request = urllib2.Request(self.base_urls['galaxy'], urllib.urlencode({'galaxy':c.galaxy, 'system':c.system}))
            urls.append(request)

        crawl_worker = WorkQueue([self.crawl for i in range(10)])

        for key, u in enumerate(urls):
            crawl_worker.enqueue(key, u)

        parse_worker = WorkQueue([galaxy.parse_galaxy for i in range(10)])

        count = 0
        for key, out in crawl_worker:
            scan_bar.update(count)
            count += 1
            parse_worker.enqueue(key, out)

        galaxy_datas = []

        scan_bar.finish()

        for key, solar in parse_worker:
            galaxy_datas.extend(solar)

        result = []
        for d in galaxy_datas:
            obj = galaxy.read_galaxy_data(d)
            if obj:
                result.append(obj)

        self.logger.info('Scan galaxy completed.')

        return result

if __name__ == '__main__':
    config = {'universe':'draco','username':'jeffrey','password':'killjava'}
    web = WebAdapter(config)
    web.do_login()
    
    request = urllib2.Request(web.base_urls['galaxy'], urllib.urlencode({'galaxy':2, 'system':291}))
    page = web.fetch_valid_response(request)
    # setup http clients
#    agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5"
#    socket.setdefaulttimeout(30.0)
#
#    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
#
#    headers = [
#        ('User-agent', self.agent),
#        ('Keep-Alive', "300")]
#    opener.addheaders = headers
