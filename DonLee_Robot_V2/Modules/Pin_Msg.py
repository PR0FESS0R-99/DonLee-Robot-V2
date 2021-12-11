# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

from pyrogram import filters, Client as DonLee_Robot_V2
from DonLee_Robot_V2 import Config, Import
COMMAND_HAND_LER = Config.COMMAND_HAND_LER
from DonLee_Robot_V2.Admins import admin_check, extract_user, admin_fliter

@DonLee_Robot_V2.on_message(filters.command(["pin"], COMMAND_HAND_LER) & admin_fliter)
async def pin(_, message: Import.Msg):
    if not message.reply_to_message:
        return
    await message.reply_to_message.pin()

@DonLee_Robot_V2.on_message(filters.command(["unpin"], COMMAND_HAND_LER) & admin_fliter)
async def unpin(_, message: Import.Msg):
    if not message.reply_to_message:
        return
    await message.reply_to_message.unpin()
