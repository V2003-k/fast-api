from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row
import time
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(engine)

app = FastAPI()

while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='2003', row_factory=dict_row)
        cursor = conn.cursor()
        print("Database Connection was Successfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
async def root():
    return { "message": "Welcome to my API!" }