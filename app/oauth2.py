from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# OAuth2PasswordBearer instance for token retrieval 
# --- Instance of OAuth2PasswordBearer for handling token retrieval ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Load settings from config
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    """
    Create a new JWT access token with the provided data.

    Args:
    - data (dict): Data to be encoded into the token payload.
    """
    # --- Copy the data dictionary to avoid depricating the original ---
    to_encode = data.copy()

    # --- Calculates the token expiration time ---
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # --- Inserts the token expiration time in the "to_encode" dictionary ---
    to_encode.update({"exp": expire})

    # --- Encode the token using the provided data, secret key, and algorithm ---
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt  

def verify_access_token(token: str, credentials_exception):
    """
    Verify the provided JWT access token.

    Args:
    - token (str): JWT access token to verify.
    - credentials_exception (HTTPException): Exception to raise if verification fails.
    """
    try:
        # --- Decode the JWT token using the secret key and algorithm ---
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: int = payload.get("user_id")

        # --- Check if the user_id is present in the payload; raise exception if not ---
        if id is None:
            raise credentials_exception
        
        # --- Create a TokenData object with the extracted user_id ---
        token_data = schemas.TokenData(id=id)

    except JWTError:
        # --- Raise credentials_exception if decoding fails ---
        raise credentials_exception
    
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Get the current user based on the JWT access token.

    Args:
    - token (str, optional): JWT access token obtained from the request header.
    - db (Session): Database session dependency.

    """
    # --- Handle unauthorized access exceptions ---
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not verify credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # --- Verify the JWT access token and retrieve token data ---
    token_data = verify_access_token(token, credentials_exception)

    # --- Query the database to fetch the user using the user_id from token_data ---
    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    return user
