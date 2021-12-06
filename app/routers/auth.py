from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..import models, schema, utils, db
from . import oauth2



router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schema.Token)
def Login(user_credentials: schema.UserLogin, db: Session = Depends(db.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credentials.email).first()
    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    token = oauth2.create_access_token(data={"id":user.id})
    return {"token": token}

@router.post("/logout")
def logout(userloggedIn=Depends(oauth2.IsAuthenticated)):
    pass