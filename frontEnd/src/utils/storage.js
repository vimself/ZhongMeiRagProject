/**
 * 本地存储工具
 * 用于管理localStorage和sessionStorage
 */

const TOKEN_KEY = 'rag_token'
const USER_INFO_KEY = 'rag_user_info'

/**
 * 存储token
 * @param {string} token - 用户token
 * @param {boolean} remember - 是否记住登录
 */
export function setToken(token, remember = false) {
  if (remember) {
    localStorage.setItem(TOKEN_KEY, token)
  } else {
    sessionStorage.setItem(TOKEN_KEY, token)
  }
}

/**
 * 获取token
 * @returns {string|null} token
 */
export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem(TOKEN_KEY)
}

/**
 * 移除token
 */
export function removeToken() {
  localStorage.removeItem(TOKEN_KEY)
  sessionStorage.removeItem(TOKEN_KEY)
}

/**
 * 存储用户信息
 * @param {object} userInfo - 用户信息
 */
export function setUserInfo(userInfo) {
  localStorage.setItem(USER_INFO_KEY, JSON.stringify(userInfo))
}

/**
 * 获取用户信息
 * @returns {object|null} 用户信息
 */
export function getUserInfo() {
  const info = localStorage.getItem(USER_INFO_KEY)
  return info ? JSON.parse(info) : null
}

/**
 * 移除用户信息
 */
export function removeUserInfo() {
  localStorage.removeItem(USER_INFO_KEY)
}

/**
 * 清空所有存储
 */
export function clearAll() {
  removeToken()
  removeUserInfo()
}

