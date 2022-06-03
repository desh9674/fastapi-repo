
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import  List, Optional

from sqlalchemy import func
from .. import oauth2, models, schemas
from ..database import SessionLocal, get_db

router = APIRouter( prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # curser.execute("""SELECT * FROM posts""")
    # posts  = curser.fetchall()  # this is previous way, writing manualquery
     
    
    #my_posts = db.query(models.Post).filter(models.Post.owner_id==token.id).all()
    # url = posts?limit=3&search=Star%20Wars 
    #posts = db.query(models.Post).all() # this is ORM way, writing python query
    #skipped_posts = db.query(models.Post).filter(models.Post.content.contains(search)).offset(skip).limit(limit).all()

    #PostBase scehema
    skipped_posts = db.query(models.Post).filter(models.Post.content.contains(search)).offset(skip).limit(limit).all()
    
    #PostOut schema, beacause of join
    results = db.query(models.Post,  func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()


    
    return results #FAST api handles conversion to JSON



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), token: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=token.id,**post.dict())# map user given fields to db model
    db.add(new_post)
    db.commit()
    db.refresh(new_post)# this is like RETURNING *
    return new_post


@router.get("/{id}", response_model=schemas.PostOut) 
def get_post(id: int, response: Response, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id==id).first()

    results = db.query(models.Post,  func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post was with id : {id}  was not found")
    
    return results


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int, db: Session = Depends(get_db), token: int = Depends(oauth2.get_current_user) ): 
    
    delete_query = db.query(models.Post).filter(models.Post.id==id)
    deleted_post = delete_query.first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post was with id : {id}  was not found to delete")
    if deleted_post.owner_id != int(token.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete another jedi's post")

    delete_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) # this wont return becaz  by default DELETE method returns nothing

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), token: int = Depends(oauth2.get_current_user) ):
    
    update_query = db.query(models.Post).filter(models.Post.id==id)
    updated_post = update_query.first()

    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post was with id : {id}  was not found to update")
    
    
    if updated_post.owner_id != int(token.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update another jedi's post")

    update_query.update(post.dict(), synchronize_session=False)
    db.commit()
    #print(post.dict(), "post has been updated")
    return update_query.first()
