// 简单工具函数

// 格式化时间：2026-09-13T12:30:00 -> 2026-09-13 12:30
function formatTime(value) {
  if (!value) {
    return ''
  }
  const text = String(value)
    .replace('T', ' ')
    .replace(/\.\d+/, '')
    .replace('Z', '')
  const date = new Date(text.replace(/-/g, '/'))
  if (isNaN(date.getTime())) {
    return value
  }
  const pad = (n) => (n < 10 ? '0' + n : '' + n)
  return (
    date.getFullYear() +
    '-' +
    pad(date.getMonth() + 1) +
    '-' +
    pad(date.getDate()) +
    ' ' +
    pad(date.getHours()) +
    ':' +
    pad(date.getMinutes())
  )
}

// 格式化金额：28 -> 28.00
function formatPrice(value) {
  const num = Number(value)
  return isNaN(num) ? '0.00' : num.toFixed(2)
}

module.exports = {
  formatTime,
  formatPrice
}
