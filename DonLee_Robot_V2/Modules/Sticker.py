# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

from pyrogram import filters, Client as DonLee_Robot_V2
from DonLee_Robot_V2.Config_Vars.H_Vars import BUTTONS 
from DonLee_Robot_V2 import Import

@DonLee_Robot_V2.on_message(filters.command(["stickerid"]))
async def stickerid(bot, message):   
    if message.reply_to_message.sticker:
       await message.reply(f"Sticker ID is \n <code>{message.reply_to_message.sticker.file_id}</code>\n\nUnique ID is\n\n<code>{message.reply_to_message.sticker.file_unique_id}</code>", reply_markup=BUTTONS, quote=True)
    else: 
       await message.reply("Oops !! Not a sticker file")
