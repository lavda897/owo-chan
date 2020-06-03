import os
import platform
import sys
import traceback

import discord
import pymongo
from discord.ext import commands
from dotenv import load_dotenv

from database import db
from variables import BOT_PREFIX, loaded_extensions

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

description = "OwO-Chan"
bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True, description=description)

col = db["selfconfig"]

try:
    activity = col.find_one({"_name": "activity"}, {"_id": 0, "_name": 0})
except:
    activity = {"type": 0, "name": "(⁎˃ᆺ˂) | OwO help"}

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('Discord Python Version:')
    print(discord.__version__)
    print('------')
    print('Python Version:')
    print(platform.python_version())
    print('------')
    await bot.change_presence(activity=discord.Activity(type=activity['type'], name=activity['name'])) #unknown = -1 playing = 0 streaming = 1 listening = 2 watching = 3 

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('> Missing required argument')
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send('> This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.author.send('> Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        original = error.original
        if not isinstance(original, discord.HTTPException):
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(original.__traceback__)
            print(f'{original.__class__.__name__}: {original}', file=sys.stderr)
    elif isinstance(error, commands.ArgumentParsingError):
        await ctx.send(error)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        loaded_extensions.append(filename[:-3])

bot.run(TOKEN)
