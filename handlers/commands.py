from aiogram import Router, F
from aiogram.types import Message, BotCommand
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from dto.user import Permissions, User
from util.auth import need_permissions

router = Router(name=__name__)

@router.message(CommandStart())
# @need_permissions([Permissions.create_audio_prompt])
async def start_bot(message: Message, state: FSMContext, user: User):
    await message.answer("Відправте аудіофайл або голосове повідомлення")