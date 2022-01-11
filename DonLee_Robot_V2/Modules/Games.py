from pyrogram import filters, Client as DonLee_Robot_V2
from DonLee_Robot_V2.Config_Vars.Vars import Config
from DonLee_Robot_V2 import Text
from DonLee_Robot_V2.Admins import f_onw_fliter

@DonLee_Robot_V2.on_message(filters.command(["throw", "dart"], Config.COMMAND_HAND_LER) & f_onw_fliter)
async def throw_dart(client, message):
    rep_mesg_id = message.message_id
    if message.reply_to_message:
        rep_mesg_id = message.reply_to_message.message_id
    await client.send_dice(
        chat_id=message.chat.id,
        emoji=Text.DART_E_MOJI_1,
        disable_notification=True,
        reply_to_message_id=rep_mesg_id
    )

@DonLee_Robot_V2.on_message(filters.command(["roll", "dice"], Config.COMMAND_HAND_LER) & f_onw_fliter)
async def roll_dice(client, message):
    rep_mesg_id = message.message_id
    if message.reply_to_message:
        rep_mesg_id = message.reply_to_message.message_id
    await client.send_dice(
        chat_id=message.chat.id,
        emoji=Text.DICE_E_MOJI_2,
        disable_notification=True,
        reply_to_message_id=rep_mesg_id
    )

@DonLee_Robot_V2.on_message(filters.command("runs", Config.COMMAND_HAND_LER) & f_onw_fliter)
async def runs(_, message):
    effective_string = random.choice(Text.RUN_STRINGS)
    if message.reply_to_message:
        await message.reply_to_message.reply_text(effective_string)
    else:
        await message.reply_text(effective_string)




