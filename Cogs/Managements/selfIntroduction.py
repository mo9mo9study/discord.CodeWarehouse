import discord
from discord.ext import commands

from mo9mo9db.dbtables import Selfintroduction


class Self_Introduction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488  # mo9mo9サーバーのID
        self.INTRODUCTION_CHANNEL_ID = 615185771565023244  # mo9mo9の自己紹介チャンネル
        self.LOG_CHANNEL_ID = 801060150433153054
        # self.GUILD_ID = 696268022930866177
        # self.INTRODUCTION_CHANNEL_ID = 909813699072643092
        # self.LOG_CHANNEL_ID = 909813908699754516

        self.emoji_number = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣"]
        # 以下、質問６項目
        self.question1 = "\> 呼び名を教えてください"  # noqa: W605
        self.question2 = "\> [男/女/非公開]から選んで送信してください"  # noqa: W605
        self.question3 = "\> TwitterIDを入力してください\n@マークは要りません"  # noqa: W605
        self.question4 = "\> 得意分野は何ですか？"  # noqa: W605
        self.question5 = "\> 今まで何を勉強してきましたか？"  # noqa: W605
        self.question6 = "\> これから勉強していきたいことは何ですか？"  # noqa: W605
        self.command_names = ["¥predit"]

    # Botを起動したときに__init__に格納したIDからオブジェクトを取得

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.INTRODUCTION_CHANNEL = self.GUILD.get_channel(
            self.INTRODUCTION_CHANNEL_ID)
        self.LOG_CHANNEL = self.GUILD.get_channel(self.LOG_CHANNEL_ID)
        # 全てのパラメータが埋まっている状態で、まだ自己紹介を送信していない場合
        # 後ほど必要になるだろう処理

        # 再度確認用のメッセージをDMに送る処理追加
        # for channel in self.DEBUG_GUILD.text_channels:
        #     count = await self.get_count(channel)
        #     if count == 6:
        #         member = guild.get_member(
        #             int(channel.name))
        #         print(f"自己紹介を送信していないユーザー: {member}/{channel}")
        #         if member is None:
        #             return
        #         await self.complete(channel, member.id)

    async def db_insert_selfintroduction(self, session, member):
        """
        メンバー参加時、その他レコードが存在しない時に対象メンバーのレコードを作成
        ギルドID,メンバーID,次修正するカラムに"nickname"を挿入する

        Parameter
        ---------
        member : discord.Member
            message.authorから取得したメンバーオブジェクト
        """
        member_data = self.db_select_selfintroduction(session, member)
        if not member_data:
            # メンバーのレコードが存在しなければ作成する
            obj = Selfintroduction(
                guild_id=member.guild.id,
                member_id=member.id,
            )
            obj.mod_column = "nickname"
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
        session = Selfintroduction.session()
        # selfintroductionテーブルに参加したメンバーの情報をinsert
        await self.db_insert_selfintroduction(session, member)
        # 参加者にdmを送る
        send_msg = "ギルドへの参加ありがとうございます"\
            + "\nこれから自己紹介の処理を進めますので、質問に答えて下さい"
        await dm.send(embed=self.strfembed(send_msg))  # noqa: E501
        await dm.send(embed=self.strfembed(self.question1))

    def db_select_selfintroduction(self, session, member):
        """
        対象メンバーの自己紹介データを取得する

        Parameter
        ---------
        member : discord.Member
            message.authorから取得したメンバーオブジェクト
        """
        # session = Selfintroduction.session()
        obj = Selfintroduction.objects(session).filter(
            Selfintroduction.member_id == member.id,
            Selfintroduction.guild_id == member.guild.id).first()
        return obj

    def db_reset_selfintroduction(self, session, member) -> None:
        """
        対象メンバーの自己紹介データのメンバーが対話式でデータを挿入できるカラムを初期化

        Parameter
        ---------
        member : discord.Member
            message.authorから取得したメンバーオブジェクト
        """
        # session = Selfintroduction.session()
        obj = self.db_select_selfintroduction(session, member)
        reset_columns = ["nickname", "gender", "twitter_id", "specialty",
                         "before_study", "after_study"]
        for column in reset_columns:
            setattr(obj, column, None)
        obj.mod_column = "nickname"
        session.add(obj)
        session.commit()

    def db_update_selfintroduction(self, session, member, select_column,
                                   after_value, next_mod_column) -> None:
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
        # session = Selfintroduction.session()
        obj = self.db_select_selfintroduction(session, member)
        # obj(bind=session)
        setattr(obj, select_column, after_value)
        if select_column != "mod_column":
            # 変更するカラムが"mod_column"以外の時
            if next_mod_column:
                # next_mod_columnに値が含まれている時
                obj.mod_column = next_mod_column
            else:
                # 自己紹介送信時にmod_columnをNoneにするため
                obj.mod_column = None
        session.add(obj)
        # session.flush()
        session.commit()

    def check_missingdata(self, session, member) -> str:
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
        member_data = self.db_select_selfintroduction(session, member)
        m_d = member_data
        missingdata_column = None
        next_missingdata_column = None
        # 次修正するカラムを確認
        if not m_d.nickname and m_d.mod_column != "nickname":
            next_missingdata_column = "nickname"
        elif not m_d.gender and m_d.mod_column != "gender":
            next_missingdata_column = "gender"
        elif not m_d.twitter_id and m_d.mod_column != "twitter_id":
            next_missingdata_column = "twitter_id"
        elif not m_d.specialty and m_d.mod_column != "specialty":
            next_missingdata_column = "specialty"
        elif not m_d.before_study and m_d.mod_column != "before_study":
            next_missingdata_column = "before_study"
        elif not m_d.after_study and m_d.mod_column != "after_study":
            next_missingdata_column = "after_study"
        elif not m_d.sendmsg_id and m_d.mod_column != "sendmsg_id":
            next_missingdata_column = "sendmsg_id"
        # 今回修正するカラムを確認
        if m_d.mod_column:
            missingdata_column = m_d.mod_column
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
        elif next_missingdata_column == "gender":
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
        elif not next_missingdata_column:
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
            send_msg = "自己紹介の編集中です\n文字列を送信してください"
            await dm.send(embed=self.strfembed(send_msg))
            check_msg = False
        else:
            if missingdata_column == "gender":
                if msg_cont not in ["男", "女", "非公開"]:
                    check_msg = False
        return check_msg

    async def send_selfintroduction(self, session, member) -> None:
        """
        DBに補完された自己紹介データをEmbedの形に入れ込み、自己紹介を送信する

        Parameter
        ---------
        member : discord.Member
            message.authorから取得したメンバーオブジェクト
        """
        dm = await member.create_dm()
        embed = self.add_embed(session, member)
        # 完成した自己紹介文の最終チェック(修正が可能)
        embed_message = await dm.send(embed=embed)
        send_msg = "この内容で自己紹介を登録しますか？"\
            + "\nOKなら👍リアクションを、修正する場合は♻️リアクションを押して下さい。"\
            + "\n部分的に修正する場合は一度👍リアクションを押して投稿した後に修正可能になります"  # noqa: E501
        await dm.send(embed=self.strfembed(send_msg))
        # リアクションを追加
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("♻️")
        # 押されたemojiを取得
        emoji = await self.wait_reaction_add(embed_message, ["👍", "♻️"])
        # 押された絵文字が👍の時(今の内容で登録する)
        if emoji == "👍":
            # 新しい自己紹介を送信
            after_msg = await self.INTRODUCTION_CHANNEL.send(embed=embed)
            # 過去の自己紹介を削除
            await self.delete_before_selfintroduction_msg(session, member)
            # await after_msg.add_reaction("<:yoroshiku:761730298106478592>")
            send_msg2 = "登録が完了しました" \
                + "\n※登録した自己紹介を修正したい場合は[ ¥predit ]のコマンド(7文字)を送信してください"   # noqa: E501
            await dm.send(embed=self.strfembed(send_msg2))
            # DBの自己紹介メッセージのIDを過去のIDから新しいIDに更新する
            self.db_update_selfintroduction(session, member, "sendmsg_id",
                                            after_msg.id, None)
        elif emoji == "♻️":
            await self.selfintroduction_reset(session, member, dm)

    async def delete_before_selfintroduction_msg(self, session, member):
        """DBから過去にメッセージを送信した記録があった場合、そのメッセージを削除する"""
        member_data = self.db_select_selfintroduction(session, member)
        channel = self.INTRODUCTION_CHANNEL
        msg_id = member_data.sendmsg_id
        log_msg = ""
        if msg_id:
            if msg_id.isdecimal():
                # 既存の自己紹介メッセージを削除
                try:
                    selfintroduction_msg = await channel.fetch_message(int(msg_id))  # noqa: E501
                    # メッセージが取得できない場合の処理
                    await selfintroduction_msg.delete()
                    log_msg = f"[INFO] {member.name}の過去の自己紹介を削除し、新しい自己紹介を送信しました"  # noqa: E501
                except discord.NotFound:
                    log_msg = f"[WARN] {member.name}の自己紹介を送信しましたが、過去の自己紹介の削除に失敗しました"  # noqa: E501
        if not log_msg:
            # 新規自己紹介（過去に自己紹介を送信してない）場合
            log_msg = f"[INFO] {member.name}の自己紹介が送信されました"
        await self.LOG_CHANNEL.send(log_msg)
        print(log_msg)

    # 自己紹介を初期化する処理
    async def selfintroduction_reset(self, session, member, dm) -> None:
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
        self.db_reset_selfintroduction(session, member)
        await dm.send(embed=self.strfembed(self.question1))

    def strfembed(self, str) -> discord.Embed:
        """
        ---completeメソッド内でのみ呼び出される---
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
    def add_embed(self, session, member) -> discord.Embed:
        """
        自己紹介メッセージを作成するテンプレート
        DBから自己紹介データを取得し、
        自己紹介メッセージの完成形を作成する

        Parameter
        ---------
        member : discord.Member
            message.authorから取得したメンバーオブジェクト

        Return
        ------
        embed : discord.Embed
            自己紹介メッセージの完成版のembedオブジェクト
        """
        obj = self.db_select_selfintroduction(session, member)
        desc_msg = f"name: {member.name}"\
            + f"\njoined: {str(member.joined_at.strftime('%Y-%m-%d'))}"
        embed = discord.Embed(
            title="自己紹介",
            description=desc_msg,
            color=self.gender_color(obj.gender))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="【 __呼び名__ 】",
                        value=f":name_badge: {obj.nickname}",
                        inline=False)
        embed.add_field(name="【 __TwitterID__ 】",
                        value=f":globe_with_meridians: @{obj.twitter_id}",
                        inline=False)
        embed.add_field(name="【 __得意分野__ 】",
                        value=f":ideograph_advantage: {obj.specialty}",
                        inline=False)
        embed.add_field(name="【 __今まで勉強してきたこと__ 】",
                        value=f":books: {obj.before_study}",
                        inline=False)
        embed.add_field(name="【 __これから勉強していきたいこと__ 】",
                        value=f":pencil: {obj.after_study}",
                        inline=False)
        embed.set_footer(text=f"{member.id}")
        return embed

    def gender_color(self, gender) -> int:
        """
        入力された性別によって、embedのカラーを変える

        Parameter
        ---------
        gender : str
            メンバーが指定した性別を格納している

        Return
        ------
        int
            16進数のカラーコード
        """
        if gender in "男":
            return 0x4093cf
        elif gender in "女":
            return 0xba3fb4
        elif gender in "非公開":
            return 0x51c447

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

    def current_setting(self, session, member, number):
        obj = self.db_select_selfintroduction(session, member)
        desc = f"修正したい項目があればこのメッセージに付与されたリアクション（{number[0]}〜{number[-1]}）を押してください"  # noqa: E501
        embed = discord.Embed(
            title="現在自己紹介を修正",
            description=desc,
            color=self.gender_color(obj.gender))
        embed.add_field(name=f"{number[0]}",
                        value=obj.nickname, inline=False)
        embed.add_field(name=f"{number[1]}", value=obj.gender, inline=False)
        embed.add_field(name=f"{number[2]}",
                        value=obj.twitter_id, inline=False)
        embed.add_field(name=f"{number[3]}",
                        value=obj.specialty, inline=False)
        embed.add_field(name=f"{number[4]}",
                        value=obj.before_study, inline=False)
        embed.add_field(name=f"{number[5]}",
                        value=obj.after_study, inline=False)
        embed.add_field(
            name="♻️",
            value="初期化してもう一度初めから自己紹介を作成する場合",
            inline=False)
        return embed

    def emoji_mod_column(self, session, member, emoji):
        send_msg = f"[INFO] BOTのDMで{member.name}が{emoji}のリアクションを押下"
        print(send_msg)
        if emoji in self.emoji_number:
            if emoji == "1⃣":
                select_column = "nickname"
            elif emoji == "2⃣":
                select_column = "gender"
            elif emoji == "3⃣":
                select_column = "twitter_id"
            elif emoji == "4⃣":
                select_column = "specialty"
            elif emoji == "5⃣":
                select_column = "before_study"
            elif emoji == "6⃣":
                select_column = "after_study"
            self.db_update_selfintroduction(session, member, "mod_column",
                                            select_column, None)
        elif emoji == "♻️":
            self.db_reset_selfintroduction(session, member)
        else:
            # 想定する絵文字以外のリアクションが発生した場合
            log_msg = "[WARN] 想定しないリアクションです"
            print(log_msg)
            return

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        メンバーから送信されるBOTへのDMをトリガーに実行される
        自己紹介を作成、修正する際に使用される
        """
        if not isinstance(message.channel, discord.DMChannel):
            return
        if message.author.bot:
            return
        # on_messageはcommand[¥predit]のメッセージにも反応してしまい
        # 1つのメッセージで2度処理されてしまう問題を以下のreturnで解決
        if message.content in self.command_names:
            return
        dm = await message.author.create_dm()
        member = self.GUILD.get_member(message.author.id)
        session = Selfintroduction.session()
        # メンバーのレコードが存在しない場合には新規作成
        await self.db_insert_selfintroduction(session, member)
        # 受信したメッセージの内容をどのカラムに保存するかを確認
        # 次不足しているデータの確認
        missingdata_column, next_missingdata_column = self.check_missingdata(
            session, member)
        if missingdata_column != "sendmsg_id":
            # mod_columnが[sendmsg_id]以外の時
            # データのチェック
            check_msg = await self.check_msg_content(dm, missingdata_column,
                                                     message.content)
            if not check_msg:
                # 想定しない文字列の場合は再度同じ質問を行い、return
                send_msg = self.select_nextquestionmsg(missingdata_column)
                await dm.send(embed=self.strfembed(send_msg))
                return
        if missingdata_column:
            # 修正するカラムがある時
            if "sendmsg_id" not in missingdata_column:
                # 自己紹介が完成した時
                self.db_update_selfintroduction(session, member,
                                                missingdata_column,
                                                message.content,
                                                next_missingdata_column)
                # 不足しているデータから次の送信メッセージを選択
                send_msg = self.select_nextquestionmsg(next_missingdata_column)
                await dm.send(embed=self.strfembed(send_msg))
            if next_missingdata_column is None and "sendmsg_id" not in missingdata_column:  # noqa: E501
                # ¥predit（自己紹介送信済）から一つのカラムを修正した時
                await self.send_selfintroduction(session, member)

            if "sendmsg_id" in [missingdata_column, next_missingdata_column]:
                # メッセージを勉強ギルドに送信する処理
                await self.send_selfintroduction(session, member)
            # session.commit()
        else:
            # 自己紹介が完成しており、変更カラムもなく送信済み
            send_msg = f"{message.author.name}さんの自己紹介文は既に登録済みです。"\
                + "\n変更する場合は、[ ¥predit ]とコマンドを送信して下さい。"
            await dm.send(embed=self.strfembed(send_msg))
            return

    @commands.command()
    async def predit(self, message):
        """
        既存の自己紹介データを送信し、修正するカラムをメンバーに指定してもらう
        リアクションで対象のカラムを指定し、mod_columnに対象カラムを保存する
        """
        if not isinstance(message.channel, discord.DMChannel):
            return
        member = self.GUILD.get_member(message.author.id)
        dm = await message.author.create_dm()
        session = Selfintroduction.session()
        embed = self.current_setting(session, member, self.emoji_number)
        send_embedmsg = await dm.send(embed=embed)
        # メッセージにリアクションを付与
        for emoji in self.emoji_number:
            await send_embedmsg.add_reaction(emoji)
        await send_embedmsg.add_reaction("♻️")
        check_emojis = self.emoji_number + ["♻️"]
        emoji = await self.wait_reaction_add(send_embedmsg, check_emojis)
        if emoji in self.emoji_number:
            # 指定した修正するカラムをDBに保存
            self.emoji_mod_column(session, member, emoji)
            missingdata_column, _ = self.check_missingdata(
                session, member)
            send_msg = self.select_nextquestionmsg(missingdata_column)
            await dm.send(embed=self.strfembed(send_msg))
        if emoji == "♻️":
            await self.selfintroduction_reset(session, member, dm)
        # DBのmod_columnから次の質問する内容を選別し、DMで送信する


def setup(bot):
    return bot.add_cog(Self_Introduction(bot))
