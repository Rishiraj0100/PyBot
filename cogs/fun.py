from code import interact
from os import getloadavg
from socket import timeout
import discord
from discord.ext import commands
from discord.ui import Button, View
import requests

from cogs.music import MyView

class memeView(View):

    def __init__(self):
        super().__init__(timeout=20)

    @discord.ui.button(label='Next Meme', style=discord.ButtonStyle.green, custom_id='meme')
    async def meme_callback(self, button, interaction):
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
        self.stop()
    
    # async def on_timeout(self) -> None:
    #     memeButton = [x for x in self.children if x.custom_id == 'meme'][0]
    #     end = [x for x in self.children if x.custom_id == 'end'][0]
    #     end.disabled = True
    #     memeButton.disabled = True
    #     return await self.message.edit(view=self)


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner Only Cog has been loaded\n-------------------------")

    @commands.command(usage='meme')
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def meme(self, ctx):
        view = memeView()
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

def setup(bot):
    bot.add_cog(Fun(bot))