/**
 * 环境配置工具
 * 用于区分开发环境和生产环境
 */

// 当前环境：development | production
export const ENV = import.meta.env.MODE || 'development'

// 是否为开发环境
export const isDev = ENV === 'development'

// API基础路径
export const API_BASE_URL = isDev 
  ? 'http://localhost:3000/api'  // 开发环境API地址
  : '/api'  // 生产环境API地址

// 是否使用模拟数据
export const USE_MOCK = isDev

