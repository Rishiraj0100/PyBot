from __future__ import annotations
import discord
from discord.ext import commands
import platform
import time
from time import time
import datetime
import random
import re
import _json

class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utilities Cog has been loaded\n-----")
        
    @commands.command(name="userinfo", aliases=["memberinfo", "ui", "mi"])
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def user_info(self, ctx: commands.Context, *, member: discord.Member = None):
        target = member or ctx.author
        roles = list(target.roles)
        embed = discord.Embed(
            title="User information",
            colour=target.colour,
            timestamp=datetime.datetime.utcnow(),
        )

        embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_footer(text=f"ID: {target.id}")
        fields = [
            ("Name", str(target), True),
            ("Created at", f"<t:{int(target.created_at.timestamp())}>", True),
            ("Status", f"{str(target.status).title()} [Blame Discord]", True),
            (
                "Activity",
                f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''} [Blame Discord]",
                True,
            ),
            ("Joined at", f"<t:{int(target.joined_at.timestamp())}>", True),
            ("Boosted", bool(target.premium_since), True),
            ("Bot?", target.bot, True),
            ("Nickname", target.display_name, True),
            (f"Top Role [{len(roles)}]", target.top_role.mention, True),
        ]
        perms = []
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        if target.guild_permissions.administrator:
            perms.append("Administrator")
        if (
            target.guild_permissions.kick_members
            and target.guild_permissions.ban_members
            and target.guild_permissions.manage_messages
        ):
            perms.append("Server Moderator")
        if target.guild_permissions.manage_guild:
            perms.append("Server Manager")
        if target.guild_permissions.manage_roles:
            perms.append("Role Manager")
        embed.description = f"Key perms: {', '.join(perms if perms else ['NA'])}"
        if target.banner:
            embed.set_image(url=target.banner.url)
        await ctx.reply(embed=embed)
    
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def roleinfo(self, ctx: commands.Context, *, role: discord.Role):
        embed = discord.Embed(
            title=f"Role Information: {role.name}",
            description=f"ID: `{role.id}`",
            color=role.color,
            timestamp=datetime.datetime.utcnow(),
        )
        data = [
            ("Created At", f"<t:{int(role.created_at.timestamp())}>", True),
            ("Is Hoisted?", role.hoist, True),
            ("Position", role.position, True),
            ("Managed", role.managed, True),
            ("Mentionalble?", role.mentionable, True),
            ("Members", len(role.members), True),
            ("Mention", role.mention, True),
            ("Is Boost role?", role.is_premium_subscriber(), True),
            ("Is Bot role?", role.is_bot_managed(), True),
        ]
        for name, value, inline in data:
            embed.add_field(name=name, value=value, inline=inline)
        perms = []
        if role.permissions.administrator:
            perms.append("Administrator")
        if (
            role.permissions.kick_members
            and role.permissions.ban_members
            and role.permissions.manage_messages
        ):
            perms.append("Server Moderator")
        if role.permissions.manage_guild:
            perms.append("Server Manager")
        if role.permissions.manage_roles:
            perms.append("Role Manager")
        embed.description = f"Key perms: {', '.join(perms if perms else ['NA'])}"
        embed.set_footer(text=f"ID: {role.id}")
        await ctx.reply(embed=embed)
        
    @commands.command(name='channelstats', aliases=['cs', 'channelinfo'], usage='channelstats', brief='-channelstats')
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channelstats(self, ctx):
        channel = ctx.channel
        embed = discord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}", color=random.choice(self.bot.color_list))
        embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel Id", value=channel.id, inline=False)
        embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
        embed.add_field(name="Channel Position", value=channel.position, inline=False)
        embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
        embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
        embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
        embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
        await ctx.reply(embed=embed)
    
    

def setup(bot):
    bot.add_cog(Utilities(bot))   