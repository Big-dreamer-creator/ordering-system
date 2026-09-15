const api = require('../../utils/api')
const util = require('../../utils/util')

Page({
  data: {
    user: null,
    stats: {
      total: 0,
      amount: '0.00',
      active: 0
    }
  },

  onShow() {
    const app = getApp()
    const user = app.globalData.user
    if (!user) {
      wx.reLaunch({ url: '/pages/login/login' })
      return
    }

    this.renderUser(user)
    this.loadStats(user.id)

    // 拉取最新资料，保持与后端一致
    api
      .getUser(user.id)
      .then((fresh) => {
        app.setUser(fresh)
        this.renderUser(fresh)
      })
      .catch(() => {})
  },

  renderUser(user) {
    this.setData({
      user: {
        ...user,
        initial: user.nickname ? user.nickname.charAt(0) : ''
      }
    })
  },

  loadStats(userId) {
    api
      .getOrders(userId)
      .then((orders) => {
        const total = orders.length
        const amount = orders
          .filter((order) => order.status !== '已取消')
          .reduce((sum, order) => sum + Number(order.total_amount), 0)
        const active = orders.filter((order) => order.status === '已提交').length
        this.setData({
          stats: {
            total: total,
            amount: util.formatPrice(amount),
            active: active
          }
        })
      })
      .catch(() => {})
  },

  onEdit() {
    wx.navigateTo({ url: '/pages/profile-edit/profile-edit' })
  },

  onLogout() {
    wx.showModal({
      title: '提示',
      content: '确定退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          getApp().clearUser()
          wx.reLaunch({ url: '/pages/login/login' })
        }
      }
    })
  },

  onClearCache() {
    wx.showModal({
      title: '提示',
      content: '确定清空本地购物车缓存吗？',
      success: (res) => {
        if (res.confirm) {
          wx.removeStorageSync('cart')
          wx.showToast({ title: '已清空', icon: 'success' })
        }
      }
    })
  }
})
