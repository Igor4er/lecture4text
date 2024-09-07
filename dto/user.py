from pydantic import BaseModel, field_validator
from typing import List
from enum import Enum


# Define an Enum for permissions
class Permissions(str, Enum):
    all = "*"
    create_audio_prompt = "create_audio_prompt"


# Define a Pydantic model for the User
class User(BaseModel):
    exp: int
    for_ids: List[int]
    permissions: List[Permissions]

    @field_validator('permissions', mode="before")
    def handle_all_permissions(cls, value):
        if len(value) == 1 and value[0] == Permissions.all:
            return [perm for perm in Permissions if perm != Permissions.all]
        return value

