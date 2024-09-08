from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from dto.user import UserSettings


async def make_settings_params_kb(settings: UserSettings):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{'✅' if settings.has_deepgram_key() else '❌'} Deepgram API Ключ", callback_data="settings:keys:deepgram_key")
            ],
            [
                InlineKeyboardButton(text=f"{'✅' if settings.has_openai_key() else '❌'} OpenAI API Ключ", callback_data="settings:keys:openai_key")
            ],
            [
                InlineKeyboardButton(text=f"{'✅' if settings.has_gist_key() else '❌'} Gist API Ключ", callback_data="settings:keys:gist_key")
            ]
        ]
    )

