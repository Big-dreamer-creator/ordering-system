"""用户业务：注册、登录、资料更新。

密码使用 sha256 + 固定盐做哈希，不保存明文。
（课程演示用的简化方案，未做逐用户随机盐和 token 鉴权。）
"""

import hashlib
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import User
from ..schemas import UserLogin, UserRegister, UserUpdate

# 固定盐，仅用于演示，真实项目应使用 bcrypt 等方案
PASSWORD_SALT = "ordering_system_salt"


def hash_password(password: str) -> str:
    """对密码做 sha256 哈希。"""
    return hashlib.sha256((password + PASSWORD_SALT).encode("utf-8")).hexdigest()


def get_user(db: Session, user_id: int) -> Optional[User]:
    """按 ID 查询用户。"""
    return db.get(User, user_id)


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """按用户名查询用户。"""
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalars().first()


def register_user(db: Session, data: UserRegister) -> User:
    """注册新用户，用户名不能重复。"""
    if get_user_by_username(db, data.username) is not None:
        raise ValueError("用户名已存在")

    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        nickname=data.nickname or data.username,
        phone=data.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, data: UserLogin) -> User:
    """校验用户名和密码，成功返回用户。"""
    user = get_user_by_username(db, data.username)
    if user is None or user.password_hash != hash_password(data.password):
        raise ValueError("用户名或密码错误")
    return user


def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    """更新用户资料，只更新传入的字段。"""
    user = get_user(db, user_id)
    if user is None:
        raise ValueError("用户不存在")

    if data.nickname is not None:
        user.nickname = data.nickname
    if data.phone is not None:
        user.phone = data.phone

    db.commit()
    db.refresh(user)
    return user
