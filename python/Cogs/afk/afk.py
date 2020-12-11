from discord.ext import commands
import discord
import asyncio

class AFK(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        if before.channel is None:
            await member.edit(mute=False)

    @commands.command()
    async def mmv(self,ctx, mention):
        server = self.bot.get_guild(770973096215707648)
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
                        afk_channel = server.get_channel(770973905312808991)
                        await member.move_to(afk_channel)
                        await member.edit(mute=True)
                        for channel in server.text_channels:
                            if channel.topic == str(member_id):
                                await channel.send(f"{mention} 寝落ちされていたようなので、ミュート＆移動しました。")
                                break
                        else:
                            await ctx.send('チャンネルが見つかりませんでした。')
                else:
                    await ctx.send("同じvcチャンネルに参加してください。")
            else:
                await ctx.send("vcに参加してください。")

def setup(bot):
    return bot.add_cog(AFK(bot))