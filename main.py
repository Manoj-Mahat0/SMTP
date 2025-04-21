from fastapi import FastAPI
from routes import contact

app = FastAPI()
app.include_router(contact.router)
