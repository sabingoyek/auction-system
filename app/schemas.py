from typing import List

from pydantic import BaseModel

class AuctionBase(BaseModel):
    title: str
    description: str = None

class AuctionCreate(AuctionBase):
    pass

class Auction(AuctionBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
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