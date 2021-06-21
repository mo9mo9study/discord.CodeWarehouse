from discord.ext import commands
import discord
import asyncio
import inspect
from sqlalchemy import Column, String, Integer, DateTime, Boolean
import emojis
import re

from mo9mo9db.dbtables import Studymembers
from mo9mo9db.dbsession import get_db_engine

class Join_Leave_Log(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488 # mo9mo9サーバーID
        self.CHANNEL_ID = 708303469882114058 #参加・離脱ログ用チャンネルid
        self.old_invite_list = []

    def remove_emoji(self, src_str):
        decode_str = emojis.decode(src_str)
        return re.sub(":.*:", "" ,decode_str)

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.CHANNEL = self.GUILD.get_channel(self.CHANNEL_ID)
        self.old_invite_list = await self.GUILD.invites()

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        self.old_invite_list = await self.GUILD.invites()

    async def uses_if(self,U_new_list,U_old_list,new_list):
        for a,b,c in zip(U_new_list,U_old_list,range(len(new_list))):
            if a != b:
                return new_list[c].inviter.mention

    @commands.Cog.listener()
    async def on_member_join(self, member):
        new_invite_list = await self.GUILD.invites()
        old_invite_list_uses = list(map(lambda invite: invite.uses, self.old_invite_list))
        new_invite_list_uses = list(map(lambda invite: invite.uses, new_invite_list))
        inviter_mention = await self.uses_if(new_invite_list_uses,old_invite_list_uses,new_invite_list)
        text = f"**{member.name} (id:__{str(member.id)}__) が参加しました。【 招待者：{inviter_mention} 】**"
        # dbにメンバー情報書き込み
        session = Studymembers.session()
        add_date = Studymembers(
            guild_id = member.guild.id,
            member_id = member.id,
            member_name = self.remove_emoji(member.display_name),
            joined_dt = member.joined_at,
            enrollment = True
        )
        Studymembers.insert(add_date)
        print(text)
        await self.CHANNEL.send(text)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        text = f"**{member.name} (id:__{str(member.id)}__) が離脱しました。**"
        # dbからメンバー情報を削除
        session = Studymembers.session()
        delete_date = session.query(Studymembers).filter(Studymembers.member_id==member.id).first()
        session.delete(delete_date)
        session.commit()
        print(text)
        await self.CHANNEL.send(text)


def setup(bot):
    return bot.add_cog(Join_Leave_Log(bot))