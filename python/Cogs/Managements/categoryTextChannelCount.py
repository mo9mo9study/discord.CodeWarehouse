from discord.ext import commands
import discord
import asyncio

class CategoryTextChannelCount(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)

    @commands.command()
    async def cc(self, ctx, id_):
        category = self.GUILD.get_channel(int(id_))
        try:
            channels = category.text_channels
        except AttributeError:
            await ctx.send("CategoryChannelが取得できませんでした。")
        else:
            count = len(channels)
            await ctx.send(f"{category.name}の現在のチャンネル数は{count}chです")

def setup(bot):
    return bot.add_cog(CategoryTextChannelCount(bot))