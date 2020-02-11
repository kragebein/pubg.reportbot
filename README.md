# pubg.report discord bot

  

A bot that will announce your kill/you being killed in pubg to your discord channel with video from your enemies point of view via their Twitchstream.

**How to download:**

> git clone https://github.com/kragebein/pubg.reportbot.git

or

> click here: https://github.com/kragebein/pubg.reportbot/archive/master.zip


**Setup:**

> pip3 install -f requirements.txt

To run the bot you need the following:

* A discord API key, you can get that here:
https://discordapp.com/developers/applications/
* A webhook. This you can get in the settings of a text channel. 
	
In the file pubgbot.py you will find these settings: 
>  bot_token =  ''  # Api key 

>  webhook_uri =  ''  #Webhook URL 

>  check_time = 10 # How often the bot will check for updates, in minutes (no less than ten minutes or you'll be banned from pubg.report)

Please update them accordingly.

*Please make sure to have check_time above 10. Setting it to below 10 minutes will result in a ban from pubg.report*

**To start the bot:**
> python3.6 pubgbot.py

Bot is still under development, further debugging and testing is necessary.

*Also, after the first time you register, the bot will announce -all- clips up to this date, after the first loop, it will only announce the latest clip. Can be expedited by using :*

>!test playername

![Example](https://i.imgur.com/LNEESew.png)
  

Just note: The match must be ended before the clips will show up. Even if you are the first to die, the clips will not be available until the game has had its Chicken Dinner. 