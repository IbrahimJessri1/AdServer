from uuid import uuid4
from fastapi import APIRouter, status
from models.ssp import Ad_Request
from models.ssp import ApplyAd
from repositries import serve_ads as repo_serve
from fastapi.responses import RedirectResponse
from fastapi.requests import Request

serve_ads_router = APIRouter(
    prefix="/serve_ad",
    tags = ['Serve Ads']
)

@serve_ads_router.get('/impression/{id}')
async def redirect(id):
    redirect_url =  repo_serve.redirect_impression(id)
    return RedirectResponse(redirect_url, status_code= status.HTTP_302_FOUND)

@serve_ads_router.get('/click/{id}')
async def redirect(id):
    redirect_url =  repo_serve.redirect_click(id)
    return RedirectResponse(redirect_url, status_code= status.HTTP_302_FOUND)