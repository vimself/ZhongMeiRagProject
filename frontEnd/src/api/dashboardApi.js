/**
 * 仪表盘API
 * 包含仪表盘统计数据、系统状态等接口
 */

import { apiRequest } from '../utils/request'

/**
 * 获取仪表盘统计数据
 * 
 * 功能描述：获取仪表盘首页的关键统计指标，包括今日问答、搜索次数、知识库数量、文档总数等
 * 
 * 接口地址: /api/dashboard/stats
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数: 无
 * 
 * 返回值:
 * @returns {Promise<object>} 统计数据
 * {
 *   todayQuestions: {
 *     count: number,        // 今日问答次数
 *     change: number,       // 变化百分比
 *     changeType: string    // 变化类型：increase/decrease
 *   },
 *   searchCount: {
 *     count: number,        // 搜索次数
 *     change: number,       // 变化百分比
 *     changeType: string
 *   },
 *   knowledgeBaseCount: {
 *     count: number,        // 知识库数量
 *     newCount: number      // 本周新增数量
 *   },
 *   documentCount: {
 *     count: number,        // 文档总数
 *     newCount: number      // 本周新增数量
 *   }
 * }
 */
export async function getDashboardStats() {
  return await apiRequest('/api/dashboard/stats', {
    method: 'POST',
    body: {},
    needAuth: true
  })
}

/**
 * 获取系统状态
 * 
 * 功能描述：获取系统各个服务的运行状态，包括LLM模型、向量模型、数据库等
 * 
 * 接口地址: /api/dashboard/system-status
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数: 无
 * 
 * 返回值:
 * @returns {Promise<object>} 系统状态
 * {
 *   llmModel: {
 *     name: string,         // 服务名称
 *     description: string,  // 描述
 *     status: string,       // 状态：online/offline
 *     online: number,       // 在线数量
 *     total: number         // 总数量
 *   },
 *   vectorModel: {
 *     name: string,
 *     description: string,
 *     status: string,
 *     online: number,
 *     total: number
 *   },
 *   vectorDb: {
 *     name: string,
 *     description: string,
 *     status: string        // 状态：normal/error
 *   },
 *   relationalDb: {
 *     name: string,
 *     description: string,
 *     status: string
 *   },
 *   systemStatus: string,   // 系统整体状态：normal/warning/error
 *   lastUpdate: string      // 最后更新时间
 * }
 */
export async function getSystemStatus() {
  return await apiRequest('/api/dashboard/system-status', {
    method: 'POST',
    body: {},
    needAuth: true
  })
}

/**
 * 刷新系统状态
 * 
 * 功能描述：手动触发刷新系统状态检查
 * 
 * 接口地址: /api/dashboard/refresh-status
 * 方法: POST
 * 需要登录: 是
 * 需要权限: admin
 * 
 * 请求参数: 无
 * 
 * 返回值:
 * @returns {Promise<object>} 刷新后的系统状态
 */
export async function refreshSystemStatus() {
  return await apiRequest('/api/dashboard/refresh-status', {
    method: 'POST',
    body: {},
    needAuth: true
  })
}


