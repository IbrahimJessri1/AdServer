from pydoc import cli
import shutil
from tempfile import gettempdir
from uuid import uuid4
from fastapi import HTTPException, status
from config.db import advertisement_collection, interactive_advertisement_collection
from repositries import generics as gen
from models.advertisement import AdInfo, Advertisement, InteractiveAdvertisementInput, MarketingInfo, InteractiveAdInfo, InteractiveAdvertisement, InteractiveMarketingInfo, AdType
import datetime
from .utilites import get_dict
import requests
import os



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


##admin uses
def get_all():
    return gen.get_many(advertisement_collection, {})

def get_my_ads(username):
    return gen.get_many(advertisement_collection, {"ad_info.advertiser_username" : username})


def remove(constraints):
    gen.remove(advertisement_collection, constraints)
    


def download_file(URL, dir, filename):
    os.makedirs(dir, exist_ok=True) 
    path = dir + "/" + filename
    response = requests.get(URL)
    open(path, "wb").write(response.content)