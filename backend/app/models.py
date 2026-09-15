"""数据库模型。

核心实体：用户、菜品、订单、订单明细。
关系：用户 -> 订单 -> 订单明细 -> 菜品
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """用户表。"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(50), unique=True, nullable=False, comment="登录用户名")
    password_hash = Column(String(64), nullable=False, comment="密码哈希")
    nickname = Column(String(50), nullable=False, comment="昵称")
    phone = Column(String(20), nullable=True, comment="手机号")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    orders = relationship("Order", back_populates="user")


class Dish(Base):
    """菜品表。"""

    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="菜品ID")
    name = Column(String(100), nullable=False, comment="菜品名称")
    category = Column(String(50), nullable=False, default="其他", comment="分类")
    description = Column(String(255), nullable=True, comment="描述")
    price = Column(Numeric(10, 2), nullable=False, comment="价格")
    image = Column(String(255), nullable=True, comment="图片地址")
    is_available = Column(Boolean, default=True, comment="是否上架")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")


class Order(Base):
    """订单表。"""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="订单ID")
    order_no = Column(String(32), unique=True, nullable=False, comment="订单编号")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    total_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="总金额")
    status = Column(String(20), nullable=False, default="已提交", comment="订单状态")
    remark = Column(String(255), nullable=True, comment="备注")
    created_at = Column(DateTime, default=datetime.now, comment="下单时间")

    user = relationship("User", back_populates="orders")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderItem(Base):
    """订单明细表。"""

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="明细ID")
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, comment="订单ID")
    dish_id = Column(Integer, ForeignKey("dishes.id"), nullable=False, comment="菜品ID")
    dish_name = Column(String(100), nullable=False, comment="菜品名称快照")
    price = Column(Numeric(10, 2), nullable=False, comment="单价快照")
    quantity = Column(Integer, nullable=False, default=1, comment="数量")
    subtotal = Column(Numeric(10, 2), nullable=False, default=0, comment="小计")

    order = relationship("Order", back_populates="items")
