
from psycopg import Connection
from pydantic import EmailStr

from notes_api.core.utils import hash_password
from notes_api.schemas.notes import User

async def add_user(username: str, email: EmailStr, password: str | bytes, conn: Connection):
    sql = """INSERT INTO users(username, email, password) VALUES (%s, %s, %s);"""
    hashed_password = hash_password(password)
    with conn.cursor() as cur:
        cur.execute(sql, (username, email, hashed_password))

async def get_user(email: str, conn: Connection):
    sql = """SELECT * FROM users WHERE email = %(email)s;"""
    with conn.cursor() as cur:
        cur.execute(sql, {'email': email})
        return cur.fetchone()
    
async def update_user(user_id: int, user: User, conn: Connection):
    sql = """UPDATE users SET username = %s, email = %s, password = %s WHERE user_id = %s RETURNING *;"""
    with conn.cursor() as cur:
        cur.execute(sql, {'user_id': user_id, **user.model_dump()})
        return cur.fetchone()
    
#async def delete_user(user_id, conn: Connection):
 #   sql = """DELETE FROM users WHERE user_id = %(user_id)s; RETURNING *"""
  #  with conn.cursor() as cur:
   #     cur.execute(sql, {'user_id': user_id})
    #    return cur.fetchone()