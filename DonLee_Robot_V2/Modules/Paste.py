# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

import os
import re
import json
import aiohttp
import requests
from pyrogram import filters, Client as DonLee_Robot_V2

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "content-type": "application/json",
}

async def p_paste(message, extension=None):
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        purl = (
            f"https://pasty.lus.pm/{response['id']}.{extension}"
            if extension
            else f"https://pasty.lus.pm/{response['id']}.txt"
        )
        return {
            "url": purl,
            "raw": f"https://pasty.lus.pm/{response['id']}/raw",
            "bin": "Pasty",
        }
    return {"error": "Unable to reach pasty.lus.pm"}

@DonLee_Robot_V2.on_message(filters.command(["paste"]))
async def pasty(client, message):
    pablo = await message.reply_text("`𝖯𝗅𝖾𝖺𝗌𝖾 𝗐𝖺𝗂𝗍...`")
    tex_t = message.text
    message_s = tex_t
    if not tex_t:
        if not message.reply_to_message:
            await pablo.edit("`𝖮𝗇𝗅𝗒 𝗍𝖾𝗑𝗍 𝖺𝗇𝖽 𝖽𝗈𝖼𝗎𝗆𝖾𝗇𝗍𝗌 𝖺𝗋𝖾 𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽.`")
            return
        if not message.reply_to_message.text:
            file = await message.reply_to_message.download()
            m_list = open(file, "r").read()
            message_s = m_list
            os.remove(file)
        elif message.reply_to_message.text:
            message_s = message.reply_to_message.text
    
    ext = "py"
    x = await p_paste(message_s, ext)
    p_link = x["url"]
    p_raw = x["raw"]
    
    pasted = f"""𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖯𝖺𝗌𝗍𝖾 𝗍𝗈 𝖯𝖺𝗌𝗍𝗒\n\n Link:- <a href=f"{p_link}">𝖢𝗅𝗂𝖼𝗄 𝖧𝖾𝗋𝖾</a>\n\nRaw Link:- <a href=f"{p_raw}">𝖢𝗅𝗂𝖼𝗄 𝖧𝖾𝗋𝖾</a>"""
    await pablo.edit(pasted, disable_web_page_preview=True)
