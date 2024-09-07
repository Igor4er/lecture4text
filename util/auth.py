from functools import wraps
from aiogram.types import Message
from dto.user import Permissions


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