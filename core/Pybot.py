from async_property import async_property
import discord
from discord.ext import commands
import json
from pathlib import Path
import logging
import os
from utils.mongo import Document
import motor.motor_asyncio
import time
import calendar
import asyncpg

os.environ["SHELL"]="/bin/bash"
import os;os.environ["JISHAKU_NO_UNDERSCORE"]="t"
os.environ["JISHAKU_FORCE_PAGINATOR"]="t"

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

async def get_prefix(Pybot, message):
    if message.author.id == 939887303403405402 or message.author.id == 749559849460826112:
            return commands.when_mentioned_or('')(Pybot, message)
    if not message.guild:
        return commands.when_mentioned_or("-")(Pybot, message)
    try:
        data = await Pybot.db.fetchrow("SELECT * FROM prefix WHERE guild_id = $1", message.guild.id)
        if not data or "prefix" not in data:
            return commands.when_mentioned_or("-")(Pybot, message)
        return commands.when_mentioned_or(data["prefix"])(Pybot, message)
    except:
        return commands.when_mentioned_or("-")(Pybot, message)

intents = discord.Intents.all()

secret_file = json.load(open(cwd+'/config/config.json'))

owners = [749559849460826112, 939887303403405402]

Pybot = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, owner_ids = set(owners), intents=intents, strip_after_prefix=True,)

logging.basicConfig(level=logging.INFO)

Pybot.cwd = cwd

Pybot.config_token = secret_file['token']
Pybot.connection_url = secret_file["mongo"]
Pybot.seen_messages = 0
Pybot.version = '0.1 beta'

Pybot.colors = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}
Pybot.color_list = [c for c in Pybot.colors.values()]
@Pybot.event
async def on_ready():

    print(f"-----\nLogged in as: {Pybot.user.name} : {Pybot.user.id}\n-----\nMy current prefix is: -\n-----")
    await Pybot.change_presence(activity=discord.Game(name=f"Hi, my name is {Pybot.user.name}.\nUse - to interact with me!"))

    Pybot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(Pybot.connection_url))
    Pybot.mongodb = Pybot.mongo["pybot"]
    Pybot.welcomer = Document(Pybot.mongodb, "welcomer")

    
    print("-------------------------\nInitialized Database\n-------------------------")

Pybot.remove_command('help')

@Pybot.event
async def on_message(message):
    Pybot.seen_messages +=1

Pybot.load_extension ('jishaku')

if __name__ == '__main__':
    for file in os.listdir(cwd+"./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            Pybot.load_extension(f"cogs.{file[:-3]}")

async def create_db_pool():
    Pybot.db = await asyncpg.create_pool(database='railway', user='postgres', password='iKfF0EalhC1Oa1AFXira', host='containers-us-west-27.railway.app', port='7301')
    print('-------------------------\nConnected to DataBase\n-------------------------')

Pybot.loop.create_task(create_db_pool())

Pybot.run(Pybot.config_token)