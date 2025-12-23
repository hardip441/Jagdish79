
import random
import datetime
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import PREMIUM_AND_REFERAL_MODE, CHNL_LNK, REFERAL_COUNT, REFERAL_PRE, REFERAL_PREMEIUM_TIME
from database import db, referal_add_user, get_referal_users_count, delete_all_referal_users
import script

PICS = ["https://telegra.ph/file/abcd.jpg", "https://telegra.ph/file/efgh.jpg"]  # Example photos

@TechVJBot.on_message()
async def start_command(client, message):
    if len(message.command) == 2:
        data = message.command[1]

        if data in ["subscribe", "error", "okay", "help"]:
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
                caption=script.START_TXT.format(
                    message.from_user.mention,
                    temp.U_NAME,
                    temp.B_NAME
                ),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
            return

        if data.split("-", 1)[0] == "VJ":
            user_id = int(data.split("-", 1)[1])
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
                        f"<b>{message.from_user.mention} start the bot with your referral link\n\n"
                        f"Total Referals - {num_referrals}</b>"
                    )
                )

                if num_referrals == REFERAL_COUNT:
                    time = REFERAL_PRE
                    # Handle premium time
                    seconds = await get_seconds(time)
                    if seconds > 0:
                        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
                        user_data = {"id": user_id, "expiry_time": expiry_time} 
                        await db.update_user(user_data)
                        await delete_all_referal_users(user_id)
                        await client.send_message(
                            chat_id=user_id,
                            text=f"<b>You Have Successfully Completed Total Referal.\n\nYou Added In Premium For {REFERAL_PREMEIUM_TIME}</b>"
                        )
                        return

@TechVJBot.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data

    if data == "help":
        await callback_query.message.edit_text(
            script.HELP_TXT,
            parse_mode=enums.ParseMode.HTML
        )
    elif data == "about":
        await callback_query.message.edit_text(
            script.ABOUT_TXT,
            parse_mode=enums.ParseMode.HTML
        )
    elif data == "subscription":
        buttons = [[
            InlineKeyboardButton('ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ', url=CHNL_LNK)
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await callback_query.message.edit_text(
            script.SUBSCRIPTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif data == "shortlink_info":
        await callback_query.message.edit_text(
            script.SHORTLINK_INFO,
            parse_mode=enums.ParseMode.HTML
        )

# Referral reward logic after user completes required referrals
async def handle_referral_reward(user_id):
    num_referrals = await get_referal_users_count(user_id)
    if num_referrals >= REFERAL_COUNT:
        # Give premium
        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=REFERAL_PREMEIUM_TIME)
        user_data = {"id": user_id, "expiry_time": expiry_time}
        await db.update_user(user_data)
        await delete_all_referal_users(user_id)
        await TechVJBot.send_message(
            chat_id=user_id,
            text=f"<b>Congratulations! You have completed all referrals.\nYou are now premium until {expiry_time}.</b>"
        )
# Handle /start with referral link
@TechVJBot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    if len(message.command) == 1:
        # Normal start
        buttons = [[
            InlineKeyboardButton('⤬ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
        ], [
            InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url=CHNL_LNK)
        ]]

        if PREMIUM_AND_REFERAL_MODE:
            buttons.append([
                InlineKeyboardButton('ᴘʀᴇᴍɪᴜᴍ ᴀɴᴅ ʀᴇғᴇʀʀᴀʟ', callback_data='subscription')
            ])

        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return

    # Start with referral
    data = message.command[1]
    if data.split("-", 1)[0] == "VJ":
        user_id = int(data.split("-", 1)[1])
        vj = await referal_add_user(user_id, message.from_user.id)

        if vj and PREMIUM_AND_REFERAL_MODE:
            await message.reply(
                f"<b>You have joined using the referral link of user with ID {user_id}\n\nSend /start again to use the bot</b>"
            )

            num_referrals = await get_referal_users_count(user_id)
            await client.send_message(
                chat_id=user_id,
                text=f"<b>{message.from_user.mention} started the bot using your referral link\nTotal Referrals - {num_referrals}</b>"
            )

            # Handle referral reward
            await handle_referral_reward(user_id)

