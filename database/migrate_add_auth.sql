-- ============================================================
-- 增量迁移：给“已有的旧版 users 表”补充登录字段
-- 适用场景：数据库里已经有用户/订单数据，不想用 init.sql 重建
-- 使用方式：
--   mysql -u root -p --default-character-set=utf8mb4 < database/migrate_add_auth.sql
-- 注意：只需执行一次
-- ============================================================

USE ordering_system;

SET NAMES utf8mb4;

-- 1. 新增 username、password_hash 两列
ALTER TABLE users
    ADD COLUMN username VARCHAR(50) NOT NULL DEFAULT '' COMMENT '登录用户名' AFTER id,
    ADD COLUMN password_hash VARCHAR(64) NOT NULL DEFAULT '' COMMENT '密码哈希' AFTER username;

-- 2. 给已有用户补一个不重复的用户名
UPDATE users SET username = CONCAT('user', id) WHERE username = '';

-- 3. 演示账号：demo / 123456（id=1 如果是老演示用户，就改成 demo）
UPDATE users
SET username = 'demo',
    password_hash = 'a359119dcbcee07851d5ce01a182ba1e911ce5fc76d16925b634263e0b1491b6'
WHERE id = 1;

-- 4. 其余用户的密码统一重置为 123456（登录后可在“编辑资料”外自行改）
UPDATE users
SET password_hash = 'a359119dcbcee07851d5ce01a182ba1e911ce5fc76d16925b634263e0b1491b6'
WHERE password_hash = '';

-- 5. 给 username 加唯一索引
ALTER TABLE users ADD UNIQUE KEY uk_username (username);
