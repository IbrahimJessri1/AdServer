from unicodedata import category
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List

from models.advertisement import AdType


class Gender(str, Enum):
    MALE= "male"
    FELMALE= "female"




class Language(str, Enum):
    EN= "en"
    AR = "ar"


class UserInfo(BaseModel):
    location: Optional[str] = None
    gender: Optional[Gender] = None
    age: Optional[int] = None
    language: Optional[Language] = None

    
class Category(str, Enum):
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
    MEDIA = "media"
    JOBS= "jobs"


class Ad_Request(BaseModel):
    min_cpc: float
    user_info: Optional[UserInfo] = None
    categories: Optional[List[Category]] = []
    type: AdType
    keywords: Optional[List[str]] = []

class ApplyAd(BaseModel):
    cpc: float
    ad_id: str