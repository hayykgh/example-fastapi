from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import engine, get_db


router = APIRouter(
    prefix="/posts", # All the APIs bellow grab /posts as a path
    tags=["Posts"]   # Everything below will be grouped under the "Post" section in the swagger
)


# GET ALL POSTS            
@router.get("/", response_model=List[schemas.PostOut]) # this enshures that all the posts only have the presaved parameters in the response body
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              skip: int = 0, limit: int = 10,  # Skip and limit querries for showing specific nuber of posts per request
              search: Optional[str] = ""):     # Search querry for searching though the post titles
    
 # --- grabs the posts based on the given criterias from the DB and stors in 'posts' variable ---
   posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   results = results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
               .outerjoin(models.Vote, models.Vote.post_id == models.Post.id) \
               .group_by(models.Post.id) \
               .filter(models.Post.title.contains(search)).order_by(models.Post.id)\
               .limit(limit).offset(skip)
   return results


# GET ONE POST BY ID            
@router.get("/{id}", response_model=schemas.PostOut) # this enshures the post only havs the presaved parameters in the response body
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
 # --- finds the post based on the id from the 'posts/{id}' path, and stors in posts variable ---

   post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
               .outerjoin(models.Vote, models.Vote.post_id == models.Post.id) \
               .group_by(models.Post.id).filter(models.Post.id == id).first()
               
 
 # --- raises HTTP 404 status code with an error if the provided post does not exist in DB ---
   if not post:
      raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
   
   return post


# CREATE POST            
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) # this enshures the post only havs the presaved parameters in the response body
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
 # --- grabs the given request body, adds "owner_id" parameter and stors in 'new_post' variable --- 
   new_post = models.Post(owner_id=current_user.id, **post.dict())
 
 # --- adds, commits, and refreshes the posts into DB ---
   db.add(new_post)
   db.commit()
   db.refresh(new_post)

   return  new_post


# DELETE A POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):

 # --- stors the querry to find the post into the 'post_query' variable ---
   post_query = db.query(models.Post).filter(models.Post.id == id)
 # --- stors the post into the 'post' variable ---
   post = post_query.first()

 # --- raises a 404 exception with an error if the post wasn't found in DB ---
   if post == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

 # --- raises a forbidden exception with an error if the given id of post does not belong to the logged-in account ---
   if post.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
 # --- delete the given post from the DB ---
   post_query.delete(synchronize_session=False)    
   db.commit()
   
   return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE A POST
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

 # --- stors the querry to find the post into the 'post_query' variable ---   
    post_querry = db.query(models.Post).filter(models.Post.id==id)
    
 # --- raises a 404 exception with an error if the post wasn't found in DB ---
    if post_querry.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} does not exist")
    
 # --- raises a forbidden exception with an error if the given id of post does not belong to the logged-in account ---
    if post_querry.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
 # --- updates the post details with the given data, and commits it ---
    post_querry.update(post.dict(), synchronize_session=False) 
    db.commit()

    return post_querry.first()