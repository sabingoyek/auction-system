from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, deps, models, schemas

router = APIRouter()


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read users.

    Doesn't require authentication.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/me/", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Read the user data for the currently authenticated user.
    """
    return current_user


@router.get("/users/{user_id}/", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(deps.get_db)):
    """
    Read the data for a specific user.

    Doesn't require authentication.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post(
    "/users/",
    response_model=schemas.User,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    """
    Create a new user. Ony accessible by the superuser.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.delete("/user/me/",response_model=schemas.User, dependencies=[Depends(deps.get_current_user)])
def remove_user(
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)):
    """
    Delete the user account
    """
    db_user = crud.get_user(db, user_id = current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_user_active_auctions = crud.get_user_active_auctions(db=db, user_id=current_user.id)
    if current_user_active_auctions:
        raise HTTPException(status_code=403, detail="Action forbidden: you have an active auction")

    current_user_items = crud.get_user_items(db=db, user_id=current_user.id)
    for item in current_user_items:
        if crud.get_auction_active_status(db=db, auction_id=item.auction_id).is_active:
            raise HTTPException(status_code=403, detail="Action forbidden: you have an active item.")

    active_items = crud.get_active_items(db=db)
    for item in active_items:
        item_highest_bid = crud.get_highest_bid_by_item(db=db, item_id = item.id)
        if item_highest_bid.owner_id == current_user.id:
            raise HTTPException(status_code=403, detail="Action forbidden: you hold the highest bid for an active item(" + str(item) + ").")
    setattr(db_user, "is_active", False)
    db.delete(db_user)
    db.commit()
    return {"ok": True}
