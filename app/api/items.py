import imp
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, deps, models, schemas

router = APIRouter()

@router.post("/auctions/{auction_id}/items/", response_model=schemas.Item, dependencies=[Depends(deps.get_current_user)],)
def create_item_for_auction(
    item: schemas.ItemCreate,
    user_id: int = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)):
    """
    Create an item for an auction
    
    Requires authentication and the item will be assigned to the auction. The current user must the owner of the auction.
    """
    # CHeck existence of the auction
    auction = crud.get_auction(db, auction_id=item.auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    # check if the auction already has item
    #if auction.item_id:
    #   raise HTTPException(status_code=400, detail="Auction already has item")
    # check if the current user is the owner of the auction
    #if user_id == auction.owner_id:
    #    raise HTTPException(status_code=404, detail="This user is not the owner of this auction")
    return crud.create_auction_item(db=db, item=item)
