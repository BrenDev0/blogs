from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserShemaBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        str_min_length=1,
        alias_generator=to_camel,
        extra="forbid"
    )

class UserPublic(UserShemaBase):
    user_id: UUID
    email: str
    name:str
    created_at: datetime

class CreateUserRequest(UserShemaBase):
    code: int
    name: str
    email: str
    password: str

class VerifiedUserUpdateRequest(UserShemaBase):
    email: Optional[str] = None
    password: Optional[str] = None

class UpdateUserRequest(UserShemaBase):
    name: Optional[str] = None
    password: Optional[str] = None
    old_password: Optional[str] = None

class VerifiedUserUpdateRequest(UserShemaBase):
    email: Optional[str] = None
    password: Optional[str] = None

class LoginRequest(UserShemaBase):
    email: str
    password: str

class UpdateUserSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    email_hash: Optional[str] = None
    password: Optional[str] = None