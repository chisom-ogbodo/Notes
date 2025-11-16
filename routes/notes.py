from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from psycopg import Connection

from notes_api.crud.note import * 
from notes_api.models.db import get_conn
from notes_api.schemas.notes import Notes

router = APIRouter(prefix='/note', tags=['notes'])

@router.get('/{note_id}')
async def get_one(note_id: int, conn=Depends(get_conn)):
    val = await crud_get_one(int(note_id), conn)
    if not val:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')
    return val

#This endpoint is still buggy, to be fixed in the future    
@router.get('/get_all')
async def get_notes(conn = Depends(get_conn)):
    data = await crud_retrieve(conn)
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {'notes': data}

@router.post('/create_note', status_code=status.HTTP_201_CREATED)
async def create_note(note: Annotated[Notes, Body()], conn=Depends(get_conn)):
    await crud_create(Notes(**note.model_dump()), conn)
    return f'notes created successfully'.capitalize()

@router.put('/update/{note_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_note(note_id: int, note: Annotated[Notes, Body()], conn=Depends(get_conn)):
    data = await crud_update(note_id, Notes(**note.model_dump()), conn)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return 'update successful'.capitalize()
    
@router.delete('/delete/{note_id}', status_code=200)
async def delete_note(note_id: int, conn=Depends(get_conn)):
    data = await crud_delete(note_id, conn)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return f'Delete successful'
