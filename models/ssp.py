from unicodedata import category
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List
from models.advertisement import AdType, Category, Shape


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

class Ad_Request(BaseModel):
    min_cpc: float
    user_info: Optional[UserInfo] = None
    categories: Optional[List[Category]] = []
    type: AdType
    keywords: Optional[List[str]] = []
    shape: Shape

class ApplyAd(BaseModel):
    cpc: float
    ad_id: str
    payment_account:str
    max_width:int
    max_height:int