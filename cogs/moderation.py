import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def clear(self, ctx, amount: int):
        """Clear recent messages"""
        amount=amount+1
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick member"""
        try:
            await member.kick(reason=reason)
        except:
            await ctx.send("Uuf, I can't kick that user eh")
        else:
            await ctx.send(f'Member {member.mention} has been kicked lmao\nReason : {reason}')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban member"""
        try:
            await member.ban(reason=reason)
        except:
            await ctx.send("Uuf, I can't ban that user eh")
        else:
            await ctx.send(f'Retard {member.mention} has been banned lol\nReason : {reason}')

    @commands.command()
    async def unban(self, ctx, *, member):
        """Unban banned member"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

def setup(bot):
    bot.add_cog(Moderation(bot))
