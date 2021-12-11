# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

from pyrogram import filters, Client as DonLee_Robot_V2
from DonLee_Robot_V2 import Config 
COMMAND_HAND_LER = Config.COMMAND_HAND_LER
from DonLee_Robot_V2.Admins import admin_check, extract_user
from pyrogram.types import ChatPermissions

@DonLee_Robot_V2.on_message(filters.command("mute", COMMAND_HAND_LER))
async def mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            )
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "👍🏻 "
                f"{user_first_name}"
                " ലവന്റെ വായടച്ചിട്ടുണ്ട്! 🤐"
            )
        else:
            await message.reply_text(
                "👍🏻 "
                f"<a href='tg://user?id={user_id}'>"
                "ലവന്റെ"
                "</a>"
                " വായടച്ചിട്ടുണ്ട്! 🤐"
            )


@DonLee_Robot_V2.on_message(filters.command("tmute", COMMAND_HAND_LER))
async def temp_mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    if not len(message.command) > 1:
        return

    user_id, user_first_name = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "അസാധുവായ സമയ തരം വ്യക്തമാക്കി. "
                "പ്രതീക്ഷിച്ചതു m, h, or d, കിട്ടിയത്: {}"
            ).format(
                message.command[1][-1]
            )
        )
        return

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            ),
            until_date=until_date_val
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "കുറച്ചുനേരം മിണ്ടാതിരിക്ക്! 😠"
                f"{user_first_name}"
                f" muted for {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "കുറച്ചുനേരം മിണ്ടാതിരിക്ക്! 😠"
                f"<a href='tg://user?id={user_id}'>"
                "ലവന്റെ"
                "</a>"
                " വായ "
                f" muted for {message.command[1]}!"
            )
