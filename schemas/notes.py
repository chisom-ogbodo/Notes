from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

class Notes(BaseModel):
    #note_id: int
    #user_id: int
    title: Annotated[str | None, Field(max_length=57)] = None
    content: str
    #created_date: datetime

class NotesUpdate(BaseModel):
    title: str | None = None
    content: str

class User(BaseModel):
    username: str | None = None
    email: EmailStr
    password: str

class UserOut(User):
    #username: str | None = None
    user_id: int
   

class UserInDb(UserOut, User):
    pass
    #hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

