import discord
from discord.ext import commands
from discord.ui import Button, View
import requests
from nekobot import NekoBot
api = NekoBot()

class memeView(View):

    def __init__(self, ctx):
        super().__init__(timeout=20)
        self.ctx = ctx

    @discord.ui.button(label='Next Meme', style=discord.ButtonStyle.green, custom_id='meme')
    async def meme_callback(self, button, interaction):
        if interaction.user != self.ctx.author:
            embeda = discord.Embed(
            description=f"Sorry, but this interaction can only be used by **{self.ctx.author.name}**.", color=0x3498DB)
            return await interaction.response.send_message(embed=embeda, ephemeral=True)
        r = requests.get('https://memes.blademaker.tv/api?lang=en')
        res = r.json()
        title = res["title"]
        image = res["image"]
        ups = res["ups"]

        memeEmbed = discord.Embed(title=title, color=discord.Color.blue())
        memeEmbed.set_image(url=image)
        memeEmbed.url = 'https://discord.gg/zacxpxwhn8'
        memeEmbed.set_footer(text=f'👍 {ups}')

        await interaction.response.edit_message(embed=memeEmbed, view=self)
    
    @discord.ui.button(label='End Interaction', style=discord.ButtonStyle.danger, custom_id='end')
    async def end_callback(self, button, interaction):
        if interaction.user != self.ctx.author:
            embeda = discord.Embed(
            description=f"Sorry, but this interaction can only be used by **{self.ctx.author.name}**.", color=0x3498DB)
            return await interaction.response.send_message(embed=embeda, ephemeral=True)
        self.stop()
    



class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner Only Cog has been loaded\n-------------------------")

    @commands.command(usage='meme')
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def meme(self, ctx):
        view = memeView(ctx)
        r = requests.get('https://memes.blademaker.tv/api?lang=en')
        res = r.json()
        title = res["title"]
        image = res["image"]
        ups = res["ups"]

        memeEmbed = discord.Embed(title=f'{title}', color=discord.Color.blue())
        memeEmbed.set_image(url=image)
        memeEmbed.url = 'https://discord.gg/zacxpxwhn8'
        memeEmbed.set_footer(text=f'👍 {ups}')

        msg = await ctx.send(embed=memeEmbed, view=view)

        await view.wait()
        m = [x for x in view.children if x.custom_id == 'meme'][0]
        e = [x for x in view.children if x.custom_id == 'end'][0]
        m.disabled = True
        e.disabled = True
        await msg.edit(view=view)
    
    @commands.command(usage='threats [member]')
    async def threats(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.url
        img = (api.threats(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='bauguette [member]')
    async def bauguette(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.url
        img = (api.baguette(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    

    @commands.command(usage='cylde [member] [text]')
    async def clyde(self, ctx, *, text=None):
        if text is None:
            text = 'PyBot is OP'

        img = (api.clyde(f"{text}"))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}') 
        await ctx.send(embed=embed)   

    @commands.command(usage='captcha [member]')
    async def captcha(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.url
        img = (api.captcha(avatar, f"{member.name}"))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='trash [member]')
    async def trash(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.url
        img = (api.trash(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='iphone [member]')
    async def iphone(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.url
        img = (api.iphonex(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='tweet [member] [text]')
    async def tweet(self, ctx, member: discord.Member=None, *, text='PyBot is OP'):
        if member is None:
            member = ctx.author

        img = (api.tweet(f"{member.name}", f"{text}"))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)

    @commands.command(usage='animeface [member]')
    async def animeface(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.url
        img = (api.animeface(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='awooify [member]')
    async def awooify(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.url
        img = (api.awooify(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='deepfry [member]')
    async def deepfry(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.url
        img = (api.deepfry(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='stickbug [member]')
    async def stickbug(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.url
        img = (api.stickbug(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)

    @commands.command(usage='magik [member]')
    async def magik(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.url
        img = (api.magik(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)

    api.close()

def setup(bot):
    bot.add_cog(Fun(bot))