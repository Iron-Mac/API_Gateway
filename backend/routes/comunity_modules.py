from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import requests
from security import get_current_user
from models import User, Module, UserModule
from schemas import ModuleRequest, SetRateLimit, AddModuleToUser, CreateModule, ModuleDeleteRequest
import time

router = APIRouter()


@router.post("/process-module")
def process_module(request_data: ModuleRequest, user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user_db = session.query(User).filter_by(username=user).first()
    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid user")
    if not user_db.is_admin:
        module = session.query(Module).filter_by(id=request_data.module_id).first()
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

        user_module = session.query(UserModule).filter_by(user_id=user_db.id, module_id=module.id).first()
        if not user_module:
            raise HTTPException(status_code=403, detail="Access denied to module")

        print(user_module.tokens, user_module.last_refill)
        # Deduct token and update last refill time
        now = time.time()

        # Check if 24 hours have passed since the last refill, and reset tokens if needed
        if now - user_module.last_refill >= 86400:  # 24 hours in seconds
            user_module.tokens = user_module.limit
            user_module.last_refill = now
            session.commit()

        if user_module.tokens <= 0:
            raise HTTPException(status_code=429, detail="Rate limit exceeded for this module. Please try again later.")

        # Deduct token
        user_module.tokens -= 1
        session.commit()

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

    # Check if the URL already exists in the database
    existing_module = session.query(Module).filter_by(url=module_data.url).first()
    if existing_module:
        raise HTTPException(status_code=400, detail="URL already exists")

    # Create a new module instance and store it in the database
    new_module = Module(
        creator_id=user_db.id,
        title=module_data.title,
        description=module_data.description,
        url=module_data.url
    )
    session.add(new_module)
    session.flush()  # Flush to obtain the new_module.id

    # Create a UserModule instance to store rate limit for the module and user
    user_module = UserModule(user_id=user_db.id, module_id=new_module.id, limit=module_data.limit, tokens=module_data.limit)
    session.add(user_module)
    session.commit()
    # Add the module to the user's list of modules with rate limit
    user_db.modules.append(new_module)
    session.commit()

    return {"message": "Module created successfully", "module_id": new_module.id}


@router.get("/user-modules")
def get_user_modules(user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user_db = session.query(User).filter_by(username=user).first()
    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid user")

    user_modules = user_db.modules

    module_list = [{"id": module.id, "title": module.title, "description": module.description, "url": module.url} for module in user_modules]

    return {"user": user_db.username, "modules": module_list}


@router.delete("/delete-module")
def delete_module(request_data: ModuleDeleteRequest, user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user_db = session.query(User).filter_by(username=user).first()
    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid user")

    module = session.query(Module).filter_by(id=request_data.module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    if module.creator_id != user_db.id:
        raise HTTPException(status_code=403, detail="Access denied to delete module")

    # Delete the module from the user's list of modules
    user_db.modules.remove(module)

    # Delete the module from the database
    session.delete(module)

    session.commit()

    return {"message": "Module deleted successfully"}
