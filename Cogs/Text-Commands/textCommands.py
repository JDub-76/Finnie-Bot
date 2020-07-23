from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)


class textCommands(commands.Cog, name="text-commands Cog"):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        # bot.help_command = MyHelpCommand()
        # bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @commands.command(name="ping")
    async def ping(self, ctx, arg):
        await ctx.send("pong" + arg)

    @commands.command(name="kick")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, arg,arg2="Not specified"): #arg is used for the @mention

        user = ctx.message.guild.get_member(ctx.message.mentions[0].id)
        await user.kick(reason=arg2)
        await user.send("U got kicked from " + ctx.message.guild.name + " \n Reason for kick: " + arg2)


    @kick.error
    async def kick_error(self, ctx, error):

        print(type(error))
        #if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")

def setup(bot):
    bot.add_cog(textCommands(bot))
