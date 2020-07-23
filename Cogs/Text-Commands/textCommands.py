from discord.ext import commands



class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

class textCommands(commands.Cog, name="text-commands Cog"):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @commands.command(name="ping")
    async def ping(self,ctx,arg):
        await ctx.send("pong"+arg)

def setup(bot):
    bot.add_cog(textCommands(bot))