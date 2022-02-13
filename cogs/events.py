import discord
from discord.ext import commands
from urllib.request import urlopen
import time, calendar

class Events(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print("Events Cog has been loaded\n-------------------------")
        
        @commands.Cog.listener()
        async def on_message(self, message):
            self.bot.seen_messages += 1

            if message.author.id == self.bot.user.id:
                return

            data = await self.bot.blacklist.find_by_id(message.author.id)
            if data:
                return

            if message.content.startswith('#'):
                return

            data = await self.bot.afk.get_by_id(message.author.id)
            if not data or "afk" not in data:
                pass
            else:
                if "guild" not in data:
                    pass
                else:
                    if message.guild.id != data["guild"]:
                        return await self.bot.process_commands(message)
                await self.bot.afk.delete(message.author.id)
                
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
                    aa = await self.bot.fetch_user(a)
                    name = aa
                except:
                    name = 'User'
                afk = await self.bot.afk.get_by_id(a)

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
                    await self.bot.afk.upsert({"_id": a, "ping": l})

            if f'<@!{self.bot.user.id}' in message.content:
                for command in self.bot.commands:
                    if command.name.lower() in message.content.lower():
                        break
                else:
                    for command in self.bot.commands:
                        for aliases in command.aliases:
                            if aliases.lower() in message.content.lower():
                                break
                    else:
                        data = await self.bot.prefix.get_by_id(message.guild.id)
                        if not data or "prefix" not in data:
                            prefix = "-"
                        else:
                            prefix = data["prefix"]
                        await message.channel.send(f"My prefix here is `{prefix}` \nI was developed by `Jash_2312` & `Anshuman..!!#5404`", delete_after=10)
            await self.bot.process_commands(message)

        @commands.Cog.listener()
        async def on_member_join(self, member):
            data = await self.bot.welcomer.get_by_id(member.guild.id)
            if data["autorole"] == True and data["autorole_human"] != 0:
                if not member.bot:
                    try:
                        role = member.guild.get_role(data["autorole_human"])
                        await member.add_roles(role, reason='Pybot\'s Autorole')
                    except:
                        pass
            if data["autorole"] == True and data["autorole_bot"] != 0:
                if data["autorole_bot"] != 0:
                    if member.bot:
                        role = member.guild.get_role(data["autorole_bot"])
                        await member.add_roles(role, reason='Pybot\'s Autorole')

            if data["type"] == 'message' and data["message"] != 'none' and data["channel"] != 0 and data["welcomer"] == True:
                if not member.bot:
                    a = data["message"]
                    a = a.replace('{user}', f'{member.mention}')
                    a = a.replace('{username}', f'{member.name}')
                    a = a.replace('{server}', f'{member.guild.name}')
                    channel = member.guild.get_channel(data["channel"])
                    await channel.send(a)
    
            elif data["type"] == 'embed' and data["channel"] != 0 and data["welcomer"] == True:
                channel = member.guild.get_channel(data["channel"])

                title = data["title"]
                title = title.replace('{user}', f'{member.name}')
                title = title.replace('{username}', f'{member.name}')
                title = title.replace('{server}', f'{member.guild.name}')

                description = data["description"]
                description = description.replace(
                    '{user}', f'{member.mention}')
                description = description.replace(
                    '{username}', f'{member.name}')
                description = description.replace(
                        '{server}', f'{member.guild.name}')

                footer = data["footer"]
                footer = footer.replace('{user}', f'{member.name}')
                footer = footer.replace('{username}', f'{member.name}')
                footer = footer.replace('{server}', f'{member.guild.name}')

                if data["title"].lower() == "none" and data["description"].lower() == "none":
                    embed = discord.Embed(color=discord.Color.blue())
                    try:
                        if data["image"].lower() != 'none':
                            image_formats = ("image/png", "image/jpeg", "image/gif")
                            url = f'{data["image"]}'
                            site = urlopen(url)
                            meta = site.info()
                            if meta["content-type"] in image_formats:
                                embed.set_image(url=data["image"])
                    except:
                        pass
                    try:
                        if data["thumbnail"].lower() != 'none':
                            image_formats = ("image/png", "image/jpeg", "image/gif")
                            url = f'{data["thumbnail"]}'
                            site = urlopen(url)
                            meta = site.info()
                            if meta["content-type"] in image_formats:
                                embed.set_thumbnail(url=data["thumbnail"])
                    except:
                        pass
                    try:
                        if data["footer"].lower() != 'none':
                            embed.set_footer(text=footer)
                    except:
                        pass
                    try:
                        await channel.send(embed=embed)
                    except:
                        pass
                elif data["title"].lower() != "none" and data["description"].lower() != "none":
                    embed = discord.Embed(
                        color=discord.Color.blue(), title=title, description=description)
                    try:
                        if data["image"].lower() != 'none':
                            image_formats = ("image/png", "image/jpeg", "image/gif")
                            url = f'{data["image"]}'
                            site = urlopen(url)
                            meta = site.info()
                            if meta["content-type"] in image_formats:
                                embed.set_image(url=data["image"])
                    except:
                        pass
                    try:
                        if data["thumbnail"].lower() != 'none':
                            image_formats = ("image/png", "image/jpeg", "image/gif")
                            url = f'{data["thumbnail"]}'
                            site = urlopen(url)
                            meta = site.info()
                            if meta["content-type"] in image_formats:
                                embed.set_thumbnail(url=data["thumbnail"])
                    except:
                        pass
                    try:
                        if data["footer"].lower() != 'none':
                            embed.set_footer(text=footer)
                    except:
                        pass
                    try:
                        await channel.send(embed=embed)
                    except:
                        pass
                elif data["title"].lower() != "none" and data["description"].lower() == "none":
                    embed = discord.Embed(
                        color=discord.Color.blue(), title=title)
                    try:
                        if data["image"].lower() != 'none':
                            image_formats = ("image/png", "image/jpeg", "image/gif")
                            url = f'{data["image"]}'
                            site = urlopen(url)
                            meta = site.info()
                            if meta["content-type"] in image_formats:
                                embed.set_image(url=data["image"])
                    except:
                        pass
                    try:
                        if data["thumbnail"].lower() != 'none':
                            image_formats = ("image/png", "image/jpeg", "image/gif")
                            url = f'{data["thumbnail"]}'
                            site = urlopen(url)
                            meta = site.info()
                            if meta["content-type"] in image_formats:
                                embed.set_thumbnail(url=data["thumbnail"])
                    except:
                        pass
                    try:
                        if data["footer"].lower() != 'none':
                            embed.set_footer(text=footer)
                    except:
                        pass
                    try:
                        await channel.send(embed=embed)
                    except:
                        pass
                elif data["title"].lower() == "none" and data["description"].lower() != "none":
                    embed = discord.Embed(
                        color=discord.Color.blue(), description=description)
                    try:
                        if data["image"].lower() != 'none':
                            image_formats = ("image/png", "image/jpeg", "image/gif")
                            url = f'{data["image"]}'
                            site = urlopen(url)
                            meta = site.info()
                            if meta["content-type"] in image_formats:
                                embed.set_image(url=data["image"])
                    except:
                        pass
                    try:
                        if data["thumbnail"].lower() != 'none':
                            image_formats = ("image/png", "image/jpeg", "image/gif")
                            url = f'{data["thumbnail"]}'
                            site = urlopen(url)
                            meta = site.info()
                            if meta["content-type"] in image_formats:
                                embed.set_thumbnail(url=data["thumbnail"])
                    except:
                        pass
                    try:
                        if data["footer"].lower() != 'none':
                            embed.set_footer(text=footer)
                    except:
                        pass
                    await channel.send(embed=embed)

        @commands.Cog.listener()
        async def on_guild_join(self, guild):
            pdata = await self.bot.prefix.get_by_id(guild.id)
            if not pdata or "prefix" not in pdata:
                await self.bot.prefix.upsert({"_id": guild.id, "prefix": '-'})
            wdata = await self.bot.welcomer.get_by_id(guild.id)
            if not wdata or "welcomer" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "welcomer": False})
            if not wdata or "type" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "type": "embed"})
            if not wdata or "autorole" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "autorole": False})
            if not wdata or "autorole_human" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "autorole_human": 0})
            if not wdata or "autorole_bot" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "autorole_bot": 0})
            if not wdata or "channel" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "channel": 0})
            if not wdata or "message" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "message": "{user} Welcome to {server}"})
            if not wdata or "title" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "title": "Hello {user} Welcome to {server}"})
            if not wdata or "description" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "description": "Have a great time here!"})
            if not wdata or "image" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "image": "none"})
            if not wdata or "thumbnail" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "thumbnail": "none"})
            if not wdata or "footer" not in wdata:
                await self.bot.welcomer.upsert({"_id": guild.id, "footer": "{server}"})
            

        @commands.Cog.listener()
        async def on_command_error(self, ctx, error):
            ignored = (commands.CommandNotFound, commands.UserInputError)
            if isinstance(error, ignored):
                return
            
            elif isinstance(error, commands.NotOwner):
                return await ctx.send("*Hmmm* 😷")

            elif isinstance(error, commands.CommandOnCooldown):
                m, s = divmod(error.retry_after, 60)
                h, m = divmod(m, 60)
                if int(h) == 0 and int(m) == 0:
                    await ctx.send(f' You must wait {int(s)} seconds to use this command!')
                elif int(h) == 0 and int(m) != 0:
                    await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
                else:
                    await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
            # elif isinstance(error, commands.CheckFailure):
            #     # If the command has failed a check, trip this
            #     await ctx.send("Hey! You lack permission to use this command.")
            # raise error

def setup(bot):
    bot.add_cog(Events(bot))