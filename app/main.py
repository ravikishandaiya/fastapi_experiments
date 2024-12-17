import sys
sys.dont_write_bytecode = True

from fastapi import FastAPI
from .routers import authentication, users, posts
from .config import settings


## FastAPI app object
app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(authentication.router)


## ROOT
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World!"}


