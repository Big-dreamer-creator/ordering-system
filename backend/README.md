# 后端（FastAPI）

## 目录结构

```
backend/
├── app/
│   ├── main.py            # 应用入口，注册路由、启动时初始化数据库
│   ├── config.py          # 读取配置
│   ├── database.py        # 数据库连接、会话、Base
│   ├── models.py          # 数据库模型：User / Dish / Order / OrderItem
│   ├── schemas.py         # Pydantic 请求/响应模型
│   ├── init_data.py       # 建表 + 演示数据
│   ├── api/               # API 层：接收请求、参数校验、返回响应
│   │   ├── dishes.py
│   │   ├── orders.py
│   │   └── users.py
│   └── services/          # Service 层：业务逻辑
│       ├── dish_service.py
│       ├── order_service.py
│       └── user_service.py
├── pyproject.toml         # 项目依赖（由 uv 管理）
├── uv.lock                # uv 锁定文件
├── .python-version        # Python 版本
└── .env.example
```

## 运行步骤

依赖由 [uv](https://docs.astral.sh/uv/) 管理。uv 会自动下载所需 Python 版本并创建 `.venv`。

```bash
# 1. 进入后端目录
cd backend

# 2. 安装依赖并创建虚拟环境
uv sync

# 3. 配置数据库连接（复制后按需修改）
copy .env.example .env        # Windows
# cp .env.example .env        # macOS / Linux

# 4. 启动服务
uv run uvicorn app.main:app --reload
```

启动后：

- 接口地址：http://127.0.0.1:8000
- Swagger 文档：http://127.0.0.1:8000/docs

首次启动会自动建表并写入演示菜品和演示用户（`AUTO_INIT_DB=true`）。
也可以先执行 `database/init.sql` 手动初始化数据库。
