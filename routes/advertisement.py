
from fastapi import APIRouter, UploadFile, status, HTTPException, UploadFile, File, Depends
from repositries import oauth2
from models.token import TokenData
from models.advertisement import AdvertisementInput, InteractiveAdvertisementInput, adLimitedGet
from repositries import advertisement as repo_advertisement
from repositries.validation import Validator
from repositries.authorize import Authorize

advertisement_router = APIRouter(
    prefix="/advertisement",
    tags = ['Advertisement']
)




@advertisement_router.post('/create_ad',  status_code=status.HTTP_201_CREATED)
async def create_ad(ad_input:AdvertisementInput, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("create_ad", current_username.username)
    val_res = Validator.validate_ad_input(ad_input)
    if val_res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= val_res)
    return repo_advertisement.create_ad(ad_input, current_username.username)


############ permission = create_interactive_ad
@advertisement_router.post('/create_interactive_ad',  status_code=status.HTTP_201_CREATED)
async def create_interactive_ad(ad_input:InteractiveAdvertisementInput, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("create_interactive_ad", current_username.username)
    val_res = Validator.validate_interactive_ad_input(ad_input)
    if val_res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= val_res)
    return repo_advertisement.create_interactive_ad(ad_input, current_username.username)



@advertisement_router.get('/my_ads')
async def get_my_ads(current_username : TokenData = Depends(oauth2.get_current_user), limit : int = -1, skip : int  = 0, interative : int = 0):
    Authorize.auth("self_get_ad", current_username.username)
    return repo_advertisement.get_my_ads(username= current_username.username, limit=limit, skip=skip, interactive= interative)



#admin
@advertisement_router.post('/')
async def get(ad_limited_input : adLimitedGet, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("get_advertisement", current_username.username)
    return repo_advertisement.get(ad_limited_input.constraints, limit=ad_limited_input.limit, skip=ad_limited_input.skip, interactive= ad_limited_input.interactive)


@advertisement_router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def remove(constraints : dict, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("delete_advertisement", current_username.username)
    repo_advertisement.remove(constraints)

@advertisement_router.get('/my_served_ads')
async def get_my_served_ads(current_username : TokenData = Depends(oauth2.get_current_user), limit : int = -1, skip : int  = 0):
    Authorize.auth("self_get_served_ad", current_username.username)
    return repo_advertisement.get_my_served_ads(username= current_username.username, limit=limit, skip=skip)


@advertisement_router.get('/my_served_ad/{id}')
async def get_served_ad(id, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("self_get_served_ad", current_username.username)
    return repo_advertisement.get_served_ad(id, current_username.username)

@advertisement_router.get('/total_payment/')
async def get_total_payment_ad(current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("self_get_tot_payment", current_username.username)
    return repo_advertisement.get_tot_payment(current_username.username)

@advertisement_router.get('/total_payment/{id}')
async def get_total_ad_payment(id, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("self_get_ad_payment", current_username.username)
    return repo_advertisement.get_ad_payment(current_username.username, id)


@advertisement_router.get('/{id}')
async def get_ad(id, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("self_get_ad", current_username.username)
    return repo_advertisement.get_ad(id, current_username.username)





##update_advertisement, self_update
##delete_advertisement, self_delete
