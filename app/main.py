from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(engine)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # created_at: Optional[datetime]

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

my_posts = []

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get('/')
async def root():
    return { "message": "Welcome to my API!" }

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # return { "data": jsonable_encoder(my_posts) }
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    # my_posts.extend(posts)
    
    posts = db.query(models.Post).all()
    return { "data": posts }

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(f""" INSERT INTO posts (title, content, ispublished) VALUES ({post.title}, {post.content}, {post.ispublished}) """)
    # cursor.execute(""" INSERT INTO posts (title, content, ispublished) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.ispublished))
    
    # new_posts = cursor.fetchone()
    # conn.commit()

    new_posts = models.Post(**post.model_dump())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return { "data": new_posts }

@app.get('/posts/latest')
def get_latest_posts(db: Session = Depends(get_db)):
    # post = my_posts[len(my_posts)-1]
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()

    return { "detail": post }

@app.get('/posts/{id}')
def get_posts(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id, ))
    # post = cursor.fetchone()
    # print(post)
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    
    if post == None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { "message": f"post with id: {id} was not found" }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return { "post_details": post }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s""", (id,))

    # deleted_post = cursor.fetchone()
    
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists"
        )
    
    post.delete(synchronize_session=False)
    db.commit()

    return { "data": post }

@app.put('/posts/{id}')
def update_posts(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, ispublished = %s WHERE ID = %s RETURNING * """, (post.title, post.content, post.ispublished, id, ))
    # updated_post = cursor.fetchone()
    
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return { "data": post }