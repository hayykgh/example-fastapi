from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",  # Base path for all endpoints in this router
    tags=["Posts"]    # Tags for OpenAPI (Swagger) documentation grouping
)

# GET ALL POSTS
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),                # Dependency injection for database session
    skip: int = 0,                                # Number of records to skip
    limit: int = 10,                              # Maximum number of records to return
    search: Optional[str] = ""                    # Search query for filtering posts by title
):
    """
    Retrieve a list of posts based on search criteria.

    Args:
    - db (Session): Database session dependency.
    - skip (int): Number of records to skip (for pagination).
    - limit (int): Maximum number of records to return.
    - search (Optional[str]): Search query to filter posts by title.

    Returns:
    - List[schemas.PostOut]: List of posts with additional details.
    """
    # Query posts with votes count
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
              .outerjoin(models.Vote, models.Vote.post_id == models.Post.id) \
              .group_by(models.Post.id) \
              .filter(models.Post.title.contains(search)) \
              .order_by(models.Post.id) \
              .offset(skip).limit(limit).all()

    return posts

# GET ONE POST BY ID
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,                                      # id of the post that should be retrived
    db: Session = Depends(get_db),                # Dependency injection for database session
):
    """
    Args:
    - id (int): Post ID to retrieve.
    - db (Session): Database session dependency.

    Returns:
    - schemas.PostOut: Detailed information about the requested post.
    """
    # Query post details with votes count
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
             .outerjoin(models.Vote, models.Vote.post_id == models.Post.id) \
             .group_by(models.Post.id).filter(models.Post.id == id).first()

    # Raise HTTP 404 if post not found
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    return post

# CREATE POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),                        # Dependency injection for database session
    current_user: str = Depends(oauth2.get_current_user)  # Dependency injection for current user
):
    """
    Args:
    - post (schemas.CreatePost): Data to create a new post.
    - db (Session): Database session dependency.
    - current_user (int): Current authenticated user ID.

    Returns:
    - schemas.PostResponse: Details of the newly created post.
    """
    # Create new post with owner_id from current_user
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    # Add new post to database, commit, and refresh to get complete details
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# DELETE A POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),                        # Dependency injection for database session
    current_user: int = Depends(oauth2.get_current_user)  # Dependency injection for current user
):
    """
    Args:
    - id (int): Post ID to delete.
    - db (Session): Database session dependency.
    - current_user (int): Current authenticated user ID.

    Returns:
    - Response: HTTP 204 No Content on successful deletion.
    """
    # Query post to delete
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Raise HTTP 404 if post not found
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    # Raise HTTP 403 if current user is not the owner of the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete post {id}")

    # Delete post from database
    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE A POST
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(
    id: int,
    post: schemas.CreatePost,
    db: Session = Depends(get_db),                        # Dependency injection for database session
    current_user: int = Depends(oauth2.get_current_user)  # Dependency injection for current user
):
    """
    Args:
    - id (int): Post ID to update.
    - post (schemas.CreatePost): Data to update the post.
    - db (Session): Database session dependency.
    - current_user (int): Current authenticated user ID.

    Returns:
    - schemas.PostResponse: Updated details of the post.
    """
    # Query post to update
    post_query = db.query(models.Post).filter(models.Post.id == id)

    # Raise HTTP 404 if post not found
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    # Raise HTTP 403 if current user is not the owner of the post
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update post {id}")

    # Update post details with given data and commit
    post_query.update(post.dict())
    db.commit()

    return post_query.first()
