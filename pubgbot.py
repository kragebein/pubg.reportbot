#!/usr/bin/python3.6
''' pubg report bot'''

import discord, logging
from bot.main import client as client
logging.basicConfig(level=logging.DEBUG)

# Create an API key here: https://discordapp.com/developers/applications/
# Create a webhook in the channel settings of your discord server
bot_token = 'NjMyNzA4OTk4ODEzOTc0NTM4.Xaz-Aw.mO1vi-UsUmYymQ7wVPYjUxa1Aa0' # Bot token (discordapi)
webhook_uri = 'https://discordapp.com/api/webhooks/672039725271613441/JWWMXhka6W9yfaTmMqpXYtFahaGTJ6gmKcSfPAiqvhvP9McAhH3Tp7zTMf4VD9Rapsyc' #Webhook URL (discord client)

check_rate = 10  # How often the bot will check for updates, in minutes (no less than five minutes or you'll be banned from pubg.report)
if __name__ == "__main__":
    client.run(bot_token)
