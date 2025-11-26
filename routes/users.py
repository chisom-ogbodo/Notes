
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from notes_api.core.oauth import get_current_user
from notes_api.crud.user import add_user, delete_user, update_user
from notes_api.models.db import get_conn
from notes_api.schemas.notes import User

router = APIRouter(prefix='/users', tags=['users'])

@router.post('/signup')
async def create_acct(detail: Annotated[OAuth2PasswordRequestForm, Depends()], \
                    email: Annotated[EmailStr, Form()], conn=Depends(get_conn)):
    username, password = detail.username, detail.password
    await add_user(username, email, password, conn)
    return 'successful'

@router.put('/update_user/{user_id}')
async def user_update(details: User, user_id=Depends(get_current_user), conn=Depends(get_conn)):
    info = await update_user(int(user_id), details, conn)
    if not info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')
    return 'Update Successful'

@router.delete('/{user_id}')
async def user_delete(user_id=Depends(get_current_user), conn=Depends(get_conn)):
    info = await delete_user(user_id, conn)
    if not info: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found') 
    return f'User deleted successfully'
