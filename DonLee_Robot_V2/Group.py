# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

import re
import logging
import asyncio
import urllib.request
from pyrogram import filters, Client as DonLee_Robot_V2
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid, FloodWait
from DonLee_Robot_V2.Database import Database, donlee_imdb, add_filter, find_filter, get_filters, delete_filter, count_filters, active_connection, add_user, all_users,  parser, split_quotes, IMDBCONTROL, google_search 
from DonLee_Robot_V2.Config_Vars.Vars import Config
from DonLee_Robot_V2.Translation import Text
FIND = {}
INVITE_LINK = {}
ACTIVE_CHATS = {}

db = Database()

@DonLee_Robot_V2.on_message(filters.command("addfilter"))
async def addfilter(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type
    args = message.text.html.split(None, 1)
    if chat_type == "private":
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝖨'𝗆 𝗉𝗋𝖾𝗌𝖾𝗇𝗍 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉!!", quote=True)
                return
        else:
            await message.reply_text("𝖨'𝗆 𝗇𝗈𝗍 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗍𝗈 𝖺𝗇𝗒 𝗀𝗋𝗈𝗎𝗉𝗌!", quote=True)
            return
    elif (chat_type == "group") or (chat_type == "supergroup"):
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return
    st = await client.get_chat_member(grp_id, userid)
    if not ((st.status == "administrator") or (st.status == "creator") or (str(userid) in Config.DEV_ID)):
        return
    if len(args) < 2:
        await message.reply_text("https://youtu.be/neJ4jHC9Hng", quote=True)
        return    
    extracted = split_quotes(args[1])
    text = extracted[0].lower()   
    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("𝖠𝖽𝖽 𝗌𝗈𝗆𝖾 𝖼𝗈𝗇𝗍𝖾𝗇𝗍 𝗍𝗈 𝗌𝖺𝗏𝖾 𝗒𝗈𝗎𝗋 𝖿𝗂𝗅𝗍𝖾𝗋!", quote=True)
        return
    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = parser(extracted[1], text)
        fileid = None
        if not reply_text:
            await message.reply_text("𝖸𝗈𝗎 𝖼𝖺𝗇𝗇𝗈𝗍 𝗁𝖺𝗏𝖾 𝖻𝗎𝗍𝗍𝗈𝗇𝗌 𝖺𝗅𝗈𝗇𝖾, 𝗀𝗂𝗏𝖾 𝗌𝗈𝗆𝖾 𝗍𝖾𝗑𝗍 𝗍𝗈 𝗀𝗈 𝗐𝗂𝗍𝗁 𝗂𝗍!", quote=True)
            return
    elif message.reply_to_message and message.reply_to_message.reply_markup:
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            msg = message.reply_to_message.document or\
                  message.reply_to_message.video or\
                  message.reply_to_message.photo or\
                  message.reply_to_message.audio or\
                  message.reply_to_message.animation or\
                  message.reply_to_message.sticker
            if msg:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            else:
                reply_text = message.reply_to_message.text.html
                fileid = None
            alert = None
        except:
            reply_text = ""
            btn = "[]" 
            fileid = None
            alert = None
    elif message.reply_to_message and message.reply_to_message.photo:
        try:
            fileid = message.reply_to_message.photo.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.video:
        try:
            fileid = message.reply_to_message.video.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.audio:
        try:
            fileid = message.reply_to_message.audio.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None   
    elif message.reply_to_message and message.reply_to_message.document:
        try:
            fileid = message.reply_to_message.document.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.animation:
        try:
            fileid = message.reply_to_message.animation.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.sticker:
        try:
            fileid = message.reply_to_message.sticker.file_id
            reply_text, btn, alert =  parser(extracted[1], text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = parser(message.reply_to_message.text.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    else:
        return    
    await add_filter(grp_id, text, reply_text, btn, fileid, alert)
    await message.reply_text(
        f"`{text}` 𝖠𝖽𝖽𝖾𝖽 𝗂𝗇  **{title}**",
        quote=True,
        parse_mode="md"
    )


@DonLee_Robot_V2.on_message(filters.command('filters'))
async def get_all(client, message):    
    chat_type = message.chat.type
    if chat_type == "private":
        userid = message.from_user.id
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝖨'𝗆 𝗉𝗋𝖾𝗌𝖾𝗇𝗍 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉!!", quote=True)
                return
        else:
            await message.reply_text("𝖨'𝗆 𝗇𝗈𝗍 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗍𝗈 𝖺𝗇𝗒 𝗀𝗋𝗈𝗎𝗉𝗌!", quote=True)
            return
    elif (chat_type == "group") or (chat_type == "supergroup"):
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    st = await client.get_chat_member(grp_id, userid)
    if not ((st.status == "administrator") or (st.status == "creator") or (str(userid) in Config.AUTH_USERS)):
        return
    texts = await get_filters(grp_id)
    count = await count_filters(grp_id)
    if count:
        filterlist = f"𝖳𝗈𝗍𝖺𝗅 𝗇𝗎𝗆𝖻𝖾𝗋 𝗈𝖿 𝖿𝗂𝗅𝗍𝖾𝗋𝗌 𝗂𝗇 **{title}** : {count}"
        for text in texts:
            keywords = "  • `{}`\n".format(text)            
            filterlist += keywords
        if len(filterlist) > 4096:
            with io.BytesIO(str.encode(filterlist.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await message.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        filterlist = f"𝖳𝗁𝖾𝗋𝖾 𝖺𝗋𝖾 𝗇𝗈 𝖺𝖼𝗍𝗂𝗏𝖾 𝖿𝗂𝗅𝗍𝖾𝗋𝗌 𝗂𝗇 **{title}**"
    await message.reply_text(
        text=filterlist,
        quote=True,
        parse_mode="md"
    )
        
@DonLee_Robot_V2.on_message(filters.command("delfilter"))
async def deletefilter(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type

    if chat_type == "private":
        grpid  = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝖨'𝗆 𝗉𝗋𝖾𝗌𝖾𝗇𝗍 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉!!", quote=True)
                return
        else:
            await message.reply_text("𝖨'𝗆 𝗇𝗈𝗍 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗍𝗈 𝖺𝗇𝗒 𝗀𝗋𝗈𝗎𝗉𝗌!", quote=True)

    elif (chat_type == "group") or (chat_type == "supergroup"):
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if not ((st.status == "administrator") or (st.status == "creator") or (str(userid) in Config.AUTH_USERS)):
        return

    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "𝖬𝖾𝗇𝗍𝗂𝗈𝗇 𝗍𝗁𝖾 𝖿𝗂𝗅𝗍𝖾𝗋𝗇𝖺𝗆𝖾 𝗐𝗁𝗂𝖼𝗁 𝗒𝗈𝗎 𝗐𝖺𝗇𝗇𝖺 𝖽𝖾𝗅𝖾𝗍𝖾!\n\n"
            "<code>/delfilter 𝖿𝗂𝗅𝗍𝖾𝗋𝗇𝖺𝗆𝖾</code>\n\n"
            "𝖴𝗌𝖾 /filters 𝗍𝗈 𝗏𝗂𝖾𝗐 𝖺𝗅𝗅 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝖿𝗂𝗅𝗍𝖾𝗋𝗌",
            quote=True
        )
        return

    query = text.lower()

    await delete_filter(message, query, grp_id)
    
@DonLee_Robot_V2.on_message(filters.command("delallfilters"))
async def delallconfirm(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type

    if chat_type == "private":
        grpid  = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝖨'𝗆 𝗉𝗋𝖾𝗌𝖾𝗇𝗍 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉!!", quote=True)
                return
        else:
            await message.reply_text("𝖨'𝗆 𝗇𝗈𝗍 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗍𝗈 𝖺𝗇𝗒 𝗀𝗋𝗈𝗎𝗉𝗌!", quote=True)
            return

    elif (chat_type == "group") or (chat_type == "supergroup"):
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (st.status == "creator") or (str(userid) in Config.AUTH_USERS):
        await message.reply_text(
            f"This will delete all filters from '{title}'.\nDo you want to continue??",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="✅️ 𝖸𝖾𝗌",callback_data="delallconfirm"),
                 InlineKeyboardButton(text="❎️ 𝖢𝗅𝗈𝗌𝖾",callback_data="delallcancel")]
            ]),
            quote=True
        )

@DonLee_Robot_V2.on_message(filters.text & filters.group & ~filters.media & ~filters.forwarded & ~filters.via_bot & ~filters.channel)
async def auto_filter(bot, update):

    group_id = update.chat.id
    the_query = update.text
    query = re.sub(r"[1-2]\d{3}", "", update.text) 
    tester = 2
   
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, the_query, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await update.reply_text(reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await update.reply_text(
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                    else:
                        if btn == "[]":
                            await update.reply_cached_media(
                                fileid,
                                caption=reply_text or ""
                            )
                        else:
                            button = eval(btn) 
                            await update.reply_cached_media(
                                fileid,
                                caption=reply_text or "",
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                except Exception as e:
                    print(e)
                    pass
                break 
                
    if Config.SAVE_USER == "yes":
        try:
            await add_user(
                str(update.from_user.id),
                str(update.from_user.username),
                str(update.from_user.first_name + " " + (message.from_user.last_name or "")),
                str(update.from_user.dc_id)
            )
        except:
            pass


    if re.findall(r"((^\/|^,|^\.|^[\U0001F600-\U000E007F]).*)", update.text):
        return

    for a in "https:// http:// thanks thank tnx tnq tq tqsm #".split():
      if a in update.text.lower():
          return
    
    if len(query) < 2:
        return
                  
    results = []
    
    global ACTIVE_CHATS
    global FIND
    
    configs = await db.find_chat(group_id)
    achats = ACTIVE_CHATS[str(group_id)] if ACTIVE_CHATS.get(str(group_id)) else await db.find_active(group_id)
    ACTIVE_CHATS[str(group_id)] = achats
    
    if not configs:
        return
    
    allow_video = configs["types"]["video"]
    allow_audio = configs["types"]["audio"] 
    allow_document = configs["types"]["document"]
    
    max_pages = configs["configs"]["max_pages"] # maximum page result of a query
    pm_file_chat = configs["configs"]["pm_fchat"] # should file to be send from bot pm to user
    max_results = configs["configs"]["max_results"] # maximum total result of a query
    max_per_page = configs["configs"]["max_per_page"] # maximum buttom per page 
    show_invite = configs["configs"]["show_invite_link"] # should or not show active chat invite link
    
    show_invite = (False if pm_file_chat == True else show_invite) # turn show_invite to False if pm_file_chat is True
    
    filters = await db.get_filters(group_id, query)
    
    if filters:
        for filter in filters: # iterating through each files
            file_name = filter.get("file_name")
            file_type = filter.get("file_type")
            file_link = filter.get("file_link")
            file_size = int(filter.get("file_size", "0"))
            
            # from B to MiB
            
            if file_size < 1024:
                file_size = f"[{file_size} B]"
            elif file_size < (1024**2):
                file_size = f" {str(round(file_size/1024, 2))} 𝖪𝖡 "
            elif file_size < (1024**3):
                file_size = f" {str(round(file_size/(1024**2), 2))} 𝖬𝖡 "
            elif file_size < (1024**4):
                file_size = f"{str(round(file_size/(1024**3), 2))} 𝖦𝖡 "
            
            
            file_size = "" if file_size == ("[0 B]") else file_size
                     
            if file_type == "video":
                if allow_video: 
                    pass
                else:
                    continue
                
            elif file_type == "audio":
                if allow_audio:
                    pass
                else:
                    continue
                
            elif file_type == "document":
                if allow_document:
                    pass
                else:
                    continue
            
            if len(results) >= max_results:
                break
            
            if pm_file_chat: 
                unique_id = filter.get("unique_id")
                if not FIND.get("bot_details"):
                    try:
                        bot_= await bot.get_me()
                        FIND["bot_details"] = bot_
                    except FloodWait as e:
                        asyncio.sleep(e.x)
                        bot_= await bot.get_me()
                        FIND["bot_details"] = bot_
               

                bot_ = FIND.get("bot_details")
                file_link = f"https://t.me/{bot_.username}?start={unique_id}"
            if Config.BUTTON_MODE == "single":
               button_text = f"{file_size} || {file_name}"
               results.append(

                [

                    InlineKeyboardButton(button_text, url=file_link)

                ]

            )
            else:
               results.append(
                [
                    InlineKeyboardButton(f"{file_name}", url=file_link),
                    InlineKeyboardButton(f"{file_size}", url=file_link)
                ]
            )
              
           
        
    else: #return if no files found for that query
        Auto_Delete=await bot.send_message(
            chat_id = update.chat.id,
            text=Text.SPELLING_TEXT.format(update.from_user.mention, the_query, the_query),
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔍 Search Google 🔎", url="https://google.com/")]]),
            reply_to_message_id=update.message_id
        )
        await asyncio.sleep(60) # in seconds
        await Auto_Delete.delete()
        return
    
    if len(results) == 0: # double check
        return
    
    else:
    
        result = []
        # seperating total files into chunks to make as seperate pages
        result += [results[i * max_per_page :(i + 1) * max_per_page ] for i in range((len(results) + max_per_page - 1) // max_per_page )]
        len_result = len(result)
        len_results = len(results)
        results = None # Free Up Memory
        
        FIND[query] = {"results": result, "total_len": len_results, "max_pages": max_pages} # TrojanzHex's Idea Of Dicts😅

        # Add next buttin if page count is not equal to 1
        if len_result != 1:
            result[0].append(
                [
                    InlineKeyboardButton("𝖭𝖾𝗑𝗍 »»", callback_data=f"navigate(0|next|{query})"),
                    InlineKeyboardButton(f"🧾 1/{len_result if len_result < max_pages else max_pages}", callback_data="ignore"),
                ]
            )

            
            
        
        
        # if show_invite is True Append invite link buttons
        if show_invite:
            
            ibuttons = []
            achatId = []
            await gen_invite_links(configs, group_id, bot, update)
            
            for x in achats["chats"] if isinstance(achats, dict) else achats:
                achatId.append(int(x["chat_id"])) if isinstance(x, dict) else achatId.append(x)

            ACTIVE_CHATS[str(group_id)] = achatId
            
            for y in INVITE_LINK.get(str(group_id)):
                
                chat_id = int(y["chat_id"])
                
                if chat_id not in achatId:
                    continue
                
                chat_name = y["chat_name"]
                invite_link = y["invite_link"]
                
                if ((len(ibuttons)%2) == 0):
                    ibuttons.append(
                        [
                            InlineKeyboardButton(f"⚜ {chat_name} ⚜", url=invite_link)
                        ]
                    )

                else:
                    ibuttons[-1].append(
                        InlineKeyboardButton(f"⚜ {chat_name} ⚜", url=invite_link)
                    )
                
            for x in ibuttons:
                result[0].insert(0, x) #Insert invite link buttons at first of page
                
            ibuttons = None # Free Up Memory...
            achatId = None

        reply_markup = InlineKeyboardMarkup(result[0])

        year = 2021
        for i in the_query.split():
            try :
                year = int(i)
                the_query = the_query.replace(i,"")
            except :
                pass
        for i in "movie malayalam english tamil kannada telugu subtitles esub esubs".split():
            if i in the_query.lower().split():
                the_query = the_query.replace(i,"")

        try:
            ia = IMDBCONTROL
            my_movie=the_query
            movies = ia.search_movie(my_movie)
            #print(f"{movies[0].movieID} {movies[0]['title']}")
            movie_url = movies[0].get_fullsizeURL()
            imdb = await donlee_imdb(the_query)
            await bot.send_photo(
                photo=movie_url,
                caption=f"""
↪️ 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖬𝗈𝗏𝗂𝖾: {query}
🎞️ 𝖳𝗂𝗍𝗅𝖾: <a href={imdb['url']}>{imdb.get('title')}
🎭 𝖦𝖾𝗇𝗋𝖾𝗌: {imdb.get('genres')}
📆 𝖸𝖾𝖺𝗋: <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>
🌟 𝖱𝖺𝗍𝗂𝗇𝗀: <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10
🗃️ 𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝖾𝗌 : {(len_results)}
📑 𝖳𝗈𝗍𝖺𝗅 𝖯𝖺𝗀𝖾 : 1/{len_result if len_result < max_pages else max_pages}
👤 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖡𝗒 : {update.from_user.mention}
🖋 𝖲𝗍𝗈𝗋𝗒𝗅𝗂𝗇𝖾: <code>{imdb.get('plot')}</code>
☑️ 𝖢𝗁𝖺𝗍 : {update.chat.title}""",
                reply_markup=reply_markup,
                chat_id=update.chat.id,
                reply_to_message_id=update.message_id,
                parse_mode="html"
            )

        except Exception as e:
          print(e)

          try:
              await bot.send_message(
                chat_id = update.chat.id,
                text=f"""
↪️ 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖬𝗈𝗏𝗂𝖾: {query}
🗃️ 𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝖾𝗌 : {(len_results)}
📑 𝖳𝗈𝗍𝖺𝗅 𝖯𝖺𝗀𝖾 : 1/{len_result if len_result < max_pages else max_pages}
👤 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖡𝗒 : {update.from_user.mention}
☑️ 𝖢𝗁𝖺𝗍 : {update.chat.title}
""",
                reply_markup=reply_markup,
                parse_mode="html",
                reply_to_message_id=update.message_id
            )

          except ButtonDataInvalid:
              print(result[0])

        
async def gen_invite_links(db, group_id, bot, update):
    """
    A Funtion To Generate Invite Links For All Active 
    Connected Chats In A Group
    """
    chats = db.get("chat_ids")
    global INVITE_LINK
    
    if INVITE_LINK.get(str(group_id)):
        return
    
    Links = []
    if chats:
        for x in chats:
            Name = x["chat_name"]
            
            if Name == None:
                continue
            
            chatId=int(x["chat_id"])
            
            Link = await bot.export_chat_invite_link(chatId)
            Links.append({"chat_id": chatId, "chat_name": Name, "invite_link": Link})

        INVITE_LINK[str(group_id)] = Links
    return 


async def recacher(group_id, ReCacheInvite=True, ReCacheActive=False, bot=DonLee_Robot_V2, update=Message):
    """
    A Funtion To rechase invite links and active chats of a specific chat
    """
    global INVITE_LINK, ACTIVE_CHATS

    if ReCacheInvite:
        if INVITE_LINK.get(str(group_id)):
            INVITE_LINK.pop(str(group_id))
        
        Links = []
        chats = await db.find_chat(group_id)
        chats = chats["chat_ids"]
        
        if chats:
            for x in chats:
                Name = x["chat_name"]
                chat_id = x["chat_id"]
                if (Name == None or chat_id == None):
                    continue
                
                chat_id = int(chat_id)
                
                Link = await bot.export_chat_invite_link(chat_id)
                Links.append({"chat_id": chat_id, "chat_name": Name, "invite_link": Link})

            INVITE_LINK[str(group_id)] = Links
    
    if ReCacheActive:
        
        if ACTIVE_CHATS.get(str(group_id)):
            ACTIVE_CHATS.pop(str(group_id))
        
        achats = await db.find_active(group_id)
        achatId = []
        if achats:
            for x in achats["chats"]:
                achatId.append(int(x["chat_id"]))
            
            ACTIVE_CHATS[str(group_id)] = achatId
    return
