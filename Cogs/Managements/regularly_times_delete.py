import discord
from discord.ext import commands, tasks

from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class RegularlyTimesDelete(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488
        self.LOG_CHANNEL_ID = 801060150433153054
        self.RETENTIONPERIOD = 3

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.LOG_CHANNEL = self.GUILD.get_channel(self.LOG_CHANNEL_ID)
        self.regularly_times_delete.start()

    async def times_delete(self):
        deletetimes_count = 0
        dt_retentionperiod = datetime.now() \
            - relativedelta(months=self.RETENTIONPERIOD)
        print(f"[DEBUG] 総チャンネル数：{len(self.GUILD.text_channels)}")
        for times_channel in self.GUILD.text_channels:
            if times_channel.name[0:6] == "times_":
                times_lastmessage = await times_channel.history(limit=1).flatten()  # noqa: E501
                last_message = await times_channel.fetch_message(times_lastmessage[0].id)  # noqa: E501
                if dt_retentionperiod > last_message.created_at:
                    reason_msg = f"最終投稿日: {last_message.created_at}"
                    # 以下の処理がこのコードでメインとなる処理になる
                    # print(f"[DEBUG] ( {times_channel.name} ) {reason_msg}")
                    await times_channel.delete(reason=f"３ヶ月以上未使用のため({reason_msg})")  # noqa: E501
                    deletetimes_count += 1
        # botの実行ログをdiscordに送信する場合
        return deletetimes_count

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def admin_timesinfo(self, ctx):
        """timesの保持期間を表示"""
        dt_retentionperiod = datetime.now() \
            - relativedelta(months=self.RETENTIONPERIOD)
        embed = discord.Embed(title="現在のtimes保持期間は、",
                              description=f"{self.RETENTIONPERIOD}ヶ月 (最終投稿日:{dt_retentionperiod}以前削除)")  # noqa: E501
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def admin_timesdelete(self, ctx):
        """保持期間を過ぎたtimesの手動削除"""
        deletetimes_count = await self.times_delete()
        # ログの送信
        send_msg = f"[INFO] delete(schedule)times: {deletetimes_count}"
        await self.LOG_CHANNEL.send(send_msg)

    @tasks.loop(seconds=3600)
    async def regularly_times_delete(self):
        """
        毎時定期実行するトリガーで、深夜3時に実行される
        設定された保持期間を過ぎて使用されていないtimesチャンネルを削除する処理
        """
        await self.bot.wait_until_ready()  # Botが準備状態になるまで待機
        if date.today().weekday() != 0:  # 週一回の実行予定
            return
        if datetime.now().strftime('%H') == "03":
            deletetimes_count = await self.times_delete()
            # ログの送信
            send_msg = f"[INFO] delete(schedule)times: {deletetimes_count}"
            await self.LOG_CHANNEL.send(send_msg)


def setup(bot):
    return bot.add_cog(RegularlyTimesDelete(bot))
