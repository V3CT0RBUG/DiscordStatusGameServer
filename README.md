[![GitHub license](https://img.shields.io/badge/license-Apache-blue.svg)](
https://github.com/V3CT0RBUG/DiscordStatusGameServerBattlemetrics/blob/master/LICENSE)

<h3 align="center">Bot Discord Status Games Server</h3>
<img src="https://i.imgur.com/d2xe7YO.png" align="center" width="50%" height="50%">

### Prerequisites

* python used 3.7

* pip
  ```sh
  pip install discord.py
  pip install requests
  pip install asyncio
  ```
* You need to have your server registered in https://www.battlemetrics.com/servers/add

### Installation
1. Open your account in https://discord.com/developers/
2. Clone the repo
   ```sh
   git clone https://github.com/V3CT0RBUG/DiscordStatusGameServer.git
   ``` 
3. Edit StatusGameServer.py 
4. Edit configuration `StatusGameServer.py`
   ```python
   DEBUG = True  # Use "True" to enable Debug Mode or "False" to disable Debug Mode
   TOKEN = 'YOUR_BOT_TOKEN'  # Your Discord bot token - Get it from https://discord.com/developers/applications/
   API_TYPE = 'steam'  # Use 'battlemetrics', 'steam', 'minecraft_java' or 'minecraft_bedrock'
   SERVER_IDS = [23485992]  # BattleMetrics Server ID Example: https://www.battlemetrics.com/servers/rust/23485992
   IP_SERVERS = [('127.0.0.1', 25562)]  # IP and PORT of your server in Steam Game Server List or Minecraft server
   CHANNEL_ID = 1231231231231231231  # ID of the status channel in your Discord server
   STEAM_API_KEY = 'YOUR_STEAM_API_KEY'  # Your Steam API Key - Get it from https://steamcommunity.com/dev/apikey

   ```
5. Start your bot
   ```python
   py StatusGameServer.py
   ```
### Debuggin
1. Change False to True to enable debug mode
```python
    DEBUG = False
   ```
