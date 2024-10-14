# GoonBot
EFT GoonTracker Discord Bot 
** This Bot will post every 5 minutes. If you do not have something else to remove the other messages, it will just continue to post to the discord channel. I recommend looking up AutoDelete as another bot to run side by side with this one. The reports for this bot depend on the reporting and API from tarkovpal.com.

I currently have the bot running on a Linux Ubuntu 22.04 Server. 

- Create a directory named goonbot in the Home Directory.
- Download the goonbot.py file to ~/goonbot directory. 
- Create a file at ~ and name it channel_ids.txt
    - Input the Channel ID from the discord channel you want this bot to post in and place it in the channel_ids.txt file, then save that file.  https://support-dev.discord.com/hc/en-us/articles/360028717192-Where-can-I-find-my-Application-Team-Server-ID
 

Running as a Service:
- go to /etc/systemd/system
- download the goonbot_service.txt file to that location
- type 'sudo systemctl start goonbot'
- type 'sudo systemctl enable goonbot' (this will allow the service to restart with the reboot/restart of the host)






Discord Developer Tools 
https://discord.com/developers/docs/developer-tools/game-sdk
Discord Developer Site
https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications
How to Enable Developer Mode in Discord and find your Channel ID
https://support-dev.discord.com/hc/en-us/articles/360028717192-Where-can-I-find-my-Application-Team-Server-ID
