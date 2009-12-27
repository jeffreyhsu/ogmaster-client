# -*- coding: utf-8 -*-

from time import sleep

from BeautifulSoup import BeautifulSoup
from entity import *
import logging
import re
import threading
import traceback
from utils import *

def parse_galaxy(page_entry):
    page = page_entry['page']
    params = page_entry['params']

    galaxy_p = int(re.findall(r'galaxy=(\d+)', params)[0])
    system_p = int(re.findall(r'system=(\d+)', params)[0])

    soup = BeautifulSoup(page)

    rows = soup.findAll("tr", "row")

    result = []

    for row in rows:
        try:
            planet = Planet()
            player = Player()

            row_data = {
                'planet': None,
                'player': None,
                'alliance': None,
                'ogevent': None,
            }

            pos_p = int(row.find("td", "position").string.strip())

            # 判断是否是空白星球
            if row.find("td", "microplanet1"):
                planet.status = 'vacant'
                planet.set_coordinate([galaxy_p, system_p, pos_p])
                row_data['planet'] = planet
                result.append(row_data)
                continue

            position = row.find("span", id="pos-planet").string.strip()[1:-1]
            player_e = row.find("a", rel=re.compile('#player\d+'))
            if not player_e:
                continue

            player_id = int(player_e['rel'][7:])

            # 判断是否是摧毁的星球
            if player_id == 99999:
                planet = Planet()
                planet.set_coordinate = parse_coord(position)
                planet.status = 'destroyed'

                row_data['planet'] = planet
                result.append(row_data)
                continue

            planet.player_ogameid = player_id

            player_rank = row.find("div", id="TTPlayer").find("li", "rank").string.strip()[9:]
            try:
                player.rank = int(player_rank)
            except:
                player.rank = 0


            planet.player_name = player_e.span.string.strip()

            player.name = planet.player_name
            player.ogameid = planet.player_ogameid

            planet.name = row.h4.find("span", "textNormal").string.strip()
            planet.set_coordinate(parse_coord(position))
            planet.status = 'colonized'

            ogevent = None
            ogevent_e = row.find("span", "undermark")
            if ogevent_e:
                ogevent = OgameEvent()
                ogevent.data = ogevent_e.string.strip()
                ogevent.type = 'planet'

            alliance_e = row.find("span", rel=re.compile('#alliance\d+'))
            alliance = None
            if alliance_e:
                alliance = Alliance()
                alliance.name = alliance_e.contents[0].strip()
                alliance.ogameid = int(alliance_e['rel'][9:])

            debris_e = row.find("td", "debris")
            deb_metal = None
            deb_crystal = None
            deb_recyclers = None
            if debris_e.img:
                debris_content = debris_e.findAll("li", "debris-content")
                deb_metal = int(debris_content[0].string.strip()[7:].replace('.', ''))
                deb_crystal = int(debris_content[1].string.strip()[9:].replace('.', ''))
                deb_recyclers = int(debris_e.find("li", "debris-recyclers").string.strip()[18:])
                planet.debris_amount = deb_recyclers
                planet.debris_metal = deb_metal
                planet.debris_crystal = deb_crystal

            player_status = set()

            if row.find("span", "status_abbr_vacation"): player_status.add('v')
            if row.find("span", "status_abbr_noob"): player_status.add('n')
            if row.find("span", "status_abbr_inactive"): player_status.add('i')
            if row.find("span", "status_abbr_longinactive"): player_status.add('I')
            if row.find("span", "status_abbr_banned"): player_status.add('b')

            if row.find("td", "moon").a: planet.has_moon = True

            player.status = player_status
            planet.player_status = player_status

            row_data['planet'] = planet
            row_data['alliance'] = alliance
            row_data['ogevent'] = ogevent
            row_data['player'] = player

            result.append(row_data)
        except BaseException, e:
            traceback.print_exc()
            
    return result

def read_galaxy_data(data):
    def check_name(entity, name):
        if entity.name != name:
            entity.name = name
            entity.prev_names.append(name)

    player = data['player']
    planet = data['planet']
    alliance = data['alliance']
    ogevent = data['ogevent']

    datas = {'ogevent':ogevent}

    if planet.status == 'vacant':
        old_planet_query = db.query(Planet).filter_by(formated_coord = planet.formated_coord)
        # 查找该星球是否以前有人殖民过
        old_planet = old_planet_query.filter_by(status='colonized').first()
        if old_planet:
            # 如果找到，设置以前的星球为destroyed状态
            if old_planet:
                old_planet.status = 'destroyed'
                db.merge(old_planet)
        if old_planet_query.filter_by(status='vacant').count() <= 0:
            db.add(planet)
        db.flush()
        datas['planet'] = planet
        return datas

    # 查找这个摧毁的星球以前的情况
    if planet.status == 'destroyed':
        old_planet = db.query(Planet).filter_by(formated_coord = planet.formated_coord, status='colonized').first()
        # 找到该记录，设置以前的星球为destroyed状态
        if old_planet:
            old_planet.status = 'destroyed'
            db.merge(old_planet)
            db.flush()
        # 增加一个空白星球，因为很快该摧毁的星球将变成空白
        planet.status = 'vacant'
        db.add(planet)
        db.flush()
        datas['planet'] = planet
        return datas

    if alliance:
        alliance_entity = db.query(Alliance).filter_by(ogameid=alliance.ogameid).first()
        if alliance_entity:
            check_name(alliance_entity, alliance.name)
            db.merge(alliance_entity)
        else:
            db.add(alliance)
            alliance_entity = alliance
    else:
        alliance_entity = None

    player_entity = db.query(Player).filter_by(ogameid=player.ogameid).first()
    if player_entity:
        check_name(player_entity, player.name)
        player_entity.rank = player.rank
        player_entity.status = player.status
        if alliance_entity:
            player_entity.alliance_id = alliance_entity.id
        db.merge(player_entity)
    else:
        player_entity = player
        if alliance_entity:
            player_entity.alliance_id = alliance_entity.id
        db.add(player_entity)


    # 有人殖民的星球：
    
    planet_entity = db.query(Planet).filter_by(formated_coord=planet.formated_coord).first()
    if planet_entity:
        # 检查该星球是否改名
        check_name(planet_entity, planet.name)
        # 检查该星球是否易主
        if planet_entity.player_ogameid == player_entity.ogameid:
            # 同属于一个玩家，更新该星球的信息
            planet_entity.player_name = player_entity.name
            planet_entity.player = player_entity
            planet_entity.debris_metal = planet.debris_metal
            planet_entity.debris_crystal = planet.debris_crystal
            planet_entity.debris_amount = planet.debris_amount
            player_entity.status = player.status
            player_entity.rank = player.rank
            db.merge(planet_entity)
            db.merge(player_entity)
        else:
            # 属于不同的玩家
            # 设置过去的星球为destroyed状态
            planet_entity.status = 'destroyed'
            db.merge(planet_entity)
            # 添加新的星球信息
            planet.player = player_entity
            db.add(planet)
            planet_entity = planet
    else:
        # 完全新发现的星球
        planet.player = player_entity
        db.add(planet)
        planet_entity = planet

    if ogevent:
        ogevent.owner = player_entity
        ogevent.owner_planet = planet_entity
        db.add(ogevent)

    datas['planet'] = planet_entity
    datas['ogevent'] = ogevent
    db.flush()
    return datas