import discord
from discord.ext import commands


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("https://discordapp.com/oauth2/authorize?permissions=60422&client_id=648870316931678208&scope=bot")


def setup(bot):
    bot.add_cog(Invite(bot))
