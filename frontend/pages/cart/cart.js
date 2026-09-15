const api = require('../../utils/api')
const cart = require('../../utils/cart')
const util = require('../../utils/util')

Page({
  data: {
    items: [],
    totalText: '0.00',
    count: 0,
    remark: '',
    submitting: false
  },

  onShow() {
    this.refresh()
  },

  refresh() {
    const items = cart.getCart().map((item) => ({
      ...item,
      priceText: util.formatPrice(item.price),
      subtotalText: (Number(item.price) * item.quantity).toFixed(2)
    }))
    this.setData({
      items: items,
      totalText: util.formatPrice(cart.getTotal()),
      count: cart.getCount()
    })
    cart.updateBadge()
  },

  onPlus(e) {
    const dishId = e.currentTarget.dataset.id
    const item = this.data.items.find((i) => i.dish_id === dishId)
    cart.updateQuantity(dishId, item.quantity + 1)
    this.refresh()
  },

  onMinus(e) {
    const dishId = e.currentTarget.dataset.id
    const item = this.data.items.find((i) => i.dish_id === dishId)
    cart.updateQuantity(dishId, item.quantity - 1)
    this.refresh()
  },

  onRemove(e) {
    cart.removeFromCart(e.currentTarget.dataset.id)
    this.refresh()
  },

  onRemarkInput(e) {
    this.setData({ remark: e.detail.value })
  },

  onClear() {
    wx.showModal({
      title: '提示',
      content: '确定清空购物车吗？',
      success: (res) => {
        if (res.confirm) {
          cart.clearCart()
          this.refresh()
        }
      }
    })
  },

  onSubmit() {
    if (this.data.items.length === 0) {
      wx.showToast({ title: '购物车是空的', icon: 'none' })
      return
    }
    const user = getApp().globalData.user
    if (!user) {
      wx.reLaunch({ url: '/pages/login/login' })
      return
    }
    if (this.data.submitting) {
      return
    }
    this.setData({ submitting: true })

    const payload = {
      user_id: user.id,
      remark: this.data.remark,
      items: this.data.items.map((item) => ({
        dish_id: item.dish_id,
        quantity: item.quantity
      }))
    }

    api
      .createOrder(payload)
      .then(() => {
        cart.clearCart()
        this.setData({ submitting: false, remark: '' })
        wx.showToast({ title: '下单成功', icon: 'success' })
        setTimeout(() => {
          wx.switchTab({ url: '/pages/index/index' })
        }, 800)
      })
      .catch((err) => {
        this.setData({ submitting: false })
        wx.showToast({ title: err.message, icon: 'none' })
      })
  }
})
