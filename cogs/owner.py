import discord
from discord.ext import commands


class OwnerOnly(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner Only Cog has been loaded\n-------------------------")


    @commands.command(name='blacklist', aliases=['bl'], hidden=True)
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        # if ctx.message.author.id == user.id:
        #     await ctx.send("Hey!, you cannot blacklist yourself!")
        #     return
        record = await self.bot.db.fetchrow('SELECT * FROM blacklist WHERE (user_id) = ($1)', user.id)
        if record:
            return await ctx.send(f'**{user.name}** is already Blacklisted!')
        await self.bot.db.execute("INSERT INTO blacklist (user_id) VALUES ($1)", user.id)
        await ctx.send(f'Blacklisted **{user.name}**')


    @commands.command(name='whitelist', aliases=['wl'], hidden=True)
    @commands.is_owner()
    async def whitelist(self, ctx, user: discord.Member):
        record = await self.bot.db.fetchrow('SELECT * FROM blacklist WHERE (user_id) = ($1)', user.id)
        if not record:
            return await ctx.send(f'**{user.name}** is not Blacklisted!')
        await self.bot.db.execute('DELETE FROM blacklist WHERE (user_id) = ($1)', user.id)
        return await ctx.send(f'Whitelisted **{user.name}**')


    @commands.command(name='changeStatus', aliases=['status'], hidden=True)
    @commands.is_owner()
    async def status(self, ctx, status=None, *, message=None):
        """
        Change Status of Bot
        """
        message = message or f"Hi, my name is {self.bot.user.name}.\nUse - to interact with me!"
        status = status or 'p'

        if status.startswith('w'):
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching , name=message))
            await ctx.message.add_reaction('<a:tick:940816615237357608>')
        elif status.startswith('p'):
            await self.bot.change_presence(activity=discord.Game(name=message))
            await ctx.message.add_reaction('<a:tick:940816615237357608>')
        elif status.startswith('l'):
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=message))
            await ctx.message.add_reaction('<a:tick:940816615237357608>')
        elif status.startswith('c'):
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=message))
            await ctx.message.add_reaction('<a:tick:940816615237357608>')
        else:
            await self.bot.change_presence(activity=discord.Game(name=message))
            await ctx.message.add_reaction('<a:tick:940816615237357608>')

def setup(bot):
    bot.add_cog(OwnerOnly(bot))