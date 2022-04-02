from operator import attrgetter
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

    Also the item must exist and the auction that it belong is not over.
    """
    db_item = crud.get_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_status = crud.get_auction_active_status(db=db, auction_id=db_item.auction_id).is_active
    if not item_status:
        raise HTTPException(status_code=403, detail="Auction that belong this item is not active.")
    if db_item.bids:
        current_highest_bid = crud.get_highest_bid_by_item(db=db,item_id=item_id)
        if current_highest_bid.price > bid.price:
            raise HTTPException(status_code=403, detail="Action forbidden: Current highest bid(" + str(current_highest_bid.price) +") is greater than your bid.")
    return crud.create_item_bid(db=db, bid=bid, item_id=item_id, owner_id=current_user.id)

@router.get("/items/{item_id}/bids/", response_model=List[schemas.Bid])
def read_bids_for_item(item_id: int, order_by: schemas.BidOrder = "price", desc_order: bool = True, skip:int=0, limit:int=100, db: Session=Depends(deps.get_db)):
    """
    Read all the bids for a specific item.

    Does'nt require authentication.
    
    The item must exist and published.

    order_by: id or price or bid_date

    desc_order: True for descending order(default value) and False for ascending order.

    """
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item_published_status = crud.get_auction_published_status(db, auction_id=db_item.auction_id)
    if not item_published_status:
        raise HTTPException(status_code=403, detail="Auction that belong this item is not published yet.")
    bids = crud.get_bids_for_item(db=db, item_id=item_id, order_by=order_by, desc_order=desc_order, skip=skip, limit=limit)
    return bids

@router.get("/items/{item_id}/bids/highest", response_model=schemas.Bid)
def read_highest_bid_for_item(item_id: int, db: Session=Depends(deps.get_db)):
    """
    Read the highest bid for a specific item.

    Does'nt require authentication.
    
    The item must exist and published.
    """

    db_item = crud.get_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_published_status = crud.get_auction_published_status(db, auction_id=db_item.auction_id)
    if not item_published_status:
        raise HTTPException(status_code=403, detail="Auction that belong this item is not published yet.")
    #bids = db_item.bids
    #highest_bid = max(bids, key=attrgetter('price'))
    highest_bid = crud.get_highest_bid_by_item(db=db, item_id=item_id)
    return highest_bid

@router.get("/bids/", response_model=List[schemas.Bid], dependencies=[Depends(deps.get_current_superuser)])
def read_all_bids(skip:int=0, limit:int=100, db: Session=Depends(deps.get_db)):
    """
    Read all bids
    Must be superuser.
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


@router.get("/users/{user_id}/bids/", response_model=List[schemas.Bid])
def read_user_bids(user_id: int, item_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read all the bids of a specific user for an item.
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_item = crud.get_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    bids = crud.get_bids_by_user_for_item(db, user_id=user_id, item_id=item_id, skip=skip, limit=limit)
    return bids