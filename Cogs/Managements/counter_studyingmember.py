from discord.ext import commands, tasks


class CounterStudyingmember(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488
        self.COUNTER_STUDYING_CHANNEL_ID = 896540898026999808
        self.counter_studyingmembers.start()

    def count_member(self, channels):
        count_member = 0
        for channel in channels:
            if len(channel.members) == 0:
                continue
            for member in channel.members:
                if member.bot:
                    continue
                count_member += 1
        return count_member

    @tasks.loop(seconds=60)
    async def counter_studyingmembers(self):
        await self.bot.wait_until_ready()  # Botが準備状態になるまで待機
        GUILD = self.bot.get_guild(self.GUILD_ID)
        CHANNEL = self.bot.get_channel(self.COUNTER_STUDYING_CHANNEL_ID)
        before_name = CHANNEL.name
        counter_studyingmember = 0
        counter_studyingmember += self.count_member(GUILD.voice_channels)
        counter_studyingmember += self.count_member(GUILD.stage_channels)
        after_name = f"勉強中：{counter_studyingmember} users"
        print(f"[DEBUG] {counter_studyingmember} users")
        if before_name != after_name:
            await CHANNEL.edit(name=after_name)
            print(f"[INFO] 勉強中カウンター名を変更しました({before_name} → {after_name})")


def setup(bot):
    return bot.add_cog(CounterStudyingmember(bot))
