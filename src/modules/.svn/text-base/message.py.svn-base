# -*- coding: utf-8 -*-

from time import sleep

from BeautifulSoup import BeautifulSoup
from entity import *
import logging
import re
import threading
import traceback
from utils import *

def parse_spy_report(page):

    result = {}
    
    p = re.compile(r'>\[(.*)\]</a> \(Player \'(.*)\'\).*?Metal:</td><td> ([\d\.]+)</td> .*?Crystal:</td> <td>([\d\.]+)</td>.*?Deuterium:</td><td> ([\d\.]+)</td> .*?Energy:</td> <td>([\d\.]+)</td>', re.DOTALL)

    g = p.search(self.content).groups(0)

    result['coord'] = Coord(g[0])
    result['player'] = g[1]
    result['metal'] = parse_decimal(g[2])
    result['metal'] = parse_decimal(g[3])
    result['deuterium'] = parse_decimal(g[4])
    result['energy'] = parse_decimal(g[5])

    has_fleets = re.compile(r'colspan="6">fleets</th>').search(page)
    has_defense = re.compile(r'colspan="6">Defense</th>').search(page)
    has_building = re.compile(r'colspan="6">Building</th>').search(page)
    has_research = re.compile(r'colspan="6">Research</th>').search(page)

    small_cargo = re.compile(r'Small Cargo</td><td class=value>([\d\.]+)</td>').search(page)
    large_cargo = re.compile(r'Large Cargo</td><td class=value>([\d\.]+)</td>').search(page)
    light_fighter = re.compile(r'Light Fighter</td><td class=value>([\d\.]+)</td>').search(page)
    heavy_fighter = re.compile(r'Heavy Fighter</td><td class=value>([\d\.]+)</td>').search(page)
    cruiser = re.compile(r'Cruiser</td><td class=value>([\d\.]+)</td>').search(page)
    battleship = re.compile(r'Battleship</td><td class=value>([\d\.]+)</td>').search(page)
    battlecruiser = re.compile(r'Battlecruiser</td><td class=value>([\d\.]+)</td>').search(page)
    recycler = re.compile(r'Recycler</td><td class=value>([\d\.]+)</td>').search(page)
    esp_probe = re.compile(r'Espionage Probe</td><td class=value>([\d\.]+)</td>').search(page)
    solar_satellite = re.compile(r'Solar Satellite</td><td class=value>([\d\.]+)</td>').search(page)

    rl = re.compile(r'Rocket Launcher</td><td class=value>([\d\.]+)</td>').search(page)
    ll = re.compile(r'Light Laser</td><td class=value>([\d\.]+)</td>').search(page)
    hl = re.compile(r'Heavy Laser</td><td class=value>([\d\.]+)</td>').search(page)
    gc = re.compile(r'Gauss Cannon</td><td class=value>([\d\.]+)</td>').search(page)
    ssd = re.compile(r'Small Shield Dome</td><td class=value>([\d\.]+)</td>').search(page)
    lsd = re.compile(r'Large Shield Dome</td><td class=value>([\d\.]+)</td>').search(page)
    abm = re.compile(r'Anti-Ballistic Missiles</td><td class=value>([\d\.]+)</td>').search(page)

    weapon = re.compile(r'Weapons Technology</td><td class=value>([\d\.]+)</td>').search(page)
    shield = re.compile(r'Shielding Technology</td><td class=value>([\d\.]+)</td>').search(page)
    armour = re.compile(r'Armour Technology</td><td class=value>([\d\.]+)</td>').search(page)

    if has_fleets:
        result['SC'] = parse_decimal(small_cargo[0]) if small_cargo else 0
        result['LC'] = parse_decimal(large_cargo[0]) if large_cargo else 0
        result['LF'] = parse_decimal(light_fighter[0]) if light_fighter else 0
        result['HF'] = parse_decimal(heavy_fighter[0]) if heavy_fighter else 0
        result['CC'] = parse_decimal(cruiser[0]) if cruiser else 0
        result['BS'] = parse_decimal(battleship[0]) if battleship else 0
        result['BC'] = parse_decimal(battlecruiser[0]) if battlecruiser else 0
        result['RECY'] = parse_decimal(recycler[0]) if recycler else 0
        result['ESP'] = parse_decimal(esp_probe[0]) if esp_probe else 0
        result['SS'] = parse_decimal(solar_satellite[0]) if solar_satellite else 0

    if has_defense:
        result['RL'] = parse_decimal(rl[0]) if rl else 0
        result['LL'] = parse_decimal(ll[0]) if ll else 0
        result['HL'] = parse_decimal(hl[0]) if hl else 0
        result['GC'] = parse_decimal(gc[0]) if gc else 0
        result['SD'] = parse_decimal(ssd[0]) if ssd else 0
        result['LD'] = parse_decimal(lsd[0]) if lsd else 0
        result['abm'] = parse_decimal(abm[0]) if abm else 0

    if has_research:
        result['weapon'] = int(weapon[0]) if weapon else -1
        result['shield'] = int(shield[0]) if shield else -1
        result['armour'] = int(armour[0]) if armour else -1

    return result

def parse_messages(page, all=False):

    soup = BeautifulSoup(page)

    messages_html = soup.findAll("tr", {'class': True if all else re.compile(r'.*?new.*')}, id=True)

    messages = []

    next_page = 0
    if soup.find("div", "selectContainer"):
        next = soup.find("a", "changePage", style="margin-right:2px;", href=True)
        if next:
            next_page = int(re.search(r'\d,(\d+)', next['onclick']).group(1))

    for m in messages_html:

        sender = m.find("td", "from").string.strip()
        msg_id = m.find("td", "check").find("input")['id']

        date_str = m.find("td", "date").string.strip()
        sender = m.find("td", "from").string.strip()
        servertime = parse_time(date_str)
        subject_p = m.find("td", "subject")
        subject = subject_p.find("span").string.strip() if subject_p.find('span') else subject_p.find("a").contents[0].strip()
        # skip own fleet activity
        if subject in ("Reaching a planet", "Return of a fleet", "Fleet deployment") or subject.startswith('Expedition Result [') or subject.startswith('Harvesting report') or sender == 'Fleet':
            continue
        
        if sender == "Space monitoring":
            msg = Message(type='EspAction', subject=subject, servertime=servertime, content="", ogameid=msg_id, sender='SYSTEM')
        elif sender == "Fleet Command":
            if subject.startswith('Combat Report'):
                msg = Message(type='ComatReport', subject=subject, servertime=servertime, content="", ogameid=msg_id, sender='SYSTEM')
            elif subject.startswith('Espionage report'):
                msg = Message(type='SpyReport', subject=subject, servertime=servertime, content="", ogameid=msg_id, sender='SYSTEM')
        else:
            msg = Message(type='msg', subject=subject, servertime=servertime, content="", ogameid=msg_id, sender=sender)

        messages.append(msg)

    return messages, next_page