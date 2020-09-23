#!/usr/bin/python3.6
''' This is a future implementation '''

''' Using pubgs open API to create another layer of detail on the announced kill, game placement, damage dealt, etc. '''
import json, requests, traceback
from abc import ABC, abstractmethod

class Api(ABC):
    ''' Trying to learn abc..'''
    def __init__(self):
        self.url = 'https://api.pubg.com/shards/steam'

class GetData(Api):
    def MatchInfo(self, matchid=None):
        ''' Returns data and statistics for this match '''
        if matchid is None:
            return False
        headers = {'Accept': 'application/vnd.api+json'}
        self.append = '/matches/{}'.format(matchid)
        get = requests.get(self.url + self.append, headers=headers)
        data = json.loads(get.text)
        if data is None:
            return False
      
        return data

def compute(victim=None, matchid=None):
    ''' Get match data from pubg'''
    from bot.pubg import Api as dApi
    x = GetData() # Init pubg api
    y = dApi()    # Init report api
    victimid = y.getId(victim)
    proc = x.MatchInfo(matchid=matchid)
    if victimid == None:
        return False
    try:
        if 'included' in proc:
            for i in proc['included']:
                if i['id'] == victimid: # AccountID
                    diter = i['attributes']['stats']
                    place = diter['winPlace']
                    kills = diter['kills']
                    time = diter['timeSurvived'] / 60
                    knocked = diter['DBNOs']
                    return('{} had {} kills, {} knock(s), was alive for {} minutes and was ranked {}/100 in this match.'.format(victim, kills, knocked, round(time,1), place))
    except:
        #DEBUG
        traceback.print_exc()
        pass
    return False
