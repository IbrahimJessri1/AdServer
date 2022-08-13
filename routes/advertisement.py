
from fastapi import APIRouter, UploadFile, status, HTTPException, UploadFile, File, Depends
from repositries import oauth2
from models.token import TokenData
from models.advertisement import AdvertisementInput, InteractiveAdvertisementInput
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
    if not Validator.validate(ad_input):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='make sure of request arguments')
    return repo_advertisement.create_ad(ad_input, current_username.username)


############ permission = create_interactive_ad
@advertisement_router.post('/create_interactive_ad',  status_code=status.HTTP_201_CREATED)
async def create_interactive_ad(ad_input:InteractiveAdvertisementInput, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("create_interactive_ad", current_username.username)
    if not Validator.validate(ad_input):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='make sure of request arguments')
    return repo_advertisement.create_interactive_ad(ad_input, current_username.username)



@advertisement_router.get('/my_ads')
async def get_my_ads(current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("self_get_ad", current_username.username)
    return repo_advertisement.get_my_ads(current_username.username)



#admin
@advertisement_router.get('/')
async def get_all(current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("get_advertisement", current_username.username)
    return repo_advertisement.get_all()


@advertisement_router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def remove(constraints : dict, current_username : TokenData = Depends(oauth2.get_current_user)):
    Authorize.auth("delete_advertisement", current_username.username)
    repo_advertisement.remove(constraints)





##update_advertisement, self_update
##delete_advertisement, self_delete
