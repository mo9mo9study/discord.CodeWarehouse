from discord.ext import commands
import discord
import asyncio

class Quest(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.channel_id = 771006468216193064 #クエスト提示版のチャンネルid
        self.check1 = True #titleが入力されるとFalseになる
        self.user = None #他の方と競合しない様にするため
        self.Achieved_channel_id = 788847284606861334

    @commands.Cog.listener()
    async def on_message(self,message):
        #メッセージ送信者がBotの場合、処理を実行しない
        if message.author.bot:
            return
        #チャンネルがクエスト提示版か確認
        if message.channel.id == self.channel_id:
            # self.check1がTrueの場合実行される
            # titleを取得
            if self.check1:
                self.title = message.content
                self.check1 = False
                self.send_bot = await message.channel.send("質問内容を入力してください")
                self.user = message.author
                await message.delete()
                return

            #userがtitleを入力したユーザーと同じ場合実行される
            #内容を取得し、整形したメッセージをEmbedにし送信する
            if self.user.id == message.author.id:
                self.content = message.content
                embed = discord.Embed(title=self.title,description=await self.txt(message.author.name, self.content, "まだいません"))
                self.embed_message = await message.channel.send(embed=embed)
                await message.delete()
                await self.embed_message.add_reaction("✋")
                await self.init()
                await self.wait_reaction(message)


            #titleとcontentを別のユーザーが入力した場合の処理
            else:
                await message.delete()
                warning_msg = await message.channel.send(f"{self.user.name}さんが現在入力中です。\nお待ちください。")
                await asyncio.sleep(5)
                await warning_msg.delete()

    #Embed作成後にリアクションを押した人が受注者欄の名前に反映される
    async def wait_reaction(self, message):
        def check(reaction,user):
            return user.id != self.user.id and reaction.emoji == "✋"
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        embed = discord.Embed(title=self.title, description=await self.txt(message.author.name, self.content, user.name))
        await self.embed_message.edit(embed=embed)

    #設定を全て初期化する
    #embedが送信された場合に呼び出される
    async def init(self):
        self.check1 = True
        await self.send_bot.delete()

    #Embedの整形用関数
    async def txt(self, name, content, contractor):
        return f"""
----------------
依頼人 : {name}
----------------
{content}
----------------
受注者 : {contractor}
"""

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == self.channel_id:
            guild = payload.member.guild
            message = await guild.get_channel(payload.channel_id).fetch_message(payload.message_id)

            #titleだけ入力し、内容を書かずに放置されてた場合に、リアクションを押すとresetできる機能
            if str(payload.emoji) == "🛑":
                await message.delete()
                await self.init()

            # 達成したクエストを達成済みクエストチャンネルに移動させる機能
            if str(payload.emoji) == "✅":
                Achieved_channel = guild.get_channel(self.Achieved_channel_id)
                embed_obj = message.embeds[0]
                embed = discord.Embed(title=embed_obj.title,description=embed_obj.description)
                await Achieved_channel.send(embed=embed)
                await message.delete()

def setup(bot):
    return bot.add_cog(Quest(bot))