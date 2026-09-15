// 购物车状态管理（保存在本地缓存，未提交订单前只存在前端）
const CART_KEY = 'cart'

function getCart() {
  return wx.getStorageSync(CART_KEY) || []
}

function setCart(cart) {
  wx.setStorageSync(CART_KEY, cart)
  updateBadge(cart)
}

// 加入购物车，已存在则累加数量
function addToCart(dish, quantity) {
  const count = quantity || 1
  const cart = getCart()
  const item = cart.find((i) => i.dish_id === dish.id)
  if (item) {
    item.quantity += count
  } else {
    cart.push({
      dish_id: dish.id,
      name: dish.name,
      price: Number(dish.price),
      quantity: count
    })
  }
  setCart(cart)
  return cart
}

// 修改数量，数量 <= 0 时移除
function updateQuantity(dishId, quantity) {
  let cart = getCart()
  if (quantity <= 0) {
    cart = cart.filter((i) => i.dish_id !== dishId)
  } else {
    const item = cart.find((i) => i.dish_id === dishId)
    if (item) {
      item.quantity = quantity
    }
  }
  setCart(cart)
  return cart
}

function removeFromCart(dishId) {
  return updateQuantity(dishId, 0)
}

function clearCart() {
  setCart([])
}

function getCount(cart) {
  const list = cart || getCart()
  return list.reduce((sum, i) => sum + i.quantity, 0)
}

function getTotal(cart) {
  const list = cart || getCart()
  const total = list.reduce((sum, i) => sum + Number(i.price) * i.quantity, 0)
  return total
}

// 更新购物车 tab 上的角标
function updateBadge(cart) {
  const count = getCount(cart)
  if (count > 0) {
    wx.setTabBarBadge({ index: 1, text: String(count), fail() {} })
  } else {
    wx.removeTabBarBadge({ index: 1, fail() {} })
  }
}

module.exports = {
  getCart,
  addToCart,
  updateQuantity,
  removeFromCart,
  clearCart,
  getCount,
  getTotal,
  updateBadge
}
