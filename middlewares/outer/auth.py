from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
import jwt
from config import CONFIG
from dto.user import User


class CounterMiddleware(BaseMiddleware):
    A_MSG = "🔓 Authenticate using /start command\nUsage: <code>/start ACCESS_KEY</code>"
    Q_MSG = "😔 I will miss you"
    E_MSG = "🤡"
    K_MSG = "❇️ lecture4text made by @ig4er"

    def __init__(self) -> None:
        self.AUTHENTICATED_USERS: dict[int, User] = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        uid = event.from_user.id
        message = event
        message_text = message.text
        user = self.AUTHENTICATED_USERS.get(uid, None)
        if isinstance(user, User):
            if message_text in ("/quit", "/stop"):
                del self.AUTHENTICATED_USERS[uid]
                return await message.answer(self.Q_MSG)
            data.update({"user": user})
            return await handler(event, data)
        elif len(message_text) > 0 and message_text.startswith("/start") and user is None:
            mts = message_text.split()
            if len(mts) != 2:
                return await message.answer(self.A_MSG)
            token = mts[1]
            if len(token) < 100:
                return await message.answer(self.E_MSG)
            try:
                user = jwt.decode(token, CONFIG.JWT_SECRET.get_secret_value(), algorithms=["HS256"])
            except:
                return await message.answer(self.E_MSG)
            
            for_ids = user.get("for_ids", None)
            if isinstance(for_ids, list):
                if uid not in for_ids:
                    return await message.answer(self.E_MSG)

            try:
                u = User.model_validate(user)
            except Exception as E:
                return await message.answer(self.E_MSG)

            await message.answer(self.K_MSG)
            return self.AUTHENTICATED_USERS.update({uid: u})
        await message.answer(self.A_MSG)
        
        
    
middleware = CounterMiddleware
