from discord.ext import commands,tasks
import discord
import asyncio
import yaml

import types

class LanguageVisualization(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488
        self.CHANNEL_ID = 809322291813023784
        self.embettitle = "勉強中 or 習得済み言語がある場合は、リアクションを押して登録しましょう！"

    @commands.Cog.listener()
    async def on_ready(self):
        #with open('Settings/language.yaml',encoding="utf-8") as file:
        #    self.language = yaml.safe_load(file.read())
        self.readlanguageyaml()
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.CHANNEL = self.GUILD.get_channel(self.CHANNEL_ID)
        messages = await self.CHANNEL.history(limit=1).flatten()
        for message in messages: # py再起動時にこの処理で送信されたEmbedメッセージ削除
            if message.embeds:
                if self.embettitle in message.embeds[0].title:
                    await message.delete()

        language_name = map(lambda language_obj: language_obj["language_name"], self.language["languages"])
        language_emoji = map(lambda language_obj: language_obj["emoji"], self.language["languages"])
        desc = "\n".join(f"- {a} : {b}" for a, b in zip(language_emoji, language_name))
        embed = discord.Embed(title=self.embettitle, description=desc)
        embed = self.addembedlanguage(embed)
        embed.add_field(name="📝 活用方法",value="各言語ごとに役職を用意していて、もし言語についてわからないことがあれば「（例）@Python {聞きたい内容}」の様にメンションをすることで言語の権限を付与しているメンバーに通知が飛ぶようになっています。気軽に活用してみてくださいね", inline=False)
        embed.add_field(name="📁 全ての言語役職を一括で付与/剥奪する方法", value="「🗑」のリアクションを押してください", inline=True)
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

    def readlanguageyaml(self):
        with open('Settings/language.yaml',encoding="utf-8") as file:
            self.language = yaml.safe_load(file.read())


    def addembedlanguage(self, embed):
        # embedで使用するオブジェクトの作成
        language_names = []
        for i in self.language["languages"]:
            language_names.append({"language_name":i["language_name"],"emoji":i["emoji"]})
        # embedの作成と追加
        for language in language_names:
            language_role = discord.utils.get(self.GUILD.roles, name=language["language_name"])
            if language_role.members:
                desc = "\n".join("- " + member.name for member in language_role.members)
                embed.add_field(name=f'{language["emoji"]} {language["language_name"]}', value=desc, inline=True)
            else:
                embed.add_field(name=f'{language["emoji"]} {language["language_name"]}', value="none", inline=True)
        return embed

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def embedreset(self, ctx):
        messages = await self.CHANNEL.history(limit=1).flatten()
        for message in messages:
            if message.embeds:
                if self.embettitle in message.embeds[0].title:
                    embed = message.embeds[0]
                    embed.clear_fields()
                    embed = self.addembedlanguage(embed)
                    await message.edit(embed=embed)
                    break


    ## ---------------定期処理---------------
    ##午前2:00に実行されます
    #@tasks.loop(seconds=60)
    #async def loop(self):
    #    await self.bot.wait_until_ready()
    #    #now = datetime.now().strftime('%H:%M')
    #    #if now == "02:00":
    


def setup(bot):
    return bot.add_cog(LanguageVisualization(bot))
