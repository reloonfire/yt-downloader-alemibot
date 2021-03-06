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

HELP.add_help(["yt-download", "yt"], "Download audio from YT!", "Download audio in mp3 from a valid youtube link video :D. You can reply to a valid link to download or use .yt <link>",args="<link>")
@alemiBot.on_message(is_superuser & filterCommand(["yt-download", "yt"], list(alemiBot.prefixes)))
async def yt_download(client, message):
    args = ""
    if "arg" not in message.command:
        if message.reply_to_message is not None:
            args = message.reply_to_message.text
        else:
            return await edit_or_reply(message, "`[!] → ` No link provided")
    else:
        args = message.command["arg"]
    msg = await edit_or_reply(message, "` → ` Downloading...")
    try:
        logger.info(f"Downloading video → \"{args}\"")
        proc = await asyncio.create_subprocess_shell(
            "youtube-dl --extract-audio --audio-format mp3 " + args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT)

        stdout, stderr = await proc.communicate()

        match = re.search(r"\[ffmpeg\] Destination: (?P<path>.*)", stdout.decode())
        if match:
            filename = match["path"]
            logger.info("Uploading media")
            await client.send_audio(message.chat.id, filename, caption=f'` → {filename}`')
            os.remove(filename)
        else:
            await edit_or_reply(msg, f"`$ yt-down`\n`[!] → ` something wrong happen, probably you send an invalid url.")
        
    except Exception as e:
        traceback.print_exc()
        await edit_or_reply(msg, f"`$ yt-down`\n`[!] → ` " + str(e))

