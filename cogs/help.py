import discord
from discord.ext import commands
from discord.ui import Button, View
import random

class Help(commands.Cog):
    """
    Sends this help message
    """

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Cog has loaded\n-------------------------")

    def __init__(self, bot):
        """! 
        Constructor
        @param bot The bot instance to be used.
        """
        self.bot = bot

    @commands.command(aliases=['h'], hidden=True)
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *params):
        """!
        Shows all modules of that bot
        
        @param ctx Context of the message.
        @param params further arguments
        """
        data = await self.bot.db.fetchrow('SELECT * FROM prefix WHERE guild_id = $1', ctx.guild.id)
        if not data:
            PREFIX = "-"
        else:
            PREFIX = data["prefix"]
        
        # checks if cog parameter was given
        # if not: sending all modules and commands not associated with a cog
        if not params:
            # checks if owner is on this server - used to 'tag' owner
            # starting to build embed
            invite = Button(label='Invite Me', style=discord.ButtonStyle.link, url='https://discord.com/api/oauth2/authorize?client_id=938699822922346536&permissions=21175985838&scope=bot')
            support = Button(label='Support Server', style=discord.ButtonStyle.link, url='https://discord.gg/WNJUBGvh4j')
            view = View()
            view.add_item(support)
            view.add_item(invite)

            emb = discord.Embed(color=0x2097d8,
                                description=f'⇛ Prefix for {ctx.guild.name} is `{PREFIX}`\n\n')
                                            # f'⇛ `{PREFIX} <command> for more information on a particular Command.`\n\n')
            ran = random.randint(1,2)
            if ran == 1:
                emb.set_footer(text='Made with 🤍 by Jash_2312 and Anshuman..!!', icon_url='https://images-ext-2.discordapp.net/external/9uZU0K1ngMtQgIElGm3XSqPOSxuty4T7ADJQ_kIbcpA/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/749559849460826112/cac1f6ee316353004c9e8bdce8a54b75.png')
            else:
                emb.set_footer(text='Made with 🤍 by Anshuman..!! and Jash_2312', icon_url='https://cdn.discordapp.com/avatars/939887303403405402/0ac574b14a954715efe8cd81196cb042.png')
            emb.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
            for cog in self.bot.cogs:
                # check if cog is the matching one
                if cog == 'Moderation' or cog == 'Channels' or cog == 'Welcomer' or cog == 'Utilities' or cog == 'Music' or cog == 'Fun':
                    # making title - getting description from doc-string below class
                    com = []
                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # if command is not hidden
                        if not command.hidden:
                            com.append(f'`{command.name}`')
                    try:
                        emb.add_field(name=f"{cog}", value=f"{', '.join(com)}", inline=False)
                    except:
                        pass
            
            await ctx.send(embed=emb, view=view)

            # setting information about author

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(params) == 1:

            # iterating trough cogs
            for cog in self.bot.cogs:
                # check if cog is the matching one
                if cog.lower() == params[0].lower():

                    # making title - getting description from doc-string below class
                    emb = discord.Embed(title=f'{cog} ({len(self.bot.get_cog(cog).get_commands())})',
                                        color=0x3498DB)

                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.add_field(name=f"`{PREFIX}{command.name}`", value=command.help, inline=False)
                    # found cog - breaking loop
                    break
    
            else: 
                for command in self.bot.commands:
                    if command.name.lower() == params[0].lower():
                        # print('Milgya')
                        
                        emb = discord.Embed(title=f'{command.name.capitalize()}',description=f'> {command.help}',color=0x2097d8)
                        # emb.add_field(name='**Command**', value=f'```{command.name}```', inline=False)
                        # emb.add_field(name='**Description**', value=f'`{command.help}`', inline=False)
                        if command.aliases:
                            emb.add_field(name='**Aliases**', value=f"`{', '.join(sorted(command.aliases))}`", inline=False)
                        else:
                            emb.add_field(name='**Aliases**', value=f"`None`", inline=False)

                        if command.usage:
                            emb.add_field(name='**Usage**', value=f'`{command.usage}`', inline=False)
                        else:
                            emb.add_field(name='**Usage**', value=f'`{PREFIX}{command.name}`', inline=False)
                                    
                        if command.brief:
                            emb.add_field(name='**Example**', value=f'```{command.brief}```', inline=False)
                        else:
                            emb.add_field(name='**Example**', value=f'```Command has No Example```', inline=False)

                        emb.add_field(name='\u200b', value='```yaml\n• [] = optional argument\n• <> = required argument\n• Do NOT type these when using commands!```')

                        emb.set_author(name=command.cog_name, icon_url=self.bot.user.display_avatar.url)
                        break
                    else:
                        for command in self.bot.commands:
                            for aliases in command.aliases:
                                if aliases.lower() == params[0].lower():
                                    emb = discord.Embed(title=f'{command.name.capitalize()}',description=f'> {command.help}',color=0x2097d8)

                                    if command.aliases:
                                        emb.add_field(name='**Aliases**', value=f"`{', '.join(command.aliases)}`", inline=False)
                                    else:
                                        emb.add_field(name='**Aliases**', value=f"`None`", inline=False)

                                    if command.usage:
                                        emb.add_field(name='**Usage**', value=f'`{command.usage}`', inline=False)
                                    else:
                                        emb.add_field(name='**Usage**', value=f'`None`', inline=False)
                                    
                                    if command.brief:
                                        emb.add_field(name='**Example**', value=f'```{command.brief}```', inline=False)
                                    else:
                                        emb.add_field(name='**Example**', value=f'```Command Has No Example```', inline=False)

                                    emb.set_author(name=command.cog_name, icon_url=self.bot.user.display_avatar.url)
                                    break
        # sending reply embed using our own function defined above
            await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Help(bot))