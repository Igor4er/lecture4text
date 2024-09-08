from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from keyboards import inline
from dto.user import Permissions, User
from util.auth import need_permissions
from .keys import router as keys_router


router = Router(name=__name__)
router.include_router(keys_router)



@router.message(Command("settings"))
# @need_permissions([Permissions.create_audio_prompt])
async def show_settings(message: Message, state: FSMContext, user: User):
    await message.answer("⚙️ Налаштування прив'язуються до вашого Telegram аккаунту. Виберіть що хочете змінити", parse_mode="markdown", reply_markup=inline.settings_params)