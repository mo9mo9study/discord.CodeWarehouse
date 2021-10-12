from datetime import datetime, timedelta
import random
import re

from discord.ext import commands


class SlotStudyrecord(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488  # mo9mo9サーバーID
        self.RECORD_CHANNEL_ID = 618081921611726851  # 勉強記録チャンネル
        self.CHANNEL_ID = 684736099565830169  # 勉強スロット当選者
        self.LOG_CHANNEL_ID = 801060150433153054
        self.notOutputTime = 20
        self.slot1 = ['🙈', '👹', '👾']
        self.slot2 = ['🙉', '🤡', '💀']
        self.slot3 = ['🙊', '💩', '👻']

    def intRandom(self, emojis):
        i = random.randrange(len(emojis))
        return i

    async def addReaction(self, message, emojis, i):
        reactionId = emojis[i]
        await message.add_reaction(reactionId)

    @commands.Cog.listener()
    async def on_ready(self):
        self.CHANNEL = self.bot.get_channel(self.CHANNEL_ID)
        self.LOG_CHANNEL = self.bot.get_channel(self.LOG_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:  # BOTじゃなければreturn
            print(message)
            return
        # 勉強ログのメッセージのみtrue
        if message.channel.id != self.RECORD_CHANNEL_ID:
            return
        if 'Study time' in message.content:
            result_studytime = re.compile(
                r'.*Study time  (.*) /分.*').match(message.content)
            intStudyTime = int(result_studytime[1])
            result_name = re.compile(
                r'.*\[.*\]\s*(.*)  Study time.*').match(message.content)
            strName = result_name[1]
            # 5分以内の記録では動作しないようにするため
            if intStudyTime < self.notOutputTime:
                return
            else:
                slotresult1 = self.intRandom(self.slot1)
                slotresult2 = self.intRandom(self.slot2)
                slotresult3 = self.intRandom(self.slot3)
                await self.addReaction(message, self.slot1, slotresult1)
                await self.addReaction(message, self.slot2, slotresult2)
                await self.addReaction(message, self.slot3, slotresult3)
            # 当選者用の処理
            if slotresult1 == 0 and slotresult2 == 0 and slotresult3 == 0:
                now = datetime.utcnow() + timedelta(hours=9)
                # messageと文字列の名前を紐づけてmembers.mentionの取得
                guildMembers = message.guild.members
                for member in guildMembers:
                    if member.name == strName:
                        send_msg = f'{member.mention}\n[ {now:%m/%d %H:%M} ] 勉強時間ボーナススロット大当たり🎉 {intStudyTime}分の勉強お疲れ様 🍵'  # noqa #501
                        log_msg = f"[INFO] {strName}が勉強スロットに当選"
                        await self.CHANNEL.send(send_msg)
                        await self.LOG_CHANNEL.send(log_msg)
                        break


def setup(bot):
    return bot.add_cog(SlotStudyrecord(bot))
