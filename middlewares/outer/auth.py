from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
import jwt
from api.auth import authenticate_user, logout_user
from api.auth import get_user
from config import CONFIG
from dto.user import User


class CounterMiddleware(BaseMiddleware):
    A_MSG = "🔓 Authenticate using /start command\nUsage: <code>/start ACCESS_KEY</code>"
    Q_MSG = "😔 I will miss you"
    E_MSG = "🤡"
    K_MSG = "❇️ lecture4text made by @ig4er"

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        uid = event.from_user.id
        message = event
        if isinstance(event, CallbackQuery):
            message = event.message
        message_text = message.text
        user = await get_user(uid)
        if isinstance(user, User):
            if message_text in ("/quit", "/stop"):
                await logout_user(uid)
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
                print(E)
                return await message.answer(self.E_MSG)

            await message.answer(self.K_MSG)
            return await authenticate_user(u, uid)
        await message.answer(self.A_MSG)
        
        
    
middleware = CounterMiddleware
