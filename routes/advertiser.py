from fastapi import APIRouter, status, Depends, HTTPException
from models.token import TokenData
from models.users import Advertiser, AdvertiserUpdate
from repositries import advertiser as repo_advertiser, generics as gen, oauth2
from repositries.authorize import Authorize
from repositries.validation import Validator
# import time
# from repositries import similarity as model


advertiser_router = APIRouter(
    prefix="/advertiser",
    tags = ['Advertiser']
)


@advertiser_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def sign_up(advertiser: Advertiser):
    val_res = Validator.validate_advertiser(advertiser)
    if val_res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= val_res)
    return repo_advertiser.signup(advertiser)


@advertiser_router.put('/account')
async def update_account(advertiser_update : AdvertiserUpdate, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("self_update_account_adv", current_username.username)
    val_res = Validator.validate_advertiser_update(advertiser_update)
    if val_res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= val_res)
    return repo_advertiser.update_adv_account(advertiser_update, current_username.username)



@advertiser_router.get('/')
async def my_account(current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("self_get_adv", current_username.username)
    return repo_advertiser.get(current_username.username)





# @advertiser_router.get('/sim')
# async def get_sim(ph1: str, ph2: str):
#     start = time.time()
#     res = {'value' : float(model.get_similarity(ph1, ph2))}
#     end = time.time()
#     print(end - start)
#     return res