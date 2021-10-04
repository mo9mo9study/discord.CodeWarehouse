from discord.ext import commands
import discord


class TimesnameUpdate(commands.Cog):

    def self(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488
        self.CHANNEL_ID = 894577054262116426

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(self.GUILD_ID)
        self.channel = self.guild.get_channel(self.CHANNEL_ID)
        # await self.channel.purge()
        embed = discord.Embed(title="あなたのtimesのチャンネル名を更新します",
                              description="- discord名(ニックネーム)を変更した人などは活用してみてね")
        embed.add_field(name=" 👇 使い方", value="（超簡単）このメッセージにリアクションをするだけ‼️ ")
        self.message = await self.channel.send(embed=embed)
        self.message_id = self.message.id
        await self.message.add_reaction("🛎️")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # BOTとのDMのリアクションの場合payload.memberの値がNoneになってしまうため
        # reaction_remove同様にreaction_addでもfetch_memberでmenberオブジェクトを取得する
        # discord.Userではnickの属性がないのでdiscord.Memberを取得する
        # discord.Member.display_nameはニックネームNoneならアカウント名が適用される
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        member = await self.GUILD.fetch_member(payload.user_id)
        if member.bot:
            return
        if payload.message_id == self.message_id:
            member_id = payload.member.id
            select_msg = await self.channel.fetch_message(payload.message_id)
            for times_channel in self.GUILD.text_channels:
                if times_channel.topic == str(member_id):
                    before_name = times_channel.name
                    fix_name = f"times_{member.display_name}"
                    await times_channel.edit(name=fix_name)
                    after_name = times_channel.name
                    await select_msg.remove_reaction(payload.emoji, member)
                    if before_name != after_name:
                        embed = discord.Embed(title="あなたのtimesのチャンネル名を変更しました",
                                              description=member.mention)
                        embed.add_field(name="変更前のチャンネル名",
                                        value=before_name)
                        embed.add_field(name="変更後のチャンネル名",
                                        value=after_name)
                        await times_channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="変更前と変更後の名前に差分がありませんでした",
                                              description=f"{member.mention} チャンネル名を変更しませんでした")  # noqa #501
                        await times_channel.send(embed=embed)
                    break


def setup(bot):
    return bot.add_cog(TimesnameUpdate(bot))
