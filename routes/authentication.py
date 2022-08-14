from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from repositries.hashing import Hash
from repositries import generics as gen
from config.db import user_collection
from models.token import Token
from repositries.JWTtoken import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
authentication_router = APIRouter(tags=['Authentication'])




@authentication_router.post('/login')
def login(login_info : OAuth2PasswordRequestForm = Depends()):
    collection  = user_collection
    user = gen.get_one(collection, {"username" : login_info.username})
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Invalid Credentials")
    if not Hash.verify(user["password"],  login_info.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Incorrect Password")
    access_token = create_access_token(data={"sub": user["username"]})
    return Token(access_token = access_token, token_type= "bearer")
    