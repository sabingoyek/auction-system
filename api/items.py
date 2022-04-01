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
    owner: int = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)):
    """
    Create an item for an auction. The auction must not be published
    
    Requires authentication and the item will be assigned to the auction. The current user must the owner of the auction.
    """
    # Check existence of the auction
    db_auction = crud.get_auction(db, auction_id=auction_id)
    if not db_auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if db_auction.items:
        raise HTTPException(status_code=403, detail="Action forbidden: Auction already has an item.")
    if db_auction.is_published:
        raise HTTPException(status_code=403, detail="Can't create item for this auction: it is already published")
    return crud.create_auction_item(db=db, item=item, auction_id=auction_id, owner_id=owner.id)

@router.get("/auctions/{auction_id}/items/", response_model=List[schemas.Item])
def read_auction_items(
    auction_id: int,
    current_user = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)):
    """
    Get the items of an auction.
    Access to anyone if it is published.
    Otherwise only the owner of the auction can access to it or the owner of the auction that it belong to.
    """
    db_auction = crud.get_auction(db, auction_id=auction_id)
    if not db_auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if not db_auction.is_published:
        if db_auction.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not allowed to access these items: the auction are not yet published.")
        else:
            return crud.get_auction_items(db=db,auction_id=auction_id, skip=skip, limit=limit)
    else:
        return crud.get_auction_items(db=db,auction_id=auction_id, skip=skip, limit=limit)

@router.get("/items/", response_model=List[schemas.Item], dependencies=[Depends(deps.get_current_superuser)])
def read_all_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)):
    """
    Read all items. Published and Unpublished. Must be super user
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