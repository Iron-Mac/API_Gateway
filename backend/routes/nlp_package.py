from datetime import datetime, timedelta
import secrets
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import requests
from security import get_current_user
from models import User, Module, UserModule, AuthToken
from schemas import PackageRequest, AuthTokenCreate
import time

router = APIRouter()


def is_expired(expire_time: datetime) -> bool:
    current_time = datetime.now()
    return current_time > expire_time


@router.post("/nlp-call")
def process_module(request_data: PackageRequest, session: Session = Depends(get_db)):
    auth_token = session.query(AuthToken).filter_by(token=request_data.auth_token).first()
    if not auth_token:
        raise HTTPException(status_code=401, detail="توکن شما نامعتبر است")
    if is_expired(auth_token.expire_date):
        raise HTTPException(status_code=403, detail="زمان اعتبار توکن منقضی شده است")
    user_db = session.query(User).filter_by(id=auth_token.user_id).first()
    module = session.query(Module).filter_by(id=request_data.module_id).first()
    if not user_db:
        raise HTTPException(status_code=401, detail="کاربر نامعتبر است")
    if not user_db.is_admin:
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
        print(response.status_code)
    except Exception:
        raise HTTPException(status_code=400, detail="امکان دسترسی به دامنه شما وجود ندارد.")

    if response.status_code == 200:
        try:
            json_result = response.json()
            if module.output_type == 1:
                if json_result["result"]:
                    return {"result": json_result["result"]}
                else:
                    raise HTTPException(status_code=400, detail="پاسخ خالی است.")
            elif module.output_type == 2:
                if not json_result['output_list']:
                    raise HTTPException(status_code=400, detail="نوع قالب خروجی اشتباه است.")
                if isinstance(json_result['output_list'], list):
                    is_list_of_strings = all(isinstance(item, str) for item in json_result['output_list'])
                    if is_list_of_strings:
                        return json_result
                    else:
                        raise HTTPException(status_code=400, detail="لیست output_list یک لیست است، اما همه موارد رشته نیستند.")
                else:
                    raise HTTPException(status_code=400, detail="output_list یک لیست نیست")
            elif module.output_type == 3:
                if isinstance(json_result['output_list'], list):
                    is_list_of_2_pair_strings = all(
                        isinstance(sublist, list) and len(sublist) == 2 and all(isinstance(item, str) for item in sublist)
                        for sublist in json_result['output_list']
                    )
                    if is_list_of_2_pair_strings:
                        return json_result
                    else:
                        raise HTTPException(status_code=400, detail="لیست output_list یک لیست است، اما همه زیرلیست‌ها معتبر نیستند.")
                else:
                    raise HTTPException(status_code=400, detail="output_list یک لیست نیست")

        except ValueError:
            raise HTTPException(status_code=400, detail="امکان تجزیه و تحلیل پاسخ JSON از ماژول وجود ندارد.")
    else:
        error_message = str(requests.exceptions.RequestException)
        raise HTTPException(status_code=400, detail=error_message)


@router.get("/get_auth_tokens/")
def get_auth_token(user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user_db = session.query(User).filter_by(username=user).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")
    user_tokens = user_db.personal_tokens
    print(user_tokens)
    user_token_list = []
    for user_token in user_tokens:
        user_token_data = {
            "user_id": user_token.user_id,
            "id": user_token.id,
            "title": user_token.title,
            "description": user_token.description,
            "expire_time": user_token.expire_date
        }
        user_token_list.append(user_token_data)
    return {"user_tokens": user_token_list}


@router.post("/create_auth_tokens/")
def create_auth_token(token_data: AuthTokenCreate, user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    ruser = session.query(User).filter(User.username == user).first()
    if ruser is None:
        raise HTTPException(status_code=401, detail="کاربر نامعتبر است")

    expire_days = token_data.expire_days
    expire_date = datetime.now() + timedelta(days=expire_days)

    random_token = generate_random_token(32)  # Generate a random 32-character token

    db_token = AuthToken(
        user_id=ruser.id,
        title=token_data.title,
        description=token_data.description,
        token=random_token,
        expire_date=expire_date
    )
    session.add(db_token)
    session.commit()
    session.refresh(db_token)
    return db_token


def generate_random_token(length: int):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
