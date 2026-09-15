const api = require('../../utils/api')
const cart = require('../../utils/cart')

Page({
  data: {
    categories: [],
    activeCategory: '',
    keyword: '',
    dishes: [],
    loading: true
  },

  onLoad() {
    this.loadCategories()
    this.loadDishes()
  },

  onShow() {
    cart.updateBadge()
  },

  loadCategories() {
    api
      .getCategories()
      .then((categories) => {
        this.setData({ categories: categories })
      })
      .catch(() => {})
  },

  loadDishes() {
    this.setData({ loading: true })
    api
      .getDishes(this.data.activeCategory, this.data.keyword)
      .then((dishes) => {
        const list = dishes.map((dish) => ({
          ...dish,
          initial: dish.name.charAt(0),
          priceText: Number(dish.price).toFixed(2)
        }))
        this.setData({ dishes: list, loading: false })
      })
      .catch((err) => {
        this.setData({ loading: false })
        wx.showToast({ title: err.message, icon: 'none' })
      })
  },

  onSelectCategory(e) {
    this.setData({ activeCategory: e.currentTarget.dataset.category })
    this.loadDishes()
  },

  onKeywordInput(e) {
    this.setData({ keyword: e.detail.value })
  },

  onSearch() {
    this.loadDishes()
  },

  onAddToCart(e) {
    cart.addToCart(e.currentTarget.dataset.dish)
    wx.showToast({ title: '已加入购物车', icon: 'success' })
  }
})
