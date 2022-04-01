from typing import List

from pydantic import BaseModel
from datetime import datetime

AUCTION_NUMBER = 0

class BidBase(BaseModel):
    price: int
#   bidder_id: int  # get current user 

class BidCreate(BidBase):
    pass

class Bid(BidBase):
    id: int
    bidder_id: int
    item_id: int        # path parameter
    bid_date: datetime
    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    title: str
    description: str
    start_price: int
    picture_url: str = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int
    auction_id: int
    bids: List[Bid] = []

    class Config:
        orm_mode = True

class AuctionBase(BaseModel):
    title: str
    description: str = None

class AuctionCreate(AuctionBase):
    pass

class AuctionUpdate(BaseModel):
    is_published: bool = True

class Auction(AuctionBase):
    id: int
    owner_id: int           # path parameter
    creation_date: datetime
    start_date: datetime = None
    end_date: datetime = None
    is_published: bool = False
    is_active: bool = False
    items: List[Item] = []
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    first_name:str
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


class TokenPayload(BaseModel):
    sub: int


