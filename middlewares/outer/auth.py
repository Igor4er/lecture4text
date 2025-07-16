from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
import jwt
from api.auth import authenticate_user, logout_user
from api.auth import get_user
from config import CONFIG
from dto.user import User
from util.auth import get_promos

PROMOS = get_promos()
SET_DG_KEY_KEY = "set_dg_key"

class CounterMiddleware(BaseMiddleware):
    A_MSG = "🔓 Authenticate using /start command\nUsage: <code>/start ACCESS_KEY</code>"
    Q_MSG = "😔 I will miss you"
    E_MSG = "🤡"
    K_MSG = "❇️ lecture4text made by @ig4er\nUse /help if you wonder what's next"

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        assert(event.from_user is not None)
        uid = event.from_user.id
        message = event
        if isinstance(event, CallbackQuery):
            message = event.message
        assert(isinstance(message, Message))
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
            if len(token) < 30:
                return await message.answer(self.E_MSG)

            print(token)
            if token.startswith("l4t__"):
                promo_code = token.removeprefix("l4t__")
                if promo_code in PROMOS:
                    promo = PROMOS[promo_code]
                    await message.answer(promo["msg"])
                    user = promo["user"]
                    user.update(for_ids=[uid])
            else:
                try:
                    user = jwt.decode(token, CONFIG.JWT_SECRET.get_secret_value(), algorithms=["HS256"])
                except Exception as E:
                    print(E)
                    return await message.answer(self.E_MSG)
            if not isinstance(user, dict):
                return await message.answer(self.E_MSG)

            for_ids = user.get("for_ids", None)
            if isinstance(for_ids, list):
                if uid not in for_ids:
                    return await message.answer(self.E_MSG)

            try:
                u = User.model_validate({**user, "uid": uid})
                if SET_DG_KEY_KEY in user:
                    s = await u.get_settings()
                    await s.update_deepgram_key(user[SET_DG_KEY_KEY])
            except Exception as E:
                print(E)
                return await message.answer(self.E_MSG)

            await message.answer(self.K_MSG)
            return await authenticate_user(u, uid)
        await message.answer(self.A_MSG)



middleware = CounterMiddleware
