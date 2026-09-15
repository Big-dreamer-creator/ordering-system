"""菜品相关接口。"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import DishOut
from ..services import dish_service

router = APIRouter(prefix="/api", tags=["菜品"])


@router.get("/dishes", response_model=List[DishOut], summary="获取菜品列表")
def list_dishes(
    category: Optional[str] = Query(default=None, description="按分类筛选"),
    keyword: Optional[str] = Query(default=None, description="按名称关键字搜索"),
    db: Session = Depends(get_db),
):
    return dish_service.list_dishes(db, category=category, keyword=keyword)


@router.get("/dishes/{dish_id}", response_model=DishOut, summary="获取菜品详情")
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = dish_service.get_dish(db, dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="菜品不存在")
    return dish


@router.get("/categories", response_model=List[str], summary="获取菜品分类")
def list_categories(db: Session = Depends(get_db)):
    return dish_service.list_categories(db)
