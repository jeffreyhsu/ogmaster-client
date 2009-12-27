# -*- coding: utf-8 -*-

from time import sleep

from BeautifulSoup import BeautifulSoup
from entity import *
import logging
import re
import threading
import traceback
from utils import *

def parse_player_stat(page):
    soup = BeautifulSoup(page)

    trs = soup.find("table", id="ranks").findAll("tr")

    records = []

    updated = parse_time(soup.find("h3").string.strip()[21:-1])

    for row in trs[1:]:
        rank = re.compile('\d+').search(row.find("td", "position").contents[0].strip()).group()
        name_p = row.find("td", "name")
        ally_p = name_p.find("span")
        if ally_p:
            ally = ally_p.a.string.strip()[1:-1]
        else:
            ally = None
        player_name = name_p.findAll("a")[-1].string.strip()
        score = parse_decimal(row.find("td", "score").string.strip())

        msg_p = row.find("td", "sendmsg")
        if msg_p.find("a"):
            ogameid = re.compile('&to=(\d+)&ajax=1').search(msg_p.a['href']).group(1)
        else:
            ogameid = None
        
        records.append(PlayerRecord(player_name=player_name, points=score, ogameid=ogameid, ally=ally, rank=rank, updated=updated))
    return records

def stat(records):

    for r in records:
        db.add(r)

#    players = db.query(Player)
#
#    for p in players:
#        result = [r for r in records if r.ogameid == p.ogameid]
#        if result:
#            r = result[0]
#            if p.name != r.player_name:
#                print 'player %s rename to %s' % (p.name, r.player_name)
#                p.name = r.name
#                p.updated = get_servertime_now()
#                db.update(p)

    db.flush()