import os
from asyncio import sleep

import nextcord
from nextcord.ext import commands
from source import log as Log, whitelist as whitelist_, timeout as timeout_, verify as verify_, music as music_

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)
log: Log.Log = Log.Log()

with open("token", 'r', encoding="utf-8") as file:
    DISCORDTOKEN = file.read()

# Initializing bot stuff
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
client = nextcord.Client(intents=intents)


@bot.command(name="timeout")
async def timeout(ctx: commands.context.Context, author: str = ""):
    await timeout_.timeout_start(ctx=ctx, log=log)


@bot.slash_command(name="roleout", description="Timeout a role for x minutes.")
async def roleout(interaction: nextcord.Interaction, role: str, time: str):
    """
    Timeout all members of a role for specified amount of minutes
    :param interaction: nextcord.Interaction object
    :param role: The role to timeout
    :param time: The amount of time to timeout for in minutes
    :return: None
    """
    await interaction.response.defer()
    await timeout_.timeout2_start(interaction=interaction, role=role, time=time, log=log)


@bot.command(name="verify")
async def verify_start(ctx: commands.context.Context, author: str = ""):
    pass


@bot.slash_command(name="whitelist",
                   description="Whitelist yourself on the Minecraft server. Format: /whitelist [username]")
async def whitelist(interaction: nextcord.Interaction, username: str):
    print(interaction.data)
    # await whitelist_.whitelist_start(interaction=interaction, username=username, log=log)


@bot.command(name='music', help='Format: !whitelist [username]')
async def music(ctx: commands.context.Context, author: str = ""):
    pass
    await music_.music_start(ctx=ctx, log=log)


log.append_log("Starting!")
bot.run(DISCORDTOKEN)
