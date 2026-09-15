-- ============================================================
-- 点餐系统数据库初始化脚本
-- 数据库：MySQL 8.0
-- 说明：包含建库、建表和测试数据
-- 使用方式：
--   mysql -u root -p < database/init.sql
-- 若命令行出现中文乱码，可加上字符集参数：
--   mysql -u root -p --default-character-set=utf8mb4 < database/init.sql
-- ============================================================

-- 设置客户端连接字符集，保证中文默认值和测试数据正常写入
SET NAMES utf8mb4;

-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS ordering_system
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE ordering_system;

-- 2. 删除旧表（注意外键顺序：先删子表，再删父表）
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS dishes;
DROP TABLE IF EXISTS users;

-- ============================================================
-- 3. 用户表
-- ============================================================
CREATE TABLE users (
    id            INT          NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    username      VARCHAR(50)  NOT NULL               COMMENT '登录用户名',
    password_hash VARCHAR(64)  NOT NULL               COMMENT '密码哈希（sha256）',
    nickname      VARCHAR(50)  NOT NULL               COMMENT '昵称',
    phone         VARCHAR(20)  NULL                   COMMENT '手机号',
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_username (username)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '用户表';

-- ============================================================
-- 4. 菜品表
-- ============================================================
CREATE TABLE dishes (
    id           INT           NOT NULL AUTO_INCREMENT COMMENT '菜品ID',
    name         VARCHAR(100)  NOT NULL               COMMENT '菜品名称',
    category     VARCHAR(50)   NOT NULL DEFAULT '其他' COMMENT '分类',
    description  VARCHAR(255)  NULL                   COMMENT '描述',
    price        DECIMAL(10,2) NOT NULL               COMMENT '价格',
    image        VARCHAR(255)  NULL                   COMMENT '图片地址',
    is_available TINYINT(1)    NOT NULL DEFAULT 1     COMMENT '是否上架：1上架 0下架',
    created_at   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '菜品表';

-- ============================================================
-- 5. 订单表
-- ============================================================
CREATE TABLE orders (
    id           INT           NOT NULL AUTO_INCREMENT COMMENT '订单ID',
    order_no     VARCHAR(32)   NOT NULL               COMMENT '订单编号',
    user_id      INT           NOT NULL               COMMENT '下单用户ID',
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00  COMMENT '订单总金额',
    status       VARCHAR(20)   NOT NULL DEFAULT '已提交' COMMENT '订单状态：已提交/已取消',
    remark       VARCHAR(255)  NULL                   COMMENT '备注',
    created_at   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '下单时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_order_no (order_no),
    KEY idx_user_id (user_id),
    CONSTRAINT fk_order_user FOREIGN KEY (user_id) REFERENCES users (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '订单表';

-- ============================================================
-- 6. 订单明细表
-- 说明：保存下单时的菜品名称和单价快照，避免菜品后续修改影响历史订单
-- ============================================================
CREATE TABLE order_items (
    id        INT           NOT NULL AUTO_INCREMENT COMMENT '明细ID',
    order_id  INT           NOT NULL               COMMENT '订单ID',
    dish_id   INT           NOT NULL               COMMENT '菜品ID',
    dish_name VARCHAR(100)  NOT NULL               COMMENT '菜品名称快照',
    price     DECIMAL(10,2) NOT NULL               COMMENT '单价快照',
    quantity  INT           NOT NULL DEFAULT 1     COMMENT '数量',
    subtotal  DECIMAL(10,2) NOT NULL DEFAULT 0.00  COMMENT '小计',
    PRIMARY KEY (id),
    KEY idx_order_id (order_id),
    CONSTRAINT fk_item_order FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
    CONSTRAINT fk_item_dish FOREIGN KEY (dish_id) REFERENCES dishes (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '订单明细表';

-- ============================================================
-- 7. 测试数据：用户
-- ============================================================
-- 默认演示账号：demo / 123456
INSERT INTO users (id, username, password_hash, nickname, phone) VALUES
    (1, 'demo', 'a359119dcbcee07851d5ce01a182ba1e911ce5fc76d16925b634263e0b1491b6', '演示用户', '13800000000');

-- ============================================================
-- 8. 测试数据：菜品
-- ============================================================
INSERT INTO dishes (name, category, description, price, image, is_available) VALUES
    ('宫保鸡丁', '热菜', '鸡肉丁配花生米，微辣', 28.00, '', 1),
    ('鱼香肉丝', '热菜', '经典川菜，酸甜微辣', 26.00, '', 1),
    ('红烧肉',   '热菜', '肥而不腻，入口即化', 38.00, '', 1),
    ('麻婆豆腐', '热菜', '麻辣鲜香，下饭首选', 18.00, '', 1),
    ('凉拌黄瓜', '凉菜', '清爽开胃', 10.00, '', 1),
    ('口水鸡',   '凉菜', '麻辣鲜香，回味无穷', 22.00, '', 1),
    ('米饭',     '主食', '东北大米，粒粒分明', 2.00,  '', 1),
    ('蛋炒饭',   '主食', '粒粒分明，蛋香十足', 12.00, '', 1),
    ('可乐',     '饮品', '冰镇可乐 330ml', 4.00,  '', 1),
    ('酸梅汤',   '饮品', '自制酸梅汤，解腻', 6.00,  '', 1);
