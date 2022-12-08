import nextcord
from nextcord.ext import commands
import source.log as log

def verify_command(ctx: commands.context.Context, no_parameters: int, role_allowed: str, command: str, log: log.Log):

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

def verify_command(interaction: nextcord.Interaction, role_allowed: str, command: str, log: log.Log):

    return_str = []
    commands = {
        "whitelist": "!whitelist [Username]",
        "timeout": "!timeout [role to timeout] [length in minutes]"
    }

    if nextcord.utils.get(interaction.guild.roles, name=role_allowed) not in interaction.user.roles:
        log.append_log(f'Error in role verification user did not have the role: {role_allowed}')
        return_str.append("You do not have permission to use this command")

    return "\n".join(return_str)
