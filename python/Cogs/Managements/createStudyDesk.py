from discord.ext import commands
import discord
import asyncio

class CreateStudyDesk(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.GUILD_ID = 603582455756095488
        self.CATEGORY_ID = 603582455756095491

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD = self.bot.get_guild(self.GUILD_ID)
        self.CATEGORY = self.GUILD.get_channel(self.CATEGORY_ID)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        count = 0
        if after.channel is not None:
        #if after.channel is not (id_):
            vc_list = list(filter(lambda channel: channel.name[0:7] == "もくもく勉強机", self.GUILD.voice_channels))
            for channel in vc_list:
                members = channel.members
                count += len(members)
            if len(vc_list) - count == 1:
                channel = await self.CATEGORY.create_voice_channel(name=f"もくもく勉強机{str(len(vc_list) + 1)}")
                vc_count = len(self.CATEGORY.voice_channels)
                pos = vc_count - 4
                await channel.edit(position=pos)

def setup(bot):
    return bot.add_cog(CreateStudyDesk(bot))