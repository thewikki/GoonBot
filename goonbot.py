import requests
from datetime import datetime
import pytz
import discord
from discord.ext import commands, tasks
from discord import Embed, File
import json

TOKEN = 'Discord token here'  # Replace with your Discord bot token
API_URL = 'https://tarkovpal.com/api'  # Replace with your API endpoint URL
TIMEZONE = 'America/Chicago'  # Set the timezone to 'America/Chicago' for Dallas, TX (CST)
CHANNEL_FILE = 'channel_ids.txt'  # Path to the text file containing channel IDs

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

channel_ids = []
current_map = "N/A"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Tracking updates..."))
    load_channel_ids()
    track_updates.start()

@tasks.loop(minutes=5)
async def track_updates():
    global current_map
    response = requests.get(API_URL)
    data = response.json()  # Assuming the API response is in JSON format

    current_map = data.get('Current Map', ['N/A'])[0]
    await bot.change_presence(activity=discord.Game(name=f"{current_map}"))

    times = data.get('Time', [])

    for channel_id in channel_ids:
        channel = bot.get_channel(channel_id)
        if channel is None:
            print(f"Failed to find channel with ID {channel_id}")
            continue

        embed = Embed(title="Goons, Where are you?", color=discord.Color.dark_red())
        embed.add_field(name="Current Location", value=f"[{current_map}](https://tarkovpal.com)", inline=False)

        for reported_time in times:
            datetime_object = datetime.strptime(reported_time, '%B %d, %Y, %I:%M %p')
            datetime_object = pytz.timezone(TIMEZONE).localize(datetime_object)
            current_time = datetime.now(pytz.timezone(TIMEZONE))
            time_difference = current_time - datetime_object

            last_seen = f"{int(time_difference.total_seconds() / 60 * -1)} minutes ago"
            embed.add_field(name="Last Seen", value=last_seen, inline=False)

        embed.add_field(name="Bot Data", value="provided from TarkovPal.com")

        image_url = get_map_image_url(current_map.lower())
        image_file = await download_image(image_url)

        if image_file is not None:
            file = File(image_file, filename='map_image.png')
            embed.set_image(url=f'attachment://map_image.png')
            await channel.send(file=file, embed=embed)
        else:
            await channel.send(embed=embed)

@bot.command()
async def track(ctx, channel_id_param=None):
    if channel_id_param is not None:
        channel_id = int(channel_id_param)
        if channel_id not in channel_ids:
            channel_ids.append(channel_id)
            save_channel_ids()
            await ctx.send(f"Tracking updates in channel ID: {channel_id}")
        else:
            await ctx.send(f"Channel ID {channel_id} is already being tracked.")
    else:
        await ctx.send("Please provide a channel ID.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Use !track to track the current map.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

async def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open('map_image.png', 'wb') as file:
            file.write(response.content)
        return 'map_image.png'
    except Exception as e:
        print(f"Failed to download image: {e}")
        return None

def save_channel_ids():
    with open(CHANNEL_FILE, 'w') as file:
        file.write('\n'.join(map(str, channel_ids)))

def load_channel_ids():
    global channel_ids
    try:
        with open(CHANNEL_FILE, 'r') as file:
            channel_ids = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        channel_ids = []

def get_map_image_url(map_name):
    map_images = {
        'customs': 'https://tarkovpal.com/img/Customs2.png',
        'shoreline': 'https://tarkovpal.com/img/Shoreline2.png',
        'lighthouse': 'https://tarkovpal.com/img/Lighthouse2.png',
        'woods': 'https://tarkovpal.com/img/Woods2.png',
        'factory': 'https://tarkovpal.com/img/Factory2.png'
    }
    return map_images.get(map_name, '')

@bot.event
async def on_connect():
    await bot.change_presence(activity=discord.Game(name="Tracking updates..."))

bot.run(TOKEN)
