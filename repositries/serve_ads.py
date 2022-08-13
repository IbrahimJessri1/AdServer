
from fastapi import HTTPException, status
from repositries import generics as gen
from config.db import interactive_advertisement_collection, interactive_advertisement_collection

def redirect(id):
    ad = gen.get_one(interactive_advertisement_collection, {"id": id})
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found..")
    gen.update_one(interactive_advertisement_collection, {"id" : ad["id"]}, { "$inc": { "marketing_info.clicks": 1 } })
    return ad["ad_info"]["redirect_url"]