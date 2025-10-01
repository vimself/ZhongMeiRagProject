/**
 * 用户认证API
 * 包含登录、登出、修改密码等接口
 */

import { apiRequest } from '../utils/request'

/**
 * 用户登录
 * 
 * 功能描述：用户通过用户名和密码进行登录认证，登录成功后返回token和用户信息
 * 
 * 接口地址: /auth/login
 * 方法: POST
 * 需要登录: 否
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 登录参数
 * @param {string} params.username - 用户名
 * @param {string} params.password - 密码
 * 
 * 返回值: 
 * @returns {Promise<object>} 包含token和用户信息
 * {
 *   token: string,
 *   user: {
 *     id: string,
 *     username: string,
 *     name: string,
 *     role: string,
 *     email: string,
 *     phone: string
 *   }
 * }
 */
export async function login(params) {
  return await apiRequest('/auth/login', {
    method: 'POST',
    body: params
  })
}

/**
 * 用户登出
 * 
 * 功能描述：退出当前登录状态，清除服务端session或token
 * 
 * 接口地址: /auth/logout
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数: 无
 * 
 * 返回值:
 * @returns {Promise<object>} 登出结果
 */
export async function logout() {
  return await apiRequest('/auth/logout', {
    method: 'POST',
    body: {},
    needAuth: true
  })
}

/**
 * 修改密码
 * 
 * 功能描述：用户修改自己的登录密码
 * 
 * 接口地址: /auth/change-password
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 修改密码参数
 * @param {string} params.oldPassword - 旧密码
 * @param {string} params.newPassword - 新密码
 * 
 * 返回值:
 * @returns {Promise<object>} 修改结果
 */
export async function changePassword(params) {
  return await apiRequest('/auth/change-password', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 重置密码（忘记密码）
 * 
 * 功能描述：通过邮箱或手机号重置密码
 * 
 * 接口地址: /auth/reset-password
 * 方法: POST
 * 需要登录: 否
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 重置密码参数
 * @param {string} params.account - 账号（邮箱或手机号）
 * @param {string} params.code - 验证码
 * @param {string} params.newPassword - 新密码
 * 
 * 返回值:
 * @returns {Promise<object>} 重置结果
 */
export async function resetPassword(params) {
  return await apiRequest('/auth/reset-password', {
    method: 'POST',
    body: params
  })
}

