#!/usr/bin/python3.6
''' This is a future implementation '''

''' Using pubgs open API to create another layer of detail on the announced kill, game placement, damage dealt, etc. '''
import json, requests
from abc import ABC, abstractmethod

class Api(ABC):
    ''' Using abc for future expandability '''
    def __init__(self):
        self.url = 'https://api.pubg.com/shards/steam'

class GetData(Api):

    def MatchInfo(self, matchid=None):
        ''' Returns data and statistics for this match '''
        if matchid is None:
            return None
        headers = {'Accept': 'application/vnd.api+json'}
        self.append = '/matches/{}'.format(matchid)
        get = requests.get(self.url + self.append, headers=headers)
        data = json.loads(get.text)
        return data

x = GetData()
proc = x.MatchInfo(matchid='adcad302-8371-4aca-86ba-8274488f5f87') # Match ID

# We'll just iterate through the statistics for the match.
for i in proc['included']:
    try:
        if i['attributes']['stats']['playerId'] == 'account.ec42e2bbdc6e46768ac054ab87e3e142': # AccountID
            diter = i['attributes']['stats']
            place = diter['winPlace']
            kills = diter['kills']
            time = diter['timeSurvived'] / 60
            knocked = diter['DBNOs']
            print('Player had {} kills (and {} knocks), was alive for {} minutes and was ranked {}/100 in this match.'.format(kills, knocked, round(time,1), place))
            break
    except:
        pass

