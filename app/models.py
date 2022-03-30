<<<<<<< HEAD
import email
from email.policy import default
from enum import unique
from operator import index
from xmlrpc.client import DateTime
=======
from datetime import datetime
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    auctions = relationship("Auction", back_populates="owner")
    bids = relationship("Bid", back_populates="owner")

class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(String)
<<<<<<< HEAD
    creation_date = Column(String)

    owner = relationship("User", back_populates="auctions")
    bids = relationship("Bid", back_populates="auction")

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    bid_date = Column(String)
    price = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    auction_id = Column(Integer, ForeignKey("auctions.id"))

    auction = relationship("Auction", back_populates="bids")

=======
    is_active = Column(Boolean, default=False)
    creation_date = Column(String, default=datetime.now())

    owner = relationship("User", back_populates="auctions")
    items = relationship("Item", back_populates="auction")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    start_price= Column(Integer)
    picture_url = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    auction_id = Column(Integer, ForeignKey("auctions.id"))

    auction = relationship("Auction", back_populates="items")
    bids = relationship("Bid", back_populates="item")

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    bid_date = Column(String, default=datetime.now())
    price = Column(Integer)
    bidder_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    item = relationship("Item", back_populates="bids")
    owner = relationship("User", back_populates="bids")
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf
