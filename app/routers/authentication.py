from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from . import schemas, OAuth2
from .. import utils
from ..database import db_conn

# DB connection
conn = db_conn().conn
cursor = conn.cursor()

# API Router
router = APIRouter(
    tags=["Login"]
)


## OAuth2PasswordRequestForm picks up datas form form automatially, username and password
# Login
@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.LoginUserResponse)
def login(credentials: OAuth2PasswordRequestForm = Depends()):

    query = """
            SELECT *
            FROM users
            WHERE email = %s;           
        """
    
    cursor.execute(query, (credentials.username,))
    result = cursor.fetchone()

    if not (result and utils.verify_password(credentials.password, result['password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Credentials"
            )
    
    token = OAuth2.create_access_token({"email": credentials.username})
    
    return {"access_token": token, "token_type": "bearer"}


@router.get("/login", status_code=status.HTTP_200_OK)
def get_current_user(current_user: dict = Depends(OAuth2.get_current_user)):
    return {"user": current_user}



