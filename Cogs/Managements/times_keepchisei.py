import textwrap

from discord.ext import commands
import discord

from .view_TimesChannel import ViewTimesChannel


class TimesKeepChisei(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488
        self.CHANNEL_ID = 897075228935610378  # チャンネル[timeeでchiseiを飼う]
        self.CREATE_TIMES_ID = 872257840528646144  # チャンネル[timesを作成]
        self.LOG_CHANNEL_ID = 801060150433153054

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.CHANNEL = self.GUILD.get_channel(self.CHANNEL_ID)
        self.CREATE_TIMES = self.GUILD.get_channel(self.CREATE_TIMES_ID)
        self.LOG_CHANNEL = self.GUILD.get_channel(self.LOG_CHANNEL_ID)
        await self.CHANNEL.purge()
        embed = discord.Embed(title="自分のtimesに(bot)chiseiを呼びます",
                              description="- 許可するとchiseiからランダムでメッセージが届くことがあります")  # noqa #501
        embed.add_field(name=" 👇 使い方", value="（超簡単）このメッセージにリアクションをするだけ‼️ ")  # noqa #501
        self.message = await self.CHANNEL.send(embed=embed)
        self.message_id = self.message.id
        await self.message.add_reaction("🦎")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        member = await self.bot.fetch_user(payload.user_id)
        if member.bot:
            return
        if payload.message_id == self.message_id:
            member_id = member.id
            select_msg = await self.CHANNEL.fetch_message(payload.message_id)
            for times_channel in self.GUILD.text_channels:
                if times_channel.topic == str(member_id):
                    await self.channel_editpermission(times_channel,
                                                      True)
                    msg = f"{times_channel.mention}にchiseiを呼びました"
                    send_msg = await self.CHANNEL.send(msg)
                    await ViewTimesChannel(self.bot).time_sleep(send_msg)
                    log_msg = f"[INFO] {times_channel.mention}にロールchisei2からの送信権限をTrueに変更"  # noqa #501
                    await self.LOG_CHANNEL.send(log_msg)
                    break
            else:
                msg = await self.CHANNEL.send(textwrap.dedent(f"""\
                    timesチャンネルが見つかりませんでした。
                    {self.CREATE_TIMES.mention} でtimesを作成してください。"""))
                await self.time_sleep(msg)
                await select_msg.remove_reaction(payload.emoji, member)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        member = await self.bot.fetch_user(payload.user_id)
        print(member)
        if member.bot:
            return
        if payload.message_id == self.message_id:
            member_id = member.id
            select_msg = await self.CHANNEL.fetch_message(payload.message_id)  # noqa #841
            for times_channel in self.GUILD.text_channels:
                if times_channel.topic == str(member_id):
                    await self.channel_editpermission(times_channel,
                                                      None)
                    msg = f"{times_channel.mention}からchiseiを追い出しました"
                    send_msg = await self.CHANNEL.send(msg)
                    await ViewTimesChannel(self.bot).time_sleep(send_msg)
                    log_msg = f"[INFO] {times_channel.mention}にロールchisei2からの送信権限をNoneに変更"  # noqa #501
                    await self.LOG_CHANNEL.send(log_msg)
                    break

    async def channel_editpermission(self, times_channel, per_bool):
        chisei2_role = discord.utils.get(self.GUILD.roles, name="chisei2")
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = per_bool
        await times_channel.set_permissions(chisei2_role, overwrite=overwrite)


def setup(bot):
    return bot.add_cog(TimesKeepChisei(bot))
