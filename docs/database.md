# 数据库设计

数据库：MySQL 8.0
字符集：utf8mb4
初始化脚本：`database/init.sql`

## 表关系

```
users (用户)
  └─ orders (订单)
        └─ order_items (订单明细)
              └─ dishes (菜品)
```

- 一个用户可以有多个订单
- 一个订单可以有多个订单明细
- 一条明细对应一个菜品

## 1. users 用户表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| id | INT | 主键，自增 | 用户 ID |
| username | VARCHAR(50) | 非空，唯一 | 登录用户名 |
| password_hash | VARCHAR(64) | 非空 | 密码哈希（sha256） |
| nickname | VARCHAR(50) | 非空 | 昵称 |
| phone | VARCHAR(20) | 可空 | 手机号 |
| created_at | DATETIME | 非空，默认当前时间 | 创建时间 |

> 密码使用 `sha256(密码 + 固定盐)` 保存，不存明文。
> 这是课程演示的简化方案，真实项目应使用 bcrypt 等更安全的方式。

## 2. dishes 菜品表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| id | INT | 主键，自增 | 菜品 ID |
| name | VARCHAR(100) | 非空 | 菜品名称 |
| category | VARCHAR(50) | 非空，默认“其他” | 分类 |
| description | VARCHAR(255) | 可空 | 描述 |
| price | DECIMAL(10,2) | 非空 | 价格 |
| image | VARCHAR(255) | 可空 | 图片地址 |
| is_available | TINYINT(1) | 非空，默认 1 | 是否上架 |
| created_at | DATETIME | 非空，默认当前时间 | 创建时间 |

## 3. orders 订单表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| id | INT | 主键，自增 | 订单 ID |
| order_no | VARCHAR(32) | 非空，唯一 | 订单编号 |
| user_id | INT | 非空，外键 -> users.id | 下单用户 |
| total_amount | DECIMAL(10,2) | 非空，默认 0 | 订单总金额 |
| status | VARCHAR(20) | 非空，默认“已提交” | 订单状态 |
| remark | VARCHAR(255) | 可空 | 备注 |
| created_at | DATETIME | 非空，默认当前时间 | 下单时间 |

订单状态：`已提交`、`已取消`。

## 4. order_items 订单明细表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| id | INT | 主键，自增 | 明细 ID |
| order_id | INT | 非空，外键 -> orders.id | 所属订单 |
| dish_id | INT | 非空，外键 -> dishes.id | 菜品 ID |
| dish_name | VARCHAR(100) | 非空 | 菜品名称快照 |
| price | DECIMAL(10,2) | 非空 | 单价快照 |
| quantity | INT | 非空，默认 1 | 数量 |
| subtotal | DECIMAL(10,2) | 非空，默认 0 | 小计 |

> 说明：`dish_name` 和 `price` 保存的是下单时的快照，
> 这样菜品后续改名或调价都不会影响历史订单。

## 金额计算规则

```
小计 subtotal = price × quantity
总金额 total_amount = 所有明细 subtotal 之和
```

金额使用 `DECIMAL(10,2)`，避免浮点误差；计算在后端 Service 层完成。

## 演示数据

`init.sql` 会写入：

- 1 个演示用户（`username=demo`，`password=123456`）
- 10 个菜品，覆盖热菜、凉菜、主食、饮品四类

## 升级已有数据库

如果之前已经建过库，`users` 表还没有 `username` / `password_hash` 字段，
后端启动会报 `Unknown column 'users.username' in 'field list'`。

原因是 `Base.metadata.create_all()` 只会创建缺失的表，**不会修改已存在的表**。

两种处理方式：

**方式一：直接重建（简单，会清空数据）**

```bash
mysql -u root -p < database/init.sql
```

**方式二：保留数据，执行增量迁移（只需执行一次）**

```bash
mysql -u root -p --default-character-set=utf8mb4 < database/migrate_add_auth.sql
```

迁移脚本会：新增 `username` / `password_hash` 两列 → 给老用户补用户名 →
把 id=1 设为演示账号 `demo / 123456` → 给 `username` 加唯一索引。
