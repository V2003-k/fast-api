from fastapi import status, Depends, HTTPException, Response, APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..schemas import Post, PostCreate
from .. import models, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_posts = models.Post(**post.model_dump())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)

    return new_posts

# @router.get('/latest', response_model=Post)
# def get_latest_posts(db: Session = Depends(get_db)):
#     post = db.query(models.Post).order_by(models.Post.id.desc()).first()

#     return post

@router.get('/{id}', response_model=Post)
def get_posts(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists"
        )
    
    post.delete(synchronize_session=False)
    db.commit()

    return post

@router.put('/{id}', response_model=Post)
def update_posts(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()