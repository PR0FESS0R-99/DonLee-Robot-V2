import pyromod.listen
from pyrogram import Client, __version__
from pyrogram.raw.all import layer 
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

class DonLee_Robot(Client):
    USER: User = None
    USER_ID: int = None

    def __init__(self):
        super().__init__(
            "bot",
            api_hash=Config.API_HASH,
            api_id=Config.API_ID,
            plugins={
                "root": "DonLee_Robot_V2"
            },
            workers=200,
            bot_token=Config.BOT_TOKEN,
            sleep_threshold=10
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        bot_details = await self.get_me()
        self.set_parse_mode("html")
        self.LOGGER(__name__).info(
            f"@{bot_details.username}  started! "
        )
        self.USER, self.USER_ID = await User().start()

app = DonLee_Robot()
app.run()
