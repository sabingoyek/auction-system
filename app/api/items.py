import imp
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, deps, models, schemas

router = APIRouter()

<<<<<<< HEAD
@router.post(
    "/users/{user_id}/items",
    response_model=schemas.Item,
    dependencies=[Depends(deps.get_current_superuser)],
)
def create_auction_for_user(
    user_id: int, Item: schemas.ItemCreate, db: Session = Depends(deps.get_db)):
    """
    Create an Item for a specific user.

    Only allowed to the super user
    The user must exist
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not exist")
    return crud.create_user_auction(db=db, Item=Item, user_id=user_id)

@router.post("/items/", response_model=schemas.Item)
def create_auction_for_current_user(
    Item: schemas.ItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)):
    """
    Create an Item
    
    Requires authentication and the Item will be assigned to the current user.
    """
    return crud.create_user_auction(db=db, Item=Item, user_id=current_user.id)

@router.get("/items/", response_model=List[schemas.Item])
def read_auctions(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read all the items. Doesn't need authentication.
    """
    items = crud.get_auctions(db, skip=skip, limit=limit)
    return items

@router.get("/items/{item_id}/", response_model=schemas.Item)
def read_auction(item_id: int, db: Session = Depends(deps.get_db)):
    """
    Read a Item. Doesn't nedd authentication.
    """
    Item = crud.get_auction(db, item_id=item_id)
    return Item
=======
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
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf
