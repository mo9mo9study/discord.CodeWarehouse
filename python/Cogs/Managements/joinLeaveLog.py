from discord.ext import commands
import discord
import asyncio
import inspect

class Join_Leave_Log(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488 # mo9mo9サーバーID
        self.CHANNEL_ID = 708303469882114058 #参加・離脱ログ用チャンネルid
        self.old_invite_list = []

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
        text = f"{member.name} (id:__{str(member.id)}__) が参加しました。【 招待者：{inviter_mention} 】"
        print(text)
        await self.CHANNEL.send(text)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        text = f"{member.name} (id:__{str(member.id)}__) が離脱しました。"
        print(text)
        await self.CHANNEL.send(text)


def setup(bot):
    return bot.add_cog(Join_Leave_Log(bot))