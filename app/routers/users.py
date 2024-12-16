from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.params import Body
from typing import List
from pydantic import EmailStr

from . import schemas, OAuth2
from .. import utils
from ..database import db_conn

#DB connection
conn = db_conn().conn
cursor = conn.cursor()

router = APIRouter(
    prefix="",
    tags=['Users']
)

## Get all users -> List of dict
@router.get("/users", response_model=List[schemas.CreateUserResponse])
def get_user():
    query = """
            select *
            from users;           
        """
    cursor.execute(query)
    result = cursor.fetchall()

    return [dict(row) for row in result]


@router.get("/user", response_model=schemas.CreateUserResponse) # {email}
def get_user(payload: dict = Depends(OAuth2.verify_token)):  # email: EmailStr

    query = """
            select *
            from users
            where email = %s;          
        """
    cursor.execute(query, (payload["email"],))
    result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    return result


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model= schemas.CreateUserResponse)
def create_user(data: schemas.CreateUser = Body(...)):
    data = data.dict()
    data['password'] = utils.hash(data['password'])

    cols = ', '.join(data.keys())
    values = tuple(data.values())

    values = "','".join(values)

    query = f"""
            INSERT INTO users
            ({cols})
            VALUES ('%s')
            ON CONFLICT (email) DO UPDATE SET email = EXCLUDED.email  -- No-op update
            RETURNING *,
                    CASE
                        WHEN xmax = 0 THEN FALSE  -- Inserted
                        ELSE TRUE  -- Existing
                    END AS user_exist;
        """%(values)
    
    # print(query)
    cursor.execute(query)
    conn.commit()

    result = cursor.fetchone()

    return result
