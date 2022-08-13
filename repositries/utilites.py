from pydantic import BaseModel
from enum import Enum
from uuid import UUID
import random
from models.ssp import UserInfo
from models.advertisement import Language, TargetAge
from repositries import generics as gen
import requests, os

def get_dict(obj):
    res = {}
    for att in dir(obj):
        if att.startswith('__') or att in dir(BaseModel) or att in dir(Enum) or att in dir(str) or att in dir(UUID):
            continue
        value = getattr(obj, att)
        if type(value).__name__ == 'int':
            res[att] = value
        elif type(value).__name__ == 'float':
            res[att] = value
        elif type(value).__name__ == 'list':
            res[att] = value
        elif type(value).__name__ == 'str':
            res[att] = value
        elif issubclass(type(value), UUID):
            res[att] = str(value)
        elif issubclass(type(value), Enum):
            res[att] = value.value
        else:
            res[att] = get_dict(value)
    return res



def probability_get(param):
    sum = 0
    for t in param:
        sum += t[1]
    param.sort(key= lambda x : x[1])
    val = random.uniform(0, sum)
    yet = 0
    for t in param:
        yet += t[1]
        if yet >= val:
            return t[0]

def rand(start, end, decimal_places):
    return  round(random.uniform(start, end), decimal_places)


gender_weight = 1
age_weight = 1
language_weight = 1
location_weight = 1



def get_weight_user_info(user_info : UserInfo, ad):
    total_weight = 0
    weight_gained = 0
    if user_info is not None:
            if user_info.gender is not None:
                total_weight += gender_weight
                if user_info.gender.value == ad["target_user_info"]["gender"]:
                    weight_gained += gender_weight
                elif 'both'== ad["target_user_info"]["gender"]:
                    weight_gained += gender_weight/2

            if user_info.age is not None:
                total_weight += age_weight
                if TargetAge.ALL_AGES in ad["target_user_info"]["age"]:
                    weight_gained += 3 * age_weight / 4
                else:
                    required_age = ""
                    if user_info.age <= 12:
                        required_age = TargetAge.KID
                    elif user_info.age <= 39:
                        required_age = TargetAge.YOUTH
                    elif user_info.age <= 55:
                        required_age = TargetAge.ADULT
                    else:
                        required_age = TargetAge.OLD
                    if required_age in ad["target_user_info"]["age"]:
                        weight_gained += age_weight

            if user_info.language is not None:
                total_weight += language_weight
                if ad["target_user_info"]["language"] == Language.ANY:
                    weight_gained += 3 * language_weight / 4
                elif ad["target_user_info"]["language"] == user_info.language:
                    weight_gained += language_weight
            if user_info.location is not None:
                total_weight += location_weight
                if ad["target_user_info"]["location"].lower() == user_info.location.lower():
                    weight_gained += location_weight
                elif ad["target_user_info"]["location"].lower() == 'any':
                    weight_gained += 3*location_weight/4
    if total_weight == 0:
        return -1
    return weight_gained * 100 / total_weight



def limited_get(collection , limit, skip, constraints):
    all_items = gen.get_many(collection, constraints)
    count = len(all_items) 
    if skip > count:
        return []
    if limit == -1:
        limit = count
    begin = skip
    end = min(count, begin + limit)
    return all_items[begin:end]



def download_file(URL, dir, filename):
    os.makedirs(dir, exist_ok=True) 
    path = dir + "/" + filename
    response = requests.get(URL)
    open(path, "wb").write(response.content)