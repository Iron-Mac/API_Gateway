from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 15

security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_tokens(username: str):
    access_token = create_access_token(username)
    refresh_token = create_refresh_token(username)
    return access_token, refresh_token


def create_refresh_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


# Generate access token
def create_access_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# Verify access token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Hash password
def get_password_hash(password: str):
    return pwd_context.hash(password)


# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# Dependency function to verify access token and extract user information
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        username = verify_token(token)
        return username
    except HTTPException as e:
        if "Token expired" in e.detail:
            raise HTTPException(status_code=401, detail="Access token expired")
        elif "Invalid token" in e.detail:
            refresh_token = credentials.credentials
            try:
                username = verify_refresh_token(refresh_token)
                return username
            except HTTPException:
                raise HTTPException(status_code=401, detail="Invalid access/refresh token")
            

def get_admin_user(user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    # Implement this function
    admin_db = session.query(User).filter_by(username=user).first()
    if not admin_db or not admin_db.is_admin:
        raise HTTPException(status_code=403, detail="Access forbidden for non-admin users")
    else:
        return user
