import imp
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, deps, models, schemas

router = APIRouter()

@router.post("/users/{user_id}/auctions/", response_model=schemas.Auction, dependencies=[Depends(deps.get_current_user)],)
def create_auction_for_user(
    auction: schemas.AuctionCreate,
    user_id: int,
    db: Session = Depends(deps.get_db)):
    """
    Create an auction
    
    Requires authentication and the auction will be assigned to the current user.
    """
    if not crud.get_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_auction(db=db, auction=auction, user_id=user_id)

@router.get("/users/{user_id}/auctions/", response_model=List[schemas.Auction])
def read_user_auctions(user_id: int,skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read all the auctions of a specific user. Doesn't need authentication.
    """
    if not crud.get_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    auctions = crud.get_user_auctions(db, user_id=user_id, skip=skip, limit=limit)
    return auctions


@router.get("/auctions/", response_model=List[schemas.Auction])
def read_auctions(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read all the auctions. Doesn't need authentication.
    """
    auctions = crud.get_auctions(db, skip=skip, limit=limit)
    return auctions

@router.get("/auctions/{auction_id}/", response_model=schemas.Auction)
def read_auction(auction_id: int, db: Session = Depends(deps.get_db)):
    """
    Read a auction. Doesn't nedd authentication.
    """
    auction = crud.get_auction(db, auction_id=auction_id)
    if auction:
        return auction
    raise HTTPException(status_code=404, detail="Auction not found")
