import imp
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, deps, models, schemas

router = APIRouter()

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
