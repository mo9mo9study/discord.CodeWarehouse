from discord.ext import commands


class CreateStudyDesk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488  # mo9mo9 Guild Id
        self.CATEGORY_ID = 873317086439546900  # Study Space Category Id
        self.LOG_CHANNEL_ID = 801060150433153054  # 通知用 Channel Id

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.CATEGORY = self.GUILD.get_channel(self.CATEGORY_ID)
        self.LOG_CHANNEL = self.GUILD.get_channel(self.LOG_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_voice_state_updat(self, member, before, after):
        count = 0
        if self.check_name(after.channel):
            vc_list = list(filter(lambda channel: channel.name.startswith(
                "もくもく勉強机"), self.GUILD.voice_channels))
            for channel in vc_list:
                members = channel.members
                count = count + len(members)
            print(len(vc_list))
            if len(vc_list) - count == 1:
                # vc_listで取得する最後の「もくもく勉強机」のポジションが正しいと信じて位置を取得
                studydesk_lastpos = vc_list[-1].position
                # 最後の「もくもく勉強机」のポジションの一つ下の位置の数字を変数化
                create_position = int(studydesk_lastpos) + 1
                create_channelname = f"もくもく勉強机{str(len(vc_list) + 1)}"
                channel = await self.CATEGORY.create_voice_channel(
                    name=create_channelname)
                await channel.edit(position=create_position, user_limit=1)
                log_msg = f"[INFO] {channel.name} を作成 (Before_studydeskCount: {len(vc_list)}"  # noqa: E501
                await self.LOG_CHANNEL.send(log_msg)

    def check_name(self, channel):
        try:
            if channel.name.startswith("もくもく勉強机"):
                return True
            else:
                return False
        except Exception as e:
            return False
            print(f"[ERROR] {e}")


def setup(bot):
    return bot.add_cog(CreateStudyDesk(bot))
