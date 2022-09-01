from models.users import Advertiser, AdvertiserShow, Role
from fastapi import HTTPException, status
from config.db import user_collection
from repositries import generics as gen
from .hashing import Hash
import datetime


def signup(advertiser : Advertiser):
    try:
        collection = user_collection
        user = gen.get_one(collection, {"username" : advertiser.username})
        if user:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="username taken!")
        advertiser.password = Hash.bcrypt(advertiser.password)
        user = dict(advertiser)
        user["role"] = Role.ADVERTISER.value
        user["create_date"] = str(datetime.datetime.now())
        collection.insert_one(user)
        inserted = gen.get_one(collection, {"username" : advertiser.username})
        return AdvertiserShow(username = inserted["username"], role = inserted["role"], membership = inserted["membership"], create_date = inserted["create_date"])
    except HTTPException as http_excep:
        raise http_excep    
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An Error Happaned, try again later") 




def update_adv_account(advertiser_update, username):
    try:
        query = { "username": username}
        in_values = {}
        if advertiser_update.membership is not None:
            in_values["membership"] = advertiser_update.membership.value
        if advertiser_update.password is not None:
            in_values["password"] = Hash.bcrypt(advertiser_update.password)
        new_values = { "$set": in_values }
        res = gen.update_one(user_collection, query, new_values)
        return AdvertiserShow(username=res["username"], role=res["role"], membership = res["membership"], create_date=res["create_date"])
    except HTTPException as http_excep:
        raise http_excep    
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An Error Happaned, try again later") 



def get(username):
    try:
        res = gen.get_one(user_collection, {"username" : username})
        return AdvertiserShow(username=res["username"], role=res["role"], membership = res["membership"], create_date=res["create_date"])
    except HTTPException as http_excep:
        raise http_excep    
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An Error Happaned, try again later")   




