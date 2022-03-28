from sqlalchemy.orm import Session

import models, schemas, security

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int, limit: int):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email:str, password: str):
    user = get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

def get_auctions(db: Session, skip:int=0, limit: int = 100):
    return db.query(models.Auction).offset(skip).limit(limit).all()

def create_user_auction(db: Session, auction: schemas.AuctionCreate, user_id: int):
    db_auction = models.Auction(**auction.dict(), owner_id=user_id)
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    return db_auction
