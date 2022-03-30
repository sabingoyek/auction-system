from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, deps, models, schemas

router = APIRouter()

@router.post(
    "/items/{item_id}/bids",
    response_model=schemas.Bid,
    dependencies=[Depends(deps.get_current_user)],
)
def create_bid_for_item(
    bid: schemas.BidCreate,
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)):
    """
    Create an Bid for a specific item.

    Only allowed to an authenticated user. He will be it owner

    Also the item must exist.
    """
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.create_item_bid(db=db, bid=bid, item_id=item_id, owner_id=current_user.id)

@router.get("/items/{item_id}/bids/", response_model=List[schemas.Bid])
def read_bids_for_item(item_id: int, skip:int=0, limit:int=100, db: Session=Depends(deps.get_db)):
    """
    Read all the bids for a specific item.
    Does'nt require authentication.
    The item must exist.
    """
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    bids = crud.get_bids_for_item(db=db, item_id=item_id, skip=skip, limit=limit)
    return bids

@router.get("/bids/", response_model=List[schemas.Bid])
def read_all_bids(skip:int=0, limit:int=100, db: Session=Depends(deps.get_db)):
    """
    Read all bids
    Does'nt require authentication.
    """
    bids = crud.get_bids(db=db, skip=skip, limit=limit)
    return bids

@router.get("/bids/{bid_id}/", response_model=schemas.Bid)
def read_bid(bid_id: int, db: Session = Depends(deps.get_db)):
    """
    Read a bid. Doesn't nedd authentication.
    """
    bid = crud.get_bid(db, bid_id=bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    return bid

@router.get("/users/me/bids/", response_model=List[schemas.Bid], dependencies=[Depends(deps.get_current_user)])
def read_my_bids(skip: int = 0, limit: int = 100, current_user = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    """
    Read all my bids.
    """
    bids = crud.get_bids_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return bids

@router.get("/users/{user_id}/bids/", response_model=List[schemas.Bid])
def read_user_bids(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read all the bids of a specific user.
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    bids = crud.get_bids_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return bids

@router.get("/users/me/bids/{auction_id}", response_model=List[schemas.Bid], dependencies=[Depends(deps.get_current_user)])
def read_my_bids_for_auction(auction_id: int, skip: int = 0, limit: int = 100, current_user = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    """
    Read all my bids for an auction
    """
    db_auction = crud.get_auction(db=db, auction_id=auction_id)
    if db_auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    bids = crud.get_bids_by_user_for_auction(db, user_id=current_user.id, auction_id=auction_id, skip=skip, limit=limit)
    return bids
   
"""
@router.get("/users/{user_id}/bids/auction", response_model=List[schemas.Bid])
def read_user_bids_for_auction(user_id: int, auction_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    
    #Read all the bids of a specific user for an auction
    
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_auction = crud.get_auction(db=db, auction_id=auction_id)
    if db_auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    bids = crud.get_bids_by_user_for_auction(db, user_id=user_id, auction_id=auction_id, skip=skip, limit=limit)
    return bids
   """ 
@router.get("/users/{user_id}/bids/item", response_model=List[schemas.Bid])
def read_user_bids_for_item(user_id: int, item_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read all the bids of a specific an user for an item
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    bids = crud.get_bids_by_user_for_item(db, user_id=user_id, item_id=item_id, skip=skip, limit=limit)
    return bids