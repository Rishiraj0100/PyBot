import discord
from discord.ext import commands
import time, calendar, datetime

class Events(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print("Events Cog has been loaded\n-------------------------")
        
        @commands.Cog.listener()
        async def on_message_delete(self, message):
            record = await self.bot.db.fetchrow("SELECT * FROM snipe WHERE channel_id = $1", message.channel.id)
            channel = message.channel.id
            author = message.author.name+'#'+message.author.discriminator
            content = message.content if message.content else "*[Content Unavailable]*"
            if not record:
                return await self.bot.db.execute("INSERT INTO snipe (channel_id, content, author, time) VALUES ($1,$2,$3,$4)", channel, content, author, int(time.time()))
            await self.bot.db.execute("UPDATE snipe SET (content,author,time) = ($2,$3,$4) WHERE channel_id = $1", message.channel.id, content, author, int(time.time()))
            # await ctx.send(f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!")
        
        @commands.Cog.listener()
        async def on_message(self, message):

            if message.author.id == self.bot.user.id:
                return

            data = await self.bot.db.fetchrow('SELECT * FROM blacklist WHERE (user_id) = ($1)', message.author.id)
            if data:
                return
            
            record = await self.bot.db.fetchrow('SELECT * FROM afk WHERE (guild_id,user_id) = ($1,$2)', 0, message.author.id)
            if record and message.content.startswith('#'):
                return
            
            if record:
                await self.bot.db.execute('DELETE FROM afk WHERE (guild_id,user_id) = ($1,$2)', 0, message.author.id)
                
                for g in message.author.mutual_guilds:
                    try:
                        m = g.get_member(message.author.id)
                        a = m.nick
                        a = a.replace('[AFK]', '')
                        a = a.replace('AFK', '')
                        await m.edit(nick=f'{a}')
                    except:
                        pass

                if len(record["ping"]) == 0:
                    pmsg  = '\n**You were not pinged while you were AFK.**'
                elif len(record["ping"]) == 1:
                    pmsg = f'**You were pinged {len(record["ping"])} time.\n\nClick Below to View them.**'
                else:
                    pmsg = f'**You were pinged {len(record["ping"])} times.\n\nClick Below to View them.**'

                t = int(record["time"])
                embed = discord.Embed(color=0x3498DB, description=f'Welcome Back **{message.author}**, I have removed your AFK.\nYou had gone afk <t:{t}:R>\n{pmsg}')
                view = discord.ui.View()
                # i = 0
                for link in record["ping"]:
                    but = discord.ui.Button(url=link, label='Go to Message')
                    view.add_item(but)
                    # i+=1
                if not view:
                    view = None
                await message.channel.send(embed=embed, view=view)

            a = None
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
                
                afk = await self.bot.db.fetchrow('SELECT * FROM afk WHERE (guild_id,user_id) = ($1,$2)', 0, a)

                if afk:
                    if "reason" not in afk:
                        reason = 'I am AFK :)'
                    else:
                        reason = afk["reason"]
                    t = int(afk["time"])
                    await message.reply(f'**{name}** went afk <t:{t}:R> : {reason}')
                    l = afk["ping"]
                    l.append(f"https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}")
                    await self.bot.db.execute("UPDATE afk SET ping = $3 WHERE (guild_id,user_id) = ($1,$2)", 0, a, l)
                    return

            data = await self.bot.db.fetchrow('SELECT * FROM afk WHERE (guild_id,user_id) = ($1,$2)', message.guild.id, message.author.id)
            if data and message.content.startswith('#'):
                return

            if data:
                await self.bot.db.execute('DELETE FROM afk WHERE (guild_id,user_id) = ($1,$2)', message.guild.id, message.author.id)
                
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

                t = int(data["time"])
                embed = discord.Embed(color=0x3498DB, description=f'Welcome Back **{message.author}**, I have removed your AFK.\nYou had gone afk <t:{t}:R>\n{pmsg}')
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
                
                afk = await self.bot.db.fetchrow('SELECT * FROM afk WHERE (guild_id,user_id) = ($1,$2)', message.guild.id, a)

                if afk:
                    if "reason" not in afk:
                        reason = 'I am AFK :)'
                    else:
                        reason = afk["reason"]
                    t = int(afk["time"])
                    await message.reply(f'**{name}** went afk <t:{t}:R> : {reason}')
                    l = afk["ping"]
                    l.append(f"https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}")
                    await self.bot.db.execute("UPDATE afk SET ping = $3 WHERE (guild_id,user_id) = ($1,$2)", message.guild.id, a, l)
                    return

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
                        data = await self.bot.db.fetchrow('SELECT * FROM prefix WHERE guild_id = $1', message.guild.id)
                        if not data:
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
                            embed.set_image(url=data["image"])
                    except:
                        pass
                    try:
                        if data["thumbnail"].lower() != 'none':
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
                            embed.set_image(url=data["image"])
                    except:
                        pass
                    try:
                        if data["thumbnail"].lower() != 'none':
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
                                embed.set_image(url=data["image"])
                    except:
                        pass
                    try:
                        if data["thumbnail"].lower() != 'none':
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
                                embed.set_image(url=data["image"])
                    except:
                        pass
                    try:
                        if data["thumbnail"].lower() != 'none':
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
            pdata = await self.bot.db.fetchrow('SELECT * FROM prefix WHERE guild_id = $1', guild.id)
            if not pdata:
                return await self.bot.db.execute("INSERT INTO prefix (guild_id, prefix) VALUES ($1,$2)", guild.id, '-')

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