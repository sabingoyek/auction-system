from datetime import datetime
from typing import List

from pydantic import BaseModel

class BidBase(BaseModel):
    id: int
    price: int 
    owner_id: int
    bid_date: datetime

    class Config:
        orm_mode = True

class BidCreate(BaseModel):
    price: int

class Bid(BidBase):
    auction_id: int

    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    id: int
    title: str
    description: str
    picture_url: str = None

    class Config:
        orm_mode = True

class ItemCreate(ItemBase):
    auction_id: int

class Item(BaseModel):
    id: int
    auction_id: int
    title: str
    description: str
    picture_url: str = None

    

    class Config:
        orm_mode = True

class AuctionBase(BaseModel):
    title: str
    description: str = None
    start_date: datetime
    

class AuctionCreate(AuctionBase):
    pass

class Auction(AuctionBase):
    id: int
    owner_id: int
    creation_date: datetime
    items: List[ItemBase] = []
    #item: Item = None
    bids: List[BidBase] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    auctions: List[Auction] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayLoad(BaseModel):
    sub: int