from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from keyboards import inline
from dto.user import Permissions, User
from util.auth import need_permissions

router = Router(name=__name__)

@router.message(Command("help"))
@router.message(CommandStart())
# @need_permissions([Permissions.create_audio_prompt])
async def start_bot(message: Message, state: FSMContext, user: User):
    T = """
    /settings Вставше ваші ключі від сервісів. Вони зберігають в безпеці під шифром AES-256
    <20Мб: Відправте аудіофайл або голосове повідомлення \n>20Мб: Відправте посилання на аудіофайл
    """.replace("    ", "")
    await message.answer(T, parse_mode="markdown", reply_markup=inline.file_sharing_links)
