from discord.ext import commands,tasks
import discord
import asyncio
from datetime import datetime
import re

class Times(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488  # mo9mo9サーバーのid
        self.CHANNEL_ID = 615185771565023244  # 自己紹介チャンネルのid
        self.ANNOUNCE_ID = 801060150433153054  # アナウンス用のチャンネルid
        self.ROLE_ID = 801060326627999774  # announceチャンネルでメンションする役職のid
        self.ACTIVE_CATEGORY_ID = 709805664163332147  # activetimesカテゴリーのid
        self.az09_Channel_ID = 673004651871993866  # A-Z:数字の分報カテゴリーid
        self.OTHER_CHANNEL_ID = 719095356218146879  # その他の分報カテゴリーid
        self.EMOJIS = ["1⃣","2⃣","3⃣","4⃣","5⃣","6⃣"] #Tutorialメッセージに追加するリアクション一覧
        self.loop.start()

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.CHANNEL = self.GUILD.get_channel(self.CHANNEL_ID)
        self.ANNOUNCE = self.GUILD.get_channel(self.ANNOUNCE_ID)
        self.ACTIVE_CATEGORY = self.GUILD.get_channel(self.ACTIVE_CATEGORY_ID)
        self.az09_Channel = self.GUILD.get_channel(self.az09_Channel_ID)
        self.OTHER_CHANNEL = self.GUILD.get_channel(self.OTHER_CHANNEL_ID)
        self.ROLE = self.GUILD.get_role(self.ROLE_ID)

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
                user_id = message.embeds[0].footer.text #footerのidを取得
                user_id = int(user_id)
                for channel in self.GUILD.text_channels:
                    if channel.topic == str(user_id):
                        print(f"(userid: {str(user_id)})timesチャンネルが既に存在するので、作成しませんでした。")
                        break
                else:
                    await self.channelCreateSend(self.getMember(user_id))

        # ---------------active_times処理---------------
        elif message.channel.name[0:6] == "times_":
            await message.channel.edit(category=self.ACTIVE_CATEGORY)

    #ユーザーidからメンバーオブジェクトを取得
    def getMember(self,user_id):
        member = self.GUILD.get_member(user_id)
        return member

    #timesチャンネルがなかった時に呼び出される
    async def channelCreateSend(self, member):
        channel = await self.ACTIVE_CATEGORY.create_text_channel(name=f"times_{member.name}")
        await channel.edit(topic=member.id)

        await channel.send(f"""
{member.mention}
このチャンネルはあなたの分報(個人)チャンネルです。
使い方は「参考資料」又は「他メンバーの分報チャンネル」をご覧ください。
上手に活用してみてくださいね
 　参考資料：http://c16e.com/1511101558/
""")

        embedMsg = await channel.send(embed = self.createEmbed()) #embedメッセージを送信
        await self.addReaction(embedMsg) #Tutorialメッセージにリアクションを付ける
        count = self.getChannelCount() #timesチャンネルの総数を取得
        await self.ANNOUNCE.send(f"{self.ROLE.mention}\n",embed=self.createAnnounce()) #announceチャンネルにtimesチャンネル総数を送信

    #---channelCreateSendメソッドからのみ呼び出される---
    #Tutorialメッセージを作成
    def createEmbed(self):
        embed = discord.Embed(title="チュートリアル")
        embed.add_field(name=":one:", value="自己紹介しよう", inline=False)
        embed.add_field(name=":two: ", value="アイコン設定をしよう", inline=False)
        embed.add_field(name=":three:", value="ボイスチャット（ラウンジ、もくもく勉強机n）に参加して勉強を開始しよう", inline=False)
        embed.add_field(name=":four:", value="ボイスチャット（ラウンジ、もくもく勉強机n）に5分以上参加してから退席して、勉強記録をつけよう", inline=False)
        embed.add_field(name=":five:", value="今日の積み上げを確認してみよう「¥result_d」だけのメッセージを送信してみてね", inline=False)
        embed.add_field(name=":six:", value="昨日の勉強記録は「¥result_d ago」だけのメッセージを送信してみてね", inline=False)
        embed.add_field(name=":tada: **全チュートリアル完了した方へ**",
                        value="お疲れ様です。timesという個人チャンネルについては他の人のtimesチャンネルをみて刺激もらったり、使い方を学んでみよう！", inline=True)
        embed.add_field(name=":beginner: **チュートリアルの進捗管理**",
                        value="このメッセージの下にチュートリアルの数だけ対応するスタンプを付与していますので、クリアしたらスタンプを押して進捗を管理してみてください。", inline=True)
        return embed

    #---channelCreateSendメソッドからのみ呼び出される---
    #Tutorialメッセージにリアクションを付ける
    async def addReaction(self,message):
        for emoji in self.EMOJIS:
            await message.add_reaction(emoji)

    #---channelCreateSendメソッドからのみ呼び出される---
    #timesチャンネルの合計を取得する
    def getChannelCount(self):
        timesChannels = list(filter(lambda channel: channel.name[0:6] == "times_", self.GUILD.text_channels))
        count = len(timesChannels)
        return count

    #---channelCreateSendメソッドからのみ呼び出される---
    #announce用のembedを作成
    def createAnnounce(self):
        az09, other = self.getChannelTotalNumber()
        embed = discord.Embed(title=f"times_Channel総数： {az09+other}個")
        embed.add_field(name=f"{self.az09_Channel.name}の総数：", value=f"{az09}個", inline=True)
        embed.add_field(name=f"{self.OTHER_CHANNEL.name}の総数：", value=f"{other}個", inline=True)
        return embed

    #---createAnnounceメソッドからのみ呼び出される---
    #---各timesの総数を取得---
    def getChannelTotalNumber(self):
        az09 = 0
        other = 0
        for channel in self.ACTIVE_CATEGORY.text_channels:
            if channel.name[6].encode('utf-8').isalnum():
                az09 = az09 +  1 #処理速度を上げるために自己代入の省略をしていません
            else:
                other = other + 1
        az09 = az09 + len(self.az09_Channel.text_channels)
        other = other + len(self.OTHER_CHANNEL.text_channels)
        return az09, other

    def getActiveChannels(self):
        activeChannels = self.ACTIVE_CATEGORY.text_channels
        return activeChannels

    # ---------------定期処理---------------
    #午前2:00に実行されます
    @tasks.loop(seconds=60)
    async def loop(self):
        await self.bot.wait_until_ready()
        now = datetime.now().strftime('%H:%M')
        if now == "02:00":
            for channel in self.getActiveChannels():
                if channel.name[6].encode('utf-8').isalnum():
                    await channel.edit(category=self.az09_Channel)
                else:
                    await channel.edit(category=self.OTHER_CHANNEL)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def times_reset(self, ctx):
        for channel in self.getActiveChannels():
            if channel.name[6].encode('utf-8').isalnum():
                print(channel.name[6])
                await channel.edit(category=self.az09_Channel)
            else:
                await channel.edit(category=self.OTHER_CHANNEL)    


def setup(bot):
    return bot.add_cog(Times(bot))

