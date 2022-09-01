
from fastapi import HTTPException, status
from repositries import generics as gen
from config.db import interactive_advertisement_collection, advertisement_collection, served_ad_collection




def redirect_impression(id):
    served_ad = gen.get_one(served_ad_collection, {"id": id})
    if not served_ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found..")
    charges_inc = 0
    if served_ad['clicks'] == -1:
        ad = gen.get_one(advertisement_collection, {"id" : served_ad["ad_id"]})
        charges_inc = round(float(served_ad['agreed_cpc']) /20, 4)
        gen.update_one(advertisement_collection, {"id" : ad["id"]}, { "$inc": { "marketing_info.impressions": 1, "marketing_info.tot_charges" : charges_inc } })
    else:
        ad = gen.get_one(interactive_advertisement_collection, {"id": served_ad["ad_id"]})
        gen.update_one(interactive_advertisement_collection, {"id" : ad["id"]}, { "$inc": { "marketing_info.impressions": 1 } })

    gen.update_one(served_ad_collection, {"id" : id}, { "$inc": { "impressions": 1, "charges": charges_inc } })
    return ad["url"]



def redirect_click(id):
    served_ad = gen.get_one(served_ad_collection, {"id": id})
    if not served_ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found..")
    ad = gen.get_one(interactive_advertisement_collection, {"id": served_ad["ad_id"]})
    gen.update_one(interactive_advertisement_collection, {"id" : ad["id"]}, { "$inc": { "marketing_info.clicks": 1, "marketing_info.tot_charges" : float(served_ad['agreed_cpc'])} })
    gen.update_one(served_ad_collection, {"id" : id}, { "$inc": { "clicks": 1, "charges" : float(served_ad['agreed_cpc'])} })
    return ad["redirect_url"]