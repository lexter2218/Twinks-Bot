import os
import discord
from discord.ext import commands
from discord.ext.commands import is_owner

import Twinks

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["exit", "kill", "terminate"])
    @is_owner()
    async def close(self, ctx):
        await Twinks.Appearance(self.bot).Set(status=discord.Status.offline, activity="")
        await ctx.channel.send(f"Goodbye for the meantime guys! {self.bot.user} is closing!")
        print(f"{self.bot.user} is closing!")

        os._exit(1)

    @close.error
    async def close_error(self, error, ctx):
        await ctx.channel.send(f"Only the owners are allowed to close me!")
        print(f"A non-owner ({ctx.author}) tried to close me!")


async def setup(bot):
    await bot.add_cog(Owner(bot))