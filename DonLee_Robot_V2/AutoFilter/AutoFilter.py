# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

import re
import time
import asyncio
from pyrogram import filters, Client as DonLee_Robot_V2
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery  
from DonLee_Robot_V2 import Config, donlee_imdb, Database, VERIFY, remove_emoji, FIND, INVITE_LINK, ACTIVE_CHATS, recacher, gen_invite_links

db = Database()
@DonLee_Robot_V2.on_callback_query(filters.regex(r"navigate\((.+)\)"), group=2)
async def cb_navg(bot, update: CallbackQuery):
    """
    A Callback Funtion For The Next Button Appearing In Results
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    index_val, btn, query = re.findall(r"navigate\((.+)\)", query_data)[0].split("|", 2)
    try:
        ruser_id = update.message.reply_to_message.from_user.id
    except Exception as e:
        print(e)
        ruser_id = None
    
    admin_list = VERIFY.get(str(chat_id))
    if admin_list == None: # Make Admin's ID List
        
        admin_list = []
        
        async for x in bot.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
            
        admin_list.append(None) # Just For Anonymous Admin....
        VERIFY[str(chat_id)] = admin_list
    
    if not ((user_id == ruser_id) or (user_id in admin_list)): # Checks if user is same as requested user or is admin
        await update.answer("Ask for your own movie 🤗",show_alert=True)
        return


    if btn == "next":
        index_val = int(index_val) + 1
    elif btn == "back":
        index_val = int(index_val) - 1
    
    achats = ACTIVE_CHATS[str(chat_id)]
    configs = await db.find_chat(chat_id)
    pm_file_chat = configs["configs"]["pm_fchat"]
    show_invite = configs["configs"]["show_invite_link"]
    show_invite = (False if pm_file_chat == True else show_invite)
    
    results = FIND.get(query).get("results")
    leng = FIND.get(query).get("total_len")
    max_pages = FIND.get(query).get("max_pages")
    
    try:
        temp_results = results[index_val].copy()
    except IndexError:
        return # Quick Fix🏃🏃
    except Exception as e:
        print(e)
        return

    if ((index_val + 1 )== max_pages) or ((index_val + 1) == len(results)): # Max Pages
        temp_results.append([
            InlineKeyboardButton("«« 𝖡𝖺𝖼𝗄", callback_data=f"navigate({index_val}|back|{query})"),
            InlineKeyboardButton(f"{index_val + 1}/{len(results) if len(results) < max_pages else max_pages}", callback_data="ignore")
        ])

    elif int(index_val) == 0:
        pass

    else:
        temp_results.append([
            InlineKeyboardButton("«« 𝖡𝖺𝖼𝗄", callback_data=f"navigate({index_val}|back|{query})"),
            InlineKeyboardButton(f"{index_val + 1}/{len(results) if len(results) < max_pages else max_pages}", callback_data="ignore"),
            InlineKeyboardButton("𝖭𝖾𝗑𝗍 »»", callback_data=f"navigate({index_val}|next|{query})")
        ])

    
    if show_invite and int(index_val) !=0 :
        
        ibuttons = []
        achatId = []
        await gen_invite_links(configs, chat_id, bot, update)
        
        for x in achats["chats"] if isinstance(achats, dict) else achats:
            achatId.append(int(x["chat_id"])) if isinstance(x, dict) else achatId.append(x)
        
        for y in INVITE_LINK.get(str(chat_id)):
            
            chat_id = int(y["chat_id"])
            
            if chat_id not in achatId:
                continue
            
            chat_name = y["chat_name"]
            invite_link = y["invite_link"]
            
            if ((len(ibuttons)%2) == 0):
                ibuttons.append(
                    [
                        InlineKeyboardButton
                            (
                                f"⚜ {chat_name} ⚜", url=invite_link
                            )
                    ]
                )

            else:
                ibuttons[-1].append(
                    InlineKeyboardButton
                        (
                            f"⚜ {chat_name} ⚜", url=invite_link
                        )
                )
            
        for x in ibuttons:
            temp_results.insert(0, x)
        ibuttons = None
        achatId = None
    
    reply_markup = InlineKeyboardMarkup(temp_results)
    text=f"""
↪️ 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖬𝗈𝗏𝗂𝖾: {query}
🗃️ 𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝖾𝗌 : {leng}
📑 𝖳𝗈𝗍𝖺𝗅 𝖯𝖺𝗀𝖾 : 1/{index_val + 1}/{len(results) if len(results) < max_pages else max_pages}
👤 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖡𝗒 : {update.from_user.mention}"""
     
    try:
        imdb = await donlee_imdb(query)
        await update.message.edit_caption(
                caption=f"""
↪️ 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖬𝗈𝗏𝗂𝖾: {query}
🎞️ 𝖳𝗂𝗍𝗅𝖾: <a href={imdb['url']}>{imdb.get('title')}
🎭 𝖦𝖾𝗇𝗋𝖾𝗌: {imdb.get('genres')}
📆 𝖸𝖾𝖺𝗋: <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>
🌟 𝖱𝖺𝗍𝗂𝗇𝗀: <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10
🗃️ 𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝖾𝗌 : {leng}
📑 𝖳𝗈𝗍𝖺𝗅 𝖯𝖺𝗀𝖾 : 1/{index_val + 1}/{len(results) if len(results) < max_pages else max_pages}
👤 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖡𝗒 : {update.from_user.mention}
🖋 𝖲𝗍𝗈𝗋𝗒𝗅𝗂𝗇𝖾: <code>{imdb.get('plot')}</code>""",
                reply_markup=reply_markup,
                parse_mode="html"
        )
    except Exception as e:
        print(e)
        try:
            await update.message.edit(
                text,
                reply_markup=reply_markup,
                parse_mode="html"
            )
        
        except FloodWait as f: # Flood Wait Caused By Spamming Next/Back Buttons
           await asyncio.sleep(f.x)
           try:
              imdb = await donlee_imdb(query)
              await update.message.edit_caption(
                caption=f"""
↪️ 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖬𝗈𝗏𝗂𝖾: {query}
🎞️ 𝖳𝗂𝗍𝗅𝖾: <a href={imdb['url']}>{imdb.get('title')}
🎭 𝖦𝖾𝗇𝗋𝖾𝗌: {imdb.get('genres')}
📆 𝖸𝖾𝖺𝗋: <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>
🌟 𝖱𝖺𝗍𝗂𝗇𝗀: <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10
🗃️ 𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝖾𝗌 : {leng}
📑 𝖳𝗈𝗍𝖺𝗅 𝖯𝖺𝗀𝖾 : 1/{index_val + 1}/{len(results) if len(results) < max_pages else max_pages}
👤 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖡𝗒 : {update.from_user.mention}
🖋 𝖲𝗍𝗈𝗋𝗒𝗅𝗂𝗇𝖾: <code>{imdb.get('plot')}</code>""",
                reply_markup=reply_markup,
                parse_mode="html"
              )
           except Exception :
               await update.message.edit(
                text,
                reply_markup=reply_markup,
                parse_mode="html"
               )
@DonLee_Robot_V2.on_callback_query(filters.regex(r"settings"), group=2)
async def cb_settings(bot, update: CallbackQuery):

    global VERIFY
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)): # Check If User Is Admin
        return

    bot_status = await bot.get_me()
    bot_fname= bot_status.first_name
    
    text =f"{bot_fname}'s  𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌 𝖯𝖺𝗇𝗇𝖾𝗅.....\n"
    text+=f"\n𝖸𝗈𝗎 𝖢𝖺𝗇 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖬𝖾𝗇𝗎 𝖳𝗈 𝖢𝗁𝖺𝗇𝗀𝖾 𝖢𝗈𝗇𝗇𝖾𝖼𝗍𝗂𝗏𝗂𝗍𝗒 𝖠𝗇𝖽 𝖪𝗇𝗈𝗐 𝖲𝗍𝖺𝗍𝗎𝗌 𝖮𝖿 𝖸𝗈𝗎𝗋 𝖤𝗏𝖾𝗋𝗒 𝖢𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝖢𝗁𝖺𝗇𝗇𝖾𝗅, 𝖢𝗁𝖺𝗇𝗀𝖾 𝖥𝗂𝗅𝗍𝖾𝗋 𝖳𝗒𝗉𝖾𝗌, 𝖢𝗈𝗇𝖿𝗂𝗀𝗎𝗋𝖾 𝖥𝗂𝗅𝗍𝖾𝗋 𝖱𝖾𝗌𝗎𝗅𝗍𝗌 𝖠𝗇𝖽 𝖳𝗈 𝖪𝗇𝗈𝗐 𝖲𝗍𝖺𝗍𝗎𝗌 𝖮𝖿 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉..."
    
    buttons = [[
        InlineKeyboardButton("📣 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌 📣", callback_data=f"channel_list({chat_id})")
        ],[             
        InlineKeyboardButton("📖 𝖥𝗂𝗅𝗍𝖾𝗋 𝖳𝗒𝗉𝖾𝗌 📖", callback_data=f"types({chat_id})")
        ],[
        InlineKeyboardButton("🛠 𝖢𝗈𝗇𝖿𝗂𝗀𝗎𝗋𝖾 🛠", callback_data=f"config({chat_id})")
        ],[
        InlineKeyboardButton("👩‍👦‍👦 𝖦𝗋𝗈𝗎𝗉 𝖲𝗍𝖺𝗍𝗎𝗌 👩‍👦‍👦", callback_data=f"status({chat_id})"), 
        InlineKeyboardButton("🤖 𝖡𝗈𝗍 𝖲𝗍𝖺𝗍𝗎𝗌 🤖", callback_data=f"about({chat_id})")
        ],[
        InlineKeyboardButton("🔐 𝖢𝗅𝗈𝗌𝖾 🔐", callback_data="close")
        ]]

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.edit_text(text, reply_markup=reply_markup, parse_mode="html")



@DonLee_Robot_V2.on_callback_query(filters.regex(r"warn\((.+)\)"), group=2)
async def cb_warn(bot, update: CallbackQuery):

    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    chat_name = chat_name.encode('ascii', 'ignore').decode('ascii')[:35]
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return
    
    channel_id, channel_name, action = re.findall(r"warn\((.+)\)", query_data)[0].split("|", 2)
    
    if action == "connect":
        text=f"<i>Are You Sure You Want To Enable Connection With</i> <code>{channel_name}</code><i>..???</i>\n"
        text+=f"\n<i>This Will Show File Links From</i> <code>{channel_name}</code> <i>While Showing Results</i>..."
    
    elif action == "disconnect":
        text=f"Are You Sure You Want To Disable <code>{channel_name}</code> Connection With The Group???....</i>\n"
        text+=f"\nThe DB Files Will Still Be There And You Can Connect Back To This Channel Anytime From Settings Menu Without Adding Files To DB Again...</i>\n"
        text+=f"\nThis Disabling Just Hide Results From The Filter Results..."
    
    elif action == "c_delete":
        text=f"Are You Sure You Want To Disconnect <code>{channel_name}</code> From This Group??\n"
        text+=f"\n<b>This Will Delete Channel And All Its Files From DB Too....!!</b>\n"
        text+=f"\nYou Need To Add Channel Again If You Need To Shows It Result..."
        
    
    elif action=="f_delete":
        text=f"Are You Sure That You Want To Clear All Filter From This Chat <code>{channel_name}</code>???</i>\n"
        text+=f"\nThis Will Erase All Files From DB.."
        
    buttons = [[
        InlineKeyboardButton("✅️Yes", callback_data=f"{action}({channel_id}|{channel_name})"), 
        InlineKeyboardButton("No❎️", callback_data="close")
        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(text, reply_markup=reply_markup, parse_mode="html")



@DonLee_Robot_V2.on_callback_query(filters.regex(r"channel_list\((.+)\)"), group=2)
async def cb_channel_list(bot, update: CallbackQuery):    
    
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    chat_name = chat_name.encode('ascii', 'ignore').decode('ascii')[:35]
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return
        
    chat_id =  re.findall(r"channel_list\((.+)\)", query_data)[0]
    
    text = "Semms Like You Dont Have Any Channel Connected...\n\nConnect To Any Chat To Continue With This Settings..."
    
    db_list = await db.find_chat(int(chat_id))
    
    channel_id_list = []
    channel_name_list = []
    
    if db_list:
        for x in db_list["chat_ids"]:
            channel_id = x["chat_id"]
            channel_name = x["chat_name"]
            
            try:
                if (channel_id == None or channel_name == None):
                    continue
            except:
                break
            
            channel_name = remove_emoji(channel_name).encode('ascii', 'ignore').decode('ascii')[:35]
            channel_id_list.append(channel_id)
            channel_name_list.append(channel_name)
        
    buttons = []

    buttons.append([
        InlineKeyboardButton("🔙 𝖡𝖺𝖼𝗄", callback_data="settings"),
        InlineKeyboardButton("𝖢𝗅𝗈𝗌𝖾 🔐", callback_data="close")
        ]
    ) 

    if channel_name_list:
        
        text=f"List Of Connected Channels With <code>{chat_name}</code> With There Settings..\n"
    
        for x in range(1, (len(channel_name_list)+1)):
            text+=f"\n<code>{x}. {channel_name_list[x-1]}</code>\n"
    
        text += "\nChoose Appropriate Buttons To Navigate Through Respective Channels"
    
        
        btn_key = [
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
            "11", "12", "13", "14", "15", "16", "17", 
            "18", "19", "20" # Just In Case 😂🤣
        ]
    
        for i in range(1, (len(channel_name_list) + 1)): # Append The Index Number of Channel In Just A Single Line
            if i == 1:
                buttons.insert(0,
                    [
                    InlineKeyboardButton
                        (
                            btn_key[i-1], callback_data=f"info({channel_id_list[i-1]}|{channel_name_list[i-1]})"
                        )
                    ]
                )
        
            else:
                buttons[0].append(
                    InlineKeyboardButton
                        (
                            btn_key[i-1], callback_data=f"info({channel_id_list[i-1]}|{channel_name_list[i-1]})"
                        )
                )
    
    reply_markup=InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
            text = text,
            reply_markup=reply_markup,
            parse_mode="html"
        )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"info\((.+)\)"), group=2)
async def cb_info(bot, update: CallbackQuery):
    """
    A Callback Funtion For Displaying Details Of The Connected Chat And Provide
    Ability To Connect / Disconnect / Delete / Delete Filters of That Specific Chat
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    channel_id, channel_name = re.findall(r"info\((.+)\)", query_data)[0].split("|", 1)
    
    f_count = await db.cf_count(chat_id, int(channel_id)) 
    active_chats = await db.find_active(chat_id)

    if active_chats: # Checks for active chats connected to a chat
        dicts = active_chats["chats"]
        db_cids = [ int(x["chat_id"]) for x in dicts ]
        
        if int(channel_id) in db_cids:
            active_chats = True
            status = "Connected"
            
        else:
            active_chats = False
            status = "Disconnected"
            
    else:
        active_chats = False
        status = "Disconnected"

    text=f"Info About <b>{channel_name}</b>\n"
    text+=f"\nChannel Name: <code>{channel_name}</code>\n"
    text+=f"\nChannel ID: <code>{channel_id}</code>\n"
    text+=f"\nChannel Files: <code>{f_count}</code>\n"
    text+=f"\nCurrent Status: <code>{status}</code>\n"


    if active_chats:
        buttons = [
                    [
                        InlineKeyboardButton
                            (
                                "🚨 Disconnect 🚨", callback_data=f"warn({channel_id}|{channel_name}|disconnect)"
                            ),
                        
                        InlineKeyboardButton
                            (
                                "Delete ❌", callback_data=f"warn({channel_id}|{channel_name}|c_delete)"
                            )
                    ]
        ]

    else:
        buttons = [ 
                    [
                        InlineKeyboardButton
                            (
                                "💠 Connect 💠", callback_data=f"warn({channel_id}|{channel_name}|connect)"
                            ),
                        
                        InlineKeyboardButton
                            (
                                "Delete ❌", callback_data=f"warn({channel_id}|{channel_name}|c_delete)"
                            )
                    ]
        ]

    buttons.append(
            [
                InlineKeyboardButton
                    (
                        "Delete Filters ⚠", callback_data=f"warn({channel_id}|{channel_name}|f_delete)"
                    )
            ]
    )
    
    buttons.append(
            [
                InlineKeyboardButton
                    (
                        "🔙 Back", callback_data=f"channel_list({chat_id})"
                    )
            ]
    )

    reply_markup = InlineKeyboardMarkup(buttons)
        
    await update.message.edit_text(
            text, reply_markup=reply_markup, parse_mode="html"
        )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"^connect\((.+)\)"), group=2)
async def cb_connect(bot, update: CallbackQuery):
    """
    A Callback Funtion Helping The user To Make A Chat Active Chat Which Will
    Make The Bot To Fetch Results From This Channel Too
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    

    if user_id not in VERIFY.get(str(chat_id)):
        return

    channel_id, channel_name = re.findall(r"connect\((.+)\)", query_data)[0].split("|", 1)
    channel_id = int(channel_id)
    
    f_count = await db.cf_count(chat_id, channel_id)
    
    add_active = await db.update_active(chat_id, channel_id, channel_name)
    
    if not add_active:
        await update.answer(f"{channel_name} Is Aldready in Active Connection", show_alert=True)
        return

    text= f"😘Sucessfully Connected To <code>{channel_name}</code>\n"
    text+=f"\n🤠Info About <b>{channel_name}</b>\n"
    text+=f"\n📢Channel Name: <code>{channel_name}</code>\n"
    text+=f"\n🆔Channel ID: <code>{channel_id}</code>\n"
    text+=f"\n🗃️Channel Files: <code>{f_count}</code>\n"
    text+=f"\n🥰Current Status: <code>Connected</code>\n"

    buttons = [
                [
                    InlineKeyboardButton
                        (
                            "🚨 Disconnect 🚨", callback_data=f"warn({channel_id}|{channel_name}|disconnect)"
                        ),
                    
                    InlineKeyboardButton
                        (
                            "Delete ❌", callback_data=f"warn({channel_id}|{channel_name}|c_delete)"
                        )
                ]
    ]
    
    buttons.append(
            [
                InlineKeyboardButton
                    (
                        "⚠ Delete Filters ⚠", callback_data=f"warn({channel_id}|{channel_name}|f_delete)"
                    )
            ]
    )
    
    buttons.append(
            [
                InlineKeyboardButton
                    (
                        "🔙 Back", callback_data=f"channel_list({chat_id})"
                    )
            ]
    )
    await recacher(chat_id, False, True, bot, update)
    
    reply_markup = InlineKeyboardMarkup(buttons)
        
    await update.message.edit_text(
            text, reply_markup=reply_markup, parse_mode="html"
        )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"disconnect\((.+)\)"), group=2)
async def cb_disconnect(bot, update: CallbackQuery):
    """
    A Callback Funtion Helping The user To Make A Chat inactive Chat Which Will
    Make The Bot To Avoid Fetching Results From This Channel
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    channel_id, channel_name = re.findall(r"connect\((.+)\)", query_data)[0].split("|", 1)
    
    f_count = await db.cf_count(chat_id, int(channel_id))
    
    remove_active = await db.del_active(chat_id, int(channel_id))
    
    if not remove_active:
        await update.answer("Couldnt Full Fill YOur Request...\n Report This @CrazyBotszGrp Along With Bot's Log", show_alert=True)
        return
    
    text= f"😑Sucessfully Disconnected From <code>{channel_name}</code>\n"
    text+=f"\n😮‍💨Info About <b>{channel_name}</b>\n"
    text+=f"\n😶‍🌫️Channel Name: <code>{channel_name}</code>\n"
    text+=f"\n🆔Channel ID: <code>{channel_id}</code>\n"
    text+=f"\n🗂️Channel Files: <code>{f_count}</code>\n"
    text+=f"\n🤨Current Status: <code>Disconnected</code>\n"
    
    buttons = [ 
                [
                    InlineKeyboardButton
                        (
                            "💠 Connect 💠", callback_data=f"warn({channel_id}|{channel_name}|connect)"
                        ),
                    
                    InlineKeyboardButton
                        (
                            "Delete ❌", callback_data=f"warn({channel_id}|{channel_name}|c_delete)"
                        )
                ]
    ]
    
    buttons.append(
            [
                InlineKeyboardButton
                    (
                        "Delete Filters ⚠", callback_data=f"warn({channel_id}|{channel_name}|f_delete)"
                    )
            ]
    )
    
    buttons.append(
            [
                InlineKeyboardButton
                    (
                        "🔙 Back", callback_data=f"channel_list({chat_id})"
                    )
            ]
    )
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await recacher(chat_id, False, True, bot, update)

    await update.message.edit_text(
            text, reply_markup=reply_markup, parse_mode="html"
        )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"c_delete\((.+)\)"), group=2)
async def cb_channel_delete(bot, update: CallbackQuery):
    """
    A Callback Funtion For Delete A Channel Connection From A Group Chat History
    Along With All Its Filter Files
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    channel_id, channel_name = re.findall(r"c_delete\((.+)\)", query_data)[0].split("|", 1)
    channel_id = int(channel_id)
    
    c_delete = await db.del_chat(chat_id, channel_id)
    a_delete = await db.del_active(chat_id, channel_id) # pylint: disable=unused-variable
    f_delete = await db.del_filters(chat_id, channel_id)

    if (c_delete and f_delete ):
        text=f"<code>{channel_name} [ {channel_id} ]</code> Has Been Sucessfully Deleted And All Its Files Were Cleared From DB...."

    else:
        text=f"<i>Couldn't Delete Channel And All Its Files From DB Sucessfully....</i>\n<i>Please Try Again After Sometimes...Also Make Sure To Check The Logs..!!</i>"
        await update.answer(text=text, show_alert=True)

    buttons = [
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"channel_list({chat_id})"
                ),
                
            InlineKeyboardButton
                (
                    "Close 🔐", callback_data="close"
                )
        ]
    ]

    await recacher(chat_id, True, True, bot, update)
    
    reply_markup=InlineKeyboardMarkup(buttons)

    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode="html"
    )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"f_delete\((.+)\)"), group=2)
async def cb_filters_delete(bot, update: CallbackQuery):
    """
    A Callback Funtion For Delete A Specific Channel's Filters Connected To A Group
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    channel_id, channel_name = re.findall(r"f_delete\((.+)\)", query_data)[0].split("|", 1)

    f_delete = await db.del_filters(chat_id, int(channel_id))

    if not f_delete:
        text="<b><i>Oops..!!</i></b>\n\nEncountered Some Error While Deleteing Filters....\nPlease Check The Logs...."
        await update.answer(text=text, show_alert=True)
        return

    text =f"All Filters Of <code>{channel_id}[{channel_name}]</code> Has Been Deleted Sucessfully From My DB.."

    buttons=[
        [
            InlineKeyboardButton
                (
                    "Back", callback_data="settings"
                ),
            
            InlineKeyboardButton
                (
                    "Close", callback_data="close"
                )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode="html"
    )
    


@DonLee_Robot_V2.on_callback_query(filters.regex(r"types\((.+)\)"), group=2)
async def cb_types(bot, update: CallbackQuery):
    """
    A Callback Funtion For Changing The Result Types To Be Shown In While Sending Results
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    chat_id = re.findall(r"types\((.+)\)", query_data)[0]
    
    _types = await db.find_chat(int(chat_id))
    
    text=f"<i>Filter Types Enabled/Disbled In <code>{chat_name}</code></i>\n"
    
    _types = _types["types"]
    vid = _types["video"]
    doc = _types["document"]
    aud = _types["audio"]
    
    buttons = []
    
    if vid:
        text+="\n<i><b>Video Index:</b> Enabled</i>\n"
        v_e = "✅"
        vcb_data = f"toggle({chat_id}|video|False)"
    
    else:
        text+="\n<i><b>Video Index:</b> Disabled</i>\n"
        v_e="❎"
        vcb_data = f"toggle({chat_id}|video|True)"

    if doc:
        text+="\n<i><b>Document Index:</b> Enabled</i>\n"
        d_e = "✅"
        dcb_data = f"toggle({chat_id}|document|False)"

    else:
        text+="\n<i><b>Document Index:</b> Disabled</i>\n"
        d_e="❎"
        dcb_data = f"toggle({chat_id}|document|True)"

    if aud:
        text+="\n<i><b>Audio Index:</b> Enabled</i>\n"
        a_e = "✅"
        acb_data = f"toggle({chat_id}|audio|False)"

    else:
        text+="\n<i><b>Audio Index:</b> Disabled</i>\n"
        a_e="❎"
        acb_data = f"toggle({chat_id}|audio|True)"

    
    text+="\n<i>Below Buttons Will Toggle Respective Media Types As Enabled Or Disabled....\n</i>"
    text+="<i>This Will Take Into Action As Soon As You Change Them....</i>"
    
    buttons.append([InlineKeyboardButton(f"{v_e} Video Index {v_e}", callback_data=vcb_data)])
    buttons.append([InlineKeyboardButton(f"{a_e} Audio Index {a_e}", callback_data=acb_data)])
    buttons.append([InlineKeyboardButton(f"{d_e} Document Index {d_e}", callback_data=dcb_data)])
    
    buttons.append(
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"settings"
                )
        ]
    )
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text,
        reply_markup=reply_markup, 
        parse_mode="html"
    )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"toggle\((.+)\)"), group=2)
async def cb_toggle(bot, update: CallbackQuery):
    """
    A Callback Funtion Support handler For types()
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    chat_id, types, val = re.findall(r"toggle\((.+)\)", query_data)[0].split("|", 2)
    
    _types = await db.find_chat(int(chat_id))
    
    _types = _types["types"]
    vid = _types["video"]
    doc = _types["document"]
    aud = _types["audio"]
    
    if types == "video":
        vid = True if val=="True" else False
    elif types == "audio":
        aud = True if val=="True" else False
    elif types == "document":
        doc = True if val=="True" else False
    
        
    settings = {
        "video": vid,
        "audio": aud,
        "document": doc
    }

    process = await db.update_settings(chat_id, settings)
    
    if process:
        await update.answer(text="Filter Types Updated Sucessfully", show_alert=True)
    
    else:
        text="Something Wrong Please Check Bot Log For More Information...."
        await update.answer(text, show_alert=True)
        return
    
    _types = await db.find_chat(int(chat_id))
    
    text =f"<i>Filter Types Enabled In <code>{update.message.chat.title}</code></i>\n"
    
    _types = _types["types"]
    vid = _types["video"]
    doc = _types["document"]
    aud = _types["audio"]
    
    buttons = []
    
    if vid:
        text+="\n<i><b>Video Index:</b> Enabled</i>\n"
        v_e = "✅"
        vcb_data = f"toggle({chat_id}|video|False)"
    
    else:
        text+="\n<i><b>Video Index:</b> Disabled</i>\n"
        v_e="❎"
        vcb_data = f"toggle({chat_id}|video|True)"

    if doc:
        text+="\n<i><b>Document Index:</b> Enabled</i>\n"
        d_e = "✅"
        dcb_data = f"toggle({chat_id}|document|False)"

    else:
        text+="\n<i><b>Document Index:</b> Disabled</i>\n"
        d_e="❎"
        dcb_data = f"toggle({chat_id}|document|True)"

    if aud:
        text+="\n<i><b>Audio Index:</b> Enabled</i>\n"
        a_e = "✅"
        acb_data = f"toggle({chat_id}|audio|False)"

    else:
        text+="\n<i><b>Audio Index:</b> Disabled</i>\n"
        a_e="❎"
        acb_data = f"toggle({chat_id}|audio|True)"

    
    text+="\nBelow Buttons Will Toggle Respective Media Types As Enabled Or Disabled....\n"
    text+="This Will Take Into Action As Soon As You Change Them...."
    
    buttons.append([InlineKeyboardButton(f"{v_e} Video Index {v_e}", callback_data=vcb_data)])
    buttons.append([InlineKeyboardButton(f"{a_e} Audio Index {a_e}", callback_data=acb_data)])
    buttons.append([InlineKeyboardButton(f"{d_e} Document Index {d_e}", callback_data=dcb_data)])
    
    buttons.append(
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"settings"
                )
        ]
    )
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text,
        reply_markup=reply_markup, 
        parse_mode="html"
    )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"config\((.+)\)"), group=2)
async def cb_config(bot, update: CallbackQuery):
    """
    A Callback Funtion For Chaning The Number Of Total Pages / 
    Total Results / Results Per pages / Enable or Diable Invite Link /
    Enable or Disable PM File Chat
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    chat_id = re.findall(r"config\((.+)\)", query_data)[0]
    
    settings = await db.find_chat(int(chat_id))
    
    mp_count = settings["configs"]["max_pages"]
    mf_count = settings["configs"]["max_results"]
    mr_count = settings["configs"]["max_per_page"]
    show_invite = settings["configs"]["show_invite_link"]
    pm_file_chat  = settings["configs"].get("pm_fchat", False)
    accuracy_point = settings["configs"].get("accuracy", 0.80)
    
    text=f"<b>Configure Your <u><code>{chat_name}</code></u> Group's Filter Settings...</b>\n"
    
    text+=f"\n{chat_name} Current Settings:\n"

    text+=f"\n • Max Filter: <code>{mf_count}</code>\n"
    
    text+=f"\n • Max Pages: <code>{mp_count}</code>\n"
    
    text+=f"\n • Max Filter Per Page: <code>{mr_count}</code>\n"

    text+=f"\n • Accuracy Percentage: <code>{accuracy_point}</code>\n"
    
    text+=f"\n • Show Invitation Link: <code>{show_invite}</code>\n"
    
    text+=f"\n • Provide File In Bot PM: <code>{pm_file_chat}</code>\n"
    
    text+="\nAdjust Above Value Using Buttons Below... "
    buttons = [[
       InlineKeyboardButton("📑𝖥𝗂𝗅𝗍𝖾𝗋 𝖯𝖾𝗋 𝖯𝖺𝗀𝖾", callback_data=f"mr_count({mr_count}|{chat_id})"),
       InlineKeyboardButton("📖𝖬𝖺𝗑 𝖯𝖺𝗀𝖾𝗌", callback_data=f"mp_count({mp_count}|{chat_id})")
       ]]


    buttons.append([
       InlineKeyboardButton("✌️𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝗍𝖾𝗋 𝖢𝗈𝗎𝗇𝗍✌️", callback_data=f"({mf_count}|{chat_id})")
       ]
    )

    buttons.append([
       InlineKeyboardButton("⤵️𝖠𝖼𝖼𝗎𝗋𝖺𝖼𝗒⤵️", callback_data=f"accuracy({accuracy_point}|{chat_id})")
       ]
    )

    buttons.append([                
       InlineKeyboardButton("🧐𝖲𝗁𝗈𝗐 𝖨𝗇𝗏𝗂𝗍𝖾 𝖫𝗂𝗇𝗄𝗌", callback_data=f"show_invites({show_invite}|{chat_id})"),
       InlineKeyboardButton("🤖𝖡𝗈𝗍 𝖥𝗂𝗅𝖾 𝖢𝗁𝖺𝗍", callback_data=f"inPM({pm_file_chat}|{chat_id})")
       ]
    )

    buttons.append([
       InlineKeyboardButton("🔙 𝖡𝖺𝖼𝗄", callback_data=f"settings")
       ]
    )
    
    
    reply_markup=InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text, 
        reply_markup=reply_markup, 
        parse_mode="html"
    )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"mr_count\((.+)\)"), group=2)
async def cb_max_buttons(bot, update: CallbackQuery):
    """
    A Callback Funtion For Changing The Count Of Result To Be Shown Per Page
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    count, chat_id = re.findall(r"mr_count\((.+)\)", query_data)[0].split("|", 1)

    text = f"<i>Choose Your Desired 'Max Filter Count Per Page' For Every Filter Results Shown In</i> <code>{chat_name}</code>"

    buttons = [
        [
            InlineKeyboardButton
                (
                    "📝 Filters 📝", callback_data="hi"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "5", callback_data=f"set(per_page|5|{chat_id}|{count})"
                ),
            InlineKeyboardButton
                (
                    "8", callback_data=f"set(per_page|8|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "16", callback_data=f"set(per_page|16|{chat_id}|{count})"
                ),
            InlineKeyboardButton
                (
                    "20", callback_data=f"set(per_page|20|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "25", callback_data=f"set(per_page|25|{chat_id}|{count})"
                ),
            InlineKeyboardButton
                (
                    "30", callback_data=f"set(per_page|30|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "🔙 𝖡𝖺𝖼𝗄", callback_data=f"config({chat_id})"
                )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode="html"
    )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"mp_count\((.+)\)"), group=2)
async def cb_max_page(bot, update: CallbackQuery):
    """
    A Callback Funtion For Changing The Count Of Maximum Result Pages To Be Shown
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    count, chat_id = re.findall(r"mp_count\((.+)\)", query_data)[0].split("|", 1)
    
    text = f"<i>Choose Your Desired 'Max Filter Page Count' For Every Filter Results Shown In</i> <code>{chat_name}</code>"
    
    buttons = [

        [
            InlineKeyboardButton
                (
                    "📰 Pages 📰", callback_data="hi"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "2", callback_data=f"set(pages|2|{chat_id}|{count})"
                ),
            InlineKeyboardButton
                (
                    "4", callback_data=f"set(pages|4|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "6", callback_data=f"set(pages|6|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "8", callback_data=f"set(pages|8|{chat_id}|{count})"
                ),
            InlineKeyboardButton
                (
                    "10", callback_data=f"set(pages|10|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"config({chat_id})"
                )
        ]

    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode="html"
    )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"mf_count\((.+)\)"), group=2)
async def cb_max_results(bot, update: CallbackQuery):
    """
    A Callback Funtion For Changing The Count Of Maximum Files TO Be Fetched From Database
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    count, chat_id = re.findall(r"mf_count\((.+)\)", query_data)[0].split("|", 1)

    text = f"<i>Choose Your Desired 'Max Filter' To Be Fetched From DB For Every Filter Results Shown In</i> <code>{chat_name}</code>"

    buttons = [

        [
InlineKeyboardButton
                (
                    "😵‍💫Results😵‍💫", callback_data="hi"
                )
        ],
        [    
            InlineKeyboardButton
                (
                    "50", callback_data=f"set(results|50|{chat_id}|{count})"
                ),
            InlineKeyboardButton
                (
                    "100", callback_data=f"set(results|100|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "150", callback_data=f"set(results|150|{chat_id}|{count})"
                ),
            InlineKeyboardButton
                (
                    "200", callback_data=f"set(results|200|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "250", callback_data=f"set(results|250|{chat_id}|{count})"
                ),
            InlineKeyboardButton
                (
                    "300", callback_data=f"set(results|300|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"config({chat_id})"
                ),
            InlineKeyboardButton
                (
                    "Close 🔐", callback_data="close"
                )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode="html"
    )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"show_invites\((.+)\)"), group=2)
async def cb_show_invites(bot, update: CallbackQuery):
    """
    A Callback Funtion For Enabling Or Diabling Invite Link Buttons
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    value, chat_id = re.findall(r"show_invites\((.+)\)", query_data)[0].split("|", 1)
    
    value = True if value=="True" else False
    
    if value:
        buttons= [
            [
                InlineKeyboardButton
                    (
                        "Disable ❌", callback_data=f"set(showInv|False|{chat_id}|{value})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "Back 🔙", callback_data=f"config({chat_id})"
                    )
            ]
        ]
    
    else:
        buttons =[
            [
                InlineKeyboardButton
                    (
                        "Enable ✔", callback_data=f"set(showInv|True|{chat_id}|{value})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "Back 🔙", callback_data=f"config({chat_id})"
                    )
            ]
        ]
    
    text=f"<i>This Config Will Help You To Show Invitation Link Of All Active Chats Along With The Filter Results For The Users To Join.....</i>"
    
    reply_markup=InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"inPM\((.+)\)"), group=2)
async def cb_pm_file(bot, update: CallbackQuery):
    """
    A Callback Funtion For Enabling Or Diabling File Transfer Through Bot PM
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    value, chat_id = re.findall(r"inPM\((.+)\)", query_data)[0].split("|", 1)

    value = True if value=="True" else False
    
    if value:
        buttons= [
            [
                InlineKeyboardButton
                    (
                        "Disable ❎", callback_data=f"set(inPM|False|{chat_id}|{value})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "Back 🔙", callback_data=f"config({chat_id})"
                    )
            ]
        ]
    
    else:
        buttons =[
            [
                InlineKeyboardButton
                    (
                        "Enable ✔", callback_data=f"set(inPM|True|{chat_id}|{value})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "Back 🔙", callback_data=f"config({chat_id})"
                    )
            ]
        ]
    
    text=f"<i>This Config Will Help You To Enable/Disable File Transfer Through Bot PM Without Redirecting Them To Channel....</i>"
    
    reply_markup=InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"accuracy\((.+)\)"), group=2)
async def cb_accuracy(bot, update: CallbackQuery):
    """
    A Callaback Funtion to control the accuracy of matching results
    that the bot should return for a query....
    """
    global VERIFY
    chat_id = update.message.chat.id
    chat_name = update.message.chat.title
    user_id = update.from_user.id
    query_data = update.data
    
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    val, chat_id = re.findall(r"accuracy\((.+)\)", query_data)[0].split("|", 1)
    
    text = f"<i>Choose Your Desired 'Accuracy Perceentage' For Every Filter Results Shown In</i> <code>{chat_name}</code>\n\n"
    text+= f"<i>NB: Higher The Value Better Matching Results Will Be Provided... And If Value Is Lower It Will Show More Results \
        Which Is Fimilary To Query Search (Wont Be Accurate)....</i>"

    buttons = [
        [
            InlineKeyboardButton
                (
                    "100 %", callback_data=f"set(accuracy|1.00|{chat_id}|{val})"
                ),
            InlineKeyboardButton
                (
                    "80 %", callback_data=f"set(accuracy|0.80|{chat_id}|{val})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "65 %", callback_data=f"set(accuracy|0.65|{chat_id}|{val})"
                ),
            InlineKeyboardButton
                (
                    "60 %", callback_data=f"set(accuracy|0.60|{chat_id}|{val})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "55 %", callback_data=f"set(accuracy|0.55|{chat_id}|{val})"
                ),
            InlineKeyboardButton
                (
                    "50 %", callback_data=f"set(accuracy|0.50|{chat_id}|{val})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"config({chat_id})"
                ),
            InlineKeyboardButton
                (
                    "Close 🔐", callback_data="close"
                )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode="html"
    )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"set\((.+)\)"), group=2)
async def cb_set(bot, update: CallbackQuery):
    """
    A Callback Funtion Support For config()
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    action, val, chat_id, curr_val = re.findall(r"set\((.+)\)", query_data)[0].split("|", 3)

    try:
        val, chat_id, curr_val = float(val), int(chat_id), float(curr_val)
    except:
        chat_id = int(chat_id)
    
    if val == curr_val:
        await update.answer("New Value Cannot Be Old Value...Please Choose Different Value...!!!", show_alert=True)
        return
    
    prev = await db.find_chat(chat_id)

    accuracy = float(prev["configs"].get("accuracy", 0.80))
    max_pages = int(prev["configs"].get("max_pages"))
    max_results = int(prev["configs"].get("max_results"))
    max_per_page = int(prev["configs"].get("max_per_page"))
    pm_file_chat = True if prev["configs"].get("pm_fchat") == (True or "True") else False
    show_invite_link = True if prev["configs"].get("show_invite_link") == (True or "True") else False
    
    if action == "accuracy": # Scophisticated way 😂🤣
        accuracy = val
    
    elif action == "pages":
        max_pages = int(val)
        
    elif action == "results":
        max_results = int(val)
        
    elif action == "per_page":
        max_per_page = int(val)

    elif action =="showInv":
        show_invite_link = True if val=="True" else False

    elif action == "inPM":
        pm_file_chat = True if val=="True" else False
        

    new = dict(
        accuracy=accuracy,
        max_pages=max_pages,
        max_results=max_results,
        max_per_page=max_per_page,
        pm_fchat=pm_file_chat,
        show_invite_link=show_invite_link
    )
    
    append_db = await db.update_configs(chat_id, new)
    
    if not append_db:
        text="Something Wrong Please Check Bot Log For More Information...."
        await update.answer(text=text, show_alert=True)
        return
    
    text=f"𝖸𝗈𝗎𝗋 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖶𝖺𝗌 𝖴𝗉𝖽𝖺𝗍𝖾𝖽 𝖲𝗎𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒....\𝗇𝖭𝗈𝗐 𝖠𝗅𝗅 𝖴𝗉𝖼𝗈𝗆𝗂𝗇𝗀 𝖱𝖾𝗌𝗎𝗅𝗍𝗌 𝖶𝗂𝗅𝗅 𝖲𝗁𝗈𝗐 𝖠𝖼𝖼𝗈𝗋𝖽𝗂𝗇𝗀 𝖳𝗈 𝖳𝗁𝗂𝗌 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌..."
        
    buttons = [
        [
            InlineKeyboardButton
                (
                    "Back 🔙", callback_data=f"config({chat_id})"
                ),
            
            InlineKeyboardButton
                (
                    "Close 🔐", callback_data="close"
                )
        ]
    ]
    
    reply_markup=InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode="html"
    )



@DonLee_Robot_V2.on_callback_query(filters.regex(r"status\((.+)\)"), group=2)
async def cb_status(bot, update: CallbackQuery):

    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return
    
    chat_id = re.findall(r"status\((.+)\)", query_data)[0]
    
    total_filters, total_chats, total_achats = await db.status(chat_id)
    
    text = f"<b><u>🤓Status Of {chat_name}</u></b>\n"
    text += f"\n🔗Total Connected Chats: <code>{total_chats}</code>\n"
    text += f"\n🙂Total Active Chats: <code>{total_achats}</code>\n"
    text += f"\n📄Total Filters: <code>{total_filters}</code>"
    
    buttons = [
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data="settings"
                ),
            
            InlineKeyboardButton
                (
                    "Close 🔐", callback_data="close"
                )
        ]
    ]
   
    
    await update.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="html")



@DonLee_Robot_V2.on_callback_query(filters.regex(r"about\((.+)\)"), group=2)
async def cb_about(bot, update: CallbackQuery):
    """
    A Callback Funtion For Showing About Section In Bot Setting Menu
    """
    global VERIFY
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    text=f"<b><u>🤖Bot's Status</u></b>\n"
    text+=f"\n🕐Bot's Uptime: <code>{time_formatter(time.time() - start_uptime)}</code>\n"
    text+=f"\nBot Funtion: <b><>Auto Filter & Manual Filters</b>"

    buttons = [[
         InlineKeyboardButton("🔙 Back", callback_data="settings"),
         InlineKeyboardButton("Close 🔐", callback_data="close")
         ]]    
    await update.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="html")



def time_formatter(seconds: float) -> str:
    """ 
    humanize time 
    """
    minutes, seconds = divmod(int(seconds),60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s") if seconds else "")
    return tmp
