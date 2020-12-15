from discord.ext import commands
import discord
import asyncio
import yaml

class Emoji(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        with open('Settings/emoji.yaml',encoding="utf-8") as file:
            self.emojis = yaml.safe_load(file.read())

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return
        for emoji in self.emojis:
            if message.content == emoji:
                await message.add_reaction(emoji)

def setup(bot):
    return bot.add_cog(Emoji(bot))
