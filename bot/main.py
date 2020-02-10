#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-
import discord, logging, json, requests, datetime, sqlite3, time, asyncio, os
from discord import Webhook, RequestsWebhookAdapter
from calendar import timegm
name = 'pubg.report bot'
bot_username = ''
init = 'no'
weapons_list = {}
map_list = {}
damage_list = {}
logging.basicConfig(level=logging.INFO)

if os.path.exists('database.db') is False:
    print('Setting up db..', end='')
    x = sqlite3.connect('database.db')
    c = x.cursor()
    queries = [
    'CREATE TABLE players (discordname TEXT, pubgname TEXT);',
    'CREATE TABLE matches (eventid TEXT);'
    ]
    for i in queries:
        c.execute(i)
    x.commit()
    x.close()
    print('Done')

#Load the neccecary assets before we do anything else.
print('Loading external assets..') 
a = requests.get('https://raw.githubusercontent.com/pubg/api-assets/master/dictionaries/telemetry/damageCauserName.json')
weapons_list.update(json.loads(a.text))
c = requests.get('https://raw.githubusercontent.com/pubg/api-assets/master/dictionaries/telemetry/mapName.json')
map_list.update(json.loads(c.text))

def getUser(i):
    '''Find the discord username of whoever owns this id'''
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    query = 'SELECT discordname FROM players WHERE pubgname = "{}"'.format(i)
    result = c.execute(query)
    result = result.fetchall()
    conn.close()
    if len(result) > 0:
        return result[0]
    return False

def checkforupdate():
    with open('version.txt', 'r') as versions:
        version = json.loads(versions.read())
    version = version['version']
    versions.close()
    def update(update):
        newversion = update['version']
        if float(newversion) > float(version):
            print('\n\n\n{} v{}\nNew version available: v{}\nGet it here: https://github.com/kragebein/pubg.reportbot\n\n\n\n\n'.format(name, version, newversion))
        else:
            print(name + ' v' + version)
    try:
        f = requests.get('https://raw.githubusercontent.com/kragebein/pubg.reportbot/master/version.txt')
        upt = f.json()
    except:
        pass
    try:
        update(upt)
    except:
        print(name + ' v' + version)

checkforupdate()

def getEvent(i):
    '''Check if this is already processed.'''
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    query = 'SELECT eventid FROM matches WHERE eventid = "{}"'.format(i)
    result = c.execute(query)
    result = result.fetchall()
    conn.close()
    if len(result) > 0:
        return True
    return False

def build_embed(apiobj, discorduser=None, killer=None, victim=None, distance=None, mmap=None, mode=None, weapon=None, event=None, twitchID=None, videoID=None, matchID=None, eventID=None, when=None, diff=None, test=None):
    ''' Function to build embed data'''
    if getEvent(eventID):
        return # stop execution if event has already been posted.    
    logging.info('Update Found!')
    # We need to name and add a few assets to the embed. 
    DamageCauser = {
        "LogPlayerKill": 'killed' ,
        "LogPlayerDeath": 'killed',
        "LogTeammateKill": 'killed teammate',
        "LogTeammateDeath": 'killed by teammate',
        "LogPlayerMadeGroggy": 'knocked out',
        "LogPlayerMakeGroggy": 'knocked',
        "LogTeammateMakeGroggy": 'knocked',
        "LogTeammateMadeGroggy": 'knocked out',
        "redzone": "Redzoned",
        "blackzone": "BlackZoned",
        "bluezoned": "BlueZoned"
    }
    imagetype = {
        "killed": "https://raw.githubusercontent.com/pubg/api-assets/master/Assets/Icons/Killfeed/Death.png",
        "killed teammate": "https://raw.githubusercontent.com/pubg/api-assets/master/Assets/Icons/Killfeed/Death.png",
        "killed by teammate": "https://raw.githubusercontent.com/pubg/api-assets/master/Assets/Icons/Killfeed/Death.png",
        "knocked out": "https://raw.githubusercontent.com/pubg/api-assets/master/Assets/Icons/Killfeed/Groggy.png",
        "knocked": "https://raw.githubusercontent.com/pubg/api-assets/master/Assets/Icons/Killfeed/Groggy.png",
        "Redzoned": "https://raw.githubusercontent.com/pubg/api-assets/master/Assets/Icons/Killfeed/Redzone.png",
        "BlueZoned": "https://raw.githubusercontent.com/pubg/api-assets/master/Assets/Icons/Killfeed/Bluezone.png",
        "BlackZoned": "https://raw.githubusercontent.com/pubg/api-assets/master/Assets/Icons/Killfeed/Blackzone.png"
    }

    maptype = {
        "Erangel (Remastered)": "https://github.com/pubg/api-assets/raw/master/Assets/MapSelection/Erangel.png",
        "Erangel": "https://github.com/pubg/api-assets/raw/master/Assets/MapSelection/Erangel.png",
        "Miramar": "https://github.com/pubg/api-assets/raw/master/Assets/MapSelection/Miramar.png",
        "Sanhok": "https://github.com/pubg/api-assets/raw/master/Assets/MapSelection/Sanhok.png",
        "Vikendi": "https://github.com/pubg/api-assets/raw/master/Assets/MapSelection/Vikendi.png",
        "Karakin": "https://gamerjournalist.com/wp-content/uploads/2020/01/PUBG-Karakin-Map-1024x555.jpg" # Update this when api assets are updated.
    }

    timestamp = int(time.time())
    weapon = weapons_list[weapon]
    mapp = map_list[mmap]
    event = DamageCauser[event]
    # Blatantly stolen from https://pastebin.com/XdDE81Q2
    # Calculates timestamp on twitch url
    videoID = videoID[1:]
    event_time = when
    event_time = event_time[:-1]
    epoch_time = time.strptime(event_time, "%Y-%m-%dT%H:%M:%S")
    epoch_time = timegm(epoch_time)
    timecode = diff
    timecode = timecode.split(".")
    timecode = timecode[0]
    timecode = timecode.split(":")
    h,m,s = timecode[0],timecode[1],timecode[2]
    timecode = "{}h{}m{}s".format(h,m,s)
    # Credit to whoever made this

    embed = discord.Embed(title='{} just {} {}!'.format(killer, event, victim),url="https://www.twitch.tv/videos/{}?t={}".format(videoID,timecode), timestamp=datetime.datetime.utcfromtimestamp(timestamp))
    embed.set_thumbnail(url=imagetype[event])
    embed.set_author(name=discorduser, url="https://github.com/kragebein/pubg.reportbot", icon_url="https://avatars0.githubusercontent.com/u/19599766?s=120&v=4")
    embed.set_footer(text="pubg.reportbot")
    embed.set_image(url=maptype[mapp])
    embed.add_field(name="Attacker", value="{}".format(killer), inline=True)
    embed.add_field(name="Victim", value="{}".format(victim), inline=True)
    embed.add_field(name="Map", value="{}".format(mapp))
    embed.add_field(name="Weapon", value="{}".format(weapon), inline=True)
    embed.add_field(name="Distance", value="{}".format(str(distance) + ' meters'), inline=True)

    # Add this video to the database
    # This will prevent the bot from posting this video again 
    x = sqlite3.connect('database.db')
    conn = x.cursor()
    query = 'INSERT INTO matches VALUES("{}")'.format(eventID)
    conn.execute(query)
    x.commit()
    x.close()

    # Send the data through to the webhook.
    say(embed=embed)

def say(text=None, embed=None):
    from pubgbot import webhook_uri
    uri = webhook_uri.split('/')
    webhook = Webhook.partial(uri[5], uri[6], adapter=RequestsWebhookAdapter())
    if text is None:
        text = ''
    webhook.send(text, embed=embed, username=bot_username)

class Pubgbot(discord.Client):
    async def on_ready(self):
        ''' initialize bot and report plugin'''
        logging.info('Logged in as {}'.format(self.user))
        bot_username = '{}'.format(self.user) #Make username Global. 
        loop = client.loop
        from bot.paralell import main as runloop
        await loop.run_in_executor(None, runloop)
        
    async def on_message(self, message):
        from bot.pubg import Api
        api = Api()
        text = message.content
        print('< {}> {}'.format(message.author, text))
        if message.author != self.user:
            msg = message.content.split(' ')
            if msg[0] == '!test':
                if len(msg) != 2:
                    await message.channel.send('Requires Exactly 1 argument')
                    return
                
                from bot.pubg import Api
                api = Api()
                report_id = api.getId(msg[1])
                api.event(report_id, message.author)

            ## REPORT
            if msg[0] == '!reportid':
                if len(msg) != 2:
                    await message.channel.send('This command requires an argument!')
                    return
                try: 
                    report_id = api.getId(msg[1])
                except:
                    await message.channel.send('Couldnt find that user.')
                    return
                await message.channel.send('pubg.report id: {}'.format(report_id))

            ## REGISTER
            elif msg[0] == '!register':
                if len(msg) != 2:
                    await message.channel.send('This command requires exactly 1 argument!\n!register <pubgname> (without <>)')
                    return
                try:
                    report_id = api.getId(msg[1])
                    print(report_id)
                    if report_id is None:
                        await message.channel.send('Sorry. Couldnt find match for that playername')
                        return False
                except Exception as r: 
                    await message.channel.send('Sorry, couldnt find any players with that name.')
                    logging.info(r)
                    return False
                register = api.report_register(message.author, report_id)
                if register is False:
                    await message.channel.send('Sorry, couldnt track this player. Already registered?')
                    return False
                elif register is True:
                    await message.channel.send('Added player "{}" to the tracking.'.format(msg[1]))
                    return False
                
            ## UNREGISTER
            elif msg[0] == '!unregister':
                if len(msg) != 2:
                    await message.channel.send('This command requires exactly 1 argument!\n!unregister <pubgname> (without <>)')
                    return
                report_id = api.getId(msg[1])
                unregister = api.report_unregister(message.author, report_id)
                if unregister is True:
                    await message.channel.send('Removed {} from tracking.'.format(msg[1]))
                    return
                elif unregister is False:
                    await message.channel.send('Couldnt remove {} from tracking, are you sure the user exists?'.format(msg[1]))
                    return
client = Pubgbot()



