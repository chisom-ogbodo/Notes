from psycopg_pool import AsyncConnectionPool, ConnectionPool


from notes_api.core import settings

#settings = Settings()
POSTGRES_DSN = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}"
pool: ConnectionPool = ConnectionPool(POSTGRES_DSN)
#pool: ConnectionPool = ConnectionPool('dbname=notesapi user=postgres')
#for trying out the async pool
async_pool: AsyncConnectionPool = AsyncConnectionPool(POSTGRES_DSN)  

def get_conn():
    with pool.connection() as conn: 
        yield conn

# async db dependency function
async def async_get_conn():
    async with async_pool.connection() as async_conn:
        yield async_conn
