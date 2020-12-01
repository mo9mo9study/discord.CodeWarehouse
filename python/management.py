# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio
import sys

TOKEN = '' #TOKENを入力してください
prefix = "/" #お好きなプレフィックス

bot = commands.Bot(command_prefix=prefix,help_command=None)

sys.path.append('..')
bot.load_extension("Cogs.default")
bot.load_extension("Cogs.Managements.voiceChannelJoinLeave_roleModify")

bot.run(TOKEN)