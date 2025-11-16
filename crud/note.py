
from typing import Annotated

from psycopg import Connection

from notes_api.schemas.notes import Notes

async def crud_get_one(id: int, conn: Connection):
    sql = """SELECT * FROM notes WHERE note_id = %s"""
    with conn.cursor() as cur:
        cur.execute(sql, (id,))
        val = cur.fetchone()
        return val
    
async def crud_retrieve(conn: Connection):
    sql = """SELECT * FROM notes;"""
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()
        
async def crud_create(note: Notes, conn: Connection):
    sql = """INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING *"""
    with conn.cursor() as cur:
        #if not note.title: 
         #   note.title = note.title[:58]
        cur.execute(sql, (note.title, note.content,))
        
async def crud_update(note_id: int, note: Notes, conn: Connection):
    sql = """UPDATE notes SET content = %s WHERE note_id = %s RETURNING *;""" 
    with conn.cursor() as cur:
        if note.title:
            sql = """UPDATE notes SET title = %s, content = %s WHERE note_id = %s RETURNING *;"""       
            cur.execute(sql, (note.title, note.content, note_id,))
        else:
            cur.execute(sql, (note.content, note_id,))
        return cur.fetchone()
       
    
async def crud_delete(note_id: int, conn: Connection):
    sql = """DELETE FROM notes WHERE note_id = %s RETURNING *;"""
    with conn.cursor() as cur:
        cur.execute(sql, (note_id,))
        data = cur.fetchone()
    return data