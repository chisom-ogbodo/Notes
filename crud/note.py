
from psycopg import Connection

from notes_api.schemas.notes import Notes, NotesUpdate
    
async def crud_retrieve(user_id: int, conn: Connection, skip: int = 0, limit: int = 10):
    sql = f"""SELECT * FROM notes
    WHERE user_id = %s ORDER BY note_id 
    OFFSET {skip} ROWS FETCH FIRST {limit} ROWS ONLY;"""
    with conn.cursor() as cur:
        cur.execute(sql, (user_id,))
        res = cur.fetchall()
        return res
    
async def crud_create(user_id: int, note: Notes, conn: Connection):
    sql = """INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s) RETURNING *"""
    with conn.cursor() as cur:
        if not note.title: 
           note.title = note.content[:57]
           print(note.title)
        cur.execute(sql, (user_id, note.title, note.content,))
        
async def crud_update(user_id: int, note_id, note: NotesUpdate, conn: Connection):
    sql = """UPDATE notes SET content = %s WHERE user_id = %s AND note_id = %s RETURNING *;""" 
    with conn.cursor() as cur:
        if note.title:
            sql = """UPDATE notes SET title = %s, content = %s WHERE user_id = %s AND note_id = %s RETURNING *;"""       
            cur.execute(sql, (note.title, note.content, user_id, note_id,))
        else:
            cur.execute(sql, (note.content, user_id, note_id,))
        return cur.fetchone()
       
async def crud_delete(user_id: int, note_id: int, conn: Connection):
    sql = """DELETE FROM notes WHERE user_id = %s AND note_id = %s RETURNING *;"""
    with conn.cursor() as cur:
        cur.execute(sql, (user_id, note_id,))
        data = cur.fetchone()
    return data