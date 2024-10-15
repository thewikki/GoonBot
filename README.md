# GoonBot
EFT GoonTracker Discord Bot 
** This Bot will post every 5 minutes. I recommend muting the channel you have the bot posting to. The reports for this bot depend on the reporting and API from tarkovpal.com.

I currently have the bot running on a Linux Ubuntu 22.04 Server. 

Python comes pre installed on various versions of Linux.

run ```python3 -V``` to check the version of Python installed. If it is not installed, you will need to install Python to the system.

Create a goonbot directory
```mkdir goonbot```

create a .env file for the discord token
```nano .env```  how to get the discord token https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications
How to make your own Discord bot:

    Turn on “Developer mode” in your Discord account.
    Click on “Discord API”.
    In the Developer portal, click on “Applications”. Log in again and then, back in the “Applications” menu, click on “New Application”.
    Name the bot and then click “Create”.
    Go to the “Bot” menu and generate a token using “Add Bot”.
    Program your bot using the bot token and save the file.
    Define other details for your bot under “General Information”.
    Click on “OAuth2”, activate “bot”, set the permissions, and then click on “Copy”.
    Select your server to add your bot to it.

DISCORD_TOKEN=(insert discord token here) **Do not give out your Bot Token**

create a file named channel_ids.txt
```nano channel_ids.txt```
Right click on the channel you want the bot to post to, then click copy id. Enter just the ID into the file and save and exit the file. 
https://support-dev.discord.com/hc/en-us/articles/360028717192-Where-can-I-find-my-Application-Team-Server-ID

Download the goonbot.py file into the goonbot directory
```wget https://github.com/thewikki/GoonBot/blob/main/goonbot.py```

add permission to run the file
```sudo chmod +x goonbot.py```


install discord.py (https://discordpy.readthedocs.io/en/latest/intro.html)
```sudo apt install python3-discord```

isntall python-dotenv
```sudo apt install python3-dotenv```

add the bot to your discord server.
go into the discord dev site 
https://discord.com/developers/applications/1128692617392181349/oauth2

Click OAuth2 on the left side.
The Scope = bot
Bot Permissions = send messages, manage messages, manage threads, read message hisory.

ensure Integration type is set to Guild Install

Copy and paste the generated URL into a web browser and then add to the desired server.

## To Make the bot run as a service(restart when the host is rebooted/always running)
go to the system directory
```cd /etc/systemd/system```
download the goonbot.service file to this directory
```wget https://github.com/thewikki/GoonBot/blob/main/goonbot.service```

edit the goonbot.service file 
```sudo nano goonbot.service```
you will need to edit the <user> out and input what the username you are logged in with as.

Once the user has been set, save and exit then run the following to start and enable the service
```sudo systemctl start goonbot.service```
```sudo systemctl enable goonbot.service```
