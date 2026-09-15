"""项目配置。

只从环境变量（或 backend/.env）中读取少量配置，保持简单。
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# backend 目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 加载 backend/.env（如果存在）
load_dotenv(BASE_DIR / ".env")

# MySQL 连接地址
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:123456@127.0.0.1:3306/ordering_system?charset=utf8mb4",
)

# 是否在启动时自动建表并写入演示数据
AUTO_INIT_DB = os.getenv("AUTO_INIT_DB", "true").lower() == "true"
