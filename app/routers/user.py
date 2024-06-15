from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# CREATE USER
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    """
    Args:
    - user (schemas.CreateUser): User data to create a new user.
    - db (Session): Database session dependency.

    Returns:
    - schemas.UserResponse: Created user details.

    Raises:
    - HTTPException: If the email provided already exists in the database.
    """
    # Check if user with the same email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash the password before storing
    user.password = utils.hash_password(user.password)

    # Create new user object and add to database
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()

    return new_user

# GET USER BY ID
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    """
    Args:
    - id (int): ID of the user to retrieve.
    - db (Session): Database session dependency.

    Returns:
    - schemas.UserResponse: Retrieved user details.

    Raises:
    - HTTPException: If no user found with the provided ID.
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user
