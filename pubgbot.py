#!/usr/bin/python3.6
''' pubg report bot'''

import discord, logging
from bot.main import client as client
logging.basicConfig(level=logging.DEBUG)

# Create an API key here: https://discordapp.com/developers/applications/
# Create a webhook in the channel settings of your discord server
bot_token = 'CHANGEME' # Bot token (discordapi)
webhook_uri = 'CHANGEME' #Webhook URL (discord client)

check_rate = 10  # How often the bot will check for updates, in minutes (no less than five minutes or you'll be banned from pubg.report)
if __name__ == "__main__":
    client.run(bot_token)
