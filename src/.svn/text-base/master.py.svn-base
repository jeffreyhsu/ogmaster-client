
__author__="jeffrey"
__date__ ="$Mar 13, 2009 8:29:02 PM$"

import sys, os
import traceback

sys.path.insert(0, 'src')
sys.path.insert(0, 'lib')

if os.getcwd().endswith("src"):
    os.chdir("..")

import logging
import logging.config

logging.config.fileConfig("logging.conf")

from Queue import *
import yaml
from optparse import OptionParser

import app
from common import *
from utils import *
from entity import *
from modules import intelligence as ai
from modules import statistic as stat
from webadapter import WebAdapter
from worker import *

__version__ = '0.1'
__ogameversion__ = '1.1'

class Master(object):

    def __init__(self, options, args):
        self.logger = logging.getLogger("Master")

        self.options = options
        self.args = args

        self.web = None
        self.config = {}
        
        self._load_config()
        self.i18n = Translations()

    def run(self):

        self.logger.info("Welcome, %s", self.account.username)

        # connect to server and login
        self._connect()

        self.logger.info('ServerTime: ' + get_servertime_now().strftime('%Y-%m-%d %H:%M:%S'))

        # set base planet
        planet_name = self.options.planet if self.options.planet else self.config.get('planet', self.web.home)
        if planet_name:
            self.web.go_to_planet(planet_name)
            self.logger.info("Current planet: %s" % self.web.current_planet)

        # execute tasks
        if self.options.sense:
            self.scan_galaxy(mode='sense', spy=self.options.spy)
        elif self.options.scan:
            self.scan_galaxy(mode='scan', spy=self.options.spy, expression=self.options.scan)
        elif self.options.queue:
            self.start_build_queue()
        elif self.options.message:
            
            msgs = self.web.get_messages(self.options.all)

            for m in msgs:
                try:
                    print m
                except:
                    print 'error-------', m.subject

        elif self.options.stat:
            stat.stat(self.web.statistic())

    def stop(self):
        pass

    def _connect(self):
        self.logger.info('Connecting to server %s.ogame.%s' % (self.account.universe, self.account.domain))
        self.web = WebAdapter(self)

    def scan_galaxy(self, mode, spy=False, expression=None):
        coords = []

        if mode == 'sense':
            for s in self.config['sense']:
                if not s['status']: continue
                p = self.web.planets[s['planet']]
                origin = p.coord
                (o_galaxy, o_system, o_position) = origin.tuple()

                coords.append(origin)
                for i in range(1, int(s['radius'])+1):
                    coords.append(Coord(o_galaxy, o_system + i))
                    coords.append(Coord(o_galaxy, o_system - i))

        elif mode == 'scan':
            coords = parse_coords_exp(expression)

        datas = self.web.scan_solar_systems(coords)

        if spy:
            planets_to_spy = ai.analyze_galaxy(datas)
            from progressbar import *
            spy_widgets = ['Spying: ', Percentage(), ' ', Bar('>'), ' ', ETA()]
            spy_bar = ProgressBar(widgets=spy_widgets, maxval=len(planets_to_spy)).start()
            for i,p in enumerate(planets_to_spy):
                while True:
                    if self.web.spy(p.coordinate()):
                        spy_bar.update(i)
                        break

            self.logger.info("Spy task completed")

    def start_build_queue(self):
        for p,q in self.config.queues.iteritems():
            planet = self.web.planets[p]
            build_queue = Queue()
            for b in q:
                build_queue.put(b)
            thread = BuildThread(self.web, planet, build_queue)
            thread.start()
            thread.join()

        self.logger.info('all buiding in queue is done!')
                
    def _load_config(self):
        # load basic configuration
        cf = file(os.getcwd() + '/config.yml' ,'r')
        self.config = Configuration(cf)
        of = file(os.getcwd() + '/ogame.yml', 'r')
        self.config.update(yaml.load(of.read()))
        of.close()
        
        # load profile
        self.account = Account()
        acc = self.options.account if self.options.account else self.config['default_profile']
        profile_path = os.getcwd() + '/profiles/%s/' % acc
        p = file(profile_path + 'master.yml')
        profile = yaml.load(p.read())
        self.config.update(profile)
        p.close()

        self.account.username = self.config['username']
        self.account.password = self.config['password']
        self.account.universe = self.config['universe']
        self.account.domain = self.config['domain']

        # load queue
        bq = file(profile_path + 'queue.yml')
        build_queue = yaml.load(bq)
        bq.close()
        self.config['queues'] = build_queue

        app.config = self.config

class BuildThread(threading.Thread):
    def __init__(self, web, planet, queue):
        threading.Thread.__init__(self, name="BuildThread")
        self.planet = planet
        self.queue = queue
        self.web = web

    def run(self):
        while not self.queue.empty():
            self.web.building(self.planet, self.queue.get(), wait=True)
            my_sleep(10)

class Account(object):

    def __init__(self):
        self.username = ''
        self.password = ''

    def update(self, map):
        for key, value in map.iteritems():
            setattr(self, key, value)


if __name__ == "__main__":

    print '----------------------------------------'
    print '- OGameMaster %s, Master The Universe -' % __version__
    print '- for ogame%s                         -' % __ogameversion__
    print '- Author: jeffrey                      -'
    print '- Email: jeffreyxu@gmail.com           -'
    print '----------------------------------------'
    parser = OptionParser()
    parser.add_option("-c", "--console", action="store_true", help="Run in console mode")
    parser.add_option("-a", "--account", action="store", help="Choose a account")
    parser.add_option("-p", "--planet", action="store", help="Set base planet")
    parser.add_option("-e", "--sense", action="store_true", help="Sense the surrounding")
    parser.add_option("-E", "--SENSE", action="store", help="Sense the surrounding by given coordinates")
    parser.add_option("-s", "--scan", action="store", help="Scan Galaxy")
    parser.add_option("-r", "--crawl", action="store_true", help="Scan the whole universe")
    parser.add_option("-y", "--spy", action="store_true", help="Espionage a target")
    parser.add_option("-q", "--queue", action="store_true", help="Execute building queue")
    parser.add_option("-m", "--message", action="store_true", help="")
    parser.add_option("-l", "--all", action="store_true", help="")
    parser.add_option("-t", "--stat", action="store_true", help="")
    
    (options, args) = parser.parse_args()

    if options.console:
        master = Master(options, args)
        master.run()
