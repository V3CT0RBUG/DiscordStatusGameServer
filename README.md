[![GitHub license](https://img.shields.io/badge/license-Apache-blue.svg)](
https://github.com/V3CT0RBUG/DiscordStatusGameServerBattlemetrics/blob/master/LICENSE)

<h3 align="center">Bot Discord Status Games Server</h3>
<img src="https://i.imgur.com/d2xe7YO.png" align="center" width="50%" height="50%">

### Prerequisites

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
4. Edit configuration `StatusGameServer.py`
   ```python
   TOKEN = 'YOU_TOKEN_BOT' #Your Token bot Discord https://discord.com/developers/
   SERVER_IDS = [23485992] #ID Server Battlemetrics Example: https://www.battlemetrics.com/servers/rust/23485992  <--- ID Server
   CHANNEL_ID = 1231231231231231231 #ID Channel Status
   ```
5. Start your bot
   ```python
   py StatusGameServer.py
   ```
