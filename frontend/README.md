# 前端（微信小程序原生）

## 目录结构

```
frontend/
├── app.js                 # 入口，保存全局配置（后端地址、用户ID）
├── app.json               # 页面注册、tabBar、窗口样式
├── app.wxss               # 全局样式
├── project.config.json    # 开发者工具项目配置
├── sitemap.json
├── package.json           # 依赖与脚本（由 bun 管理）
├── bun.lock               # bun 锁定文件
├── jsconfig.json          # 编辑器类型提示配置
├── scripts/
│   └── check.js           # 前端自检：校验 JSON 和 JS 语法
├── utils/
│   ├── api.js             # 后端接口封装
│   ├── cart.js            # 购物车状态（本地缓存）
│   └── util.js            # 时间、金额格式化
└── pages/
    ├── login/             # 登录 / 注册
    ├── index/             # 点餐：搜索 + 菜品分类 + 菜品列表 + 加入购物车
    ├── cart/              # 购物车：修改数量、备注、提交订单
    ├── orders/            # 订单列表
    ├── order-detail/      # 订单详情 + 取消订单
    ├── profile/           # 我的：用户信息 + 订单统计 + 退出登录
    └── profile-edit/      # 编辑资料：昵称、手机号
```

## 运行步骤

依赖和脚本由 [bun](https://bun.sh/) 管理：

```bash
cd frontend
bun install      # 安装依赖（主要是编辑器类型提示）
bun run check    # 校验 JSON 和 JS 语法
```

小程序运行步骤：

1. 先用微信开发者工具打开 `frontend` 目录。
2. 在 `project.config.json` 中把 `appid` 改成自己的小程序 AppID（或用测试号）。
3. 确认后端已启动在 `http://127.0.0.1:8000`。
4. 启动后进入登录页，使用演示账号 `demo / 123456` 登录，或直接注册新账号。
5. 如需真机预览，把 `app.js` 中的 `baseUrl` 改成电脑的局域网 IP，
   例如 `http://192.168.1.10:8000/api`，并确保手机与电脑在同一网络。

> 小程序本身是原生开发，不经过打包工具；bun 只负责管理依赖和运行校验脚本。
> 开发者工具默认已关闭域名校验（`urlCheck: false`），可直接请求本地 HTTP 接口。
