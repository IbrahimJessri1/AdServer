

from pydantic import BaseModel
from uuid import UUID , uuid4
from typing import Optional

from models.advertisement import AdType

class ServedAd(BaseModel):
    id: Optional[UUID] = uuid4()
    agreed_cpc: float
    ad_id: UUID
    impressions: int
    clicks: int
    advertiser_username : str
    payment_account:str
    create_date: str
    charges: float
    paid: float

class ServedAdShow(BaseModel):
    id:str
    agreed_cpc: float
    ad_id: UUID
    impressions: int
    clicks: int
    advertiser_username : str
    payment_account:str
    create_date: str
    charges: float
    paid: float
    url:str
    type: AdType