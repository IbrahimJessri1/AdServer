from uuid import UUID, uuid4
from pydantic import UUID4, BaseModel
from enum import Enum
from typing import List, Optional
from fastapi import UploadFile


class Category(str, Enum):
    ANY= "any"
    PLACES= "places"
    Technology= "technology"
    HEALTHCARE = "healthcare"
    APPS= "apps"
    TOYS=  "toys"
    GAMING= "gaming"
    EDUCATION = "education"
    VEHICLES= "vehicles"
    NATURE= "nature"
    FOOD= "food"
    SMARTPHONES= "smartphones"
    CARS= "cars"
    PRODUCTS= "products"
    WEBSITES= "websites"
    BIKES= "bikes"
    SCHOOL= "school"
    BOOKS= "books"
    ELECTRONICS= "electronics"
    HOUSE= "house"
    FURNITURE= "furniture"
    FAMILY= "family"
    CLOTHES= "clothes"
    WEARBLE= "wearable"
    ANIMALS= "animals"
    MEDIA= "media"
    JOBS= "jobs"

class Language(str, Enum):
    ANY = "any"
    EN = "en"
    AR = "ar"

class TargetAge(str, Enum):
    ALL_AGES= "all ages"
    KID= "kids"
    YOUTH= "youths"
    ADULT = "adults"
    OLD = "old people"

class TargetGender(str, Enum):
    BOTH="both"
    MALE= "male"
    FEMALE= "female"

class TargetUserInfo(BaseModel):
    location:str
    gender:TargetGender
    age: List[TargetAge]
    language: Language

class AdType(str, Enum):
    IMAGE= "image"
    VIDEO= "video"

class AdInfo(BaseModel):
    type : AdType
    advertiser_username: str
    url: str
    text: str
    width: int
    height: int

class InteractiveAdInfo(BaseModel):
    type : AdType
    advertiser_username: str
    url: str
    redirect_url : str
    text: str
    width: int
    height: int

class MarketingInfo(BaseModel):
    max_cpc : float
    impressions : int
    raise_percentage: float


class InteractiveMarketingInfo(BaseModel):
    max_cpc : float
    impressions : int
    clicks: int
    raise_percentage: float

class AdvertisementInput(BaseModel):
    target_user_info: TargetUserInfo
    max_cpc: float
    type: AdType
    categories: List[Category]
    url:str
    raise_percentage: float
    keywords: Optional[List[str]] = None
    text: str
    width: int
    height: int

class InteractiveAdvertisementInput(BaseModel):
    target_user_info: TargetUserInfo
    max_cpc: float
    type: AdType
    categories: List[Category]
    url:str
    redirect_url:str
    raise_percentage: float
    keywords: Optional[List[str]] = None
    text: str
    width:int
    height:int 


class Advertisement(BaseModel):
    id:Optional[UUID] = uuid4()
    create_date: str
    target_user_info: TargetUserInfo
    marketing_info: MarketingInfo
    ad_info: AdInfo
    categories: List[Category]
    keywords: Optional[List[str]] = None

class InteractiveAdvertisement(BaseModel):
    id:Optional[UUID] = uuid4()
    create_date: str
    target_user_info: TargetUserInfo
    marketing_info: InteractiveMarketingInfo
    ad_info: InteractiveAdInfo
    categories: List[Category]
    keywords: Optional[List[str]] = None
    

class AdvertisementShow(BaseModel):
    id: str
    create_date: str
    target_user_info: TargetUserInfo
    marketing_info: MarketingInfo
    ad_info: AdInfo
    categories: List[Category]
    keywords: Optional[List[str]] = None


class InteractiveAdvertisementShow(BaseModel):
    id: str
    create_date: str
    target_user_info: TargetUserInfo
    marketing_info: InteractiveMarketingInfo
    ad_info: InteractiveAdInfo
    categories: List[Category]
    keywords: Optional[List[str]] = None


class adLimitedGet(BaseModel):
    limit: Optional[int] = -1
    skip: Optional[int] = 0
    interactive: int = 0
    constraints : Optional[dict] = {}


