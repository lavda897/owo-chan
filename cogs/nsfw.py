import asyncio
import datetime
import random

import discord
import requests
import rule34
from discord.ext import commands, tasks

from variables import (neko_base_url, neko_img, neko_possible,
                       non_nsfw_channel, over_limit, post_limit)


class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def neko(self, ctx, limit=1):
        """SFW neko, wonder why this is in NSFW"""
        if limit > post_limit[0]['post_limit']:
            await ctx.send(over_limit)
        else:
            i=1
            while i <= limit:
                r = requests.get(neko_base_url + 'neko')
                data = r.json()
                neko = data['neko']
                embed = discord.Embed(
                    title = 'v(=^･ω･^=)v',
                    color = random.randint(0, 0xffffff)
                )
                embed.set_footer(text='{} | Thanks to nekos.life'.format(ctx.author))
                embed.set_image(url=neko)

                await ctx.send(embed=embed)
                i +=1

    @commands.command()
    async def lneko(self, ctx, limit=1):
        """Lewd OwO"""
        if ctx.channel.is_nsfw():
            if limit > post_limit[0]['post_limit']:
                await ctx.send(over_limit)
            else:
                i=1
                while i <= limit:
                    r = requests.get(neko_base_url + 'lewd/neko')
                    data = r.json()
                    neko = data['neko']
                    embed = discord.Embed(
                        title = 'Lewd OwO',
                        color = random.randint(0, 0xffffff)
                    )
                    embed.set_footer(text='{} | Thanks to nekos.life'.format(ctx.author))
                    embed.set_image(url=neko)

                    await ctx.send(embed=embed)
                    i +=1
        else:
            await ctx.send(non_nsfw_channel)

    @commands.command()
    async def rneko(self, ctx, limit=1):
        """Random Lewd OwO"""
        if ctx.channel.is_nsfw():
            if limit > post_limit[0]['post_limit']:
                await ctx.send(over_limit)
            else:
                i=1
                while i <= limit:
                    r = requests.get(neko_base_url + neko_img + random.choice(neko_possible))
                    data = r.json()
                    neko = data['url']
                    embed = discord.Embed(
                        title = '(^人^)',
                        color = random.randint(0, 0xffffff)
                    )
                    embed.set_footer(text='{} | Thanks to nekos.life'.format(ctx.author))
                    embed.set_image(url=neko)

                    await ctx.send(embed=embed)
                    i +=1
        else:
            await ctx.send(non_nsfw_channel)

    @commands.command()
    async def hentai(self, ctx, limit=1):
        """Hentai"""
        if ctx.channel.is_nsfw():
            if limit > post_limit[0]['post_limit']:
                await ctx.send(over_limit)
            else:
                i=1
                while i <= limit:
                    r = requests.get(neko_base_url + neko_img + 'hentai')
                    data = r.json()
                    neko = data['url']
                    embed = discord.Embed(
                        title = 'Hentai!',
                        color = random.randint(0, 0xffffff)
                    )
                    embed.set_footer(text='{} | Thanks to nekos.life'.format(ctx.author))
                    embed.set_image(url=neko)

                    await ctx.send(embed=embed)
                    i +=1
        else:
            await ctx.send(non_nsfw_channel)

    @commands.command()
    async def hentaigif(self, ctx, limit=1):
        """Hentai GIF"""
        if ctx.channel.is_nsfw():
            if limit > post_limit[0]['post_limit']:
                await ctx.send(over_limit)
            else:
                i=1
                while i <= limit:
                    r = requests.get(neko_base_url + neko_img + 'Random_hentai_gif')
                    data = r.json()
                    neko = data['url']
                    embed = discord.Embed(
                        title = 'Hentai GIF',
                        color = random.randint(0, 0xffffff)
                    )
                    embed.set_footer(text='{} | Thanks to nekos.life'.format(ctx.author))
                    embed.set_image(url=neko)

                    await ctx.send(embed=embed)
                    i +=1
        else:
            await ctx.send(non_nsfw_channel)

    @commands.command()
    async def traps(self, ctx, limit=1):
        """Delicious Traps"""
        if ctx.channel.is_nsfw():
            if limit > post_limit[0]['post_limit']:
                await ctx.send(over_limit)
            else:
                i=1
                while i <= limit:
                    r = requests.get(neko_base_url + neko_img + 'trap')
                    data = r.json()
                    neko = data['url']
                    embed = discord.Embed(
                        title = '#NoHomo',
                        color = random.randint(0, 0xffffff)
                    )
                    embed.set_footer(text='{} | Thanks to nekos.life'.format(ctx.author))
                    embed.set_image(url=neko)

                    await ctx.send(embed=embed)
                    i +=1
        else:
            await ctx.send(non_nsfw_channel)
    
    @commands.command()
    async def futa(self, ctx, limit=1):
        """Chicks with Dicks"""
        if ctx.channel.is_nsfw():
            if limit > post_limit[0]['post_limit']:
                await ctx.send(over_limit)
            else:
                i=1
                while i <= limit:
                    r = requests.get(neko_base_url + neko_img + 'futanari')
                    data = r.json()
                    neko = data['url']
                    embed = discord.Embed(
                        title = 'Chicks with Dicks',
                        color = random.randint(0, 0xffffff)
                    )
                    embed.set_footer(text='{} | Thanks to nekos.life'.format(ctx.author))
                    embed.set_image(url=neko)

                    await ctx.send(embed=embed)
                    i +=1
        else:
            await ctx.send(non_nsfw_channel)

    @commands.command()
    async def r34(self, ctx, tags:str, limit=1):
        """Rule34
        
        Example tags : "gay furry"
        """
        if ctx.channel.is_nsfw():
            if limit > post_limit[0]['post_limit']:
                await ctx.send(over_limit)
            else:
                loop = asyncio.get_event_loop()
                Rule34 = rule34.Rule34(loop)
                totalImages = await Rule34.totalImages(tags)
                if totalImages > 0:
                    if limit > totalImages:
                        ctx.send("Only {} images found".format(totalImages))
                    images = await Rule34.getImages(tags)
                    images = images[:limit]
                    for image in images:
                        embed = discord.Embed(
                            title = tags,
                            #url = 'https://rule34.xxx/index.php?page=post&s=view&id=' + image.id, #wanted to give image source but can't because of damn library
                            color = random.randint(0, 0xffffff)
                        )
                        embed.set_footer(text='{}'.format(ctx.author))
                        embed.set_image(url=image.file_url)
                        embed.timestamp = datetime.datetime.utcnow()

                        await ctx.send(embed=embed)
                else:
                    await ctx.send("> No images found")
        else:
            await ctx.send(non_nsfw_channel)

def setup(bot):
    bot.add_cog(NSFW(bot))
