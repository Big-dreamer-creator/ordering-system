"""认证相关接口：注册、登录。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserLogin, UserOut, UserRegister
from ..services import user_service

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=UserOut, status_code=201, summary="注册")
def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        return user_service.register_user(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/login", response_model=UserOut, summary="登录")
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        return user_service.login_user(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
