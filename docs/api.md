# API 接口文档

- 基础地址：`http://127.0.0.1:8000`
- 数据格式：JSON
- 交互文档（Swagger）：`http://127.0.0.1:8000/docs`
- 错误响应格式：`{"detail": "错误信息"}`

## 一、系统

### GET /

返回服务状态。

```json
{ "message": "点餐系统 API 运行中", "docs": "/docs" }
```

## 二、认证

### POST /api/auth/register

注册新用户。

```json
{
  "username": "zhangsan",
  "password": "123456",
  "nickname": "张三",
  "phone": "13900000000"
}
```

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| username | string | 是 | 用户名，3-50 位 |
| password | string | 是 | 密码，6-50 位 |
| nickname | string | 否 | 昵称，默认与用户名相同 |
| phone | string | 否 | 手机号 |

响应 `201` 为用户对象（同下方 UserOut）。用户名已存在返回 `400`。

### POST /api/auth/login

登录。

```json
{ "username": "demo", "password": "123456" }
```

响应为用户对象。用户名或密码错误返回 `400`。

```json
{
  "id": 1,
  "username": "demo",
  "nickname": "演示用户",
  "phone": "13800000000",
  "created_at": "2026-09-13T12:00:00"
}
```

> 演示账号：`demo / 123456`

## 三、菜品

### GET /api/dishes

获取菜品列表。

| 参数 | 位置 | 必填 | 说明 |
| --- | --- | --- | --- |
| category | query | 否 | 按分类筛选，如 `热菜` |
| keyword | query | 否 | 按名称关键字搜索 |

响应：

```json
[
  {
    "id": 1,
    "name": "宫保鸡丁",
    "category": "热菜",
    "description": "鸡肉丁配花生米，微辣",
    "price": 28.0,
    "image": "",
    "is_available": true
  }
]
```

### GET /api/dishes/{dish_id}

获取菜品详情。菜品不存在返回 `404`。

### GET /api/categories

获取所有已上架菜品的分类。

```json
["主食", "凉菜", "热菜", "饮品"]
```

## 四、订单

### POST /api/orders

提交订单。

请求体：

```json
{
  "user_id": 1,
  "remark": "不要辣",
  "items": [
    { "dish_id": 1, "quantity": 2 },
    { "dish_id": 7, "quantity": 1 }
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| user_id | int | 是 | 下单用户 ID |
| remark | string | 否 | 备注，最长 255 |
| items | array | 是 | 订单明细，至少一个 |
| items[].dish_id | int | 是 | 菜品 ID |
| items[].quantity | int | 是 | 数量，必须大于 0 |

响应 `201`：

```json
{
  "id": 1,
  "order_no": "202609131230001234",
  "user_id": 1,
  "total_amount": 58.0,
  "status": "已提交",
  "remark": "不要辣",
  "created_at": "2026-09-13T12:30:00",
  "items": [
    {
      "id": 1,
      "dish_id": 1,
      "dish_name": "宫保鸡丁",
      "price": 28.0,
      "quantity": 2,
      "subtotal": 56.0
    }
  ]
}
```

错误：用户不存在、菜品不存在、菜品已下架时返回 `400`。

### GET /api/orders

获取订单列表，按下单时间倒序。

| 参数 | 位置 | 必填 | 说明 |
| --- | --- | --- | --- |
| user_id | query | 否 | 按用户筛选 |

### GET /api/orders/{order_id}

获取订单详情（包含明细）。不存在返回 `404`。

### POST /api/orders/{order_id}/cancel

取消订单，仅“已提交”状态可取消，否则返回 `400`。响应为更新后的订单对象。

## 五、用户

### GET /api/users/{user_id}

获取用户信息。不存在返回 `404`。

响应：

```json
{
  "id": 1,
  "username": "demo",
  "nickname": "演示用户",
  "phone": "13800000000",
  "created_at": "2026-09-13T12:00:00"
}
```

### PUT /api/users/{user_id}

更新用户资料，字段可选，只更新传入的字段。

```json
{ "nickname": "张三", "phone": "13900000000" }
```

用户不存在返回 `400`，昵称为空返回 `422`。

## 六、状态码说明

| 状态码 | 含义 |
| --- | --- |
| 200 | 请求成功 |
| 201 | 创建成功（注册、下单） |
| 400 | 参数或业务错误（如用户名已存在、菜品已下架） |
| 404 | 资源不存在 |
| 422 | 请求参数校验失败（FastAPI 自动返回） |
