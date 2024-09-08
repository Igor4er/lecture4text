from pydantic import BaseModel, field_validator, SecretStr
from typing import List
from enum import Enum
from api.user import get_user_settings_dict, update_user_settings
from api.encryption import decrypt, encrypt


class UserSettings(BaseModel):
    uid: int
    deepgram_key_enc: str | None = None
    openai_key_enc: str | None = None
    gist_key_enc: str | None = None

    def secret_deepgram_key(self) -> str:
        return decrypt(self.deepgram_key_enc)
    
    def secret_openai_key(self) -> str:
        return decrypt(self.openai_key_enc)
    
    def secret_gist_key(self) -> str:
        return decrypt(self.gist_key_enc)


    async def update_deepgram_key(self, key: str) -> str:
        self.deepgram_key_enc = encrypt(key)
        return await self._update_settings()


    def has_deepgram_key(self) -> bool:
        return self.deepgram_key_enc is not None and len(self.deepgram_key_enc) > 10
    
    def has_openai_key(self) -> bool:
        return self.openai_key_enc is not None and len(self.openai_key_enc) > 10

    def has_gist_key(self) -> bool:
        return self.gist_key_enc is not None and len(self.gist_key_enc) > 10
    
    async def _update_settings(self):
        return await update_user_settings(self.model_dump())


class Permissions(str, Enum):
    all = "*"
    create_audio_prompt = "create_audio_prompt"
    change_settings = "change_settings"


class User(BaseModel):
    uid: int | None = None
    exp: int
    for_ids: List[int]
    permissions: List[Permissions]

    @field_validator('permissions', mode="before")
    def handle_all_permissions(cls, value):
        if len(value) == 1 and value[0] == Permissions.all:
            return [perm for perm in Permissions if perm != Permissions.all]
        return value
    
    async def get_settings(self) -> UserSettings:
        settings_dict = await get_user_settings_dict(self.uid)
        return UserSettings.model_validate(settings_dict)
