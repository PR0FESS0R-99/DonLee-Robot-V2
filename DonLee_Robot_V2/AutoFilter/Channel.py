# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

import random
import string
import asyncio

from pyrogram import filters, Client as DonLee_Robot_V2
from pyrogram.errors import UserAlreadyParticipant, FloodWait
from DonLee_Robot_V2 import VERIFY, LOGGER, Database, recacher

db = Database()
logger = LOGGER(__name__)

@DonLee_Robot_V2.on_message(filters.command(["addchannel"]) & filters.group, group=1)
async def connect(bot: DonLee_Robot_V2, update):
    """
    A Funtion To Handle Incoming /add Command TO COnnect A Chat With Group
    """
    chat_id = update.chat.id
    user_id = update.from_user.id if update.from_user else None
    target_chat = update.text.split(None, 1)
    global VERIFY
    
    if VERIFY.get(str(chat_id)) == None: # Make Admin's ID List
        admin_list = []
        async for x in bot.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
        admin_list.append(None)
        VERIFY[str(chat_id)] = admin_list

    if not user_id in VERIFY.get(str(chat_id)):
        return
    
    try:
        if target_chat[1].startswith("@"):
            if len(target_chat[1]) < 5:
                await update.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾...!!!")
                return
            target = target_chat[1]
            
        elif not target_chat[1].startswith("@"):
            if len(target_chat[1]) < 14:
                await update.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖢𝗁𝖺𝗍 𝖨𝖽...\n𝖢𝗁𝖺𝗍 𝖨𝖣 𝖲𝗁𝗈𝗎𝗅𝖽 𝖡𝖾 𝖲𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝖫𝗂𝗄𝖾 𝖳𝗁𝗂𝗌: <code>-100xxxxxxxxxx</code>")
                return
            target = int(target_chat[1])
                
    except Exception:
        await update.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖨𝗇𝗉𝗎𝗍...\n𝖸𝗈𝗎 𝖲𝗁𝗈𝗎𝗅𝖽 𝖲𝗉𝖾𝖼𝗂𝖿𝗒 𝖵𝖺𝗅𝗂𝖽 <code>chat_id(-100xxxxxxxxxx)</code> or <code>@username</code>")
        return
    
    # Exports invite link from target channel for user to join
    try:
        join_link = await bot.export_chat_invite_link(target)
        join_link = join_link.replace('+', 'joinchat/')
    except Exception as e:
        logger.exception(e, exc_info=True)
        await update.reply_text(f"Make Sure Im Admin At <code>{target}</code> And Have Permission For <i>Inviting Users via Link</i> And Try Again.....!!!\n\n<i><b>Error Logged:</b></i> <code>{e}</code>", parse_mode='html')
        return
    
    userbot_info = await bot.USER.get_me()
    
    # Joins to targeted chat using above exported invite link
    # If aldready joined, code just pass on to next code
    try:
        await bot.USER.join_chat(join_link)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        logger.exception(e, exc_info=True)
        await update.reply_text(f"{userbot_info.mention} Couldnt Join The Channel <code>{target}</code> Make Sure Userbot Is Not Banned There Or Add It Manually And Try Again....!!\n\n<i><b>Error Logged:</b></i> <code>{e}</code>", parse_mode='html')
        return
    
    try:
        c_chat = await bot.get_chat(target)
        channel_id = c_chat.id
        channel_name = c_chat.title
        
    except Exception as e:
        await update.reply_text("𝖤𝗇𝖼𝗈𝗎𝗇𝗍𝖾𝗋𝖾𝖽 𝖲𝗈𝗆𝖾 𝖨𝗌𝗌𝗎𝖾..𝖯𝗅𝖾𝖺𝗌𝖾 𝖢𝗁𝖾𝖼𝗄 𝖫𝗈𝗀𝗌..!!")
        raise e
        
        
    in_db = await db.in_db(chat_id, channel_id)
    
    if in_db:
        await update.reply_text("𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖠𝗅𝖽𝗋𝖾𝖺𝖽𝗒 𝖨𝗇 𝖣𝖻...!!!")
        return
    
    wait_msg = await update.reply_text("𝖯𝗅𝖾𝖺𝗌𝖾 𝖶𝖺𝗂𝗍 𝖳𝗂𝗅𝗅 𝖨 𝖠𝖽𝖽 𝖠𝗅𝗅 𝖸𝗈𝗎𝗋 𝖥𝗂𝗅𝖾𝗌 𝖥𝗋𝗈𝗆 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖳𝗈 𝖣𝖻\n\n𝖳𝗁𝗂𝗌 𝖬𝖺𝗒 𝖳𝖺𝗄𝖾 10 𝗈𝗋 15 𝖬𝗂𝗇𝗌 𝖣𝖾𝗉𝖾𝗇𝖽𝗂𝗇𝗀 𝖮𝗇 𝖸𝗈𝗎𝗋 𝖭𝗈. 𝖮𝖿 𝖥𝗂𝗅𝖾𝗌 𝖨𝗇 𝖢𝗁𝖺𝗇𝗇𝖾𝗅.....\n\n𝖴𝗇𝗍𝗂𝗅 𝖳𝗁𝖾𝗇 𝖯𝗅𝖾𝖺𝗌𝖾 𝖣𝗈𝗇𝗍 𝖲𝖾𝗇𝗍 𝖠𝗇𝗒 𝖮𝗍𝗁𝖾𝗋 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖮𝗋 𝖳𝗁𝗂𝗌 𝖮𝗉𝖾𝗋𝖺𝗍𝗂𝗈𝗇 𝖬𝖺𝗒 𝖡𝖾 𝖨𝗇𝗍𝗋𝗎𝗉𝗍𝖾𝖽....")
    
    try:
        type_list = ["video", "audio", "document"]
        data = []
        skipCT = 0
        
        for typ in type_list:

            async for msgs in bot.USER.search_messages(channel_id,filter=typ): #Thanks To @PrgOfficial For Suggesting
                
                # Using 'if elif' instead of 'or' to determine 'file_type'
                # Better Way? Make A PR
                try:
                    if msgs.video:
                        try:
                            file_id = await bot.get_messages(channel_id, message_ids=msgs.message_id)
                        except FloodWait as e:
                            asyncio.sleep(e.x)
                            file_id = await bot.get_messages(channel_id, message_ids=msgs.message_id)
                        except Exception as e:
                            print(e)
                            continue
                        file_id = file_id.video.file_id
                        file_name = msgs.video.file_name[0:-4]
                        file_caption  = msgs.caption if msgs.caption else ""
                        file_size = msgs.video.file_size
                        file_type = "video"
                    
                    elif msgs.audio:
                        try:
                            file_id = await bot.get_messages(channel_id, message_ids=msgs.message_id)
                        except FloodWait as e:
                            asyncio.sleep(e.x)
                            file_id = await bot.get_messages(channel_id, message_ids=msgs.message_id)
                        except Exception as e:
                            print(e)
                            continue
                        file_id = file_id.audio.file_id
                        file_name = msgs.audio.file_name[0:-4]
                        file_caption  = msgs.caption if msgs.caption else ""
                        file_size = msgs.audio.file_size
                        file_type = "audio"
                    
                    elif msgs.document:
                        try:
                            file_id = await bot.get_messages(channel_id, message_ids=msgs.message_id)
                        except FloodWait as e:
                            asyncio.sleep(e.x)
                            file_id = await bot.get_messages(channel_id, message_ids=msgs.message_id)
                        except Exception as e:
                            print(str(e))
                            continue
                        file_id = file_id.document.file_id
                        file_name = msgs.document.file_name[0:-4]
                        file_caption  = msgs.caption if msgs.caption else ""
                        file_size = msgs.document.file_size
                        file_type = "document"
                    
                    for i in ["_", "|", "-", "."]: # Work Around
                        try:
                            file_name = file_name.replace(i, " ")
                        except Exception:
                            pass
                    
                    file_link = msgs.link
                    group_id = chat_id
                    unique_id = ''.join(
                        random.choice(
                            string.ascii_lowercase + 
                            string.ascii_uppercase + 
                            string.digits
                        ) for _ in range(15)
                    )
                    
                    dicted = dict(
                        file_id=file_id, # Done
                        unique_id=unique_id,
                        file_name=file_name,
                        file_caption=file_caption,
                        file_size=file_size,
                        file_type=file_type,
                        file_link=file_link,
                        chat_id=channel_id,
                        group_id=group_id,
                    )
                    
                    data.append(dicted)
                except Exception as e:
                    if 'NoneType' in str(e): # For Some Unknown Reason Some File Names are NoneType
                        skipCT +=1
                        continue
                    print(e)

        print(f"{skipCT} Files Been Skipped Due To File Name Been None..... #BlameTG")
    except Exception as e:
        await wait_msg.edit_text("Couldnt Fetch Files From Channel... Please look Into Logs For More Details")
        raise e
    
    await db.add_filters(data)
    await db.add_chat(chat_id, channel_id, channel_name)
    await recacher(chat_id, True, True, bot, update)
    
    await wait_msg.edit_text(f"Channel Was Sucessfully Added With <code>{len(data)}</code> Files..")


@DonLee_Robot_V2.on_message(filters.command(["delchannel"]) & filters.group, group=1)
async def disconnect(bot: DonLee_Robot_V2, update):
    """
    A Funtion To Handle Incoming /del Command TO Disconnect A Chat With A Group
    """
    chat_id = update.chat.id
    user_id = update.from_user.id if update.from_user else None
    target_chat = update.text.split(None, 1)
    global VERIFY
    
    if VERIFY.get(str(chat_id)) == None: # Make Admin's ID List
        admin_list = []
        async for x in bot.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
        admin_list.append(None)
        VERIFY[str(chat_id)] = admin_list

    if not user_id in VERIFY.get(str(chat_id)):
        return
    
    try:
        if target_chat[1].startswith("@"):
            if len(target_chat[1]) < 5:
                await update.reply_text("Invalid Username...!!!")
                return
            target = target_chat[1]
            
        elif not target_chat.startswith("@"):
            if len(target_chat[1]) < 14:
                await update.reply_text("Invalid Chat Id...\nChat ID Should Be Something Like This: <code>-100xxxxxxxxxx</code>")
                return
            target = int(target_chat[1])
                
    except Exception:
        await update.reply_text("Invalid Input...\nYou Should Specify Valid chat_id(-100xxxxxxxxxx) or @username")
        return
    
    userbot = await bot.USER.get_me()
    userbot_name = userbot.first_name
    userbot_id = userbot.id
    
    try:
        channel_info = await bot.USER.get_chat(target)
        channel_id = channel_info.id
    except Exception:
        await update.reply_text(f"My UserBot [{userbot_name}](tg://user?id={userbot_id}) Couldnt Fetch Details Of `{target}` Make Sure Userbot Is Not Banned There Or Add It Manually And Try Again....!!")
        return
    
    in_db = await db.in_db(chat_id, channel_id)
    
    if not in_db:
        await update.reply_text("This Channel Is Not Connected With The Group...")
        return
    
    wait_msg = await update.reply_text("Deleting All Files Of This Channel From DB....!!!\n\nPlease Be Patience...Dont Sent Another Command Until This Process Finishes..")
    
    await db.del_filters(chat_id, channel_id)
    await db.del_active(chat_id, channel_id)
    await db.del_chat(chat_id, channel_id)
    await recacher(chat_id, True, True, bot, update)
    
    await wait_msg.edit_text("Sucessfully Deleted All Files From DB....")


@DonLee_Robot_V2.on_message(filters.command(["delallchannel"]) & filters.group, group=1)
async def delall(bot: DonLee_Robot_V2, update):
    """
    A Funtion To Handle Incoming /delall Command TO Disconnect All Chats From A Group
    """
    chat_id=update.chat.id
    user_id = update.from_user.id if update.from_user else None
    global VERIFY
    
    if VERIFY.get(str(chat_id)) == None: # Make Admin's ID List
        admin_list = []
        async for x in bot.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
        admin_list.append(None)
        VERIFY[str(chat_id)] = admin_list

    if not user_id in VERIFY.get(str(chat_id)):
        return
    
    await db.delete_all(chat_id)
    await recacher(chat_id, True, True, bot, update)
    
    await update.reply_text("Sucessfully Deleted All Connected Chats From This Group....")


@DonLee_Robot_V2.on_message(filters.channel & (filters.video | filters.audio | filters.document) & ~filters.edited, group=0)
async def new_files(bot: DonLee_Robot_V2, update):
    """
    A Funtion To Handle Incoming New Files In A Channel ANd Add Them To Respective Channels..
    """
    channel_id = update.chat.id
    
    # Using 'if elif' instead of 'or' to determine 'file_type'
    # Better Way? Make A PR
    
    try:
        if update.video: 
            file_type = "video" 
            file_id = update.video.file_id
            file_name = update.video.file_name[0:-4]
            file_caption  = update.caption if update.caption else ""
            file_size = update.video.file_size

        elif update.audio:
            file_type = "audio"
            file_id = update.audio.file_id
            file_name = update.audio.file_name[0:-4]
            file_caption  = update.caption if update.caption else ""
            file_size = update.audio.file_size

        elif update.document:
            file_type = "document"
            file_id = update.document.file_id
            file_name = update.document.file_name[0:-4]
            file_caption  = update.caption if update.caption else ""
            file_size = update.document.file_size

        for i in ["_", "|", "-", "."]: # Work Around
            try:
                file_name = file_name.replace(i, " ")
            except Exception:
                pass
    except Exception as e:
        print(e)
        return
        
    
    file_link = update.link
    group_ids = await db.find_group_id(channel_id)
    unique_id = ''.join(
        random.choice(
            string.ascii_lowercase + 
            string.ascii_uppercase + 
            string.digits
        ) for _ in range(15)
    )
    
    data = []
    
    if group_ids:
        for group_id in group_ids:
            data_packets = dict(
                    file_id=file_id, # File Id For Future Updates Maybe...
                    unique_id=unique_id,
                    file_name=file_name,
                    file_caption=file_caption,
                    file_size = file_size,
                    file_type=file_type,
                    file_link=file_link,
                    chat_id=channel_id,
                    group_id=group_id,
                )
            
            data.append(data_packets)
        await db.add_filters(data)
    return

