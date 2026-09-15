"""Pydantic 数据模型。

用于请求参数校验和响应序列化，与 models.py 中的数据库模型分开。
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# 用户
# ============================================================
class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="登录用户名")
    password: str = Field(min_length=6, max_length=50, description="密码，至少 6 位")
    nickname: Optional[str] = Field(default=None, max_length=50, description="昵称，默认与用户名相同")
    phone: Optional[str] = Field(default=None, max_length=20, description="手机号")


class UserLogin(BaseModel):
    username: str = Field(description="登录用户名")
    password: str = Field(description="密码")


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nickname: str
    phone: Optional[str] = None
    created_at: datetime


class UserUpdate(BaseModel):
    """更新用户资料，字段均为可选，只更新传入的字段。"""

    nickname: Optional[str] = Field(default=None, min_length=1, max_length=50, description="昵称")
    phone: Optional[str] = Field(default=None, max_length=20, description="手机号")


# ============================================================
# 菜品
# ============================================================
class DishOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None
    is_available: bool


# ============================================================
# 订单
# ============================================================
class OrderItemIn(BaseModel):
    """下单时提交的单个菜品。"""

    dish_id: int = Field(description="菜品ID")
    quantity: int = Field(gt=0, description="数量，必须大于 0")


class OrderCreate(BaseModel):
    """创建订单的请求体。"""

    user_id: int = Field(description="下单用户ID")
    remark: Optional[str] = Field(default=None, max_length=255, description="备注")
    items: List[OrderItemIn] = Field(min_length=1, description="订单明细，至少一个菜品")


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dish_id: int
    dish_name: str
    price: float
    quantity: int
    subtotal: float


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_no: str
    user_id: int
    total_amount: float
    status: str
    remark: Optional[str] = None
    created_at: datetime
    items: List[OrderItemOut] = []


# ============================================================
# 通用响应
# ============================================================
class MessageOut(BaseModel):
    message: str
