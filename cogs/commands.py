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

    @commands.command(name="statistics", aliases=["stat", "stats", "details"])
    async def stats(self, ctx):
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
        embed.add_field(name='Bot Developers:', value="<@749559849460826112>")

        embed.set_footer(text=f"Stats | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url)

        await ctx.send(embed=embed)
       
    @commands.command(aliases=['disconnect', 'close', 'stopbot'])
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
        await self.bot.logout()

    @commands.command()
    async def echo(self, ctx, *, message=None):
        message = message or "Please provide the message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx, *, prefix='-'):
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
            embed = discord.Embed(description='**❌ You lack Administrator Permissions to use this command.**', color=0x00ff0000)
            await ctx.send(embed=embed)


    @commands.command(name="Ping", aliases=["latency", "speed", "p"])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def ping(self, ctx: commands.Context):
        start = time()
        message = await ctx.reply("Pinging...")
        end = time()
        await message.edit(
            content=f"Pong! latency: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms."
        )   


    
def setup(bot):
    bot.add_cog(Commands(bot))
