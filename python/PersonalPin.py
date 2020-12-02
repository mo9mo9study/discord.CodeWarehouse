# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio

import setting

prefix = "¥"

TOKEN = setting.dToken
bot = commands.Bot(command_prefix=prefix,help_command=None)

bot.load_extension("Cogs.default")

@bot.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji) == "📌":
        for channel in payload.member.guild.text_channels:
            if str(payload.member.id) == channel.topic:
                ChannelID = payload.channel_id
                MessageID = payload.message_id
                message = await bot.get_channel(ChannelID).fetch_message(MessageID)
                if channel.id == ChannelID:
                    await message.pin()
                    break
                else:
                    embed = discord.Embed(color=0x80ff00)
                    embed.add_field(name=WordCount(message.content),value=f"[URL](https://discord.com/channels/{payload.member.guild.id}/{ChannelID}/{MessageID})")
                    msg = await channel.send(embed=embed)
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
                    message = await bot.get_channel(ChannelID).fetch_message(MessageID)
                    await message.unpin()
                else:
                    await channel.send("自分のチャンネルでのみ、ピンを外すことができます。")

def WordCount(message):
    if len(message) < 31:
        return message
    else:
        return message[:30] + "..."

bot.run(TOKEN)
