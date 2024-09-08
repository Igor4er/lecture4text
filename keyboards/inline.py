from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


file_sharing_links = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="File.io", url="https://www.file.io/me/")
        ]
    ]
)



settings_params = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="API Ключі", callback_data="settings:keys")
        ],
        [
            InlineKeyboardButton(text="settings:default_prcoessor", callback_data="settings:default_prcoessor")
        ],
    ]
)

