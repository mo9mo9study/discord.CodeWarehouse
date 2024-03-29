# -*- coding: utf-8 -*-

from discord.ext import commands


class VoiceJoin_Role(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488
        self.workRoomChatRoleId = 763401369784156211  # 「作業部屋用チャット」表示権限ID
        self.loungeChatRoleId = 763400537257148446  # 「ラウンジ用チャット」表示権限ID
        self.musicChatRoleId = 710333297598922752  # 「musicbot操作用」表示権限ID
        self.workRoomVoiceChatId = 683864874539024397  # 「作業部屋」ID
        self.loungeVoiceChatId = 603582455756095492  # 「ラウンジ」ID

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel != before.channel:
            if after.channel is not None:  # 対象VC参加時
                if after.channel.id == self.workRoomVoiceChatId:
                    print(f"[INFO] {member.name}が{after.channel.name}に入室")
                    await self.AddRole(member,
                                       self.GUILD,
                                       self.musicChatRoleId,
                                       self.workRoomChatRoleId)
                elif after.channel.id == self.loungeVoiceChatId:
                    print(f"[INFO] {member.name}が{after.channel.name}に入室")
                    await self.AddRole(member,
                                       self.GUILD,
                                       self.musicChatRoleId,
                                       self.loungeChatRoleId)
            if before.channel is not None:  # 対象VC退室時
                if before.channel.id in (self.workRoomVoiceChatId,
                                         self.loungeVoiceChatId):
                    print(f"[INFO] {member.name}が{before.channel.name}から退室")
                    await self.RemoveRole(member,
                                          self.GUILD,
                                          self.musicChatRoleId,
                                          self.workRoomChatRoleId,
                                          self.loungeChatRoleId)

    async def AddRole(self, member, guild, *args):
        for role_id in args:
            role = guild.get_role(role_id)
            print(f"[INFO] {member.name}に権限「{role.name}」を付与")
            await member.add_roles(role)

    async def RemoveRole(self, member, guild, *args):
        for role_id in args:
            role = guild.get_role(role_id)
            print(f"[INFO] {member.name}から権限「{role.name}」を剥奪")
            await member.remove_roles(role)


def setup(bot):
    return bot.add_cog(VoiceJoin_Role(bot))
