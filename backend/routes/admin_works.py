from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from security import get_current_user, get_admin_user
from models import User, Module, UserModule
from schemas import SetRateLimit, ModuleDeleteRequest, EditUserRole

router = APIRouter()


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

    if rate_limit_data.expire_time < datetime.now():
        raise HTTPException(status_code=400, detail="زمان انقضا باید در آینده باشد")

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
            expire_time=rate_limit_data.expire_time
        )
        session.add(new_user_module)
        session.commit()
    else:
        user_module.limit = rate_limit_data.limit
        user_module.tokens = rate_limit_data.limit
        user_module.expire_time = rate_limit_data.expire_time
        session.commit()

    return {"message": "محدودیت نرخ با موفقیت بروزرسانی شد"}


@router.delete("/edit-user-role")
def edit_user_role(request_data: EditUserRole, user: str = Depends(get_admin_user), session: Session = Depends(get_db)):
    target_user = session.query(User).filter_by(username=request_data.username).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    target_user.is_admin = request_data.is_admin
    target_user.is_registerer = request_data.is_registerer

    session.commit()

    return {"message": f"کاربر {target_user.username} با موفقیت تغییر پیدا کرد"}
