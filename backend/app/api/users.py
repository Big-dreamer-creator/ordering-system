"""用户相关接口。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserOut, UserUpdate
from ..services import user_service

router = APIRouter(prefix="/api/users", tags=["用户"])


@router.get("/{user_id}", response_model=UserOut, summary="获取用户信息")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/{user_id}", response_model=UserOut, summary="更新用户资料")
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    try:
        return user_service.update_user(db, user_id, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
