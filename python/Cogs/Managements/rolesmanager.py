from discord.ext import commands
import discord
import asyncio
from voiceChannelJoinLeave_roleModify import VoiceJoin_Role
import yaml

class Reaction_AddRole(VoiceJoin_Role):

    def __init__(self,bot):
        self.bot = bot
        self.guild_id = 603582455756095488
        self.channel_id = 704579339173494835

    @commands.Cog.listener()
    async def on_ready(self):
        with open('role.yaml',encoding="utf-8") as file:
            self.role = yaml.safe_load(file.read())

        channel = self.bot.get_guild(self.guild_id).get_channel(self.channel_id)
        messages = await channel.history(limit=1).flatten()
        for message in messages:
            await message.delete()

        role_name = map(lambda role_obj: role_obj["role_name"], self.role["roles"])
        role_reaction = map(lambda role_obj: role_obj["reaction"], self.role["roles"])
        desc = "\n".join(a + " : #" + b for a, b in zip(role_reaction, role_name))
        embed = discord.Embed(title="対応した役職を付与します", description=desc + "\n(※ 🗑️ : 自動で付与/剥奪できる役職全てを剥奪します )")
        for roles in self.role["roles"]:
            values = '\n- #'.join(roles['subChannel_name'])
            embed.add_field(name=f"[{roles['reaction']} : {roles['role_name']}]", value=f"- #{values}", inline=True)
        self.message = await channel.send(embed=embed)
        self.message_id = self.message.id

        for roles in self.role["roles"]:
            await self.message.add_reaction(roles["reaction"])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.member.bot:
            return
        if payload.message_id == self.message_id:
            channel = payload.member.guild.get_channel(self.channel_id)
            await self.wastebasket(payload, channel)
            for roles in self.role["roles"]:
                await self.Add_Reaction(payload, roles["reaction"], roles["roles_id"])
            await self.send_message("add",payload,payload.member,channel)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member.bot:
            return
        if payload.message_id == self.message_id:
            message = await guild.get_channel(self.channel_id).fetch_message(self.message_id)
            reactions = message.reactions
            for reaction in reactions:
                if str(reaction) == "🗑️":
                    break
            else:
                for roles in self.role["roles"]:
                    await self.Remove_Reaction(payload, member, roles["reaction"], roles["roles_id"])
                channel = guild.get_channel(self.channel_id)
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
        for roles in self.role["roles"]:
            if str(payload.emoji) == roles["reaction"]:
                msg = await channel.send(f"{member.name}{text1}役職[ {roles['role_name']} ]{text2}")
                await self.time_sleep(5, msg)

    async def time_sleep(self,second,msg):
        await asyncio.sleep(second)
        await msg.delete()

    async def wastebasket(self,payload ,channel):
        if str(payload.emoji) == "🗑️":
            for roles in self.role["roles"]:
                await self.Remove_Reaction(payload, payload.member, "🗑️", roles["roles_id"])
                await self.message.remove_reaction(roles["reaction"], payload.member)
            msg = await channel.send("全てのロールをはく奪しました")
            await self.message.remove_reaction("🗑️", payload.member)
            await self.time_sleep(5, msg)



def setup(bot):
    return bot.add_cog(Reaction_AddRole(bot))