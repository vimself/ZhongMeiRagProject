/**
 * 用户个人信息API
 * 包含个人信息查看、修改、头像上传等接口
 */

import { apiRequest } from '../utils/request'

/**
 * 获取个人信息
 * 
 * 功能描述：获取当前登录用户的详细个人信息，包括基本资料、联系方式等
 * 
 * 接口地址: /api/user/profile
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数: 无
 * 
 * 返回值:
 * @returns {Promise<object>} 用户信息
 * {
 *   id: string,           // 用户ID
 *   username: string,     // 用户名
 *   name: string,         // 姓名
 *   email: string,        // 邮箱
 *   phone: string,        // 手机号
 *   department: string,   // 部门
 *   position: string,     // 职位
 *   avatar: string,       // 头像URL
 *   bio: string,          // 个人简介
 *   role: string,         // 用户角色
 *   createdAt: string,    // 注册时间
 *   lastLoginAt: string   // 最后登录时间
 * }
 */
export async function getUserProfile() {
  return await apiRequest('/api/user/profile', {
    method: 'POST',
    body: {},
    needAuth: true
  })
}

/**
 * 更新个人信息
 * 
 * 功能描述：更新用户的基本信息，如姓名、邮箱、手机、部门、职位、个人简介等
 * 
 * 接口地址: /api/user/profile/update
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 更新参数
 * @param {string} params.name - 姓名
 * @param {string} params.email - 邮箱地址
 * @param {string} params.phone - 手机号码
 * @param {string} params.department - 部门
 * @param {string} params.position - 职位
 * @param {string} params.bio - 个人简介
 * 
 * 返回值:
 * @returns {Promise<object>} 更新结果
 */
export async function updateUserProfile(params) {
  return await apiRequest('/api/user/profile/update', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 上传头像
 * 
 * 功能描述：上传用户头像图片，支持JPG、PNG格式，文件大小不超过2MB
 * 
 * 接口地址: /api/user/avatar/upload
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {FormData} formData - 包含头像文件的表单数据
 * @param {File} formData.avatar - 头像文件
 * 
 * 返回值:
 * @returns {Promise<object>} 上传结果
 * {
 *   avatarUrl: string  // 新头像URL
 * }
 */
export async function uploadUserAvatar(formData) {
  // 注意：文件上传需要特殊处理
  return await apiRequest('/api/user/avatar/upload', {
    method: 'POST',
    body: formData,
    needAuth: true,
    headers: {
      // FormData会自动设置Content-Type
    }
  })
}

/**
 * 获取部门列表
 * 
 * 功能描述：获取公司部门列表，用于个人信息编辑时的部门选择
 * 
 * 接口地址: /api/user/departments
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数: 无
 * 
 * 返回值:
 * @returns {Promise<Array>} 部门列表
 * [
 *   {
 *     value: string, // 部门代码
 *     label: string  // 部门名称
 *   }
 * ]
 */
export async function getDepartmentList() {
  return await apiRequest('/api/user/departments', {
    method: 'POST',
    body: {},
    needAuth: true
  })
}

/**
 * 获取登录记录
 * 
 * 功能描述：获取用户最近的登录记录，包括设备信息、IP地址、登录时间等
 * 
 * 接口地址: /api/user/login-records
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 查询参数
 * @param {number} params.limit - 返回数量，默认10
 * 
 * 返回值:
 * @returns {Promise<Array>} 登录记录列表
 * [
 *   {
 *     id: string,        // 记录ID
 *     device: string,    // 设备信息（如：Windows Chrome）
 *     ip: string,        // IP地址
 *     location: string,  // 登录地点（可选）
 *     loginTime: string, // 登录时间
 *     status: string,    // 状态：current-当前会话，ended-已结束
 *     userAgent: string  // 浏览器标识
 *   }
 * ]
 */
export async function getLoginRecords(params = {}) {
  return await apiRequest('/api/user/login-records', {
    method: 'POST',
    body: {
      limit: 10,
      ...params
    },
    needAuth: true
  })
}

/**
 * 修改密码（在个人中心页面）
 * 
 * 功能描述：在个人中心页面修改密码，需要验证当前密码
 * 
 * 接口地址: /api/user/change-password
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 修改密码参数
 * @param {string} params.currentPassword - 当前密码
 * @param {string} params.newPassword - 新密码
 * @param {string} params.confirmPassword - 确认新密码
 * 
 * 返回值:
 * @returns {Promise<object>} 修改结果
 */
export async function changeUserPassword(params) {
  return await apiRequest('/api/user/change-password', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

