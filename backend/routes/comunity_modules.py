from fastapi import APIRouter, Depends, HTTPException, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
import requests
from security import verify_token, get_current_user
from models import User, Module, UserModule
from schemas import ModuleRequest, SetRateLimit, AddModuleToUser, CreateModule

router = APIRouter()

@router.post("/process-module")
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

@router.post("/set-rate-limit")
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
@router.post("/add-module-to-user")
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

@router.post("/create-module")
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

