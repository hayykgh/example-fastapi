from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter()

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Endpoint for user login. Authenticates user credentials and returns a JWT token.

    Args:
    - user_credentials (OAuth2PasswordRequestForm): The OAuth2 form containing the username and password.
    - db (Session): Database session dependency.
    """

    # --- Retrieve the user from the database using the provided email (username) ---
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # --- Check if the user exists ---
    # If the user is not found in the database, raise an HTTP 403 Forbidden error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    # --- Verify the provided password ---
    # Use the verify_password function from utils to compare the provided password (will also be hashed in the utils.verify_password function) with the hashed password in the database
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    # --- Generate a JWT token ---
    # Create a JWT token that includes the user's id, first_name, last_name and email in the payload
    access_token = oauth2.create_access_token(data={"user_id": user.id, "first_name": user.first_name,
                                                     "last_name": user.last_name, "user_email": user.email})

    # --- Return the generated token ---
    # The response includes the access token and the token type (bearer)
    return {"access_token": access_token, "token_type": "bearer"}
