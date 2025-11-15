from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    ispublished: bool = True
    rating: Optional[int] = None

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
def get_posts():
    # return { "data": jsonable_encoder(my_posts) }
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    my_posts.extend(posts)
    return { "data": posts }

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # cursor.execute(f""" INSERT INTO posts (title, content, ispublished) VALUES ({post.title}, {post.content}, {post.ispublished}) """)
    cursor.execute(""" INSERT INTO posts (title, content, ispublished) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.ispublished))
    
    new_posts = cursor.fetchone()
    conn.commit()
    return { "data": new_posts }

@app.get('/posts/latest')
def get_latest_posts():
    post = my_posts[len(my_posts)-1]
    return { "detail": post }

@app.get('/posts/{id}')
def get_posts(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id, ))
    post = cursor.fetchone()
    print(post)
    if post == None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { "message": f"post with id: {id} was not found" }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return { "post_details": post }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s""", (id,))

    deleted_post = cursor.fetchone()

    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"post with id: {id} does not exists"
        )
    
    conn.commit()

    return { "data": deleted_post }

@app.put('/posts/{id}')
def update_posts(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, ispublished = %s WHERE ID = %s RETURNING * """, (post.title, post.content, post.ispublished, id, ))
    updated_post = cursor.fetchone()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    conn.commit()

    return { "data": updated_post }