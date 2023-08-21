from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import requests
from security import get_current_user
from models import User, Module, UserModule
from schemas import Input1
import time

router = APIRouter()


@router.post("/mock1")
def mock(request_data: Input1, user: str = Depends(get_current_user), session: Session = Depends(get_db)):
    user_db = session.query(User).filter_by(username=user).first()
    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid user")
    return {"result": f"this is mock object for summerizer: {request_data.input_data}"}
