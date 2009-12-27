## -*- coding: utf-8 -*-
#
#import threading
#import logging
#import socket
#import urllib
#import urllib2
#
#from entity import *
#from utils import *
#
#__all__ = ['SpiderThread']
#
#class SpiderThread(threading.Thread):
#    '''Posts request and get ogame pages from url_queue'''
#    def __init__(self, url_queue, page_queue, opener):
#
#        threading.Thread.__init__(self, name="SpiderThread")
#        self.logger = logging.getLogger('Spider')
#
#        self._url_queue = url_queue
#        self._page_queue = page_queue
#
#        self.opener = opener
#
#    def run(self):
#        socket.setdefaulttimeout(20)
#
#        while True:
#            