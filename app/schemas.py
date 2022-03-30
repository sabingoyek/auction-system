from datetime import datetime
from typing import List

from pydantic import BaseModel
from datetime import datetime

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

class BidBase(BaseModel):
    price: int 

class BidCreate(BidBase):
    pass

class Bid(BidBase):
    id: int
    auction_id: int
    owner_id: int
    bid_date: datetime

    class Config:
        orm_mode = True

class AuctionBase(BaseModel):
    title: str
    description: str = None
<<<<<<< HEAD
    start_date: datetime
    
=======
    start_date: datetime = None
    is_active: bool = False
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf

class AuctionCreate(AuctionBase):
    pass

class Auction(AuctionBase):
    id: int
<<<<<<< HEAD
    owner_id: int
    creation_date: datetime
    bids: List[Bid] = []

=======
    owner_id: int           # path parameter
    creation_date: datetime
    items: List[Item] = []
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf
    class Config:
        orm_mode = True

class UserBase(BaseModel):
<<<<<<< HEAD
    first_name: str
=======
    first_name:str
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf
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
