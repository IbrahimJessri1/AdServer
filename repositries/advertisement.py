from os import stat
from uuid import uuid4
from fastapi import HTTPException, status
from config.db import advertisement_collection, interactive_advertisement_collection, served_ad_collection
from models.ads_stats import ServedAd
from repositries import generics as gen
from models.advertisement import AdInfo, Advertisement, AdvertisementShow, InteractiveAdvertisementInput, MarketingInfo, InteractiveAdInfo, InteractiveAdvertisement, InteractiveMarketingInfo, AdType, InteractiveAdvertisementShow
import datetime
from .utilites import get_dict, limited_get, download_file


def create_ad(ad_input, advertiser_username):
    try:
        create_date = str(datetime.datetime.now())
        ad_info = AdInfo(type = ad_input.type, advertiser_username=advertiser_username, url=ad_input.url, text=ad_input.text)
        id = str(uuid4())
        advertisement = Advertisement(
            id= id,
            create_date = create_date,
            target_user_info=ad_input.target_user_info, 
            marketing_info=MarketingInfo(max_cpc= ad_input.max_cpc,impressions= 0, raise_percentage=ad_input.raise_percentage),
            ad_info= ad_info,
            categories=ad_input.categories
        )
        filenames = [(AdType.TEXT, '.txt'), (AdType.IMAGE, '.jpg'), (AdType.VIDEO, '.mp4')]
        dir = 'advertisements/' + advertiser_username
        filename = str(advertisement.id)
        for x in filenames:
            if x[0] == ad_input.type:
                filename += x[1]
                break
       # download_file(advertisement.ad_info.url, dir, filename)
        d = get_dict(advertisement)
        advertisement_collection.insert_one(dict(d))
        return id
    except:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail='An error happened, try again later')



def create_interactive_ad(ad_input : InteractiveAdvertisementInput, advertiser_username):
    try:
        create_date = str(datetime.datetime.now())
        ad_info = InteractiveAdInfo(type = ad_input.type, advertiser_username=advertiser_username, url=ad_input.url, redirect_url= ad_input.redirect_url, text=ad_input.text)
        id = uuid4()
        advertisement = InteractiveAdvertisement(
            id = str(id),
            create_date = create_date,
            target_user_info=ad_input.target_user_info, 
            marketing_info=InteractiveMarketingInfo(max_cpc= ad_input.max_cpc,impressions= 0, clicks=0, raise_percentage=ad_input.raise_percentage),
            ad_info= ad_info,
            categories=ad_input.categories,
            keywords=ad_input.keywords
        )
        filenames = [(AdType.TEXT, '.txt'), (AdType.IMAGE, '.jpg'), (AdType.VIDEO, '.mp4')]
        dir = 'advertisements/' + advertiser_username
        filename = str(advertisement.id)
        for x in filenames:
            if x[0] == ad_input.type:
                filename += x[1]
                break
        #download_file(advertisement.ad_info.url, dir, filename)
        d = get_dict(advertisement)
        interactive_advertisement_collection.insert_one(dict(d))
        return id
    except:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail='An error happened, try again later')


def get_my_ads(username, limit, skip, interactive):
    collection = advertisement_collection
    if interactive:
        collection = interactive_advertisement_collection
    res =  limited_get(collection=collection, limit=limit, skip=skip, constraints= {"ad_info.advertiser_username" : username})
    ads = []
    for ad in res:
        if interactive:
            ads.append(toAdShow(ad, 1))
        else:
            ads.append(toAdShow(ad))
    return ads


def get_my_served_ads(username, limit, skip):
    res =  limited_get(collection=served_ad_collection, limit=limit, skip=skip, constraints= {"advertiser_username" : username})
    ads = []
    for ad in res:
        ads.append(toServedAd(ad))
    return ads



##admin uses
def get(constraints, limit, skip, interactive):
    collection = advertisement_collection
    if interactive:
        collection = interactive_advertisement_collection
    return limited_get(collection=collection, limit=limit, skip=skip, constraints= constraints)


def remove(constraints):
    gen.remove(advertisement_collection, constraints)
    





def get_ad(id, username):
    query = {"$and" : [{"ad_info.advertiser_username" : username}, {"id" : id}]}
    ad = gen.get_one(advertisement_collection, query)
    if ad:
        return toAdShow(ad)
    ad = gen.get_one(interactive_advertisement_collection, {"$and" : [{"ad_info.advertiser_username" : username}, {"id" : id}]})
    if ad:
        return toAdShow(ad, 1)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such id")


def get_served_ad(id, username):
    query = {"$and" : [{"advertiser_username" : username}, {"id" : id}]}
    ad = gen.get_one(served_ad_collection, query)
    if ad:
        return toServedAd(ad)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such id")


def toAdShow(ad, interactive = 0):
    if interactive:
        return  InteractiveAdvertisementShow(
                    id= ad["id"],
                    create_date=ad["create_date"],
                    target_user_info=ad["target_user_info"],
                    marketing_info=ad["marketing_info"],
                    ad_info=ad["ad_info"], 
                    categories=ad["categories"],
                    keywords=ad["keywords"]
                )
    return  AdvertisementShow(
                        id= ad["id"],
                        create_date=ad["create_date"],
                        target_user_info=ad["target_user_info"],
                        marketing_info=ad["marketing_info"],
                        ad_info=ad["ad_info"], 
                        categories=ad["categories"],
                        keywords=ad["keywords"]
            )


def toServedAd(served_ad):
    return ServedAd(
        id= served_ad["id"],
        agreed_cpc=served_ad["agreed_cpc"], 
        ad_id=served_ad["ad_id"], 
        impressions=served_ad["impressions"], 
        clicks=served_ad["clicks"],
        advertiser_username=served_ad["advertiser_username"]
        )


def get_tot_payment(username):
    tot = 0
    res = gen.get_many(served_ad_collection, {"advertiser_username" : username})
    for item in res:
        tot += int(item["clicks"]) * float(item["agreed_cpc"])
    return {"total" : tot}


def get_ad_payment(username, ad_id):
    tot = 0
    res = gen.get_many(served_ad_collection, {"$and" : [{"advertiser_username" : username}, {"ad_id" : ad_id}]})
    for item in res:
        tot += int(item["clicks"]) * float(item["agreed_cpc"])
    return {"total" : tot}