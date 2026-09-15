"""数据库初始化。

服务启动时自动建表，并在表为空时写入演示数据。
如果已经用 database/init.sql 初始化过数据库，这里不会重复写入。
"""

from sqlalchemy import func, select

from .database import Base, SessionLocal, engine
from .models import Dish, User
from .services.user_service import hash_password

DEMO_DISHES = [
    {"name": "宫保鸡丁", "category": "热菜", "description": "鸡肉丁配花生米，微辣", "price": 28.00},
    {"name": "鱼香肉丝", "category": "热菜", "description": "经典川菜，酸甜微辣", "price": 26.00},
    {"name": "红烧肉", "category": "热菜", "description": "肥而不腻，入口即化", "price": 38.00},
    {"name": "麻婆豆腐", "category": "热菜", "description": "麻辣鲜香，下饭首选", "price": 18.00},
    {"name": "凉拌黄瓜", "category": "凉菜", "description": "清爽开胃", "price": 10.00},
    {"name": "口水鸡", "category": "凉菜", "description": "麻辣鲜香，回味无穷", "price": 22.00},
    {"name": "米饭", "category": "主食", "description": "东北大米，粒粒分明", "price": 2.00},
    {"name": "蛋炒饭", "category": "主食", "description": "粒粒分明，蛋香十足", "price": 12.00},
    {"name": "可乐", "category": "饮品", "description": "冰镇可乐 330ml", "price": 4.00},
    {"name": "酸梅汤", "category": "饮品", "description": "自制酸梅汤，解腻", "price": 6.00},
]


def init_db() -> None:
    """建表并写入演示数据。"""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        dish_count = db.execute(select(func.count()).select_from(Dish)).scalar()
        if dish_count == 0:
            db.add_all([Dish(**dish) for dish in DEMO_DISHES])

        if db.get(User, 1) is None:
            db.add(
                User(
                    id=1,
                    username="demo",
                    password_hash=hash_password("123456"),
                    nickname="演示用户",
                    phone="13800000000",
                )
            )

        db.commit()
    finally:
        db.close()
