from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas,models,db
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_token(data: dict):
    to_encode=data.copy() #in order to not mess up the data from the fucntion

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    exe_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return exe_jwt

def verify_jwt(token: str, cred_ex):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id") ##Mozda je us_id

        if id is None:
            raise cred_ex
        token_data  = schemas.TokenData(id=id)

    except JWTError:
        raise cred_ex

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(db.get_db)):
    cred_ex= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", 
    headers={"WWW-Authenticate": "Bearer"})

    token = verify_jwt(token, cred_ex)
    
    user = db.query(models.User).filter(models.User.id==token.id).first()
    return user