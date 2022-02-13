import discord
from discord.ext import commands
import json
from pathlib import Path
import logging
import os

os.environ["SHELL"]="/bin/bash"
import os;os.environ["JISHAKU_NO_UNDERSCORE"]="t"
os.environ["JISHAKU_FORCE_PAGINATOR"]="t"

def __init__(self, bot):
        self.bot = bot
        
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("-")(bot, message)
    try:
        data = await bot.prefix.find(message.guild.id)
        if message.author.id == 939887303403405402 or message.author.id == 749559849460826112:
            return commands.when_mentioned_or('')(bot, message)
        if not data or "prefix" not in data:
            return commands.when_mentioned_or("-")(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or("-")(bot, message)

intents = discord.Intents.all()

secret_file = json.load(open(cwd+'/config/config.json'))

owners = [749559849460826112, 939887303403405402]

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_ids = set(owners), intents=intents)

logging.basicConfig(level=logging.INFO)

bot.cwd = cwd

bot.config_token = secret_file['token']
bot.connection_url = secret_file["mongo"]

bot.version = '0.1 beta'

bot.colors = {
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
bot.color_list = [c for c in bot.colors.values()]

if __name__ == '__main__':

    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

bot.run(bot.config_token)