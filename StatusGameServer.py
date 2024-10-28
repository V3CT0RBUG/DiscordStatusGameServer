import discord
from discord.ext import commands
from discord import Colour
import requests
import asyncio

DEBUG = True  # Use "True" to enable Debug Mode or use "False" to disable Debug Mode
TOKEN = 'YOU_TOKEN_BOT'  # Your secret token discord - Get your token in https://discord.com/developers/applications/
API_TYPE = 'steam'  # use 'battlemetrics', 'steam', 'minecraft_java' or 'minecraft_bedrock'
SERVER_IDS = [23485992]  # ID Server Battlemetrics Example: https://www.battlemetrics.com/servers/rust/23485992
IP_SERVERS = [('127.0.0.1', 25562)]  # IP and PORT your server in steamgameserverlist or minecraft server
CHANNEL_ID = 1231231231231231231  # ID Channel Status in your Discord server
STEAM_API_KEY = 'YOU_STEAM_APIKEY'  # Your secret SteamApiKey - Get your API key in https://steamcommunity.com/dev/apikey

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

player_count_prev = {}

async def set_game_status():
    global player_count_prev
    game = ""
    players_online = 0

    for server in SERVER_IDS if API_TYPE == 'battlemetrics' else IP_SERVERS:
        response = get_server_info(server)
        if response.status_code == 200:
            server_data = response.json().get('data', [])
            if server_data or API_TYPE == 'steam':  # Allow steam response check even if no 'data'
                if API_TYPE == 'battlemetrics':
                    server_info = server_data.get('attributes')
                    players_online = server_info.get("players")
                else:  # Steam
                    servers_list = response.json().get('response', {}).get('servers', [])
                    if not servers_list:
                        continue
                    server_info = servers_list[0]
                    players_online = server_info.get("players")

        elif API_TYPE in ['minecraft_java', 'minecraft_bedrock']:
            # Check for Minecraft servers
            server_info = response.json()
            players_online = server_info.get('players', {}).get('online', 0)

        if DEBUG:   
            print(f"Checking {server} for players online...")

    if players_online == 0:
        game = "No players online"
        if DEBUG:
            print(f"New game status: {game}")
            print(f"Updating game status...")
        await bot.change_presence(activity=discord.Game(name=game))
        if DEBUG:
            print("Updated game status!")
    elif players_online > 0:
        game = f"Playing with {players_online} players"
        if DEBUG:
            print(f"New game status: {game}")
            print(f"Updating game status...")
        await bot.change_presence(activity=discord.Game(name=game))
        if DEBUG:
            print("Updated game status!")

async def update_player_count(channel):
    global player_count_prev
    while True:
        await asyncio.sleep(20)  # Refresh time in seconds
        for server in SERVER_IDS if API_TYPE == 'battlemetrics' else IP_SERVERS:
            response = get_server_info(server)
            if response.status_code == 200:
                server_data = response.json().get('data', [])
                if server_data or API_TYPE == 'steam':  # Allow steam response check even if no 'data'
                    if API_TYPE == 'battlemetrics':
                        server_info = server_data.get('attributes')
                        players_online = server_info.get("players")
                    else:  # Steam
                        servers_list = response.json().get('response', {}).get('servers', [])
                        if not servers_list:
                            continue
                        server_info = servers_list[0]
                        players_online = server_info.get("players")

                    if server in player_count_prev:
                        if player_count_prev[server] != players_online:
                            print(f"Player count changed for {server}: {players_online} (from {player_count_prev[server]})")
                            player_count_prev[server] = players_online
                            await set_game_status()
                    else:
                        if DEBUG:
                            print(f"Initial player count for {server}: {players_online}")  # Debugging line
                        player_count_prev[server] = players_online
        await set_game_status()

async def mostrar_estado_servidor(channel, server_id):
    global estado_messages

    response = get_server_info(server_id)

    if response.status_code == 200:
        server_data = response.json().get('data', [])
        if server_data or API_TYPE == 'steam' or API_TYPE in ['minecraft_java', 'minecraft_bedrock']:  # Allow steam response check even if no 'data'
            if API_TYPE == 'battlemetrics':
                server_info = server_data.get('attributes')
                players_online = server_info.get("players")
                max_players = server_info.get('maxPlayers')
                ip_server = server_info.get('ip')
                port_server = server_info.get('port')
                server_name = server_info.get('name')
                status = server_info.get('status')
            elif API_TYPE == 'minecraft_java' or API_TYPE == 'minecraft_bedrock':
                # Extract Minecraft server information
                server_info = response.json()
                players_online = server_info.get('players', {}).get('online', 0)
                max_players = server_info.get('players', {}).get('max', 0)
                ip_server = server_info.get('ip')
                port_server = server_info.get('port')
                server_name = server_info.get('hostname', 'Desconocido')
                status = 'online' if server_info.get('online') else 'offline'

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
    elif API_TYPE in ['minecraft_java', 'minecraft_bedrock']:
        # For Minecraft servers
        ip, port = server
        if API_TYPE == 'minecraft_java':
            url = f'https://api.mcsrvstat.us/3/{ip}:{port}'
        else:  # Bedrock
            url = f'https://api.mcsrvstat.us/bedrock/3/{ip}:{port}'
    else:  # Steam
        ip, port = server
        filter_param = f'\\gameaddr\\{ip}:{port}'
        filter_param_escaped = filter_param.replace('\\', '%5C')
        url = f'https://api.steampowered.com/IGameServersService/GetServerList/v1/?key={STEAM_API_KEY}&filter={filter_param_escaped}'
    if DEBUG:   
        print(f'Requesting server information in URL: {url}')  # Debugging line
    response = requests.get(url)
    if DEBUG:
        print(f'API Response: {response.text}')  # Debugging line
    return response

async def update_server_statuses(channel):
    while True:
        await asyncio.sleep(20)  #<--- Time refresh in seconds
        servers = SERVER_IDS if API_TYPE == 'battlemetrics' else IP_SERVERS
        for server in servers:
            await mostrar_estado_servidor(channel, server)

@bot.command()
async def players(ctx):
    await mostrar_estado_servidores(ctx.channel)

async def mostrar_estado_servidores(channel):
    servers = SERVER_IDS if API_TYPE == 'battlemetrics' else IP_SERVERS
    for server in servers:
        response = get_server_info(server)
        if response.status_code == 200:
            server_data = response.json().get('data', [])
            if server_data or API_TYPE == 'steam' or API_TYPE in ['minecraft_java', 'minecraft_bedrock']:  # Allow steam response check even if no 'data'
                if API_TYPE == 'battlemetrics':
                    server_info = server_data.get('attributes')
                    players_online = server_info.get("players")
                elif API_TYPE in ['minecraft_java', 'minecraft_bedrock']:
                    server_info = response.json()
                    players_online = server_info.get('players', {}).get('online', 0)
                else:  # Steam
                    servers_list = response.json().get('response', {}).get('servers', [])
                    if not servers_list:
                        await channel.send(f'Could not get information from Steam server with IP: {server[0]} and port: {server[1]}.')
                        return
                    server_info = servers_list[0]
                    players_online = server_info.get("players")
                await channel.send(f'**Server {server}: {players_online} players online**')
            else:
                await channel.send(f'Could not get information from server with ID: {server}.')
        else:
            await channel.send(f'An error occurred while trying to get information from the server with ID: {server}.')

@bot.command()
async def server(ctx):
    if not ctx.guild:
        await ctx.send('Este comando solo puede ser utilizado en un canal de servidor.')
    else:
        try:
            server_id = ctx.guild.id
            await mostrar_estado_servidor(ctx.channel, server_id)
        except Exception as e:
            await ctx.send(f'Error: {str(e)}')

async def main():
    async with bot:
        await bot.start(TOKEN)

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
