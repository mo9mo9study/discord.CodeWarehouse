# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio

TOKEN = 'NzcyMzczMDQ5MzYxMDM5NDEy.X55udA.dAfCLYnW_AmvSDkGfrZbeEC6peY'
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
    server = bot.get_guild(770973096215707648)
    status = ctx.author.voice
    member_id = mention[3:21]
    member = server.get_member(int(member_id))
    if status is not None and member.voice is not None:
        channel = status.channel
        mention_channel = member.voice.channel
        if channel.id == mention_channel.id:
            if channel.id == 683864874539024397 or channel.id == 603582455756095492 or channel.id == 685652747076632623 or channel.id == 777803355098710046:
                try:
                    member = server.get_member(int(member_id))
                except:
                    await ctx.send("`¥mmv {Mention}`と入力してください。")
                else:
                    if member.voice.self_mute:
                        await ctx.send("対象のユーザーがミュートなので実行されませんでした。")
                        return
                    else:
                        afk_channel = ctx.guild.get_channel(770973905312808991)
                        await member.move_to(afk_channel)
                        await member.edit(mute=True)
                        #channel = server.get_channel(778975668934672404)
                        #await channel.send(f"{mention} 寝落ちされていたようなので、ミュート＆移動しました。")
    else:
        await ctx.send("vcに参加してください。")

@bot.command()
async def m(ctx):
    await ctx.author.edit(mute=False)

@bot.command()
async def test(ctx, mention):
    member_id = mention[3:21]
    member = ctx.guild.get_member(int(member_id))
    await ctx.send(member.voice)

bot.run(TOKEN)