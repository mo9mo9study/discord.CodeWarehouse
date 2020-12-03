# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio

class VoiceJoin_Role(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        if after.channel is not None:                         #vcに参加した時
            if after.channel.id == A:                         #変数Aには作業部屋チャンネルのidを入れて下さい
                await self.AddRole(member, a, b)              #引数a,bにはmusic_role,作業部屋用チャットRoleのidを入れてください
            elif after.channel.id == B:                       #変数Bにはラウンジチャンネルのidを入れて下さい
                await AddRole(member, a, c)                   #引数a,cにはmusic_role,ラウンジ用チャットRoleのidを入れてください
        if before.channel is not None:
            if before.channel.id in (A,B):                    #変数A,Bには作業部屋チャンネル,ラウンジチャンネルのidを書いてください
                await self.RemoveRole(member, a, b, c)        #引数a,b,cにはmusic_role,作業部屋用チャットRole,ラウンジ用チャットRoleのidを書いてください

    async def AddRole(self,member,*args):
        for role_id in args:
            role = member.guild.get_role(role_id)
            await member.add_roles(role)

    async def RemoveRole(self,member,*args):
        for role_id in args:
            role = member.guild.get_role(role_id)
            await member.remove_roles(role)

def setup(bot):
    return bot.add_cog(VoiceJoin_Role(bot))