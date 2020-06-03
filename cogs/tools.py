import random

import discord
from discord.ext import commands


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(left + right)

    @commands.command()
    async def subtract(self, ctx, left: int, right: int):
        """Subtract two numbers together."""
        await ctx.send(left - right)

    @commands.command()
    async def multiply(self, ctx, left: int, right: int):
        """Multiply two numbers together."""
        await ctx.send(left * right)

    @commands.command()
    async def divide(self, ctx, left: int, right: int):
        """Divide two numbers together."""
        await ctx.send(left / right)

    @commands.command()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

def setup(bot):
    bot.add_cog(Tools(bot))
