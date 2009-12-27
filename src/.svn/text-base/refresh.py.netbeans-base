# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jeffrey"
__date__ ="$Oct 29, 2009 10:31:23 AM$"

import urllib, urllib2, socket, httplib, cookielib
import re, random
from time import sleep

username = ''
password = ''

def my_sleep(seconds):
    for dummy in range(0, random.randrange(seconds, seconds+10)):
        sleep(1)

if __name__ == "__main__":
        agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.7) Gecko/2009021906 Firefox/3.0.7"
        serverTimeDelta = None

        # setup urllib2:
        socket.setdefaulttimeout(30.0)
        #httplib.HTTPConnection.debuglevel = 1

        # set up a class to handle http cookies, passes that to http processor
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        # set us a class to keep connections open, passas that to the http processor
#        keepAliveOpener = urllib2.build_opener(keepalive.HTTPHandler())

        headers = [('User-agent', agent),('Keep-Alive', "300")]
        opener.addheaders = headers

        session = None

        while(True):

            # if has session, logout first
            if session:
                opener.open("http://draco.ogame.org/game/index.php?page=logout&session=%s", session)
                print 'logout!'
            
            resp = opener.open("http://draco.ogame.org/game/reg/login2.php?v=2&login=%s&pass=%s" % (username, password))
            page = resp.read()
            result = re.findall(r"[0-9A-Fa-f]{12}", page)
            resp.close()
            if result:
                session = result[0]
                print 'Login successful: %s' % (username)
            else:
                print 'loging failed!'

            my_sleep(10)