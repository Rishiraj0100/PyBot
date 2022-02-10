from __future__ import annotations
import discord
from discord.ext import commands
import platform
import time
from time import time
import datetime
import re
import _json

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has been loaded\n-----")

    @commands.command(name="stats", aliases=["statistics", "st", "info"], usage='stats', brief='-stats')
    async def stats(self, ctx):
        """Shows some usefull information about PyBot"""
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = sum(guild.member_count for guild in self.bot.guilds)

        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value=self.bot.version)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        jash = await self.bot.fetch_user(749559849460826112)
        anshuman = await self.bot.fetch_user(939887303403405402)
        if jash in ctx.guild.members:
            j = f'{jash.mention}'
        else:
            j = f'**{jash}**'
        if anshuman in ctx.guild.members:
            a = f'{anshuman.mention}'
        else:
            a = f'**{anshuman}**'
        embed.add_field(name='Bot Developers:', value=f"**{j}**\n**{a}**")
        embed.set_footer(text=f"Stats | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url)

        await ctx.send(embed=embed)
       
    @commands.command(name="logout", aliases=["disconnect", "shutdown"], usage='logout', brief='-logout')
    @commands.is_owner()
    async def logout(self, ctx):
        """Logout the bot (owner only)"""
        await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
        await self.bot.logout()

    @commands.command()
    async def echo(self, ctx, *, message=None):
        """repeats your message"""
        message = message or "Please provide the message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name="prefix", aliases=["pre"], usage='prefix [newprefix]', brief='-prefix !')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx, *, prefix='-'):
        """To check the current prefix or change it to a new one"""
        if(prefix == None):
            data = await self.bot.prefix.get_by_id(ctx.guild.id)
            if not data or "prefix" not in data:
                prefix = "-"
            else:
                prefix = data["prefix"]
            await ctx.send(f'My prefix for this server is `{prefix}`\nYou can start with `{prefix}help`')
        else:
            await self.bot.prefix.upsert({"_id": ctx.guild.id, "prefix": prefix})
            await ctx.send(f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!")
    
    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> You lack Administrator Permissions to use this command.**', color=0x00ff0000)
            await ctx.send(embed=embed)


    @commands.command(name="ping", aliases=["latency", "speed", "p"], usage='ping', brief='-ping')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def ping(self, ctx: commands.Context):
        """Shows the Latency of the bot"""
        start = time()
        message = await ctx.reply("Pinging...")
        end = time()
        await message.edit(
            content=f"Pong! latency: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms."
        )   


    
def setup(bot):
    bot.add_cog(Commands(bot))
