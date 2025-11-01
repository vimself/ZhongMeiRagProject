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
  mockExportSearchResults,
  mockGetUserProfile,
  mockUpdateUserProfile,
  mockUploadUserAvatar,
  mockGetDepartmentList,
  mockGetLoginRecords,
  mockChangeUserPassword,
  mockGetDashboardStats,
  mockGetSystemStatus,
  mockGetUserStats,
  mockGetUserList,
  mockCreateUser,
  mockUpdateUser,
  mockDeleteUser,
  mockToggleUserStatus,
  mockResetUserPassword,
  mockExportUsers,
  mockGetKnowledgeBaseDocuments,
  mockUploadDocument,
  mockDeleteDocument,
  mockGetUploadedFiles,
  mockGetVectorModels,
  mockCreateKnowledgeBaseFull,
  mockUpdateKnowledgeBase,
  mockGetDocumentPreview,
  mockGetModelStats,
  mockGetModelDetail,
  mockCreateModel,
  mockUpdateModel,
  mockDeleteModel,
  mockSetDefaultModel,
  mockTestModel,
  mockHealthCheckModels,
  mockUpdateModelStatus
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

  // 检查是否是FormData（文件上传）
  const isFormData = body instanceof FormData

  // 构建请求头
  const requestHeaders = {}
  
  // FormData 不需要手动设置Content-Type，让浏览器自动设置（包含boundary）
  if (!isFormData) {
    requestHeaders['Content-Type'] = 'application/json'
  }
  
  // 添加认证token
  if (needAuth) {
    const token = getToken()
    if (token) {
      requestHeaders['Authorization'] = `Bearer ${token}`
    }
  }
  
  // 合并自定义headers（但不覆盖已设置的关键header）
  if (headers && Object.keys(headers).length > 0) {
    // 过滤掉空的或undefined的header
    Object.keys(headers).forEach(key => {
      if (headers[key] !== undefined && headers[key] !== null && headers[key] !== '') {
        requestHeaders[key] = headers[key]
      }
    })
  }

  // 构建请求配置
  const config = {
    method,
    headers: requestHeaders
  }

  // 添加请求体
  if (method !== 'GET') {
    if (isFormData) {
      // FormData 直接赋值，不需要JSON.stringify
      config.body = body
    } else if (Object.keys(body).length > 0) {
      config.body = JSON.stringify(body)
    }
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
  } else if (url.includes('/user/profile') && !url.includes('update')) {
    return mockGetUserProfile()
  } else if (url.includes('/user/profile/update')) {
    return mockUpdateUserProfile(body)
  } else if (url.includes('/user/avatar/upload')) {
    return mockUploadUserAvatar(body)
  } else if (url.includes('/user/departments')) {
    return mockGetDepartmentList()
  } else if (url.includes('/user/login-records')) {
    return mockGetLoginRecords(body)
  } else if (url.includes('/user/change-password')) {
    return mockChangeUserPassword(body)
  } else if (url.includes('/dashboard/stats')) {
    return mockGetDashboardStats()
  } else if (url.includes('/dashboard/system-status') || url.includes('/dashboard/refresh-status')) {
    return mockGetSystemStatus()
  } else if (url.includes('/admin/users/stats')) {
    return mockGetUserStats()
  } else if (url.includes('/admin/users/list')) {
    return mockGetUserList(body)
  } else if (url.includes('/admin/users/create')) {
    return mockCreateUser(body)
  } else if (url.includes('/admin/users/update')) {
    return mockUpdateUser(body)
  } else if (url.includes('/admin/users/delete')) {
    return mockDeleteUser(body)
  } else if (url.includes('/admin/users/toggle-status')) {
    return mockToggleUserStatus(body)
  } else if (url.includes('/admin/users/reset-password')) {
    return mockResetUserPassword(body)
  } else if (url.includes('/admin/users/export')) {
    return mockExportUsers(body)
  } else if (url.includes('/knowledge-base/documents')) {
    return mockGetKnowledgeBaseDocuments(body)
  } else if (url.includes('/knowledge-base/upload-document')) {
    return mockUploadDocument(body)
  } else if (url.includes('/knowledge-base/delete-document')) {
    return mockDeleteDocument(body)
  } else if (url.includes('/knowledge-base/uploaded-files')) {
    return mockGetUploadedFiles(body)
  } else if (url.includes('/knowledge-base/vector-models')) {
    return mockGetVectorModels()
  } else if (url.includes('/knowledge-base/create-full')) {
    return mockCreateKnowledgeBaseFull(body)
  } else if (url.includes('/knowledge-base/update')) {
    return mockUpdateKnowledgeBase(body)
  } else if (url.includes('/knowledge-base/document-preview')) {
    return mockGetDocumentPreview(body)
  } else if (url.includes('/models/stats')) {
    return mockGetModelStats()
  } else if (url.includes('/models/detail')) {
    return mockGetModelDetail(body)
  } else if (url.includes('/models/create')) {
    return mockCreateModel(body)
  } else if (url.includes('/models/update') && !url.includes('update-status')) {
    return mockUpdateModel(body)
  } else if (url.includes('/models/delete')) {
    return mockDeleteModel(body)
  } else if (url.includes('/models/set-default')) {
    return mockSetDefaultModel(body)
  } else if (url.includes('/models/test')) {
    return mockTestModel(body)
  } else if (url.includes('/models/health-check')) {
    return mockHealthCheckModels()
  } else if (url.includes('/models/update-status')) {
    return mockUpdateModelStatus(body)
  } else if (url.includes('/models/list')) {
    return mockGetModelList(body)
  }

  // 默认返回成功
  return {
    success: true,
    data: {},
    message: '操作成功'
  }
}

