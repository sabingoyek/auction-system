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
    
    db_auction = crud.get_auction(db, auction_id=auction_id)
    if not db_auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if db_auction.items:
        raise HTTPException(status_code=403, detail="Action forbidden: Auction already has an item.")
    if db_auction.owner_id != owner.id:
        raise HTTPException(status_code=403, detail="Action forbidden: you are not the owner ot this auction")
    if db_auction.is_published:
        raise HTTPException(status_code=403, detail="Can't create item for this auction: it is already published")
    return crud.create_auction_item(db=db, item=item, auction_id=auction_id, owner_id=owner.id)

@router.get("/auctions/{auction_id}/items/", response_model=List[schemas.Item])
def read_auction_items(
    auction_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)):
    """
    Get the items of an published auction.
    """
    db_auction = crud.get_auction(db, auction_id=auction_id)
    if not db_auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if not db_auction.is_published:
        raise HTTPException(status_code=403, detail="You are not allowed to access these items: the auction are not yet published.")
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
def read_item(item_id:int, db: Session = Depends(deps.get_db)):
    """
    Read an item.
    """
    item = crud.get_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_published_status = crud.get_auction_published_status(db, item.auction_id).is_published
    if not item_published_status:
        raise HTTPException(status_code=403, detail="Action forbidden: Item not published yet.")
    return item

@router.get("/items/{item_id}/winner/", response_model=schemas.UserBase)
def read_item_winner(item_id:int, db: Session = Depends(deps.get_db)):
    """
    Read the winner of an item.
    """
    item = crud.get_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_active_status = crud.get_auction_active_status(db, item.auction_id).is_active
    if item_active_status:
        raise HTTPException(status_code=403, detail="Action forbidden: Auction that this article belong to is not over yet.")
    item_highest_bid = crud.get_highest_bid_by_item(db=db, item_id=item_id)
    return crud.get_user(db=db, user_id=item_highest_bid.bidder_id)


@router.get("/users/me/items/",response_model=List[schemas.Item], dependencies=[Depends(deps.get_current_user)])
def read_my_items(
    current_user: schemas.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)):
    """
    Read the connected user's items.
    """
    items = crud.get_user_items(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return items

@router.get("/users/me/items/{item_id}/",response_model=schemas.Item, dependencies=[Depends(deps.get_current_user)])
def read_my_item(
    item_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)):
    """
    Read the connected user's items.
    """
    item = crud.get_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Action forbidden: your are not the owner of this item.")
    return item

@router.get("/users/me/auctions/{auction_id}/items/",response_model=List[schemas.Item], dependencies=[Depends(deps.get_current_user)])
def read_my_items_by_auction(
    auction_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)):
    """
    Read the connected user's items by auction.
    """
    item_auction = crud.get_auction(db, auction_id=auction_id)
    if not item_auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    items = crud.get_user_items_by_auction(db=db, user_id=current_user.id, auction_id=auction_id, skip=skip, limit=limit)
    return items

@router.patch("/user/me/items/{item_id}/",response_model=schemas.Item, dependencies=[Depends(deps.get_current_user)])
def update_my_item(
    item_id: int,
    item: schemas.ItemBase,
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)):
    """
    Update the item
    """
    db_item = crud.get_item(db, item_id = item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Action forbidden: your are not the owner of this item.")
    item_auction = crud.get_auction(db, auction_id=db_item.auction_id)
    if item_auction.is_published:
        raise HTTPException(status_code=403, detail="Item already published.")
    
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/user/me/items/{item_id}", dependencies=[Depends(deps.get_current_user)])
def delete_item(item_id: int, user: schemas.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    """Delete an unpublished item. The performer must be its owner. 
    """
    db_item = crud.get_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if  db_item.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Action forbidden: Your aren't the owner of this item")
    item_auction = crud.get_auction(db, auction_id=db_item.auction_id)
    if item_auction.is_published:
        raise HTTPException(status_code=403, detail="Item already published.")
    db.delete(db_item)
    db.commit()
    return {"ok": True}