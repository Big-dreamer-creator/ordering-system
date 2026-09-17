# 前端说明文档（微信小程序）

本文档面向**第一次接触本项目的人**，从上到下说明：

- 前端目录里每个文件放在哪里、负责什么
- 每个页面长什么样、有哪些操作
- 每个页面调用了哪些后端接口、请求是怎么发出去的
- 一次完整的“点餐 → 下单 → 查看订单”在前后端之间如何流转

配合阅读：`docs/architecture.md`（整体架构）、`docs/api.md`（接口字段明细）。

---

## 一、前端技术栈与总体思路

| 项目 | 说明 |
| --- | --- |
| 框架 | 微信小程序**原生开发**（无 Vue / React / uni-app） |
| 语言 | JavaScript + WXML + WXSS + JSON |
| 通信 | `wx.request` 发 HTTP 请求，数据格式 JSON，REST 风格 |
| 后端地址 | `http://127.0.0.1:8000/api`（写在 `app.js`，真机调试改成电脑局域网 IP） |

设计原则：页面只做“展示 + 收集用户操作”，所有网络请求统一走 `utils/api.js`，
所有购物车逻辑统一走 `utils/cart.js`，页面代码保持简单、易讲解。

登录方式很简单：登录/注册成功后，后端返回用户对象，小程序把用户信息存在**本地缓存**里。
之后请求需要用户身份时，直接把 `user_id` 作为参数传给后端（**没有 token / JWT**）。

---

## 二、目录结构总览

```
frontend/
├── app.js                     # 小程序入口：全局配置（后端地址、当前用户）
├── app.json                   # 页面注册、tabBar、窗口样式
├── app.wxss                   # 全局样式（按钮、卡片、空状态等）
├── project.config.json        # 微信开发者工具项目配置（appid、urlCheck 等）
├── sitemap.json               # 小程序索引配置（默认即可）
├── package.json / bun.lock    # 依赖与脚本（bun 管理，仅用于类型提示和自检）
├── jsconfig.json              # 编辑器类型提示配置
├── scripts/
│   └── check.js               # 前端自检脚本：校验 JSON / JS 语法
├── utils/
│   ├── api.js                 # 所有后端接口的封装（唯一发请求的地方）
│   ├── cart.js                # 购物车状态管理（存本地缓存）
│   └── util.js                # 时间、金额格式化
└── pages/
    ├── login/                 # 登录 / 注册
    ├── index/                 # 点餐（首页 tab）
    ├── cart/                  # 购物车（tab）
    ├── orders/                # 订单列表（tab）
    ├── order-detail/          # 订单详情 + 取消订单
    ├── profile/               # 我的（tab）
    └── profile-edit/          # 编辑资料
```

每个页面目录下都有 4 个同名文件，职责固定：

| 文件 | 职责 |
| --- | --- |
| `xxx.js` | 页面逻辑：生命周期、事件处理、调用接口 |
| `xxx.wxml` | 页面结构：用数据渲染界面、绑定事件 |
| `xxx.wxss` | 页面样式 |
| `xxx.json` | 页面配置（本项目只用来设置导航栏标题） |

---

## 三、全局文件详解

### `app.js` —— 小程序入口

- `globalData.baseUrl`：后端接口地址，默认 `http://127.0.0.1:8000/api`。
- `globalData.user`：当前登录用户，未登录为 `null`。
- `onLaunch()`：启动时从本地缓存 `user` 恢复登录状态。
- `setUser(user)`：登录/注册/改资料成功后调用，保存到内存 + 本地缓存。
- `clearUser()`：退出登录或登录失效时调用，清空内存 + 本地缓存。

```js
App({
  globalData: {
    baseUrl: 'http://127.0.0.1:8000/api',
    user: null
  },
  onLaunch() {
    this.globalData.user = wx.getStorageSync('user') || null
  },
  setUser(user) { ... },
  clearUser() { ... }
})
```

### `app.json` —— 页面注册与 tabBar

- `pages`：注册全部 7 个页面，**第一项 `pages/login/login` 是启动页**。
- `tabBar`：底部 4 个 tab，对应 4 个页面：

| 序号(index) | 页面 | 文字 |
| --- | --- | --- |
| 0 | `pages/index/index` | 点餐 |
| 1 | `pages/cart/cart` | 购物车 |
| 2 | `pages/orders/orders` | 订单 |
| 3 | `pages/profile/profile` | 我的 |

> `cart.js` 里的 `updateBadge()` 会把购物车数量显示在 **index = 1（购物车）** 的角标上。

### `utils/api.js` —— 接口封装（核心）

**所有**网络请求都在这里发，页面只调用这里的方法。核心是 `request(method, url, data)`：

```js
function request(method, url, data) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: getBaseUrl() + url,           // 拼接 baseUrl + 路径
      method: method,
      data: data || {},                  // GET 时作为 query，POST/PUT 时作为 JSON body
      header: { 'content-type': 'application/json' },
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)              // 2xx 成功，返回后端数据
        } else {
          reject(handleError(res.statusCode, res.data))  // 非 2xx，转成 Error
        }
      },
      fail() {
        reject(new Error('网络请求失败，请检查后端服务是否启动'))
      }
    })
  })
}
```

要点：

- 返回 **Promise**，页面里用 `.then(...).catch(...)` 处理。
- 请求头固定 `content-type: application/json`。
- GET 参数通过 `data` 传入，`wx.request` 会自动拼成 URL 查询串；
  POST/PUT 的 `data` 会自动序列化成 JSON 请求体。
- 统一错误处理 `handleError`：

| 状态码 | 处理方式 |
| --- | --- |
| 401 | 清空本地用户，延迟后 `reLaunch` 到登录页（登录失效） |
| 403 | 提示“没有操作权限” |
| 404 | 提示“请求的资源不存在” |
| >= 500 | 提示“服务器开小差了，请稍后重试” |
| 其他 | 使用后端返回的 `detail` 作为错误信息 |

`pickDetail(data)` 负责从后端错误体 `{ "detail": ... }` 中取出提示文字，
`detail` 既可能是字符串，也可能是 FastAPI 校验失败的数组（422），两种都能处理。

对外暴露的方法（页面实际调用的就是这些）：

| 方法 | HTTP | 路径 | 说明 |
| --- | --- | --- | --- |
| `register(data)` | POST | `/auth/register` | 注册 |
| `login(data)` | POST | `/auth/login` | 登录 |
| `getDishes(category, keyword)` | GET | `/dishes` | 菜品列表（可按分类/关键字） |
| `getCategories()` | GET | `/categories` | 菜品分类列表 |
| `createOrder(data)` | POST | `/orders` | 提交订单 |
| `getOrders(userId)` | GET | `/orders?user_id=` | 某用户的订单列表 |
| `getOrder(id)` | GET | `/orders/{id}` | 订单详情 |
| `cancelOrder(id)` | POST | `/orders/{id}/cancel` | 取消订单 |
| `getUser(id)` | GET | `/users/{id}` | 用户信息 |
| `updateUser(id, data)` | PUT | `/users/{id}` | 更新用户资料 |

> 路径都是相对 `baseUrl` 的，所以实际请求地址是
> `http://127.0.0.1:8000/api` + 上表路径。

### `utils/cart.js` —— 购物车状态

购物车**只存在前端本地缓存**（key 为 `cart`），提交订单前不落库。

| 方法 | 作用 |
| --- | --- |
| `getCart()` | 读取购物车数组 |
| `addToCart(dish, quantity)` | 加入购物车，已存在则累加数量 |
| `updateQuantity(dishId, quantity)` | 修改数量，`<= 0` 时移除 |
| `removeFromCart(dishId)` | 删除某个菜品 |
| `clearCart()` | 清空 |
| `getCount(cart)` | 商品总件数 |
| `getTotal(cart)` | 总金额 |
| `updateBadge(cart)` | 更新购物车 tab 角标（index = 1） |

购物车每一项的结构：

```json
{ "dish_id": 1, "name": "宫保鸡丁", "price": 28, "quantity": 2 }
```

### `utils/util.js` —— 格式化工具

- `formatTime(value)`：把 `2026-09-13T12:30:00` 格式化成 `2026-09-13 12:30`。
- `formatPrice(value)`：把 `28` 格式化成 `28.00`。

---

## 四、页面详解

下面按“页面路径 → 页面做什么 → 调了什么接口 → 关键流程”逐一说明。

---

### 1. `pages/login/login` —— 登录 / 注册

- 文件：`login.js` / `login.wxml` / `login.wxss` / `login.json`（标题“登录”）
- 定位：小程序**启动页**，同一个页面通过 `mode` 在“登录”和“注册”之间切换。

页面数据：`mode`、`username`、`password`、`nickname`、`phone`、`submitting`。

关键逻辑：

| 函数 | 说明 |
| --- | --- |
| `onLoad()` | 如果 `globalData.user` 已存在，直接 `switchTab` 到点餐页 |
| `onSwitchMode(e)` | 切换登录/注册模式（`data-mode`） |
| `onInput(e)` | 通用输入处理，用 `data-field` 决定更新哪个字段 |
| `onSubmit()` | 校验后发起请求 |

调用的接口：

| 模式 | 接口 | 请求体 |
| --- | --- | --- |
| 登录 | `POST /api/auth/login` | `{ username, password }` |
| 注册 | `POST /api/auth/register` | `{ username, password, nickname, phone }` |

请求发送流程（以登录为例）：

```
用户点击“登录”
  → onSubmitting 校验：用户名/密码非空；注册时密码 ≥ 6 位
  → api.login({ username, password })        // utils/api.js → wx.request POST /api/auth/login
  → .then(user)  getApp().setUser(user)      // 保存登录状态
  → 弹出“登录成功” → 600ms 后 wx.switchTab 到 pages/index/index
  → .catch(err)  wx.showToast(err.message)   // 展示后端错误（如“用户名或密码错误”）
```

> 演示账号：`demo / 123456`。

---

### 2. `pages/index/index` —— 点餐（tab 首页）

- 文件：`index.js` / `index.wxml` / `index.wxss` / `index.json`（标题“点餐”）
- 定位：搜索 + 分类筛选 + 菜品列表 + 加入购物车。

页面数据：`categories`（分类）、`activeCategory`（当前分类）、`keyword`（搜索词）、`dishes`（菜品列表）、`loading`。

调用的接口：

| 时机 | 接口 | 参数 | 说明 |
| --- | --- | --- | --- |
| `onLoad` | `GET /api/categories` | 无 | 加载分类栏 |
| `onLoad` | `GET /api/dishes` | `category`、`keyword` | 加载菜品列表 |
| 切换分类 | `GET /api/dishes` | `category` | 重新查询 |
| 搜索 | `GET /api/dishes` | `keyword` | 重新查询 |

关键逻辑：

| 函数 | 说明 |
| --- | --- |
| `onLoad()` | 同时加载分类和菜品 |
| `onShow()` | 回到页面时刷新购物车角标 `cart.updateBadge()` |
| `loadCategories()` | 拉分类；失败静默忽略 |
| `loadDishes()` | 拉菜品，并给每条数据补充 `initial`（名称首字，当占位图）和 `priceText`（价格字符串） |
| `onSelectCategory(e)` | 记录所选分类并重新 `loadDishes()` |
| `onKeywordInput(e)` / `onSearch()` | 收集搜索词并重新 `loadDishes()` |
| `onAddToCart(e)` | **纯本地操作**，`cart.addToCart(dish)`，不调用后端 |

请求发送流程：

```
onLoad
  → api.getCategories()  → GET /api/categories  → setData({ categories })
  → api.getDishes('', '') → GET /api/dishes        → 处理后 setData({ dishes, loading:false })

点击某个分类
  → setData({ activeCategory: '热菜' })
  → api.getDishes('热菜', keyword) → GET /api/dishes?category=热菜&keyword=...

点击菜品“+”
  → cart.addToCart(dish)   // 写入本地缓存，同时更新 tab 角标
  → 提示“已加入购物车”
```

> 加入购物车**不会**请求后端，所以即使后端没启动，也能先把菜加进购物车。

---

### 3. `pages/cart/cart` —— 购物车（tab）

- 文件：`cart.js` / `cart.wxml` / `cart.wxss` / `cart.json`（标题“购物车”）
- 定位：修改数量、删除、填备注、提交订单。

页面数据：`items`、`totalText`、`count`、`remark`、`submitting`。

调用的接口：

| 时机 | 接口 | 请求体 |
| --- | --- | --- |
| 点击“提交订单” | `POST /api/orders` | 见下 |

关键逻辑：

| 函数 | 说明 |
| --- | --- |
| `onShow()` | 每次显示都 `refresh()`，从本地缓存重新渲染 |
| `refresh()` | 读取购物车，计算小计/合计/件数，更新角标 |
| `onPlus(e)` / `onMinus(e)` | 数量 +1 / -1，**本地操作** |
| `onRemove(e)` | 删除单项，**本地操作** |
| `onRemarkInput(e)` | 收集备注 |
| `onClear()` | 弹窗确认后清空购物车，**本地操作** |
| `onSubmit()` | 组装请求体并下单 |

下单请求体：

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

提交流程：

```
点击“提交订单”
  → 校验：购物车非空；未登录则 reLaunch 到登录页
  → setData({ submitting: true })                // 防重复提交
  → 组装 payload：{ user_id, remark, items:[{dish_id, quantity}] }
  → api.createOrder(payload) → POST /api/orders
  → .then()  cart.clearCart()                    // 下单成功清空本地购物车
             setData({ submitting:false, remark:'' })
             提示“下单成功” → 800ms 后 switchTab 到点餐页
  → .catch(err) 提示错误，setData({ submitting:false })
```

> 后端的订单明细会保存**菜品名称和单价快照**，所以历史订单金额不会随菜品改价而变化。

---

### 4. `pages/orders/orders` —— 订单列表（tab）

- 文件：`orders.js` / `orders.wxml` / `orders.wxss` / `orders.json`（标题“我的订单”）
- 定位：展示当前用户的订单，点击进入详情。

页面数据：`orders`、`loading`。

调用的接口：

| 时机 | 接口 | 参数 |
| --- | --- | --- |
| `onShow` | `GET /api/orders` | `user_id` |

关键逻辑：

| 函数 | 说明 |
| --- | --- |
| `onShow()` | 未登录则 `reLaunch` 到登录页；已登录则 `loadOrders(user.id)` |
| `loadOrders(userId)` | 拉订单，补充 `totalText`、`timeText`、`count`（件数） |
| `onTapOrder(e)` | `navigateTo` 到订单详情，URL 带 `id` |

请求发送流程：

```
onShow
  → 从 globalData 取 user，没有 → reLaunch /pages/login/login
  → api.getOrders(user.id) → GET /api/orders?user_id=1
  → 列表每条 order 处理：
       totalText = formatPrice(total_amount)
       timeText  = formatTime(created_at)
       count     = sum(items[].quantity)
  → setData({ orders })

点击某订单
  → wx.navigateTo({ url: '/pages/order-detail/order-detail?id=' + id })
```

---

### 5. `pages/order-detail/order-detail` —— 订单详情

- 文件：`order-detail.js` / `order-detail.wxml` / `order-detail.wxss` / `order-detail.json`（标题“订单详情”）
- 定位：查看订单明细、订单信息，可取消“已提交”状态的订单。

页面数据：`order`、`loading`；另外用实例属性 `this.orderId` 保存订单 ID。

调用的接口：

| 时机 | 接口 | 参数 |
| --- | --- | --- |
| `onShow` | `GET /api/orders/{id}` | 路径参数 `id` |
| 点击“取消订单” | `POST /api/orders/{id}/cancel` | 路径参数 `id` |

关键逻辑：

| 函数 | 说明 |
| --- | --- |
| `onLoad(options)` | 从 `options.id` 拿到订单 ID，存到 `this.orderId` |
| `onShow()` | 每次显示都重新 `loadOrder()`，保证取消后状态最新 |
| `loadOrder()` | 拉详情，给明细补 `priceText`、`subtotalText`，给订单补 `totalText`、`timeText` |
| `onCancel()` | 弹窗确认后调用取消接口，成功后重新加载详情 |

取消流程：

```
点击“取消订单”（仅 status === '已提交' 时按钮才显示）
  → wx.showModal 确认
  → api.cancelOrder(this.orderId) → POST /api/orders/{id}/cancel
  → .then() 提示“订单已取消” → this.loadOrder() 刷新
  → .catch(err) 提示错误
```

---

### 6. `pages/profile/profile` —— 我的（tab）

- 文件：`profile.js` / `profile.wxml` / `profile.wxss` / `profile.json`（标题“我的”）
- 定位：展示用户信息与订单统计，提供编辑资料、清空购物车缓存、退出登录。

页面数据：`user`、`stats`（`total` 订单数 / `amount` 累计消费 / `active` 进行中）。

调用的接口：

| 时机 | 接口 | 参数 | 说明 |
| --- | --- | --- | --- |
| `onShow` | `GET /api/orders` | `user_id` | 统计订单数、累计消费、进行中数量 |
| `onShow` | `GET /api/users/{id}` | 路径 `id` | 拉最新资料并刷新本地缓存 |

关键逻辑：

| 函数 | 说明 |
| --- | --- |
| `onShow()` | 未登录 `reLaunch` 登录页；否则先渲染本地用户 → `loadStats()` → 再拉最新资料 |
| `renderUser(user)` | 补充 `initial`（昵称首字做头像） |
| `loadStats(userId)` | 拉订单列表后在**前端**统计：总数、非“已取消”金额合计、`已提交` 数量 |
| `onEdit()` | `navigateTo` 编辑资料页 |
| `onLogout()` | 确认后 `clearUser()` 并 `reLaunch` 登录页 |
| `onClearCache()` | 确认后 `wx.removeStorageSync('cart')` |

请求发送流程：

```
onShow
  → 取 globalData.user，没有 → reLaunch /pages/login/login
  → renderUser(user)                       // 先显示缓存里的资料
  → api.getOrders(user.id) → GET /api/orders?user_id=1
       → 前端统计 setData({ stats })
  → api.getUser(user.id)   → GET /api/users/1
       → app.setUser(fresh) + renderUser(fresh)   // 与后端保持一致
```

---

### 7. `pages/profile-edit/profile-edit` —— 编辑资料

- 文件：`profile-edit.js` / `profile-edit.wxml` / `profile-edit.wxss` / `profile-edit.json`（标题“编辑资料”）
- 定位：修改昵称和手机号。

页面数据：`nickname`、`phone`、`saving`；实例属性 `this.userId`。

调用的接口：

| 时机 | 接口 | 请求体 |
| --- | --- | --- |
| 点击“保存” | `PUT /api/users/{id}` | `{ nickname, phone }` |

关键逻辑：

| 函数 | 说明 |
| --- | --- |
| `onLoad()` | 未登录 `reLaunch` 登录页；否则用当前用户资料回填表单 |
| `onNicknameInput` / `onPhoneInput` | 收集输入 |
| `onSave()` | 校验昵称非空后提交，防重复提交 |

保存流程：

```
点击“保存”
  → 校验昵称非空；saving 防重复
  → api.updateUser(this.userId, { nickname, phone }) → PUT /api/users/1
  → .then(user)  getApp().setUser(user)     // 更新本地登录信息
                 提示“保存成功” → 600ms 后 navigateBack 返回“我的”
  → .catch(err)  提示错误
```

---

## 五、接口调用汇总（按页面）

| 页面 | 接口 | 方法 | 用途 |
| --- | --- | --- | --- |
| login | `/api/auth/login` | POST | 登录 |
| login | `/api/auth/register` | POST | 注册 |
| index | `/api/categories` | GET | 分类栏 |
| index | `/api/dishes` | GET | 菜品列表（分类/搜索） |
| cart | `/api/orders` | POST | 提交订单 |
| orders | `/api/orders?user_id=` | GET | 订单列表 |
| order-detail | `/api/orders/{id}` | GET | 订单详情 |
| order-detail | `/api/orders/{id}/cancel` | POST | 取消订单 |
| profile | `/api/orders?user_id=` | GET | 订单统计 |
| profile | `/api/users/{id}` | GET | 拉最新资料 |
| profile-edit | `/api/users/{id}` | PUT | 更新资料 |

**不请求后端的功能（纯前端本地缓存）**：加入购物车、改数量、删除、清空购物车、填写备注、退出登录。

---

## 六、一次完整点餐流程（前后端串联）

```
① 登录页 pages/login/login
   用户输入账号 → api.login → POST /api/auth/login
   后端校验成功返回用户对象 → app.setUser(user) 存本地 → 跳到点餐页

② 点餐页 pages/index/index
   onLoad → GET /api/categories + GET /api/dishes 渲染菜品
   点击“+” → cart.addToCart(dish) 写入本地缓存（更新购物车 tab 角标）

③ 购物车页 pages/cart/cart
   onShow 从本地缓存渲染
   改数量 / 删除 / 填备注（全部本地）
   点击“提交订单” → api.createOrder → POST /api/orders
       请求体 { user_id, remark, items:[{dish_id, quantity}] }
   后端写 MySQL 并返回订单 → 前端 cart.clearCart() → 跳回点餐页

④ 订单列表 pages/orders/orders
   onShow → GET /api/orders?user_id=<当前用户> 展示订单

⑤ 订单详情 pages/order-detail/order-detail
   GET /api/orders/{id} 查看明细；已提交订单可 POST /api/orders/{id}/cancel 取消

⑥ 我的 pages/profile/profile
   GET /api/orders?user_id= 统计订单；GET /api/users/{id} 刷新资料；
   编辑资料页 PUT /api/users/{id} 保存修改
```

---

## 七、如何运行与调试

1. 先启动后端（`backend` 目录，`uvicorn app.main:app --reload`），确保
   `http://127.0.0.1:8000` 可访问。
2. 用**微信开发者工具**打开 `frontend` 目录。
3. 在 `project.config.json` 中把 `appid` 改成自己的 AppID（或使用测试号）。
4. 编译运行，进入登录页，用 `demo / 123456` 登录或自行注册。
5. 真机预览时，把 `app.js` 里的 `baseUrl` 改成电脑局域网 IP，
   例如 `http://192.168.1.10:8000/api`，并保证手机与电脑同一网络。

前端自检（校验 JSON / JS 语法，需要 bun）：

```bash
cd frontend
bun install
bun run check
```

> 小程序为原生开发，不经过打包工具；bun 只用于管理类型提示依赖和运行 `scripts/check.js` 自检。
> 开发者工具默认关闭域名校验（`urlCheck: false`），可直接请求本地 HTTP 接口。

---

## 八、常见疑问（答辩速查）

- **请求在哪里发？** 全部在 `utils/api.js`，页面只调用封装好的方法。
- **怎么带用户身份？** 登录后把用户存本地，请求时显式传 `user_id`，没有 token。
- **购物车存哪？** 本地缓存 `cart`，提交订单前不落库。
- **页面之间怎么跳转？** tab 页用 `wx.switchTab`，详情/编辑页用 `wx.navigateTo`，
  登录失效用 `wx.reLaunch` 回到登录页。
- **接口报错怎么提示？** `utils/api.js` 的 `handleError` 按状态码统一处理，
  页面 `.catch(err)` 里 `wx.showToast(err.message)` 展示。
