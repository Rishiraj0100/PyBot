from __future__ import annotations
import discord
from discord.ext import commands
import typing
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
        
    @commands.command(name="channelstats", aliases=["channelinfo", "cs", "ci"], usage='channelstats [channel]', brief='-channelstats #general')
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def channel_info(
        self,
        ctx: commands.Context,
        *,
        channel: typing.Union[
            discord.TextChannel,
            discord.VoiceChannel,
            discord.CategoryChannel,
            discord.StageChannel,
        ] = None,
    ):
        channel = channel or ctx.channel
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
        await ctx.send(embed=embed)
    
    @commands.command(name="serverinfo", aliases=["guildinfo", "si", "gi"])
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def server_info(self, ctx: commands.Context):
        """
        Get the basic stats about the server
        """
        guild = ctx.guild
        embed = discord.Embed(
            title=f"Server Info: {ctx.guild.name}",
            colour=ctx.guild.owner.colour,
            timestamp=datetime.datetime.utcnow(),
        )

        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f"ID: {ctx.guild.id}")
        statuses = [
            len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members))),
        ]

        fields = [
            ("Owner", ctx.guild.owner, True),
            ("Region", str(ctx.guild.region).capitalize(), True),
            ("Created at", f"<t:{int(ctx.guild.created_at.timestamp())}>", True),
            (
                "Total Members",
                f"Members: {len(ctx.guild.members)}\nHumans: {len(list(filter(lambda m: not m.bot, ctx.guild.members)))}\nBots: {len(list(filter(lambda m: m.bot, ctx.guild.members)))} ",
                True,
            ),
            (
                "Total channels",
                f"Categories: {len(ctx.guild.categories)}\nText: {len(ctx.guild.text_channels)}\nVoice:{len(ctx.guild.voice_channels)}",
                True,
            ),
            (
                "General",
                f"Roles: {len(ctx.guild.roles)}\nEmojis: {len(ctx.guild.emojis)}\nBoost Level: {ctx.guild.premium_tier}",
                True,
            ),
            (
                "Statuses",
                f":green_circle: {statuses[0]}\n:yellow_circle: {statuses[1]}\n:red_circle: {statuses[2]}\n:black_circle: {statuses[3]} [Blame Discord]",
                True,
            ),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        info = []
        features = set(ctx.guild.features)
        all_features = {
            "PARTNERED": "Partnered",
            "VERIFIED": "Verified",
            "DISCOVERABLE": "Server Discovery",
            "COMMUNITY": "Community Server",
            "FEATURABLE": "Featured",
            "WELCOME_SCREEN_ENABLED": "Welcome Screen",
            "INVITE_SPLASH": "Invite Splash",
            "VIP_REGIONS": "VIP Voice Servers",
            "VANITY_URL": "Vanity Invite",
            "COMMERCE": "Commerce",
            "LURKABLE": "Lurkable",
            "NEWS": "News Channels",
            "ANIMATED_ICON": "Animated Icon",
            "BANNER": "Banner",
        }

        for feature, label in all_features.items():
            if feature in features:
                info.append(f":ballot_box_with_check: {label}")

        if info:
            embed.add_field(name="Features", value="\n".join(info))

        if guild.premium_tier != 0:
            boosts = (
                f"Level {guild.premium_tier}\n{guild.premium_subscription_count} boosts"
            )
            last_boost = max(
                guild.members, key=lambda m: m.premium_since or guild.created_at
            )
            if last_boost.premium_since is not None:
                boosts = f"{boosts}\nLast Boost: {last_boost} ({commands.format_relative(last_boost.premium_since)})"
            embed.add_field(name="Boosts", value=boosts, inline=True)
        else:
            embed.add_field(name="Boosts", value="Level 0", inline=True)

        

        if ctx.guild.me.guild_permissions.ban_members:
            embed.add_field(
                name="Banned Members",
                value=f"{len(await ctx.guild.bans())}",
                inline=True,
            )
        if ctx.guild.me.guild_permissions.manage_guild:
            embed.add_field(
                name="Invites", value=f"{len(await ctx.guild.invites())}", inline=True
            )

        if ctx.guild.banner:
            embed.set_image(url=ctx.guild.banner.url)

        await ctx.send(embed=embed)
        
    @commands.command(name="emojiinfo", aliases=["emoji", "ei", "emo"],  usage='emojiinfo <emoji>', brief='-emojiinfo <a:emoji_54:938009504329658388>')
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def emojiinfo(self, ctx: commands.Context, *, emoji: discord.Emoji):
        """To get the info regarding the server emoji"""
        em = discord.Embed(
            title="Emoji Info",
            description=f"• [Download the emoji]({emoji.url})\n• Emoji ID: `{emoji.id}`",
            timestamp=datetime.datetime.utcnow(),
            color=ctx.author.color,
        )
        data = [
            ("Name", emoji.name, True),
            ("Is Animated?", emoji.animated, True),
            ("Created At", f"<t:{int(emoji.created_at.timestamp())}>", True),
            ("Server Owned", emoji.guild.name, True),
            ("Server ID", emoji.guild_id, True),
            ("Created By", emoji.user if emoji.user else "User Not Found", True),
            ("Available?", emoji.available, True),
            ("Managed by Twitch?", emoji.managed, True),
            ("Require Colons?", emoji.require_colons, True),
        ]
        em.set_footer(text=f"{ctx.author}")
        em.set_thumbnail(url=emoji.url)
        for name, value, inline in data:
            em.add_field(name=name, value=f"{value}", inline=inline)
        await ctx.reply(embed=em)


def setup(bot):
    bot.add_cog(Utilities(bot))   