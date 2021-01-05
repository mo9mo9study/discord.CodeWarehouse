from discord.ext import commands
import discord
import asyncio

class MemberOrganization(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.GUILD_ID = 770973096215707648 #mo9mo9サーバーのid
        self.target_list = [] #空のlist 変更しないでください

    #Bot起動時にguildを読み込む
    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)

    @commands.command()
    async def kick(self, ctx, subcommand, id=None):
        #管理者のみ実行可能
        if not ctx.author.guild_permissions.administrator:
            return

        #---対象者をtarget_listに追加する処理---
        if subcommand == "add":
            #userを取得し、成功したらTrueとdiscord.Memberオブジェクトが帰ってくる
            #エラーが出ると、FalseとNoneが帰ってくる
            bool,user = await self.get_user(ctx, id)
            #Trueだった場合
            if bool:
                #既にtarget_listにuserが入っているか確認
                if user in self.target_list:
                    #入っていた場合はlistに追加しない
                    await ctx.send(f"{user.name}は既にlistに入っています。")
                    return
                #listに追加し、今追加したユーザーの名前と現在のlistに追加されている人数を表示
                self.target_list.append(user)
                count = len(self.target_list)
                await ctx.send(f"{user.name}をlistに追加しました。現在{str(count)}人")

        #---対象者をtarget_listから取り消す処理---
        elif subcommand == "remove":
            #userを取得し、成功したらTrueとdiscord.Memberオブジェクトが帰ってくる
            #エラーが出ると、FalseとNoneが帰ってくる
            bool, user = await self.get_user(ctx, id)
            #Trueだった場合
            if bool:
                #target_listにuserが入っているか確認
                if user not in self.target_list:
                    #入ってない場合はエラー文を出す
                    await ctx.send(f"{user.name}はlistに入ってないため、取り消せませんでした。")
                    return
                #listから取り消し、今取り消したユーザーの名前と現在のlistに追加されている人数を表示
                self.target_list = [t for t in self.target_list if t != user]
                count = len(self.target_list)
                await ctx.send(f"{user.name}をlistから取り消しました。現在{str(count)}人")

        #---対象者一覧を表示する処理---
        elif subcommand == "targets":
            #target_listの中身をdiscord.Memberオブジェクトからnameオブジェクトに変更
            display_list = list(map(lambda t:t.name, self.target_list))
            #要素ごとに改行を挟む
            display_list = "\n".join(display_list)
            #現在のlistに追加されている人数とlist内の人全員を表示
            count = len(display_list)
            await ctx.send(f"現在{str(count)}人がlistに入っています。\n{display_list}")

        #---対象者に処理を実行するコマンド---
        elif subcommand == "run":
            await ctx.send("処理を開始します。")
            for member in self.target_list:
                #自動メッセージを対象者のDMに送る
                dm = await member.create_dm()
                await dm.send(txt)
                #対象者のtimesを削除
                for channel in self.GUILD.text_channels:
                    if channel.topic == str(member.id):
                        await channel.delete()
                        break
                #メンバーをキック
                await member.kick()

        #---対象者listをリセットする---
        elif subcommand == "reset":
            self.target_list = []
            await ctx.send("対象者listをリセットしました")



    #---kickコマンド内の[add/remove]処理でのみ呼び出されます---
    async def get_user(self, ctx, id):
        # idがNoneの時(引数に何も入ってない時)、idを入れるよう促す
        if id == None:
            await ctx.send("第二引数に対象者のidを入れてください。")
            return False, None
        # 引数idに数字以外を入れてしまって、intに変換した時にエラーが出るのを防ぐための例外処理
        try:
            # 引数idからdiscord.Memberオブジェクトを取得
            user = self.GUILD.get_member(int(id))
        # valueErrorが出たときに警告文を表示
        except ValueError:
            await ctx.send("第二引数には数字のみを入れて下さい。")
        # discord.Memberオブジェクトを正常に取得できた時の処理
        else:
            # userが取得出来なかった時にエラー文を出す
            if user is None:
                await ctx.send("userが見つかりませんでした。\nidが間違ってないか確認してください。")
                return False, None
            return True , user

txt = """
当ギルド[ もくもくOnline勉強会 ]で
以下の整理対象条件のいずれかを満たしたためギルドメンバーから削除致しました。
- 学びの活動(勉強記録)が２ヶ月以上確認できない
- 初参加から一定の活動がみられない

このメッセージに気付き、
また、この学び続ける仲間が居るコミュニティを活用し、
メンバー同士刺激しつつ「やる気」を維持していきたいと
思われた時は下記のTwitterかbopsyuまで連絡下さい

改めて招待URLを発行し、仲間一同参加を快く歓迎します
※ギルドの質担保のための行動へのご理解よろしくお願い致します。

・もくもくOnline勉強会専用Twitterアカウント
  	@mo9mo9study
・bosyuのギルドメンバー募集ページ
  	https://bosyu.me/b/G43e6INUpQw
"""

def setup(bot):
    return bot.add_cog(MemberOrganization(bot))