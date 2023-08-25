from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import requests
from security import get_current_user
from models import User, Module, UserModule
from schemas import ModuleRequest, CreateModule
from utils.regex_controller import is_valid_url
import time

router = APIRouter()


@router.post("/process-module")
def process_module(request_data: ModuleRequest, user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user_db = session.query(User).filter_by(username=user).first()
    if not user_db:
        raise HTTPException(status_code=401, detail="کاربر نامعتبر است")
    if not user_db.is_admin:
        module = session.query(Module).filter_by(id=request_data.module_id).first()
        if not module:
            raise HTTPException(status_code=404, detail="ماژول پیدا نشد")

        user_module = session.query(UserModule).filter_by(user_id=user_db.id, module_id=module.id).first()
        if not user_module:
            raise HTTPException(status_code=403, detail="دسترسی به ماژول رد شد")

        print(user_module.tokens, user_module.last_refill)
        now = time.time()

        if now - user_module.last_refill >= 86400:
            user_module.tokens = user_module.limit
            user_module.last_refill = now
            session.commit()

        # Check if expire_time is valid and not expired
        if user_module.expire_time and user_module.expire_time <= datetime.now():
            raise HTTPException(status_code=403, detail="زمان اعتبار ماژول منقضی شده است")
        
        if user_module.tokens <= 0:
            raise HTTPException(status_code=429, detail="نرخ محدودیت برای این ماژول تجاوز شده است. لطفاً بعداً دوباره امتحان کنید.")

        user_module.tokens -= 1
        session.commit()

    headers = {
        "accept": "application/json",
    }
    data = {
        "input_data": request_data.input_data,
    }
    try:
        response = requests.post(module.url, headers=headers, json=data)
    except Exception:
        return {"error": "امکان دسترسی به URL شما وجود ندارد."}

    if response.status_code == 200:
        try:
            json_result = response.json()
            if module.output_type == 1:
                if json_result["result"]:
                    return {"result": json_result["result"]}
                else:
                    return {"error": "پاسخ خالی است."}
            elif module.output_type == 2:
                if isinstance(json_result['output_list'], list):
                    is_list_of_strings = all(isinstance(item, str) for item in json_result['output_list'])
                    if is_list_of_strings:
                        return json_result
                    else:
                        return {"error": "لیست output_list یک لیست است، اما همه موارد رشته نیستند."}
                else:
                    return {"error": "output_list یک لیست نیست"}
            elif module.output_type == 3:
                if isinstance(json_result['output_list'], list):
                    is_list_of_2_pair_strings = all(
                        isinstance(sublist, list) and len(sublist) == 2 and all(isinstance(item, str) for item in sublist)
                        for sublist in json_result['output_list']
                    )
                    if is_list_of_2_pair_strings:
                        return json_result
                    else:
                        return {"error": "لیست output_list یک لیست است، اما همه زیرلیست‌ها معتبر نیستند."}
                else:
                    return {"error": "output_list یک لیست نیست"}

        except ValueError:
            return {"error": "امکان تجزیه و تحلیل پاسخ JSON از ماژول وجود ندارد."}
    else:
        error_message = str(requests.exceptions.RequestException)
        return {"error": error_message}


@router.post("/create-module")
def create_module(module_data: CreateModule, user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user_db = session.query(User).filter_by(username=user).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    if not user_db.is_registerer:
        raise HTTPException(status_code=401, detail="کاربر اجازه ی ثبت ندارد")

    # Check if the URL is a valid URL
    if not is_valid_url(module_data.url):
        raise HTTPException(status_code=400, detail="URL نامعتبر است")

    # Check if the URL already exists in the database
    existing_module = session.query(Module).filter_by(url=module_data.url).first()
    if existing_module:
        raise HTTPException(status_code=400, detail="URL از قبل وجود دارد")

    # Create a new module instance and store it in the database
    new_module = Module(
        creator_id=user_db.id,
        title=module_data.title,
        description=module_data.description,
        url=module_data.url,
        output_type=module_data.output_type
    )
    session.add(new_module)
    session.flush()  # Flush to obtain the new_module.id

    # Add the module to the user's list of modules with rate limit
    user_db.modules.append(new_module)
    session.commit()

    unlimited_expiretime = datetime(9999, 12, 31)
    # Check if the UserModule entry already exists for the user and module
    existing_user_module = session.query(UserModule).filter_by(user_id=user_db.id, module_id=new_module.id).first()
    if not existing_user_module:
        user_module = UserModule(
            user_id=user_db.id,
            module_id=new_module.id,
            limit=module_data.limit,
            tokens=module_data.limit,
            expire_time=unlimited_expiretime
        )
        session.add(user_module)
        session.commit()
    else:
        existing_user_module.limit = module_data.limit
        existing_user_module.tokens = module_data.limit
        existing_user_module.expire_time = unlimited_expiretime
        session.commit()

    return {"message": "Module created successfully", "module_id": new_module.id}


@router.get("/user-modules")
def get_user_modules(user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user_db = session.query(User).filter_by(username=user).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    user_modules = user_db.modules
    user_models = session.query(UserModule).filter_by(user_id=user_db.id).all()

    module_list = [{"id": module.id, "title": module.title, "description": module.description, "url": module.url, "output_type": module.output_type} for module in user_modules]
    user_model_list = [{"user_id": user_model.user_id, "module_id": user_model.module_id, "limit": user_model.limit, "tokens": user_model.tokens, "last_refill": user_model.last_refill} for user_model in user_models]

    return {"user": user_db.username, "modules": module_list, "user_models": user_model_list}
