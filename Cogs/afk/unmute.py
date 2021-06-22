# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio

class Unmute(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def m(self,ctx):
        await ctx.author.edit(mute=False)
        print(f"[ {ctx.author.name} ]のサーバーミュートを解除しました")

def setup(bot):
    return bot.add_cog(Unmute(bot))