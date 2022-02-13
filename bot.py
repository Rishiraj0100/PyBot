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

os.environ["SHELL"]="/bin/bash"
import os;os.environ["JISHAKU_NO_UNDERSCORE"]="t"
os.environ["JISHAKU_FORCE_PAGINATOR"]="t"

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

bot = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, owner_ids = set(owners), intents=intents)

logging.basicConfig(level=logging.INFO)

bot.cwd = cwd

bot.config_token = secret_file['token']
bot.connection_url = secret_file["mongo"]
bot.seen_messages = 0
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
@bot.event
async def on_ready():

    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: -\n-----")
    await bot.change_presence(activity=discord.Game(name=f"Hi, my name is {bot.user.name}.\nUse - to interact with me!"))

    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["pybot"]
    bot.afk = Document(bot.db, "afk")
    bot.prefix = Document(bot.db, "prefix")
    bot.blacklist = Document(bot.db, "blacklist")
    bot.welcomer = Document(bot.db, "welcomer")

    
    print("-------------------------\nInitialized Database\n-------------------------")

bot.remove_command('help')
@bot.event
async def on_message(message):
    bot.seen_messages += 1

    if message.author.id == bot.user.id:
        return

    data = await bot.blacklist.find_by_id(message.author.id)
    if data:
        return

    if message.content.startswith('#'):
        return

    data = await bot.afk.get_by_id(message.author.id)
    if not data or "afk" not in data:
        pass
    else:
        if "guild" not in data:
            pass
        else:
            if message.guild.id != data["guild"]:
                return await bot.process_commands(message)
        await bot.afk.delete(message.author.id)
        
        try:
            a = message.author.nick
            a = a.replace('[AFK]', '')
            a = a.replace('AFK', '')
            await message.author.edit(nick=f'{a}')
        except:
            pass
        if len(data["ping"]) == 0:
            pmsg  = '\n**You were not pinged while you were AFK.**'
        elif len(data["ping"]) == 1:
            pmsg = f'**You were pinged {len(data["ping"])} time.\n\nClick Below to View them.**'
        else:
            pmsg = f'**You were pinged {len(data["ping"])} times.\n\nClick Below to View them.**'
        obj = time.gmtime(data["time"])
        epoch = time.asctime(obj)
        ab = calendar.timegm(time.strptime(f'{epoch} UTC', '%a %b %d %H:%M:%S %Y UTC'))
        embed = discord.Embed(color=0x3498DB, description=f'Welcome Back **{message.author}**, I have removed your AFK.\nYou had gone afk <t:{ab}:R>\n{pmsg}')
        view = discord.ui.View()
        # i = 0
        for link in data["ping"]:
            but = discord.ui.Button(url=link, label='Go to Message')
            view.add_item(but)
            # i+=1
        if not view:
            view = None
        await message.channel.send(embed=embed, view=view)
    a = None
    if message.content.startswith('#'):
            return
    res = message.content.split()
    for word in res:
        if word.startswith('<@!'):
            a = word
    if a:
        a = a.replace('<@!','')
        a = a.replace('>', '')
        a = int(a)
        try:
            aa = await bot.fetch_user(a)
            name = aa
        except:
            name = 'User'
        afk = await bot.afk.get_by_id(a)

        if not afk or "afk" not in afk:
            pass
        else:
            if "reason" not in afk:
                reason = 'I am AFK :)'
            else:
                reason = afk["reason"]
            if message.guild.id != afk["guild"]:
                return

            obj = time.gmtime(afk["time"])
            epoch = time.asctime(obj)
            ab = calendar.timegm(time.strptime(f'{epoch} UTC', '%a %b %d %H:%M:%S %Y UTC'))
            await message.reply(f'**{name}** went afk <t:{ab}:R> : {reason}')
            l = afk["ping"]
            if not l:
                l = []
            l.append(f'https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}')
            await bot.afk.upsert({"_id": a, "ping": l})

    if f'<@!{bot.user.id}' in message.content:
        for command in bot.commands:
            if command.name.lower() in message.content.lower():
                break
        else:
            for command in bot.commands:
                for aliases in command.aliases:
                    if aliases.lower() in message.content.lower():
                        break
            else:
                data = await bot.prefix.get_by_id(message.guild.id)
                if not data or "prefix" not in data:
                    prefix = "-"
                else:
                    prefix = data["prefix"]
                await message.channel.send(f"My prefix here is `{prefix}` \nI was developed by `Jash_2312` & `Anshuman..!!#5404`", delete_after=10)
    await bot.process_commands(message)

bot.load_extension ('jishaku')

if __name__ == '__main__':

    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

bot.run(bot.config_token)