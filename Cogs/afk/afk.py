from discord.ext import commands
import discord
import asyncio

class AFK(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.guild_id = 603582455756095488
        self.channel_id = 778975759669788702

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        if before.channel is None:
            await member.edit(mute=False)

    @commands.command()
    async def mmv(self,ctx, mention):
        server = self.bot.get_guild(self.guild_id)
        status = ctx.author.voice
        member_id = mention[-19:-1]
        try:
            member = server.get_member(int(member_id))
        except:
            await ctx.send("`¥mmv {Mention}`と入力してください。")
        else:
            if status is not None and member.voice is not None:
                channel = status.channel
                mention_channel = member.voice.channel
                if channel.id == mention_channel.id:
                    if member.voice.self_mute:
                        await ctx.send("対象のユーザーがミュートなので実行されませんでした。")
                        return
                    else:
                        afk_channel = server.get_channel(self.channel_id)
                        await member.move_to(afk_channel)
                        await member.edit(mute=True)
                        for times_channel in server.text_channels:
                            if times_channel.topic == str(member_id):
                                await times_channel.send(f"{mention} 寝落ちされていたようなので、ミュート＆移動しました。")
                                print(f"[ {member.name} ]をAFKチャンネルに移動しました")
                                break
                        else:
                            await ctx.send(f"[ {member.name} ]のtimesチャンネルが見つかりませんでした。")
                else:
                    await ctx.send(f"[ {member.name} ]と同じvcチャンネルに参加してください。")
            else:
                await ctx.send("vcに参加してください。")

def setup(bot):
    return bot.add_cog(AFK(bot))