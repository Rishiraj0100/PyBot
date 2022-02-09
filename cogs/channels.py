import discord
from discord.ext import commands
import random

class Channels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def new(self, ctx):
        await ctx.send("Invalid sub-command passed.")

    @new.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def category(self, ctx, role: discord.Role, *, name):
        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
        role: discord.PermissionOverwrite(read_messages=True)
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.send(f"Hey dude, I made {category.name} for ya!")

    @new.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channel(self, ctx, role: discord.Role, *, name):
        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
        role: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites, category=self.bot.get_channel(709002944879656960))
        await ctx.send(f"Hey dude, I made {channel.name} for ya!")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def delete(self, ctx):
        await ctx.send("Invalid sub-command passed.")

    @delete.command(name='category')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _category(self, ctx, category: discord.CategoryChannel, *, reason=None):
        await category.delete(reason=reason)
        await ctx.send(f"Hey man! I deleted {category.name} for ya!")

    @delete.command(name='channel')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _channel(self, ctx, channel: discord.TextChannel=None, *, reason=None):
        channel = channel or ctx.channel
        await channel.delete(reason=reason)
        await ctx.send(f"Hey man! I deleted {channel.name} for ya!")

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"I have put `{channel.name}` on lockdown.")
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have put `{channel.name}` on lockdown.")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have removed `{channel.name}` from lockdown.")

def setup(bot):
    bot.add_cog(Channels(bot))
