/**
 * 模型管理相关API
 * 
 * 功能描述：
 * - 管理系统中的LLM模型和向量模型
 * - 包括模型的增删改查、状态管理、健康检查等功能
 */

import { apiRequest } from '@/utils/request'

/**
 * 获取模型统计数据
 * 
 * - 接口核心功能描述：获取系统中各类模型的统计信息，包括LLM模型数量、向量模型数量、在线服务数、离线服务数
 * - 接口地址: /api/models/stats
 * - 方法: GET
 * - 需要登录: 是
 * - 需要权限: admin
 * - 请求参数: 无
 * - 响应类型: json
 * - 返回值：{
 *     llmCount: number,        // LLM模型总数
 *     embeddingCount: number,  // 向量模型总数
 *     onlineCount: number,     // 在线服务数
 *     offlineCount: number     // 离线服务数
 *   }
 */
export async function getModelStats() {
  return await apiRequest('/api/models/stats', {
    method: 'GET'
  })
}

/**
 * 获取模型列表
 * 
 * - 接口核心功能描述：获取所有模型列表，支持按类型筛选（LLM/Embedding）、按状态筛选（在线/离线）
 * - 接口地址: /api/models/list
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 请求参数: {
 *     type: string,      // 可选，模型类型：llm | embedding | all
 *     status: string,    // 可选，状态：online | offline | all
 *     page: number,      // 可选，页码，默认1
 *     pageSize: number   // 可选，每页数量，默认20
 *   }
 * - 响应类型: json
 * - 返回值：{
 *     total: number,
 *     list: Array<{
 *       id: string,
 *       name: string,
 *       type: string,          // llm | embedding
 *       description: string,
 *       provider: string,      // 提供方
 *       status: string,        // online | offline | error
 *       isDefault: boolean,    // 是否为默认模型
 *       modelSize: string,     // 模型大小
 *       contextLength: number, // 上下文长度
 *       latency: string,       // 推理延迟
 *       gpuMemory: string,     // GPU显存
 *       endpoint: string,      // 服务地址
 *       config: object,        // 模型配置参数
 *       createdAt: string,
 *       updatedAt: string
 *     }>
 *   }
 */
export async function getModelList(params = {}) {
  return await apiRequest('/api/models/list', {
    method: 'POST',
    body: params
  })
}

/**
 * 获取模型详情
 * 
 * - 接口核心功能描述：获取指定模型的详细信息，包括所有配置参数和运行状态
 * - 接口地址: /api/models/detail
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 请求参数: {
 *     id: string  // 必填，模型ID
 *   }
 * - 响应类型: json
 * - 返回值：{
 *     id: string,
 *     name: string,
 *     type: string,
 *     description: string,
 *     provider: string,
 *     status: string,
 *     isDefault: boolean,
 *     modelSize: string,
 *     contextLength: number,
 *     latency: string,
 *     gpuMemory: string,
 *     endpoint: string,
 *     config: {
 *       temperature: number,      // 温度参数
 *       topP: number,            // TopP参数
 *       topK: number,            // TopK参数
 *       maxTokens: number,       // 最大token数
 *       frequencyPenalty: number,// 频率惩罚
 *       presencePenalty: number  // 存在惩罚
 *     },
 *     healthCheck: {
 *       lastCheckTime: string,
 *       responseTime: number,
 *       status: string,
 *       message: string
 *     },
 *     createdAt: string,
 *     updatedAt: string
 *   }
 */
export async function getModelDetail(params) {
  return await apiRequest('/api/models/detail', {
    method: 'POST',
    body: params
  })
}

/**
 * 创建模型
 * 
 * - 接口核心功能描述：添加新的AI模型到系统中，需要配置模型基本信息、服务端点和运行参数
 * - 接口地址: /api/models/create
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 请求参数: {
 *     name: string,           // 必填，模型名称
 *     type: string,           // 必填，模型类型：llm | embedding
 *     description: string,    // 可选，模型描述
 *     provider: string,       // 必填，提供方
 *     endpoint: string,       // 必填，服务地址
 *     modelSize: string,      // 可选，模型大小
 *     contextLength: number,  // 可选，上下文长度
 *     gpuMemory: string,      // 可选，GPU显存
 *     config: {               // 可选，配置参数
 *       temperature: number,
 *       topP: number,
 *       topK: number,
 *       maxTokens: number,
 *       frequencyPenalty: number,
 *       presencePenalty: number
 *     }
 *   }
 * - 响应类型: json
 * - 返回值：{
 *     id: string,
 *     name: string
 *   }
 */
export async function createModel(params) {
  return await apiRequest('/api/models/create', {
    method: 'POST',
    body: params
  })
}

/**
 * 更新模型
 * 
 * - 接口核心功能描述：更新指定模型的配置信息，包括基本信息和运行参数
 * - 接口地址: /api/models/update
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 请求参数: {
 *     id: string,             // 必填，模型ID
 *     name: string,           // 可选，模型名称
 *     description: string,    // 可选，模型描述
 *     endpoint: string,       // 可选，服务地址
 *     config: object          // 可选，配置参数
 *   }
 * - 响应类型: json
 * - 返回值：{
 *     id: string,
 *     name: string
 *   }
 */
export async function updateModel(params) {
  return await apiRequest('/api/models/update', {
    method: 'POST',
    body: params
  })
}

/**
 * 删除模型
 * 
 * - 接口核心功能描述：从系统中删除指定的模型，默认模型和正在使用的模型不能删除
 * - 接口地址: /api/models/delete
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 请求参数: {
 *     id: string  // 必填，模型ID
 *   }
 * - 响应类型: json
 * - 返回值：{}
 */
export async function deleteModel(params) {
  return await apiRequest('/api/models/delete', {
    method: 'POST',
    body: params
  })
}

/**
 * 设置默认模型
 * 
 * - 接口核心功能描述：将指定模型设置为该类型的默认模型，用于新会话时的模型选择
 * - 接口地址: /api/models/set-default
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 请求参数: {
 *     id: string,    // 必填，模型ID
 *     type: string   // 必填，模型类型：llm | embedding
 *   }
 * - 响应类型: json
 * - 返回值：{}
 */
export async function setDefaultModel(params) {
  return await apiRequest('/api/models/set-default', {
    method: 'POST',
    body: params
  })
}

/**
 * 测试模型连接
 * 
 * - 接口核心功能描述：测试指定模型的服务连接是否正常，返回响应时间和状态
 * - 接口地址: /api/models/test
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 请求参数: {
 *     id: string  // 必填，模型ID
 *   }
 * - 响应类型: json
 * - 返回值：{
 *     status: string,      // online | offline | error
 *     responseTime: number,// 响应时间(ms)
 *     message: string,     // 状态消息
 *     timestamp: string    // 测试时间
 *   }
 */
export async function testModel(params) {
  return await apiRequest('/api/models/test', {
    method: 'POST',
    body: params
  })
}

/**
 * 批量健康检查
 * 
 * - 接口核心功能描述：对所有在线模型执行健康检查，更新模型状态和延迟信息
 * - 接口地址: /api/models/health-check
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 请求参数: {}
 * - 响应类型: json
 * - 返回值：{
 *     total: number,      // 检查的模型总数
 *     success: number,    // 检查成功的数量
 *     failed: number,     // 检查失败的数量
 *     results: Array<{
 *       id: string,
 *       name: string,
 *       status: string,
 *       responseTime: number,
 *       message: string
 *     }>
 *   }
 */
export async function healthCheckModels(params = {}) {
  return await apiRequest('/api/models/health-check', {
    method: 'POST',
    body: params
  })
}

/**
 * 更新模型状态
 * 
 * - 接口核心功能描述：手动更新模型的运行状态（启用/禁用）
 * - 接口地址: /api/models/update-status
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 请求参数: {
 *     id: string,      // 必填，模型ID
 *     status: string   // 必填，状态：online | offline
 *   }
 * - 响应类型: json
 * - 返回值：{}
 */
export async function updateModelStatus(params) {
  return await apiRequest('/api/models/update-status', {
    method: 'POST',
    body: params
  })
}

