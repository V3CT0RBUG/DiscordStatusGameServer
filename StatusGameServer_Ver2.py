import discord
from discord.ext import commands
from discord import Colour
import requests
import asyncio

TOKEN = 'YOU_TOKEN_BOT' #Your secret token discord - Get your token in https://discord.com/developers/applications/
API_TYPE = 'battlemetrics'  # use 'battlemetrics' or 'steam'
SERVER_IDS = [23485992]  #ID Server Battlemetrics Example: https://www.battlemetrics.com/servers/rust/23485992  <--- ID Server , you can add more than 1 id example: [23485992,5873087,7172408]
STEAM_SERVERS = [('127.0.0.1', 28015)]  #IP and PORT your server in steamgameserverlist
CHANNEL_ID = 1231231231231231231  #ID Channel Status in your Discord server
STEAM_API_KEY = 'YOU_STEAM_APIKEY' #Your secret SteamApiKey - Get your api in https://steamcommunity.com/dev/apikey

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

estado_messages = {}

@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name}')
    await set_game_status()
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        asyncio.create_task(update_server_statuses(channel))
        asyncio.create_task(update_player_count(channel))

async def set_game_status():
    game = discord.Game("con {} jugadores".format(len(bot.users)))
    await bot.change_presence(activity=game)

async def mostrar_estado_servidor(channel, server_id):
    global estado_messages
    
    response = get_server_info(server_id)

    if response.status_code == 200:
        server_data = response.json().get('data', [])
        if server_data or API_TYPE == 'steam':  # Allow steam response check even if no 'data'
            if API_TYPE == 'battlemetrics':
                server_info = server_data.get('attributes')
                players_online = server_info.get("players")
                max_players = server_info.get('maxPlayers')
                ip_server = server_info.get('ip')
                port_server = server_info.get('port')
                server_name = server_info.get('name')
                status = server_info.get('status')
            else:  # Steam
                servers_list = response.json().get('response', {}).get('servers', [])
                if not servers_list:
                    await channel.send(f'Could not get information from Steam server with IP: {server_id[0]} and port: {server_id[1]}.')
                    return
                server_info = servers_list[0]
                players_online = server_info.get("players")
                max_players = server_info.get('max_players')
                ip_server = server_info.get('addr')
                port_server = server_info.get('gameport')
                server_name = server_info.get('name')
                status = 'online'  # Steam API doesn't provide status directly

            if status.lower() == "offline":
                embed_color = Colour.red()
                status_message = "OFFLINE 🔴"
            elif status.lower() == "online":
                embed_color = Colour.green()
                status_message = "ONLINE 🟢"
            else:
                embed_color = Colour.default()
                status_message = status

            embed = discord.Embed(title='Status Server', color=embed_color)
            embed.add_field(name='Name Server', value=server_name, inline=False)
            embed.add_field(name='Status Server', value=f'**{status_message}**', inline=False)
            embed.add_field(name='Players Online', value=f'{players_online}/{max_players}', inline=False)
            embed.add_field(name='IP Server', value=f'```{ip_server}:{port_server}```', inline=False)
            embed.set_footer(text='© V3CT0RBUG Github 2024', icon_url='https://media.discordapp.net/attachments/1006700409886343200/1142344086544724049/1.jpg')
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1006700409886343200/1142344086544724049/1.jpg")

            if server_id in estado_messages:
                old_status = estado_messages[server_id]['status']
                old_players = estado_messages[server_id]['players']

                if old_status != status_message or old_players != players_online:
                    await estado_messages[server_id]['id'].edit(embed=embed)
                    estado_messages[server_id]['status'] = status_message
                    estado_messages[server_id]['players'] = players_online
                    print(f"Edited message for server {server_id}: {status_message} with {players_online} players")

            else:
                idmessage = await channel.send(embed=embed)
                estado_messages[server_id] = {'message': embed, 'id': idmessage, 'status': status_message, 'players': players_online}
                print(f"Mensaje enviado para el servidor {server_id}: {status_message}")
        else:
            await channel.send(f'Could not get information from server with ID: {server_id}.')
    else:
        await channel.send(f'An error occurred while trying to get information from the server with ID: {server_id}.')

def get_server_info(server):
    if API_TYPE == 'battlemetrics':
        url = f'https://api.battlemetrics.com/servers/{server}'
    else:  # Steam
        ip, port = server
        filter_param = f'\\gameaddr\\{ip}:{port}'
        filter_param_escaped = filter_param.replace('\\', '%5C')
        url = f'https://api.steampowered.com/IGameServersService/GetServerList/v1/?key={STEAM_API_KEY}&filter={filter_param_escaped}'
    # print(f'Requesting server information in URL: {url}')  # Debugging line
    response = requests.get(url)
    # print(f'API Response: {response.text}')  # Debugging line
    return response

async def update_server_statuses(channel):
    while True:
        await asyncio.sleep(20)  #<--- Time refresh in seconds
        servers = SERVER_IDS if API_TYPE == 'battlemetrics' else STEAM_SERVERS
        for server in servers:
            await mostrar_estado_servidor(channel, server)

async def update_player_count(channel):
    while True:
        await asyncio.sleep(20)  #<--- Time refresh in seconds
        servers = SERVER_IDS if API_TYPE == 'battlemetrics' else STEAM_SERVERS
        for server in servers:
            response = get_server_info(server)
            if response.status_code == 200:
                server_data = response.json().get('data', [])
                if server_data or API_TYPE == 'steam':  # Allow steam response check even if no 'data'
                    if API_TYPE == 'battlemetrics':
                        server_info = server_data.get('attributes')
                        players_online = server_info.get("players")
                        max_players = server_info.get('maxPlayers')
                    else:  # Steam
                        servers_list = response.json().get('response', {}).get('servers', [])
                        if not servers_list:
                            await channel.send(f'Could not get information from Steam server with IP: {server[0]} and port: {server[1]}.')
                            return
                        server_info = servers_list[0]
                        players_online = server_info.get("players")
                        max_players = server_info.get('max_players')

                    if server in estado_messages:
                        old_players = estado_messages[server]['players']

                        if old_players != players_online:
                            estado_messages[server]['players'] = players_online
                            embed = estado_messages[server]["message"]

                            embed.set_field_at(2, name='Players Online', value=f'{players_online}/{max_players}', inline=False)
                            await estado_messages[server]["id"].edit(embed=embed)
                            print(f"Edited message for the server {server}: Players online {players_online}/{max_players}")
                else:
                    await channel.send(f'Could not get information from server with ID: {server}.')
            else:
                await channel.send(f'An error occurred while trying to get information from the server with ID: {server}.')

@bot.command()
async def estado(ctx):
    await mostrar_estados_servidores(ctx.channel)

async def mostrar_estados_servidores(channel):
    servers = SERVER_IDS if API_TYPE == 'battlemetrics' else STEAM_SERVERS
    for server in servers:
        await mostrar_estado_servidor(channel, server)

bot.run(TOKEN)
