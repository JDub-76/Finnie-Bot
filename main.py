import discord
import configparser
from discord.ext import commands


config = configparser.ConfigParser()
config.read('main-config.ini')

bot = commands.Bot(command_prefix=config["BOT-INFO"]["prefix"])
for cog in config["COGS"]:
    print(config["COGS"][cog])

    bot.load_extension("Cogs." + config["COGS"][cog])


@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))


bot.run(config["BOT-INFO"]["botToken"], bot="True", reconnect=True)
