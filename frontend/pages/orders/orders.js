const api = require('../../utils/api')
const util = require('../../utils/util')

Page({
  data: {
    orders: [],
    loading: true
  },

  onShow() {
    const app = getApp()
    const user = app.globalData.user
    if (!user) {
      wx.reLaunch({ url: '/pages/login/login' })
      return
    }
    this.loadOrders(user.id)
  },

  loadOrders(userId) {
    this.setData({ loading: true })
    api
      .getOrders(userId)
      .then((orders) => {
        const list = orders.map((order) => ({
          ...order,
          totalText: util.formatPrice(order.total_amount),
          timeText: util.formatTime(order.created_at),
          count: order.items.reduce((sum, item) => sum + item.quantity, 0)
        }))
        this.setData({ orders: list, loading: false })
      })
      .catch((err) => {
        this.setData({ loading: false })
        wx.showToast({ title: err.message, icon: 'none' })
      })
  },

  onTapOrder(e) {
    wx.navigateTo({
      url: '/pages/order-detail/order-detail?id=' + e.currentTarget.dataset.id
    })
  }
})
