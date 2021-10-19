import re
import unicodedata

from discord.ext import commands


class CreateStudyDesk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488  # mo9mo9 Guild Id
        self.CATEGORY_ID = 873317086439546900  # Study Space Category Id
        self.LOG_CHANNEL_ID = 801060150433153054  # 通知用 Channel Id
        self.CREATEDESK_CHANNEL_ID = 897995150926688286

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.CATEGORY = self.GUILD.get_channel(self.CATEGORY_ID)
        self.LOG_CHANNEL = self.GUILD.get_channel(self.LOG_CHANNEL_ID)
        self.CREATEDESK_CHANNEL = self.GUILD.get_channel(
            self.CREATEDESK_CHANNEL_ID)

    def vc_sort(self):
        vc_sorted_dict = {}
        vc_deskcreate_pos = 10
        for channel in self.CATEGORY.channels:
            if channel.name.startswith("もくもく勉強机"):
                r_d1 = re.compile(r"もくもく勉強机(\d).*")
                r_d2 = re.compile(r"もくもく勉強机(\d{2}).*")
                # 勉強机の席番が10〜
                if r_d2.match(channel.name):
                    vc_namenu = r_d2.match(channel.name)[1]
                    vc_sorted_dict[int(vc_namenu) + 1] = channel
                # 勉強机の席番が1〜9
                elif re.compile(r_d1).match(channel.name):
                    vc_namenu = unicodedata.normalize(
                        "NFKD", r_d1.match(channel.name)[1])
                    vc_sorted_dict[int(vc_namenu)] = channel
            # 勉強机を作成するチャンネル
            elif channel.name.endswith("勉強机を作成"):
                vc_sorted_dict[vc_deskcreate_pos] = channel
        return vc_sorted_dict

    async def edit_vcpos(self, vc_sorted_dict):
        for vc_pos in range(1, len(vc_sorted_dict)):
            channel = vc_sorted_dict[vc_pos]
            if vc_pos == channel.position:
                print("[DEBUG] 位置の変更なし")
            else:
                before_pos = channel.position
                await channel.edit(position=vc_pos)
                print(
                    f"[INFO] {channel.name}を位置({before_pos} -> {channel.position} )に変更")  # noqa: E501

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # [勉強机を作成]するチャンネルに参加した時
        if after.channel == self.CREATEDESK_CHANNEL and before.channel is None:
            empty_studydesk = []
            self.CATEGORY = self.GUILD.get_channel(self.CATEGORY_ID)
            studydesks = list(filter(lambda channel: channel.name.startswith(
                "もくもく勉強机"), self.GUILD.voice_channels))
            v_count = len(studydesks)
            m_count = 0
            for channel in studydesks:
                members = channel.members
                m_count = m_count + len(members)
                if 0 == len(members):
                    empty_studydesk.append(channel)
            print(f"[DEBUG] member: {v_count} / channel: {m_count}")
            # 勉強机の数と勉強机に参加している人数が同一の場合
            if not empty_studydesk:
                vc_sorted_dict = self.vc_sort()
                lastvc_pos = vc_sorted_dict[len(
                    self.CATEGORY.channels)].position
                create_channelname = f"もくもく勉強机{str(lastvc_pos)}"
                create_channelposition = lastvc_pos + 1
                new_studydesk = await self.CATEGORY.create_voice_channel(
                    name=create_channelname,
                    user_limit=1,
                    position=create_channelposition)
                await member.move_to(new_studydesk)
                log_msg = f"[INFO] {channel.name} を作成 (Before_studydeskCount: {v_count}"  # noqa: E501
                await self.LOG_CHANNEL.send(log_msg)
            # 勉強机に空きがある場合
            else:
                await member.move_to(empty_studydesk[0])
        elif before.channel != after.channel and before.channel is None:
            print("[DEBUG] 処理不要な入室時")
        # 勉強机10以降から退出した時
        # 退出時
        elif before.channel != after.channel and after.channel is None:
            # 参加していたチャンネルが勉強机の時
            if before.channel.name.startswith("もくもく勉強机"):
                r_d2 = re.compile(r"もくもく勉強机(\d{2}).*")
                # 机の席番が10以上のチャンネルから退出した時
                if r_d2.match(before.channel.name):
                    await before.channel.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def studydesk_posreset(self, ctx):
        self.CATEGORY = self.GUILD.get_channel(self.CATEGORY_ID)
        vc_sorted_dict = self.vc_sort()
        await self.edit_vcpos(vc_sorted_dict)


def setup(bot):
    return bot.add_cog(CreateStudyDesk(bot))
