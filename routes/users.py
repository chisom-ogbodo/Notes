
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from notes_api.core.oauth import get_current_user
from notes_api.crud.user import add_user, delete_user, update_user
from notes_api.models.db import get_conn
from notes_api.schemas import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix='/users', tags=['users'])

@router.post(
    '/signup', 
    status_code=status.HTTP_201_CREATED, 
    response_model=UserOut, 
    response_model_exclude_unset= True
)
async def create_acct(
    detail: Annotated[OAuth2PasswordRequestForm, Depends()], 
    email: Annotated[EmailStr, Form()], 
    conn=Depends(get_conn)
):
    username, password = detail.username, detail.password
    data: dict = await add_user(username, email, password, conn)
    return UserCreate(**data)

@router.put('/update_user/{user_id}', status_code=status.HTTP_200_OK, response_model=UserOut)
async def user_update(details: UserUpdate, user_id=Depends(get_current_user), conn=Depends(get_conn)):
    info = await update_user(int(user_id), details, conn)
    if not info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')
    return details

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user_id=Depends(get_current_user), conn=Depends(get_conn)):
    info = await delete_user(user_id, conn)
    if not info: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found') 
    return f'User deleted successfully'
