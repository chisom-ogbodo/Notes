
from typing import Annotated
from fastapi import Depends
import psycopg
from notes_api.models.db import get_conn

conn = get_conn()

def create_user(conn: psycopg.Connection = Depends(conn)):
    sql = ["""CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, username VARCHAR(50) NOT NULL, 
           email VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(50) NOT NULL, created_date TIMESTAMPTZ DEFAULT 
           NOW());""",
           """CREATE TABLE IF NOT EXISTS notes (note_id SERIAL PRIMARY KEY, user_id INT NOT NULL, title 
           VARCHAR(57), content TEXT NOT NULL, date_added TIMESTAMPTZ DEFAULT NOW()), 
           FOREIGN KEY(user_id) REFERNCES users(user_id);"""
   ]
    with conn.cursor() as cur:
        for query in sql:
            cur.execute(query)

