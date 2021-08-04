import asyncio
import textwrap
from datetime import datetime

import discord
from discord.ext import commands, tasks


class Times(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488  # mo9mo9サーバーのid
        self.CHANNEL_ID = 615185771565023244  # 自己紹介チャンネルのid
        self.ANNOUNCE_ID = 801060150433153054  # アナウンス用のチャンネルid
        self.ROLE_ID = 801060326627999774  # announceチャンネルでメンションする役職のid
        self.ACTIVE_CATEGORY_ID = 709805664163332147  # activetimesカテゴリーのid
        self.az09_Channel_ID = 673004651871993866  # A-Z:数字の分報カテゴリーid
        self.az09_Channel_ID2 = 805274560705724436  # A-Z:数字の分報カテゴリーid(2つ目)
        self.az09_Channel_ID3 = 872115965612158987  # A-Z:数字の分報カテゴリーid(3つ目)
        self.az09_Channel_ID4 = 872116088819822632  # A-Z:数字の分報カテゴリーid(4つ目)
        self.az09_Channel_ID5 = 872130055894077461  # A-Z:数字の分報カテゴリーid(5つ目)
        self.az09_Channel_ID6 = 872130106842284042  # A-Z:数字の分報カテゴリーid(6つ目)
        self.OTHER_CHANNEL_ID = 719095356218146879  # その他の分報カテゴリーid
        self.OTHER_CHANNEL_ID2 = 805275220923121714  # その他の分報カテゴリーid(2つ目)
        self.OTHER_CHANNEL_ID3 = 872116225537343558  # その他の分報カテゴリーid(3つ目)
        self.OTHER_CHANNEL_ID4 = 872116264066248765  # その他の分報カテゴリーid(4つ目)
        self.OTHER_CHANNEL_ID5 = 872130350518767717  # その他の分報カテゴリーid(5つ目)
        self.OTHER_CHANNEL_ID6 = 872130381443375124  # その他の分報カテゴリーid(6つ目)
        self.TIMES_CREATE_ID = 872257840528646144  # timesを作成チャンネルid
        self.VIEW_TIMES_ID = 792369191843135488  # チャンネル[自分のtimesへ移動]
        # Tutorialメッセージに追加するリアクション一覧
        self.EMOJIS = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣"]
        self.second = 5
        self.loop.start()

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.CHANNEL = self.GUILD.get_channel(self.CHANNEL_ID)
        self.ANNOUNCE = self.GUILD.get_channel(self.ANNOUNCE_ID)
        self.ACTIVE_CATEGORY = self.GUILD.get_channel(self.ACTIVE_CATEGORY_ID)
        self.az09_Channel = self.GUILD.get_channel(self.az09_Channel_ID)
        self.az09_Channel2 = self.GUILD.get_channel(self.az09_Channel_ID2)
        self.az09_Channel3 = self.GUILD.get_channel(self.az09_Channel_ID3)
        self.az09_Channel4 = self.GUILD.get_channel(self.az09_Channel_ID4)
        self.az09_Channel5 = self.GUILD.get_channel(self.az09_Channel_ID5)
        self.az09_Channel6 = self.GUILD.get_channel(self.az09_Channel_ID6)
        self.OTHER_CHANNEL = self.GUILD.get_channel(self.OTHER_CHANNEL_ID)
        self.OTHER_CHANNEL2 = self.GUILD.get_channel(self.OTHER_CHANNEL_ID2)
        self.OTHER_CHANNEL3 = self.GUILD.get_channel(self.OTHER_CHANNEL_ID3)
        self.OTHER_CHANNEL4 = self.GUILD.get_channel(self.OTHER_CHANNEL_ID4)
        self.OTHER_CHANNEL5 = self.GUILD.get_channel(self.OTHER_CHANNEL_ID5)
        self.OTHER_CHANNEL6 = self.GUILD.get_channel(self.OTHER_CHANNEL_ID6)
        self.TIMES_CREATE = self.GUILD.get_channel(self.TIMES_CREATE_ID)
        self.VIEW_TIMES = self.GUILD.get_channel(self.VIEW_TIMES_ID)
        self.ROLE = self.GUILD.get_role(self.ROLE_ID)
        # ユーザーが自己紹介してなくても任意でtimesを作成できる処理を追加
        await self.TIMES_CREATE.purge()
        embed = discord.Embed(title="あなたのtimesを作成します",
                              description="※ 既に存在する場合は作成されません")
        embed.add_field(name=" 👇 使い方", value="（超簡単）このメッセージにリアクションをするだけ‼️ ")
        self.message = await self.TIMES_CREATE.send(embed=embed)
        self.message_id = self.message.id
        await self.message.add_reaction("🛎️")

    @commands.Cog.listener()
    async def on_message(self, message):
        # BOTへのメッセージ送信時にもイベントが走るので、BOTのDM上のイベントはreturnする
        if isinstance(message.channel, discord.DMChannel):
            return
        if message.channel.category_id == self.ACTIVE_CATEGORY_ID:
            return
        # ---------------times作成処理---------------
        elif message.channel.id == self.CHANNEL_ID:
            if message.author.bot:
                user_id = message.embeds[0].footer.text  # footerのidを取得
                user_id = int(user_id)
                for channel in self.GUILD.text_channels:
                    if channel.topic == str(user_id):
                        print(
                            f"(userid: {str(user_id)})timesチャンネルが既に存在します。")
                        break
                else:
                    await self.channelCreateSend(self.getMember(user_id))
        # ---------------active_times処理---------------
        elif message.channel.name[0:6] == "times_":
            await message.channel.edit(category=self.ACTIVE_CATEGORY)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        if payload.message_id == self.message_id:
            user_id = int(payload.member.id)
            for channel in self.GUILD.text_channels:
                if channel.topic == str(user_id):
                    msg = await self.TIMES_CREATE.send(textwrap.dedent(f"""\
                        あなたのtimesチャンネルは既に存在します)
                        {self.VIEW_TIMES.mention} でtimesに移動しよう"""))
                    await self.time_sleep(msg)
                    await self.message.remove_reaction(payload.emoji,
                                                       payload.member)
                    break
            else:
                await self.channelCreateSend(self.getMember(user_id))
                msg = await self.TIMES_CREATE.send(textwrap.dedent(f"""\
                    あなたのtimesチャンネルを作成しました
                    {self.VIEW_TIMES.mention} でtimesに移動しよう"""))
                await self.time_sleep(msg)
                await self.message.remove_reaction(payload.emoji,
                                                   payload.member)

    async def time_sleep(self, msg):
        await asyncio.sleep(self.second)
        await msg.delete()

    # ユーザーidからメンバーオブジェクトを取得
    def getMember(self, user_id):
        member = self.GUILD.get_member(user_id)
        return member

    # timesチャンネルがなかった時に呼び出される
    async def channelCreateSend(self, member):
        channel = await self.ACTIVE_CATEGORY.create_text_channel(
            name=f"times_{member.name}")
        await channel.edit(topic=member.id)

        await channel.send(f"""
{member.mention}
このチャンネルはあなたの分報(個人)チャンネルです。
使い方は「参考資料」又は「他メンバーの分報チャンネル」をご覧ください。
上手に活用してみてくださいね
 　参考資料：http://c16e.com/1511101558/
""")

        # embedメッセージを送信
        embedMsg = await channel.send(embed=self.createEmbed())
        await self.addReaction(embedMsg)  # Tutorialメッセージにリアクションを付ける

    # ---channelCreateSendメソッドからのみ呼び出される---
    # Tutorialメッセージを作成
    def createEmbed(self):
        embed = discord.Embed(title="チュートリアル")
        embed.add_field(name=":one:", value="自己紹介しよう", inline=False)
        embed.add_field(name=":two: ", value="アイコン設定をしよう", inline=False)
        embed.add_field(
            name=":three:",
            value="ボイスチャット（ラウンジ、もくもく勉強机n）に参加して勉強を開始しよう",
            inline=False)
        embed.add_field(
            name=":four:",
            value="ボイスチャット（ラウンジ、もくもく勉強机n）に5分以上参加してから退席して、勉強記録をつけよう",
            inline=False)
        embed.add_field(
            name=":five:",
            value="今日の積み上げを確認してみよう、チャンネル<#829515424042450984>へ移動しメッセージの「今日の勉強集計」に対応するスタンプを押してみよう",  # noqa: E501
            inline=False)
        embed.add_field(
            name=":six:",
            value="今週の積み上げを確認してみよう、チャンネル<#829515424042450984>へ移動しメッセージの「今週の勉強集計」に対応するスタンプを押してみよう",  # noqa: E501
            inline=False)
        embed.add_field(name=":tada: **全チュートリアル完了した方へ**",
                        value="お疲れ様です。timesという個人チャンネルについては他の人のtimesチャンネルをみて刺激もらったり、使い方を学んでみよう！",  # noqa: E501
                        inline=True)
        embed.add_field(name=":beginner: **チュートリアルの進捗管理**",
                        value="このメッセージの下にチュートリアルの数だけ対応するスタンプを付与していますので、クリアしたらスタンプを押して進捗を管理してみてください。",  # noqa: E501
                        inline=True)
        return embed

    # ---channelCreateSendメソッドからのみ呼び出される---
    # Tutorialメッセージにリアクションを付ける
    async def addReaction(self, message):
        for emoji in self.EMOJIS:
            await message.add_reaction(emoji)

    def getActiveChannels(self):
        activeChannels = self.ACTIVE_CATEGORY.text_channels
        return activeChannels

    def getDivideTimesCount(self, which):
        if which == "az":
            return len(self.az09_Channel.text_channels)
        elif which == "az2":
            return len(self.az09_Channel2.text_channels)
        elif which == "az3":
            return len(self.az09_Channel3.text_channels)
        elif which == "az4":
            return len(self.az09_Channel4.text_channels)
        elif which == "az5":
            return len(self.az09_Channel5.text_channels)
        elif which == "other":
            return len(self.OTHER_CHANNEL.text_channels)
        elif which == "other2":
            return len(self.OTHER_CHANNEL2.text_channels)
        elif which == "other3":
            return len(self.OTHER_CHANNEL3.text_channels)
        elif which == "other4":
            return len(self.OTHER_CHANNEL4.text_channels)
        elif which == "other5":
            return len(self.OTHER_CHANNEL5.text_channels)

    async def times_classification(self, channel):
        if channel.name[6].encode('utf-8').isalnum():
            if self.getDivideTimesCount("az") < 50:
                await channel.edit(category=self.az09_Channel)
            elif self.getDivideTimesCount("az2") < 50:
                await channel.edit(category=self.az09_Channel2)
            elif self.getDivideTimesCount("az3") < 50:
                await channel.edit(category=self.az09_Channel3)
            elif self.getDivideTimesCount("az4") < 50:
                await channel.edit(category=self.az09_Channel4)
            elif self.getDivideTimesCount("az5") < 50:
                await channel.edit(category=self.az09_Channel5)
            else:
                await channel.edit(category=self.az09_Channel6)
        else:
            if self.getDivideTimesCount("other") < 50:
                await channel.edit(category=self.OTHER_CHANNEL)
            elif self.getDivideTimesCount("other2") < 50:
                await channel.edit(category=self.OTHER_CHANNEL2)
            elif self.getDivideTimesCount("other3") < 50:
                await channel.edit(category=self.OTHER_CHANNEL3)
            elif self.getDivideTimesCount("other4") < 50:
                await channel.edit(category=self.OTHER_CHANNEL4)
            elif self.getDivideTimesCount("other5") < 50:
                await channel.edit(category=self.OTHER_CHANNEL5)
            else:
                await channel.edit(category=self.OTHER_CHANNEL6)

    # ---------------定期処理---------------
    # 午前2:00に実行されます

    @tasks.loop(seconds=59)
    async def loop(self):
        await self.bot.wait_until_ready()
        now = datetime.now().strftime('%H:%M')
        if now == "02:00":
            for channel in self.getActiveChannels():
                await self.times_classification(channel)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ttimes_reset(self, ctx):
        for channel in self.getActiveChannels():
            await self.times_classification(channel)


def setup(bot):
    return bot.add_cog(Times(bot))
