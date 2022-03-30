from datetime import datetime
from sqlalchemy.orm import Session

import models, schemas, security


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
<<<<<<< HEAD
    db_user = models.User(first_name=user.first_name, last_name=user.last_name,email=user.email, hashed_password=hashed_password)
=======
    db_user = models.User(
        email=user.email,
        first_name = user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password)
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_auctions(db: Session, skip:int=0, limit: int = 100):
    return db.query(models.Auction).offset(skip).limit(limit).all()

<<<<<<< HEAD
=======
def get_user_auctions(db: Session, user_id: int, skip:int=0, limit: int = 100):
    return db.query(models.Auction).filter(models.Auction.owner_id == user_id).offset(skip).limit(limit).all()

>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf
def get_auction(db: Session, auction_id: int):
    return db.query(models.Auction).filter(models.Auction.id == auction_id).first()

def create_user_auction(db: Session, auction: schemas.AuctionCreate, user_id: int):
    creation_date= datetime.now()
    db_auction = models.Auction(**auction.dict(), owner_id=user_id, creation_date=creation_date)
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    return db_auction

<<<<<<< HEAD
def create_auction_bid(db: Session, bid: schemas.Bid, auction_id: int, owner_id: int):
    bid_date = datetime.now()
    db_bid = models.Bid(**bid.dict(), auction_id=auction_id, owner_id=owner_id, bid_date=bid_date)
=======
def get_auction_items(db: Session, auction_id: int, skip:int, limit:int):
    return db.query(models.Item).filter(models.Item.auction_id == auction_id).offset(skip).limit(limit).all()

def create_auction_item(db: Session, item: schemas.ItemCreate, auction_id:int, owner_id: int):
    db_item = models.Item(**item.dict(), auction_id=auction_id, owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session,skip:int, limit:int):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_user_items(db: Session, user_id: int, skip:int, limit:int):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).offset(skip).limit(limit).all()

def create_item_bid(db: Session, bid: schemas.Bid, item_id: int, owner_id: int):
    bid_date = datetime.now()
    db_bid = models.Bid(**bid.dict(), item_id=item_id, bidder_id=owner_id, bid_date=bid_date)
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    return db_bid

<<<<<<< HEAD
def get_bids(db: Session, auction_id:int, skip:int, limit:int):
    return db.query(models.Bid).filter(models.Bid.auction_id == auction_id).offset(skip).limit(limit).all()
=======
def get_bids_for_item(db:Session, item_id:int, skip:int, limit:int):
    return db.query(models.Bid).filter(models.Bid.item_id == item_id).offset(skip).limit(limit).all()

def get_bids(db: Session, skip:int, limit:int):
    return db.query(models.Bid).offset(skip).limit(limit).all()
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf

def get_bid(db: Session, bid_id: int):
    return db.query(models.Bid).filter(models.Bid.id == bid_id).first()

def get_bids_by_user(db: Session, user_id: int, skip:int, limit:int):
<<<<<<< HEAD
    return db.query(models.Bid).filter(models.Bid.owner_id == user_id).offset(skip).limit(limit).all()

def get_bids_by_user_for_auction(db: Session, user_id: int, auction_id: int, skip:int, limit:int):
    return db.query(models.Bid).filter(models.Bid.owner_id == user_id and models.Bid.auction_id == auction_id).offset(skip).limit(limit).all()
=======
    return db.query(models.Bid).filter(models.Bid.bidder_id == user_id).offset(skip).limit(limit).all()

def get_bids_by_user_for_auction(db: Session, user_id: int, auction_id: int, skip:int, limit:int):
    return db.query(models.Bid).filter(models.Bid.bidder_id == user_id and models.Bid.auction_id == auction_id).offset(skip).limit(limit).all()
"""
def get_bids_by_user_for_auction(db: Session, user_id: int, auction_id: int, skip:int, limit:int):
    return db.query(models.Bid).filter(models.Bid.bidder_id == user_id ).filter(models.Bid.auction_id == auction_id).offset(skip).limit(limit).all()
"""
def get_bids_by_user_for_item(db: Session, user_id: int, item_id: int, skip:int, limit:int):
    return db.query(models.Bid).filter(models.Bid.bidder_id == user_id).filter(models.Bid.item_id == item_id).offset(skip).limit(limit).all()
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf
