import os

import discord
from discord.ext import commands

from database import db
from variables import loaded_extensions, post_limit

col = db["selfconfig"]

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def setstatus(self, ctx, activity:int, *, status:str):
        """Change bot status
        unknown = -1 playing = 0 streaming = 1 listening = 2 watching = 3
        """

        try:
            col.update_one({"_name": "activity"}, {"$set": { "type": activity, "name": status }})
        except:
            await ctx.send("Failed to update entries in database.")

        await self.bot.change_presence(activity=discord.Activity(type=activity, name=status))
        await ctx.send("Successfully changed bot presence.")

    @commands.command()
    async def setpostlimit(self, ctx, limit:int):
        """Update global post limit"""

        try:
            col.update_one({"_name": "limits"}, {"$set": { "post_limit": limit}})
            post_limit.remove(post_limit[0])
            post_limit.append({"post_limit": limit})
            await ctx.send("Successfully changed post limit to {}".format(post_limit[0]['post_limit']))
        except:
            await ctx.send("Failed to update entries in database.")

    @commands.command()
    async def postlimit(self, ctx):
        "Show post limit"

        await ctx.send("Post limit: {}".format(post_limit[0]['post_limit']))

    @commands.command()
    async def load(self, ctx, module:str):
        """Load a cog located in /cogs"""

        try:
            self.bot.load_extension("cogs.{}".format(module))
            print('{} loaded module: {}'.format(ctx.author, module))
            loaded_extensions.append(module)
            await ctx.send("Successfully loaded {}.py".format(module))

        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('{} attempted to load module \'{}\' but the following '
                        'exception occured;\n\t->{}'.format(ctx.author, module, exc))
            await ctx.send('Failed to load extension {}\n\t->{}'.format(module, exc))

    @commands.command()
    async def unload(self, ctx, module: str):
        """Unload any loaded cog"""

        try:
            self.bot.unload_extension("cogs.{}".format(module))
            print('{} unloaded module: {}'.format(ctx.author, module))
            loaded_extensions.remove(module)
            await ctx.send("Successfully unloaded {}.py".format(module))

        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await ctx.send('Failed to load extension {}\n\t->{}'.format(module, exc))

    @commands.command()
    async def loaded(self, ctx):
        """List loaded cogs"""
        string = ""
        for cog in loaded_extensions:
            string += str(cog) + "\n"

        await ctx.send('Currently loaded extensions:\n```{}```'.format(string))

    @commands.command()
    async def shutdown(self, ctx):
        """Shut down the bot"""

        try:
            await ctx.send("> Shutting down...")
            await self.bot.logout()
            self.bot.loop.stop()
            print('{} has shut down the bot...'.format(ctx.author))

        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('{} has attempted to shut down the bot, but the following '
                        'exception occurred;\n\t->{}'.format(ctx.author, exc))

    @commands.command()
    async def restart(self, ctx):
        """Restart the bot"""

        try:
            await ctx.send("Restarting...")
            await self.bot.logout()
            self.bot.loop.stop()
            print('{} has restarted the bot...'.format(ctx.author))
            os.system('sh ../restart.sh')

        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('{} has attempted to restart the bot, but the following '
                        'exception occurred;\n\t->{}'.format(ctx.author, exc))

def setup(bot):
    bot.add_cog(Owner(bot))
