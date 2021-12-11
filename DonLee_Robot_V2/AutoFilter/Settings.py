# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

import random
import re

from pyrogram import filters, Client as DonLee_Robot_V2
from DonLee_Robot_V2.Config_Vars.Vars import Config
from DonLee_Robot_V2 import Import, LOGGER, VERIFY


@DonLee_Robot_V2.on_message(filters.command(["settings"]) & filters.group, group=1)
async def settings(bot, update):
    
    chat_id = update.chat.id
    user_id = update.from_user.id if update.from_user else None
    global VERIFY

    if VERIFY.get(str(chat_id)) == None: # Make Admin's ID List
        admin_list = []
        async for x in bot.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
        admin_list.append(None)
        VERIFY[str(chat_id)] = admin_list

    if not user_id in VERIFY.get(str(chat_id)): # Checks if user is admin of the chat
        return
    
    bot_info = await bot.get_me()
    bot_first_name= bot_info.first_name
    
    text =f"<u>{bot_first_name}'s</u> 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌 𝖯𝖺𝗇𝗇𝖾𝗅.....\n"
    text+=f"\n𝖸𝗈𝗎 𝖢𝖺𝗇 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖬𝖾𝗇𝗎 𝖳𝗈 𝖢𝗁𝖺𝗇𝗀𝖾 𝖢𝗈𝗇𝗇𝖾𝖼𝗍𝗂𝗏𝗂𝗍𝗒 𝖠𝗇𝖽 𝖪𝗇𝗈𝗐 𝖲𝗍𝖺𝗍𝗎𝗌 𝖮𝖿 𝖸𝗈𝗎𝗋 𝖤𝗏𝖾𝗋𝗒 𝖢𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝖢𝗁𝖺𝗇𝗇𝖾𝗅, 𝖢𝗁𝖺𝗇𝗀𝖾 𝖥𝗂𝗅𝗍𝖾𝗋 𝖳𝗒𝗉𝖾𝗌, 𝖢𝗈𝗇𝖿𝗂𝗀𝗎𝗋𝖾 𝖥𝗂𝗅𝗍𝖾𝗋 𝖱𝖾𝗌𝗎𝗅𝗍𝗌"
    
    buttons = [[
        Import.Button("📣 Channels 📣", callback_data=f"channel_list({chat_id})")
        ],[
        Import.Button("📚 Filter Types 📚", callback_data=f"types({chat_id})")
        ],[
        Import.Button("🛠 Configure 🛠", callback_data=f"config({chat_id})")
        ],[
        Import.Button("👩‍👦‍👦 Group Status", callback_data=f"status({chat_id})"), 
        Import.Button("🤖 Bot Status", callback_data=f"about({chat_id})")
        ],[
        Import.Button("🔐 Close 🔐", callback_data="close")
        ]]
    
    reply_markup = Import.Markup(buttons)
    
    await bot.send_photo (
        chat_id=chat_id,
        photo=random.choice(Config.PHOTO),
        caption=text, 
        reply_markup=reply_markup, 
        parse_mode="html",
        reply_to_message_id=update.message_id
    )
