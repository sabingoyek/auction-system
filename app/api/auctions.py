import imp
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, deps, models, schemas

router = APIRouter()

@router.post(
    "/users/{user_id}/auctions",
    response_model=schemas.Auction,
    dependencies=[Depends(deps.get_current_superuser)],
)
def create_auction_for_user(
    user_id: int, auction: schemas.AuctionCreate, db: Session = Depends(deps.get_db)):
    """
    Create an Auction for a specific user.

    Only allowed to the super user
    The user must exist
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not exist")
    return crud.create_user_auction(db=db, auction=auction, user_id=user_id)

@router.post("/auctions/", response_model=schemas.Auction)
def create_auction_for_current_user(
    auction: schemas.AuctionCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)):
    """
    Create an auction
    
    Requires authentication and the auction will be assigned to the current user.
    """
    return crud.create_user_auction(db=db, auction=auction, user_id=current_user.id)

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
    return auction

