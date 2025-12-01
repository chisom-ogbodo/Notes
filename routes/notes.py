from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status

from notes_api.core.oauth import get_current_user
from notes_api.crud.note import * 
from notes_api.models.db import get_conn, async_get_conn
from notes_api.schemas import NotesCreate, NotesUpdate

router = APIRouter(prefix='/note', tags=['notes'])
#user_id: Annotated[int, Depends(get_current_user)]

@router.get('/get_all', response_model=list[Notes])
async def get_notes(user_id=Depends(get_current_user), conn = Depends(get_conn)):
    data = await crud_retrieve(int(user_id), conn)
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your don't notes currently")
    return data

@router.post('/create_note', status_code=status.HTTP_201_CREATED, response_model=NotesCreate)
async def create_note(note: Annotated[NotesCreate, Body()], user_id=Depends(get_current_user), conn=Depends(get_conn)):
    await crud_create(user_id, NotesCreate(**note.model_dump()), conn)
    return note

@router.put('/update/{note_id}', status_code=status.HTTP_202_ACCEPTED, response_model=NotesUpdate)
async def update_note(
    note_id: int, 
    note: Annotated[NotesUpdate, Body()], 
    user_id=Depends(get_current_user), 
    conn=Depends(get_conn)
):
    data = await crud_update(int(user_id), note_id, NotesUpdate(**note.model_dump()), conn)
    #if user_id != note.user_id:
     #   raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Sorry, but you do not own this note')
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return note
    
@router.delete('/delete/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, user_id=Depends(get_current_user), conn=Depends(get_conn)):
    data = await crud_delete(user_id, note_id, conn)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return f'Delete successful'
