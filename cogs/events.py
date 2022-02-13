import discord
from discord.ext import commands
from urllib.request import urlopen

class Events(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print("Events Cog has been loaded\n-------------------------")

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