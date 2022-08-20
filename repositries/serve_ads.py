
from fastapi import HTTPException, status
from repositries import generics as gen
from config.db import interactive_advertisement_collection, advertisement_collection, served_ad_collection




def redirect_impression(id):
    served_ad = gen.get_one(served_ad_collection, {"id": id})
    if not served_ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found..")
    ad = gen.get_one(advertisement_collection, {"id" : served_ad["ad_id"]})
    if not ad:
        ad = gen.get_one(interactive_advertisement_collection, {"id": served_ad["ad_id"]})
    gen.update_one(interactive_advertisement_collection, {"id" : ad["id"]}, { "$inc": { "marketing_info.impressions": 1 } })
    gen.update_one(served_ad_collection, {"id" : id}, { "$inc": { "impressions": 1 } })
    return ad["url"]



def redirect_click(id):
    served_ad = gen.get_one(served_ad_collection, {"id": id})
    if not served_ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found..")
    ad = gen.get_one(interactive_advertisement_collection, {"id": served_ad["ad_id"]})
    gen.update_one(interactive_advertisement_collection, {"id" : ad["id"]}, { "$inc": { "marketing_info.clicks": 1 } })
    gen.update_one(served_ad_collection, {"id" : id}, { "$inc": { "clicks": 1 } })
    return ad["redirect_url"]