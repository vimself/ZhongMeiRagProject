/**
 * 文档搜索API
 * 包含文档搜索、导出等接口
 */

import { apiRequest } from '../utils/request'

/**
 * 搜索文档
 * 
 * 功能描述：在知识库中搜索文档内容，支持关键词搜索和向量检索，返回相关文档列表及高亮摘要
 * 
 * 接口地址: /api/search/documents
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 搜索参数
 * @param {string} params.keyword - 搜索关键词
 * @param {string} params.knowledgeBaseId - 知识库ID，"all"表示全部知识库
 * @param {string} params.docType - 文档类型，"all"表示全部类型
 * @param {string} params.sortBy - 排序方式：relevance-相关度，time-时间，title-标题
 * @param {number} params.page - 页码，从1开始，默认1
 * @param {number} params.pageSize - 每页数量，默认10
 * 
 * 返回值:
 * @returns {Promise<object>} 搜索结果
 * {
 *   list: Array,    // 文档列表
 *   total: number,  // 总数
 *   page: number,   // 当前页码
 *   pageSize: number // 每页数量
 * }
 * 
 * 文档对象结构:
 * {
 *   id: string,           // 文档ID
 *   title: string,        // 文档标题
 *   knowledgeBase: string,// 所属知识库
 *   docType: string,      // 文档类型
 *   excerpt: string,      // 摘要片段（带高亮）
 *   score: number,        // 相关性得分
 *   pageNumber: number,   // 页码
 *   updateTime: string,   // 更新时间
 *   size: string          // 文件大小
 * }
 */
export async function searchDocuments(params) {
  return await apiRequest('/api/search/documents', {
    method: 'POST',
    body: {
      page: 1,
      pageSize: 10,
      sortBy: 'relevance',
      knowledgeBaseId: 'all',
      docType: 'all',
      ...params
    },
    needAuth: true
  })
}

/**
 * 获取热门搜索关键词
 * 
 * 功能描述：获取系统中的热门搜索关键词，基于搜索频率统计
 * 
 * 接口地址: /api/search/hot-keywords
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 查询参数
 * @param {number} params.limit - 返回数量，默认10
 * 
 * 返回值:
 * @returns {Promise<Array>} 热门关键词列表
 * [
 *   {
 *     keyword: string,  // 关键词
 *     count: number     // 搜索次数
 *   }
 * ]
 */
export async function getHotKeywords(params = {}) {
  return await apiRequest('/api/search/hot-keywords', {
    method: 'POST',
    body: {
      limit: 10,
      ...params
    },
    needAuth: true
  })
}

/**
 * 获取文档类型列表
 * 
 * 功能描述：获取系统支持的文档类型列表，用于筛选器下拉选择
 * 
 * 接口地址: /api/search/doc-types
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数: 无
 * 
 * 返回值:
 * @returns {Promise<Array>} 文档类型列表
 * [
 *   {
 *     value: string, // 类型值
 *     label: string  // 类型显示名称
 *   }
 * ]
 */
export async function getDocTypes() {
  return await apiRequest('/api/search/doc-types', {
    method: 'POST',
    body: {},
    needAuth: true
  })
}

/**
 * 导出搜索结果
 * 
 * 功能描述：将当前搜索结果导出为CSV文件
 * 
 * 接口地址: /api/search/export
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 导出参数
 * @param {string} params.keyword - 搜索关键词
 * @param {string} params.knowledgeBaseId - 知识库ID
 * @param {string} params.docType - 文档类型
 * @param {string} params.sortBy - 排序方式
 * 
 * 返回值:
 * @returns {Promise<object>} 导出结果
 * {
 *   downloadUrl: string, // 下载链接
 *   fileName: string,    // 文件名
 *   expiresIn: number    // 过期时间（秒）
 * }
 */
export async function exportSearchResults(params) {
  return await apiRequest('/api/search/export', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

