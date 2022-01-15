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
        embed = discord.Embed(title="自分のtimesでchisei(bot)を飼えます",
                              description="- きまぐれで今まで覚えた単語を使って返事をする子です。「知性」って呼んでみると...？！興味ある人は遊んでみてね")  # noqa #501
        embed.add_field(name="リアクションを押す",
                        value="- 自分のtimesでchiseiからのメッセージ送信を権限を許可すると、chiseiからきまぐれにでメッセージが届くようになります")  # noqa #501
        embed.add_field(name="リアクションを外す",
                        value="- もう一度リアクションを押すと、chiseiからメッセージが届かなくなります")  # noqa #501
        embed.add_field(name=" 👇 使い方",
                        value="（超簡単）このメッセージにリアクションをするだけ‼️ ",
                        inline=False)
        self.message = await self.CHANNEL.send(embed=embed)
        self.message_id = self.message.id
        await self.message.add_reaction("🦎")

    async def times_chisei2permission(self, payload, bool_per, msg_action):
        member = await self.bot.fetch_user(payload.user_id)
        if member.bot:
            return
        if payload.message_id == self.message_id:
            member_id = member.id
            select_msg = await self.CHANNEL.fetch_message(payload.message_id)
            for times_channel in self.GUILD.text_channels:
                if times_channel.topic == str(member_id):
                    await self.channel_editpermission(times_channel,
                                                      bool_per)
                    msg = f"{times_channel.mention}{msg_action}"
                    send_msg = await self.CHANNEL.send(msg)
                    log_msg = f"[INFO] {times_channel.mention}にロールchisei2からのメッセージ送信権限を{bool_per}に変更"  # noqa #501
                    await self.LOG_CHANNEL.send(log_msg)
                    break
            else:
                send_msg = await self.CHANNEL.send(textwrap.dedent(f"""\
                    timesチャンネルが見つかりませんでした。
                    {self.CREATE_TIMES.mention} でtimesを作成してください。"""))
                await select_msg.remove_reaction(payload.emoji, member)
            await ViewTimesChannel(self.bot).time_sleep(send_msg)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        bool_per = True
        msg_action = "でchisei(bot)を飼い始めました"
        await self.times_chisei2permission(payload, bool_per, msg_action)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        bool_per = None
        msg_action = "でchisei(bot)とさよならしました"
        await self.times_chisei2permission(payload, bool_per, msg_action)

    async def channel_editpermission(self, channel, per_bool):
        chisei2_role = discord.utils.get(self.GUILD.roles, name="chisei2")
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = per_bool
        await channel.set_permissions(chisei2_role, overwrite=overwrite)

    async def selectchannel_chisei2permission(self, ctx, arg, per_bool):
        print(f"[DEBUG] --{arg}/{len(str(arg))}--")
        print(f"[DEBUG] --{ctx.command.name}--")
        if len(arg) != 18:
            return
        edit_channel = self.GUILD.get_channel(int(arg))
        if edit_channel and isinstance(edit_channel, discord.TextChannel):
            await self.channel_editpermission(edit_channel, per_bool)
            log_msg = f"[INFO] {edit_channel.mention}にロールchisei2からの送信権限を{per_bool}に変更"  # noqa #501
            await self.LOG_CHANNEL.send(log_msg)
        else:
            err_msg = f"[ERROR] {ctx.command.name}: 引数( {arg} )からチャンネルを取得できませんでした"  # noqa #501
            await self.LOG_CHANNEL.send(err_msg)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def chisei_sendtrue(self, ctx, arg):
        await self.selectchannel_chisei2permission(ctx, arg, True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def chisei_sendnone(self, ctx, arg):
        await self.selectchannel_chisei2permission(ctx, arg, None)


def setup(bot):
    return bot.add_cog(TimesKeepChisei(bot))
