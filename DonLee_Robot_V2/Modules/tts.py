# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

import traceback
from asyncio import get_running_loop
from io import BytesIO
from googletrans import Translator
from gtts import gTTS
from pyrogram import filters, Client as DonLee_Robot_V2
from DonLee_Robot_V2 import Import

def convert_en(text):
    audio = BytesIO()
    i = Translator().translate(text, dest="en")
    lang = i.src
    tts = gTTS(text, lang=lang)
    audio.name = lang + ".mp3"
    tts.write_to_fp(audio)
    return audio


@DonLee_Robot_V2.on_message(filters.command("tts"))
async def text_to_speech_en(_, message: Import.Msg):
    if not message.reply_to_message:
        return await message.reply_text("𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝗌𝗈𝗆𝖾 𝗍𝖾𝗑𝗍 𝖿𝖿𝗌.")
    if not message.reply_to_message.text:
        return await message.reply_text("𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝗌𝗈𝗆𝖾 𝗍𝖾𝗑𝗍 𝖿𝖿𝗌.")
    m = await message.reply_text("𝖯𝗋𝗈𝖼𝖾𝗌𝗌𝗂𝗇𝗀")
    text = message.reply_to_message.text
    try:
        loop = get_running_loop()
        audio = await loop.run_in_executor(None, convert_en, text)
        await message.reply_audio(audio)
        await m.delete()
        audio.close()
    except Exception as e:
        await m.edit(e)
        e = traceback.format_exc()
        print(e)
