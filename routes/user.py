from fastapi import APIRouter, status, Depends, HTTPException
from models.users import UserUpdate
from repositries import user as repo_user
from repositries import oauth2
from models.token import TokenData
from repositries.authorize import Authorize
from repositries.validation import Validator

user_router = APIRouter(
    prefix="/user",
    tags = ['User']
)


#create
#update

@user_router.get('/all')
async def get(current_username : TokenData = Depends(oauth2.get_current_user), limit : int = -1, skip : int  = 0, role : str = None):
    Authorize.auth("get_user", current_username.username)
    return repo_user.get_all(limit=limit, skip=skip, role= role)


@user_router.delete('/remove', status_code=status.HTTP_204_NO_CONTENT)
async def remove(constraints : dict, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("delete_user", current_username.username)
    repo_user.remove(constraints)


@user_router.put('/update')
async def update_account(user_update : UserUpdate, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("self_update_user", current_username.username)
    val_res = Validator.validate_user_update(user_update)
    if val_res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= val_res)
    return repo_user.update_account(user_update, current_username.username)




@user_router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("self_delete_user", current_username.username)
    repo_user.delete_account(current_username.username)


@user_router.get('/')
async def get_my_account(current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("self_get_user", current_username.username)
    return repo_user.get_my_account(current_username.username)