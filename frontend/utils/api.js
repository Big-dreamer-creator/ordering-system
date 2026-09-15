// 后端接口封装
function getBaseUrl() {
  const app = getApp()
  return (app && app.globalData && app.globalData.baseUrl) || 'http://127.0.0.1:8000/api'
}

function request(method, url, data) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: getBaseUrl() + url,
      method: method,
      data: data || {},
      header: { 'content-type': 'application/json' },
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          const detail = res.data && res.data.detail
          reject(new Error(typeof detail === 'string' ? detail : '请求失败'))
        }
      },
      fail() {
        reject(new Error('网络请求失败，请检查后端服务是否启动'))
      }
    })
  })
}

module.exports = {
  // 认证
  register(data) {
    return request('POST', '/auth/register', data)
  },
  login(data) {
    return request('POST', '/auth/login', data)
  },

  // 菜品
  getDishes(category, keyword) {
    const params = {}
    if (category) {
      params.category = category
    }
    if (keyword) {
      params.keyword = keyword
    }
    return request('GET', '/dishes', params)
  },
  getCategories() {
    return request('GET', '/categories')
  },

  // 订单
  createOrder(data) {
    return request('POST', '/orders', data)
  },
  getOrders(userId) {
    return request('GET', '/orders', { user_id: userId })
  },
  getOrder(id) {
    return request('GET', '/orders/' + id)
  },
  cancelOrder(id) {
    return request('POST', '/orders/' + id + '/cancel')
  },

  // 用户
  getUser(id) {
    return request('GET', '/users/' + id)
  },
  updateUser(id, data) {
    return request('PUT', '/users/' + id, data)
  }
}
