import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jdatetime import datetime as jdatetime_datetime
import redis
from database import get_db, get_redis_connection
from security import get_current_user, get_admin_user
from models import User, Module, UserModule
from schemas import SetRateLimit, ModuleDeleteRequest, EditUserRole

router = APIRouter(dependencies=[Depends(get_admin_user)])


@router.delete("/delete-module")
def delete_module(request_data: ModuleDeleteRequest, user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user_db = session.query(User).filter_by(username=user).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    module = session.query(Module).filter_by(id=request_data.module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="ماژول پیدا نشد")

    if module.creator_id != user_db.id or not user_db.is_admin:
        raise HTTPException(status_code=403, detail="شما دسترسی حذف ماژول را ندارید")

    # Delete the module from the user's list of modules
    user_db.modules.remove(module)

    # Delete the module from the database
    session.delete(module)

    session.commit()

    return {"message": "Module deleted successfully"}


@router.post("/set-rate-limit")
def set_rate_limit(rate_limit_data: SetRateLimit, admin_user: str = Depends(get_admin_user), session: Session = Depends(get_db)):

    target_user = session.query(User).filter_by(username=rate_limit_data.username).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    module = session.query(Module).filter_by(id=rate_limit_data.module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="ماژول پیدا نشد")

    try:
        # Parse the Jalali date string and create a jdatetime object
        jalali_expire_time = jdatetime_datetime.strptime(rate_limit_data.expire_time, "%Y-%m-%d %H:%M:%S")

        # Convert jdatetime object to Python datetime object
        gregorian_expire_time = jalali_expire_time.togregorian()

        # Compare with the current Gregorian datetime
        if gregorian_expire_time < jdatetime_datetime.now().togregorian():
            raise HTTPException(status_code=400, detail="زمان انقضا باید در آینده باشد")

    except ValueError:
        raise HTTPException(status_code=400, detail="فرمت تاریخ وارد شده صحیح نیست")

    # Check if the module is already associated with the target user
    if module not in target_user.modules:
        target_user.modules.append(module)
        session.commit()
    user_module = session.query(UserModule).filter_by(user_id=target_user.id, module_id=module.id).first()

    if not user_module:
        new_user_module = UserModule(
            user_id=target_user.id,
            module_id=module.id,
            limit=rate_limit_data.limit,
            tokens=rate_limit_data.limit,
            expire_time=gregorian_expire_time
        )
        session.add(new_user_module)
        session.commit()
    else:
        user_module.limit = rate_limit_data.limit
        user_module.tokens = rate_limit_data.limit
        user_module.expire_time = gregorian_expire_time
        session.commit()

    return {"message": "محدودیت نرخ با موفقیت بروزرسانی شد"}


@router.post("/edit-user-role")
def edit_user_role(request_data: EditUserRole, user: str = Depends(get_admin_user), session: Session = Depends(get_db)):
    target_user = session.query(User).filter_by(username=user).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    target_user.is_admin = request_data.is_admin
    target_user.is_registerer = request_data.is_registerer

    session.commit()

    return {"message": f"کاربر {target_user.username} با موفقیت تغییر پیدا کرد"}


def serialize_module(module):
    # Define a function to serialize a Module object to a dictionary
    return {
        "id": module.id,
        "title": module.title,
        "description": module.description,
        "url": module.url,
        "output_type": module.output_type
    }


def serialize_user(user):
    # Define a function to serialize a Module object to a dictionary
    return {
        "id": user.id,
        "username": user.username,
        "phone_number": user.phone_number,
        "admin": user.is_admin,
        "registerer": user.is_registerer
    }


@router.get("/all-module-list")
def get_all_modules(user: str = Depends(get_admin_user), session: Session = Depends(get_db), redis_conn: redis.StrictRedis = Depends(get_redis_connection)):
    # Generate a unique cache key based on the request parameters
    cache_key = "all-modules"

    # Try to fetch data from Redis cache
    cached_data = redis_conn.get(cache_key)
    if cached_data:
        # If data is in cache, deserialize it and return
        cached_modules = json.loads(cached_data.decode("utf-8"))
        return cached_modules

    # If not in cache, fetch data from the database
    modules = session.query(Module).all()

    # Serialize the list of modules to JSON before storing in Redis
    serialized_modules = json.dumps([serialize_module(module) for module in modules])
    # Set the expiration time for the cached data (e.g., 300 seconds / 5 minutes)
    ttl = 300

    # Store serialized data in Redis cache with a specified expiration time (in seconds)
    redis_conn.setex(cache_key, ttl, serialized_modules)

    return modules


@router.get("/all-user-list")
def get_all_users(admin_user: str = Depends(get_admin_user), session: Session = Depends(get_db), redis_conn: redis.StrictRedis = Depends(get_redis_connection)):
    # Generate a unique cache key based on the request parameters
    cache_key = "all-users"

    # Try to fetch data from Redis cache
    cached_data = redis_conn.get(cache_key)
    if cached_data:
        # If data is in cache, deserialize it and return
        cached_users = json.loads(cached_data.decode("utf-8"))
        return cached_users

    # If not in cache, fetch data from the database
    users = session.query(User).all()

    # Serialize the list of modules to JSON before storing in Redis
    serialized_users = json.dumps([serialize_user(user) for user in users])
    # Set the expiration time for the cached data (e.g., 300 seconds / 5 minutes)
    ttl = 300

    # Store serialized data in Redis cache with a specified expiration time (in seconds)
    redis_conn.setex(cache_key, ttl, serialized_users)

    return users
