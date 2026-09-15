"""数据库连接。

使用 SQLAlchemy 连接 MySQL，并提供 FastAPI 依赖使用的 get_db。
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL

# 创建数据库引擎
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)

# 会话工厂
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 所有模型继承的基类
Base = declarative_base()


def get_db():
    """FastAPI 依赖：为每个请求提供一个数据库会话，请求结束后关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
