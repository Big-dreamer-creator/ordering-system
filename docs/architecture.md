# 系统架构

## 总体结构

系统采用前后端分离架构：

```
微信小程序
    ↓  HTTP / JSON
FastAPI
    ↓  业务处理
SQLAlchemy
    ↓
MySQL
```

## 各层职责

### 前端（frontend）

- 页面展示与用户交互
- 维护登录状态（用户信息保存在本地缓存）
- 维护购物车状态（保存在本地缓存，提交订单前不落库）
- 通过 `utils/api.js` 调用后端接口

### 后端（backend）

后端采用简单分层：

```
API 层  ->  Service 层  ->  Model / Database 层
```

| 层 | 文件 | 职责 |
| --- | --- | --- |
| API 层 | `app/api/*.py` | 接收请求、参数校验、调用 Service、返回响应 |
| Service 层 | `app/services/*.py` | 业务逻辑：注册登录、菜品查询、下单、订单查询、取消订单 |
| Model 层 | `app/models.py` | 数据库表映射 |
| Schema 层 | `app/schemas.py` | 请求/响应数据结构 |
| 数据库 | `app/database.py` | 连接 MySQL、会话管理 |

### 数据库（database）

- `init.sql`：建库、建表、写入测试数据

## 登录与下单流程

1. 小程序启动进入登录页，可登录或注册。
2. 登录/注册调用 `POST /api/auth/login` 或 `POST /api/auth/register`，
   Service 层校验密码（sha256 哈希），返回用户信息。
3. 小程序把用户信息保存到本地缓存，作为后续下单的用户。

下单流程：

1. 用户在点餐页点击“加入购物车”，数据写入本地缓存。
2. 在购物车页点击“提交订单”，小程序调用 `POST /api/orders`，
   请求体包含 `user_id`、`remark`、`items`（菜品 ID 和数量）。
3. FastAPI 接收请求，Pydantic 校验参数，调用 `order_service.create_order`。
4. Service 层校验用户和菜品，计算小计与总价，
   创建 `orders` 和 `order_items` 记录。
5. SQLAlchemy 把数据写入 MySQL。
6. 接口返回订单详情，小程序清空购物车并返回首页。
7. 订单页通过 `GET /api/orders?user_id=<当前用户>` 查询并展示订单。

## 设计取舍

- 简单登录：用户名 + 密码，密码哈希保存；登录后小程序本地保存用户信息，
  未引入 token / JWT 等复杂鉴权，降低答辩解释成本。
- 购物车只在前端：提交订单前不占用数据库，结构更简单。
- 订单明细保存菜品名称和单价快照：即使菜品后续改价，历史订单金额不变。
