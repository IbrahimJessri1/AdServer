from asyncio import constants
from config.db import user_collection
from models.users import UserShow
from repositries import generics as gen
from .utilites import limited_get
from .hashing import Hash
from fastapi import HTTPException, status

def get_all(limit, skip, role):
    if role:
        constraints = {"role" : role}
    return limited_get(user_collection, limit=limit, skip=skip,constraints=constraints)


def remove(constraints):
    gen.remove(user_collection, constraints)



def update_account(user_update, username):
    try:
        query = { "username": username}
        in_values = {}
        in_values["password"] = Hash.bcrypt(user_update.password)
        new_values = { "$set": in_values }
        res = gen.update_one(user_collection, query, new_values)
        return UserShow(username=res["username"], role=res["role"], create_date=res["create_date"])
    except HTTPException as http_excep:
        raise http_excep    
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An Error Happaned, try again later") 


def delete_account(username):
    gen.remove(user_collection, {"username" : username})



def get(username):
    try:
        res = gen.get_one(user_collection, {"username" : username})
        return UserShow(username=res["username"], role=res["role"], create_date=res["create_date"])
    except HTTPException as http_excep:
        raise http_excep    
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An Error Happaned, try again later") 