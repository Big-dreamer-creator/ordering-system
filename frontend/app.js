// 小程序入口
App({
  globalData: {
    // 后端接口地址。真机调试时请改为电脑局域网 IP，例如 http://192.168.1.10:8000/api
    baseUrl: 'http://127.0.0.1:8000/api',
    // 当前登录用户，未登录为 null
    user: null
  },

  onLaunch() {
    this.globalData.user = wx.getStorageSync('user') || null
  },

  // 登录/注册成功后保存用户
  setUser(user) {
    this.globalData.user = user
    wx.setStorageSync('user', user)
  },

  // 退出登录
  clearUser() {
    this.globalData.user = null
    wx.removeStorageSync('user')
  }
})
