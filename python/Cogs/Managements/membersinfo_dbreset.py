from datetime import datetime
from discord.ext import commands, tasks
import emojis
import re
from sqlalchemy import Column, String, Integer, DateTime, Boolean

from mo9mo9db.dbtables import Studymembers
from mo9mo9db.dbsession import get_db_engine


class MemberstableReset(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488 # mo9mo9サーバーID
        self.engine = get_db_engine()
    
    # 注意: [🍀supleiades🍀]のような名前の場合、全て消えてしまう
    #       🍀: :four_leaf_clover:
    #       以下の関数は:と:の間の文字列を削除する処理
    def remove_emoji(self, src_str):
        decode_str = emojis.decode(src_str)
        return re.sub(":.*:", "" ,decode_str)

    def memberstable_reset(self):
        Studymembers.__table__.drop(self.engine)
        Studymembers.__table__.create(self.engine)
        session = Studymembers.session()
        members = self.bot.get_guild(self.GUILD_ID).members
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
        self.memberstable_reset()

    # ---------------定期処理---------------
    # 午前4:00に実行されます
    @tasks.loop(seconds=59)
    async def loop(self):
        await self.bot.wait_until_ready()
        now = datetime.now().strftime('%H:%M')
        if now == "04:00":
            self.memberstable_reset()


def setup(bot):
    return bot.add_cog(MemberstableReset(bot))       