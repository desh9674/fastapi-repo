from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session


from .. import oauth2, models, schemas
from ..database import SessionLocal, get_db

router = APIRouter(prefix="/vote", tags=['vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), token: int = Depends(oauth2.get_current_user)):
    #check post is available
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post was with id : {vote.post_id}  was not found to Like")
        
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == token.id)

    if vote_query.first():
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Like removed"}
    else:
        new_vote = models.Vote(post_id=vote.post_id, user_id=token.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Liked the post"}
    
