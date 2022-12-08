import os, sys
import datetime
import nextcord
from nextcord.ext import commands
from source.verify_command import verify_command
from source.log import Log


# noinspection PyArgumentList
async def timeout_start(ctx: commands.context.Context, log: Log):
    reply_message = await ctx.send("Working")
    try:
        log.append_log("[Timeout] Timeout command received")

        error = verify_command(ctx=ctx, role_allowed='mods', no_parameters=2, command="timeout", log=log)
        if error:
            await reply_message.edit(error)
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        message = ctx.message.content.split()
        role = message[1].strip("@<>&")
        time = message[2]

        try:
            role = int(role)

        except ValueError as e:
            log.append_log(f"[Timeout] Incorrect role format or tried @here or @everyone")
            await reply_message.edit("RuhRoh. Role was not entered in the correct format\nYou cannot timeout here or everyone")
            return

        try:
            time = int(time)

        except ValueError as e:
            log.append_log(f"[Timeout] Gave a non int for time")
            await reply_message.edit("RuhRoh. The time must be a whole number of the minutes you want to timeout like '3'")
            return


        role = ctx.guild.get_role(role)

        if role is None:
            log.append_log(f"[Timeout] Requested role ({message[1]}) does not exist")
            await reply_message.edit(f"RuhRoh. Role {message[1]} does not exist")
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await reply_message.edit("Finding members with role...")

        members = []

        for member in role.members:
            if not member.bot:
                members.append(member)

        await reply_message.edit("Timing out members, this may take a while...")

        failed_timeout = []
        timeout_expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=time)

        for member in members:
            try:
                await member.timeout(timeout_expire)

            except Exception as e:
                log.append_log(f"[Timeout] Failed to timeout user {member}, reason: {e}")
                failed_timeout.append(member)

        if len(failed_timeout) > 0:
            await reply_message.edit("RuhRoh. Failed to time out user(s):\n" + '\n'.join([item.name for item in failed_timeout]) )

        await reply_message.edit(f"Timed out users are timed out until {timeout_expire.strftime('%H:%M %Y-%m-%d')}")
        log.append_log("[Timeout] Timeout complete")
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_name = str(type(e)).split()[1].strip("> '")
        log.append_log(f"{err_name}: File: {fname}, Line: {exc_tb.tb_lineno}, Error: {e}")
        await reply_message.edit(f'Fatal Error Occured: {e}')


async def timeout2_start(interaction: nextcord.Interaction, role: str, time: str, log: Log):
    try:
        reply_message = []
        role = role.strip("@<>&")
        guild = interaction.guild

        log.append_log(f"[Timeout] Timeout command received. Initiated by {interaction.user.display_name} (id: {interaction.user.id})")
        error = verify_command(interaction=interaction, role_allowed='mods', command="timeout", log=log)
        error = False
        if error:
            await interaction.followup.send(error)
            return

        try:
            role = int(role)

        except ValueError as e:
            log.append_log(f"[Timeout] Incorrect role format or tried @here or @everyone")
            await interaction.followup.send("RuhRoh. Role was not entered in the correct format\nYou cannot timeout here or everyone")
            return

        try:
            time = int(time)

        except ValueError as e:
            log.append_log(f"[Timeout] Gave a non int for time")
            await interaction.followup.send("RuhRoh. The time must be a whole number of the minutes you want to timeout like '3'")
            return

        role = guild.get_role(role)

        if role is None:
            log.append_log(f"[Timeout] Role does not exist")
            await interaction.followup.send(f"RuhRoh. Role does not exist")
            return

        members = []

        for member in role.members:
            if not member.bot:
                members.append(member)

        failed_timeout = []
        timeout_expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=time)

        for member in members:
            try:
                await member.timeout(timeout_expire)

            except Exception as e:
                log.append_log(f"[Timeout] Failed to timeout user {member}, reason: {e}")
                failed_timeout.append(member)

        reply_message.append(f"Timed out users are timed out until {timeout_expire.strftime('%H:%M %Y-%m-%d')}")
        if len(failed_timeout) > 0:
            reply_message.append("RuhRoh. Failed to time out user(s):\n" + '\n'.join([member.name for member in failed_timeout]))

        log.append_log("[Timeout] Timeout complete")
        await interaction.followup.send("\n".join(reply_message))

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_name = str(type(e)).split()[1].strip("> '")
        log.append_log(f"{err_name}: File: {fname}, Line: {exc_tb.tb_lineno}, Error: {e}")
        await interaction.followup.send(f'Fatal Error Occured: {e}')