from hashlib import new
from uuid import uuid4
from fastapi import HTTPException, status
from config.db import advertisement_collection, interactive_advertisement_collection, served_ad_collection
from models.ads_stats import ServedAdShow
from repositries import generics as gen
from models.advertisement import AdInfo, AdUpdate, Advertisement, AdvertisementShow, InteractiveAdvertisementInput, MarketingInfo, InteractiveAdvertisement, InteractiveMarketingInfo, AdType, InteractiveAdvertisementShow
import datetime
from .utilites import get_dict, limited_get, download_file


def create_ad(ad_input, advertiser_username, interactive = 0):
    try:
        create_date = str(datetime.datetime.now())
        ad_info = AdInfo(type = ad_input.type, advertiser_username=advertiser_username, text=ad_input.text,  width=ad_input.width, height=ad_input.height, shape=ad_input.shape)
        id = str(uuid4())
        if interactive:
            advertisement = InteractiveAdvertisement(
                id= id,
                create_date = create_date,
                target_user_info=ad_input.target_user_info, 
                marketing_info=InteractiveMarketingInfo(max_cpc= ad_input.max_cpc,impressions= 0, clicks=0, raise_percentage=ad_input.raise_percentage,tot_charges=0,tot_paid=0),
                ad_info= ad_info,
                categories=ad_input.categories,
                url= ad_input.url,
                redirect_url=ad_input.redirect_url,
                keywords=ad_input.keywords
            )
            collection = interactive_advertisement_collection
        else:
            advertisement = Advertisement(
                id= id,
                create_date = create_date,
                target_user_info=ad_input.target_user_info, 
                marketing_info=MarketingInfo(max_cpc= ad_input.max_cpc,impressions= 0, raise_percentage=ad_input.raise_percentage,tot_charges=0,tot_paid=0),
                ad_info= ad_info,
                categories=ad_input.categories,
                url= ad_input.url,
                keywords=ad_input.keywords
            )
            collection = advertisement_collection
        ad = get_dict(advertisement)
        collection.insert_one(dict(ad))
        return id
    except:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail='An error happened, try again later')


def get_my_ads(username, limit, skip, interactive, type, shape):
    constraints = {"ad_info.advertiser_username" : username}
    if type != 'all':
        constraints = {"$and" : [constraints, {"ad_info.type" : type}]}
    if shape != 'all':
        constraints = {"$and" : [constraints, {"ad_info.shape" : shape}]}
    if interactive == 2:
        res1 = limited_get(collection=interactive_advertisement_collection, limit=limit, skip=skip, constraints= constraints)
        res2 = limited_get(collection=advertisement_collection, limit=limit, skip=skip, constraints= constraints)
        ads = []
        for ad in res1:
            ads.append(toAdShow(ad, 1))
        for ad in res2:
            ads.append(toAdShow(ad, 0))
        return ads
    else:
        collection = advertisement_collection
        if interactive == 1:
            collection = interactive_advertisement_collection
        res =  limited_get(collection=collection, limit=limit, skip=skip, constraints= constraints)
        ads = []
        for ad in res:
            ads.append(toAdShow(ad, interactive))
        return ads


def get_my_served_ads(username, limit, skip):
    res =  limited_get(collection=served_ad_collection, limit=limit, skip=skip, constraints= {"advertiser_username" : username})
    ads = []
    for ad in res:
        real_ad = get_ad(ad['ad_id'], username)
        url =  real_ad.url
        type= real_ad.ad_info.type
        ads.append(toServedAdShow(ad,url, type))
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
    ad = gen.get_one(interactive_advertisement_collection, query)
    if ad:
        return toAdShow(ad, 1)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such id")


def get_served_ad(id, username):
    query = {"$and" : [{"advertiser_username" : username}, {"id" : id}]}
    ad = gen.get_one(served_ad_collection, query)
    if ad:
        real_ad = get_ad(ad['ad_id'], username)
        url =  real_ad.url
        type= real_ad.ad_info.type
        return toServedAdShow(ad,url, type)
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
                    keywords=ad["keywords"],
                    url = ad["url"],
                    redirect_url=ad["redirect_url"],
                    tot_charges=ad['marketing_info']['tot_charges'],
                    tot_paid=ad['marketing_info']['tot_paid']
                )
    # try:
    return  AdvertisementShow(
                    id= ad["id"],
                    create_date=ad["create_date"],
                    target_user_info=ad["target_user_info"],
                    marketing_info=ad["marketing_info"],
                    ad_info=ad["ad_info"], 
                    categories=ad["categories"],
                    keywords=ad["keywords"],
                    url = ad["url"],
                    tot_charges=ad['marketing_info']['tot_charges'],
                    tot_paid=ad['marketing_info']['tot_paid']
            )
    # except Exception as e:
    #     raise e


def update_ad(ad_update : AdUpdate, username):
    query = {"$and" : [{"ad_info.advertiser_username" : username}, {"id" : ad_update.id}]}
    collection = ""
    ad = gen.get_one(advertisement_collection, query)
    if ad:
        collection = advertisement_collection
    else:
        ad = gen.get_one(interactive_advertisement_collection, query)
        if ad:
            collection = interactive_advertisement_collection
    if collection == "":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    new_values = {
        "$set" : {
            "target_user_info.age" : ad_update.target_user_info.age,
            "target_user_info.location" : ad_update.target_user_info.location,
            "target_user_info.gender" : ad_update.target_user_info.gender.value,
            "target_user_info.language" : ad_update.target_user_info.language.value,
            "marketing_info.max_cpc": ad_update.max_cpc,
            "categories": ad_update.categories,
            "marketing_info.raise_percentage": ad_update.raise_percentage,
            "keywords": ad_update.keywords,
            "text": ad_update.text,
            "ad_info.width": ad_update.width,
            "ad_info.height": ad_update.height,
            "ad_info.shape": ad_update.shape
        }
    }
    gen.update_many(collection=collection, query=query, new_values=new_values)



def toServedAdShow(served_ad, payment, url, type):
    return ServedAdShow(
            id=served_ad["id"],
            create_date= served_ad["create_date"],
            agreed_cpc=served_ad["agreed_cpc"], 
            ad_id=served_ad["ad_id"], 
            impressions=served_ad["impressions"], 
            clicks=served_ad["clicks"],
            advertiser_username=served_ad["advertiser_username"],
            payment_account=served_ad["payment_account"],
            charges= served_ad['charges'],
            paid=served_ad['paid'],
            url= url,
            type=type
        )


def get_tot_payment(username):
    tot = 0
    res = gen.get_many(served_ad_collection, {"advertiser_username" : username})
    for item in res:
        tot+= item['charges']
    return tot


def get_ad_payment(username, ad_id):
    tot = 0
    res = gen.get_many(served_ad_collection, {"$and" : [{"advertiser_username" : username}, {"ad_id" : ad_id}]})
    for item in res:
        tot+= item['charges']
    return tot



