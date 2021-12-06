from typing import List
from fastapi import status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.exceptions import HTTPException 
from ..db import  get_db
from .. import schema, models
from . import oauth2


router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[schema.PostVoteResponse])
def get_post(db: Session = Depends(get_db), userloggedIn=Depends(oauth2.IsAuthenticated)):
    """
    Get list of posts created by a current user
    """
    #posts = db.query(models.Post).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('likes')).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).all()
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schema.PostVoteResponse)
def create_post(_post:schema.PostCreate, db: Session = Depends(get_db), userloggedIn=Depends(oauth2.IsAuthenticated)):
    """
    This function creates a new post
    """
    print("user login",userloggedIn)
    new_post = models.Post(owner_id=userloggedIn.id,**_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label('likes')).join(models.Vote, models.Vote.post_id==new_post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==new_post.id)
    post = post_query.first()
    return post


@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=schema.PostVoteResponse)
def read_post(id:int,db: Session = Depends(get_db),userloggedIn=Depends(oauth2.IsAuthenticated)):
    """
    This function defines a read operation on a post
    """
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label('likes')).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found")
    
    return post


@router.delete("/{id}")
def delete_post(id:int,db: Session = Depends(get_db),userloggedIn=Depends(oauth2.IsAuthenticated)):
    """
    This function deletes a post from the database
    """
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail= f'Post with id {id} cannot be found')

    if post.owner_id!= userloggedIn.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schema.PostResponse)
def update_post(id:int,new_Post:schema.PostCreate, db: Session = Depends(get_db),userloggedIn=Depends(oauth2.IsAuthenticated)):
    """
    This function updates a post
    """
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail= f'Post with id {id} cannot be found')

    if post.owner_id!= userloggedIn.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(new_Post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()