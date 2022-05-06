import os
import nextcord
from nextcord.ext import commands
from source import log as Log, whitelist as whitelist_, timeout as timeout_, verify as verify_, music as music_

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
log: Log.Log = Log.Log()

DISCORDTOKEN = ""
with open("token", 'r', encoding="utf-8") as file:
    DISCORDTOKEN = file.read()

# Initilising bot stuff
intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
client = nextcord.Client(intents=intents)

@bot.command(name="timeout")
async def timeout(ctx: commands.context.Context, author: str = ""):
    await timeout_.timeout_start(ctx=ctx, log=log)

@bot.command(name="verify")
async def verify_start(ctx: commands.context.Context, author: str = ""):
    pass

@bot.command(name='whitelist', help='Format: !whitelist [username]')
async def whitelist(ctx: commands.context.Context, author: str = ""):
    await whitelist_.whitelist_start(ctx=ctx, log=log)
    
@bot.command(name='music', help='Format: !whitelist [username]')
async def music(ctx: commands.context.Context, author: str = ""):
    await music_.music_start(ctx=ctx, log=log)

log.append_log("Starting!")
bot.run(DISCORDTOKEN)
