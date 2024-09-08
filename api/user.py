from api.mongo import db_session


from motor.motor_asyncio import AsyncIOMotorDatabase
USERS_SETTINGS_COLLECTION_NAME = "users_settings"


async def _get_users_settings_collection():
    ses = await db_session()
    return ses[USERS_SETTINGS_COLLECTION_NAME]

async def get_user_settings_dict(uid: int):
    us = await _get_users_settings_collection()
    user = await us.find_one({
        "uid": uid
    })
    if user is None:
        return {"uid": uid}
    return user


async def update_user_settings(settings: dict):
    us = await _get_users_settings_collection()
    try:
        await us.update_one({"uid": settings["uid"]}, {"$set": settings}, upsert=True)
    except Exception as E:
        print(E)
        return False
    return True

