"""菜品业务。"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Dish


def list_dishes(
    db: Session,
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    only_available: bool = True,
) -> List[Dish]:
    """查询菜品列表，可按分类和名称关键字筛选。"""
    stmt = select(Dish)

    if only_available:
        stmt = stmt.where(Dish.is_available.is_(True))
    if category:
        stmt = stmt.where(Dish.category == category)
    if keyword:
        stmt = stmt.where(Dish.name.like(f"%{keyword}%"))

    stmt = stmt.order_by(Dish.category, Dish.id)
    return list(db.execute(stmt).scalars().all())


def get_dish(db: Session, dish_id: int) -> Optional[Dish]:
    """按 ID 查询单个菜品。"""
    return db.get(Dish, dish_id)


def list_categories(db: Session) -> List[str]:
    """查询所有已上架菜品的分类。"""
    stmt = (
        select(Dish.category)
        .where(Dish.is_available.is_(True))
        .distinct()
        .order_by(Dish.category)
    )
    return [row[0] for row in db.execute(stmt).all()]
