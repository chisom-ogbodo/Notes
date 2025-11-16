from typing import Any, reveal_type

from psycopg_pool import AsyncConnectionPool, ConnectionPool

pool: ConnectionPool = ConnectionPool(conninfo='dbname=notesapi user=postgres')
#for trying out the async pool
async_pool: AsyncConnectionPool = AsyncConnectionPool(conninfo='dbname=notesapi user=postgres')  

def get_conn():
    with pool.connection() as conn: 
        yield conn

# async db dependency function
async def async_get_conn():
    async with AsyncConnectionPool as async_conn:
        yield async_conn
