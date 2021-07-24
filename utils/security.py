from passlib.context import CryptContext
from models.jwtUser import JWTUser
from datetime import datetime, timedelta
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED
import time

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")

jwt_user1 = {"username": "user1", "password": "$2b$12$zPxJqWkZHNVzhm1wlkmo6OaEqe.n1ejVHFsz68P4EfnYymPwzYP4e",
             "disabled": False, "role": "admin"}
# "password": "password1"
db_jwt_user1 = JWTUser(**jwt_user1)


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


"""
hashed = "$2b$12$yOqwzLaEVc2DjdslvG2GreS0F1efh88iG0LSqY.dlt2zM0IOPien2"
print(get_hashed_password("mysecret"))
print(verify_password("mysecret", hashed))
"""


# Authenticate username and password to give JWT Token
def authenticate_user(user: JWTUser):
    if db_jwt_user1.username == user.username:
        if verify_password(user.password, db_jwt_user1.password):
            user.role = "admin"
            return user
    return None


# Create access JWT token
def create_jwt_token(user: JWTUser):
    expiry = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {"sub": user.username,
                   "role": user.role,
                   "exp": expiry}
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return jwt_token


# Check if JWT token is correct
def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiry = jwt_payload.get("exp")
        if time.time() < expiry:
            if db_jwt_user1.username == username:
                return final_checks(role)
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


# Last checking and returning the final result
def final_checks(role: str):
    if role == "admin":
        return True
    else:
        return False
