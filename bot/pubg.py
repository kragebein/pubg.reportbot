#!/usr/bin/python3.6
import json, re, requests, sqlite3, discord, time
class Api():
    from bot.main import build_embed
    def getId(self, i):
        url  = "https://api.pubg.report/search/" + i
        x = requests.get(url)
        z = x.text
        y = json.loads(z)
        for y in y:
            if y['shard'] == "steam":
                return y['id']
        return None
                
    def getStream(self, i):
        if i.split('.')[0] != 'account':
            id = self.getId(i)
        id = i
        if id != None:
            url = "https://api.pubg.report/v1/players/" + id + "/streams"
            x = requests.get(url)
            z = x.text
            return z

    def event(self, i, discorduser):
        k = self.getStream(i)
        if k != None:     
            k = json.loads(k)
            for i in iter(k):
                x = k[i]
                for item in x:
                    mmap = item['Map']
                    killer = item['Killer'] 
                    victim = item['Victim']
                    distance = item['Distance']
                    when = item['TimeEvent']
                    weapon = item['DamageCauser']
                    mode = item['Mode']
                    event = item['Event']
                    twitchID = item['TwitchID']
                    videoID = item['VideoID']
                    matchID = item['MatchID']
                    eventID = item['ID']
                    diff = item['TimeDiff']
                    # Send to build embed so we can prettyprint it to discord.
                    time.sleep(1)
                    self.build_embed(discorduser=discorduser, killer=killer, victim=victim, distance=distance, mmap=mmap, mode=mode, weapon=weapon, event=event, twitchID=twitchID, videoID=videoID, matchID=matchID, eventID=eventID, when=when, diff=diff)
        else:
            return None

    def report_register(self, author, name):
        ''' Handles the registration '''
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        rep_sql_reg = 'SELECT pubgname from players WHERE discordname ="{}"'.format(author)
        result = c.execute(rep_sql_reg)
        exist = result.fetchall()
        if len(exist) == 0:
            c.execute('INSERT INTO players VALUES("{}","{}")'.format(author, name))
            conn.commit()
            c.close()
            return True
        c.close()
        return False

    def report_unregister(self, author, name):
        ''' handles the de-registration '''
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        rep_sql_reg = 'SELECT pubgname from players WHERE pubgname ="{}"'.format(name)
        result = c.execute(rep_sql_reg)
        exist = result.fetchall()
        if len(exist) != 0:
            c.execute('DELETE from players WHERE pubgname = "{}"'.format(name))
            conn.commit()
            c.close()
            return True
        c.close()
        return False

