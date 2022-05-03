import os
import nextcord
from nextcord.ext import commands
from log import Log
from timeout import timeout_start
from whitelist import whitelist_start
import music as music_

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
log = Log()

DISCORDTOKEN = ""
with open("token", 'r', encoding="utf-8") as file:
    DISCORDTOKEN = file.read()

# Initilising bot stuff
intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
client = nextcord.Client(intents=intents)

def verify_command(ctx: commands.context.Context, no_parameters: int, role_allowed: str, command: str):

    return_str = []
    commands = {
        "whitelist": "!whitelist [Username]",
        "timeout": "!timeout [role to timeout] [length in minutes]"
    }

    if nextcord.utils.get(ctx.guild.roles, name=role_allowed) not in ctx.author.roles:
        log.append_log(f'Error in role verification user did not have the role: {role_allowed}')
        return_str.append("You do not have permission to use this command")

    if len(ctx.message.content.split()) != no_parameters + 1:
        log.append_log('Error in number of parameters')
        return_str.append(f"Incorrect usage of command, {commands[command]}")

    return "\n".join(return_str)

@bot.command(name="timeout")
async def timeout(ctx: commands.context.Context, author: str = ""):
    await timeout_start(ctx=ctx, log=log)

@bot.command(name="verify")
async def verify(ctx: commands.context.Context, author: str = ""):
    pass

@bot.command(name='whitelist', help='Format: !whitelist [username]')
async def whitelist(ctx: commands.context.Context, author: str = ""):
    await whitelist_start(ctx=ctx, log=log)
    
@bot.command(name='music', help='Format: !whitelist [username]')
async def music(ctx: commands.context.Context, author: str = ""):
    await music_.music_start(ctx=ctx, log=log)

log.append_log("Starting!")
bot.run(DISCORDTOKEN)
