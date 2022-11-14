import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command Prefix Change



    # Bot leave
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        await ctx.guild.system_channel.send("Goodbye!")
        await ctx.guild.leave()



async def setup(bot):
    await bot.add_cog(Admin(bot))