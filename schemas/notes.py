from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

class Notes(BaseModel):
    title: Annotated[str | None, Field(max_length=57)]
    content: str

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_date: datetime

class UserInDb(User):
    hashed_password: str
