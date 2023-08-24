import discord
from discord.ext import commands
from discord import Colour
import requests
import asyncio

TOKEN = 'YOU_TOKEN_BOT'
SERVER_IDS = [23485992] #ID Server Battlemetrics Example: https://www.battlemetrics.com/servers/rust/23485992  <--- ID Server
CHANNEL_ID = 1231231231231231231 #ID Channel Status

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
        if server_data:
            server_info = server_data.get('attributes')
            players_online = server_info.get("players")
            max_players = server_info.get('maxPlayers')
            ip_server = server_info.get('ip')
            port_server = server_info.get('port')
            server_name = server_info.get('name')
            status = server_info.get('status')

            if status.lower() == "offline":
                embed_color = Colour.red()
                status_message = "OFFLINE 🔴"
            elif status.lower() == "online":
                embed_color = Colour.green()
                status_message = "ONLINE 🟢"
            else:
                embed_color = Colour.default()
                status_message = status

            embed = discord.Embed(title='Estado del Servidor', color=embed_color)
            embed.add_field(name='Nombre del servidor', value=server_name, inline=False)
            embed.add_field(name='Estado del servidor', value=f'**{status_message}**', inline=False)
            embed.add_field(name='Jugadores en línea', value=f'{players_online}/{max_players}', inline=False)
            embed.add_field(name='IP Server', value=f'```{ip_server}:{port_server}```', inline=False)
            embed.set_footer(text='© V3CT0RBUG Github 2023', icon_url='https://media.discordapp.net/attachments/1006700409886343200/1142344086544724049/1.jpg')
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1006700409886343200/1142344086544724049/1.jpg")

            if server_id in estado_messages:
                old_status = estado_messages[server_id]['status']

                if old_status != status_message:
                    await estado_messages[server_id]['id'].edit(embed=embed)
                    estado_messages[server_id]['status'] = status_message
                    print(f"Mensaje editado para el servidor {server_id}: {status_message}")

                await update_player_count(channel)
            else:
                idmessage = await channel.send(embed=embed)
                estado_messages[server_id] = {'message': embed,'id':idmessage, 'status': status_message, 'players': players_online}
                print(f"Mensaje enviado para el servidor {server_id}: {status_message}")
        else:
            await channel.send(f'No se pudo obtener información del servidor con ID: {server_id}.')
    else:
        await channel.send(f'Ocurrió un error al intentar obtener información del servidor con ID: {server_id}.')

def get_server_info(server_id):
    url = f'https://api.battlemetrics.com/servers/{server_id}'
    response = requests.get(url)
    return response

async def update_server_statuses(channel):
    while True:
        await asyncio.sleep(120) #<--- Time refresh in seconds
        for server_id in SERVER_IDS:
            await mostrar_estado_servidor(channel, server_id)

async def update_player_count(channel):
    while True:
        await asyncio.sleep(10) #<--- Time refresh in seconds
        for server_id in SERVER_IDS:
            response = get_server_info(server_id)
            if response.status_code == 200:
                server_data = response.json().get('data', [])
                if server_data:
                    server_info = server_data.get('attributes')
                    players_online = server_info.get("players")
                    max_players = server_info.get('maxPlayers')
                    
                    if server_id in estado_messages:
                        old_players = estado_messages[server_id]['players']

                        if old_players != players_online:
                          
                            estado_messages[server_id]['players'] = players_online
                            embed = estado_messages[server_id]["message"]
                         
                            embed.set_field_at(2, name='Jugadores en línea', value=f'{players_online}/{max_players}', inline=False)
                            await estado_messages[server_id]["id"].edit(embed=embed)
                            print(f"Mensaje editado para el servidor {server_id}: Jugadores en línea {players_online}/{max_players}")
                else:
                    await channel.send(f'No se pudo obtener información del servidor con ID: {server_id}.')
            else:
                await channel.send(f'Ocurrió un error al intentar obtener información del servidor con ID: {server_id}.')

@bot.command()
async def estado(ctx):
    await mostrar_estados_servidores(ctx.channel)

async def mostrar_estados_servidores(channel):
    for server_id in SERVER_IDS:
        await mostrar_estado_servidor(channel, server_id)

bot.run(TOKEN)