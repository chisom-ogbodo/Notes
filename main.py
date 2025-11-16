
"""Entry point for the application"""

from fastapi import FastAPI

#from notes_api.models.note import create_table
from notes_api.routes import notes

app = FastAPI(title='my_notes_api')
#create_table()
app.include_router(notes.router)


@app.get('/')
async def home():
    return f'Notes Api Home'