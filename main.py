from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import requests

app = FastAPI()
security = HTTPBearer()

# Replace this with your own secret key
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Sample user model
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.get_token_bucket = 20  # Number of GET requests allowed per day
        self.post_token_bucket = 10  # Number of POST requests allowed per day

# Sample database of users
users_db = {
    "john": User("john", "password123"),
    "jane": User("jane", "password456"),
}

# Password context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
def register(username: str, password: str):
    if username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    user = User(username, hashed_password)
    users_db[username] = user
    return {"message": "User registered successfully"}

# Login and generate access token
@app.post("/login")
def login(username: str, password: str):
    if username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    user = users_db[username]
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(username)
    return {"access_token": access_token}

# Dependency function to verify access token and extract user information
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = verify_token(token)
    return username

# Protected route example
@app.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    # Example usage of the user information
    if user not in users_db:
        raise HTTPException(status_code=401, detail="Invalid user")
    return {"message": f"Hello, {user}! This is a protected route."}

# Example of an NLP module that requires the user to be logged in and enforces rate limiting for GET and POST methods separately
@app.get("/nlp")
def nlp_module_get(user: str = Depends(get_current_user)):
    # Check if the user is logged in and authorized to use the NLP module
    if user not in users_db:
        raise HTTPException(status_code=401, detail="Invalid user")

    # Retrieve the user object from the users_db
    user_obj = users_db[user]

    # Check rate limit for GET requests
    if user_obj.get_token_bucket <= 0:
        raise HTTPException(status_code=429, detail="Rate limit exceeded for GET requests. Please try again later.")

    # Perform NLP operations using the user data
    # Example: Access user attributes
    username = user_obj.username
    password = user_obj.password

    # Update the token bucket for GET requests
    user_obj.get_token_bucket -= 1

    return {"message": f"Hello, {username}! This is the NLP module for GET requests."}

@app.post("/nlp")
def nlp_module_post(text, user: str = Depends(get_current_user)):
    # Check if the user is logged in and authorized to use the NLP module
    print(users_db)
    if user not in users_db:
        raise HTTPException(status_code=401, detail="Invalid user")
    

    # Retrieve the user object from the users_db
    user_obj = users_db[user]

    # Check rate limit for POST requests
    if user_obj.post_token_bucket <= 0:
        raise HTTPException(status_code=429, detail="Rate limit exceeded for POST requests. Please try again later.")

    # Perform NLP operations using the user data
    # Example: Access user attributes
    username = user_obj.username
    password = user_obj.password

    # Update the token bucket for POST requests
    user_obj.post_token_bucket -= 1

    SERVICE_URL = f"http://localhost:8001/hash/?text={text}"
    headers = {
        "accept": "application/json",
    }
    data = {
        "text": "Your actual text here",  # Replace this with the text you want to hash
    }

    response = requests.post(SERVICE_URL)


    if response.status_code == 200:
        try:
            result = response.json()  # Parse the JSON response
            print(result)
            return {"result": result}
        except ValueError:
            return {"error": "Failed to parse the JSON response from the service."}
    else:
        return {"error": "Failed to process the text."}


