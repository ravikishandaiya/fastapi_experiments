from fastapi import APIRouter, HTTPException, status, Response
from . import schemas
from ..database import db_conn

## DB connection
conn = db_conn().conn
cursor = conn.cursor

## Rounter
router = APIRouter(
    prefix="",
    tags=['Posts']
)

## get a post
@router.get("/posts/{id}")
def get_post(id: int, response = Response):
    print(id)
    post = None

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND       # 404
        # return {"message": f"Post with id {id} not found."}
    
        # we have build in method for this
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found.")
    
    return id


## Create a post
@router.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(Post: schemas.Post):      # payload: dict = Body(...)
    print(type(Post))
    return Post
