from re import M
from typing import List
from pydantic import BaseModel
from enum import Enum
from typing import Optional

class Membership(str, Enum):
    NORMAL = "NORMAL" #0.2
    PREMIUM = "PREMIUM" #0.35
    VIP = "VIP" #0.45


class MembershipMarks(str, Enum):
    NORMAL = 50
    PREMIUM = 70
    VIP = 100


class Role(str, Enum):
    ADVERTISER = "advertiser"
    ADMIN = "admin"

class User(BaseModel):
    username: str
    password:str
    role: Role
    create_date: str


class UserShow(BaseModel):
    username: str
    role : Role
    create_date:str

class Admin(User):
    pass


class Advertiser(BaseModel):
    username: str
    password:str
    membership:Membership

class AdvertiserShow(BaseModel):
    username: str
    membership: Membership
    create_date:str
    role:Role


class UserUpdate(BaseModel):
    password:str
    

class AdvertiserUpdate(BaseModel):
    password:Optional[str] = None
    membership:Optional[Membership] = None

