from os import EX_CANTCREAT
import discord
from discord.ext import commands
import asyncio
from discord.ui import Button, View
from urllib.request import urlopen

class Welcomer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Welcomer Cog has loaded\n-------------------------")

    @commands.command(name='welcomer', aliases=['setup-welcome', 'welcome', 'setup-welcomer'], usage='-welcomer')
    @commands.has_guild_permissions(administrator=True)
    async def welcome(self, ctx):
        """
        Welcome everyone with a Sweet Greeting
        """
        data = await self.bot.welcomer.get_by_id(ctx.guild.id)
        if not data or "welcomer" not in data:
            toggle = False
            await self.bot.welcomer.upsert({"_id": ctx.guild.id, "welcomer": False})
        else:
            if data["welcomer"] == True:
                toggle = 'On'
            else:
                toggle = 'Off'

        data = await self.bot.welcomer.get_by_id(ctx.guild.id)
        if "type" not in data:
            type = 'Embed'
            await self.bot.welcomer.upsert({"_id": ctx.guild.id, "type": 'embed'})
        else:
            if data["type"] == 'message':
                type = 'Message'
            elif data["type"] == 'embed':
                type = 'Embed'
            elif data["type"] == 'embedtext':
                type = 'Embed and Text'

        data = await self.bot.welcomer.get_by_id(ctx.guild.id)
        if "autorole" not in data:
            auto = False
            await self.bot.welcomer.upsert({"_id": ctx.guild.id, "autorole": False})
        else:
            if data["autorole"] == True:
                auto = 'On'
            else:
                auto = 'Off'

        data = await self.bot.welcomer.get_by_id(ctx.guild.id)
        if "autorole_human" not in data:
            autoh = 0
            await self.bot.welcomer.upsert({"_id": ctx.guild.id, "autorole_human": 0})
        else:
            if data["autorole_human"] == 0:
                autoh = '`Not Set`'
            else:
                autoh = '<@&'+str(data["autorole_human"])+'>'

        data = await self.bot.welcomer.get_by_id(ctx.guild.id)
        if "autorole_bot" not in data:
            auto = 0
            await self.bot.welcomer.upsert({"_id": ctx.guild.id, "autorole_bot": 0})
        else:
            if data["autorole_bot"] == 0:
                autob = '`Not Set`'
            else:
                autob = '<@&'+str(data["autorole_bot"])+'>'

        data = await self.bot.welcomer.get_by_id(ctx.guild.id)
        if "channel" not in data:
            channel = '`Not Set`'
            await self.bot.welcomer.upsert({"_id": ctx.guild.id, "channel": 0})
        else:
            if data["channel"] == 0:
                channel = '`No Channel`'
            else:
                channel = '<#'+str(data["channel"])+'>'
        if "message" not in data:
            ms = '`Not Set`'
            await self.bot.welcomer.upsert({"_id": ctx.guild.id, "channel": 0})
        else:
            if data["channel"] == 0:
                channel = '`No Channel`'
            else:
                channel = '<#'+str(data["channel"])+'>'

        embed = discord.Embed(title='Welcomer and Autorole', color=0x3498DB)

        embed.add_field(
            name=f'<:Dot_One:939397712779042856>⠀ **Welcomer**', value=f'`{toggle}`')
        embed.add_field(name=f'<:Dot_Two:939397728616726528>⠀ **Message Type**',
                        value=f'`{type}`', inline=False)
        embed.add_field(
            name=f'<:Dot_Three:939397746329255976>⠀ **Channel**', value=channel, inline=False)
        embed.add_field(name=f'<:Dot_Four:939397772661125161>⠀ **Message**',
                        value=f'*Click on the Respective Button to View this.*', inline=False)
        embed.add_field(name=f'<:Dot_Five:939397784887504896>⠀ **Autorole**',
                        value=f'`{auto}`', inline=False)
        embed.add_field(
            name=f'<:Dot_Six:939397798057615360>⠀ **Human Autorole**', value=f'{autoh}', inline=False)
        embed.add_field(
            name=f'<:Dot_Seven:939397814780325958>⠀ **Bot Autorole**', value=f'{autob}', inline=False)

        stop_button = Button(emoji='<:Dot_stop:939504467328520233>')
        toggle_button = Button(emoji='<:Dot_One:939397712779042856>')
        type_button = Button(emoji='<:Dot_Two:939397728616726528>')
        channel_button = Button(emoji='<:Dot_Three:939397746329255976>')
        m_button = Button(emoji='<:Dot_Four:939397772661125161>')
        autorole_button = Button(emoji='<:Dot_Five:939397784887504896>')
        autoh_button = Button(emoji='<:Dot_Six:939397798057615360>')
        autob_button = Button(emoji='<:Dot_Seven:939397814780325958>')

        view = View()
        view.add_item(stop_button)
        view.add_item(toggle_button)
        view.add_item(type_button)
        view.add_item(channel_button)
        view.add_item(m_button)
        view.add_item(autorole_button)
        view.add_item(autoh_button)
        view.add_item(autob_button)

        msg = await ctx.send(embed=embed, view=view)

        async def stop_button_callback(interaction):
            if interaction.user != ctx.author:
                embeda = discord.Embed(
                    description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                return await interaction.response.send_message(embed=embeda, ephemeral=True)
            try:
                await msg.delete()
            except:
                pass

        stop_button.callback = stop_button_callback

        async def toggle_button_callback(interaction):
            if interaction.user != ctx.author:
                embeda = discord.Embed(
                    description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                return await interaction.response.send_message(embed=embeda, ephemeral=True)
            data = await self.bot.welcomer.get_by_id(interaction.guild.id)
            if data["welcomer"] == True:
                await self.bot.welcomer.upsert({"_id": interaction.guild.id, "welcomer": False})
                # embed.remove_field(0)
                embed.set_field_at(
                    0, name=f'<:Dot_One:939397712779042856>⠀ **Welcomer**', value=f'`Off`')
            else:
                await self.bot.welcomer.upsert({"_id": interaction.guild.id, "welcomer": True})
                # embed.remove_field(0)
                embed.set_field_at(
                    0, name=f'<:Dot_One:939397712779042856>⠀ **Welcomer**', value=f'`On`')
            await asyncio.sleep(0.2)

            await interaction.response.edit_message(embed=embed, view=view)

        toggle_button.callback = toggle_button_callback

        async def type_button_callback(interaction):
            if interaction.user != ctx.author:
                embeda = discord.Embed(
                    description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                return await interaction.response.send_message(embed=embeda, ephemeral=True)
            data = await self.bot.welcomer.get_by_id(interaction.guild.id)
            if data["welcomer"] == False:
                warn = discord.Embed(
                    description=f'<a:cross1:941287490986315776> **Turn on Welcomer to use this!**', color=0xff0000)
                return await interaction.response.send_message(embed=warn, ephemeral=True)
            if data["type"] == 'message':
                await self.bot.welcomer.upsert({"_id": interaction.guild.id, "type": 'embed'})
                # embed.remove_field(1)
                embed.set_field_at(
                    1, name=f'<:Dot_Two:939397728616726528>⠀ **Message Type**', value=f'`Embed`', inline=False)
            elif data["type"] == 'embed':
                # await self.bot.welcomer.upsert({"_id": interaction.guild.id, "type": 'embedtext'})
                await self.bot.welcomer.upsert({"_id": interaction.guild.id, "type": 'message'})
                # embed.remove_field(1)
                embed.set_field_at(
                    1, name=f'<:Dot_Two:939397728616726528>⠀ **Message Type**', value=f'`Message`', inline=False)
            # elif data["type"] == 'embedtext':
            #     await self.bot.welcomer.upsert({"_id": interaction.guild.id, "type": 'message'})
            #     # embed.remove_field(1)
            #     embed.set_field_at(
            #         1, name=f'<:Dot_Two:939397728616726528>⠀ **Message Type**', value=f'`Message`', inline=False)
            await asyncio.sleep(0.2)

            await interaction.response.edit_message(embed=embed, view=view)

        type_button.callback = type_button_callback

        async def channel_button_callback(interaction):
            if interaction.user != ctx.author:
                embeda = discord.Embed(
                    description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                return await interaction.response.send_message(embed=embeda, ephemeral=True)
            data = await self.bot.welcomer.get_by_id(interaction.guild.id)
            if data["welcomer"] == False:
                warn = discord.Embed(
                    description=f'<a:cross1:941287490986315776> **Turn on Welcomer to use this!**', color=0xff0000)
                return await interaction.response.send_message(embed=warn, ephemeral=True)

            def check(message):
                return message.author == ctx.author and message.channel == ctx.message.channel
            channelm = discord.Embed(
                description=f'**Enter Channel**', color=0x3498DB)
            await interaction.response.send_message(embed=channelm)
            res = await self.bot.wait_for(
                "message",
                check=lambda x: x.channel.id == ctx.channel.id
                and ctx.author.id == x.author.id,
                timeout=None,
            )
            await ctx.channel.purge(limit=2)
            a = res.content.replace('<#', '')
            chid = a.replace('>', '')

            for channel in ctx.guild.channels:
                if str(channel.id) in str(chid):
                    await self.bot.welcomer.upsert({"_id": interaction.guild.id, "channel": int(chid)})
                    embed.set_field_at(
                        2, name=f'<:Dot_Three:939397746329255976>⠀ **Channel**', value='<#'+str(chid)+'>', inline=False)
                    await msg.edit(embed=embed, view=view)
                    break

            else:
                mesc = discord.Embed(
                    description='Channel Not Found!', color=0xff0000)
                mes = await ctx.send(embed=mesc)
                await asyncio.sleep(5)
                try:
                    await mes.delete()
                except:
                    pass
            # await ctx.channel.purge(limit=2)

            # await self.bot.welcomer.upsert({"_id": interaction.guild.id, "channel": channel.id})
                # embed.remove_field(1)
            # embed.set_field_at(2, name=f'<:Dot_Three:939397746329255976>⠀ **Channel**', value={'<#'+str(channel.id)+'>'}, inline=False)
            # await asyncio.sleep(0.2)

            # await interaction.response.edit_message(embed=embed, view=view)

        channel_button.callback = channel_button_callback

        async def autorole_button_callback(interaction):
            if interaction.user != ctx.author:
                embeda = discord.Embed(
                    description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                return await interaction.response.send_message(embed=embeda, ephemeral=True)
            data = await self.bot.welcomer.get_by_id(interaction.guild.id)
            if data["autorole"] == True:
                await self.bot.welcomer.upsert({"_id": interaction.guild.id, "autorole": False})
                # embed.remove_field(0)
                embed.set_field_at(
                    4, name=f'<:Dot_Five:939397784887504896>⠀ **Autorole**', value=f'`Off`')
            else:
                await self.bot.welcomer.upsert({"_id": interaction.guild.id, "autorole": True})
                # embed.remove_field(0)
                embed.set_field_at(
                    4, name=f'<:Dot_Five:939397784887504896>⠀ **Autorole**', value=f'`On`')
            await asyncio.sleep(0.2)

            await interaction.response.edit_message(embed=embed, view=view)

        autorole_button.callback = autorole_button_callback

        async def autoh_button_callback(interaction):
            if interaction.user != ctx.author:
                embeda = discord.Embed(
                    description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                return await interaction.response.send_message(embed=embeda, ephemeral=True)
            bt = []
            data = await self.bot.welcomer.get_by_id(interaction.guild.id)
            if data["autorole"] == False:
                warn = discord.Embed(
                    description=f'<a:cross1:941287490986315776> **Turn on Autorole to use this!**', color=0xff0000)
                return await interaction.response.send_message(embed=warn, ephemeral=True)

            def check(message):
                return message.author == ctx.author and message.channel == ctx.message.channel
            autoroleh = discord.Embed(
                description=f'**Enter Role for Humans (Use 0 for None)**', color=0x3498DB)
            await interaction.response.send_message(embed=autoroleh)
            res = await self.bot.wait_for(
                "message",
                check=lambda x: x.channel.id == ctx.channel.id
                and ctx.author.id == x.author.id,
                timeout=None,
            )
            await ctx.channel.purge(limit=2)
            if res.content == '0':
                await self.bot.welcomer.upsert({"_id": interaction.guild.id, "autorole_human": 0})
                embed.set_field_at(
                    5, name=f'<:Dot_Six:939397798057615360>⠀ **Human Autorole**', value='`Not Set`', inline=False)
                await msg.edit(embed=embed, view=view)
            else:
                a = res.content.replace('<@&', '')
                auhid = a.replace('>', '')
                try:
                    hr = ctx.guild.get_role(int(auhid))
                    if ctx.guild.me.top_role <= hr:
                        emh = discord.Embed(
                            description=f'<a:cross1:941287490986315776> **{hr.mention} is above My Highest Role ({ctx.guild.me.top_role.mention}).**', color=0x00ff0000)
                        hm = await ctx.send(embed=emh)
                        await asyncio.sleep(5)
                        try:
                            await hm.delete()
                        except:
                            pass
                        return
                except:
                    pass

                for role in ctx.guild.roles:
                    for member in ctx.guild.members:
                        if member.bot:
                            if member.name == role.name:
                                bt.append(role.id)
                else:
                    for r in bt:
                        if str(r) == str(auhid):
                            both = discord.Embed(
                                description='**<a:cross1:941287490986315776> Cannot use a Bot Role!**', color=0xff0000)
                            bot = await ctx.send(embed=both)
                            await asyncio.sleep(5)
                            try:
                                await bot.delete()
                            except:
                                pass
                            return

                for role in ctx.guild.roles:
                    # print(f'{role.id} :: {auhid}')
                    if str(role.id) == str(auhid):
                        await self.bot.welcomer.upsert({"_id": interaction.guild.id, "autorole_human": int(auhid)})
                        embed.set_field_at(
                            5, name=f'<:Dot_Six:939397798057615360>⠀ **Human Autorole**', value='<@&'+str(auhid)+'>', inline=False)
                        await msg.edit(embed=embed, view=view)
                        break
                else:
                    print()
                    mesc = discord.Embed(
                        description='Role Not Found!', color=0xff0000)
                    mes = await ctx.send(embed=mesc)
                    await asyncio.sleep(5)
                    try:
                        await mes.delete()
                    except:
                        pass

        autoh_button.callback = autoh_button_callback

        async def autob_button_callback(interaction):
            if interaction.user != ctx.author:
                embeda = discord.Embed(
                    description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                return await interaction.response.send_message(embed=embeda, ephemeral=True)
            bt = []
            data = await self.bot.welcomer.get_by_id(interaction.guild.id)
            if data["autorole"] == False:
                warn = discord.Embed(
                    description=f'<a:cross1:941287490986315776> **Turn on Autorole to use this!**', color=0xff0000)
                return await interaction.response.send_message(embed=warn, ephemeral=True)

            def check(message):
                return message.author == ctx.author and message.channel == ctx.message.channel
            autoroleh = discord.Embed(
                description=f'**Enter Role for Bots (Use 0 for None)**', color=0x3498DB)
            await interaction.response.send_message(embed=autoroleh)
            res = await self.bot.wait_for(
                "message",
                check=lambda x: x.channel.id == ctx.channel.id
                and ctx.author.id == x.author.id,
                timeout=None,
            )
            await ctx.channel.purge(limit=2)
            if res.content == '0':
                await self.bot.welcomer.upsert({"_id": interaction.guild.id, "autorole_human": 0})
                embed.set_field_at(
                    6, name=f'<:Dot_Seven:939397814780325958>⠀ **Bot Autorole**', value='`Not Set`', inline=False)
                await msg.edit(embed=embed, view=view)
            else:
                a = res.content.replace('<@&', '')
                auhid = a.replace('>', '')
                try:
                    hr = ctx.guild.get_role(int(auhid))
                    if ctx.guild.me.top_role <= hr:
                        emh = discord.Embed(
                            description=f'<a:cross1:941287490986315776> **{hr.mention} is above My Highest Role ({ctx.guild.me.top_role.mention}).**', color=0x00ff0000)
                        hm = await ctx.send(embed=emh)
                        await asyncio.sleep(5)
                        try:
                            await hm.delete()
                        except:
                            pass
                        return
                except:
                    pass

                for role in ctx.guild.roles:
                    for member in ctx.guild.members:
                        if member.bot:
                            if member.name == role.name:
                                bt.append(role.id)
                else:
                    for r in bt:
                        if str(r) == str(auhid):
                            both = discord.Embed(
                                description='**<a:cross1:941287490986315776> Cannot use a Bot Role!**', color=0xff0000)
                            bot = await ctx.send(embed=both)
                            await asyncio.sleep(5)
                            try:
                                await bot.delete()
                            except:
                                pass
                            return

                for role in ctx.guild.roles:
                    # print(f'{role.id} :: {auhid}')
                    if str(role.id) == str(auhid):
                        await self.bot.welcomer.upsert({"_id": interaction.guild.id, "autorole_bot": int(auhid)})
                        embed.set_field_at(
                            6, name=f'<:Dot_Seven:939397814780325958>⠀ **Bot Autorole**', value='<@&'+str(auhid)+'>', inline=False)
                        await msg.edit(embed=embed, view=view)
                        break
                else:
                    print()
                    mesc = discord.Embed(
                        description='Role Not Found!', color=0xff0000)
                    mes = await ctx.send(embed=mesc)
                    await asyncio.sleep(5)
                    try:
                        await mes.delete()
                    except:
                        pass

        autob_button.callback = autob_button_callback

        async def m_button_callback(m_interaction):
            if m_interaction.user != ctx.author:
                embeda = discord.Embed(
                    description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                return await m_interaction.response.send_message(embed=embeda, ephemeral=True)
            get_button = Button(
                style=discord.ButtonStyle.blurple, label='Get Message')
            pre_button = Button(
                style=discord.ButtonStyle.green, label='Preview')
            edit_button = Button(style=discord.ButtonStyle.secondary,
                                 label='Edit', emoji='<:Dot_edit:939800272606232597>')
            preview = View()
            preview.add_item(get_button)
            preview.add_item(pre_button)
            preview.add_item(edit_button)
            data = await self.bot.welcomer.get_by_id(m_interaction.guild.id)
            if "message" not in data:
                ms = '{user} Welcome to {server}'
                await self.bot.welcomer.upsert({"_id": ctx.guild.id, "message": "{user} Welcome to {server}"})
            else:
                if data["message"] == 'none':
                    ms = '`{user} Welcome to {server}`'
                else:
                    ms = data["message"]
            if data["welcomer"] == False:
                warn = discord.Embed(
                    description=f'<a:cross1:941287490986315776> **Turn on Welcomer to use this!**', color=0xff0000)
                return await m_interaction.response.send_message(embed=warn, ephemeral=True)

            await m_interaction.response.send_message(f'\u200b', view=preview, ephemeral=True)

            async def get_button_callback(interaction):
                if interaction.user != ctx.author:
                    embeda = discord.Embed(
                        description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                    return await interaction.response.send_message(embed=embeda, ephemeral=True)
                data = await self.bot.welcomer.get_by_id(interaction.guild.id)
                if data["type"] == "message":
                    await interaction.response.send_message(f'{data["message"]}', ephemeral=True)
                elif data["type"] == "embed":
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
                                embed.set_footer(text=data["footer"])
                        except:
                            pass
                        try:
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                        except:
                            await interaction.response.send_message('Embed not Set', ephemeral=True)
                    elif data["title"].lower() != "none" and data["description"].lower() != "none":
                        embed = discord.Embed(color=discord.Color.blue(
                        ), title=data["title"], description=data["description"])
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
                                embed.set_footer(text=data["footer"])
                        except:
                            pass
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    elif data["title"].lower() != "none" and data["description"].lower() == "none":
                        embed = discord.Embed(
                            color=discord.Color.blue(), title=data["title"])
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
                                embed.set_footer(text=data["footer"])
                        except:
                            pass
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    elif data["title"].lower() == "none" and data["description"].lower() != "none":
                        embed = discord.Embed(
                            color=discord.Color.blue(), description=data["description"])
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
                                embed.set_footer(text=data["footer"])
                        except:
                            pass
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        await interaction.response.send_message('Embed Not Set', ephemeral=True)

            get_button.callback = get_button_callback

            async def pre_button_callback(interaction):
                if interaction.user != ctx.author:
                    embeda = discord.Embed(
                        description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                    return await interaction.response.send_message(embed=embeda, ephemeral=True)
                data = await self.bot.welcomer.get_by_id(interaction.guild.id)
                if data["type"] == "message":
                    data = await self.bot.welcomer.get_by_id(interaction.guild.id)
                    ab = data["message"]
                    ab = ab.replace('{user}', f'{ctx.author.mention}')
                    ab = ab.replace('{username}', f'{ctx.author.name}')
                    ab = ab.replace('{server}', f'{ctx.guild.name}')
                    await interaction.response.send_message(ab, ephemeral=True)
                elif data["type"] == "embed":

                    title = data["title"]
                    title = title.replace('{user}', f'{ctx.author.name}')
                    title = title.replace('{username}', f'{ctx.author.name}')
                    title = title.replace('{server}', f'{ctx.guild.name}')

                    description = data["description"]
                    description = description.replace(
                        '{user}', f'{ctx.author.mention}')
                    description = description.replace(
                        '{username}', f'{ctx.author.name}')
                    description = description.replace(
                        '{server}', f'{ctx.guild.name}')

                    footer = data["footer"]
                    footer = footer.replace('{user}', f'{ctx.author.name}')
                    footer = footer.replace('{username}', f'{ctx.author.name}')
                    footer = footer.replace('{server}', f'{ctx.guild.name}')

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
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                        except:
                            await interaction.response.send_message('Embed not Set', ephemeral=True)
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
                        await interaction.response.send_message(embed=embed, ephemeral=True)
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
                        await interaction.response.send_message(embed=embed, ephemeral=True)
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
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        await interaction.response.send_message('Embed Not Set', ephemeral=True)

            pre_button.callback = pre_button_callback

            async def edit_button_callback(interaction):
                if interaction.user != ctx.author:
                    embeda = discord.Embed(
                        description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                    return await interaction.response.send_message(embed=embeda, ephemeral=True)
                data = await self.bot.welcomer.get_by_id(interaction.guild.id)
                if data["type"] == "message":
                    editm = discord.Embed(
                        description='**Enter the Message to Set**\n\n**Variables**\n```yaml\n{user} - The mention of the user calling the command.\n{username} - The username of the user.\n{server} - The server name.\n```\n__**Note - Emojis should be in this Server or else they would not be displayed while Greeting Someone**__', color=0x3498DB)
                    a = await interaction.response.send_message(embed=editm, ephemeral=True)
                    res = await self.bot.wait_for(
                        "message",
                        check=lambda x: x.channel.id == ctx.channel.id
                        and ctx.author.id == x.author.id,
                        timeout=None,
                    )
                    if res.content.lower() == 'none':
                        res = '{user} Welcome to {server}'
                    else:
                        res = res.content
                    emb = discord.Embed(
                        description='**Message Changed!**', color=0x3498DB)
                    await interaction.followup.send(embed=emb, ephemeral=True)
                    await ctx.channel.purge(limit=1)

                    await self.bot.welcomer.upsert({"_id": ctx.guild.id, "message": res})

                elif data["type"] == "embed":
                    title_button = Button(
                        style=discord.ButtonStyle.blurple, label='Set Title')
                    description_button = Button(
                        style=discord.ButtonStyle.blurple, label='Set Description')
                    image_button = Button(
                        style=discord.ButtonStyle.blurple, label='Set Image')
                    footer_button = Button(
                        style=discord.ButtonStyle.blurple, label='Set Footer')
                    thumbnail_button = Button(
                        style=discord.ButtonStyle.blurple, label='Set Thumbnail')
                    done_button = Button(
                        style=discord.ButtonStyle.green, label='Done')
                    edit_view = View()
                    edit_view.add_item(title_button)
                    edit_view.add_item(description_button)
                    edit_view.add_item(image_button)
                    edit_view.add_item(footer_button)
                    edit_view.add_item(thumbnail_button)
                    edit_view.add_item(done_button)
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
                                embed.set_footer(text=data["footer"])
                        except:
                            pass
                        try:
                            editm = discord.Embed(
                            description='**Variables**\n```yaml\n{user} - The mention of the user calling the command.\n{username} - The username of the user.\n{server} - The server name.\n```\n__**Note - Emojis should be in this Server or else they would not be displayed while Greeting Someone**__', color=0x3498DB)
                            await interaction.response.send_message(embed=editm, ephemeral=True)

                            emb_embed = await ctx.send(embed=embed, view=edit_view)
                        except:
                            e_embed = discord.Embed(description='Use Buttons to Customize this Embed',color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    e_embed.set_image(url=data["image"])
                            except:
                                pass
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    e_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    e_embed.set_footer(text=data["footer"])
                            except:
                                pass

                            emb_embed = await ctx.send(embed=e_embed, view=edit_view)
                    elif data["title"].lower() != "none" and data["description"].lower() != "none":
                        embed = discord.Embed(color=discord.Color.blue(
                        ), title=data["title"], description=data["description"])
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
                                embed.set_footer(text=data["footer"])
                        except:
                            pass
                        try:
                            editm = discord.Embed(
                            description='**Variables**\n```yaml\n{user} - The mention of the user calling the command.\n{username} - The username of the user.\n{server} - The server name.\n```\n__**Note - Emojis should be in this Server or else they would not be displayed while Greeting Someone**__', color=0x3498DB)
                            await interaction.response.send_message(embed=editm, ephemeral=True)

                            emb_embed = await ctx.send(embed=embed, view=edit_view)
                        except:
                            e_embed = discord.Embed(description='Use Buttons to Customize this Embed',color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    e_embed.set_image(url=data["image"])
                            except:
                                pass
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    e_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    e_embed.set_footer(text=data["footer"])
                            except:
                                pass

                            emb_embed = await ctx.send(embed=e_embed, view=edit_view)

                    elif data["title"].lower() != "none" and data["description"].lower() == "none":
                        embed = discord.Embed(
                            color=discord.Color.blue(), title=data["title"])
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
                                embed.set_footer(text=data["footer"])
                        except:
                            pass
                        try:
                            editm = discord.Embed(
                            description='**Variables**\n```yaml\n{user} - The mention of the user calling the command.\n{username} - The username of the user.\n{server} - The server name.\n```\n__**Note - Emojis should be in this Server or else they would not be displayed while Greeting Someone**__', color=0x3498DB)
                            await interaction.response.send_message(embed=editm, ephemeral=True)

                            emb_embed = await ctx.send(embed=embed, view=edit_view)
                        except:
                            e_embed = discord.Embed(description='Use Buttons to Customize this Embed',color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    e_embed.set_image(url=data["image"])
                            except:
                                pass
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    e_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    e_embed.set_footer(text=data["footer"])
                            except:
                                pass

                            emb_embed = await ctx.send(embed=e_embed, view=edit_view)

                    elif data["title"].lower() == "none" and data["description"].lower() != "none":
                        embed = discord.Embed(
                            color=discord.Color.blue(), description=data["description"])
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
                                embed.set_footer(text=data["footer"])
                        except:
                            pass
                        try:
                            editm = discord.Embed(
                            description='**Variables**\n```yaml\n{user} - The mention of the user calling the command.\n{username} - The username of the user.\n{server} - The server name.\n```\n__**Note - Emojis should be in this Server or else they would not be displayed while Greeting Someone**__', color=0x3498DB)
                            await interaction.response.send_message(embed=editm, ephemeral=True)

                            emb_embed = await ctx.send(embed=embed, view=edit_view)
                        except:
                            e_embed = discord.Embed(description='Use Buttons to Customize this Embed',color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    e_embed.set_image(url=data["image"])
                            except:
                                pass
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    e_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    e_embed.set_footer(text=data["footer"])
                            except:
                                pass

                            emb_embed = await ctx.send(embed=e_embed, view=edit_view)

                    else:
                            e_embed = discord.Embed(description='Use Buttons to Customize this Embed',color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    e_embed.set_image(url=data["image"])
                            except:
                                pass
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    e_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    e_embed.set_footer(text=data["footer"])
                            except:
                                pass

                            emb_embed = await ctx.send(embed=e_embed, view=edit_view)

                    async def title_button_callback(interaction):
                        if interaction.user != ctx.author:
                            embeda = discord.Embed(
                            description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                            return await interaction.response.send_message(embed=embeda, ephemeral=True)

                        ask = discord.Embed(description='**Enter the Title** *(Use None to remove)*', color=discord.Color.blue())
                        await interaction.response.send_message(embed=ask)
                        title = await self.bot.wait_for(
                        "message",
                        check=lambda x: x.channel.id == ctx.channel.id
                        and ctx.author.id == x.author.id,
                        timeout=None,
                    )
                        await self.bot.welcomer.upsert({"_id": interaction.guild.id, "title": title.content})
                        await ctx.channel.purge(limit=2)
                        
                        data = await self.bot.welcomer.get_by_id(interaction.guild.id)
                        if title.content.lower() == 'none':
                            if data["description"].lower() == 'none':
                                title_embed = discord.Embed(color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        title_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        title_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        title_embed.set_footer(text=data["footer"])
                                except:
                                    pass

                            elif data["description"].lower() != 'none':
                                title_embed = discord.Embed(description=data["description"], color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        title_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        title_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        title_embed.set_footer(text=data["footer"])
                                except:
                                    pass
                            
                            try:
                                await emb_embed.edit(embed=title_embed, view=edit_view)
                            except:
                                title_embed = discord.Embed(description='Use Buttons to Customize this Embed',color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        title_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        title_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        title_embed.set_footer(text=data["footer"])
                                except:
                                    pass

                                await emb_embed.edit(embed=title_embed, view=edit_view)


                        if data["description"].lower() == 'none':
                            title_embed = discord.Embed(title=title.content, color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    title_embed.set_image(url=data["image"])
                            except:
                                pass
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    title_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    title_embed.set_footer(text=data["footer"])
                            except:
                                pass

                        elif data["description"].lower() != 'none':
                            title_embed = discord.Embed(title=title.content, description=data["description"], color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    title_embed.set_image(url=data["image"])
                            except:
                                pass
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    title_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    title_embed.set_footer(text=data["footer"])
                            except:
                                pass
                            
                        await emb_embed.edit(embed=title_embed, view=edit_view)
                    title_button.callback = title_button_callback

                    async def description_button_callback(interaction):
                        if interaction.user != ctx.author:
                            embeda = discord.Embed(
                            description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                            return await interaction.response.send_message(embed=embeda, ephemeral=True)

                        ask = discord.Embed(description='**Enter the Description** *(Use None to remove)*', color=discord.Color.blue())
                        await interaction.response.send_message(embed=ask)
                        description = await self.bot.wait_for(
                        "message",
                        check=lambda x: x.channel.id == ctx.channel.id
                        and ctx.author.id == x.author.id,
                        timeout=None,
                    )
                        await self.bot.welcomer.upsert({"_id": interaction.guild.id, "description": description.content})
                        await ctx.channel.purge(limit=2)
                        
                        data = await self.bot.welcomer.get_by_id(interaction.guild.id)
                        if description.content.lower() == 'none':
                            if data["title"].lower() == 'none':
                                description_embed = discord.Embed(color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        description_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        description_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        description_embed.set_footer(text=data["footer"])
                                except:
                                    pass

                            elif data["title"].lower() != 'none':
                                description_embed = discord.Embed(title=data["title"], color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        description_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        description_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        description_embed.set_footer(text=data["footer"])
                                except:
                                    pass
                            
                            try:
                                await emb_embed.edit(embed=description_embed, view=edit_view)
                            except:
                                description_embed = discord.Embed(description='Use Buttons to Customize this Embed',color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        description_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        description_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        description_embed.set_footer(text=data["footer"])
                                except:
                                    pass

                                await emb_embed.edit(embed=description_embed, view=edit_view)


                        if data["title"].lower() == 'none':
                            description_embed = discord.Embed(description=description.content, color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    description_embed.set_image(url=data["image"])
                            except:
                                pass
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    description_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    description_embed.set_footer(text=data["footer"])
                            except:
                                pass

                        elif data["title"].lower() != 'none':
                            description_embed = discord.Embed(title=data["title"], description=description.content, color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    description_embed.set_image(url=data["image"])
                            except:
                                pass
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    description_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    description_embed.set_footer(text=data["footer"])
                            except:
                                pass
                            
                        await emb_embed.edit(embed=description_embed, view=edit_view)
                    description_button.callback = description_button_callback

                    async def image_button_callback(interaction):
                        if interaction.user != ctx.author:
                            embeda = discord.Embed(
                            description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                            return await interaction.response.send_message(embed=embeda, ephemeral=True)

                        ask = discord.Embed(description='**Enter the Image URL** *(Use None to remove)*', color=discord.Color.blue())
                        await interaction.response.send_message(embed=ask)
                        image = await self.bot.wait_for(
                        "message",
                        check=lambda x: x.channel.id == ctx.channel.id
                        and ctx.author.id == x.author.id,
                        timeout=None,
                    )
                        data = await self.bot.welcomer.get_by_id(interaction.guild.id)
                        if data["thumbnail"].lower() != 'none':
                            image_formats = ("image/png", "image/jpeg", "image/gif")
                            url = f'{image.content}'
                            site = urlopen(url)
                            meta = site.info()
                            if meta["content-type"] in image_formats:
                                await self.bot.welcomer.upsert({"_id": interaction.guild.id, "image": image.content})
                        await ctx.channel.purge(limit=2)
                        
                        data = await self.bot.welcomer.get_by_id(interaction.guild.id)
                        if image.content.lower() == 'none':
                            if data["title"].lower() == 'none' and data["description"].lower() == 'none':
                                image_embed = discord.Embed(color=discord.Color.blue())
                                try:
                                    if image.content.lower() != 'none':
                                        image_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        image_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        image_embed.set_footer(text=data["footer"])
                                except:
                                    pass

                            elif data["title"].lower() != 'none' and data["description"].lower() != 'none':
                                image_embed = discord.Embed(title=data["title"], description=data["description"],color=discord.Color.blue())
                                try:
                                    if image.content.lower() != 'none':
                                        image_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        image_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        image_embed.set_footer(text=data["footer"])
                                except:
                                    pass

                            elif data["title"].lower() == 'none' and data["description"].lower() != 'none':
                                image_embed = discord.Embed(description=data["description"],color=discord.Color.blue())
                                try:
                                    if image.content.lower() != 'none':
                                        image_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        image_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        image_embed.set_footer(text=data["footer"])
                                except:
                                    pass
                            elif data["title"].lower() != 'none' and data["description"].lower() == 'none':
                                image_embed = discord.Embed(title=data["title"],color=discord.Color.blue())
                                try:
                                    if image.content.lower() != 'none':
                                        image_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        image_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        image_embed.set_footer(text=data["footer"])
                                except:
                                    pass
                            
                            try:
                                await emb_embed.edit(embed=image_embed, view=edit_view)
                            except:
                                image_embed = discord.Embed(description='Use Buttons to Customize this Embed',color=discord.Color.blue())
                                try:
                                    if image.content.lower() != 'none':
                                        image_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        image_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        image_embed.set_footer(text=data["footer"])
                                except:
                                    pass

                                await emb_embed.edit(embed=image_embed, view=edit_view)

                        if data["title"].lower() == 'none' and data["description"].lower() == 'none':
                            image_embed = discord.Embed(color=discord.Color.blue())
                            try:
                                if image.content.lower() != 'none':
                                    image_embed.set_image(url=image.content)
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                await ctx.send(embed=errembed)
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    image_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    image_embed.set_footer(text=data["footer"])
                            except:
                                pass

                        elif data["title"].lower() != 'none' and data["description"].lower() != 'none':
                            image_embed = discord.Embed(title=data["title"], description=data["description"], color=discord.Color.blue())
                            try:
                                if image.content.lower() != 'none':
                                    image_embed.set_image(url=image.content)
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                await ctx.send(embed=errembed)
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    image_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    image_embed.set_footer(text=data["footer"])
                            except:
                                pass
                        elif data["title"].lower() == 'none' and data["description"].lower() != 'none':
                            image_embed = discord.Embed(description=data["description"], color=discord.Color.blue())
                            try:
                                if image.content.lower() != 'none':
                                    image_embed.set_image(url=image.content)
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                await ctx.send(embed=errembed)
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    image_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    image_embed.set_footer(text=data["footer"])
                            except:
                                pass
                        elif data["title"].lower() != 'none' and data["description"].lower() == 'none':
                            image_embed = discord.Embed(title=data["title"], description=data["description"], color=discord.Color.blue())
                            try:
                                if image.content.lower() != 'none':
                                    image_embed.set_image(url=image.content)
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                d = await ctx.send(embed=errembed)
                                await asyncio.sleep(5)
                                try:
                                    await d.delete()
                                except:
                                    pass
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    image_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    image_embed.set_footer(text=data["footer"])
                            except:
                                pass
                            
                        await emb_embed.edit(embed=image_embed, view=edit_view)
                    image_button.callback = image_button_callback

                    async def thumbnail_button_callback(interaction):
                        if interaction.user != ctx.author:
                            embeda = discord.Embed(
                            description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                            return await interaction.response.send_message(embed=embeda, ephemeral=True)

                        ask = discord.Embed(description='**Enter the Thumbnail URL** *(Use None to remove)*', color=discord.Color.blue())
                        await interaction.response.send_message(embed=ask)
                        thumb = await self.bot.wait_for(
                        "message",
                        check=lambda x: x.channel.id == ctx.channel.id
                        and ctx.author.id == x.author.id,
                        timeout=None,
                    )
                        data = await self.bot.welcomer.get_by_id(interaction.guild.id)
                        if data["thumbnail"].lower() != 'none':
                            image_formats = ("image/png", "image/jpeg", "image/gif")
                            url = f'{thumb.content}'
                            site = urlopen(url)
                            meta = site.info()
                            if meta["content-type"] in image_formats:
                                await self.bot.welcomer.upsert({"_id": interaction.guild.id, "thumbnail": thumb.content})
                        await ctx.channel.purge(limit=2)
                        
                        data = await self.bot.welcomer.get_by_id(interaction.guild.id)
                        if thumb.content.lower() == 'none':
                            if data["title"].lower() == 'none' and data["description"].lower() == 'none':
                                thumb_embed = discord.Embed(color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        thumb_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if thumb.content.lower() != 'none':
                                        thumb_embed.set_thumbnail(url=thumb.content)
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        thumb_embed.set_footer(text=data["footer"])
                                except:
                                    pass

                            elif data["title"].lower() != 'none' and data["description"].lower() != 'none':
                                thumb_embed = discord.Embed(title=data["title"], description=data["description"],color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        thumb_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if thumb.content.lower() != 'none':
                                        thumb_embed.set_thumbnail(url=thumb.content)
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        thumb_embed.set_footer(text=data["footer"])
                                except:
                                    pass

                            elif data["title"].lower() == 'none' and data["description"].lower() != 'none':
                                thumb_embed = discord.Embed(description=data["description"],color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        thumb_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if thumb.content.lower() != 'none':
                                        thumb_embed.set_thumbnail(url=thumb.content)
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        thumb_embed.set_footer(text=data["footer"])
                                except:
                                    pass
                            elif data["title"].lower() != 'none' and data["description"].lower() == 'none':
                                thumb_embed = discord.Embed(title=data["title"],color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        thumb_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if thumb.content.lower() != 'none':
                                        thumb_embed.set_thumbnail(url=thumb.content)
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        thumb_embed.set_footer(text=data["footer"])
                                except:
                                    pass
                            
                            try:
                                await emb_embed.edit(embed=thumb_embed, view=edit_view)
                            except:
                                thumb_embed = discord.Embed(description='Use Buttons to Customize this Embed',color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        thumb_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if thumb.content.lower() != 'none':
                                        thumb_embed.set_thumbnail(url=thumb.content)
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        thumb_embed.set_footer(text=data["footer"])
                                except:
                                    pass

                                await emb_embed.edit(embed=thumb_embed, view=edit_view)

                        if data["title"].lower() == 'none' and data["description"].lower() == 'none':
                            thumb_embed = discord.Embed(color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    thumb_embed.set_image(url=data["image"])
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                await ctx.send(embed=errembed)
                            try:
                                if thumb.content.lower() != 'none':
                                    thumb_embed.set_thumbnail(url=thumb.contnetn)
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    thumb_embed.set_footer(text=data["footer"])
                            except:
                                pass

                        elif data["title"].lower() != 'none' and data["description"].lower() != 'none':
                            thumb_embed = discord.Embed(title=data["title"], description=data["description"], color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    thumb_embed.set_image(url=data["image"])
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                await ctx.send(embed=errembed)
                            try:
                                if thumb.content.lower() != 'none':
                                    thumb_embed.set_thumbnail(url=thumb.content)
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    thumb_embed.set_footer(text=data["footer"])
                            except:
                                pass
                        elif data["title"].lower() == 'none' and data["description"].lower() != 'none':
                            thumb_embed = discord.Embed(description=data["description"], color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    thumb_embed.set_image(url=data["image"])
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                await ctx.send(embed=errembed)
                            try:
                                if thumb.content.lower() != 'none':
                                    thumb_embed.set_thumbnail(url=thumb.content)
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    thumb_embed.set_footer(text=data["footer"])
                            except:
                                pass
                        elif data["title"].lower() != 'none' and data["description"].lower() == 'none':
                            thumb_embed = discord.Embed(title=data["title"], description=data["description"], color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    thumb_embed.set_image(url=data["image"])
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                d = await ctx.send(embed=errembed)
                                await asyncio.sleep(5)
                                try:
                                    await d.delete()
                                except:
                                    pass
                            try:
                                if thumb.content.lower() != 'none':
                                    thumb_embed.set_thumbnail(url=thumb.content)
                            except:
                                pass
                            try:
                                if data["footer"].lower() != 'none':
                                    thumb_embed.set_footer(text=data["footer"])
                            except:
                                pass
                            
                        await emb_embed.edit(embed=thumb_embed, view=edit_view)
                    thumbnail_button.callback = thumbnail_button_callback

                    async def footer_button_callback(interaction):
                        if interaction.user != ctx.author:
                            embeda = discord.Embed(
                            description=f"Sorry, but this interaction can only be used by **{ctx.author.name}**.", color=0x3498DB)
                            return await interaction.response.send_message(embed=embeda, ephemeral=True)

                        ask = discord.Embed(description='**Enter the Footer Text** *(Use None to remove)*', color=discord.Color.blue())
                        await interaction.response.send_message(embed=ask)
                        footer = await self.bot.wait_for(
                        "message",
                        check=lambda x: x.channel.id == ctx.channel.id
                        and ctx.author.id == x.author.id,
                        timeout=None,
                    )
                        await self.bot.welcomer.upsert({"_id": interaction.guild.id, "footer": footer.content})
                        await ctx.channel.purge(limit=2)
                        
                        data = await self.bot.welcomer.get_by_id(interaction.guild.id)
                        if footer.content.lower() == 'none':
                            if data["title"].lower() == 'none' and data["description"].lower() == 'none':
                                footer_embed = discord.Embed(color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        footer_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        footer_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if footer.content.lower() != 'none':
                                        footer_embed.set_footer(text=footer.content)
                                except:
                                    pass

                            elif data["title"].lower() != 'none' and data["description"].lower() != 'none':
                                footer_embed = discord.Embed(title=data["title"], description=data["description"],color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        footer_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        footer_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if data["footer"].lower() != 'none':
                                        footer_embed.set_footer(text=data["footer"])
                                except:
                                    pass

                            elif data["title"].lower() == 'none' and data["description"].lower() != 'none':
                                footer_embed = discord.Embed(description=data["description"],color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        footer_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        footer_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if footer.content.lower() != 'none':
                                        footer_embed.set_footer(text=footer.content)
                                except:
                                    pass
                            elif data["title"].lower() != 'none' and data["description"].lower() == 'none':
                                footer_embed = discord.Embed(title=data["title"],color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        footer_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        footer_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if footer.content.lower() != 'none':
                                        footer_embed.set_footer(text=footer.content)
                                except:
                                    pass
                            
                            try:
                                await emb_embed.edit(embed=footer_embed, view=edit_view)
                            except:
                                footer_embed = discord.Embed(description='Use Buttons to Customize this Embed',color=discord.Color.blue())
                                try:
                                    if data["image"].lower() != 'none':
                                        footer_embed.set_image(url=data["image"])
                                except:
                                    pass
                                try:
                                    if data["thumbnail"].lower() != 'none':
                                        footer_embed.set_thumbnail(url=data["thumbnail"])
                                except:
                                    pass
                                try:
                                    if footer.content.lower() != 'none':
                                        footer_embed.set_footer(text=footer.content)
                                except:
                                    pass

                                await emb_embed.edit(embed=footer_embed, view=edit_view)

                        if data["title"].lower() == 'none' and data["description"].lower() == 'none':
                            footer_embed = discord.Embed(color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    footer_embed.set_image(url=data["image"])
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                await ctx.send(embed=errembed)
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    footer_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if footer.content.lower() != 'none':
                                    footer_embed.set_footer(text=footer.content)
                            except:
                                pass

                        elif data["title"].lower() != 'none' and data["description"].lower() != 'none':
                            footer_embed = discord.Embed(title=data["title"], description=data["description"], color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    footer_embed.set_image(url=data["image"])
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                await ctx.send(embed=errembed)
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    footer_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if footer.content.lower() != 'none':
                                    footer_embed.set_footer(text=footer.content)
                            except:
                                pass
                        elif data["title"].lower() == 'none' and data["description"].lower() != 'none':
                            footer_embed = discord.Embed(description=data["description"], color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    footer_embed.set_image(url=data["image"])
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                await ctx.send(embed=errembed)
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    footer_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if footer.content.lower() != 'none':
                                    footer_embed.set_footer(text=footer.content)
                            except:
                                pass
                        elif data["title"].lower() != 'none' and data["description"].lower() == 'none':
                            footer_embed = discord.Embed(title=data["title"], description=data["description"], color=discord.Color.blue())
                            try:
                                if data["image"].lower() != 'none':
                                    footer_embed.set_image(url=data["image"])
                            except:
                                errembed = discord.Embed(description='**Invalid URL !**', color=0x00ff0000)
                                d = await ctx.send(embed=errembed)
                                await asyncio.sleep(5)
                                try:
                                    await d.delete()
                                except:
                                    pass
                            try:
                                if data["thumbnail"].lower() != 'none':
                                    footer_embed.set_thumbnail(url=data["thumbnail"])
                            except:
                                pass
                            try:
                                if footer.content.lower() != 'none':
                                    footer_embed.set_footer(text=footer.content)
                            except:
                                pass
                            
                        await emb_embed.edit(embed=footer_embed, view=edit_view)
                    footer_button.callback = footer_button_callback

                    async def done_button_callback(interaction):
                        try:
                            await interaction.message.delete()
                        except:
                            pass
                    done_button.callback = done_button_callback

            edit_button.callback = edit_button_callback
            
        m_button.callback = m_button_callback

    @welcome.error
    async def welcome_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> You lack Administrator Permissions to use this Command**', color=0x00ff0000)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcomer(bot))