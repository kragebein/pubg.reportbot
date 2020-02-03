
# pubg.report discord bot

A bot that will announce your kill/you being killed in pubg to your discord channel, with video. 

Setup:
> pip discord sqlite3 requests json

usage:
> !register playername

> !unregister playername

Once registered with the bot, the bot will loop through the list of players in the database and look for kills through pubg.report and announce that event in your preferred discord channel. 
![Example](https://i.imgur.com/LNEESew.png)

To set up the bot you will need two things:
A discord API key, you can get that here: 
https://discordapp.com/developers/applications/

And a webhook, this you can find under channel settings. 
Edit the pubgbot.py file with the webhook and the bot token. 

Bot is still under development, further debugging and testing is required. 

*Also, after the first time you register, the bot will announce -all- clips up to this date, after the first loop, it will only announce the latest clip. Can be expedited by using :*
>!test playername 






  
