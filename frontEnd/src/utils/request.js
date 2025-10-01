/**
 * API请求通用函数
 * 统一处理请求和响应，包括错误处理
 */

import { API_BASE_URL, USE_MOCK } from './env'
import { getToken } from './storage'
import { 
  mockLogin, 
  mockGetKnowledgeBaseStats, 
  mockGetKnowledgeBaseList,
  mockGetChatKnowledgeBaseList,
  mockGetModelList,
  mockGetSessionHistory,
  mockCreateSession,
  mockSendChatMessage,
  mockSearchDocuments,
  mockGetHotKeywords,
  mockGetDocTypes,
  mockExportSearchResults
} from '../api/mock'

/**
 * 通用API请求函数
 * @param {string} url - 接口地址
 * @param {object} options - 请求配置
 * @param {string} options.method - 请求方法，默认POST
 * @param {object} options.body - 请求体
 * @param {object} options.headers - 请求头
 * @param {boolean} options.needAuth - 是否需要token，默认false
 * @returns {Promise<object>} 返回响应数据
 */
export async function apiRequest(url, options = {}) {
  const {
    method = 'POST',
    body = {},
    headers = {},
    needAuth = false
  } = options

  // 开发环境使用模拟数据
  if (USE_MOCK) {
    return getMockData(url, body)
  }

  // 构建请求配置
  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers
    }
  }

  // 添加认证token
  if (needAuth) {
    const token = getToken()
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
  }

  // 添加请求体
  if (method !== 'GET' && Object.keys(body).length > 0) {
    config.body = JSON.stringify(body)
  }

  try {
    const response = await fetch(`${API_BASE_URL}${url}`, config)
    const data = await response.json()

    // 统一处理响应
    return handleResponse(data)
  } catch (error) {
    console.error('API请求失败:', error)
    throw new Error('网络请求失败，请检查网络连接')
  }
}

/**
 * 统一处理API响应
 * @param {object} data - 响应数据
 * @returns {object} 处理后的数据
 */
function handleResponse(data) {
  const { error, message, body } = data

  if (error === 0) {
    // 请求成功
    return { success: true, data: body, message }
  } else if (error === 401) {
    // 需要登录
    console.warn('未登录或登录已过期')
    // 可以在这里跳转到登录页
    window.location.href = '/login'
    throw new Error('请先登录')
  } else if (error === 403) {
    // 权限不足
    throw new Error('权限不足，无法访问')
  } else if (error === 500) {
    // 系统异常
    throw new Error('系统异常，请稍后重试')
  } else {
    // 业务异常
    throw new Error(message || '操作失败')
  }
}

/**
 * 获取模拟数据
 * @param {string} url - 接口地址
 * @param {object} body - 请求参数
 * @returns {Promise<object>} 模拟响应数据
 */
async function getMockData(url, body) {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, 500))

  // 根据URL返回对应的模拟数据
  if (url.includes('/auth/login')) {
    return mockLogin(body)
  } else if (url.includes('/knowledge-base/stats')) {
    return mockGetKnowledgeBaseStats()
  } else if (url.includes('/knowledge-base/list')) {
    return mockGetKnowledgeBaseList()
  } else if (url.includes('/chat/knowledge-bases')) {
    return mockGetChatKnowledgeBaseList()
  } else if (url.includes('/chat/models')) {
    return mockGetModelList()
  } else if (url.includes('/chat/sessions')) {
    return mockGetSessionHistory()
  } else if (url.includes('/chat/session/create')) {
    return mockCreateSession(body)
  } else if (url.includes('/chat/message/send')) {
    return mockSendChatMessage(body)
  } else if (url.includes('/search/documents')) {
    return mockSearchDocuments(body)
  } else if (url.includes('/search/hot-keywords')) {
    return mockGetHotKeywords()
  } else if (url.includes('/search/doc-types')) {
    return mockGetDocTypes()
  } else if (url.includes('/search/export')) {
    return mockExportSearchResults(body)
  }

  // 默认返回成功
  return {
    success: true,
    data: {},
    message: '操作成功'
  }
}

