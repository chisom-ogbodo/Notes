import datetime as dt
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt 
from jwt.exceptions import InvalidTokenError

from notes_api.core import utils, config
from notes_api.crud.user import get_user
from notes_api.models.db import get_conn
from notes_api.schemas.notes import Token

settings = config.settings
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login')
router = APIRouter(prefix='/login', tags=['OAuth'])

def create_access_token(data: dict, optional_expires: timedelta | None = None):
    token_data = data.copy()
    if optional_expires:
        expires = datetime.now(dt.UTC) + optional_expires
    else: 
        expires = datetime.now(dt.UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data.update({'exp': expires})
    jwt_data = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_data

def get_current_user(token=Depends(oauth_scheme)):
    credential_error = HTTPException(
        detail='Invalid credentials', 
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get('sub')
        if not user_id:
            raise credential_error
    except InvalidTokenError:
        raise credential_error
    return user_id


@router.post('/', response_model=Token)
async def login_user(
    flow: Annotated[OAuth2PasswordRequestForm, Depends()], 
    conn=Depends(get_conn)
):
    email = flow.username
    user = await get_user(email, conn)
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid username or pasword')
    if not utils.verify_password(flow.password, user[3]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')
    access_token = create_access_token({'sub': str(user[0])})
    return Token(access_token=access_token, token_type='Bearer')