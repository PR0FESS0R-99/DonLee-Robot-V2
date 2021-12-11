# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

from pyrogram.types import User
from datetime import datetime


def last_online(from_user: User) -> str:
    time = ""
    if from_user.is_bot:
        time += "🤖 𝖡𝗈𝗍 :("
    elif from_user.status == 'recently':
        time += "𝖱𝖾𝖼𝖾𝗇𝗍𝗅𝗒"
    elif from_user.status == 'within_week':
        time += "𝖶𝗂𝗍𝗁𝗂𝗇 𝗍𝗁𝖾 𝗅𝖺𝗌𝗍 𝗐𝖾𝖾𝗄"
    elif from_user.status == 'within_month':
        time += "𝖶𝗂𝗍𝗁𝗂𝗇 𝗍𝗁𝖾 𝗅𝖺𝗌𝗍 𝗆𝗈𝗇𝗍𝗁"
    elif from_user.status == 'long_time_ago':
        time += "𝖠 𝗅𝗈𝗇𝗀 𝗍𝗂𝗆𝖾 𝖺𝗀𝗈 :("
    elif from_user.status == 'online':
        time += "𝖢𝗎𝗋𝗋𝖾𝗇𝗍𝗅𝗒 𝖮𝗇𝗅𝗂𝗇𝖾"
    elif from_user.status == 'offline':
        time += datetime.fromtimestamp(from_user.last_online_date).strftime("%a, %d %b %Y, %H:%M:%S")
    return time
