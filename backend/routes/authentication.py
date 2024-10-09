from fastapi import APIRouter, Depends, HTTPException
import redis
import logging
from utils.custom_log_message import custom_log_message
from sqlalchemy.orm import Session
from database import get_db, get_redis_connection
from security import create_tokens, get_current_user, verify_refresh_token, get_password_hash, verify_password
from models import User
from schemas import UserInput, ResetPasswordInput, LoginInput, UserCodeVerification
import random

router = APIRouter()

auth_logger = logging.getLogger("authentication")


# Store the verification code in Redis
def store_verification_code(redis_conn: redis.StrictRedis, username: str, verification_code: str):
    redis_conn.set(f"verification_code:{username}", verification_code)
    redis_conn.expire(f"verification_code:{username}", 3600)  # Set expiration time (1 hour) for the code


# Verify the verification code from Redis
def verify_verification_code(redis_conn: redis.StrictRedis, username: str, verification_code: str):
    redis_key = f"verification_code:{username}"
    cached_verification_code = redis_conn.get(redis_key)
    if not cached_verification_code or cached_verification_code.decode("utf-8") != verification_code:
        log_msg = custom_log_message(username, 400, "کد وارد شده نادرست است")
        auth_logger.error(log_msg)
        raise HTTPException(status_code=400, detail="کد وارد شده نادرست است")


def generate_verification_code():
    return str(random.randint(1000, 9999))


# Register a new user
@router.post("/register")
def register(user_data: UserInput, redis_conn: redis.StrictRedis = Depends(get_redis_connection), session: Session = Depends(get_db)):
    if session.query(User).filter_by(username=user_data.username).first():
        log_msg = custom_log_message(user_data.username, 400, "کاربری با این نام کاربری از قبل وجود دارد")
        auth_logger.error(log_msg)
        raise HTTPException(status_code=400, detail="کاربری با این نام کاربری از قبل وجود دارد")

    hashed_password = get_password_hash(user_data.password)
    user = User(username=user_data.username, password_hash=hashed_password, phone_number=user_data.phone_number)
    session.add(user)
    verification_code = generate_verification_code()
    print(f"\n*******\n   {verification_code}   \n*******\n")
    store_verification_code(redis_conn, user_data.phone_number, str(verification_code))

    # Create a list to store user modules
    user.modules = []

    session.commit()
    log_msg = custom_log_message(user_data.username, 200, f"User registered successfully verification code sent to {user.phone_number}")
    auth_logger.info(log_msg)
    return {"message": f"User registered successfully\nverification code sent to {user.phone_number}"}


# Login and generate access token
@router.post("/login")
def login(user_data: LoginInput, session: Session = Depends(get_db)):
    user = session.query(User).filter_by(username=user_data.username).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        log_msg = custom_log_message(user_data.username, 401, "نام کاربری یا رمز عبور اشتباه است")
        auth_logger.error(log_msg)
        raise HTTPException(status_code=401, detail="نام کاربری یا رمز عبور اشتباه است")

    access_token, refresh_token = create_tokens(user_data.username)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
def refresh_tokens(refresh_token: str):
    username = verify_refresh_token(refresh_token)
    access_token, new_refresh_token = create_tokens(username)
    return {"access_token": access_token, "refresh_token": new_refresh_token}


@router.post("/verify-user")
def verify_email(user_input: UserCodeVerification, redis_conn: redis.StrictRedis = Depends(get_redis_connection), session: Session = Depends(get_db)):
    user = session.query(User).filter_by(username=user_input.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="کاربر از قبل فعال است")

    verify_verification_code(redis_conn, user.phone_number, user_input.verification_code)

    user.is_verified = True
    session.commit()

    return {"message": "User verified successfully"}


@router.post("/send-reset-code")
def send_reset_code(username: str, redis_conn: redis.StrictRedis = Depends(get_redis_connection), session: Session = Depends(get_db)):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    verification_code = generate_verification_code()
    print(f"\n*******\n   REST CODE: {verification_code}   \n*******\n")
    store_verification_code(redis_conn, user.phone_number, verification_code)

    # Here you can send the verification code to the user's phone number using SMS or any other method
    # For this example, we'll just return the verification code
    return {"message": f"SMS Sent to {user.phone_number}"}


@router.post("/reset-password")
def reset_password(user_input: ResetPasswordInput, redis_conn: redis.StrictRedis = Depends(get_redis_connection), session: Session = Depends(get_db)):
    user = session.query(User).filter_by(phone_number=user_input.phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    verify_verification_code(redis_conn, user_input.phone_number, user_input.verification_code)

    hashed_password = get_password_hash(user_input.new_password)
    user.password_hash = hashed_password
    session.commit()

    return {"message": "Password reset successful"}


@router.get("/retreive-user")
def get_user_data(user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user = session.query(User).filter_by(username=user).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    return {
        "id": user.id,
        "username": user.username,
        "phone_number": user.phone_number,
        "admin": user.is_admin,
        "registerer": user.is_registerer
    }
