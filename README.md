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
   git clone https://github.com/V3CT0RBUG/DiscordStatusGameServerBattlemetrics.git
   ``` 
3. Edit StatusGameServer.py 
4. Edit configuration `StatusGameServer.py` or `StatusGameServer_Ver2.py`
   ```python
   TOKEN = 'YOU_TOKEN_BOT' #Your secret token discord - Get your token in https://discord.com/developers/applications/
   API_TYPE = 'battlemetrics'  # use 'battlemetrics' or 'steam'
   SERVER_IDS = [23485992]  #ID Server Battlemetrics Example: https://www.battlemetrics.com/servers/rust/23485992  <--- ID Server , you can add more than 1 id example: [23485992,5873087,7172408]
   STEAM_SERVERS = [('127.0.0.1', 28015)]  #IP and PORT your server in steamgameserverlist
   CHANNEL_ID = 1231231231231231231  #ID Channel Status in your Discord server
   STEAM_API_KEY = 'YOU_STEAM_APIKEY' #Your secret SteamApiKey - Get your api in https://steamcommunity.com/dev/apikey
   ```
5. Start your bot
   ```python
   py StatusGameServer.py
   #or
   py StatusGameServer_Ver2.py
   ```
### Debuggin
1. Check the commented lines
```python
    # print(f'Requesting server information in URL: {url}')  # Debugging line 110
    # print(f'API Response: {response.text}')  # Debugging line 112
   ```
2. Uncomment lines
```python
    print(f'Requesting server information in URL: {url}')  # Debugging line 110
    print(f'API Response: {response.text}')  # Debugging line 112
```
