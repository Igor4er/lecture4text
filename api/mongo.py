import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import pytz
from config import CONFIG
from datetime import datetime, timezone


CLIENT = AsyncIOMotorClient(CONFIG.MONGO_CONN.get_secret_value(), server_api=ServerApi('1'))

async def db_session():
    return CLIENT.get_database("l4t")
    # async with await CLIENT.start_session() as session:
    #     db = session.client.get_database("l4t")
    #     return db


