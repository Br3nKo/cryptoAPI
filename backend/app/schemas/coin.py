from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from typing import List

class CoinBase(BaseModel):
    id: str
    symbol: str
    name: str
    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    total_volume: Optional[float] = None
    circulating_supply: Optional[float] = None
    high_24h: Optional[float] = None
    low_24h: Optional[float] = None
    last_updated: Optional[datetime] = None

    class Config:
        orm_mode = True

class CoinCreate(BaseModel):
    """Schema for creating a new coin entry in the database"""
    symbol: str
    name: str

class CoinResponse(CoinBase):
    """Schema for API responses when returning coin data"""
    pass

class CoinsResponse(BaseModel):
    """Schema for API response when returning a list of all coins"""
    coins: List[CoinBase]

    class Config:
        orm_mode = True