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
        self.CATEGORY = self.GUILD.get_channel(self.CATEGORY_ID)
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

    def desk_missing_number(self) -> int or False:
        desk_numbers = []
        for channel in self.CATEGORY.channels:
            if channel.name.startswith("もくもく勉強机"):
                r_d2 = re.compile(r"もくもく勉強机(\d{2}).*")
                if r_d2.match(channel.name):
                    vc_namenu = r_d2.match(channel.name)[1]
                    desk_numbers.append(int(vc_namenu))
        # 勉強机10以上が存在有無
        if not desk_numbers:
            print("[DEBUG] 勉強机10以降が存在しません")
            return False
        else:
            for i in range(10, max(desk_numbers)+1):
                if i not in desk_numbers:
                    # 欠番がある場合
                    print(f"[INFO] 勉強机10以上の連番に {i} 席番の欠番を発見しました")  # noqa: E501
                    return i
        print("[DEBUG] 欠番はありませんでした")
        return False

    async def edit_vcpos(self, vc_sorted_dict):
        for vc_pos in vc_sorted_dict.keys():
            channel = vc_sorted_dict[vc_pos]
            if vc_pos == channel.position:
                print(f"[DEBUG] {channel.name}:{channel.position} 位置の変更なし")
            else:
                before_pos = channel.position
                await channel.edit(position=vc_pos)
                print(
                    f"[INFO] {channel.name}を位置({before_pos} -> {channel.position} )に変更")  # noqa: E501

    def check_pos(self):
        self.CATEGORY = self.GUILD.get_channel(self.CATEGORY_ID)
        for channel in self.CATEGORY.channels:
            vcpos_diffarent = []
            r_d1 = re.compile(r"もくもく勉強机(\d).*")
            r_d2 = re.compile(r"もくもく勉強机(\d{2}).*")
            # 勉強机の席番が10〜
            if r_d2.match(channel.name):
                vc_namenu = r_d2.match(channel.name)[1]
                print(
                    f"[DEBUG: high] {channel.name}/{vc_namenu}:{channel.position}")  # noqa: E501
                vc_pos = int(vc_namenu)
                if (vc_pos + 1) != channel.position:
                    diff_msg = f"{channel.name}/{vc_namenu}:{channel.position}"
                    vcpos_diffarent.append(diff_msg)
            # 勉強机の席番が1〜9
            elif re.compile(r_d1).match(channel.name):
                vc_namenu = unicodedata.normalize(
                    "NFKD", r_d1.match(channel.name)[1])
                print(
                    f"[DEBUG: high] {channel.name}/{vc_namenu}:{channel.position}")  # noqa: E501
                if int(vc_namenu) != channel.position:
                    diff_msg = f"{channel.name}:{channel.position}"
                    vcpos_diffarent.append(diff_msg)
        if vcpos_diffarent:
            print(
                f"[DEBUG] 配置場所が異なる勉強机を発見({','.join(map(str, vcpos_diffarent))})")  # noqa: E501
            return True
        else:
            print("[DEBUG] 正常に配置されています")
            return False

    async def boolif_runedit(self):
        # 机の番号とpositionの番号に相違あるかどうか
        if self.check_pos():
            vc_sorted_dict = self.vc_sort()
            await self.edit_vcpos(vc_sorted_dict)
        print("[DEBUG] 勉強机の順番整理完了")

    async def create_studydesk(self, member):
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
        # empty_studydesk.clear()  # 擬似的な満席
        if not empty_studydesk:
            # 10以降の連番に欠番が存在するかどうか
            create_channelposition = self.desk_missing_number()
            if not create_channelposition:  # 10over, False
                # 連番に欠番が存在しない時
                vc_sorted_dict = self.vc_sort()
                lastvc_pos = vc_sorted_dict[len(
                    self.CATEGORY.channels)].position
                create_channelposition = lastvc_pos
            new_studydesk = await self.CATEGORY.create_voice_channel(
                name=f"もくもく勉強机{str(create_channelposition)}",
                user_limit=1,
                position=create_channelposition+1)
            await member.move_to(new_studydesk)
            log_msg = f"[INFO] もくもく勉強机{create_channelposition} を作成(Before_studydeskCount: {v_count})"  # noqa: E501
            print(log_msg)
            await self.LOG_CHANNEL.send(log_msg)
            await self.boolif_runedit()
        # 勉強机に空きがある場合
        else:
            await member.move_to(empty_studydesk[0])
            await self.boolif_runedit()

    async def remove_studydesk_10over(self, before):
        # 参加していたチャンネルが勉強机の時
        if before.channel.name.startswith("もくもく勉強机"):
            r_d2 = re.compile(r"もくもく勉強机(\d{2}).*")
            # 机の席番が10以上のチャンネルから退出した時
            if r_d2.match(before.channel.name):
                await before.channel.delete()
                print(f"[INFO] {before.channel.name} を削除しました")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel == self.CREATEDESK_CHANNEL and before.channel is None:
            # [勉強机を作成]するチャンネルに参加した時
            await self.create_studydesk(member)
        elif before.channel != after.channel and before.channel is None:
            print("[DEBUG] 処理不要な入室時")
        elif before.channel != after.channel and after.channel is None:
            # 退出時: 勉強机10以降から退出した時
            await self.remove_studydesk_10over(before)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def studydesk_posreset(self, ctx):
        self.CATEGORY = self.GUILD.get_channel(self.CATEGORY_ID)
        await self.boolif_runedit()


def setup(bot):
    return bot.add_cog(CreateStudyDesk(bot))