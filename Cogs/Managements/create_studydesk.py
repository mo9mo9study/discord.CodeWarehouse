import re
import unicodedata

from discord.ext import commands


class CreateStudyDesk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488  # mo9mo9 Guild Id
        self.CATEGORY_ID = 873317086439546900  # Study Space Category Id
        self.LOG_CHANNEL_ID = 801060150433153054  # 通知用 Channel Id
        self.CREATEDESK_CHANNEL_ID = 897995150926688286  # 勉強机に着席
        self.CREATEDESK_CHANNEL2_ID = 935921618725777448  # 勉強開始

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.CATEGORY = self.GUILD.get_channel(self.CATEGORY_ID)
        self.LOG_CHANNEL = self.GUILD.get_channel(self.LOG_CHANNEL_ID)
        self.CREATEDESK_CHANNEL = self.GUILD.get_channel(
            self.CREATEDESK_CHANNEL_ID)
        self.CREATEDESK_CHANNEL2 = self.GUILD.get_channel(
            self.CREATEDESK_CHANNEL2_ID)
        self.MOVECHANNELS = [self.CREATEDESK_CHANNEL.id, self.CREATEDESK_CHANNEL2.id]  # noqa: E501

    def vc_sort(self):
        """
        カテゴリーのチャンネルを全て取得し、チャンネルの並び順を
        想定通りになるようpos番号を振り直して辞書として値を戻す
        """
        vc_sorted_dict = {}
        vc_deskcreate_pos = 1
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
                    vc_sorted_dict[int(vc_namenu) + 1] = channel
            # 勉強机を作成するチャンネル
            elif channel.id == self.CREATEDESK_CHANNEL.id:
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
        vcpos_diffarent = []
        for channel in self.CATEGORY.channels:
            r_d1 = re.compile(r"もくもく勉強机(\d).*")
            r_d2 = re.compile(r"もくもく勉強机(\d{2}).*")
            # 勉強机の席番が10〜
            if r_d2.match(channel.name):
                vc_namenu = r_d2.match(channel.name)[1]
                print(
                    f"[DEBUG] {channel.name}/DeskNo:{vc_namenu}, DeskPos:{channel.position}")  # noqa: E501
                vc_pos = int(vc_namenu)
                if (vc_pos + 1) != channel.position:
                    diff_msg = f"{channel.name}/{vc_namenu}:{channel.position}"
                    vcpos_diffarent.append(diff_msg)
            # 勉強机の席番が1〜9
            elif re.compile(r_d1).match(channel.name):
                vc_namenu = unicodedata.normalize(
                    "NFKD", r_d1.match(channel.name)[1])
                print(
                    f"[DEBUG] {channel.name}/DeskNo:{vc_namenu}, DeskPos:{channel.position}")  # noqa: E501
                if int(vc_namenu) != channel.position:
                    diff_msg = f"{channel.name}/{vc_namenu}:{channel.position}"
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
            create_deskno = self.desk_missing_number()
            if not create_deskno:  # 10over, False
                # 連番に欠番が存在しない時
                vc_sorted_dict = self.vc_sort()
                studydesk_len = len(self.CATEGORY.channels)  # チャンネル総数
                # ソートした辞書からpos取得
                lastvc_pos = vc_sorted_dict[studydesk_len - 1].position
                create_deskno = lastvc_pos  # 作成する勉強机No
            create_deskname = f"もくもく勉強机{str(create_deskno)}"
            new_studydesk = await self.CATEGORY.create_voice_channel(
                name=create_deskname,
                user_limit=1,
                position=create_deskno+1)
            await member.move_to(new_studydesk)
            log_msg = f"[INFO] {create_deskname} を用意(出席者:{member.name})"  # noqa: E501
            print(log_msg)
            await self.LOG_CHANNEL.send(log_msg)
            await self.boolif_runedit()
        # 勉強机に空きがある場合
        else:
            await member.move_to(empty_studydesk[0])
            await self.boolif_runedit()

    async def remove_studydesk_10over(self, member, before):
        """
        勉強机から退出した際、
        退出したVC名が勉強机であり、数字が10以上(正規表現で数字2桁)の時、
        その勉強机を削除する
        """
        # 参加していたチャンネルが勉強机の時
        if before.channel.name.startswith("もくもく勉強机"):
            r_d2 = re.compile(r"もくもく勉強机(\d{2}).*")
            # 机の席番が10以上のチャンネルから退出した時
            if r_d2.match(before.channel.name):
                await before.channel.delete()
                log_msg = f"[INFO] {before.channel.name} を片付け(退席者:{member.name})"  # noqa: E501
                print(log_msg)
                await self.LOG_CHANNEL.send(log_msg)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # 入室時
        if before.channel != after.channel and before.channel is None:
            if after.channel.id in self.MOVECHANNELS:
                # [勉強机]に移動専用のVCに参加した時
                await self.create_studydesk(member)
                return
            else:
                # それ以外のVCに参加した時
                print("[DEBUG] 処理不要な入室時")
        # 退出時
        if before.channel != after.channel and after.channel is None:
            await self.remove_studydesk_10over(member, before)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def studydesk_posreset(self, ctx):
        self.CATEGORY = self.GUILD.get_channel(self.CATEGORY_ID)
        await self.boolif_runedit()


def setup(bot):
    return bot.add_cog(CreateStudyDesk(bot))
