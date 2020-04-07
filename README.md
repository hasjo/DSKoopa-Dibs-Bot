# DSKoopa-Dibs-Bot
A twitch chat bot to track dibs on DSKoopa's stream

#HOW TO USE
Make a Twitch account and get an OAuth token from a site like https://twitchapps.com/tmi/

Put the token string at like 7, where it says "PUT TOKEN HERE", then the username of the account you made at line 8 where it says "PUT BOT USERNAME HERE". Make sure what you enter is still surrounded by quotation marks. Once that's complete, make sure python3 is installed and run bot.py. The bot should just start up.

#HOW IT WORKS
This bot listens to twitch chat and watches for the dibs emote on DSKoopa's stream. Once it finds one it will display it in the console output. To get the next one, just press Enter on the window. This bot also stores a csv log of all the dibs received as they are received. 
