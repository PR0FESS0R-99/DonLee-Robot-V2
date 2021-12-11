# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

import asyncio
from pyrogram import filters, Client as DonLee_Robot_V2
from DonLee_Robot_V2 import Config
TG_MAX_SELECT_LEN = Config.TG_MAX_SELECT_LEN
COMMAND_HAND_LER = Config.COMMAND_HAND_LER
from DonLee_Robot_V2.Admins import admin_check, f_onw_fliter

@DonLee_Robot_V2.on_message(filters.command("purge", COMMAND_HAND_LER) &f_onw_fliter)
async def purge(client, message):
    if message.chat.type not in (("supergroup", "channel")):
        return

    is_admin = await admin_check(message)

    if not is_admin:
        return

    status_message = await message.reply_text("𝖣𝖾𝗅𝖾𝗍𝗂𝗇𝗀.....", quote=True)
    await message.delete()
    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        for a_s_message_id in range(
            message.reply_to_message.message_id,
            message.message_id
        ):
            message_ids.append(a_s_message_id)
            if len(message_ids) == TG_MAX_SELECT_LEN:
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=message_ids,
                    revoke=True
                )
                count_del_etion_s += len(message_ids)
                message_ids = []
        if len(message_ids) > 0:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message_ids,
                revoke=True
            )
            count_del_etion_s += len(message_ids)

    await status_message.edit_text(
        f"𝖣𝖾𝗅𝖾𝗍𝖾𝖽 <b>{count_del_etion_s}</b> 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌"
    )
    await asyncio.sleep(9)
    await status_message.delete()
