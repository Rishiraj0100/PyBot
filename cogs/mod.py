import discord
from discord.ext import commands
import time
import asyncio

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    @commands.command(name='clear', aliases=['purge', 'clean'], usage='clear <amount>', brief='$clear 100')
    @commands.has_guild_permissions(manage_messages=True)
    @commands.guild_only()
    async def clear(self, ctx, amount: int):
        """
        Clear Messages
        """
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount, check = lambda msg: not msg.pinned)
        msg = await ctx.send(f'**<a:tick:940816615237357608> Messages Purged!**')
        await asyncio.sleep(5)
        await msg.delete()

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            msg = await ctx.send('**Please Enter an Amount to Clear**')
            await asyncio.sleep(5)
            await msg.delete()
        
    @commands.command(name='ban', usage='ban <member> [reason]', brief='-ban @Ankush Get Out!')
    @commands.has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *,reason=None):
        """
        Ban a Member
        """
        await ctx.message.delete()
        if(member.id == ctx.author.id):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> You cannot ban Yourself**', color=0x00ff0000)
            return await ctx.send(embed=embed)

        if(ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner_id):
            embed = discord.Embed(description=f'**<a:cross1:941287490986315776> You cannot do this action on this user due to role hierarchy.**', colour=0xff0000)
            return await ctx.send(embed=embed)

        if(ctx.guild.me.top_role <= member.top_role or member.id == ctx.guild.owner_id):
            embed = discord.Embed(description=f'**<a:cross1:941287490986315776> My Highest Role ({ctx.guild.me.top_role.mention}) is below or equal to **{member.mention}**\'s Highest Role ({member.top_role.mention})**', colour=0xff0000)
            return await ctx.send(embed=embed)

        if(reason):
            embed = discord.Embed(description=f'<a:tick:940816615237357608> **{member} was Banned** | {reason}', color=0x3498DB)
            await ctx.send(embed=embed)
            memberembed = discord.Embed(description=f'**You have been banned from {ctx.guild.name}** for {reason}', color=0x3498DB)
            try:
                await member.send(embed=memberembed)
            except: 
                pass
            await member.ban(reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id}) - {reason}')
        else:
            embed = discord.Embed(description=f'<a:tick:940816615237357608> **{member} was Banned** | No Reason Given', color=0x3498DB)
            await ctx.send(embed=embed)
            memberembed = discord.Embed(description=f'**You have been banned from {ctx.guild.name}**', color=0x3498DB)
            try:
                await member.send(embed=memberembed)
            except:
                pass
            await member.ban(reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id})')
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> Please mention a Member in Server to Ban**', color=0x00ff0000)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> I dont have Permissions to Ban Members**', color=0x00ff0000)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> You lack Permissions to Ban Members**', color=0x00ff0000)
            await ctx.send(embed=embed)

    @commands.command(name='kick', usage='kick <member> [reason]', brief='-kick @Ankush Get Out!')
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, *,reason=None):
        """
        Kick a Member
        """
        await ctx.message.delete()
        if(member.id == ctx.author.id):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> You cannot kick Yourself**', color=0x00ff0000)
            return await ctx.send(embed=embed)

        if(member not in ctx.guild.members):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> Given Member is not in the Server.**', color=0x00ff0000)
            return await ctx.send(embed=embed)

        if(ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner_id):
            embed = discord.Embed(description=f'**<a:cross1:941287490986315776> You cannot do this action on this user due to role hierarchy.**', colour=0xff0000)
            return await ctx.send(embed=embed)

        if(ctx.guild.me.top_role <= member.top_role):
            embed = discord.Embed(description=f'**<a:cross1:941287490986315776> My Highest Role ({ctx.guild.me.top_role.mention}) is below or equal to **{member.mention}**\'s Highest Role ({member.top_role.mention})**', colour=0xff0000)
            return await ctx.send(embed=embed)

        if(reason):
            embed = discord.Embed(description=f'<a:tick:940816615237357608> **{member} was Kicked** | {reason}', color=0x3498DB)
            await ctx.send(embed=embed)
            memberembed = discord.Embed(description=f'**You have been kick from {ctx.guild.name}** for {reason}', color=0x3498DB)
            try:
                await member.send(embed=memberembed)
            except:
                pass
            await member.kick(reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id}) - {reason}')
        else:
            embed = discord.Embed(description=f'<a:tick:940816615237357608> **{member} was Kicked** | No Reason Given', color=0x3498DB)
            await ctx.send(embed=embed)
            memberembed = discord.Embed(description=f'**You have been kicked from {ctx.guild.name}**', color=0x3498DB)
            try:
                await member.send(embed=memberembed)
            except:
                pass
            await member.kick(reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id})')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> Please mention a Member to Kick**', color=0x00ff0000)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> I dont have Permissions to Kick Members**', color=0xff0000)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> You lack Permissions to Kick Members**', color=0xff0000)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.guild_only):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> This command can only be used in a Server**', color=0xff0000)
            await ctx.send(embed=embed)
    
    @commands.command(name='forceban', aliases=['hackban', 'fban'], usage='forceban <member_id> [reason]', brief='$forceban 731007992920539259 No Need')
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def forceban(self, ctx, member, *, reason=None):
        """
        Ban a member even if they are not in Server
        """
        try:
            member = int(member)
        except:
            embed = discord.Embed(description='**<a:cross1:941287490986315776> Please enter ID of the Member to Ban**', color=0x00ff0000)
            return await ctx.send(embed=embed)
        
        try:        
            member =  await self.bot.fetch_user(member)
        except:
            embed = discord.Embed(description='**<a:cross1:941287490986315776> Please enter ID of the Member to Ban**', color=0x00ff0000)
            await ctx.send(embed=embed)
        
        if(member in ctx.guild.members):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> Member is in the Server. Please try `ban` Command**', color=0x00ff0000)
            await ctx.send(embed=embed)
        
        if(reason):
            await ctx.guild.ban(member, reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id}) - {reason}')
            embed = discord.Embed(description=f'<a:tick:940816615237357608> **{member} was Banned** | {reason}', color=0x3498DB)
            await ctx.send(embed=embed)
            memberembed = discord.Embed(description=f'**You have been banned from {ctx.guild.name} for {reason}**', color=0x3498DB)
            try:
                await member.send(embed=memberembed)
            except:
                pass
        else:
            await ctx.guild.ban(member, reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id}')
            embed = discord.Embed(description=f'<a:tick:940816615237357608> **{member} was Banned** | No Reason Provided', color=0x3498DB)
            await ctx.send(embed=embed)
            memberembed = discord.Embed(description=f'**You have been banned from {ctx.guild.name}**', color=0x3498DB)
            try:
                await member.send(embed=memberembed)
            except:
                pass
    
    @forceban.error
    async def forceban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> Please enter ID of the Member to Ban**', color=0x00ff0000)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> I dont have Permissions to Ban Members**', color=0x00ff0000)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> You lack Permissions to Ban Members**', color=0x00ff0000)
            await ctx.send(embed=embed)

    @commands.command(name='unban', usage='unban <member> [reason]', brief='-unban 881473803899781120 Nice Guy')
    @commands.has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, member, *, reason=None):
        """
        Unban a Member
        """
        await ctx.message.delete()
        try:
            member = int(member)
        except:
            embed = discord.Embed(description='**<a:cross1:941287490986315776> Please enter ID of the Member to Unban**', color=0x00ff0000)
            return await ctx.send(embed=embed)
        try:        
            member =  await self.bot.fetch_user(member)
        except:
            embed = discord.Embed(description='**<a:cross1:941287490986315776> Please enter ID of the Member to Unban**', color=0x00ff0000)
            await ctx.send(embed=embed)

        if (member in ctx.guild.members):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> Member is in the Server**', color=0x00ff0000)
            await ctx.send(embed=embed)

        if(reason):
            await ctx.guild.unban(member, reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id}) - {reason}')
            embed = discord.Embed(description=f'<a:tick:940816615237357608> **{member} was Unbanned** | {reason}', color=0x3498DB)
            await ctx.send(embed=embed)
            memberembed = discord.Embed(description=f'**You have been unbanned from {ctx.guild.name} for {reason}**', color=0x3498DB)
            try:
                await member.send(embed=memberembed)
            except:
                pass
        else:
            await ctx.guild.unban(member, reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id}')
            embed = discord.Embed(description=f'<a:tick:940816615237357608> **{member} was Unbanned** | No Reason Provided', color=0x3498DB)
            await ctx.send(embed=embed)
            memberembed = discord.Embed(description=f'**You have been unbanned from {ctx.guild.name}**', color=0x3498DB)
            try:
                await member.send(embed=memberembed)
            except:
                pass

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> Please enter ID of the Member to Unban**', color=0x00ff0000)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> I dont have Permissions to Unban Members**', color=0x00ff0000)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> You lack Permissions to Unban Members**', color=0x00ff0000)
            await ctx.send(embed=embed)
    
    @commands.command(name='afk', usage='afk [reason]', brief='-afk Going Out')
    @commands.guild_only()
    async def afk(self, ctx, *,reason='I am AFK :)'):
        data = await self.bot.afk.get_by_id(ctx.author.id)
        if not data or "afk" not in data:
            if ctx.author.nick:
                a = ctx.author.nick
            else:
                a = ctx.author.name
            try:
                await ctx.author.edit(nick=f'[AFK] {a}')
            except:
                pass
            await ctx.reply(f'Your AFK is now set to: {reason}')
            await self.bot.afk.upsert({"_id": ctx.author.id, "afk": True})
            await self.bot.afk.upsert({"_id": ctx.author.id, "reason": reason})
            await self.bot.afk.upsert({"_id": ctx.author.id, "ping": []})
            await self.bot.afk.upsert({"_id": ctx.author.id, "time": time.time()})
            await self.bot.afk.upsert({"_id": ctx.author.id, "guild": ctx.guild.id})
            

def setup(bot):
    bot.add_cog(Moderation(bot))