import asyncio

from discord.ext import commands
import discord
import yaml

from .voiceChannelJoinLeave_roleModify import VoiceJoin_Role


class Reaction_AddRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488
        self.channel_id = 704579339173494835

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        with open('Settings/role.yaml', encoding="utf-8") as file:
            self.role = yaml.safe_load(file.read())

        self.channel = self.bot.get_guild(
            self.GUILD_ID).get_channel(self.channel_id)
        await self.channel.purge()

        role_name = map(
            lambda role_obj: role_obj["role_name"], self.role["roles"])
        role_reaction = map(
            lambda role_obj: role_obj["reaction"], self.role["roles"])
        desc = "\n".join(a + " : #" + b for a,
                         b in zip(role_reaction, role_name))
        embed = discord.Embed(
            title="対応した役職を付与します",
            description=desc + "\n(※ 🗑️ : 自動で付与/剥奪できる役職全てを剥奪します )")  # noqa : E501
        for roles in self.role["roles"]:
            values = '\n- #'.join(roles['subChannel_name'])
            embed.add_field(
                name=f"[{roles['reaction']} : {roles['role_name']}]",
                value=f"- #{values}",
                inline=True)
        self.message = await self.channel.send(embed=embed)
        self.message_id = self.message.id

        for roles in self.role["roles"]:
            await self.message.add_reaction(roles["reaction"])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # BOTとのDMのリアクションの場合payload.memberの値がNoneになってしまうため
        # reaction_remove同様にreaction_addでもfetch_memberでmenberオブジェクトを取得する
        # fetch_userを使わない理由はUserオブジェクトだと「add_roles」ができないため
        member = await self.GUILD.fetch_member(payload.user_id)
        if member.bot:
            return
        if payload.message_id == self.message_id:
            await self.wastebasket(payload, self.channel)
            for roles in self.role["roles"]:
                await self.Add_Reaction(payload,
                                        member,
                                        roles["reaction"],
                                        roles["roles_id"])
            await self.send_message("add", payload, member, self.channel)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        member = await self.GUILD.fetch_member(payload.user_id)
        if member.bot:
            return
        if payload.message_id == self.message_id:
            message = await self.GUILD.get_channel(
                self.channel_id).fetch_message(self.message_id)
            reactions = message.reactions
            for reaction in reactions:
                if str(reaction) == "🗑️":
                    break
            else:
                for roles in self.role["roles"]:
                    await self.Remove_Reaction(payload,
                                               member,
                                               roles["reaction"],
                                               roles["roles_id"])
                await self.send_message("remove",
                                        payload,
                                        member,
                                        self.channel)

    async def Add_Reaction(self, payload, member, reaction, *args):
        if str(payload.emoji) == reaction:
            await VoiceJoin_Role(self.bot).AddRole(member, self.GUILD,  *args)

    async def Remove_Reaction(self, payload, member, reaction, *args):
        if str(payload.emoji) == reaction:
            await VoiceJoin_Role(self.bot).RemoveRole(member, self.GUILD, *args)  # noqa : E501

    async def send_message(self, mode, payload, member, channel):
        if mode == "add":
            text1 = "に"
            text2 = "を付与しました"
        elif mode == "remove":
            text1 = "から"
            text2 = "をはく奪しました"
        for roles in self.role["roles"]:
            if str(payload.emoji) == roles["reaction"]:
                msg = await channel.send(f"{member.name}{text1}役職[ {roles['role_name']} ]{text2}")  # noqa : E501
                await self.time_sleep(5, msg)

    async def time_sleep(self, second, msg):
        await asyncio.sleep(second)
        await msg.delete()

    async def wastebasket(self, payload, channel):
        if str(payload.emoji) == "🗑️":
            for roles in self.role["roles"]:
                await self.Remove_Reaction(payload,
                                           payload.member,
                                           "🗑️",
                                           roles["roles_id"])
                await self.message.remove_reaction(roles["reaction"],
                                                   payload.member)
            msg = await channel.send("全てのロールをはく奪しました")
            await self.message.remove_reaction("🗑️", payload.member)
            await self.time_sleep(5, msg)


def setup(bot):
    return bot.add_cog(Reaction_AddRole(bot))
