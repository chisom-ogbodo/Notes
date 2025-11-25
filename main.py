
"""Entry point for the application"""

from fastapi import FastAPI

from notes_api.core import oauth, config
#from notes_api.models.note import create_table
from notes_api.routes import notes, users

app = FastAPI(title='my_notes_api')
#create_table()
app.include_router(notes.router)
app.include_router(users.router)
app.include_router(oauth.router)

@app.get('/')
async def home():
    print(config.settings)
    return f'Notes Api Home'
        
