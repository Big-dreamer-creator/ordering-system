const api = require('../../utils/api')

Page({
  data: {
    mode: 'login',
    username: '',
    password: '',
    nickname: '',
    phone: '',
    submitting: false
  },

  onLoad() {
    if (getApp().globalData.user) {
      wx.switchTab({ url: '/pages/index/index' })
    }
  },

  onSwitchMode(e) {
    this.setData({ mode: e.currentTarget.dataset.mode })
  },

  onInput(e) {
    this.setData({ [e.currentTarget.dataset.field]: e.detail.value })
  },

  onSubmit() {
    const mode = this.data.mode
    const username = this.data.username.trim()
    const password = this.data.password

    if (!username || !password) {
      wx.showToast({ title: '请输入用户名和密码', icon: 'none' })
      return
    }
    if (mode === 'register' && password.length < 6) {
      wx.showToast({ title: '密码至少 6 位', icon: 'none' })
      return
    }
    if (this.data.submitting) {
      return
    }
    this.setData({ submitting: true })

    const action =
      mode === 'login'
        ? api.login({ username: username, password: password })
        : api.register({
            username: username,
            password: password,
            nickname: this.data.nickname.trim(),
            phone: this.data.phone.trim()
          })

    action
      .then((user) => {
        getApp().setUser(user)
        this.setData({ submitting: false })
        wx.showToast({
          title: mode === 'login' ? '登录成功' : '注册成功',
          icon: 'success'
        })
        setTimeout(() => {
          wx.switchTab({ url: '/pages/index/index' })
        }, 600)
      })
      .catch((err) => {
        this.setData({ submitting: false })
        wx.showToast({ title: err.message, icon: 'none' })
      })
  }
})
