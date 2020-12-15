from discord.ext import commands
import discord
import asyncio

class ViewTimesChannel(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.channel_id = 771006468216193064 #下のメッセージがあるchannelのid
        self.message_id = 788352614517309461 #リアクションを押す用のメッセージid
        self.second = 10

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.message_id == self.message_id:
            member_id = payload.member.id
            select_channel = payload.member.guild.get_channel(self.channel_id)
            for channel in payload.member.guild.text_channels:
                if channel.topic == str(member_id):
                    msg = await select_channel.send(channel.mention)
                    await self.time_sleep(msg)
                    break
            else:
                msg = await select_channel.send("timesチャンネルが見つかりませんでした。")
                await self.time_sleep(msg)

    async def time_sleep(self,msg):
        await asyncio.sleep(self.second)
        await msg.delete()

def setup(bot):
    return bot.add_cog(ViewTimesChannel(bot))