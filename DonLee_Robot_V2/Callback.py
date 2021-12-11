# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

import math
import json
import time
import shutil
import heroku3
import requests
import os
import ast
from pyrogram import filters, Client as DonLee_Robot_V2
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from DonLee_Robot_V2.Config_Vars.Vars import Config
from DonLee_Robot_V2 import Text, Import, Database, all_connections, active_connection, if_active, delete_connection, make_active, make_inactive, del_all, find_filter, Database, add_user, all_users, humanbytes, filter_stats
 
db = Database()


@DonLee_Robot_V2.on_callback_query()
async def cb_handler(client, query):

    if query.data == "close":
        await query.message.delete()

    elif query.data == "home":
        button = [[  
          Import.Button("➕ 𝖠𝖽𝖽 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖢𝗁𝖺𝗍𝗌 ➕", url=f"http://t.me/{Config.BOT_USERNAME}?startgroup=true")
          ],[
          Import.Button("⚠️ 𝖧𝖾𝗅𝗉", callback_data="help"),
          Import.Button("𝖠𝖻𝗈𝗎𝗍 🤠", callback_data="about")
          ]]
        await query.message.edit_text(Text.START_TEXT.format(query.from_user.mention, Config.DEV_ID), reply_markup=Import.Markup(button))

    elif query.data == "help":
        button = [[
          Import.Button("𝖠𝗎𝗍𝗈𝖥𝗂𝗅𝗍𝖾𝗋", callback_data="autofilter"),
          Import.Button("𝖬𝖺𝗇𝗎𝖺𝗅𝖥𝗂𝗅𝗍𝖾𝗋", callback_data="filter"),
          Import.Button("𝖢𝗈𝗇𝗇𝖾𝖼𝗍𝗂𝗈𝗇𝗌", callback_data="connection")
          ],[
          Import.Button("𝖡𝖺𝗇", callback_data="ban"),
          Import.Button("𝖬𝗎𝗍𝖾", callback_data="mute"),
          Import.Button("𝖯𝗎𝗋𝗀𝖾", callback_data="purge")
          ],[
          Import.Button("𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝖯𝗁", callback_data="telegraph"),
          Import.Button("𝖳𝖳𝖲", callback_data="tts"),
          Import.Button("𝖲𝗍𝗂𝖼𝗄𝖾𝗋 𝖨𝖽", callback_data="sticker")
          ],[
          Import.Button("𝖢𝗈𝗏𝗂𝖽", callback_data="covid"),
          Import.Button("𝖱𝖾𝗉𝗈𝗋𝗍", callback_data="report"),
          Import.Button("𝖶𝖾𝗅𝖼𝗈𝗆𝖾", callback_data="welcome")
          ],[
          Import.Button("🏠𝖧𝗈𝗆𝖾", callback_data="home"),
          Import.Button("𝖲𝗍𝖺𝗍𝗎𝗌", callback_data="status"),
          Import.Button("𝖠𝖻𝗈𝗎𝗍🤠", callback_data="about")
          ]]
        await query.message.edit_text(Text.HELP_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "about":
        button = [[
          Import.Button("👨‍💻𝖣𝖾𝗉𝗅𝗈𝗒", url='https://www.youtube.com/watch?v=NrbMc93aCzA'),
          Import.Button("𝖲𝗈𝗎𝗋𝖼𝖾📦", callback_data="source")
          ],[
          Import.Button("⚠️𝖧𝖾𝗅𝗉", callback_data="help"),
          Import.Button("🏠𝖧𝗈𝗆𝖾", callback_data="home"),
          Import.Button("𝖢𝗅𝗈𝗌𝖾🗑️", callback_data="close")
          ]]
        await query.message.edit_text(Text.ABOUT_TEXT.format(Config.BOT_USERNAME, Config.DEV_ID, Config.DEV_NAME, Config.BOT_USERNAME), reply_markup=Import.Markup(button))

    elif query.data == "autofilter":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help"),
          Import.Button("𝖭𝖾𝗑𝗍 ➡️", callback_data="autofilter1")
          ]] 
        await query.message.edit_text(Text.AUTO_FILTER_1_TEXH, reply_markup=Import.Markup(button))

    elif query.data == "autofilter1":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="autofilter")
          ]]
        await query.message.edit_text(Text.AUTO_FILTER_2_TEXH, reply_markup=Import.Markup(button))

    elif query.data == "filter":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help"),
          Import.Button("𝖵𝗂𝖽𝖾𝗈 📽️", url="https://youtu.be/neJ4jHC9Hng")
          ]]
        await query.message.edit_text(Text.FILTER_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "connection":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help")
          ]]
        await query.message.edit_text(Text.CONNECTION_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "ban":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help")
          ]]
        await query.message.edit_text(Text.BAN_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "mute":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help")
          ]]
        await query.message.edit_text(Text.MUTE_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "pin":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help")
          ]]
        await query.message.edit_text(Text.PIN_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "purge":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help")
          ]]
        await query.message.edit_text(Text.PURGE_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "status":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help"),
          Import.Button("🔃", callback_data="status")
          ]]
        total_users = await db.total_users_count()
        chats, filters = await filter_stats()
        uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - Config.Up_Time))
        await query.message.edit_text(Text.STATUS_TEXT.format(total_users, chats, filters, uptime), reply_markup=Import.Markup(button))

    elif query.data == "welcome":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help")
          ]]
        await query.message.edit_text(Text.WELCOME_TEXT.format(Config.CUSTOM_WELCOME, Config.CUSTOM_WELCOME_TEXT), reply_markup=Import.Markup(button))

    elif query.data == "telegraph":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help")
          ]]
        await query.message.edit_text(Text.TELEGRAPH_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "covid":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help")
          ]]
        await query.message.edit_text(Text.COVID_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "tts":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help")
          ]]
        await query.message.edit_text(Text.TTS_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "sticker":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help")
          ]]
        await query.message.edit_text(Text.STICKER_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "source":
        button = [[
          Import.Button("🖥️ 𝖵𝗂𝖽𝖾𝗈 🖥️", url="https://www.youtube.com/watch?v=NrbMc93aCzA"),
          ],[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="about"),
          Import.Button("𝖢𝗋𝖾𝖽𝗂𝗍𝗌 💞", callback_data="credits")
          ]]
        await query.message.edit_text(Text.SOURCE_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "credits":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="source")
          ]]
        await query.message.edit_text(Text.CREDITS_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "report":
        button = [[
          Import.Button("🔙 𝖡𝖺𝖼𝗄", callback_data="help")
          ]]
        await query.message.edit_text(Text.REPORT_TEXT, reply_markup=Import.Markup(button))

    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            grpid  = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("𝖬𝖺𝗄𝖾 𝖲𝗎𝗋𝖾 𝖨𝖺𝗆 𝖯𝗋𝖾𝗌𝖾𝗇𝗍 𝗂𝗇 𝗒𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉!!", quote=True)
                    return
            else:
                await query.message.edit_text(
                    "𝖨'𝗆 𝗇𝗈𝗍 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗍𝗈 𝖺𝗇𝗒 𝗀𝗋𝗈𝗎𝗉𝗌!\n𝖢𝗁𝖾𝖼𝗄 /connections 𝗈𝗋 𝖼𝗈𝗇𝗇𝖾𝖼𝗍 𝗍𝗈 𝖺𝗇𝗒 𝗀𝗋𝗈𝗎𝗉𝗌",
                    quote=True
                )
                return

        elif (chat_type == "group") or (chat_type == "supergroup"):
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in Config.AUTH_USERS):    
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("𝖸𝗈𝗎 𝗇𝖾𝖾𝖽 𝗍𝗈 𝖻𝖾 𝖦𝗋𝗈𝗎𝗉 𝖮𝗐𝗇𝖾𝗋 𝗈𝗋 𝖺𝗇 𝖠𝗎𝗍𝗁 𝖴𝗌𝖾𝗋 𝗍𝗈 𝖽𝗈 𝗍𝗁𝖺𝗍!",show_alert=True)
    
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type
        
        if chat_type == "private":
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif (chat_type == "group") or (chat_type == "supergroup"):
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in Config.AUTH_USERS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("𝖳𝗁𝖺𝗍𝗌 𝗇𝗈𝗍 𝖿𝗈𝗋 𝗒𝗈𝗎!!",show_alert=True)


    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        title = query.data.split(":")[2]
        act = query.data.split(":")[3]
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnectbot"

        keyboard = Import.Markup([
            [Import.Button(f"{stat}", callback_data=f"{cb}:{group_id}:{title}"),
                Import.Button("D𝖾𝗅𝖾𝗍𝖾", callback_data=f"deletecb:{group_id}")],
            [Import.Button("𝖡𝖺𝖼𝗄", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"𝖦𝗋𝗈𝗎𝗉 𝖭𝖺𝗆𝖾 : **{title}**\n𝖦𝗋𝗈𝗎𝗉 𝖨𝖣 : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return

    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        title = query.data.split(":")[2]
        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"𝖢𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗍𝗈 **{title}**",
                parse_mode="md"
            )
            return
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
            return

    elif "disconnectbot" in query.data:
        await query.answer()

        title = query.data.split(":")[2]
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"𝖣𝗂𝗌𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝖿𝗋𝗈𝗆 **{title}**",
                parse_mode="md"
            )
            return
        else:
            await query.message.edit_text(
                f"𝖲𝗈𝗆𝖾 𝖾𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝖾𝖽!!",
                parse_mode="md"
            )
            return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝗂𝗈𝗇"
            )
            return
        else:
            await query.message.edit_text(
                f"𝖲𝗈𝗆𝖾 𝖾𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝖾𝖽!!",
                parse_mode="md"
            )
            return
    
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "𝖳𝗁𝖾𝗋𝖾 𝖺𝗋𝖾 𝗇𝗈 𝖺𝖼𝗍𝗂𝗏𝖾 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝗂𝗈𝗇𝗌!! 𝖢𝗈𝗇𝗇𝖾𝖼𝗍 𝗍𝗈 𝗌𝗈𝗆𝖾 𝗀𝗋𝗈𝗎𝗉𝗌 𝖿𝗂𝗋𝗌𝗍",
            )
            return
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                if active:
                    act = " - ACTIVE"
                else:
                    act = ""
                buttons.append(
                    [
                        Import.Button(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{title}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "𝖸𝗈𝗎𝗋 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗀𝗋𝗈𝗎𝗉 𝖽𝖾𝗍𝖺𝗂𝗅𝗌;\n\n",
                reply_markup=Import.Markup(buttons)
            )
   
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert,show_alert=True)
