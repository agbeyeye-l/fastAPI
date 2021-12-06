from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from . import oauth2
from .. import schema, models

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote, db:Session = Depends(get_db), current_user=Depends(oauth2.IsAuthenticated)):
    
    #check existence of post
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post does not exist")

    vote_query = db.query(models.Vote).filter(
            models.Vote.post_id==vote.post_id, models.Vote.user_id==current_user.id)
    get_vote = vote_query.first()
    if vote.vote_cast:
        if get_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail=f'User {current_user.id} already has a vote on post {vote.post_id}')

        new_vote_query = models.Vote(user_id=current_user.id, post_id = vote.post_id)
        db.add(new_vote_query)
        db.commit()
        return {"message":"Successfully added vote"}
    else:
        
        if not get_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return Response(content="vote removed successfully",status_code=status.HTTP_204_NO_CONTENT)