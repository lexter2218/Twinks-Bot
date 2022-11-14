from peewee import *

db = SqliteDatabase("data/twinks.db")
conn = False

def connector(func):
    def wrapper(*args):
        global conn
        if not conn:
            conn = True
            db.connect()
        result = func(*args)
        if conn:
            conn = False
            db.close()
        return result
    return wrapper

class BaseModel(Model):
    class Meta:
        database = db

class GuildInit(BaseModel):
    guild_id = IntegerField(unique=True)
    command_prefix = TextField() 


@connector
def setup():
    db.create_tables([GuildInit])

# Guild Init Model Fetcher
class GuildInitMF:
    def __init__(self):
        self.defaults = {
            "command_prefix" : "."
        }


    @connector
    def rowplace(self, fetched_guild_id : int):
        guild_data = GuildInit(guild_id=fetched_guild_id, command_prefix=self.defaults["command_prefix"])
        guild_data.save()

        return guild_data

    @connector
    def rowremove(self, fetched_guild_id : int):
        guild_data = GuildInit.get(GuildInit.guild_id == fetched_guild_id)
        guild_data.delete_instance()

        return guild_data

    @connector
    def rowfetch(self, fetched_guild_id : int):
        try:
            guild_data = GuildInit.get(GuildInit.guild_id == fetched_guild_id)
        except DoesNotExist as e:
            guild_data = self.rowplace(fetched_guild_id)

        return guild_data

    @connector
    def rowreset(self, guild_id : int):
        guild_data = self.rowfetch(guild_id)
        guild_data.command_prefix = self.defaults
        guild_data.save()

        return guild_data

    # ================================ SPECIFIC FETCH ================================
    def datafetch(self, guild_id : int, output : str):
        output = output.lower().strip()
        if output == "command_prefix":
            return self.rowfetch(guild_id).command_prefix

    def botprefix(self, bot, message):
        return self.datafetch(message.guild.id, 'command_prefix')

    def datainit(self, guild_id : int):
        self.rowfetch(guild_id)

    