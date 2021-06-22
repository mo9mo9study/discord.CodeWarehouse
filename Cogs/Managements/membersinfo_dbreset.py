from datetime import datetime
from discord.ext import commands, tasks
import emojis
import re
from sqlalchemy import Column, String, Integer, DateTime, Boolean
import os

from mo9mo9db.dbtables import Studymembers
from mo9mo9db.dbsession import get_db_engine


class MemberstableReset(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488 # mo9mo9サーバーID
        self.engine = get_db_engine()
        self.fname = os.path.basename(__file__)
    
    # 注意: [🍀supleiades🍀]のような名前の場合、全て消えてしまう
    #       🍀: :four_leaf_clover:
    #       以下の関数は:と:の間の文字列を削除する処理
    def remove_emoji(self, src_str) -> str:
        decode_str = emojis.decode(src_str)
        return re.sub(":.*:", "", decode_str)
    
    def users_counter(self) -> [int, int]:
        session = Studymembers.session()
        db_userscount = session.query(Studymembers).filter(Studymembers.enrollment==True).count()
        members = self.bot.get_guild(self.GUILD_ID).members
        discord_userscount = sum(1 for member in members if not member.bot)
        return db_userscount, discord_userscount

    async def memberstable_reset(self):
        session = Studymembers.session()
        session.query(Studymembers).delete()
        members = self.bot.get_guild(self.GUILD_ID).members
        discord_userscount = sum(1 for member in members if not member.bot)
        members_human = []
        for i in members:
            if not i.bot:
                members_human.append(Studymembers(
                    guild_id = i.guild.id,
                    member_id = i.id,
                    member_name = self.remove_emoji(i.display_name),
                    joined_dt = i.joined_at,
                    enrollment = True
                ))
        session.bulk_save_objects(members_human)
        session.commit()
        return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def admin_memberstable_reset(self, ctx):
        db_userscount, discord_userscount = self.users_counter()
        print(f"({self.fname}):[INFO]: Discord({discord_userscount}/users),DB({db_userscount}/users)")
        await self.memberstable_reset()

    # ---------------定期処理---------------
    # 午前4:00に実行されます
    # データを全削除してユーザー数分追加するので
    # オートインクリメントのnoカラムは連続して記録されるので
    # 160人分削除した場合、追加は161からの数字が振られます
    @tasks.loop(seconds=59)
    async def loop(self):
        await self.bot.wait_until_ready()
        now = datetime.now().strftime('%H:%M')
        if now == "04:00":
            db_userscount, discord_userscount = self.users_counter()
            # DBとDiscordのユーザー数が異なる時のみ実行
            if db_userscount != discord_userscount:
                self.memberstable_reset()
                print(f"({self.fname}):[INFO]: Discord({discord_userscount})とDB({db_userscount})にユーザーの差分が見つかったので実行しました。")
            else:
                print(f"({self.fname}):[INFO]: Discord({discord_userscount})とDB({db_userscount})にユーザーの差分が無かったので実行しませんでした。")


def setup(bot):
    return bot.add_cog(MemberstableReset(bot))       