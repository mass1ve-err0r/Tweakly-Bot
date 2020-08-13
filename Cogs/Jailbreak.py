from os import environ as env
import aiohttp
from datetime import datetime
from discord import Embed, Colour
from discord.ext import commands
from disputils import BotEmbedPaginator


class Jailbreak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = env.get('API_URL')
        self.api_token = env.get('API_TOKEN')

    @commands.command(name="search", aliases=["s"])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def search_tweak(self, ctx, suggestion: str = None):
        dt = datetime.now()

        if suggestion is None:
            embedx0 = Embed(title="**Command Error**", colour=Colour(0xff6699), timestamp=dt)
            embedx0.set_footer(text="Prototype X1")
            embedx0.add_field(name="➡️ Error Message", value="You did _NOT_ a name to search for, aborting...", inline=False)
            await ctx.send(embed=embedx0)
            return

        baseURL = self.api_url + suggestion
        auth_str = "Bearer " + self.api_token
        r_hdr = {"Authorization": auth_str}
        async with aiohttp.ClientSession(headers=r_hdr) as session:
            async with session.get(baseURL) as r:
                if r.status != 200:
                    embedx1 = Embed(title="**API Error**", colour=Colour(0xff0066), timestamp=dt)
                    embedx1.set_footer(text="Prototype X1")
                    embedx1.add_field(name="➡️ Error Message",
                                      value="API call failed, please try again later or contact the bot administrator",
                                      inline=False)
                    await ctx.send(embed=embedx1)
                    return

                data = await r.json()
                if not data:
                    embedx2 = Embed(title="**Search Error**", colour=Colour(0xff9966), timestamp=dt)
                    embedx2.set_footer(text="Prototype X1")
                    embedx2.add_field(name="➡️ Error Message",
                                      value="Search yielded no result, try a shorter term or perhaps keyword?",
                                      inline=False)
                    await ctx.send(embed=embedx2)
                else:
                    embeds = []
                    for provider in data:
                        _matches = len(data[provider])
                        for idx, item in enumerate(data[provider]):
                            _t = f"({provider.title()}) Match #{idx+1} / {_matches}"
                            _embed = Embed(title=_t, colour=Colour(0x33cccc), timestamp=dt)
                            _embed.set_footer(text="Prototype X1")
                            _embed.add_field(name="➡️ Tweak Name", value=data[provider][idx]['Name'], inline=False)
                            _embed.add_field(name="➡️ Author", value=data[provider][idx]['Author'], inline=False)
                            _embed.add_field(name="➡️ Description", value=data[provider][idx]['Description'], inline=False)
                            _embed.add_field(name="➡️ Version", value=data[provider][idx]['Version'], inline=False)
                            _embed.add_field(name="➡️ Paid?", value="Yes" if data[provider][idx]['Paid'] else "No", inline=False)
                            _embed.add_field(name="➡️ Depiction Link", value=data[provider][idx]['Depiction'], inline=False)
                            embeds.append(_embed)
                    paginator = BotEmbedPaginator(ctx, embeds)
                    await paginator.run()
        return


def setup(bot):
    bot.add_cog(Jailbreak(bot))
