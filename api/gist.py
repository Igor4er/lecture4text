import aiohttp
import time

GIST_BASE_URL = "https://api.github.com/gists"

class Gist:
    def __init__(self, g_key: str) -> None:
        self._gist_key = g_key

    async def create_gist_from_text(self, txt: str):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Accept": "Accept: application/vnd.github+json",
                "Authorization": f"Bearer {self._gist_key}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            data = {
                "public": False,
                "description": f"Created with lecture4text at {int(time.time())}",
                "files": {
                    f"l4t_{time.time()}.txt": {"content": txt.replace(". ", ".\n")}
                }
            }
            resp = await session.post(GIST_BASE_URL, headers=headers, json=data)
            if not resp.ok:
                print(resp.status, await resp.text())
            return resp.ok
