# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import sys
import re
import json
import time
import base64
import asyncio
import random
import string
import logging
import datetime
from urllib.parse import quote_plus

from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, ChatAdminRequired
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
    WebAppInfo
)

from Script import script
from info import (
    CLONE_MODE,
    OWNER_LNK,
    REACTIONS,
    CHANNELS,
    REQUEST_TO_JOIN_MODE,
    TRY_AGAIN_BTN,
    ADMINS,
    SHORTLINK_MODE,
    PREMIUM_AND_REFERAL_MODE,
    STREAM_MODE,
    AUTH_CHANNEL,
    REFERAL_PREMEIUM_TIME,
    REFERAL_COUNT,
    PAYMENT_TEXT,
    PAYMENT_QR,
    LOG_CHANNEL,
    PICS,
    BATCH_FILE_CAPTION,
    CUSTOM_FILE_CAPTION,
    PROTECT_CONTENT,
    CHNL_LNK,
    GRP_LNK,
    REQST_CHANNEL,
    SUPPORT_CHAT,
    MAX_B_TN,
    VERIFY,
    SHORTLINK_API,
    SHORTLINK_URL,
    TUTORIAL,
    VERIFY_TUTORIAL,
    IS_TUTORIAL,
    URL
)

from utils import (
    get_settings,
    pub_is_subscribed,
    get_size,
    is_subscribed,
    save_group_settings,
    temp,
    verify_user,
    check_token,
    check_verification,
    get_token,
    get_shortlink,
    get_tutorial,
    get_seconds
)

from database.ia_filterdb import (
    col,
    sec_col,
    get_file_details,
    unpack_new_file_id,
    get_bad_files
)

from database.users_chats_db import (
    db,
    delete_all_referal_users,
    get_referal_users_count,
    get_referal_all_users,
    referal_add_user
)

from database.join_reqs import JoinReqs
from database.connections_mdb import active_connection

from TechVJ.util.file_properties import (
    get_name,
    get_hash,
    get_media_file_size
)

logger = logging.getLogger(__name__)

BATCH_FILES = {}
join_db = JoinReqs()


# ========================= START COMMAND ========================= #

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client: Client, message: Message):

    try:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    except Exception:
        pass

    # -------- GROUP START -------- #
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:

        buttons = [
            [
                InlineKeyboardButton(
                    "⤬ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⤬",
                    url=f"https://t.me/{temp.U_NAME}?startgroup=true"
                )
            ],
            [
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url=f"https://t.me/{SUPPORT_CHAT}"),
                InlineKeyboardButton("ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘ", url=GRP_LNK)
            ],
            [
                InlineKeyboardButton("ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=CHNL_LNK)
            ]
        ]

        await message.reply(
            text=script.START_TXT.format(
                message.from_user.mention if message.from_user else message.chat.title,
                temp.U_NAME,
                temp.B_NAME
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        return

    # -------- USER / PRIVATE START -------- #

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            script.LOG_TEXT_P.format(
                message.from_user.id,
                message.from_user.mention
            )
                )
        
