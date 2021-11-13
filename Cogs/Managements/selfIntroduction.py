import discord
from discord.ext import commands

from mo9mo9db.dbtables import Selfintroduction


class Self_Introduction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488  # mo9mo9サーバーのID
        self.INTRODUCTION_CHANNEL_ID = 615185771565023244  # mo9mo9の自己紹介チャンネル
        self.DEBUG_GUILD_ID = 795337147149189148  # DEBUGサーバーのID ※変更不可
        # 以下、質問６項目
        self.question1 = "\> 呼び名を教えてください"  # noqa: W605
        self.question2 = "\> [男/女/非公開]から選んで送信してください"  # noqa: W605
        self.question3 = "\> TwitterIDを入力してください\n@マークは要りません"  # noqa: W605
        self.question4 = "\> 得意分野は何ですか？"  # noqa: W605
        self.question5 = "\> 今まで何を勉強してきましたか？"  # noqa: W605
        self.question6 = "\> これから勉強していきたいことは何ですか？"  # noqa: W605

    # Botを起動したときに__init__に格納したIDからオブジェクトを取得

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.INTRODUCTION_CHANNEL = self.GUILD.get_channel(
            self.INTRODUCTION_CHANNEL_ID)
        self.DEBUG_GUILD = self.bot.get_guild(self.DEBUG_GUILD_ID)
        # 全てのパラメータが埋まっている状態で、まだ自己紹介を送信していない場合
        # 再度確認用のメッセージをDMに送る処理追加
        guild = self.bot.get_guild(self.GUILD_ID)
        for channel in self.DEBUG_GUILD.text_channels:
            count = await self.get_count(channel)
            if count == 6:
                member = guild.get_member(
                    int(channel.name))
                print(f"自己紹介を送信していないユーザー: {member}/{channel}")
                if member is None:
                    return
                await self.complete(channel, member.id)

    async def db_insert_selfintroduction(self, member):
        obj = Selfintroduction(
            guild_id=member.guild.id,
            member_id=member.id,
            mod_column="nickname"
        )
        Selfintroduction.insert(obj)

    # サーバーにメンバーが参加した時
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        メンバー参加時に処理が実行され
        参加したメンバーのメンバー情報（レコード）がselfintroductionテーブルに作成される
        """
        # discord.DMChannelオブジェクトを取得
        dm = await member.create_dm()
        # selfintroductionテーブルに参加したメンバーの情報をinsert
        await self.db_insert_selfintroduction(member)
        # 参加者にdmを送る
        await dm.send(embed=self.strfembed("ギルドへの参加ありがとうございます\nこれから自己紹介の処理を進めますので、質問に答えて下さい"))  # noqa: E501
        await dm.send(embed=self.strfembed(self.question1))

    def db_select_selfintroduction(self, member):
        """
        対象メンバーの自己紹介データを取得する

        Parameter
        ---------
        member : discord.Member
            message.authorから取得したメンバーオブジェクト
        """
        session = Selfintroduction.session()
        obj = Selfintroduction.objects(session).filter(
            Selfintroduction.member_id == member.id,
            Selfintroduction.guild_id == member.guild.id).first()
        return obj

    def db_reset_selfintroduction(self, member) -> None:
        """
        対象メンバーの自己紹介データのメンバーが対話式でデータを挿入できるカラムを初期化

        Parameter
        ---------
        member : discord.Member
            message.authorから取得したメンバーオブジェクト
        """
        session = Selfintroduction.session()
        obj = Selfintroduction.objects(session).filter(
            Selfintroduction.member_id == member.id,
            Selfintroduction.guild_id == member.guild.id).first()
        reset_columns = ["nickname", "sex", "twitter_id", "specialty",
                         "before_study", "after_study"]
        for column in reset_columns:
            obj[column] = None
        obj["mod_column"] = "nickname"
        obj.commit()

    def db_update_selfintroduction(self, member, select_column, after_value,
                                   next_mod_column) -> None:
        """
        カラムを指定して自己紹介データを修正する

        Parameter
        ---------
        select_columns : str
            カラム名[mod_column]から取得した、今回修正されるカラム名
        after_value : str
            メンバーから送信されたメッセージの内容
        next_mod_column : str
            カラム名[mod_column]に保存される、次修正対象となるカラム名
        """
        obj = self.db_select_selfintroduction(member)
        obj[select_column] = after_value
        if next_mod_column:
            obj["mod_column"] = next_mod_column
        obj.commit()

    def check_missingdata(self, member) -> str:
        """
        DBからメンバーの自己紹介情報を取得し、現在の処理で受け取ったメッセージ内容を
        どのカラムに保存するかをかをmod_columnから確認する
        この処理が正常に終了後、次に修正するカラム名を比較し確定する

        Return
        ------
        missingdata_column : str, None
            今回修正するカラム名
        next_missingdata_column : str, None
            今回の処理が正常に完了した場合、次に修正するカラム名
        """
        member_data = self.db_select_selfintroduction(member)
        missingdata_column = None
        next_missingdata_column = None
        # 次修正するカラムを確認
        if not member_data["nickname"]:
            next_missingdata_column = "nickname"
        elif not member_data["sex"]:
            next_missingdata_column = "sex"
        elif not member_data["twitter_id"]:
            next_missingdata_column = "twitter_id"
        elif not member_data["specialty"]:
            next_missingdata_column = "specialty"
        elif not member_data["before_study"]:
            next_missingdata_column = "before_study"
        elif not member_data["after_study"]:
            next_missingdata_column = "after_study"
        elif not member_data["sendmsg_id"]:
            next_missingdata_column = "sendmsg_id"
        # 今回修正するカラムを確認
        if member_data["mod_column"]:
            missingdata_column = member_data["mod_column"]
        else:
            # mod_columnには修正するカラムの指定はないが
            # 不足しているデータがあった場合
            # 不足しているデータを今回の修正カラムとして昇格する
            if next_missingdata_column:
                missingdata_column = next_missingdata_column
        return missingdata_column, next_missingdata_column

    def select_nextquestionmsg(self, next_missingdata_column) -> str:
        """
        次に不足しているデータの情報を元に、次に質問するメッセージを選択する

        Parameters
        ----------
        next_missingdata_column : str
            今回のメッセージの内容をDBに登録した後、次に不足しているカラムの情報

        Return
        ------
        next_msg : str
            botがDBでメンバーに送信するDMメッセージの内容
        """
        if next_missingdata_column == "nickname":
            next_msg = self.question1
        elif next_missingdata_column == "sex":
            next_msg = f"""\> 性別を教えて下さい。\n{self.question2}"""  # noqa: W605
        elif next_missingdata_column == "twitter_id":
            next_msg = self.question3
        elif next_missingdata_column == "specialty":
            next_msg = self.question4
        elif next_missingdata_column == "before_study":
            next_msg = self.question5
        elif next_missingdata_column == "after_study":
            next_msg = self.question6
        elif next_missingdata_column == "sendmsg_id":
            next_msg = "これで質問は終了です"
        return next_msg

    async def check_msg_content(self, dm, missingdata_column, msg_cont) -> bool:  # noqa: E501
        """
        データの値を判定し、想定通りでなければエラーを出す

        Returns
        -------
        check_msg : boolen

        Notes
        -----
        future: データが想定通りじゃない場合は、適当な値に修正する処理も追加したい
            例: TwitterIDが英数字記号以外が含まれていた場合は一律"not_account"にするなど
        """
        check_msg = True
        if msg_cont == "":
            await dm.send(embed=self.strfembed("自己紹介の編集中です\n文字列を送信してください"))
            check_msg = False
        else:
            if missingdata_column == "sex":
                if msg_cont not in ["男", "女", "非公開"]:
                    check_msg = False
        return check_msg

    @commands.Cog.listener()
    @commands.dm_only()
    async def on_message(self, message):
        """
        メンバーとBOT間のDMをトリガーに実行される
        """
        # if isinstance(message.channel, discord.DMChannel):
        # 送信者がbotの場合は無視する
        if message.author.bot:
            return
        dm = await message.author.create_dm()
        member = self.GUILD.get_member(dm.me.id)
        # 受信したメッセージの内容をどのカラムに保存するかを確認
        # 次不足しているデータの確認
        missingdata_column, next_missingdata_column = self.check_missingdata(
            member)
        # データのチェック
        check_msg = await self.check_msg_content(dm, missingdata_column,
                                                 message.content)
        if check_msg:
            return
        # 不足しているデータをDBに書き込み
        self.db_update_selfintroduction(member, missingdata_column,
                                        message.content,
                                        next_missingdata_column)
        # 不足しているデータから次の送信メッセージを選択
        send_msg = self.select_nextquestionmsg(next_missingdata_column)
        await dm.send(embed=self.strfembed(send_msg))
        if not missingdata_column and not next_missingdata_column:
            # データに不足がない場合
            comp_msg = f"{message.author.name}さんの自己紹介文は既に登録済みです。"\
                + "\n変更する場合は、[ ¥predit ]とコマンドを送信して下さい。"
            await message.channel.send(embed=self.strfembed(comp_msg))
            return
        # メッセージを勉強ギルドに送信する処理
        # ここ続けて書く必要あり

    async def send_selfintroduction(self, member) -> None:
        """
        DBに補完された自己紹介データをEmbedの形に入れ込み、自己紹介を送信する

        Parameter
        ---------
        member : discord.Member
            message.authorから取得したメンバーオブジェクト
        """
        dm = await member.create_dm()
        embed = self.add_embed(member)
        # 完成した自己紹介文の最終チェック(修正が可能)
        embed_message = await dm.send(embed=embed)
        send_msg = "この内容で自己紹介を登録しますか？"\
            + "OKなら👍リアクションを、修正する場合は♻️リアクションを押して下さい。"\
            + "部分的に修正する場合は一度👍リアクションを押して投稿した後に修正可能になります"  # noqa: E501
        await dm.send(embed=self.strfembed(send_msg))
        # リアクションを追加
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("♻️")
        # 押されたemojiを取得
        emoji = await self.wait_reaction_add(embed_message, ["👍", "♻️"])
        # 押された絵文字が👍の時(今の内容で登録する)
        if emoji == "👍":
            after_msg = await self.INTRODUCTION_CHANNEL.send(embed=embed)
            await after_msg.add_reaction("<:yoroshiku:761730298106478592>")
            # DBの自己紹介メッセージIDを送信後のメッセージIDに変更
            await self.db_update_selfintroduction(member, "sendmsg_id",
                                                  after_msg.id, None)
            send_msg2 = "登録が完了しました" \
                + "※登録した自己紹介を修正したい場合は[ ¥predit ]とコマンドを送信してください"   # noqa: E501
            await dm.send(embed=self.strfembed(send_msg2))
        elif emoji == "♻️":
            await self.selfintroduction_reset(dm)

    async def selfintroduction_msg_update(self, member):
        member_data = self.db_select_selfintroduction(member)
        channel = self.INTRODUCTION_CHANNEL
        msg_id = member_data["sendmsg_id"]
        if msg_id:
            # 既存の自己紹介メッセージを削除
            selfintroduction_msg = await channel.fetch_message(msg_id)
            await selfintroduction_msg.delete()
        # 完成した自己紹介を送信
        await self.send_selfintroduction(member)

    async def send_message(self, channel, dm, msgcontent, content):
        """
        ---on_messageイベント内でのみ呼び出される---
        channelとdmにメッセージを送信するメソッド
        """
        await channel.send(msgcontent)
        await dm.send(embed=self.strfembed(content))

    # ---on_messageイベント内でのみ呼び出される---
    # チャンネル内のメッセージ総数を取得し、returnする
    async def get_count(self, channel):
        messages = await channel.history(limit=None).flatten()
        return len(messages)

    # ---全ての質問に答えたときに呼び出される---
    async def complete(self, channel, member_id):
        member = self.GUILD.get_member(member_id)
        print(f"complete: {member}")
        # dmオブジェクト作成
        dm = await member.create_dm()
        # 格納されたメッセージをすべて取得
        # embedにして整形
        embed = self.add_embed(member)
        # 完成した自己紹介文の最終チェック(修正が可能)
        embed_message = await dm.send(embed=embed)
        await dm.send(embed=self.strfembed("""\
この内容で自己紹介を登録しますか？
OKなら👍リアクションを、修正する場合は♻️リアクションを押して下さい。
部分的に修正する場合は一度👍リアクションを押して投稿した後に修正可能になります"""))
        # リアクションを追加
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("♻️")
        # 押されたemojiを取得
        emoji = await self.wait_reaction_add(channel,
                                             embed_message, ["👍", "♻️"])
        # 押された絵文字が👍の時(今の内容で登録する)
        if emoji == "👍":
            register_msg = await self.INTRODUCTION_CHANNEL.send(embed=embed)
            await register_msg.add_reaction("<:yoroshiku:761730298106478592>")
            await channel.send(register_msg.id)
            send_msg2 = "登録が完了しました" \
                + "※登録した自己紹介を修正したい場合は[ ¥predit ]とコマンドを送信してください"  # noqa: E501
            await dm.send(embed=self.strfembed(send_msg2))
        elif emoji == "♻️":
            await self.selfintroduction_reset(dm)

    # 自己紹介を初期化する処理
    async def selfintroduction_reset(self, dm) -> None:
        """
        DBの自己紹介データを初期化する処理
        ギルド・メンバーID、自己紹介が送信済みなら送信済みのカラムは変更しない
        その他のカラムをNoneに書き換える

        Parameter
        ---------
        dm : Discord.dm
            BOTにDMしたメンバーのDMオブジェクト
        """
        await dm.send(embed=self.strfembed("内容を全てリセットします"))
        # TextChannelを再度作成し直し、リセットする
        member = self.GUILD.get_member(dm.me.id)
        self.db_reset_selfintroduction(member)
        await dm.send(embed=self.strfembed(self.question1))

    # ---completeメソッド内でのみ呼び出される---
    # Embedオブジェクトを作成するメソッド

    def strfembed(self, str):
        """
        文字列をembedに変換する処理

        Parameter
        ---------
        str :　str
            embedに変換したい文字列

        Return
        ------
        embed : Discord.Embed
            strをDiscord.Embedに変換したオブジェクト
        """
        embed = discord.Embed(title=str)
        return embed

    # 質問内容を追加する場合は、ここを弄る
    def add_embed(self, member):
        obj = self.db_select_selfintroduction(member)
        embed = discord.Embed(
            title="自己紹介",
            description=f"name: {member.name}\njoined: {str(member.joined_at.strftime('%Y-%m-%d'))}",  # noqa: E501
            color=self.gender_color(obj['sex']))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="【 __呼び名__ 】",
                        value=f":name_badge: {obj['nickname']}",
                        inline=False)
        embed.add_field(name="【 __TwitterID__ 】",
                        value=f":globe_with_meridians: @{obj['twitter_id']}",
                        inline=False)
        embed.add_field(name="【 __得意分野__ 】",
                        value=f":ideograph_advantage: {obj['specialty']}",
                        inline=False)
        embed.add_field(name="【 __今まで勉強してきたこと__ 】",
                        value=f":books: {obj['before_study']}",
                        inline=False)
        embed.add_field(name="【 __これから勉強していきたいこと__ 】",
                        value=f":pencil: {obj['after_study']}",
                        inline=False)
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
    # channel内のメッセージlistの並びを逆にし、
    # disocrd.Messageオブジェクトじゃなくdiscord.Message.Contentを格納
    def adjust(self, messages):
        messages.reverse()
        return list(map(lambda messages: messages.content, messages))

    def messages_id(self, messages):
        return list(map(lambda messages: messages.id, messages))

    # ---completeメソッド内でのみ呼び出される---
    # リアクションが押されたら、そのリアクションをreturnする
    async def wait_reaction_add(self, message, emojis):
        """
        リアクションを押したユーザーがbotじゃなく、
        押された絵文字がemojisに格納されている絵文字あり、
        リアクションを押したメッセージのidが送信されたembedメッセージのidと同じで、
        リアクションを押したユーザーのidとDEBUGサーバー内のchannel名が一致した場合のみ、処理が走る

        Parameter
        ---------
        message : discord.Message
            自己紹介完成後の送信前の確認用のembedメッセージオブジェクト
        emojis : list
            確認用のembedメッセージに付与されて処理を通す絵文字の一覧
        """
        def check(reaction, user):
            return user.bot is False and reaction.emoji in emojis and reaction.message.id == message.id  # noqa: E501
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        # リアクションが押されたら、押されたリアクションをreturnする
        if reaction.emoji in emojis:
            return reaction.emoji

    def current_setting(self, list, member, number):
        desc = f"修正したい項目があればこのメッセージに付与されたリアクション（{number[0]}〜{number[4]}）を押してください"  # noqa: E501
        embed = discord.Embed(
            title="現在自己紹介を修正",
            description=desc,
            color=self.gender_color(list[1]))
        embed.add_field(name=f"{number[0]}", value=f"{list[0]}", inline=False)
        embed.add_field(name=f"{number[1]}", value=f"{list[2]}", inline=False)
        embed.add_field(name=f"{number[2]}", value=f"{list[3]}", inline=False)
        embed.add_field(name=f"{number[3]}", value=f"{list[4]}", inline=False)
        embed.add_field(name=f"{number[4]}", value=f"{list[5]}", inline=False)
        embed.add_field(
            name="♻️",
            value="初期化してもう一度初めから自己紹介を作成する場合",
            inline=False)
        return embed

    @commands.command()
    async def predit(self, message):
        if not isinstance(message.channel, discord.DMChannel):
            return
        member = self.GUILD.get_member(message.author.id)
        dm = await message.author.create_dm()
        for channel in self.DEBUG_GUILD.text_channels:
            if channel.name == str(message.author.id):
                # channelを見つけたらそのチャンネル内の合計メッセージ数を取得する
                messages = await channel.history(limit=None).flatten()
                if len(messages) != 7:
                    await dm.send(embed=self.strfembed("""\
自己紹介を登録してから[ ¥predit ]コマンドを使用して下さい。
何かメッセージを送信してみてください"""))
                    break
                # 修正項目を指定するためのリアクションのemojiを配列に格納
                emoji_number = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣"]
                embed = self.current_setting(
                    self.adjust(messages), member, emoji_number)
                embed_message = await dm.send(embed=embed)
                for emoji in emoji_number:
                    await embed_message.add_reaction(emoji)
                await embed_message.add_reaction("♻️")
                emoji_number.append("♻️")
                emoji = await self.wait_reaction_add(channel,
                                                     embed_message,
                                                     emoji_number)
                pr_messages = self.messages_id(messages)
                if emoji == "1⃣":
                    print(f"[INFO]: {member.name}: {emoji} のリアクションが押されました")
                    await self.send_message(channel,
                                            dm,
                                            pr_messages[0],
                                            self.question1)
                    break
                if emoji == "2⃣":
                    print(f"[INFO]: {member.name}: {emoji} のリアクションが押されました")
                    await self.send_message(channel,
                                            dm,
                                            pr_messages[2],
                                            self.question3)
                    break
                if emoji == "3⃣":
                    print(f"[INFO]: {member.name}: {emoji} のリアクションが押されました")
                    await self.send_message(channel,
                                            dm,
                                            pr_messages[3],
                                            self.question4)
                    break
                if emoji == "4⃣":
                    print(f"[INFO]: {member.name}: {emoji} のリアクションが押されました")
                    await self.send_message(channel,
                                            dm,
                                            pr_messages[4],
                                            self.question5)
                    break
                if emoji == "5⃣":
                    print(f"[INFO]: {member.name}: {emoji} のリアクションが押されました")
                    await self.send_message(channel,
                                            dm, pr_messages[5],
                                            self.question6)
                    break
                if emoji == "♻️":
                    print(f"[INFO]: {member.name}: {emoji} のリアクションが押されました")
                    await self.selfintroduction_reset(channel, message.channel)
                    break
        else:
            await self.DEBUG_GUILD.create_text_channel(str(message.author.id))
            await dm.send(embed=self.strfembed("""\
自己紹介文が見つかりませんでした。
質問に答えると自己紹介が登録できます。"""))
            await dm.send(embed=self.strfembed(self.question1))


def setup(bot):
    return bot.add_cog(Self_Introduction(bot))
