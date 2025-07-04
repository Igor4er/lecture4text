from io import BytesIO
from typing import Awaitable
from aiofiles.threadpool.binary import AsyncBufferedReader
from deepgram import (
    AsyncListenRESTClient,
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
from config import CONFIG
import httpx

OPTIONS = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            language="uk",
        )


class Deepgram():
    def __init__(self, dg_key: str):
        self._dg = DeepgramClient(dg_key)

        api = self._dg.listen.asyncrest.v("1")
        assert(isinstance(api, AsyncListenRESTClient))

        self.api = api

    async def get_words_from_file_bytes(self, file) -> dict:
        payload: FileSource = {
            "buffer": file
        }

        response = await self.api.transcribe_file(
            payload, OPTIONS, timeout=httpx.Timeout(300.0, connect=10.0)
        )
        return response.to_dict()

    async def get_words_from_file_url(self, url) -> dict:
        response = await self.api.transcribe_url(
            {"url": url}, OPTIONS, timeout=httpx.Timeout(300.0, connect=10.0)
        )
        return response.to_dict()
