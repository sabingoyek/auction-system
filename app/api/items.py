import imp
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, deps, models, schemas

router = APIRouter()

@router.post("/auctions/{auction_id}/items/", response_model=schemas.Item, dependencies=[Depends(deps.get_current_user)],)
def create_item_for_auction(
    item: schemas.ItemCreate,
    auction_id: int,
    owner_id: int,
    db: Session = Depends(deps.get_db)):
    """
    Create an item for an auction
    
    Requires authentication and the item will be assigned to the auction. The current user must the owner of the auction.
    """
    # Check existence of the user
    user = crud.get_user(db, user_id=owner_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check existence of the auction
    auction = crud.get_auction(db, auction_id=auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    return crud.create_auction_item(db=db, item=item, auction_id=auction_id, owner_id=owner_id)

@router.get("/auctions/{auction_id}/items/", response_model=List[schemas.Item])
def read_auction_items(
    auction_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)):
    """
    Get the items of an auction.
    """
    # Check existence of the auction
    auction = crud.get_auction(db, auction_id=auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    return crud.get_auction_items(db=db,auction_id=auction_id, skip=skip, limit=limit)

@router.get("/items/", response_model=List[schemas.Item])
def read_all_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)):
    """
    Read all items.
    """
    return crud.get_items(db=db,skip=skip, limit=limit)

@router.get("/items/{item_id}/", response_model=schemas.Item)
def read_item(
    item_id: int,
    db: Session = Depends(deps.get_db)):
    """
    Read an items.
    """
    item = crud.get_item(db=db,item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/users/{user_id}/items/", response_model=List[schemas.Item])
def read_user_items(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)):
    """
    Read an user's items.
    """
    items = crud.get_user_items(db=db, user_id=user_id, skip=skip, limit=limit)
    return items