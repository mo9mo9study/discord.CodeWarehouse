from discord.ext import commands
import discord

import datetime


class DeletesMsg(commands.Cog):
    """
    To delete a message after trolls/vandalism has occurred.
    Since the message is deleted without confirmation with strong authority,
    the argument of the command is increased to make it difficult to execute.
    assumption:
        Delete message by user ID:
            Deletes vandalism messages left by one-sided users.
        Delete message by message ID:
            Deletes all messages corrupted by the bot command.
    command:
        # {prefix}{command_name} {target} {delete_true/false}
        ¥deletes_msginmemberid {message_id} {true/false}
        ¥deletes_msginword {message_word} {true/false}
    """

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488
        self.LOG_CHANNEL_ID = 801060150433153054

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.LOG_CHANNEL = self.GUILD.get_channel(self.LOG_CHANNEL_ID)

    def action_check(self, delete: bool):
        if delete:
            action = "削除"
        else:
            action = "検索"
        return action

    async def before_sendmsg(self, message, searchtarget, action):
        """
        Confirmation of processing start.
        """
        logmsg = f"[INFO] ギルド内で指定ワード({searchtarget})を含むメッセージ(24時間以内)の{action}を開始しました"  # noqa: E501
        await message.reply(logmsg)
        print(logmsg)

    async def after_sendmsg(self, message, searchtarget,
                            action, msg_count, delete):
        """
        Confirmation of the end of processing.
        """
        if delete:
            # send log channel
            logmsg = f"[INFO] 指定ワード({searchtarget})を含むメッセージ(24時間以内)を{msg_count}件{action}しました"  # noqa: E501
            await self.LOG_CHANNEL.send(logmsg)
        else:
            # send message reply
            logmsg = f"[INFO] 指定ワード({searchtarget})を含むメッセージ(24時間以内)を{msg_count}件{action}しました"  # noqa: E501
            await message.reply(logmsg)
        print(f"[DEBUG] 対象: {searchtarget}/メッセージ件数: {msg_count}件/ アクション: {action}")  # noqa: E501

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def deletes_msginword(self, ctx, delete_word: str, delete: bool):
        """
        Delete message by user ID:
            Deletes vandalism messages left by one-sided users.
        """
        action = self.action_check(delete)
        msg_count = 0
        aftertime = datetime.datetime.now() - datetime.timedelta(days=1)
        await self.before_sendmsg(ctx, delete_word, action)
        for channel in self.GUILD.text_channels:
            if isinstance(channel, discord.TextChannel):
                messages = await channel.history(
                    limit=100, after=aftertime).flatten()
                for message in messages:
                    if delete_word in message.content:
                        print(f"[DEBUG] ({message.channel.name}){message.content[:10]}")  # noqa: E501
                        if delete:
                            await message.delete()
                        msg_count += 1
        await self.after_sendmsg(ctx, delete_word, action, msg_count, delete)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def deletes_msginmemberid(self, ctx,
                                    delete_memberid: int, delete: bool):
        """
        Delete message by message ID:
            Deletes all messages corrupted by the bot command.
        """
        action = self.action_check(delete)
        msg_count = 0
        aftertime = datetime.datetime.now() - datetime.timedelta(days=1)
        await self.before_sendmsg(ctx, delete_memberid, action)
        for channel in self.GUILD.text_channels:
            if isinstance(channel, discord.TextChannel):
                messages = await channel.history(
                    limit=100, after=aftertime).flatten()
                for message in messages:
                    if delete_memberid == message.author.id:
                        if message.content:
                            debugmsg = f"[DEBUG] ({message.channel.name}){message.content[:10]}"  # noqa: E501
                        else:
                            debugmsg = f"[DEBUG] ({message.channel.name}){message.embeds[0].title}"  # noqa: E501
                        if delete:
                            await message.delete()
                        print(debugmsg)
                        msg_count += 1
        await self.after_sendmsg(ctx, delete_memberid,
                                 action, msg_count, delete)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        At the time of error when there is no argument.
        """
        print("[ERROR] {ctx.invoked_with}: {error}")


def setup(bot):
    return bot.add_cog(DeletesMsg(bot))
