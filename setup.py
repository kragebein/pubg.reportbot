#!/usr/bin/python3
import sqlite3

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
print('Database has been created.')