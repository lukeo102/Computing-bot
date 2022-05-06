import queue
import nextcord
from nextcord.ext import commands
from source.verify_command import verify_command
from source.log import Log

song_queue = queue.Queue

def music_add(ctx: commands.context.Context, log: Log):
    log.append_log("[Music] Add command received")
        

def music_remove(ctx: commands.context.Context, log: Log):
    log.append_log("[Music] Remove command received")
    

def music_play(ctx: commands.context.Context, log: Log):
    log.append_log("[Music] Play command received")
    

def music_pause(ctx: commands.context.Context, log: Log):
    log.append_log("[Music] Pause command received")
    

def music_skip(ctx: commands.context.Context, log: Log):
    log.append_log("[Music] Skip command received")
    

def music_queue(ctx: commands.context.Context, log: Log):
    log.append_log("[Music] Queue command received")
    if song_queue.qsize() == 0:
        log.append_log("[Music] Queue is empty")
        ctx.reply("Queue is empty.")
        return
    
    log.append_log("[Music] Queue is not empty")
    song_queue_str = "\n".join([f'{i + 1}. {item}' for i, item in enumerate(song_queue)])
    ctx.reply("The song queue is: \n" + song_queue_str)
    return

def music_start(ctx: commands.context.Context, log: Log):
    log.append_log("[Music] Music command received")
    
