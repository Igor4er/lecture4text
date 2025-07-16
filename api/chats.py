from api.mongo import db_session


USERS_CHATS_COLLECTION_NAME = "users_chats"


async def _get_users_chats_collection():
    ses = await db_session()
    return ses[USERS_CHATS_COLLECTION_NAME]


async def update_user_chat(uid: int, text: str):
    us = await _get_users_chats_collection()
    try:
        await us.update_one({"uid": uid}, {"$set": {"text": text}}, upsert=True)
    except Exception as E:
        print(E)
        return False
    return True
