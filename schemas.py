from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

class Notes(BaseModel):
    note_id: int
    user_id: int
    title: Annotated[str | None, Field(max_length=57)] = None
    content: str
    created_date: datetime

class NotesUpdate(BaseModel):
    title: Annotated[str | None, Field(max_length=57)] = None
    content: str

class NotesCreate(NotesUpdate):
    pass

class UserBase(BaseModel):
    username: Annotated[str | None, Field(max_length=50)] = None
    email: Annotated[EmailStr, Field(max_length=50)]
    
class UserOut(UserBase):
    pass

class UserCreate(UserBase):
    password: Annotated[str, Field(max_length=255)]

class UserUpdate(UserCreate):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

#class TokenData(BaseModel):
 #   username: str | None = None

