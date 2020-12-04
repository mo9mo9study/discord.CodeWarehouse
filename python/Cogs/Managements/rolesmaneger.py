from discord.ext import commands
import discord
import asyncio
from voiceChannelJoinLeave_roleModify import VoiceJoin_Role

class Reaction_AddRole(VoiceJoin_Role):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.message_id == 770081696761905163:
            await self.Add_Reaction(payload, "🇦", )
            await self.Add_Reaction(payload, "🇧", )
            await self.Add_Reaction(payload, "🇨", )
            await self.Add_Reaction(payload, "🇩", )
            await self.Add_Reaction(payload, "🇪", )
            await self.Add_Reaction(payload, "🇫", )
            await self.Add_Reaction(payload, "🇬", )
            channel = payload.member.guild.get_channel(704579339173494835)
            await self.send_message("add",payload,payload.member,channel)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        if payload.message_id == 770081696761905163:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            await self.Remove_Reaction(payload, member, "🇦", )
            await self.Remove_Reaction(payload, member, "🇧", )
            await self.Remove_Reaction(payload, member, "🇨", )
            await self.Remove_Reaction(payload, member, "🇩", )
            await self.Remove_Reaction(payload, member, "🇪", )
            await self.Remove_Reaction(payload, member, "🇫", )
            await self.Remove_Reaction(payload, member, "🇬", )
            channel = guild.get_channel(704579339173494835)
            await self.send_message("remove",payload,member,channel)

    async def Add_Reaction(self, payload, reaction, *args):
        if str(payload.emoji) == reaction:
            await self.AddRole(payload.member, *args)

    async def Remove_Reaction(self, payload, member, reaction, *args):
        if str(payload.emoji) == reaction:
            await self.RemoveRole(member, *args)

    async def send_message(self, mode, payload, member, channel):
        if mode == "add":
            text1 = "に"
            text2 = "を付与しました"
        elif mode == "remove":
            text1 = "から"
            text2 = "をはく奪しました"
        if str(payload.emoji) == "🇦":
            msg = await channel.send(f"{member.name}{text1}役職[ JOIN_gym ]{text2}")
        elif str(payload.emoji) == "🇧":
            msg = await channel.send(f"{member.name}{text1}役職[ RSS_AWS公式 ]{text2}")
        elif str(payload.emoji) == "🇨":
            msg = await channel.send(f"{member.name}{text1}役職[ RSS_AWS技術ブログ ]{text2}")
        elif str(payload.emoji) == "🇩":
            msg = await channel.send(f"{member.name}{text1}役職[ RSS_GCP公式 ]{text2}")
        elif str(payload.emoji) == "🇪":
            msg = await channel.send(f"{member.name}{text1}役職[ RSS_GCP技術ブログ ]{text2}")
        elif str(payload.emoji) == "🇫":
            msg = await channel.send(f"{member.name}{text1}役職[ RSS_etc ]{text2}")
        elif str(payload.emoji) == "🇬":
            msg = await channel.send(f"{member.name}{text1}役職[ RSS_itnews ]{text2}")
        await self.time_sleep(5,msg)

    async def time_sleep(self,second,msg):
        await asyncio.sleep(second)
        await msg.delete()

def setup(bot):
    return bot.add_cog(Reaction_AddRole(bot))