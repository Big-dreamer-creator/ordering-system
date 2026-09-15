"""FastAPI 应用入口。

运行方式：
    uvicorn app.main:app --reload
在 backend 目录下执行。
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, dishes, orders, users
from .config import AUTO_INIT_DB
from .init_data import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动时初始化数据库。"""
    if AUTO_INIT_DB:
        init_db()
    yield


app = FastAPI(
    title="点餐系统 API",
    description="课程设计：简易点餐系统的后端接口。",
    version="1.0.0",
    lifespan=lifespan,
)

# 允许小程序开发工具跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(dishes.router)
app.include_router(orders.router)
app.include_router(users.router)


@app.get("/", tags=["系统"], summary="服务状态")
def root():
    return {"message": "点餐系统 API 运行中", "docs": "/docs"}
