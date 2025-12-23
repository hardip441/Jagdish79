# commands.py

import random
import datetime
from pyrogram import Client, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Agar tumhara DB ya referral module alag hai, unhe import karna mat bhoolna
# from database_module import db, referal_add_user, get_referal_users_count, delete_all_referal_users

# Bot constants (tumhare original values se replace kar dena)
PREMIUM_AND_REFERAL_MODE = True
REFERAL_COUNT = 5
REFERAL_PRE = 86400  # seconds, example: 1 day
REFERAL_PREMEIUM_TIME = "7 days"
CHNL_LNK = "https://t.me/your_channel"  # channel link
PICS = ["https://telegra.ph/file/example.jpg"]  # start command images

# Temp class for placeholders (tumhare original user data se replace kar dena)
class Temp:
    U_NAME = "YourBotUsername"
    B_NAME = "YourBotName"

temp = Temp()

# MEIUM_TIME placeholder function
async def get_seconds(time):
    return time  # simple placeholder, tumhare logic se replace kar dena

# Part 2: /start command
async def start_command(client, message):
    if len(message.command) == 1:
        # Normal /start without referral
        buttons = [[
            InlineKeyboardButton(
                '⤬ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⤬',
                url=f'http://t.me/{temp.U_NAME}?startgroup=true'
            )
        ], [
            InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url=CHNL_LNK)
        ]]

        if PREMIUM_AND_REFERAL_MODE:
            buttons.append([
                InlineKeyboardButton(
                    'ᴘʀᴇᴍɪᴜᴍ ᴀɴᴅ ʀᴇғᴇʀʀᴀʟ',
                    callback_data='subscription'
                )
            ])

        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply_photo(
            photo=random.choice(PICS),
            caption=f"Hello {message.from_user.mention}! Welcome to {temp.B_NAME}.",
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return

    # /start with referral link
    data = message.command[1]

    if data.split("-", 1)[0] == "VJ":
        user_id = int(data.split("-", 1)[1])

        # Add referral user
        vj = await referal_add_user(user_id, message.from_user.id)

        if vj and PREMIUM_AND_REFERAL_MODE:
            await message.reply(
                f"<b>You have joined using the referral link of user with ID {user_id}\n\n"
                "Send /start again to use the bot</b>"
            )

            num_referrals = await get_referal_users_count(user_id)

            await client.send_message(
                chat_id=user_id,
                text=(
                    f"<b>{message.from_user.mention} started the bot with your referral link\n\n"
                    f"Total Referrals - {num_referrals}</b>"
                )
            )

            if num_referrals == REFERAL_COUNT:
                seconds = await get_seconds(REFERAL_PRE)
                if seconds > 0:
                    expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
                    user_data = {"id": user_id, "expiry_time": expiry_time} 
                    await db.update_user(user_data)  # update user in DB
                    await delete_all_referal_users(user_id)
                    await client.send_message(
                        chat_id=user_id,
                        text=f"<b>You Have Successfully Completed Total Referrals.\n\nYou Are Added To Premium For {REFERAL_PREMEIUM_TIME}</b>"
                    )
                    return

        # Buttons after referral
        buttons = [[
            InlineKeyboardButton(
                '⤬ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⤬',
                url=f'http://t.me/{temp.U_NAME}?startgroup=true'
            )
        ], [
            InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url=CHNL_LNK)
        ], [
            InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('ᴇᴀʀɴ ᴍᴏɴᴇʏ', callback_data="shortlink_info")
        ]]

        if PREMIUM_AND_REFERAL_MODE:
            buttons.append([
                InlineKeyboardButton(
                    'ᴘʀᴇᴍɪᴜᴍ ᴀɴᴅ ʀᴇғᴇʀʀᴀʟ',
                    callback_data='subscription'
                )
            ])

        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=f"Hello {message.from_user.mention}! Welcome to {temp.B_NAME}.",
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

# Part 3: Callback queries
@TechVJBot.on_callback_query()
async def callback_handlers(client, callback_query):
    data = callback_query.data

    if data == "help":
        await callback_query.message.edit_text(
            text=script.HELP_TXT,
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "about":
        await callback_query.message.edit_text(
            text=script.ABOUT_TXT,
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "subscription":
        buttons = [[
            InlineKeyboardButton('💳 Buy Premium', url=PREMIUM_LINK),
            InlineKeyboardButton('🔙 Back', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await callback_query.message.edit_text(
            text=script.SUBSCRIPTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "shortlink_info":
        await callback_query.message.edit_text(
            text=script.SHORTLINK_TXT,
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "start":
        # Re-run start command
        await start_command(client, callback_query.message)

# Part 4: Admin & Utility Functions

# ---------- Referral Handling ----------
async def referal_add_user(referrer_id: int, user_id: int) -> bool:
    """Add a user under a referrer in database"""
    try:
        # Check if user already referred
        exists = await db.check_referral(referrer_id, user_id)
        if exists:
            return False
        await db.add_referral(referrer_id, user_id)
        return True
    except Exception as e:
        print(f"Referral add error: {e}")
        return False

async def get_referal_users_count(user_id: int) -> int:
    """Return total referrals of a user"""
    try:
        count = await db.count_referrals(user_id)
        return count
    except:
        return 0

async def delete_all_referal_users(user_id: int):
    """Delete all referral records of a user"""
    try:
        await db.clear_referrals(user_id)
    except:
        pass

async def get_seconds(time_str: str) -> int:
    """Convert time string like '1d', '2h' to seconds"""
    num = int(time_str[:-1])
    unit = time_str[-1].lower()
    if unit == "d":
        return num * 86400
    elif unit == "h":
        return num * 3600
    elif unit == "m":
        return num * 60
    return num

# ---------- Admin Commands ----------
@TechVJBot.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_message(client, message):
    text = message.text.split(None, 1)[1] if len(message.text.split(None, 1)) > 1 else None
    if not text:
        await message.reply("Please provide a message to broadcast.")
        return
    users = await db.get_all_users()
    for user_id in users:
        try:
            await client.send_message(chat_id=user_id, text=text)
        except:
            continue
    await message.reply("Broadcast completed.")

@TechVJBot.on_message(filters.command("stats") & filters.user(ADMINS))
async def bot_stats(client, message):
    total_users = await db.total_users()
    total_referrals = await db.total_referrals()
    await message.reply(f"Total Users: {total_users}\nTotal Referrals: {total_referrals}")

# ---------- Premium Check ----------
async def is_premium(user_id: int) -> bool:
    user = await db.get_user(user_id)
    if not user:
        return False
    if "expiry_time" not in user:
        return False
    return datetime.datetime.now() < user["expiry_time"]

# ---------- Utilities ----------
async def start_command(client, message):
    # Your start command logic here
    await message.reply("Welcome to the bot!")

async def add_premium(user_id: int, time_str: str):
    seconds = await get_seconds(time_str)
    expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    user_data = {"id": user_id, "expiry_time": expiry_time}
    await db.update_user(user_data)
    
# Part 5: Callback Queries & Final Helpers

from pyrogram import enums, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import datetime

# ---------- Callback Query Handlers ----------
@TechVJBot.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data

    if data == "help":
        await callback_query.message.edit(
            text="Here is how to use the bot...",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Back", callback_data="start")
            ]])
        )

    elif data == "about":
        await callback_query.message.edit(
            text="This bot is made by VJ Team. Enjoy!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Back", callback_data="start")
            ]])
        )

    elif data == "subscription":
        await callback_query.message.edit(
            text="Check our premium & referral plans...",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Back", callback_data="start")
            ]])
        )

    elif data == "start":
        buttons = [[
            InlineKeyboardButton('⤬ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⤬', url=f'http://t.me/{callback_query.from_user.username}?startgroup=true')
        ], [
            InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url=CHNL_LNK)
        ]]
        if PREMIUM_AND_REFERAL_MODE:
            buttons.append([
                InlineKeyboardButton('ᴘʀᴇᴍɪᴜᴍ ᴀɴᴅ ʀᴇғᴇʀʀᴀʟ', callback_data='subscription')
            ])

        await callback_query.message.edit(
            text=script.START_TXT.format(callback_query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )

# ---------- Utility: Random Photo Reply ----------
async def send_random_photo(message):
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Help", callback_data="help")]
        ]),
        parse_mode=enums.ParseMode.HTML
    )

# ---------- Startup Hook ----------
@TechVJBot.on_message(filters.command("start"))
async def start_handler(client, message):
    data = message.text.split(None, 1)[1] if len(message.text.split(None, 1)) > 1 else None

    if data and data.split("-", 1)[0] == "VJ":
        user_id = int(data.split("-", 1)[1])
        vj = await referal_add_user(user_id, message.from_user.id)
        if vj and PREMIUM_AND_REFERAL_MODE:
            await message.reply(f"<b>You have joined using the referral link of user with ID {user_id}\n\nSend /start again to use the bot</b>")
            num_referrals = await get_referal_users_count(user_id)
            await client.send_message(chat_id=user_id, text=f"<b>{message.from_user.mention} started the bot with your referral link\n\nTotal Referrals - {num_referrals}</b>")
            if num_referrals == REFERAL_COUNT:
                await add_premium(user_id, REFERAL_PRE)
    await send_random_photo(message)

# ---------- End of commands.py ----------


