from fastapi import APIRouter, HTTPException, status, Request
from models.ssp import Ad_Request
from repositries import adexchange as repo_adexchange
from models.ssp import ApplyAd
from repositries.validation import Validator
from fastapi.responses import HTMLResponse

adexchange_router = APIRouter(
    prefix="/adexchange",
    tags = ['AdExchange']
)



@adexchange_router.post('/negotiate')
async def negotiate(request : Ad_Request):
    val_res = Validator.validate_ad_request(request)
    if val_res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= val_res)
    return repo_adexchange.negotiate(request)


@adexchange_router.post('/negotiate_interactive')
async def negotiate_interactive(request : Ad_Request):
    val_res = Validator.validate_ad_request(request)
    if val_res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= val_res)
    return repo_adexchange.negotiate(request, 1)


@adexchange_router.post('/request')
async def request(request : ApplyAd):
    val_res = Validator.validate_ad_apply(request)
    if val_res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= val_res)
    return repo_adexchange.request(request)

@adexchange_router.post('/request_interactive')
async def request(request : ApplyAd):
    val_res = Validator.validate_ad_apply(request)
    if val_res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= val_res)
    return repo_adexchange.request(request, 1)




@adexchange_router.post('/request/html', response_class=HTMLResponse)
async def html_request(request : Request, apply_ad : ApplyAd):
    val_res = Validator.validate_ad_apply(apply_ad)
    if val_res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= val_res)
    return repo_adexchange.html_request(request, apply_ad)

@adexchange_router.post('/request_interactive/html', response_class=HTMLResponse)
async def html_request(request : Request, apply_ad : ApplyAd):
    val_res = Validator.validate_ad_apply(apply_ad)
    if val_res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= val_res)
    return repo_adexchange.html_request(request,apply_ad, 1)