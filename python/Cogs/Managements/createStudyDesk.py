from discord.ext import commands
import discord
import asyncio

class CreateStudyDesk(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488 #mo9mo9 Guild Id
        self.CATEGORY_ID = 603582455756095491 #Study Space Category Id
        self.ANNOUNCE_CHANNEL_ID = 801060150433153054 #通知用 Channel Id

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.CATEGORY = self.GUILD.get_channel(self.CATEGORY_ID)
        self.ANNOUNCE_CHANNEL = self.GUILD.get_channel(self.ANNOUNCE_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        count = 0
        if self.check_name(after.channel):
            vc_list = list(filter(lambda channel: channel.name[0:7] == "もくもく勉強机", self.GUILD.voice_channels))
            for channel in vc_list:
                members = channel.members
                count = count + len(members)
            print(len(vc_list))
            if len(vc_list) - count == 1:
                # vc_listで取得する最後の「もくもく勉強机」のポジションが正しいと信じて位置を取得
                studydesk_lastpos = vc_list[-1].position
                # 最後の「もくもく勉強机」のポジションの一つ下の位置の数字を変数化
                create_position = int(studydesk_lastpos) + 1
                channel = await self.CATEGORY.create_voice_channel(name=f"もくもく勉強机{str(len(vc_list) + 1)}")
                await channel.edit(position=create_position, user_limit=1)
                await self.ANNOUNCE_CHANNEL.send(f"{channel.name}を作成しました : id `{channel.id}`")
                await self.ANNOUNCE_CHANNEL.send(f"勉強机作成前の合計勉強机数:{len(vc_list)}")

    def check_name(self,channel):
        try:
            if channel.name[0:7] == "もくもく勉強机":
                return True
            else:
                return False
        except Exception as e:
            return False

def setup(bot):
    return bot.add_cog(CreateStudyDesk(bot))