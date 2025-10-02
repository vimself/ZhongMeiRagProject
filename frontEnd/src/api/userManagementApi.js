/**
 * 用户管理API
 * 包含用户列表、创建、编辑、删除、状态管理等接口
 */

import { apiRequest } from '../utils/request'

/**
 * 获取用户统计数据
 * 
 * 功能描述：获取用户统计概览，包括总用户数、活跃用户数、管理员数、禁用用户数
 * 
 * 接口地址: /api/admin/users/stats
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数: 无
 * 
 * 返回值:
 * @returns {Promise<object>} 统计数据
 * {
 *   totalUsers: number,    // 总用户数
 *   activeUsers: number,   // 活跃用户数
 *   adminUsers: number,    // 管理员数
 *   disabledUsers: number  // 禁用用户数
 * }
 */
export async function getUserStats() {
  return await apiRequest('/api/admin/users/stats', {
    method: 'POST',
    body: {},
    needAuth: true
  })
}

/**
 * 获取用户列表
 * 
 * 功能描述：获取系统用户列表，支持搜索、角色筛选、状态筛选和分页
 * 
 * 接口地址: /api/admin/users/list
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数:
 * @param {object} params - 查询参数
 * @param {string} params.keyword - 搜索关键词（姓名、邮箱、手机号），可选
 * @param {string} params.role - 角色筛选（admin/user），可选，空字符串表示全部
 * @param {string} params.status - 状态筛选（active/disabled），可选，空字符串表示全部
 * @param {number} params.page - 页码，从1开始，默认1
 * @param {number} params.pageSize - 每页数量，默认10
 * 
 * 返回值:
 * @returns {Promise<object>} 用户列表数据
 * {
 *   list: Array,    // 用户列表
 *   total: number,  // 总数
 *   page: number,   // 当前页码
 *   pageSize: number // 每页数量
 * }
 * 
 * 用户对象结构:
 * {
 *   id: string,           // 用户ID
 *   name: string,         // 姓名
 *   username: string,     // 用户名
 *   email: string,        // 邮箱
 *   phone: string,        // 手机号（部分隐藏）
 *   role: string,         // 角色：admin-管理员，user-普通用户
 *   status: string,       // 状态：active-活跃，disabled-禁用
 *   avatarColor: string,  // 头像背景色
 *   lastLogin: string,    // 最后登录时间
 *   createdAt: string     // 创建时间
 * }
 */
export async function getUserList(params = {}) {
  return await apiRequest('/api/admin/users/list', {
    method: 'POST',
    body: {
      page: 1,
      pageSize: 10,
      ...params
    },
    needAuth: true
  })
}

/**
 * 创建用户
 * 
 * 功能描述：创建新用户账号
 * 
 * 接口地址: /api/admin/users/create
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数:
 * @param {object} params - 创建参数
 * @param {string} params.name - 姓名
 * @param {string} params.username - 用户名（唯一）
 * @param {string} params.email - 邮箱
 * @param {string} params.phone - 手机号
 * @param {string} params.role - 角色（admin/user）
 * @param {string} params.password - 初始密码
 * 
 * 返回值:
 * @returns {Promise<object>} 创建结果
 */
export async function createUser(params) {
  return await apiRequest('/api/admin/users/create', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 更新用户信息
 * 
 * 功能描述：更新用户的基本信息（不包括密码）
 * 
 * 接口地址: /api/admin/users/update
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数:
 * @param {object} params - 更新参数
 * @param {string} params.id - 用户ID
 * @param {string} params.name - 姓名
 * @param {string} params.email - 邮箱
 * @param {string} params.phone - 手机号
 * @param {string} params.role - 角色（admin/user）
 * 
 * 返回值:
 * @returns {Promise<object>} 更新结果
 */
export async function updateUser(params) {
  return await apiRequest('/api/admin/users/update', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 删除用户
 * 
 * 功能描述：删除用户账号（不可恢复）
 * 
 * 接口地址: /api/admin/users/delete
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数:
 * @param {object} params - 删除参数
 * @param {string} params.userId - 用户ID
 * 
 * 返回值:
 * @returns {Promise<object>} 删除结果
 */
export async function deleteUser(params) {
  return await apiRequest('/api/admin/users/delete', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 切换用户状态
 * 
 * 功能描述：启用或禁用用户账号
 * 
 * 接口地址: /api/admin/users/toggle-status
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数:
 * @param {object} params - 切换参数
 * @param {string} params.userId - 用户ID
 * @param {string} params.status - 目标状态（active/disabled）
 * 
 * 返回值:
 * @returns {Promise<object>} 切换结果
 */
export async function toggleUserStatus(params) {
  return await apiRequest('/api/admin/users/toggle-status', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 重置用户密码
 * 
 * 功能描述：重置用户密码为随机密码
 * 
 * 接口地址: /api/admin/users/reset-password
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数:
 * @param {object} params - 重置参数
 * @param {string} params.userId - 用户ID
 * 
 * 返回值:
 * @returns {Promise<object>} 重置结果
 * {
 *   newPassword: string  // 新密码（明文，仅此次返回）
 * }
 */
export async function resetUserPassword(params) {
  return await apiRequest('/api/admin/users/reset-password', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 导出用户列表
 * 
 * 功能描述：导出用户列表为CSV文件
 * 
 * 接口地址: /api/admin/users/export
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数:
 * @param {object} params - 导出参数
 * @param {string} params.keyword - 搜索关键词，可选
 * @param {string} params.role - 角色筛选，可选
 * @param {string} params.status - 状态筛选，可选
 * 
 * 返回值:
 * @returns {Promise<object>} 导出结果
 * {
 *   downloadUrl: string, // 下载链接
 *   fileName: string,    // 文件名
 *   expiresIn: number    // 过期时间（秒）
 * }
 */
export async function exportUsers(params = {}) {
  return await apiRequest('/api/admin/users/export', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

