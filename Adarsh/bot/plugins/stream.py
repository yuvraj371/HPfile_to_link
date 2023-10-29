import os
import asyncio
from asyncio import TimeoutError
from Adarsh.bot import StreamBot
from Adarsh.utils.database import Database
from Adarsh.utils.human_readable import humanbytes
from Adarsh.vars import Var
from urllib.parse import quote_plus
from pyrogram import filters, Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.name)

MY_PASS = None  # Remove password

@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio | filters.photo), group=4)
async def private_receive_handler(c: Client, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"New User Joined: Name: [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started Your Bot!!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == enums.ChatMemberStatus.BANNED:
                await c.send_message(
                    chat_id=m.chat.id,
                    text="You are banned due to violating rules."
                )
                return
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="Join my updates channel to use me.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Join Now", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                )
            )
            return
        except Exception as e:
            await m.reply_text(e)
            await c.send_message(
                chat_id=m.chat.id,
                text="Error: Something went wrong."
            )
            return
    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        msg_text = """
        File Name: {0}
        File Size: {1}
        Download Link: {2}
        Watch Online: {3}
        This link is permanent and won't get expired
        """.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link, stream_link)
        await log_msg.reply_text(
            text=f"Requested by: [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nUser ID: `{m.from_user.id}`\nStream Link: {stream_link}",
            disable_web_page_preview=True,
            quote=True
        )
        await m.reply_text(
            text=msg_text,
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Watch", url=stream_link),
                 InlineKeyboardButton('Download', url=online_link)]
            ])
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Got FloodWait of {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nUser ID: `{str(m.from_user.id)}`", disable_web_page_preview=True)

@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.photo), group=-1)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        await log_msg.reply_text(
            text=f"Channel Name: `{broadcast.chat.title}`\nChannel ID: `{broadcast.chat.id}`\nRequest URL: {stream_link}",
            quote=True
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            id=broadcast.id,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Watch", url=stream_link),
                 InlineKeyboardButton('Download', url=online_link)]
            ])
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"Got FloodWait of {str(w.x)}s from {broadcast.chat.title}\nChannel ID: `{str(broadcast.chat.id)}`", disable_web_page_preview=True)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"Error Traceback: `{e}`", disable_web_page_preview=True)
        print(f"Can't Edit Broadcast Message!\nError: {e}")
