import discord
from discord.ext import commands
import time
class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name='kick', usage='kick <member> [reason]', brief='$kick @Ankush Get Out!')
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, *,reason=None):
        """
        Kick a Member
        """
        await ctx.message.delete()
        if(member.id == ctx.author.id):
            embed = discord.Embed(description='**❌ You cannot kick Yourself**', color=0x3498DB)
            return await ctx.send(embed=embed)

        if(member not in ctx.guild.members):
            embed = discord.Embed(description='**❌ Given Member is not in the Server.**', color=0x3498DB)
            return await ctx.send(embed=embed)

        if(ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner_id):
            embed = discord.Embed(description=f'**❌ You cannot do this action on this user due to role hierarchy.**', colour=0xff0000)
            return await ctx.send(embed=embed)

        if(ctx.guild.me.top_role <= member.top_role):
            embed = discord.Embed(description=f'**❌ My Highest Role ({ctx.guild.me.top_role.mention}) is below or equal to **{member.mention}**\'s Highest Role ({member.top_role.mention})**', colour=0xff0000)
            return await ctx.send(embed=embed)

        if(reason):
            embed = discord.Embed(description=f'<a:tick:940816615237357608> **{member} was Kicked** | {reason}', color=0xff0000)
            await ctx.send(embed=embed)
            memberembed = discord.Embed(description=f'**You have been kick from {ctx.guild.name}** for {reason}', color=0xff0000)
            try:
                await member.send(embed=memberembed)
            except:
                pass
            await member.kick(reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id}) - {reason}')
        else:
            embed = discord.Embed(description=f'<a:tick:940816615237357608> **{member} was Kicked** | No Reason Given', color=0xff0000)
            await ctx.send(embed=embed)
            memberembed = discord.Embed(description=f'**You have been kicked from {ctx.guild.name}**', color=0xff0000)
            try:
                await member.send(embed=memberembed)
            except:
                pass
            await member.kick(reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id})')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='**❌ Please mention a Member to Kick**', color=0x3498DB)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(description='**❌ I dont have Permissions to Kick Members**', color=0x3498DB)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='**❌ You lack Permissions to Kick Members**', color=0x3498DB)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.guild_only):
            embed = discord.Embed(description='**❌ This command can only be used in a Server**', color=0x3498DB)
            await ctx.send(embed=embed)
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(user=member, reason=reason)

        channel = self.bot.get_channel(704301090471936253)
        embed = discord.Embed(title=f"{ctx.author.name} banned: {member.name}", description=reason)
        await channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member, *, reason=None):
        member = await self.bot.fetch_user(int(member))
        await ctx.guild.unban(member, reason=reason)

        channel = self.bot.get_channel(704301090471936253)
        embed = discord.Embed(title=f"{ctx.author.name} unbanned: {member.name}", description=reason)
        await channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, amount=15):
        await ctx.channel.purge(limit=amount+1)

        channel = self.bot.get_channel(704301090471936253)
        embed = discord.Embed(title=f"{ctx.author.name} purged: {ctx.channel.name}", description=f"{amount} messages were cleared")
        await channel.send(embed=embed)
    
    @commands.command(name='afk', usage='afk [reason]', brief='-afk Going Out')
    @commands.guild_only()
    async def afk(self, ctx, *,reason='I am AFK :)'):
        data = await self.bot.afk.get_by_id(ctx.author.id)
        # if not data or "afk" not in data:
        if ctx.author.nick:
            a = ctx.author.nick
        else:
            a = ctx.author.name
        try:
            await ctx.author.edit(nick=f'[AFK] {a}')
        except:
            pass
        await self.bot.afk.upsert({"_id": ctx.author.id, "afk": True})
        await self.bot.afk.upsert({"_id": ctx.author.id, "reason": reason})
        await self.bot.afk.upsert({"_id": ctx.author.id, "ping": []})
        await self.bot.afk.upsert({"_id": ctx.author.id, "time": time.time()})
        if data or "guild" in data:
            l = data["guild"]
            if ctx.guild.id in l:
                return
            l.append(ctx.guild.id)
            await self.bot.afk.upsert({"_id": ctx.author.id, "guild": l})
        else:
            await self.bot.afk.upsert({"_id": ctx.author.id, "guild": []})
        await ctx.reply(f'Your AFK is now set to: {reason}')

def setup(bot):
    bot.add_cog(Moderation(bot))
