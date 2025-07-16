from genericpath import exists
from sys import exit
from functools import wraps
from aiogram.types import Message
from dto.user import Permissions
import os
import json


def need_permissions(req: list[Permissions]):
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            user = kwargs["user"]
            if all(req_p in user.permissions for req_p in req):
                return await func(message, *args, **kwargs)
            else:
                return await message.answer("❌ У вас немає прав на виконання цієї дії")
        return wrapper
    return decorator

def get_promos() -> dict:
    FILE_PATH = "promos.json"
    if not os.path.exists(FILE_PATH):
        return {}
    with open("promos.json", "r") as f:
        c = f.read()
        return json.loads(c)
