"""订单业务。"""

import random
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..models import Dish, Order, OrderItem, User
from ..schemas import OrderCreate


def _generate_order_no() -> str:
    """生成订单编号：时间戳 + 4 位随机数。"""
    return datetime.now().strftime("%Y%m%d%H%M%S") + f"{random.randint(0, 9999):04d}"


def create_order(db: Session, data: OrderCreate) -> Order:
    """创建订单。

    流程：校验用户 -> 逐个校验菜品 -> 计算金额 -> 保存订单和明细。
    """
    user = db.get(User, data.user_id)
    if user is None:
        raise ValueError("用户不存在")

    order = Order(
        order_no=_generate_order_no(),
        user_id=data.user_id,
        status="已提交",
        remark=data.remark,
        total_amount=Decimal("0.00"),
    )

    total = Decimal("0.00")
    for item in data.items:
        dish = db.get(Dish, item.dish_id)
        if dish is None:
            raise ValueError(f"菜品不存在（id={item.dish_id}）")
        if not dish.is_available:
            raise ValueError(f"菜品「{dish.name}」已下架")

        price = Decimal(dish.price)
        subtotal = (price * item.quantity).quantize(Decimal("0.01"))
        total += subtotal

        order.items.append(
            OrderItem(
                dish_id=dish.id,
                dish_name=dish.name,
                price=price,
                quantity=item.quantity,
                subtotal=subtotal,
            )
        )

    order.total_amount = total
    db.add(order)
    db.commit()
    # 重新查询，确保订单明细已加载后返回
    return get_order(db, order.id)


def list_orders(db: Session, user_id: Optional[int] = None) -> List[Order]:
    """查询订单列表，可按用户筛选，按下单时间倒序。"""
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc(), Order.id.desc())
    )
    if user_id is not None:
        stmt = stmt.where(Order.user_id == user_id)

    return list(db.execute(stmt).scalars().all())


def get_order(db: Session, order_id: int) -> Optional[Order]:
    """按 ID 查询订单详情（包含明细）。"""
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    )
    return db.execute(stmt).scalars().first()


def cancel_order(db: Session, order_id: int) -> Order:
    """取消订单，仅「已提交」状态可取消。"""
    order = get_order(db, order_id)
    if order is None:
        raise ValueError("订单不存在")
    if order.status != "已提交":
        raise ValueError(f"订单当前状态为「{order.status}」，不能取消")

    order.status = "已取消"
    db.commit()
    return get_order(db, order_id)
