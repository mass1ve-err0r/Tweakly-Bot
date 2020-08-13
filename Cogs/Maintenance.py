from os import environ as env
from discord.ext import commands


class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.maintainer = int(env.get('MAINTAINER_ID'))

    @commands.command(name='ping')
    async def ping(self, ctx):
        if ctx.author.id != self.maintainer:
            return

        await ctx.send('pong! (Heartbeat: {0} seconds)'.format(round(self.bot.latency, 1)))


def setup(bot):
    bot.add_cog(Maintenance(bot))
