from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row
import time

SQLMODEL_DATABASE_URL = "postgresql+psycopg://postgres:2003@localhost/fastapi"

engine = create_engine(SQLMODEL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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