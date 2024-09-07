from io import BytesIO
from aiofiles.threadpool.binary import AsyncBufferedReader
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
from config import CONFIG
import httpx

OPTIONS = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            language="uk"

        )

async def get_words_from_file_bytes(file) -> dict:
    dc = DeepgramClient(CONFIG.DEEPGRAM_API_KEY.get_secret_value())
    payload: FileSource = {
        "buffer": file
    }
    response = await dc.listen.asyncrest.v("1").transcribe_file(
        payload, OPTIONS, timeout=httpx.Timeout(300.0, connect=10.0)
    )
    return response.to_dict()
