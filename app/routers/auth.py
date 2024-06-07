from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2


router = APIRouter(
    tags=["Authentication"] # Everything below will be grouped under the "Authentication" section in the swagger
)


# Login function
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

 # --- finds the user from the request in DB using models.User and stores in the user variable ---
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

 # --- raises HTTP 403 status code with an error if the provided email does not exist in DB ---
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
    
 # --- raises HTTP 403 status code with an error if the provided password is incorrect ---
 # --- uses CryptContext liberary to hash the provided password with the already hashed one in DB ---
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
    
 # --- creates JWT and passes the provided user's id into the token and returns it as a bearer token ---
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
