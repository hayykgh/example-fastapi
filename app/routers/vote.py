from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

# Add / Remove vote
@router.post("/{id}", response_model=schemas.VoteResponse)
def vote(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Args:
    - id (int): ID of the post to vote on.
    - db (Session): Database session dependency.
    - current_user (int): ID of the current authenticated user.

    Returns:
    - dict: Message indicating success or failure of the vote operation.

    Raises:
    - HTTPException: If the post with the provided ID doesn't exist.
    """

    # Query the post with the provided ID
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Raise HTTP 404 if the post doesn't exist
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    # Check if the user has already voted on the post
    found_vote = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == id).first()

    # If the user has already voted, delete the existing vote
    if found_vote:
        db.delete(found_vote)
        db.commit()
        message = "Successfully deleted the vote"
    else:
        # If the user hasn't voted yet, add a new vote
        new_vote = models.Vote(post_id=id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        message = "Successfully added the vote"

    # Count the total number of votes (likes) for the post
    total_likes = db.query(models.Vote).filter(models.Vote.post_id == id).count()

    return {"message": message, "likes": total_likes}
