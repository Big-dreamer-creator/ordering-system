# 简易点餐系统

一个用于课程设计和答辩的前后端分离点餐系统。

- 前端：微信小程序原生开发（JavaScript / WXML / WXSS）
- 后端：Python + FastAPI + SQLAlchemy
- 数据库：MySQL
- 通信：HTTP + JSON，REST 风格 API

## 功能

```
登录/注册 -> 查看菜品 -> 加入购物车 -> 修改购物车 -> 提交订单 -> 查看订单
```

- 用户注册、登录（密码使用 sha256 哈希保存）
- 菜品搜索、按分类展示
- 购物车数量增减、删除、清空（保存在小程序本地缓存）
- 提交订单，后端保存到 MySQL
- 订单列表、订单详情、取消订单
- 个人中心：订单统计、编辑昵称和手机号、退出登录

## 目录结构

```
ordering-system/
├── backend/      # FastAPI 后端
├── frontend/     # 微信小程序
├── database/     # 数据库初始化 SQL
└── docs/         # 项目文档
```

## 快速开始

### 1. 初始化数据库

```bash
mysql -u root -p < database/init.sql
```

（也可以跳过这一步，后端首次启动会自动建表并写入演示数据）

> 如果之前已经建过库、启动报 `Unknown column 'users.username'`，
> 说明旧表没同步。执行 `database/init.sql` 重建，
> 或执行 `database/migrate_add_auth.sql` 做增量迁移（保留数据）。

### 2. 启动后端（uv 管理）

```bash
cd backend
uv sync                         # 创建虚拟环境并安装依赖
copy .env.example .env          # 按需修改数据库账号密码
uv run uvicorn app.main:app --reload
```

- 接口地址：http://127.0.0.1:8000
- Swagger 文档：http://127.0.0.1:8000/docs

### 3. 启动前端（bun 管理）

```bash
cd frontend
bun install
bun run check
```

然后用微信开发者工具打开 `frontend` 目录即可。

## 文档

- [答辩代码讲解文档](docs/答辩文档.md)
- [系统架构](docs/architecture.md)
- [API 接口文档](docs/api.md)
- [数据库设计](docs/database.md)
