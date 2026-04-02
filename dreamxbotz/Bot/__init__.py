import logging
import asyncio
import uvloop
from pyrogram import Client, types
from typing import Union, Optional, AsyncGenerator
from info import *

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("uvloop").setLevel(logging.WARNING)

# --- Loop Policy Setup ---
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

class dreamcinezoneXBot(Client):
    def __init__(self):
        # Pass all arguments to the parent Client class
        super().__init__(
            name="dreamxbotz",  # Using a string name for the session
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=min(32, (os.cpu_count() or 1) + 4), # Optimized worker count
            plugins={"root": "plugins"},
            sleep_threshold=15, # Increased threshold to handle FloodWait better
        )
        self.username = None # Will be set on start

    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> AsyncGenerator["types.Message", None]:
        """
        Optimized message iterator for Kurigram/Pyrogram.
        Uses get_messages to fetch chunks based on message IDs.
        """
        current = offset
        while current < limit:
            # Determine how many messages to fetch in this batch (Max 200)
            to_fetch = min(200, limit - current)
            
            # Generate a list of message IDs for this chunk
            ids = [i for i in range(current, current + to_fetch)]
            
            try:
                # get_messages returns a list of messages
                messages = await self.get_messages(chat_id, ids)
                
                for message in messages:
                    yield message
                    current += 1
                    
            except Exception as e:
                logging.error(f"Error in iter_messages: {e}")
                break

# Initialize the single client instance
dreamxbotz = dreamcinezoneXBot()

# For managing multiple user-clients (if needed for your bypass logic)
multi_clients = {}
work_loads = {}
