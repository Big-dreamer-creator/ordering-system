"""订单相关接口。"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import OrderCreate, OrderOut
from ..services import order_service

router = APIRouter(prefix="/api/orders", tags=["订单"])


@router.post("", response_model=OrderOut, status_code=201, summary="提交订单")
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    try:
        return order_service.create_order(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("", response_model=List[OrderOut], summary="获取订单列表")
def list_orders(
    user_id: Optional[int] = Query(default=None, description="按用户筛选"),
    db: Session = Depends(get_db),
):
    return order_service.list_orders(db, user_id=user_id)


@router.get("/{order_id}", response_model=OrderOut, summary="获取订单详情")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order


@router.post("/{order_id}/cancel", response_model=OrderOut, summary="取消订单")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    try:
        return order_service.cancel_order(db, order_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
