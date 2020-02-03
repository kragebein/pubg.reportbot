#!/usr/bin/python3.6
''' Module that checks pubg.report for updates '''
import sqlite3, time, logging
from bot.pubg import Api
from pubgbot import check_rate

def getUser(i): 
        query = 'SELECT discordname FROM players WHERE pubgname = "{}"'.format(i)
        conn = sqlite3.connect('database.db')
        sql = conn.cursor()
        data = sql.execute(query)
        data = data.fetchone()[0]
        conn.close()
        return data

   
'''Initialize what we need for the loop'''
timer = check_rate * 60
accountlist = [] #TODO: make some statistics.

def sql():
    query = 'SELECT pubgname FROM players'
    conn = sqlite3.connect('database.db')
    sql = conn.cursor()
    data = sql.execute(query)
    data = data.fetchall()
    conn.close()
    return data

def calculate_checkrate(data):
    ''' Checkrate cannot be lower than the amount of time we use to check each player '''
    # We gape big and use five seconds to process each player
    # This is to *try* to not be banned from pubg.report
    length = len(data)
    estimate = length / 5
    cal = estimate * length
    if cal > check_rate:
        # Calculated estimate exeeds check rate, aborting.
        return False
    return True

def main():
    ''' actual loop'''
    now = int(time.time())
    api = Api()
    run = now
    while True:
        now = int(time.time())
        if run < now:
            data = sql()
            if calculate_checkrate(data) is False:
                logging.info('check_rate in pubgbot.py is too low based on the amount of active users. Either remove users, on increase the rate.')
                break
            logging.info('Checking pubg.report for updates..')
            if len(data) == 0:
                break   #Dont run any further without any data
            for i in range(0, len(data)):
                accountlist.append(data[i][0]) #update list.
            for i in accountlist:
                pubgname = i
                discord = getUser(pubgname)
                #print('Parsing: {}: {}'.format(discord, pubgname))
                try:
                    api.event(pubgname, discord) # Run the results through pubg.report api
                except Exception as r:
                    logging.info('Something went wrong while checking pubg.report. See debug.')
                    logging.debug('Error, unable to connect to api.pubg.report, debug:')
                    logging.debug(r)
                    break
            run += timer
            
        
        

        
        