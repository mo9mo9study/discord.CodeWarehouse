from discord.ext import commands
import discord
import asyncio
import requests

class Self_Introduction(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488 #mo9mo9サーバーのID
        self.INTRODUCTION_CHANNEL_ID = 673006702924136448 #mo9mo9サーバー内の自己紹介チャンネルID
        self.DEBUG_GUILD_ID = 795337147149189148 #DEBUGサーバーのID ※変更しないようにお願いします。
        # 以下、質問６項目
        self.question1 = "\> 呼び名を教えてください"
        self.question2 = "\> [男/女/非公開]から選んで送信してください"
        self.question3 = "\> TwitterIDを入力してください\n@マークは要りません"
        self.question4 = "\> 得意分野は何ですか？"
        self.question5 = "\> 今まで何を勉強してきましたか？"
        self.question6 = "\> これから勉強していきたいことは何ですか？"


    # Botを起動したときに__init__に格納したIDからオブジェクトを取得
    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.INTRODUCTION_CHANNEL = self.GUILD.get_channel(self.INTRODUCTION_CHANNEL_ID)
        self.DEBUG_GUILD = self.bot.get_guild(self.DEBUG_GUILD_ID)


    # サーバーにメンバーが参加した時
    @commands.Cog.listener()
    async def on_member_join(self, member):
        #discord.DMChannelオブジェクトを取得
        dm = await member.create_dm()
        #参加したメンバーのidを名前にしたTextChannelを作成
        await self.DEBUG_GUILD.create_text_channel(str(member.id))
        #参加者にdmを送る
        await dm.send(embed=self.strfembed("ギルドへの参加ありがとうございます:D\nこれから自己紹介の処理を進めますので、質問に答えて下さい"))
        await dm.send(embed=self.strfembed(self.question1))


    # DMチャンネルにメッセージが送られた時
    @commands.Cog.listener()
    async def on_message(self, message):
        #if message.content.startswith("¥predit"): 
        #    print("コマンドおおおおおお")
        #    return
        dm = await message.author.create_dm()
        if isinstance(message.channel, discord.DMChannel):
            if message.content == "":                    
                await dm.send(embed=self.strfembed("自己紹介の編集中です\n文字列を送信してください"))
                return
            # 送信者がbotの場合は無視する
            if message.author.bot:
                return
            for channel in self.DEBUG_GUILD.text_channels:
                # DEBUGサーバーからメッセージ送信者のidと同じ名前のTextChannelを見つける
                if channel.name == str(message.author.id):
                    # channelを見つけたらそのチャンネル内の合計メッセージ数を取得する
                    count = await self.get_count(channel)
                    # メッセージ数が0の時の処理(名前が格納される)
                    if count == 0:
                        await self.send_message(channel, message.channel, message.content, f"\> 性別を教えて下さい。\n{self.question2}")
                        break
                    # メッセージ数が1の時(性別が格納される)
                    elif count == 1:
                        if message.content in ["男","女","非公開"]:
                            await self.send_message(channel, message.channel, message.content, self.question3)
                        else:
                            await message.channel.send(self.question2)
                        break
                    # メッセージ数が2の時(TwitterIDが格納される)
                    elif count == 2:
                        await self.send_message(channel, message.channel, message.content, self.question4)
                        break
                    # メッセージ数が3の時(得意分野が格納される)
                    elif count == 3:
                        await self.send_message(channel, message.channel, message.content, self.question5)
                        break
                    # メッセージ数が4の時(今まで勉強してきたことが格納される)
                    elif count == 4:
                        await self.send_message(channel, message.channel, message.content, self.question6)
                        break
                    # メッセージ数が5の時(これから勉強していきたいことが格納される)
                    elif count == 5:
                        await self.send_message(channel, message.channel, message.content, "これで質問は終了です")
                        await self.complete(channel, message)
                        break
                    elif count == 6:
                        await self.complete(channel, message)
                        break
                    # メッセージ数が7の時
                    elif count == 7:
                        await message.channel.send(embed=self.strfembed(f"{message.author.name}さんの自己紹介文は既に登録済みです。\n変更する場合は、[ ¥predit ]とコマンドを送信して下さい"))
                        break
                    # メッセージ数が8の時、最新メッセージに書かれたメッセージIDの内容を修正
                    elif count == 8:                            
                        messages = await channel.history(limit=None).flatten()
                        #DEBUG_GUILD_CHANNEL = self.DEBUG_GUILD.get_channel(channel.id) 
                        #self.message_editdelete(message, messages[0], messages[1], DEBUG_GUILD_CHANNEL)
                        # messages[0]: 修正対象のIDをmessage.contentに格納したメッセージ
                        # messages[0].content: 修正する対象のメッセージID
                        # messages[1]: mo9mo9ギルドに送信したメッセージIDをmessage.contentに格納したメッセージ
                        # messages[1].content: mo9mo9ギルドに送信された自己紹介メッセージのID
                        edit_message = await channel.fetch_message(int(messages[0].content))
                        # mo9mo9ギルドに送信した自己紹介メッセージを示すメッセージオブジェクト
                        #selfintroduction_message = await self.INTRODUCTION_CHANNEL.fetch_message(int(message[0].content))
                        selfintroduction_message = await self.INTRODUCTION_CHANNEL.fetch_message(int(messages[1].content))

                        # 編集対象のメッセージ内容を修正する
                        await edit_message.edit(content=message.content)
                        # 8個目の編集対象を示すメッセージオブジェクト削除
                        await messages[0].delete()
                        await selfintroduction_message.delete()
                        await messages[1].delete()
                        # 完成した自己紹介を送信する
                        print(message)
                        await self.complete(channel, message)
                        break
                    else:
                        print(f"{message.author.id}のメッセージの取得数が想定外です： (取得数: {count})")
                        break
            #DEBUGサーバー内にメッセージ送信者のチャンネルが見つからなかったときに、TextChanenlを作成する
            else:
                await self.DEBUG_GUILD.create_text_channel(str(message.author.id))
                await message.channel.send("自己紹介文が見つかりませんでした。\n質問に答えると自己紹介が登録できます。")
                await message.channel.send(self.question1)

    # ---on_messageイベント内でのみ呼び出される---
    # channelとdmにメッセージを送信するメソッド
    async def send_message(self, channel, dm , msgcontent, content):
        await channel.send(msgcontent)
        # await message.channel.send(embed=self.strfembed(content))
        await dm.send(embed=self.strfembed(content))

    # ---on_messageイベント内でのみ呼び出される---
    # チャンネル内のメッセージ総数を取得し、returnする
    async def get_count(self, channel):
        messages = await channel.history(limit=None).flatten()
        return len(messages)

    # ---全ての質問に答えたときに呼び出される---
    async def complete(self, channel, message):
        member = self.GUILD.get_member(message.author.id)
        # 格納されたメッセージをすべて取得
        messages = await channel.history(limit=None).flatten()
        # embedにして整形
        embed = self.add_embed(self.adjust(messages), member)
        # 完成した自己紹介文の最終チェック(修正が可能)
        embed_message = await message.channel.send(embed=embed)
        #await message.channel.send(embed=self.strfembed("この内容で自己紹介を登録しますか？\nOKなら👍リアクションを、修正する場合は❌リアクションを押して下さい"))
        await message.channel.send(embed=self.strfembed("この内容で自己紹介を登録しますか？\nOKなら👍リアクションを、修正する場合は♻️リアクションを押して下さい。\n部分的に修正する場合は一度👍リアクションを押して投稿した後に修正可能になります"))
        # リアクションを追加
        await embed_message.add_reaction("👍")
        #await embed_message.add_reaction("❌")
        await embed_message.add_reaction("♻️")
        # 押されたemojiを取得
        #emoji = await self.wait_reaction_add(channel, embed_message, ["👍", "❌"])
        emoji = await self.wait_reaction_add(channel, embed_message, ["👍", "♻️"])
        # 押された絵文字が👍の時(今の内容で登録する)
        if emoji == "👍":
            register_msg = await self.INTRODUCTION_CHANNEL.send(embed=embed)
            await channel.send(register_msg.id)
            await message.channel.send(embed=self.strfembed("登録が完了しました\n※登録した自己紹介を修正したい場合は[ ¥predit ]とコマンドを送信してください"))
        # 押された絵文字が❌の時(内容を変更する)
        #elif emoji == "❌":
        elif emoji == "♻️":
            await self.selfintroduction_reset(channel, message)
            #await message.channel.send(embed=self.strfembed("内容を全てリセットします"))
            ## TextChannelを再度作成し直し、リセットする
            #await channel.delete()
            #await self.DEBUG_GUILD.create_text_channel(message.author.id)
            #await message.channel.send(embed=self.strfembed(self.question1))


    # 自己紹介を初期化する処理
    async def selfintroduction_reset(self, channel, message):
        await message.channel.send(embed=self.strfembed("内容を全てリセットします"))
        # TextChannelを再度作成し直し、リセットする
        await channel.delete()
        await self.DEBUG_GUILD.create_text_channel(message.author.id)
        await message.channel.send(embed=self.strfembed(self.question1))


    # 自己紹介の部分的な修正を行う時の、編集、削除の処理
    #async def message_editdelete(self, message, editmsg, deletemsg, channel):
    #    #edit_message = DEBUG_GUILD_CHANNEL.fetch_message(int(editmsg.content))
    #    edit_message = channel.fetch_message(int(editmsg.content))
    #    # 8個目の編集対象を示すメッセージオブジェクト削除
    #    await editmsg.delete()
    #    # mo9mo9ギルドに送信した自己紹介メッセージを示すメッセージオブジェクト
    #    await deletemsg.delete()
    #    #selfintroduction_post_message = DEBUG_GUILD_CHANNEL.fetch_message(int(deletemsg.content))
    #    selfintroduction_post_message = channel.fetch_message(int(deletemsg.content))
    #    await selfintroduction_post_message.delete()
    #    # 編集対象の内容を変更
    #    edit_message.edit(content=message.content)


    # ---completeメソッド内でのみ呼び出される---
    # Embedオブジェクトを作成するメソッド
    def strfembed(self, str):
        embed = discord.Embed(title=str)
        return embed

    # 質問内容を追加する場合は、ここを弄る
    def add_embed(self, list, member):
        embed = discord.Embed(title="自己紹介",description=f"name: {member.name}\njoined: {str(member.joined_at.strftime('%Y-%m-%d'))}", color=self.gender_color(list[1]))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=f"【 __呼び名__ 】", value=f":name_badge: {list[0]}", inline=False)
        embed.add_field(name=f"【 __TwitterID__ 】", value=f":globe_with_meridians: @{list[2]}", inline=False)
        embed.add_field(name=f"【 __得意分野__ 】", value=f":ideograph_advantage: {list[3]}", inline=False)
        embed.add_field(name=f"【 __今まで勉強してきたこと__ 】", value=f":books: {list[4]}", inline=False)
        embed.add_field(name=f"【 __これから勉強していきたいこと__ 】", value=f":pencil: {list[5]}", inline=False)
        embed.set_footer(text=f"{member.id}")
        return embed

    # ---add_embedメソッド内でのみ呼び出される---
    # 入力された性別によって、embedのカラーを変える
    def gender_color(self, gender):
        if gender in "男":
            return 0x4093cf
        elif gender in "女":
            return 0xba3fb4
        elif gender in "非公開":
            return 0x51c447

    # ---completeメソッド内でのみ呼び出される---
    # channel内のメッセージlistの並びを逆にし、disocrd.Messageオブジェクトじゃなくdiscord.Message.Contentを格納
    def adjust(self, messages):
        messages.reverse()
        return list(map(lambda messages: messages.content, messages))
    
    def messages_id(self, messages):
        return list(map(lambda messages: messages.id, messages))        

    # ---completeメソッド内でのみ呼び出される---
    # リアクションが押されたら、そのリアクションをreturnする
    async def wait_reaction_add(self, channel, message, emojis):
        #リアクションを押したユーザーがbotじゃなく、押された絵文字がemojisに格納されている絵文字あり、リアクションを押したメッセージのidが送信されたembedメッセージのidと同じで、リアクションを押したユーザーのidとDEBUGサーバー内のchannel名が一致した場合のみ、処理が走る
        def check(reaction,user):
            # 一応元のコード残すが、以下の処理で問題なければ削除する予定
            #return user.bot == False and reaction.emoji == "👍" and reaction.message.id == message.id and str(user.id) == channel.name or user.bot == False and reaction.emoji == "❌" and reaction.message.id == message.id and str(user.id) == channel.name
            return user.bot == False and reaction.emoji in emojis and reaction.message.id == message.id and str(user.id) == channel.name
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        # リアクションが押されたら、押されたリアクションをreturnする
        # 一応元のコード残すが、以下の処理で問題なければ削除する予定
        # if reaction.emoji == "👍" or reaction.emoji == "❌":
        if reaction.emoji in emojis:
            return reaction.emoji

    def current_setting(self, list, member, number):
        desc = f"修正したい項目があればこのメッセージに付与されたリアクション（{number[0]}〜{number[4]}）を押してください"
        embed = discord.Embed(title="現在自己紹介を修正",description=desc, color=self.gender_color(list[1]))
        embed.add_field(name=f"{number[0]}", value=f"{list[0]}", inline=False)
        embed.add_field(name=f"{number[1]}", value=f"{list[2]}", inline=False)
        embed.add_field(name=f"{number[2]}", value=f"{list[3]}", inline=False)
        embed.add_field(name=f"{number[3]}", value=f"{list[4]}", inline=False)
        embed.add_field(name=f"{number[4]}", value=f"{list[5]}", inline=False)
        embed.add_field(name=f"♻️", value=f"初期化してもう一度初めから自己紹介を作成する場合", inline=False)
        return embed


    @commands.command()
    async def predit(self, message):
        member = self.GUILD.get_member(message.author.id)
        dm = await message.author.create_dm()
        for channel in self.DEBUG_GUILD.text_channels:
            print(f"channel.id: {channel.id}")
            if channel.name == str(message.author.id):
                # channelを見つけたらそのチャンネル内の合計メッセージ数を取得する
                messages = await channel.history(limit=None).flatten()
                if len(messages) != 7:
                    await dm.send(embed=self.strfembed("自己紹介を登録してから[ ¥predit ]コマンドを使用して下さい。"))
                    break
                # 修正項目を指定するためのリアクションのemojiを配列に格納
                emoji_number = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣"]
                embed = self.current_setting(self.adjust(messages), member, emoji_number)
                embed_message = await dm.send(embed=embed)
                for emoji in emoji_number:
                    await embed_message.add_reaction(emoji)     
                await embed_message.add_reaction("♻️")
                emoji = await self.wait_reaction_add(channel, embed_message, emoji_number)                
                pr_messages = self.messages_id(messages)
                if emoji == "1⃣":
                    await self.send_message(channel, dm, pr_messages[0], self.question1)
                    break
                if emoji == "2⃣":
                    await self.send_message(channel, dm, pr_messages[2], self.question3)
                    break
                if emoji == "3⃣":
                    await self.send_message(channel, dm, pr_messages[3], self.question4)
                    break
                if emoji == "4⃣":
                    await self.send_message(channel, dm, pr_messages[4], self.question5)
                    break
                if emoji == "5⃣":
                    await self.send_message(channel, dm, pr_messages[5], self.question6)
                    break
                if emoji == "♻️":
                    await self.selfintroduction_reset(channel, message)
                    break

        else:

            await self.DEBUG_GUILD.create_text_channel(str(message.author.id))
            await dm.send(embed=self.strfembed("自己紹介文が見つかりませんでした。\n質問に答えると自己紹介が登録できます。"))
            await dm.send(embed=self.strfembed(self.question1))

def setup(bot):
    return bot.add_cog(Self_Introduction(bot))