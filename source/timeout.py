import datetime
import nextcord
from nextcord.ext import commands
from source.verify_command import verify_command
from source.log import Log

async def timeout_start(ctx: commands.context.Context, log: Log):
    try:
        log.append_log("[Timeout] Timeout command received")

        reply_message = await ctx.send("Working")

        error = verify_command(ctx=ctx, role_allowed='mods', no_parameters=2, command="timeout", log=log)
        if error:
            await reply_message.edit(error)
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        message = ctx.message.content.strip('@').split()

        guild: nextcord.Guild = ctx.guild
        role_list = await guild.fetch_roles()
        roles = {}
        for item in role_list:
            roles[item.name.strip('@')] = item.id

        await reply_message.edit("Finding role...")

        if not message[1] in roles.keys():
            log.append_log(f"[Timeout] Requested role ({message[1]}) does not exist")
            await reply_message.edit(f"RuhRoh. Role {message[1]} does not exist")
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await reply_message.edit("Finding members with role...")

        role = guild.get_role(roles[message[1]])
        members = role.members

        for i, member in enumerate(members):
            if member.bot:
                members.pop(i)

        await reply_message.edit("Timing out members, this may take a while...")

        failed_timeout = []
        timeout_expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=int(message[2]))
        for member in members:
            try:
                await member.timeout(timeout_expire)

            except Exception as e:
                log.append_log(f"[Timeout] Failed to timeout user {member}, reason: {e}")
                failed_timeout.append(member)

        if len(failed_timeout) > 0:
            await reply_message.edit("RuhRoh. Failed to time out user(s):\n" + '\n'.join([item.name for item in failed_timeout]) )

        reply_message.edit(f"Timed out users will be timed out until {timeout_expire.strftime('%H:%M %Y-%m-%d')}")
        log.append_log("[Timeout] Timeout complete")
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
    except Exception as e:
        log.append_log(f'[Timeout] {e}')
        await reply_message.edit(f'Fatal Error Occured: {e}')