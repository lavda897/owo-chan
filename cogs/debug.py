import datetime
import os
import random
import time

import discord
import psutil
from discord.ext import commands

start_time = time.time()

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx):
        """Check bot latency ping to the discord server"""

        await ctx.send('Pong! {0}ms'.format(round(self.bot.latency * 1000)))

    @commands.command()
    async def uptime(self, ctx):
        """Says bot uptime"""
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=random.randint(0, 0xffffff))
        embed.add_field(name='Uptime', value=text)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send('Current uptime: ' + text)

    @commands.command()
    async def status(self, ctx):
        """Shows OwO-Chan status, ping, uptime, memory stats, and so on"""

        embed = discord.Embed(colour=random.randint(0, 0xffffff))
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name='Ping', value='{0}ms'.format(round(self.bot.latency * 1000)))

        current_time = time.time()
        difference = int(round(current_time - start_time))
        embed.add_field(name='Uptime', value=str(datetime.timedelta(seconds=difference)))

        memory_usage = self.process.memory_info().rss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        embed.add_field(name='Process', value=f'{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU')

        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Debug(bot))
