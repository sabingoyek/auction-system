from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

<<<<<<< HEAD
import crud, deps, models, security, schemas
from api import auctions, users, bids
=======
import crud, deps, models, schemas, security
from api import items, users, auctions, bids
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf
from database import SessionLocal, engine
from settings import settings

app = FastAPI()

app.include_router(users.router, tags=["users"])
app.include_router(auctions.router, tags=["auctions"])
<<<<<<< HEAD
app.include_router(bids.router, tags=["bids"])
=======
app.include_router(items.router, tags=["items"])
app.include_router(bids.router, tags=["bids"])

>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf

@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    user = crud.get_user_by_email(db, settings.super_user_email)
    if not user:
        user_in = schemas.UserCreate(
<<<<<<< HEAD
            first_name=settings.super_user_first_name,
            last_name=settings.super_user_last_name,
=======
            first_name=settings.first_name,
            last_name=settings.last_name,
>>>>>>> ee03a7a9dd239739ba02c1b44a33bd3ef9e86eaf
            email=settings.super_user_email, password=settings.super_user_password
        )
        crud.create_user(db, user_in)
    db.close()


@app.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {
        "access_token": security.create_access_token(subject=user.id),
        "token_type": "bearer",
    }
