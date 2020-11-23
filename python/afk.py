# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio

TOKEN = 'NzcyMzczMDQ5MzYxMDM5NDEy.X55udA.BAo3aX98kqK6CCEWMCnOqlVy7aw'
bot = commands.Bot(command_prefix="¥",help_command=None)

@bot.event
async def on_ready():
    print('--------------------')
    print('起動中...')
    print('BOT NAME : ' + bot.user.name)
    print('BOT ID : ' + str(bot.user.id))
    print('--------------------')

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None:
        await member.edit(mute=False)

@bot.command()
async def mmv(ctx, mention):
    server = bot.get_guild(603582455756095488)
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
                    afk_channel = server.get_channel(778975759669788702)
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

@bot.command()
async def m(ctx):
    await ctx.author.edit(mute=False)

bot.run(TOKEN)