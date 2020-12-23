# Integration of youtube-dl
from bot import alemiBot

import asyncio
import re
import os
import logging
import traceback

from pyrogram import filters
from util.command import filterCommand
from util.parse import cleartermcolor
from util.message import tokenize_json, tokenize_lines, is_me, edit_or_reply
from util.serialization import convert_to_dict
from util.permission import is_superuser
from plugins.help import HelpCategory

logger = logging.getLogger(__name__)

HELP = HelpCategory("Youtube Utilities")

HELP.add_help(["yt-download", "yt"], "Download video from YT", "Download audio in mp3 from a valid youtube link video :D",args="<link>")
@alemiBot.on_message(is_superuser & filterCommand(["yt-download", "yt"], list(alemiBot.prefixes)))
async def yt_download(client, message):
    #args = re.sub(r"-delme(?: |)(?:[0-9]+|)", "", message.command["raw"])
    if "arg" not in message.command:
        return await edit_or_reply(message, "`[!] → ` No link provided")

    msg = await edit_or_reply(message, "` → ` Downloading...")
    try:
        args = message.command["arg"]
        logger.info(f"Downloading video → \"{args}\"")
        proc = await asyncio.create_subprocess_shell(
            "youtube-dl --extract-audio --audio-format mp3 " + args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT)

        stdout, stderr = await proc.communicate()
        #output = cleartermcolor(stdout.decode())

        match = re.search(r"\[ffmpeg\] Destination: (?P<path>.*)", stdout.decode())
        if match:
            filename = match["path"]
            logger.info("Uploading media")
            #await client.send_chat_action(message.chat.id, "upload_document")
            await client.send_audio(message.chat.id, filename, caption=f'` → {filename}`')
            os.remove(filename)
        else:
            await msg.edit_or_reply(f"`$ yt-down`\n`[!] → ` something wrong happen, probably you send an invalid url.")
        
    except Exception as e:
        traceback.print_exc()
        await msg.edit_or_reply(f"`$ yt-down`\n`[!] → ` " + str(e))

