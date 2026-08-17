import os
from dotenv import load_dotenv

load_dotenv()

TICKET_CATEGORY_ID = int(
    os.getenv("TICKET_CATEGORY_ID", "0")
)

STAFF_ROLE_ID = int(
    os.getenv("STAFF_ROLE_ID", "0")
)

LOG_CHANNEL_ID = int(
    os.getenv("LOG_CHANNEL_ID", "0")
)

DATABASE_FILE = "database/jstore.db"

PURPLE = 0x8B5CF6
DARK_PURPLE = 0x6D28D9
