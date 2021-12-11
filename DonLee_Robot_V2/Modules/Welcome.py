# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

from pyrogram import filters, Client as DonLee_Robot_V2
from DonLee_Robot_V2 import Config, Import

@DonLee_Robot_V2.on_message(filters.new_chat_members)
async def auto_welcome(bot: DonLee_Robot_V2, msg: Import.Msg):
#   from PR0FESS0R-99 import Auto-Welcome-Bot
#   from PR0FESS0R-99 import ID-Bot
#   first = msg.from_user.first_name
#   last = msg.from_user.last_name
#   mention = msg.from_user.mention
#   username = msg.from_user.username
#   id = msg.from_user.id
#   group_name = msg.chat.title
#   group_username = msg.chat.username
#   button_name = os.environ.get("WELCOME_BUTTON_NAME", name_button)
#   button_link = os.environ.get("WELCOME_BUTTON_LINK", link_button)
#   welcome_text = f"Hey {mention}\nWelcome To {group_name}"
#   WELCOME_TEXT = os.environ.get("WELCOME_TEXT", welcome_text)
#   YES = "True"
#   NO = "False"
#   HOOOO = CUSTOM_WELCOME
#   BUTTON = bool(os.environ.get("CUSTOM_WELCOME"))
    if Config.CUSTOM_WELCOME == "on":
        print("Welcome Message Activate")
        Auto_Delete=await msg.reply_text(text=Config.CUSTOM_WELCOME_TEXT.format(
            mention = msg.from_user.mention,
            groupname = msg.chat.title),
        reply_markup=Import.Markup([[
            Import.Button(Config.WELCOME_BUTTON_NAME, url="t.me/{Config.FORCE_CHANNEL}")
            ]] 
            )
        )
        await asyncio.sleep(60) # in seconds
        await Auto_Delete.delete()
    else:
        await msg.delete()
