from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from keyboards import inline, dynamic
from dto.user import Permissions, User
from util.auth import need_permissions
from util.states import UpdateAPIKey


router = Router(name=__name__)


@router.callback_query(F.data == "settings:keys")
async def setup_api_keys(event: CallbackQuery, state: FSMContext, user: User):
    await event.message.edit_text("⚙️ Налаштування API ключів", parse_mode="markdown", reply_markup=await dynamic.make_settings_params_kb(await user.get_settings()))


@router.callback_query(F.data == "settings:keys:deepgram_key")
@need_permissions([Permissions.change_settings])
async def setup_deepgram_key(event: CallbackQuery, state: FSMContext, user: User):
    await state.set_state(UpdateAPIKey.deepgram)
    msg = await event.message.answer("👉 Відправте новий ключ в чат")
    await state.set_data({"msg": msg})

@router.message(UpdateAPIKey.deepgram, F.text)
async def setup_deepgram_key(message: Message, state: FSMContext, user: User):
    state_data = await state.get_data()
    await state.clear()
    state_data["msg"].delete()
    await message.delete()
    settings = await user.get_settings()
    changed = await settings.update_deepgram_key(message.text)
    if not changed:
        await message.answer("❌ Ключ не було змінено")
    await message.answer("⚙️ Налаштування API ключів", parse_mode="markdown", reply_markup=await dynamic.make_settings_params_kb(await user.get_settings()))
