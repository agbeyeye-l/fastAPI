from typing import Set
from fastapi.exceptions import HTTPException
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import JWTError
from fastapi import status, Depends
from sqlalchemy.orm import Session
from ..db import  get_db
from .. import models, schema  
from ..config import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = Settings.SECRET_KEY
ALGORITHM = Settings.ALGORITHM
ACCESS_TOKEN_EXPIRATION_DURATION_MINUTES= Settings.ACCESS_TOKEN_EXPIRATION_DURATION_MINUTES

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRATION_DURATION_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token


def verify_access_token(token, credentialException):
    try:
        decoded_data= jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = decoded_data["id"]
        if not user_id:
            raise credentialException
        token_data = schema.TokenData(id=user_id)
        
    except JWTError:
        raise credentialException

    return token_data

def IsAuthenticated(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credentialException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail=f'Could not validate credentials',
                                        headers={"WWW-Authenticate":"Bearer"})
    token= verify_access_token(token, credentialException)
    user = db.query(models.User).filter(models.User.id==token.id).first()
    return user
