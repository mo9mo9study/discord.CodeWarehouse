from discord.ext import commands
import discord

import setting

intents = discord.Intents.all()
TOKEN = setting.dToken
#TOKEN = setting.tToken
prefix = "¥"

bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)

bot.load_extension("Cogs.default")

bot.load_extension("Cogs.Managements2.PersonalPin")

bot.run(TOKEN)
