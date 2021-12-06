from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException 
from ..db import get_db
from .. import schema, utils, models
from . import oauth2

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schema.CreateUserResponse)
def createUser(user:schema.CreateUser, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    # hashing user password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model= schema.GetUserResponse)
def get_user(id:int, db: Session = Depends(get_db),userloggedIn=Depends(oauth2.IsAuthenticated)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail= f'User with id {id} cannot be found')

    return user
