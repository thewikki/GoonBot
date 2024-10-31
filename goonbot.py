import requests
from datetime import datetime
import pytz
import discord
from discord.ext import commands, tasks
from discord import Embed, File
import json
import os
from dotenv import load_dotenv
import logging

# Load environment variables from the .env file
load_dotenv()

# Get the Discord token from the environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

API_URL = 'https://tarkovpal.com/api'
TIMEZONE = 'America/Chicago'
CHANNEL_FILE = 'channel_ids.txt'

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Adjust to DEBUG for more details
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

channel_ids = []
current_map = "N/A"

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Tracking updates..."))
    load_channel_ids()
    track_updates.start()

@tasks.loop(minutes=5)
async def track_updates():
    global current_map
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        logging.info("Successfully fetched data from API.")

        current_map = data.get('Current Map', ['N/A'])[0]
        await bot.change_presence(activity=discord.Game(name=f"{current_map}"))

        times = data.get('Time', [])

        for channel_id in channel_ids:
            channel = bot.get_channel(channel_id)
            if channel is None:
                logging.warning(f"Failed to find channel with ID {channel_id}")
                continue

            # Check if the bot has permission to manage messages
            permissions = channel.permissions_for(channel.guild.me)
            if not permissions.manage_messages:
                logging.warning(f"Missing Manage Messages permission in channel {channel_id}")
                continue

            # Remove previous messages by custom purge method
            await custom_purge(channel, limit=10)

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

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")

# Custom purge method to delete messages one by one
async def custom_purge(channel, limit=10):
    messages = []
    async for message in channel.history(limit=limit):
        messages.append(message)

    for message in messages:
        if message.author == bot.user:
            try:
                await message.delete()
            except discord.errors.Forbidden:
                logging.warning(f"Failed to delete message {message.id} due to missing permissions")

@bot.command()
async def track(ctx, channel_id_param=None):
    if channel_id_param is not None:
        channel_id = int(channel_id_param)
        if channel_id not in channel_ids:
            channel_ids.append(channel_id)
            save_channel_ids()
            await ctx.send(f"Tracking updates in channel ID: {channel_id}")
            logging.info(f"Added channel {channel_id} to tracking list.")
        else:
            await ctx.send(f"Channel ID {channel_id} is already being tracked.")
            logging.info(f"Channel ID {channel_id} is already tracked.")
    else:
        await ctx.send("Please provide a channel ID.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Use !track to track the current map.")
        logging.warning("Invalid command used.")

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
        logging.info("Image downloaded successfully.")
        return 'map_image.png'
    except Exception as e:
        logging.error(f"Failed to download image: {e}")
        return None

def save_channel_ids():
    with open(CHANNEL_FILE, 'w') as file:
        file.write('\n'.join(map(str, channel_ids)))
    logging.info("Channel IDs saved successfully.")

def load_channel_ids():
    global channel_ids
    try:
        with open(CHANNEL_FILE, 'r') as file:
            channel_ids = [int(line.strip()) for line in file.readlines()]
        logging.info("Channel IDs loaded successfully.")
    except FileNotFoundError:
        channel_ids = []
        logging.warning("Channel file not found; starting with an empty list.")

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
    logging.info("Bot connected.")

bot.run(TOKEN)
