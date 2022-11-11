import os
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import is_owner

brief_close = "$command-prefix$close"
help_close = "closes the bot.\n\n$command-prefix$close"

class Owner(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Closes the Bot, Only owners can do it
	@commands.command(brief=brief_close, help=help_close)
	@is_owner()
	async def close(self, ctx):
		await ctx.channel.send(f"Goodbye for the meantime guys! BSCoE Class Support Bot is closing!")
		print(f"Class Support Bot is closing!")

		os._exit(1)

	#When a non-owner tries to execute a close command
	@close.error
	async def close_error(self, ctx, error):
		await ctx.channel.send(f"Only the owners are allowed to close me!")
		print(f"A non-owner tried to close me!")


def setup(bot):
	bot.add_cog(Owner(bot))