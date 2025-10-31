/**
 * 环境配置工具
 * 用于区分开发环境和生产环境
 */

// 当前环境：development | production
export const ENV = import.meta.env.MODE || 'development'

// 是否为开发环境
export const isDev = ENV === 'development'

// API基础路径
// 注意：前端API文件中已经包含了 /api 前缀，这里应该为空字符串
// Vite配置中会自动将 /api 开头的请求代理到后端 http://localhost:8000
export const API_BASE_URL = ''

// 是否使用模拟数据
// 开发时修改此处：true=使用Mock数据，false=连接真实后端API
export const USE_MOCK = false  // 联调模式：连接真实后端API

