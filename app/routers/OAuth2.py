from jose import JWTError,jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# SECRET KEY
# ALOG
# Expiration Time

from .. secrets import SECRET_KEY, ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Header
# Payload
# Signature


# OAuth2PasswordBearer is used to extract the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = access_token_expire_minutes)
    to_encode["exp"] = expire

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


# To verify the JWT Token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as err:
        print("Error:", err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something Went Wrong."
        )


def get_current_user(payload: dict = Depends(verify_token)): # token: str = Depends(oauth2_scheme)
    return payload