

from pydantic import BaseModel
from uuid import UUID , uuid4
from typing import Optional

class Served_Ad(BaseModel):
    id: Optional[UUID] = uuid4()
    agreed_cpc: float
    ad_id: UUID
    impressions: int
    clicks: int