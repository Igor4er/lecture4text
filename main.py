import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import importlib
from handlers import handlers_list
from middlewares.outer import outer_middlewares
from dotenv import load_dotenv
from config import CONFIG


load_dotenv()
dp = Dispatcher()


def match(module: str, name: str, obj: str, fn: callable):
    mod = importlib.import_module(f"{module}.{name}")
    return hasattr(mod, obj) and fn(getattr(mod, obj))

def register_handlers(dp: Dispatcher):
    for name in handlers_list:
        handler = match("handlers", name, "router", dp.include_router)
        if not handler:
            raise ModuleNotFoundError(f"router missing in handlers/{name}")

def register_middlewares(dp: Dispatcher):
    def regboth(mw):
        dp.message.outer_middleware(mw())
        dp.callback_query.outer_middleware(mw())
        return True
    for name in outer_middlewares:
        handler = match("middlewares.outer", name, "middleware", regboth)
        if not handler:
            raise ModuleNotFoundError(f"middleware missing: {name}")


async def main() -> None:
    bot = Bot(token=CONFIG.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    register_handlers(dp)
    register_middlewares(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
