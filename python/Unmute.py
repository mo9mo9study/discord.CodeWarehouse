# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio
import setting

TOKEN           = setting.mToken

bot = commands.Bot(command_prefix="¥",help_command=None)

@bot.command()
async def m(ctx):
    await ctx.author.edit(mute=False)

bot.run(TOKEN)
