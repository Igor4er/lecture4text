from io import BytesIO
from aiofiles.threadpool.binary import AsyncBufferedReader
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
from config import CONFIG
import httpx
from dto.user import UserSettings

OPTIONS = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            language="uk"

        )


class Deepgram():
    def __init__(self, settings: UserSettings):
        self.dg = DeepgramClient(settings.secret_deepgram_key())
    
    async def get_words_from_file_bytes(self, file) -> dict:
        payload: FileSource = {
            "buffer": file
        }
        response = await self.dg.listen.asyncrest.v("1").transcribe_file(
            payload, OPTIONS, timeout=httpx.Timeout(300.0, connect=10.0)
        )
        return response.to_dict()
    
    async def get_words_from_file_url(self, url) -> dict:
        response = await self.dg.listen.asyncrest.v("1").transcribe_url(
            {"url": url}, OPTIONS, timeout=httpx.Timeout(300.0, connect=10.0)
        )
        return response.to_dict()
