from discord.ext import commands,tasks
import discord
import asyncio
import yaml

class LanguageVisualization(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488
        self.CHANNEL_ID = 673006702924136448

    @commands.Cog.listener()
    async def on_ready(self):
        with open('Settings/language.yaml',encoding="utf-8") as file:
            self.language = yaml.safe_load(file.read())

        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.CHANNEL = self.GUILD.get_channel(self.CHANNEL_ID)
        messages = await self.CHANNEL.history(limit=1).flatten()
        for message in messages:
            await message.delete()

        language_name = map(lambda language_obj: language_obj["language_name"], self.language["languages"])
        language_emoji = map(lambda language_obj: language_obj["emoji"], self.language["languages"])
        desc = "\n".join(a + " : " + b for a, b in zip(language_emoji, language_name))
        embed = discord.Embed(title="勉強中 or 習得済み言語がある場合は、リアクションを押して登録しましょう！", description=desc + "\n(※ 🗑️ : 自動で付与/剥奪できる役職全てを剥奪します )")
        self.message = await self.CHANNEL.send(embed=embed)
        self.message_id = self.message.id

        for languages in self.language["languages"]:
            await self.message.add_reaction(languages["emoji"])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.guild_id == None:
            return
        if payload.member.bot:
            return
        if payload.message_id == self.message_id:
            await self.wastebasket(payload, self.CHANNEL)
            for languages in self.language["languages"]:
                await self.Add_Reaction(payload, languages["emoji"], languages["role_id"])
            await self.send_message("add",payload,payload.member, self.CHANNEL)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        if payload.guild_id == None:
            return
        member = self.GUILD.get_member(payload.user_id)
        if member.bot:
            return
        if payload.message_id == self.message_id:
            reactions = self.message.reactions
            if "🗑️" in reactions:
                return
            else:
                for languages in self.language["languages"]:
                    await self.Remove_Reaction(payload, member, languages["emoji"], languages["role_id"])
                await self.send_message("remove",payload,member, self.CHANNEL)

    async def Add_Reaction(self, payload, reaction, *args):
        if str(payload.emoji) == reaction:
            await self.AddRole(payload.member, *args)

    async def Remove_Reaction(self, payload, member, reaction, *args):
        if str(payload.emoji) == reaction:
            await self.RemoveRole(member, *args)

    async def AddRole(self,member,*args):
        for role_id in args:
            role = member.guild.get_role(role_id)
            await member.add_roles(role)

    async def RemoveRole(self,member,*args):
        for role_id in args:
            role = member.guild.get_role(role_id)
            await member.remove_roles(role)

    async def send_message(self, mode, payload, member, channel):
        if mode == "add":
            text1 = "に"
            text2 = "を付与しました"
        elif mode == "remove":
            text1 = "から"
            text2 = "をはく奪しました"
        for languages in self.language["languages"]:
            if str(payload.emoji) == languages["emoji"]:
                msg = await channel.send(f"{member.name}{text1}役職[ {languages['language_name']} ]{text2}")
                await self.time_sleep(5, msg)

    async def time_sleep(self,second,msg):
        await asyncio.sleep(second)
        await msg.delete()

    async def wastebasket(self,payload ,channel):
        if str(payload.emoji) == "🗑️":
            for languages in self.language["languages"]:
                await self.Remove_Reaction(payload, payload.member, "🗑️", languages["role_id"])
                await self.message.remove_reaction(languages["emoji"], payload.member)
            msg = await channel.send("全てのロールをはく奪しました")
            await self.message.remove_reaction("🗑️", payload.member)
            await self.time_sleep(5, msg)



def setup(bot):
    return bot.add_cog(LanguageVisualization(bot))
