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

    # -------- PRIVATE START STICKER -------- #
    sticker_msg = None
    if message.chat.type == enums.ChatType.PRIVATE:
        try:
            sticker_msg = await message.reply_sticker("CAACAgIAAxkBAAKa1Weu-cAFlaKn6nLLfZnMr6CZyq0vAAJvPQACSgThSVvFRwJ3swa3NgQ")
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

        if sticker_msg:
            try:
                await asyncio.sleep(2)
                await sticker_msg.delete()
            except Exception:
                pass
        
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
        
# -------- FORCE SUBSCRIBE -------- #

    if AUTH_CHANNEL:
        try:
            subscribed = await is_subscribed(client, message)
        except Exception:
            subscribed = False

        if not subscribed:
            try:
                if REQUEST_TO_JOIN_MODE:
                    invite = await client.create_chat_invite_link(
                        chat_id=int(AUTH_CHANNEL),
                        creates_join_request=True
                    )
                else:
                    invite = await client.create_chat_invite_link(
                        chat_id=int(AUTH_CHANNEL)
                    )
            except ChatAdminRequired:
                await message.reply_text("❌ Bot must be admin in force-sub channel")
                return

            buttons = [
                [InlineKeyboardButton("📢 Join Channel", url=invite.invite_link)]
            ]

            if TRY_AGAIN_BTN:
                buttons.append(
                    [InlineKeyboardButton("🔁 Try Again", callback_data="checksub")]
                )

            await message.reply_text(
                text="⚠️ You must join our channel to use this bot.",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return

    # -------- NORMAL START (NO PAYLOAD) -------- #

    if len(message.command) == 1:

        if PREMIUM_AND_REFERAL_MODE:
            buttons = [
                [
                    InlineKeyboardButton(
                        "⤬ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⤬",
                        url=f"https://t.me/{temp.U_NAME}?startgroup=true"
                    )
                ],
                [
                    InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
                    InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=CHNL_LNK)
                ],
                [
                    InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help"),
                    InlineKeyboardButton("ᴇᴀʀɴ", callback_data="shortlink_info")
                ],
                [
                    InlineKeyboardButton(
                        "👑 Premium & Referral",
                        callback_data="subscription"
                    )
                ]
            ]
        else:
            buttons = [
                [
                    InlineKeyboardButton(
                        "⤬ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⤬",
                        url=f"https://t.me/{temp.U_NAME}?startgroup=true"
                    )
                ],
                [
                    InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
                    InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=CHNL_LNK)
                ],
                [
                    InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help")
                ]
            ]

        if CLONE_MODE:
            buttons.append(
                [InlineKeyboardButton("🤖 Create Clone Bot", callback_data="clone")]
            )

        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(
                message.from_user.mention,
                temp.U_NAME,
                temp.B_NAME
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
        return

    # -------- START PAYLOAD -------- #

    data = message.command[1]

    # -------- REFERRAL PAYLOAD -------- #
    if data.startswith("VJ-"):
        try:
            ref_user = int(data.split("-", 1)[1])
            added = await referal_add_user(ref_user, message.from_user.id)

            if added and PREMIUM_AND_REFERAL_MODE:
                await message.reply_text(
                    "✅ Referral registered!\n\nSend /start again."
                )

                total = await get_referal_users_count(ref_user)

                await client.send_message(
                    chat_id=ref_user,
                    text=f"🎉 New referral joined!\nTotal referrals: {total}"
                )

                if total >= REFERAL_COUNT:
                    seconds = await get_seconds(REFERAL_PREMEIUM_TIME)
                    if seconds > 0:
                        expire = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
                        await db.update_user({
                            "id": ref_user,
                            "expiry_time": expire
                        })
                        await delete_all_referal_users(ref_user)

                        await client.send_message(
                            chat_id=ref_user,
                            text="👑 You are now Premium user!"
                        )
            return
        except Exception as e:
            logger.error(f"Referral error: {e}")

    # -------- SIMPLE PAYLOADS -------- #

    if data in ["help", "about", "subscribe", "okay", "error"]:
        await message.reply_text(
            "ℹ️ Use menu buttons below.",
        )
        return
# ========================= Plan & MyPlan ========================= #

@Client.on_message(filters.command("plan") & filters.private)
async def plan_command(client, message):

    text = (
        "<b>💎 PREMIUM PLANS</b>\n\n"
        "🚀 Unlock all premium features:\n"
        "• No Shortlink\n"
        "• Unlimited Files\n"
        "• Faster Access\n"
        "• Priority Support\n\n"
        "<b>💰 Pricing:</b>\n"
        "🔹 1 Month  - ₹99\n"
        "🔹 3 Months - ₹249\n"
        "🔹 Lifetime - ₹499\n\n"
        "📩 Contact Admin to buy premium 👇"
    )

    buttons = [
        [InlineKeyboardButton("💬 Contact Admin", url="https://t.me/bambhaniya_jagdish_79")]
    ]

    if PREMIUM_AND_REFERAL_MODE:
        buttons.append([InlineKeyboardButton("👥 Refer & Earn", callback_data="refer_info")])

    await message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("myplan") & filters.private)
async def myplan_command(client, message):

    user_id = message.from_user.id

    # check premium
    if not await db.has_premium_access(user_id):
        return await message.reply_text(
            "<b>❌ You don't have any active premium plan.</b>\n\n"
            "💎 Buy premium to unlock all features.\n"
            "👉 Send /plan"
        )

    # get premium data
    premium = await db.get_premium(user_id)

    start_time = datetime.fromtimestamp(premium["start_time"])
    end_time = datetime.fromtimestamp(premium["end_time"])

    remaining_days = (end_time - datetime.now()).days

    text = (
        "<b>👤 YOUR PREMIUM DETAILS</b>\n\n"
        f"✅ <b>Status:</b> Active\n"
        f"📅 <b>Plan Started:</b> {start_time.strftime('%d %b %Y')}\n"
        f"⏳ <b>Plan Expiry:</b> {end_time.strftime('%d %b %Y')}\n"
        f"🕒 <b>Days Remaining:</b> {remaining_days} days\n\n"
        "❤️ Thank you for supporting us!"
    )

    await message.reply_text(text)


# ========================= GROUP MESSAGE HANDLER ========================= #

@Client.on_message(
    filters.text
    & filters.group
    & ~filters.command(["start", "help", "about"])
)
async def group_message_handler(client: Client, message: Message):

    if not message.text:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()

    settings = await get_settings(chat_id)

    if settings is None:
        await save_group_settings(chat_id)
        settings = await get_settings(chat_id)

    # -------- AUTH CHANNEL CHECK -------- #
    if AUTH_CHANNEL and not await pub_is_subscribed(client, message):
        try:
            await message.delete()
        except Exception:
            pass
        return

    # -------- VERIFICATION CHECK -------- #
    if VERIFY:
        verified = await check_verification(user_id)
        if not verified:
            token = await get_token(user_id)
            link = f"https://t.me/{temp.U_NAME}?start=verify_{token}"

            buttons = [
                [InlineKeyboardButton("✅ Verify", url=link)]
            ]

            await message.reply_text(
                "⚠️ Please verify yourself to use this bot.",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return

    # -------- AUTO FILTER SEARCH -------- #

    files = await get_file_details(query)

    if not files:
        return

    await auto_send_files(
        client=client,
        message=message,
        files=files,
        settings=settings
    )


# ========================= AUTO SEND FILES ========================= #

async def auto_send_files(client, message, files, settings):

    user_id = message.from_user.id
    chat_id = message.chat.id

    sent = 0

    for file in files:

        if sent >= MAX_B_TN:
            break

        file_id = unpack_new_file_id(file.file_id)
        file_name = file.file_name
        file_size = get_size(file.file_size)

        caption = CUSTOM_FILE_CAPTION.format(
            file_name=file_name,
            file_size=file_size
        )

        # -------- SHORTLINK CHECK -------- #
        if SHORTLINK_MODE and not await db.has_premium_access(user_id):
            short = await get_shortlink(user_id, file_id)
            buttons = [
                [InlineKeyboardButton("⬇️ Get File", url=short)]
            ]
        else:
            buttons = [
                [InlineKeyboardButton("⬇️ Download", callback_data=f"file_{file_id}")]
            ]

        try:
            await client.send_message(
                chat_id=chat_id,
                text=caption,
                reply_markup=InlineKeyboardMarkup(buttons),
                protect_content=PROTECT_CONTENT
            )
            sent += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            continue

# ========================= CALLBACK QUERY HANDLER ========================= #

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):

    data = query.data
    user_id = query.from_user.id
    message = query.message

    try:
        await query.answer()
    except Exception:
        pass

    # -------- FORCE SUB CHECK (CALLBACK) -------- #
    if AUTH_CHANNEL and not await pub_is_subscribed(client, message):
        await query.answer("❌ Join channel first!", show_alert=True)
        return

    # -------- FILE DOWNLOAD CALLBACK -------- #
    if data.startswith("file_"):

        file_id = data.split("_", 1)[1]

        # ---- verification check ---- #
        if VERIFY:
            verified = await check_verification(user_id)
            if not verified:
                token = await get_token(user_id)
                link = f"https://t.me/{temp.U_NAME}?start=verify_{token}"
                await query.answer("⚠️ Please verify first", show_alert=True)
                await message.reply_text(
                    "🔐 Verification required",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("✅ Verify", url=link)]]
                    )
                )
                return

        # ---- shortlink check ---- #
        if SHORTLINK_MODE and not await db.has_premium_access(user_id):
            short = await get_shortlink(user_id, file_id)
            await query.answer("🔗 Get link to download", show_alert=True)
            await message.reply_text(
                "⬇️ Click below to download",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("⬇️ Download", url=short)]]
                )
            )
            return

        # ---- send actual file ---- #
        file = await get_file_details(file_id)
        if not file:
            await query.answer("❌ File not found", show_alert=True)
            return

        try:
            await client.send_cached_media(
                chat_id=user_id,
                file_id=file.file_id,
                caption=CUSTOM_FILE_CAPTION.format(
                    file_name=file.file_name,
                    file_size=get_size(file.file_size)
                ),
                protect_content=PROTECT_CONTENT
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            logger.error(f"Send file error: {e}")

        return

    # -------- VERIFY CALLBACK -------- #
    if data.startswith("verify_"):
        token = data.split("_", 1)[1]
        ok = await check_token(user_id, token)

        if ok:
            await query.answer("✅ Verified Successfully", show_alert=True)
            await message.edit_text("✅ You are verified, send your search again.")
        else:
            await query.answer("❌ Invalid or expired token", show_alert=True)
        return

    # -------- BATCH FILE CALLBACK -------- #
    if data.startswith("batch_"):
        batch_id = data.split("_", 1)[1]
        BATCH_FILES[user_id] = batch_id

        await query.answer("📦 Batch started", show_alert=True)
        await message.reply_text(
            "📦 Batch request received.\nSend /start again to receive files."
        )
        return

    # -------- TRY AGAIN FORCE SUB -------- #
    if data == "checksub":
        await query.answer("🔁 Checking subscription...")
        await message.delete()
        return

# ========================= BATCH FILE SENDER ========================= #

@Client.on_message(filters.command("batch") & filters.private)
async def batch_command(client: Client, message: Message):

    user_id = message.from_user.id

    if user_id not in BATCH_FILES:
        await message.reply_text("❌ No batch request found.")
        return

    batch_id = BATCH_FILES.get(user_id)

    status = await message.reply_text("⏳ Processing batch files...")

    try:
        files = await get_file_details(batch_id)
    except Exception:
        await status.edit("❌ Failed to fetch batch files.")
        return

    sent_msgs = []

    for file in files:
        try:
            file_id = unpack_new_file_id(file.file_id)
            file_name = file.file_name
            file_size = get_size(file.file_size)

            caption = CUSTOM_FILE_CAPTION.format(
                file_name=file_name,
                file_size=file_size
            )

            # -------- STREAM MODE -------- #
            if STREAM_MODE:
                log_msg = await client.send_cached_media(
                    chat_id=LOG_CHANNEL,
                    file_id=file.file_id
                )

                stream = f"{URL}watch/{log_msg.id}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
                download = f"{URL}{log_msg.id}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

                buttons = [
                    [
                        InlineKeyboardButton("▶️ Watch", url=stream),
                        InlineKeyboardButton("⬇️ Download", url=download)
                    ]
                ]

                sent = await client.send_message(
                    chat_id=user_id,
                    text=caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )

            else:
                sent = await client.send_cached_media(
                    chat_id=user_id,
                    file_id=file.file_id,
                    caption=caption,
                    protect_content=PROTECT_CONTENT
                )

            sent_msgs.append(sent)

        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            logger.error(f"Batch send error: {e}")
            continue

    await status.edit("✅ Batch completed!")

    # -------- AUTO DELETE AFTER 10 MIN -------- #
    await asyncio.sleep(600)

    for msg in sent_msgs:
        try:
            await msg.delete()
        except Exception:
            pass

    try:
        del BATCH_FILES[user_id]
    except Exception:
        pass


# ========================= STREAM CLEANUP ========================= #

@Client.on_message(filters.command("clear") & filters.user(ADMINS))
async def clear_logs(client: Client, message: Message):

    try:
        await message.reply_text("🧹 Cleaning cache done.")
    except Exception:
        pass

# ========================= MENU CALLBACKS ========================= #

@Client.on_callback_query(filters.regex("^about$"))
async def about_cb(client: Client, query: CallbackQuery):

    await query.answer()
    await query.message.edit_text(
        text=script.ABOUT_TXT,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="home")]]
        ),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("^help$"))
async def help_cb(client: Client, query: CallbackQuery):

    await query.answer()
    await query.message.edit_text(
        text=script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="home")]]
        ),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("^subscription$"))
async def subscription_cb(client: Client, query: CallbackQuery):

    await query.answer()
    await query.message.edit_text(
        text=PAYMENT_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("💳 Buy Premium", url=OWNER_LNK)],
                [InlineKeyboardButton("🔙 Back", callback_data="home")]
            ]
        )
    )


@Client.on_callback_query(filters.regex("^home$"))
async def home_cb(client: Client, query: CallbackQuery):

    await query.answer()

    buttons = [
        [
            InlineKeyboardButton(
                "⤬ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⤬",
                url=f"https://t.me/{temp.U_NAME}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help")
        ],
        [
            InlineKeyboardButton("👑 Premium", callback_data="subscription")
        ]
    ]

    await query.message.edit_text(
        text=script.START_TXT.format(
            query.from_user.mention,
            temp.U_NAME,
            temp.B_NAME
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


# ========================= SAFETY FALLBACK ========================= #

@Client.on_message(filters.private & filters.command("help"))
async def help_cmd(client: Client, message: Message):
    await message.reply_text(script.HELP_TXT)


@Client.on_message(filters.private & filters.command("about"))
async def about_cmd(client: Client, message: Message):
    await message.reply_text(script.ABOUT_TXT)


# ========================= END OF FILE ========================= #





