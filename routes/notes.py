from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from psycopg import Connection

from notes_api.core.oauth import get_current_user
from notes_api.crud.note import * 
from notes_api.models.db import get_conn, async_get_conn
from notes_api.schemas.notes import Notes, NotesUpdate

router = APIRouter(prefix='/note', tags=['notes'])
#user_id: Annotated[int, Depends(get_current_user)]

@router.get('/get_all')
async def get_notes(user_id=Depends(get_current_user), conn = Depends(get_conn)):
    data = await crud_retrieve(int(user_id), conn)
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your don't notes currently")
    return {'notes': data}

@router.get('/{note_id}')
async def get_one(note_id: int, conn=Depends(get_conn)):
    val = await crud_get_one(int(note_id), conn)
    if not val:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')
    return val

@router.post('/create_note', status_code=status.HTTP_201_CREATED)
async def create_note(note: Annotated[Notes, Body()], user_id=Depends(get_current_user), conn=Depends(get_conn)):
    await crud_create(user_id, Notes(**note.model_dump()), conn)
    return f'notes created successfully'.capitalize()

@router.put('/update/{note_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_note(note_id: int, note: Annotated[NotesUpdate, Body()], user_id=Depends(get_current_user), 
                      conn=Depends(get_conn)):
    data = await crud_update(int(user_id), note_id, NotesUpdate(**note.model_dump()), conn)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #if user_id != note.user_id:
     #   raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Sorry, but you do not own this note')
    return 'update successful'.capitalize()
    
@router.delete('/delete/{note_id}', status_code=200)
async def delete_note(note_id: int, user_id=Depends(get_current_user), conn=Depends(get_conn)):
    data = await crud_delete(user_id, note_id, conn)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return f'Delete successful'
