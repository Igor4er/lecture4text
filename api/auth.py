from api.mongo import db_session
from dto.user import User


from motor.motor_asyncio import AsyncIOMotorDatabase
AUTHENTICATED_USERS_COLLECTION_NAME = "authenticated_users"


async def _get_authenticated_users_collection():
    ses = await db_session()
    return ses[AUTHENTICATED_USERS_COLLECTION_NAME]


async def authenticate_user(user: User, uid: int):
    au = await _get_authenticated_users_collection()
    await au.insert_one({
        **user.model_dump(),
        "uid": uid
    })


async def logout_user(uid: int):
    au = await _get_authenticated_users_collection()
    await au.delete_one({
        "uid": uid
    })


async def get_user(uid: int):
    au = await _get_authenticated_users_collection()
    user = await au.find_one({
        "uid": uid
    })
    if user is None:
        return None
    return User.model_validate(user)
