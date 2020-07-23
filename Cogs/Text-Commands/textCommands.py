import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import wikipedia


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)


class textCommands(commands.Cog, name="text-commands Cog"):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        # bot.help_command = MyHelpCommand()
        # bot.help_command.cog = self
        self.bot = bot

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @commands.command(name="ping")
    async def ping(self, ctx, arg):
        await ctx.send("pong" + arg, delete_after=5)

    @commands.command(name="wiki")
    async def wiki(self, ctx):
        query = ctx.message.content.split(" ", 1)[1]  # removes the !wiki part
        lang, query = await self.setlang(query)

        await self.printout(ctx.message, query, lang)

    async def printout(self, message, query, lang):
        wikipage = None
        lookup = True
        disambiguation = False
        print("printout")

        wikipedia.set_lang(lang)

        try:
            wikipage = wikipedia.page(query)
            print("I found directly")

        except wikipedia.PageError:
            print("Can't access by default. Trying to search")

        except wikipedia.DisambiguationError:
            await message.channel.send("This query leads to a disambiguation page. Please be more specific.")
            disambiguation = True

        except Exception:
            lookup = False

        if wikipage is None and lookup and not disambiguation:
            wikipage = wikipedia.suggest(query)


        if wikipage is None and lookup and not disambiguation:
            await message.channel.send("Sorry, cannot find " + query + " :v")
        elif not lookup:
            await message.channel.send("Something went wrong. Check the language, or maybe I can't reach Wikipedia")
        else:
            imglist = wikipage.images
            if len(imglist) == 0:
                print("no pics :(")
                em = discord.Embed(title=wikipage.title, description=wikipedia.summary(query, sentences=40),
                                   colour=0x2DAAED,
                                   url=wikipage.url)
            else:
                print(len(imglist))
                print(imglist[0])
                em = discord.Embed(title=wikipage.title, description=wikipedia.summary(query, sentences=40),
                                   colour=0x2DAAED,
                                   url=wikipage.url, image=imglist[0])
                em.set_thumbnail(url=imglist[0])
            em.set_author(name=self.bot.user.name, icon_url="")
            await message.channel.send( embed=em)
            await message.channel.send( "More at <" + wikipage.url + ">")

        wikipedia.set_lang("en")

    async def setlang(self, query):
        if len(query) <= 3 or query[2] != " ":
            return "en", query
        else:
            lang = query[0] + query[1]
            nquery = query[3:]
            return lang, nquery

    @commands.command(name="edenzero")
    async def edenzero(self,ctx,lang="en"):
        if len(lang)>2:
            lang="en"

        await self.printout(ctx.message, " eden zero ", lang)

    @commands.command(name="kick")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, arg, arg2="Not specified"):  # arg is used for the @mention arg2 is the reason

        user = ctx.message.guild.get_member(ctx.message.mentions[0].id)
        await user.kick(reason=arg2)
        await user.send("U got kicked from " + ctx.message.guild.name + " \n Reason for kick: " + arg2)

    @kick.error
    async def kick_error(self, ctx, error):
        print(type(error))
        # if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!", delete_after=5)


def setup(bot):
    bot.add_cog(textCommands(bot))
