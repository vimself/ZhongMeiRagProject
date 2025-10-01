/**
 * 智能问答API
 * 包含会话管理、消息发送、模型选择等接口
 */

import { apiRequest } from '../utils/request'

/**
 * 获取知识库列表（用于对话页面选择）
 * 
 * 功能描述：获取用户可访问的知识库简化列表，用于智能问答页面的知识库选择下拉框
 * 
 * 接口地址: /api/chat/knowledge-bases
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数: 无
 * 
 * 返回值:
 * @returns {Promise<Array>} 知识库列表
 * [
 *   {
 *     id: string,   // 知识库ID
 *     name: string  // 知识库名称
 *   }
 * ]
 */
export async function getKnowledgeBaseList() {
  return await apiRequest('/api/chat/knowledge-bases', {
    method: 'POST',
    body: {},
    needAuth: true
  })
}

/**
 * 获取可用模型列表
 * 
 * 功能描述：获取系统配置的可用大语言模型列表，用于智能问答页面的模型选择下拉框
 * 
 * 接口地址: /api/chat/models
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数: 无
 * 
 * 返回值:
 * @returns {Promise<Array>} 模型列表
 * [
 *   {
 *     id: string,        // 模型ID
 *     name: string,      // 模型名称
 *     description: string // 模型描述
 *   }
 * ]
 */
export async function getModelList() {
  return await apiRequest('/api/chat/models', {
    method: 'POST',
    body: {},
    needAuth: true
  })
}

/**
 * 获取会话历史列表
 * 
 * 功能描述：获取当前用户的历史会话列表，按时间倒序排列
 * 
 * 接口地址: /api/chat/sessions
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 查询参数
 * @param {number} params.limit - 返回数量限制，默认20
 * 
 * 返回值:
 * @returns {Promise<Array>} 会话列表
 * [
 *   {
 *     id: string,      // 会话ID
 *     title: string,   // 会话标题
 *     time: string,    // 时间显示（如"今天 14:30"、"昨天 16:45"）
 *     createdAt: string // 创建时间戳
 *   }
 * ]
 */
export async function getSessionHistory(params = {}) {
  return await apiRequest('/api/chat/sessions', {
    method: 'POST',
    body: {
      limit: 20,
      ...params
    },
    needAuth: true
  })
}

/**
 * 创建新会话
 * 
 * 功能描述：创建一个新的对话会话
 * 
 * 接口地址: /api/chat/session/create
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 创建参数
 * @param {string} params.knowledgeBaseId - 知识库ID，"all"表示全部知识库
 * @param {string} params.modelId - 模型ID
 * 
 * 返回值:
 * @returns {Promise<object>} 会话信息
 * {
 *   id: string,      // 会话ID
 *   title: string,   // 会话标题
 *   createdAt: string // 创建时间
 * }
 */
export async function createSession(params) {
  return await apiRequest('/api/chat/session/create', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 发送消息
 * 
 * 功能描述：向指定会话发送用户问题，获取AI回答及引用来源
 * 
 * 接口地址: /api/chat/message/send
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 发送参数
 * @param {string} params.sessionId - 会话ID
 * @param {string} params.question - 用户问题
 * @param {string} params.knowledgeBaseId - 知识库ID
 * @param {string} params.modelId - 模型ID
 * 
 * 返回值:
 * @returns {Promise<object>} AI回答
 * {
 *   answer: string,    // AI生成的回答
 *   references: Array  // 引用来源列表
 *   [
 *     {
 *       title: string,      // 文档标题
 *       page: number,       // 页码
 *       content: string,    // 引用内容片段
 *       score: number       // 相关性得分
 *     }
 *   ]
 * }
 */
export async function sendChatMessage(params) {
  return await apiRequest('/api/chat/message/send', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 获取会话消息列表
 * 
 * 功能描述：获取指定会话的所有历史消息
 * 
 * 接口地址: /api/chat/session/messages
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 查询参数
 * @param {string} params.sessionId - 会话ID
 * 
 * 返回值:
 * @returns {Promise<Array>} 消息列表
 * [
 *   {
 *     id: string,          // 消息ID
 *     role: string,        // 角色: user-用户, assistant-助手
 *     content: string,     // 消息内容
 *     references: Array,   // 引用来源（仅assistant消息有）
 *     createdAt: string    // 创建时间
 *   }
 * ]
 */
export async function getSessionMessages(params) {
  return await apiRequest('/api/chat/session/messages', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 删除会话
 * 
 * 功能描述：删除指定会话及其所有消息
 * 
 * 接口地址: /api/chat/session/delete
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 删除参数
 * @param {string} params.sessionId - 会话ID
 * 
 * 返回值:
 * @returns {Promise<object>} 删除结果
 */
export async function deleteSession(params) {
  return await apiRequest('/api/chat/session/delete', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

/**
 * 重命名会话
 * 
 * 功能描述：修改会话标题
 * 
 * 接口地址: /api/chat/session/rename
 * 方法: POST
 * 需要登录: 是
 * 需要权限: 无
 * 
 * 请求参数:
 * @param {object} params - 重命名参数
 * @param {string} params.sessionId - 会话ID
 * @param {string} params.title - 新标题
 * 
 * 返回值:
 * @returns {Promise<object>} 更新结果
 */
export async function renameSession(params) {
  return await apiRequest('/api/chat/session/rename', {
    method: 'POST',
    body: params,
    needAuth: true
  })
}

