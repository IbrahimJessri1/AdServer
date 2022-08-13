from uuid import uuid4
from fastapi import APIRouter, status
from models.ssp import Ad_Request
from models.ssp import ApplyAd
from repositries import serve_ads as repo_serve
from fastapi.responses import RedirectResponse


serve_ads_router = APIRouter(
    prefix="/serve_ad",
    tags = ['Serve Ads']
)

@serve_ads_router.get('/{id}')
async def redirect(id):
    redirect_url =  repo_serve.redirect(id)
    return RedirectResponse(redirect_url, status_code= status.HTTP_303_SEE_OTHER)