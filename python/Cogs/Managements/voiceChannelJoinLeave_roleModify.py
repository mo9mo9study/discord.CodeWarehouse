# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio


# 「作業部屋用チャット」表示権限ID
workRoomChatRoleId = 763401369784156211
# 「ラウンジ用チャット」表示権限ID
loungeChatRoleId = 763400537257148446
# 「musicbot操作用」表示権限ID
musicChatRokeId = 710333297598922752
# 「作業部屋」ID
workRoomVoiceChatId = 683864874539024397
# 「ラウンジ」ID
loungeVoiceChatId = 603582455756095492

class VoiceJoin_Role(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        print(0)
        print("after: ", after)
        print("before: ", before)
        if after.channel != before.channel: 
            print("-------------------")
            print(member.name)
            print(1)
            if after.channel is not None:                         #vc参加時
                print(2)
                if after.channel.id == workRoomVoiceChatId:
                    print("after: ",after.channel.name)
                    print(3)
                    await self.AddRole(member, musicChatRokeId, workRoomChatRoleId)
                elif after.channel.id == loungeVoiceChatId:
                    print(4)
                    await self.AddRole(member, musicChatRokeId, loungeChatRoleId)
            if before.channel is not None:                        #vc退席時
                print("before: ",before.channel.name)
                print(5)
                if before.channel.id in (workRoomVoiceChatId, loungeVoiceChatId):
                    await self.RemoveRole(member, musicChatRokeId, workRoomChatRoleId, loungeChatRoleId)

    async def AddRole(self,member,*args):
        print(6)
        for role_id in args:
            role = member.guild.get_role(role_id)
            print("付与した権限名: ",role.name)
            await member.add_roles(role)
        print("入室後の付与されている権限: ",member.roles)

    async def RemoveRole(self,member,*args):
        print(7)
        for role_id in args:
            role = member.guild.get_role(role_id)
            print("剥奪した権限名: ",role.name)
            await member.remove_roles(role)
        print("退室後の付与されている権限: ",member.roles)

def setup(bot):
    return bot.add_cog(VoiceJoin_Role(bot))
