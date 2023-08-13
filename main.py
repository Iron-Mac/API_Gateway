from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from model_evaluation import print_word_tag
from TextRankMedium import textrank
from Roge import roge
import jwt
import time
import requests
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = FastAPI()
security = HTTPBearer()

# Replace this with your own secret key
DATABASE_URL = "sqlite:///./test.db"  # SQLite database URL
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Sample user model
class UserInput(BaseModel):
    username: str
    password: str
    refresh_token: str = None  # Include refresh token field


class CreateModule(BaseModel):
    title: str
    description: str
    url: str
    limit: int  # Add a field for rate limit

class ModuleRequest(BaseModel):
    module_id: int
    input_data: str

class Input1(BaseModel):
    input_data: str

class Input2(BaseModel):
    phrase1: str
    phrase2: str

class SetRateLimit(BaseModel):
    url: str
    limit: int

class AddModuleToUser(BaseModel):
    username: str
    module_id: int

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define User model for the database
class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(String)
    url = Column(String)

    creator = relationship("User", back_populates="modules")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_admin = Column(Boolean, default=False)
    url_token_buckets = Column(JSON)
    # Define the many-to-many relationship with Module
    modules = relationship("Module", secondary="user_module", back_populates="users")

# Association table for User and Module many-to-many relationship
class UserModule(Base):
    __tablename__ = "user_module"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), primary_key=True)
    limit = Column(Integer, default=0)
    tokens = Column(Float, default=0.0)
    last_refill = Column(Float, default=time.time())


Base.metadata.create_all(bind=engine)

# Password context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

# Register a new user
@app.post("/register")
def register(username: str, password: str, is_admin: bool = False, session: Session = Depends(get_db)):
    if session.query(User).filter_by(username=username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(password)
    user = User(username=username, password_hash=hashed_password, is_admin=is_admin, url_token_buckets={})
    session.add(user)

    # Create a list to store user modules
    user.modules = []
    
    session.commit()
    return {"message": "User registered successfully"}

# Login and generate access token
@app.post("/login")
def login(user_data: UserInput, session: Session = Depends(get_db)):
    user = session.query(User).filter_by(username=user_data.username).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token, refresh_token = create_tokens(user_data.username)
    return {"access_token": access_token, "refresh_token": refresh_token}


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


@app.post("/refresh")
def refresh_tokens(refresh_token: str):
    username = verify_refresh_token(refresh_token)
    access_token, new_refresh_token = create_tokens(username)
    return {"access_token": access_token, "refresh_token": new_refresh_token}

@app.post("/process-module")
def process_module(request_data: ModuleRequest, user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user_db = session.query(User).filter_by(username=user).first()
    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid user")

    module = session.query(Module).filter_by(id=request_data.module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # Check if the user has access to the requested module
    if module not in user_db.modules:
        raise HTTPException(status_code=403, detail="Access denied to module")

    url_bucket = user_db.url_token_buckets.get(module.url)
    if not url_bucket:
        raise HTTPException(status_code=429, detail="Rate limit exceeded for this module")

    if url_bucket['tokens'] <= 0:
        raise HTTPException(status_code=429, detail="Rate limit exceeded for this module. Please try again later.")

    # Deduct token and update last refill time
    now = time.time()
    time_since_last_refill = now - url_bucket['last_refill']
    refill_rate = 86400  # 24 hours in seconds

    url_bucket['tokens'] = min(url_bucket['tokens'] + time_since_last_refill * (1 / refill_rate), url_bucket['limit'])

    # Update last refill time
    url_bucket['last_refill'] = now

    # Send a request to the module URL with the provided input
    headers = {
        "accept": "application/json",
    }
    data = {
        "input_data": request_data.input_data,
    }
    response = requests.post(module.url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            result = response.json()  # Parse the JSON response
            return result
        except ValueError:
            return {"error": "Failed to parse the JSON response from the module."}
    else:
        error_message = str(requests.exceptions.RequestException)
        return {"error": error_message}

@app.post("/set-rate-limit")
def set_rate_limit(rate_limit_data: SetRateLimit, admin_user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    admin_db = session.query(User).filter_by(username=admin_user).first()
    if not admin_db or not admin_db.is_admin:
        raise HTTPException(status_code=401, detail="Access denied")

    target_user = session.query(User).filter_by(username=rate_limit_data.username).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get the user's module association with the specified module
    module = session.query(Module).filter_by(url=rate_limit_data.url).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    user_module = session.query(UserModule).filter_by(user_id=target_user.id, module_id=module.id).first()
    if not user_module:
        raise HTTPException(status_code=404, detail="User does not have access to this module")

    # Update the rate limit for the module
    user_module.limit = rate_limit_data.limit
    session.commit()

    return {"message": "Rate limit updated successfully"}


# Example of adding a module to a user's list of modules
@app.post("/add-module-to-user")
def add_module_to_user(module_data: AddModuleToUser, admin_user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    admin_db = session.query(User).filter_by(username=admin_user).first()
    if not admin_db or not admin_db.is_admin:
        raise HTTPException(status_code=401, detail="Access denied")

    user_db = session.query(User).filter_by(username=module_data.username).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    module = session.query(Module).filter_by(id=module_data.module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # Add the module to the user's list of modules
    user_db.modules.append(module)

    session.commit()

    return {"message": "Module added to user successfully"}

@app.post("/create-module")
def create_module(module_data: CreateModule, user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user_db = session.query(User).filter_by(username=user).first()
    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid user")

    # Create a new module instance and store it in the database
    new_module = Module(
        creator_id=user_db.id,
        title=module_data.title,
        description=module_data.description,
        url=module_data.url
    )
    session.add(new_module)
    
    # Create a UserModule instance to store rate limit for the module and user
    user_module = UserModule(user_id=user_db.id, module_id=new_module.id, limit=module_data.limit, tokens=module_data.limit)

    # Add the module to the user's list of modules with rate limit
    user_db.modules.append(new_module)
    user_db.url_token_buckets[new_module.url] = {"limit": user_module.limit, "tokens": user_module.tokens, "last_refill": user_module.last_refill}

    session.commit()

    return {"message": "Module created successfully", "module_id": new_module.id}

@app.post("/postager/")
async def read_root(user_input: Input1):
    res = print_word_tag(user_input.input_data)
    return {"res": res}

@app.post("/textrank/")
async def read_root(user_input: Input1):
    res = textrank(user_input.input_data)
    return {"res": res}

@app.post("/roge/")
async def read_root(user_input: Input2):
    res = roge(user_input.phrase1, user_input.phrase2)
    return {"res": res}
