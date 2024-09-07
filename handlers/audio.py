from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from io import BytesIO

from api.deepgram import get_words_from_file_bytes
from dto.user import Permissions, User
from util.auth import need_permissions


router = Router(name=__name__)

@router.message(F.voice)
@router.message(F.audio)
@need_permissions([Permissions.create_audio_prompt])
async def start_audio_prompt(message: Message, state: FSMContext, user: User):
    data = BytesIO()
    if message.voice is not None:
        await message.bot.download(message.voice, data)
    elif message.audio is not None:
        if not message.audio.mime_type.startswith("audio"):
            return await message.answer("❌ Цей файл не підтрмауються. Підтримувані розширення: <code>MP3, WAV, FLAC, Ogg, Opus</code>")
        await message.bot.download(message.audio, data)
    voice = data.read()
    resp = await get_words_from_file_bytes(voice)
    text = resp["results"]["channels"][0]["alternatives"][0]['transcript']
    print(text)
    def split_long_string(text, max_length=4000):
        # Split the text into chunks of 'max_length' characters or less
        return [text[i:i + max_length] for i in range(0, len(text), max_length)]
    for t in split_long_string(text):
        await message.answer(t)
