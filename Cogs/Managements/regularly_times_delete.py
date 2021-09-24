import discord
from discord.ext import commands, tasks

from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class RegularlyTimesDelete(commands.Cog):

    def self(self, bot):
        self.bot = bot
        self.GUILD_ID = 0
        # botの実行ログをdiscordに送信する場合
        self.LOG_CHANNEL_ID = 0

    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.LOG_CHANNEL = self.bot.get_guild(self.LOG_CHANNEL_ID)

    # ちょっとおまけで作ったコマンド
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def admin_timesinfo(self, ctx):
        dt_retentionperiod = datetime.now() \
            - relativedelta(months=self.RETENTIONPERIOD)
        embed = discord.Embed(title="現在のtimes保持期間は、",
                              description=f"{self.RETENTIONPERIOD}ヶ月 (最終投稿日:{dt_retentionperiod}以前削除)")  # noqa: E501
        await ctx.reply(embed=embed)

    # 毎時定期実行するトリガーで、深夜3時に実行される
    # 設定された保持期間を過ぎて使用されていないtimesチャンネルを削除する処理

    @tasks.loop(seconds=3600)
    async def regularly_times_delete(self):
        await self.bot.wait_until_ready()  # Botが準備状態になるまで待機
        if date.today().weekday() != 0:  # 週一回の実行予定
            return
        if datetime.now().strftime('%H') == "03":
            count = 0
            dt_retentionperiod = datetime.now() \
                - relativedelta(months=self.RETENTIONPERIOD)
            print(len(self.GUILD.text_channels))
            for times_channel in self.GUILD.text_channels:
                if times_channel.name[0:6] == "times_":
                    times_lastmessage = await times_channel.history(limit=1).flatten()  # noqa: E501
                    last_message = await times_channel.fetch_message(times_lastmessage[0].id)  # noqa: E501
                    if dt_retentionperiod > last_message.created_at:
                        count += 1
                        print(f"[DEBUG] ( {times_channel.name} ) 最終投稿日: {last_message.created_at}")  # noqa: E501
            # send_msg = f"[INFO] done, delete(schedule)times: {count}"
            # botの実行ログをdiscordに送信する場合
            # await self.LOG_CHANNEL.channel.send(send_msg)


def setup(bot):
    return bot.add_cog(RegularlyTimesDelete(bot))
