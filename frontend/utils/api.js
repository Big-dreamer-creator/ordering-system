// 后端接口封装
function getBaseUrl() {
  const app = getApp()
  return (app && app.globalData && app.globalData.baseUrl) || 'http://127.0.0.1:8000/api'
}

// 从后端返回体里取出错误信息（detail 可能是字符串或数组）
function pickDetail(data) {
  if (!data || !data.detail) {
    return ''
  }
  const detail = data.detail
  if (typeof detail === 'string') {
    return detail
  }
  if (Array.isArray(detail)) {
    return detail
      .map((item) => item && item.msg)
      .filter(Boolean)
      .join('；')
  }
  return ''
}

// 按状态码做不同处理
function handleError(statusCode, data) {
  const detail = pickDetail(data)

  if (statusCode === 401) {
    const app = getApp()
    if (app) {
      app.clearUser()
    }
    setTimeout(() => {
      wx.reLaunch({ url: '/pages/login/login' })
    }, 800)
    return new Error(detail || '登录已失效，请重新登录')
  }

  if (statusCode === 403) {
    return new Error(detail || '没有操作权限')
  }

  if (statusCode === 404) {
    return new Error(detail || '请求的资源不存在')
  }

  if (statusCode >= 500) {
    return new Error('服务器开小差了，请稍后重试')
  }

  return new Error(detail || '请求失败')
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
          reject(handleError(res.statusCode, res.data))
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
