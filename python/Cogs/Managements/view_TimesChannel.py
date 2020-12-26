from discord.ext import commands
import discord
import asyncio

class ViewTimesChannel(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.guild_id = 603582455756095488
        self.channel_id = 792369191843135488 #下のメッセージがあるchannelのid
        self.second = 5

    # 移動用のembedメッセージ
    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_guild(self.guild_id).get_channel(self.channel_id)
        await self.channel.purge()

        embed = discord.Embed(title="各自timesへの移動を簡単にします", description="- あなたのtimesへのリンク(移動手段)を5秒表示します")
        embed.add_field(name=" 👇 使い方", value="（超簡単）このメッセージにリアクションをするだけ‼️ ")
        self.message = await self.channel.send(embed=embed)
        self.message_id = self.message.id
        await self.message.add_reaction("🛎️")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.member.bot:
            return
        if payload.message_id == self.message_id:
            member_id = payload.member.id
            select_msg = await self.channel.fetch_message(payload.message_id)

            for times_channel in payload.member.guild.text_channels:
                if times_channel.topic == str(member_id):
                    msg = await self.channel.send(times_channel.mention)
                    await self.time_sleep(msg)
                    await select_msg.remove_reaction(payload.emoji, payload.member)
                    break
            else:
                msg = await self.channel.send("timesチャンネルが見つかりませんでした。")
                await self.time_sleep(msg)

    async def time_sleep(self,msg):
        await asyncio.sleep(self.second)
        await msg.delete()

def setup(bot):
    return bot.add_cog(ViewTimesChannel(bot))