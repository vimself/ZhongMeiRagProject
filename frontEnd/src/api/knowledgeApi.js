/**
 * 知识库管理API
 * 包含知识库的查询、创建、更新、删除等接口
 */

import { apiRequest } from '../utils/request'

/**
 * 获取知识库统计数据
 * 
 * 功能描述：获取用户可访问的知识库统计信息，包括知识库数量、文档数量、今日问答次数等
 * 
 * 接口地址: /api/knowledge-base/stats
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数: 无
 * 
 * 返回值:
 * @returns {Promise<object>} 统计数据
 * {
 *   accessibleKnowledgeBase: number, // 可访问知识库数量
 *   accessibleDocuments: number,     // 可查阅文档数量
 *   todayQuestions: number           // 今日问答次数
 * }
 */
export async function getKnowledgeBaseStats() {
  return await apiRequest('/api/knowledge-base/stats', {
    method: 'POST',
    body: {},
    needAuth: true
  })
}

/**
 * 获取知识库列表
 * 
 * 功能描述：获取当前用户有权访问的知识库列表，包含知识库的基本信息、统计数据和状态
 * 
 * 接口地址: /api/knowledge-base/list
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 查询参数
 * @param {number} params.page - 页码，从1开始，默认1
 * @param {number} params.pageSize - 每页数量，默认20
 * @param {string} params.keyword - 搜索关键字，可选
 * 
 * 返回值:
 * @returns {Promise<Array>} 知识库列表
 * [
 *   {
 *     id: string,           // 知识库ID
 *     name: string,         // 知识库名称
 *     code: string,         // 知识库编码
 *     description: string,  // 描述
 *     icon: string,         // 图标类名
 *     iconColor: string,    // 图标颜色
 *     documentCount: number,// 文档数量
 *     storageSize: string,  // 存储大小
 *     lastUpdate: string,   // 最后更新时间
 *     status: string,       // 状态: active-活跃, processing-处理中, inactive-未激活
 *     progress: number,     // 处理进度(0-100)，仅status为processing时有效
 *     viewers: number       // 查看人数
 *   }
 * ]
 */
export async function getKnowledgeBaseList(params = {}) {
  return await apiRequest('/api/knowledge-base/list', {
    method: 'POST',
    body: {
      page: 1,
      pageSize: 20,
      ...params
    },
    needAuth: true
  })
}

/**
 * 获取知识库详情
 * 
 * 功能描述：获取指定知识库的详细信息
 * 
 * 接口地址: /api/knowledge-base/detail
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 对该知识库有查看权限
 * 
 * 请求参数:
 * @param {object} params - 请求参数
 * @param {string} params.id - 知识库ID
 * 
 * 返回值:
 * @returns {Promise<object>} 知识库详情
 */
export async function getKnowledgeBaseDetail(params) {
  return await apiRequest('/api/knowledge-base/detail', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 创建知识库
 * 
 * 功能描述：创建一个新的知识库（仅管理员）
 * 
 * 接口地址: /api/knowledge-base/create
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数:
 * @param {object} params - 创建参数
 * @param {string} params.name - 知识库名称
 * @param {string} params.code - 知识库编码
 * @param {string} params.description - 描述
 * @param {string} params.visible - 可见范围: all-所有人, authorized-授权用户, private-私有
 * 
 * 返回值:
 * @returns {Promise<object>} 创建的知识库信息
 */
export async function createKnowledgeBase(params) {
  return await apiRequest('/api/knowledge-base/create', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 更新知识库
 * 
 * 功能描述：更新知识库信息（需要管理权限）
 * 
 * 接口地址: /api/knowledge-base/update
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 对该知识库有管理权限
 * 
 * 请求参数:
 * @param {object} params - 更新参数
 * @param {string} params.id - 知识库ID
 * @param {string} params.name - 知识库名称
 * @param {string} params.description - 描述
 * 
 * 返回值:
 * @returns {Promise<object>} 更新后的知识库信息
 */
export async function updateKnowledgeBase(params) {
  return await apiRequest('/api/knowledge-base/update', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 删除知识库
 * 
 * 功能描述：删除指定知识库（仅管理员）
 * 
 * 接口地址: /api/knowledge-base/delete
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数:
 * @param {object} params - 删除参数
 * @param {string} params.id - 知识库ID
 * 
 * 返回值:
 * @returns {Promise<object>} 删除结果
 */
export async function deleteKnowledgeBase(params) {
  return await apiRequest('/api/knowledge-base/delete', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

