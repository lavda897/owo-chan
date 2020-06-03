import asyncio
import copy
import random

import discord
from discord.ext import commands

import core.konachan.konachan as konachan
import core.r34.rule34 as rule34
from core.utils.r34dbPost import Rule34dbPost
from database import db

r34 = rule34.Rule34()
konachan = konachan.Konachan()

col = db["autopost"]
colr34 = db['r34posts']
colKonachan = db['konachanPosts']

class Autopost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bg_task = self.bot.loop.create_task(self.auto_r34())
        self.bg_task = self.bot.loop.create_task(self.auto_konachan())

        self.load = True

    async def auto_r34(self):
        await self.bot.wait_until_ready()
        r34old_posts = []
        while self.load:

            if r34old_posts == []:
                try:
                    r34tempPosts = colr34.find({}, {"_id": 0})
                except:
                    print("Failed to fetch posts from database.")
                    break

                for post in r34tempPosts:
                    image = Rule34dbPost()
                    image.parse(post)
                    r34old_posts.append(image)
            
            try:
                r34fetched_channels = col.find({"type": "rule34"}, {"_id": 0, "guild_id": 0})
            except:
                print("Failed to fetch channels id from database.")
                break

            r34new_posts = r34.getPosts(limit=42)

            r34unique_posts = r34.findNew(r34old_posts, r34new_posts)

            r34old_posts = copy.deepcopy(r34new_posts)

            for post in r34unique_posts:
                embed = discord.Embed(
                    title = 'Rule34.xxx - ' + str(post.id),
                    url = 'https://rule34.xxx/index.php?page=post&s=view&id=' + str(post.id),
                    color = random.randint(0, 0xffffff)
                )
                embed.set_footer(text=post.source)
                embed.set_image(url=post.file_url)

                r34_channels_to_send = copy.deepcopy(r34fetched_channels)

                for channel_id in r34_channels_to_send:
                    channel = self.bot.get_channel(channel_id['channel_id'])
                    await channel.send(embed=embed)

            db_posts = []
            for post in r34new_posts:
                db_posts.append({"id": post.id})

            colr34.drop()
            colr34.insert_many(db_posts)

            await asyncio.sleep(90)

    async def auto_konachan(self):
        await self.bot.wait_until_ready()
        konachan_old_posts = []
        while self.load:

            if konachan_old_posts == []:
                try:
                    konachan_tempPosts = colr34.find({}, {"_id": 0})
                except:
                    print("Failed to fetch posts from database.")
                    break

                for post in konachan_tempPosts:
                    image = Rule34dbPost() # well both have same object type
                    image.parse(post)
                    konachan_old_posts.append(image)
            
            try:
                konachan_fetched_channels = col.find({"type": "konachan"}, {"_id": 0, "guild_id": 0})
            except:
                print("Failed to fetch channels id from database.")
                break

            konachan_new_posts = konachan.getPosts(limit=21)

            konachan_unique_posts = konachan.findNew(konachan_old_posts, konachan_new_posts)

            konachan_old_posts = copy.deepcopy(konachan_new_posts)

            for post in konachan_unique_posts:
                embed = discord.Embed(
                    title = 'Konachan.com - ' + str(post.id),
                    url = 'https://konachan.com/post/show/' + str(post.id),
                    color = random.randint(0, 0xffffff)
                )
                embed.set_footer(text=post.source)
                embed.set_image(url=post.file_url)

                konachan_channels_to_send = copy.deepcopy(konachan_fetched_channels)

                for channel_id in konachan_channels_to_send:
                    channel = self.bot.get_channel(channel_id['channel_id'])
                    await channel.send(embed=embed)

            db_posts = []
            for post in konachan_new_posts:
                db_posts.append({"id": post.id})

            colKonachan.drop()
            colKonachan.insert_many(db_posts)

            await asyncio.sleep(180)

    @commands.has_permissions(manage_messages=True)
    @commands.group()
    async def autopost(self, ctx):
        """Get info about autopost subcommands"""

        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title = 'OwO autopost',
                description = 'Set up autopost to the current channel',
                color = random.randint(0, 0xffffff)
            )
            embed.add_field(name='Usage:', value='`OwO autopost <subcommand>`', inline=False)
            embed.add_field(name='Subcommands', value='r34\nkonachan')

            await ctx.send(embed=embed)

    @autopost.command()
    async def r34(self, ctx):
        """Enable/disable rule34 autopost to this channel"""

        try:
            autopostexists = col.find_one({"type": "rule34", "channel_id": ctx.channel.id, "guild_id": ctx.guild.id})
        except:
            await ctx.send("Failed to fetch queries from database.")
            return
        
        if(autopostexists):
            try:
                col.delete_one({"type": "rule34", "channel_id": ctx.channel.id, "guild_id": ctx.guild.id})
                await ctx.send("Rule34 autopost has been removed from this channel.")
            except:
                await ctx.send("Failed to update queries in database.")
        else:
            if ctx.channel.is_nsfw():
                try:
                    col.insert_one({"type": "rule34", "channel_id": ctx.channel.id, "guild_id": ctx.guild.id})
                    await ctx.send("Rule34 autopost has been added to this channel.")
                except:
                    await ctx.send("Failed to update queries in database.")
            
            else:
                await ctx.send("Can't post NSfW here, kids here eh")

    @autopost.command()
    async def konachan(self, ctx):
        """Enable/disable Konachan autopost to this channel"""

        try:
            autopostexists = col.find_one({"type": "konachan", "channel_id": ctx.channel.id, "guild_id": ctx.guild.id})
        except:
            await ctx.send("Failed to fetch queries from database.")
            return
        
        if(autopostexists):
            try:
                col.delete_one({"type": "konachan", "channel_id": ctx.channel.id, "guild_id": ctx.guild.id})
                await ctx.send("Konachan autopost has been removed from this channel.")
            except:
                await ctx.send("Failed to update queries in database.")
        else:
            if ctx.channel.is_nsfw():
                try:
                    col.insert_one({"type": "konachan", "channel_id": ctx.channel.id, "guild_id": ctx.guild.id})
                    await ctx.send("Konachan autopost has been added to this channel.")
                except:
                    await ctx.send("Failed to update queries in database.")
            
            else:
                await ctx.send("Can't post NSfW here, kids here eh")


def setup(bot):
    bot.add_cog(Autopost(bot))
