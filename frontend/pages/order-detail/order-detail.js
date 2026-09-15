const api = require('../../utils/api')
const util = require('../../utils/util')

Page({
  data: {
    order: null,
    loading: true
  },

  onLoad(options) {
    this.orderId = options.id
  },

  onShow() {
    this.loadOrder()
  },

  loadOrder() {
    this.setData({ loading: true })
    api
      .getOrder(this.orderId)
      .then((order) => {
        const items = order.items.map((item) => ({
          ...item,
          priceText: util.formatPrice(item.price),
          subtotalText: util.formatPrice(item.subtotal)
        }))
        this.setData({
          order: {
            ...order,
            items: items,
            totalText: util.formatPrice(order.total_amount),
            timeText: util.formatTime(order.created_at)
          },
          loading: false
        })
      })
      .catch((err) => {
        this.setData({ loading: false })
        wx.showToast({ title: err.message, icon: 'none' })
      })
  },

  onCancel() {
    wx.showModal({
      title: '提示',
      content: '确定取消该订单吗？',
      success: (res) => {
        if (!res.confirm) {
          return
        }
        api
          .cancelOrder(this.orderId)
          .then(() => {
            wx.showToast({ title: '订单已取消', icon: 'success' })
            this.loadOrder()
          })
          .catch((err) => {
            wx.showToast({ title: err.message, icon: 'none' })
          })
      }
    })
  }
})
