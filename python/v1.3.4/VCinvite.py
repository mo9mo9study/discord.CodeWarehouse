# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio
import setting 

prefix = "¥"

TOKEN = setting.mToken
bot = commands.Bot(command_prefix=prefix,help_command=None)

@bot.event
async def on_ready():
    print('--------------------')
    print('起動中...')
    print('BOT NAME : ' + bot.user.name)
    print('BOT ID : ' + str(bot.user.id))
    print('--------------------')

@bot.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji) == "⛔":
        channel = payload.member.guild.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        if msg.content[0:3] == "¥vc" and msg.content[-19:-1].isdecimal():
            try:
                member = payload.member.guild.get_member(int(msg.content[-19:-1] ))
            except:
                pass
            else:
                dm = await member.create_dm()
                messages = await dm.history(limit=50).flatten()
                for i in messages:
                    if "https://discord.gg/" in i.content:
                        await i.delete()
                        await msg.delete()
                        break


@bot.command()
async def vc(ctx,mention):
    server = ctx.author.guild
    status = ctx.author.voice
    member_id = mention[-19:-1]
    if status is not None:
        try:
            member = server.get_member(int(member_id))
        except:
            await ctx.send("`¥vc {Mention}`と入力してください。")
        else:
            if status.channel.user_limit != 1:
                try:
                    member_channel_id = member.voice.channel.id
                except:
                    dm = await member.create_dm()
                    url = await status.channel.create_invite(max_age=30 * 60, max_uses=1, reason=f"{ctx.author.name}が{member.name}を{status.channel.name}に招待しました")
                    await dm.send(f"{ctx.author.name}が{status.channel.name}に招待しました\n{url}")
                else:
                    if member_channel_id != status.channel.id:
                        dm = await member.create_dm()
                        url = await status.channel.create_invite(max_age=30*60,max_uses=1,reason=f"{ctx.author.name}が{member.name}を{status.channel.name}に招待しました")
                        await dm.send(f"{ctx.author.name}が{status.channel.name}に招待しました\n{url}")
            else:
                await ctx.send("vcが満員なため、招待出来ませんでした。")
    else:
        await ctx.send("vcに参加してから実行してください")

bot.run(TOKEN)