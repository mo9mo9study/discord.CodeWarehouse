from discord.ext import commands
import datetime
import asyncio


class Bump(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content == "!d bump":
            await asyncio.sleep(0.5)
            if message.channel.last_message.author.id == 302050872383242240:
                two_hour_later = datetime.datetime.now() + datetime.timedelta(hours=2)
                await message.channel.send("次にbump出来る時間は" + two_hour_later.strftime("%H時%M分") + "です")


def setup(bot):
    return bot.add_cog(Bump(bot))
