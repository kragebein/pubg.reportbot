#!/usr/bin/python3.6
''' pubg report bot'''

import discord, logging
from bot.main import client as client
logging.basicConfig(level=logging.INFO)

# Create an API key here: https://discordapp.com/developers/applications/
bot_token = '' # Bot token (discordapi)

# Create Webhook under channel settings, it looks like this:
# https://discordapp.com/api/webhooks/67203972522511613441/JWWMXhka6W9yfaTmMqpXYtFahaGHh3hasgmKcSfPAiqvhvP9Masd23H3Tp7zTMf4VD9Rapsyc
#                                        Webhook                            Webhook Token
webhook_token = '' # Webhook token
webhook = '' # Webhook ID
check_rate = 5  # How often the bot will check for updates, in minutes (no less than five minutes or you'll be banned from pubg.report)

if __name__ == "__main__":
    client.run(bot_token)
