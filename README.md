
# GoonBot from TarkovPal.com

![Bot Online](https://github.com/user-attachments/assets/b82fdb1a-5f49-463d-aae4-14a1f3b71212)

![Bot Post](https://github.com/user-attachments/assets/b9c68f23-e4bd-4d7b-83e5-9826a0b18aa4)

EFT GoonTracker Discord Bot using Tarkovpal.com API

**This Bot will post every 5 minutes. I recommend muting the channel you have the bot posting to.**

*This documentation is based on the installation of the bot on a Linux Ubuntu 22.04 Server, of which Python is already pre installed*

## Installation

Check that Python is installed
```
python3 -V
```
    
You should get e returned result of the version of Python that is installed.

create a goonbot directory, then go to that directory
```
mkdir ~/goonbot
cd ~/goonbot
```
Obtain a Discord Bot/App token at the following site.

[Discord Developer Login](https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications)

Follow the instructions blow to obtain the token.
*remember this token, but keep it secret as it should not be shared*
```
1. In the Developer portal, click on “Applications”. Log in again and then, back in the “Applications” menu, click on “New Application”.
2. Name the bot and then click “Create”.
3. Go to the “Bot” menu on the left, then click "Reset Token"
4. Copy the token to someplace safe we will need it in the next step
```

Go back to the Linux Host, and in the goonbot directory create a .env file.
```
nano .env
```
Inside the file type out

```
DISCORD_TOKEN=<Insert your generated token here>
```
Save and exit the file

Create a new file named channel_ids.txt
```
nano channel_ids.txt
```
In this file you will input the Channel ID in the discord server that you will be having the bot post to.
For this, you will need to enable developer mode within your server to gather the Channel ID.
Follow the steps here to [Enable Developer Mode](https://support-dev.discord.com/hc/en-us/articles/360028717192-Where-can-I-find-my-Application-Team-Server-ID)

Once Developer mode is turned on, right click on the channel you would like the bot to post to and at the bottom of the menu, you will see 'Copy ID.'

Copy and paste this ID into the channel_ids.txt file and save and exit.

download the goonbot script into the goonbot directory (~/goonbot)
```
wget https://raw.githubusercontent.com/thewikki/GoonBot/main/goonbot.py
```

Add permissions to run the file
```
sudo chmod +x goonbot.py
```

Install [discord.py](https://discordpy.readthedocs.io/en/latest/intro.html)
```
sudo apt install python3-discord
```
Install python-dotenv
```
sudo apt install python3-dotenv
```
Start the script
```
python3 ~/goonbot/goonbot.py
```
*Once started, the script will run until stopped or the Host shutdown*
### Add the Bot to your server
Go to the [Discord Developer Webpage](https://discord.com/developers/applications/1128692617392181349/oauth2)
```
1. click OAuth2
2. Under Scope, select 'bot'
3. Under Bot Permissions, select 'Send Messages,' 'Manage Messages,' 'Manage Threads,' and 'Read Message History.'
4. Leave Integration Type as Guild Install.
5. Copy and Paste the Generated URL into a web browser and add it to your desired server.
```
## Run the GoonBot as a Service(restart when the host is rebooted/always running)
Go to the System directory
```
cd /etc/systemd/system
```
Download the goonbot.service file to this directory.
```
wget https://raw.githubusercontent.com/thewikki/GoonBot/main/goonbot.service
```
Edit the goonbot.service file and replace <user> with the user that you are logged into the host with.

Once the user is updated, save and exit. Then run the following to start
```
sudo systemctl start goonbot.service
```
Then enable the service
```
sudo systemctl enable goonbot.service
```

## Support

For support or use the bot in my discord, join [Here](https://discord.gg/VzUdSqn)
