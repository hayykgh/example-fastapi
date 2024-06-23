from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import oauth2
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

# DELETE USER 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_user(id: int,
    db: Session = Depends(get_db),                        # Dependency injection for database session
    current_user: int = Depends(oauth2.get_current_user) ):

    # Query User to delete
    user = db.query(models.User).filter(models.User.id == id).first()

    # Raise HTTP 404 if post not found
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")

    # Raise HTTP 403 if current user is not the owner of the post
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete post {id}")

    # Delete post from database
    db.delete(user)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE USER
@router.patch("/", status_code=status.HTTP_200_OK)
def update_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Update user details.

    Args:
    - user_update (schemas.UpdateUser): Updated user data.
    - db (Session): Database session dependency.
    - current_user (models.User): Current authenticated user.

    Raises:
    - HTTPException: If the email provided already exists in the database.
    """
    # Query the user to update
    db_user = db.query(models.User).filter(models.User.id == current_user.id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if the new email is already taken by another user, if email is updated
    if user_update.email and user_update.email != db_user.email:
        existing_user = db.query(models.User).filter(models.User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Update user attributes based on provided data
    if user_update.email:
        db_user.email = user_update.email
    if user_update.first_name:
        db_user.first_name = user_update.first_name
    if user_update.last_name:
        db_user.last_name = user_update.last_name
    if user_update.password:
        db_user.password = utils.hash_password(user_update.password)

    # Commit changes to the database
    db.commit()

    # Generate a new access token (if necessary, depending on your auth setup)
    new_token_data = {
        "user_id": db_user.id,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "user_email": db_user.email
    }
    new_access_token = oauth2.create_access_token(new_token_data)

    # Prepare response
    user_response = schemas.UserUpdateResponse(
        id=db_user.id,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        created_at=db_user.created_at,
        access_token=new_access_token
    )

    return user_response