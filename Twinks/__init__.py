import discord

# Send system channel a message
class System_Channel:
    def __init__(self, guild : discord.Guild, msg : str = ""):
        self.guild = guild
        self.msg = msg

    async def send(self):
        if self.msg.strip() == "": return

        await self.guild.system_channel.send(self.msg)

    async def greetings(self, target : any = None):
        if self.msg.strip() == "":
            if isinstance(target, (discord.User, discord.Member, discord.TextChannel, discord.VoiceChannel, discord.Role)):
                target = target.name
            else:
                target = self.guild.name
            
            self.msg = f"Good day, {target}!"
        await self.guild.system_channel.send(self.msg)

class Status:
    @property
    def On():
        return discord.Status.online

    @property
    def Off():
        return discord.Status.offline

    @property
    def idle():
        return discord.Status.idle

class Appearance:
    def __init__(self, bot : discord.ext.commands.Bot):
        self.bot = bot
        self._status = Status.Off
        self._activity = ""

    @property
    def status(self):
        return self._status

    @property
    def activity(self):
        return self._activity

    async def Set(self, **kwargs):
        for key, value in kwargs.items():
            if key.lower().strip() == ["status"]:
                self._status = value
            elif key.lower().strip() == ["activity"]:
                self._activity = value
        await self.bot.change_presence(status=self.status, activity=discord.Game(self.activity))