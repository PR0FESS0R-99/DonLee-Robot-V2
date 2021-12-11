# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

from pyrogram import Client, __version__
from DonLee_Robot_V2 import LOGGER, Config

class User(Client):
    def __init__(self):
        super().__init__(
            Config.USER_SESSION,
            api_hash=Config.API_HASH,
            api_id=Config.API_ID,
            workers=4
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        return (self, usr_bot_me.id)
