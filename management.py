from discord.ext import commands
import discord

import setting

intents = discord.Intents.all()
TOKEN = setting.dToken
# TOKEN = setting.tToken
prefix = "¥"

bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)

bot.load_extension("Cogs.default")

# 以下issueの検証により、Cogs.afk.afkが今回の問題を発生させているためコメントアウト
# https://github.com/mo9mo9study/discord.CodeWarehouse/issues/136
# bot.load_extension("Cogs.afk.afk")
bot.load_extension("Cogs.afk.unmute")
bot.load_extension("Cogs.Managements.voiceChannelJoinLeave_roleModify")
bot.load_extension("Cogs.Managements.rolesmanager")
bot.load_extension("Cogs.Managements.emoji")
bot.load_extension("Cogs.Managements.VCinvite")
bot.load_extension("Cogs.Managements.view_TimesChannel")
bot.load_extension("Cogs.Managements.selfIntroduction")
bot.load_extension("Cogs.Managements.createStudyDesk")
bot.load_extension("Cogs.Managements.memberOrganization")
bot.load_extension("Cogs.Managements.times")
bot.load_extension("Cogs.Managements.joinLeaveLog")
bot.load_extension("Cogs.Managements.slotstudyrecord")
bot.load_extension("Cogs.Managements.languageVisualization")
bot.load_extension("Cogs.Managements.membersinfo_dbreset")
bot.load_extension("Cogs.Managements.regularly_times_delete")
bot.load_extension("Cogs.Managements.timesname_update")
bot.load_extension("Cogs.Managements.counter_studyingmember")

bot.run(TOKEN)
