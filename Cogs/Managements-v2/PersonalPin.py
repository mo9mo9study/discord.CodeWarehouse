#!!! このコードは discord.py 2.0 以降のバージョンで実行してください。 !!!

from discord.ext import commands
import discord


class PersonalPin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_join(self, thread):
        await thread.join()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) == "📌":
            for channel in payload.member.guild.text_channels:
                if str(payload.member.id) == channel.topic:
                    ChannelID = payload.channel_id
                    MessageID = payload.message_id
                    message = await self.bot.get_channel(ChannelID).fetch_message(MessageID)  # noqa: E501
                    if channel.id == ChannelID:
                        await message.pin()
                        break
                    else:
                        embed = discord.Embed(color=0x80ff00)
                        embed.add_field(
                            name=self.WordCount(message.content),  # noqa: E501
                            value=f"[URL](https://discord.com/channels/{payload.member.guild.id}/{ChannelID}/{MessageID})"  # noqa: E501
                        )
                        msg = await channel.send(embed=embed)
                        try:
                            await msg.pin()
                        except Exception:
                            await msg.send("pin数が上限に達しました。")
                        else:
                            await msg.pin()
                        break
            else:
                print(f"{payload.member.name}のtimesチャンネルがありません")

        elif str(payload.emoji) == "⛔":
            for channel in payload.member.guild.text_channels:
                if str(payload.member.id) == channel.topic:
                    ChannelID = payload.channel_id
                    MessageID = payload.message_id
                    if channel.id == ChannelID:
                        message = await self.bot.get_channel(ChannelID).fetch_message(MessageID)  # noqa: E501
                        await message.unpin()
                    else:
                        await channel.send("自分のチャンネルでのみ、ピンを外すことができます。")

    def WordCount(self, message):
        if len(message) < 51:
            return message
        else:
            return message[:50] + "..."


def setup(bot):
    return bot.add_cog(PersonalPin(bot))
