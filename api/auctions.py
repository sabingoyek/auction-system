from datetime import datetime
import imp
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, deps, models, schemas

router = APIRouter()

@router.post("/users/me/auctions/", response_model=schemas.Auction, dependencies=[Depends(deps.get_current_user)],)
def create_my_auction(
    auction: schemas.AuctionCreate,
    user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)):
    """
    Create an auction
    
    Requires authentication and the auction will be assigned to the current user.
    """
    return crud.create_user_auction(db=db, auction=auction, user_id=user.id)

@router.get("/users/me/auctions/", response_model=List[schemas.Auction], dependencies=[Depends(deps.get_current_user)])
def read_my_auctions(is_published: bool = True, is_active: bool = True, skip: int = 0, limit: int = 100, user: schemas.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    """
    Read all my auctions.
    True for published, and False for unpublished.
    Default value for the parameter is True.
    Need authentication.
    """
    if is_published:
        if is_active:
            return crud.get_user_published_active_auctions(db, user_id=user.id, skip=skip, limit=limit)
        else:
            return crud.get_user_published_inactive_auctions(db, user_id=user.id, skip=skip, limit=limit)

    else:
        if is_active:
            return crud.get_user_unpublished_active_auctions(db, user_id=user.id, skip=skip, limit=limit)
        else:
            return crud.get_user_unpublished_inactive_auctions(db, user_id=user.id, skip=skip, limit=limit)


@router.get("/users/{user_id}/auctions/", response_model=List[schemas.Auction])
def read_user_published_auctions(user_id: int,skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read all the auctions that a specific user published. Doesn't need authentication.
    """
    if not crud.get_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    auctions = crud.get_user_published_auctions(db, user_id=user_id, skip=skip, limit=limit)
    return auctions


@router.get("/auctions/", response_model=List[schemas.Auction])
def read_all_published_auctions(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read all published auctions. Doesn't need authentication.
    """
    return crud.get_all_published_auctions(db, skip=skip, limit=limit)

@router.get("/auctions/{auction_id}/", response_model=schemas.Auction)
def read_auction(auction_id: int, db: Session = Depends(deps.get_db)):
    """
    Read a auction. Doesn't need authentication.
    """
    auction = crud.get_auction(db, auction_id=auction_id)
    if auction:
        if auction.is_published:
            return auction
        else:
            raise HTTPException(status_code=404, detail="Auction not published yet")
    else:
        raise HTTPException(status_code=404, detail="Auction not found")

@router.patch("/auctions/{auction_id}/", response_model=schemas.Auction, dependencies=[Depends(deps.get_current_user)])
def publish_auction(auction_id: int, user: schemas.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    db_auction = crud.get_auction(db, auction_id=auction_id)
    if not db_auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if db_auction.is_published:
        raise HTTPException(status_code=404, detail="This auction is already published")
    if db_auction.owner_id is not user.id:
        raise HTTPException(status_code=404, detail="You are not allowed to publish this auction, because you are not it owner.")
    if not db_auction.items:
        raise HTTPException(status_code=404, detail="Your auction doesn't have any item yet. So you can't publish it. Create an item and retry.")
    setattr(db_auction, "is_published", True)
    setattr(db_auction, "is_active", True)
    setattr(db_auction, "start_date", datetime.now())
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    return db_auction

@router.get("/auctions/{auction_id}/status/", response_model=bool)
def get_auction_status(auction_id: int, db: Session = Depends(deps.get_db)):
    """Get an auction status: active or not"""
    db_auction = crud.get_auction(db, auction_id=auction_id)
    if not db_auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if not db_auction.is_active:
        return False
    return True

@router.patch("/auctions/{auction_id}/status", response_model=schemas.Auction, dependencies=[Depends(deps.get_current_user)])
def terminate_auction(auction_id: int, user: schemas.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    """Marque an auction terminated"""
    db_auction = crud.get_auction(db, auction_id=auction_id)
    if not db_auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if not db_auction.is_published:
        raise HTTPException(status_code=404, detail="This auction is not published")
    if not db_auction.is_active:
        raise HTTPException(status_code=404, detail="This auction is already terminated.")
    if db_auction.owner_id is not user.id:
        raise HTTPException(status_code=404, detail="You are not allowed to terminate this auction, because you are not it owner.")
    setattr(db_auction, "is_active", False)
    setattr(db_auction, "end_date", datetime.now())
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    return db_auction

@router.delete("/auction/{auction_id}", dependencies=[Depends(deps.get_current_user)])
def delete_auction(auction_id: int, user: schemas.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    """Delete an unpublished auction. The performer must be its owner. 
    """
    db_auction = crud.get_auction(db, auction_id=auction_id)
    if not db_auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if  db_auction.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Action forbidden: Your aren't the owner of this auction")
    if db_auction.is_published:
        raise HTTPException(status_code=403, detail="Action forbidden: the auction is already published")
    db.delete(db_auction)
    db.commit()
    return {"ok": True}
