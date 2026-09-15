const api = require('../../utils/api')

Page({
  data: {
    nickname: '',
    phone: '',
    saving: false
  },

  onLoad() {
    const user = getApp().globalData.user
    if (!user) {
      wx.reLaunch({ url: '/pages/login/login' })
      return
    }
    this.userId = user.id
    this.setData({
      nickname: user.nickname || '',
      phone: user.phone || ''
    })
  },

  onNicknameInput(e) {
    this.setData({ nickname: e.detail.value })
  },

  onPhoneInput(e) {
    this.setData({ phone: e.detail.value })
  },

  onSave() {
    const nickname = this.data.nickname.trim()
    if (!nickname) {
      wx.showToast({ title: '昵称不能为空', icon: 'none' })
      return
    }
    if (this.data.saving) {
      return
    }
    this.setData({ saving: true })

    api
      .updateUser(this.userId, {
        nickname: nickname,
        phone: this.data.phone.trim()
      })
      .then((user) => {
        getApp().setUser(user)
        this.setData({ saving: false })
        wx.showToast({ title: '保存成功', icon: 'success' })
        setTimeout(() => wx.navigateBack(), 600)
      })
      .catch((err) => {
        this.setData({ saving: false })
        wx.showToast({ title: err.message, icon: 'none' })
      })
  }
})
