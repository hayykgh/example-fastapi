from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2 

router = APIRouter(
    prefix="/vote", 
    tags=["Vote"]
)



@router.post("/{id}")
def vote(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(id == models.Post.id)
    found_vote = db.query(models.Vote).filter(current_user.id == models.Vote.user_id, id == models.Vote.post_id).first()
    

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if found_vote:
        db.delete(found_vote)   
        db.commit()
        return {"message": "Successfully deleted the vote"}
    
    else:
        new_vote = models.Vote(post_id = id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added the vote"}    

