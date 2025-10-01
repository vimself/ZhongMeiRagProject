# 前后端接口文档

> **文档说明**: 本文档汇总所有前端需要调用的后端接口,供后端开发参考实现。
> 
> **更新日期**: 2025-10-01  
> **版本**: v1.0  
> **维护者**: 前端开发团队

---

## 目录

- [1. 用户认证模块](#1-用户认证模块)
- [2. 知识库管理模块](#2-知识库管理模块)
- [3. 文档管理模块](#3-文档管理模块)
- [4. RAG 智能问答模块](#4-rag-智能问答模块)
- [5. 搜索模块](#5-搜索模块)
- [6. 用户管理模块](#6-用户管理模块)
- [7. 模型管理模块](#7-模型管理模块)
- [8. 权限管理模块](#8-权限管理模块)

---

## 通用说明

### 请求规范
- **请求方式**: 默认使用 POST,特殊情况会标注
- **请求头**: 
  - `Content-Type: application/json`
  - `Authorization: Bearer {token}` (需要登录的接口)
- **请求体**: 统一使用 JSON 格式,空参数使用 `{}`

### 响应规范
所有接口统一返回格式:
```json
{
  "error": 0,
  "message": "操作成功",
  "body": {}
}
```

**响应码说明**:
- `error = 0`: 请求成功,无异常
- `error = 401`: 需要登录或登录已过期
- `error = 403`: 权限不足
- `error = 500`: 系统异常(需要弹出系统错误提示)
- `error = 其他值`: 业务异常(直接弹出 message 内容)

### 认证机制
- 登录成功后,后端返回 token
- 前端将 token 保存在本地存储(localStorage/sessionStorage)
- 后续请求在 Header 中携带: `Authorization: Bearer {token}`
- token 过期或无效时,返回 `error = 401`,前端跳转到登录页

---

## 1. 用户认证模块

### 1.1 用户登录

**功能描述**: 用户通过用户名和密码进行系统登录,登录成功后返回访问令牌(token)用于后续接口认证。

**业务背景**: 作为系统入口,所有用户必须通过认证才能访问系统功能。支持普通用户和管理员两种角色登录。

**接口地址**: `/api/auth/login`

**请求方法**: POST

**需要登录**: 否

**需要权限**: 无

**请求头 (Headers)**:
```
Content-Type: application/json
```

**请求体 (Body)**:
```json
{
  "username": "string, 用户名",
  "password": "string, 密码"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| username | string | 是 | 用户登录名 | "zhangsan" |
| password | string | 是 | 用户密码 | "Pass@123" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "登录成功",
  "body": {
    "token": "string, 访问令牌",
    "user": {
      "id": "string, 用户ID",
      "username": "string, 用户名",
      "name": "string, 真实姓名",
      "role": "string, 角色(user/admin)",
      "email": "string, 邮箱",
      "phone": "string, 手机号"
    }
  }
}
```

**Body 数据结构说明**:
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| token | string | JWT 访问令牌,有效期24小时 | "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." |
| user.id | string | 用户唯一标识 | "user_001" |
| user.username | string | 用户登录名 | "zhangsan" |
| user.name | string | 用户真实姓名 | "张三" |
| user.role | string | 用户角色: user-普通用户, admin-管理员 | "admin" |
| user.email | string | 用户邮箱 | "zhangsan@company.com" |
| user.phone | string | 手机号码 | "13800138000" |

**请求示例**:
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "Admin@123"
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "登录成功",
  "body": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJ1c2VyXzAwMSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcyNzg2NDQwMH0.abc123...",
    "user": {
      "id": "user_001",
      "username": "admin",
      "name": "系统管理员",
      "role": "admin",
      "email": "admin@company.com",
      "phone": "13800138000"
    }
  }
}
```

**失败响应示例**:
```json
{
  "error": 1001,
  "message": "用户名或密码错误",
  "body": {}
}
```

```json
{
  "error": 1002,
  "message": "账号已被禁用,请联系管理员",
  "body": {}
}
```

**前端调用示例**:
```javascript
/**
 * 用户登录
 * - 接口地址: /api/auth/login
 * - 方法: POST
 * - 需要登录: 否
 * - 请求参数: { username, password }
 * - 返回值: { token, user }
 */
export async function login(username, password) {
  return await apiRequest('/api/auth/login', {
    method: 'POST',
    body: { username, password }
  });
}
```

**注意事项**:
- 密码应在前端进行加密传输(建议使用 HTTPS)
- token 有效期为 24 小时,过期后需要重新登录
- 连续登录失败 5 次后,账号将被锁定 30 分钟
- 登录成功后,前端应将 token 保存到 localStorage,并将用户信息保存到 Vuex store

---

### 1.2 用户登出

**功能描述**: 用户退出登录,清除服务端 session 和前端 token。

**业务背景**: 用户主动退出系统或切换账号时调用。

**接口地址**: `/api/auth/logout`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 无

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{}
```

**响应格式**: 
```json
{
  "error": 0,
  "message": "登出成功",
  "body": {}
}
```

**请求示例**:
```
POST /api/auth/logout
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "登出成功",
  "body": {}
}
```

**前端调用示例**:
```javascript
/**
 * 用户登出
 * - 接口地址: /api/auth/logout
 * - 方法: POST
 * - 需要登录: 是
 * - 请求参数: 无
 * - 返回值: 无
 */
export async function logout() {
  return await apiRequest('/api/auth/logout', {
    method: 'POST',
    body: {}
  });
}
```

**注意事项**:
- 前端调用后应清除本地存储的 token 和用户信息
- 无论接口调用成功与否,前端都应清除本地数据并跳转到登录页

---

### 1.3 修改密码

**功能描述**: 用户修改自己的登录密码。

**业务背景**: 用户自主修改密码以提高账号安全性。

**接口地址**: `/api/auth/change-password`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 无

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "oldPassword": "string, 原密码",
  "newPassword": "string, 新密码"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| oldPassword | string | 是 | 原密码 | "OldPass@123" |
| newPassword | string | 是 | 新密码,长度8-20位,需包含大小写字母和数字 | "NewPass@456" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "密码修改成功,请重新登录",
  "body": {}
}
```

**请求示例**:
```
POST /api/auth/change-password
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "oldPassword": "OldPass@123",
  "newPassword": "NewPass@456"
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "密码修改成功,请重新登录",
  "body": {}
}
```

**失败响应示例**:
```json
{
  "error": 1003,
  "message": "原密码错误",
  "body": {}
}
```

```json
{
  "error": 1004,
  "message": "新密码格式不符合要求",
  "body": {}
}
```

**前端调用示例**:
```javascript
/**
 * 修改密码
 * - 接口地址: /api/auth/change-password
 * - 方法: POST
 * - 需要登录: 是
 * - 请求参数: { oldPassword, newPassword }
 * - 返回值: 无
 */
export async function changePassword(oldPassword, newPassword) {
  return await apiRequest('/api/auth/change-password', {
    method: 'POST',
    body: { oldPassword, newPassword }
  });
}
```

**注意事项**:
- 密码强度要求: 8-20位,包含大小写字母、数字
- 修改成功后,前端应清除 token 并跳转到登录页
- 新密码不能与最近 3 次使用过的密码相同

---

## 2. 知识库管理模块

### 2.1 获取知识库统计数据

**功能描述**: 获取当前用户可访问的知识库统计信息，包括可访问知识库数量、可查阅文档数量、今日问答次数等，用于首页展示统计卡片。

**业务背景**: 为用户提供知识库使用情况的整体概览，帮助用户快速了解自己的知识库访问权限和使用情况。

**接口地址**: `/api/knowledge-base/stats`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 无

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{}
```

**参数说明**:
无参数

**响应格式**: 
```json
{
  "error": 0,
  "message": "获取成功",
  "body": {
    "accessibleKnowledgeBase": "number, 可访问知识库数量",
    "accessibleDocuments": "number, 可查阅文档数量",
    "todayQuestions": "number, 今日问答次数"
  }
}
```

**Body 数据结构说明**:
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| accessibleKnowledgeBase | number | 用户可访问的知识库总数 | 3 |
| accessibleDocuments | number | 用户可查阅的文档总数(所有可访问知识库) | 312 |
| todayQuestions | number | 今日用户的问答次数 | 15 |

**请求示例**:
```
POST /api/knowledge-base/stats
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "获取成功",
  "body": {
    "accessibleKnowledgeBase": 3,
    "accessibleDocuments": 312,
    "todayQuestions": 15
  }
}
```

**前端调用示例**:
```javascript
/**
 * 获取知识库统计数据
 * - 接口地址: /api/knowledge-base/stats
 * - 方法: POST
 * - 需要登录: 是
 * - 请求参数: 无
 * - 返回值: { accessibleKnowledgeBase, accessibleDocuments, todayQuestions }
 */
export async function getKnowledgeBaseStats() {
  return await apiRequest('/api/knowledge-base/stats', {
    method: 'POST',
    body: {},
    needAuth: true
  });
}
```

**注意事项**:
- 统计数据基于用户当前的权限实时计算
- 今日问答次数在每天00:00重置
- 数据更新可能有1-2分钟延迟

---

### 2.2 获取知识库列表

**功能描述**: 获取当前用户有权访问的知识库列表，包含知识库的基本信息、统计数据、状态等详细信息，用于知识库页面展示。

**业务背景**: 用户登录后需要查看自己可以访问的所有知识库，并了解每个知识库的基本情况，以便选择合适的知识库进行查询或管理。

**接口地址**: `/api/knowledge-base/list`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 无

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "page": "number, 页码，从1开始，默认1",
  "pageSize": "number, 每页数量，默认20",
  "keyword": "string, 搜索关键字，可选"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| page | number | 否 | 页码，从1开始 | 1 |
| pageSize | number | 否 | 每页数量 | 20 |
| keyword | string | 否 | 搜索关键字，匹配知识库名称或描述 | "技术" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    {
      "id": "string, 知识库ID",
      "name": "string, 知识库名称",
      "code": "string, 知识库编码",
      "description": "string, 知识库描述",
      "icon": "string, 图标类名",
      "iconColor": "string, 图标背景色(CSS渐变)",
      "documentCount": "number, 文档数量",
      "storageSize": "string, 存储大小",
      "lastUpdate": "string, 最后更新时间(相对时间)",
      "status": "string, 状态: active-活跃, processing-处理中, inactive-未激活",
      "progress": "number, 处理进度(0-100)，仅status为processing时有效",
      "viewers": "number, 查看人数"
    }
  ]
}
```

**Body 数据结构说明**:
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| id | string | 知识库唯一标识 | "kb_001" |
| name | string | 知识库名称 | "技术规范库" |
| code | string | 知识库编码(英文) | "tech-standards" |
| description | string | 知识库描述 | "包含编程规范、API设计、架构指南等技术文档" |
| icon | string | 图标CSS类名 | "icon-code" |
| iconColor | string | 图标背景渐变色 | "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" |
| documentCount | number | 知识库中的文档数量 | 156 |
| storageSize | string | 存储空间大小 | "2.3 GB" |
| lastUpdate | string | 最后更新时间(相对) | "2小时前" |
| status | string | 知识库状态 | "active" |
| progress | number | 处理进度(仅processing状态) | 85 |
| viewers | number | 查看该知识库的用户数 | 1200 |

**请求示例**:
```
POST /api/knowledge-base/list
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "page": 1,
  "pageSize": 20
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    {
      "id": "kb_001",
      "name": "技术规范库",
      "code": "tech-standards",
      "description": "包含编程规范、API设计、架构指南等技术文档",
      "icon": "icon-code",
      "iconColor": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      "documentCount": 156,
      "storageSize": "2.3 GB",
      "lastUpdate": "2小时前",
      "status": "active",
      "progress": 100,
      "viewers": 1200
    },
    {
      "id": "kb_002",
      "name": "产品手册",
      "code": "product-manual",
      "description": "产品功能介绍、使用指南、常见问题等",
      "icon": "icon-book",
      "iconColor": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
      "documentCount": 89,
      "storageSize": "1.5 GB",
      "lastUpdate": "1天前",
      "status": "active",
      "progress": 100,
      "viewers": 892
    },
    {
      "id": "kb_003",
      "name": "运维文档",
      "code": "ops-docs",
      "description": "系统部署、监控、故障处理等运维类文档",
      "icon": "icon-gear",
      "iconColor": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
      "documentCount": 67,
      "storageSize": "890 MB",
      "lastUpdate": "3天前",
      "status": "processing",
      "progress": 85,
      "viewers": 456
    }
  ]
}
```

**失败响应示例**:
```json
{
  "error": 403,
  "message": "无权访问知识库",
  "body": []
}
```

**前端调用示例**:
```javascript
/**
 * 获取知识库列表
 * - 接口地址: /api/knowledge-base/list
 * - 方法: POST
 * - 需要登录: 是
 * - 请求参数: { page, pageSize, keyword }
 * - 返回值: Array<KnowledgeBase>
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
  });
}
```

**注意事项**:
- 只返回用户有查看权限的知识库
- status 为 processing 时，表示知识库正在导入文档，progress 显示处理进度
- lastUpdate 为相对时间格式(如"2小时前"、"1天前")，便于用户理解
- viewers 统计最近30天访问过该知识库的去重用户数
- 知识库按最后更新时间倒序排列

---

### 2.3 获取知识库详情

**功能描述**: 获取指定知识库的详细信息，包括完整配置、文档列表、授权用户等。

**业务背景**: 用户点击知识库卡片进入详情页时调用，查看知识库的详细信息和管理设置。

**接口地址**: `/api/knowledge-base/detail`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 对该知识库有查看权限

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "id": "string, 知识库ID"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| id | string | 是 | 知识库ID | "kb_001" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "获取成功",
  "body": {
    "id": "string, 知识库ID",
    "name": "string, 知识库名称",
    "code": "string, 知识库编码",
    "description": "string, 描述",
    "visible": "string, 可见范围",
    "createdAt": "string, 创建时间",
    "createdBy": "string, 创建人",
    "permission": "string, 当前用户权限: view-查看, manage-管理"
  }
}
```

**请求示例**:
```
POST /api/knowledge-base/detail
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "id": "kb_001"
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "获取成功",
  "body": {
    "id": "kb_001",
    "name": "技术规范库",
    "code": "tech-standards",
    "description": "包含编程规范、API设计、架构指南等技术文档",
    "visible": "all",
    "createdAt": "2025-09-01T10:30:00Z",
    "createdBy": "admin",
    "permission": "view"
  }
}
```

**失败响应示例**:
```json
{
  "error": 2001,
  "message": "知识库不存在",
  "body": {}
}
```

```json
{
  "error": 403,
  "message": "无权访问该知识库",
  "body": {}
}
```

**前端调用示例**:
```javascript
/**
 * 获取知识库详情
 * - 接口地址: /api/knowledge-base/detail
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: 对该知识库有查看权限
 * - 请求参数: { id }
 * - 返回值: KnowledgeBase详情对象
 */
export async function getKnowledgeBaseDetail(params) {
  return await apiRequest('/api/knowledge-base/detail', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

**注意事项**:
- 需要用户对该知识库有查看或管理权限
- permission 字段表示当前用户对该知识库的权限级别
- visible 字段值: all-所有人可见, authorized-仅授权用户, private-私有

---

## 3. 文档管理模块

*待补充:当生成文档管理相关前端界面时,此部分将被填充*

---

## 4. RAG 智能问答模块

### 4.1 获取知识库列表（对话页面）

**功能描述**: 获取用户可访问的知识库简化列表，用于智能问答页面的知识库选择下拉框。

**业务背景**: 用户在智能问答时需要选择要查询的知识库范围，此接口提供知识库的简化列表。

**接口地址**: `/api/chat/knowledge-bases`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 无

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{}
```

**响应格式**: 
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    {
      "id": "string, 知识库ID",
      "name": "string, 知识库名称"
    }
  ]
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    { "id": "kb_001", "name": "技术规范库" },
    { "id": "kb_002", "name": "产品手册" },
    { "id": "kb_003", "name": "运维文档" }
  ]
}
```

**前端调用示例**:
```javascript
/**
 * 获取知识库列表（对话页面）
 * - 接口地址: /api/chat/knowledge-bases
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: Array<{id, name}>
 */
export async function getKnowledgeBaseList() {
  return await apiRequest('/api/chat/knowledge-bases', {
    method: 'POST',
    body: {},
    needAuth: true
  });
}
```

---

### 4.2 获取可用模型列表

**功能描述**: 获取系统配置的可用大语言模型列表，用于智能问答页面的模型选择下拉框。

**业务背景**: 不同的模型有不同的能力和性能特点，用户可根据需求选择合适的模型进行对话。

**接口地址**: `/api/chat/models`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 无

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{}
```

**响应格式**: 
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    {
      "id": "string, 模型ID",
      "name": "string, 模型名称",
      "description": "string, 模型描述"
    }
  ]
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    {
      "id": "qwen2-7b",
      "name": "Qwen2-7B",
      "description": "通义千问2 7B版本，适合日常问答"
    },
    {
      "id": "qwen2-14b",
      "name": "Qwen2-14B",
      "description": "通义千问2 14B版本，性能更强"
    }
  ]
}
```

**前端调用示例**:
```javascript
/**
 * 获取可用模型列表
 * - 接口地址: /api/chat/models
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: Array<{id, name, description}>
 */
export async function getModelList() {
  return await apiRequest('/api/chat/models', {
    method: 'POST',
    body: {},
    needAuth: true
  });
}
```

---

### 4.3 获取会话历史列表

**功能描述**: 获取当前用户的历史会话列表，按时间倒序排列，用于智能问答页面左侧的会话历史展示。

**业务背景**: 用户可以查看和切换历史对话，继续之前的对话或回顾历史记录。

**接口地址**: `/api/chat/sessions`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 无

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "limit": "number, 返回数量限制，默认20"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| limit | number | 否 | 返回数量限制 | 20 |

**响应格式**: 
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    {
      "id": "string, 会话ID",
      "title": "string, 会话标题",
      "time": "string, 时间显示（如'今天 14:30'）",
      "createdAt": "string, 创建时间戳"
    }
  ]
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    {
      "id": "session_001",
      "title": "API设计最佳实践",
      "time": "今天 14:30",
      "createdAt": "2025-10-01T14:30:00Z"
    },
    {
      "id": "session_002",
      "title": "数据库连接池配置",
      "time": "今天 10:15",
      "createdAt": "2025-10-01T10:15:00Z"
    }
  ]
}
```

**前端调用示例**:
```javascript
/**
 * 获取会话历史列表
 * - 接口地址: /api/chat/sessions
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: Array<Session>
 */
export async function getSessionHistory(params = {}) {
  return await apiRequest('/api/chat/sessions', {
    method: 'POST',
    body: { limit: 20, ...params },
    needAuth: true
  });
}
```

**注意事项**:
- 会话按创建时间倒序排列
- time字段为前端友好的相对时间显示
- title字段通常为会话的第一条用户消息或自动生成的摘要

---

### 4.4 创建新会话

**功能描述**: 创建一个新的对话会话。

**业务背景**: 用户点击"新建对话"按钮时调用，开启新的问答会话。

**接口地址**: `/api/chat/session/create`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 无

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "knowledgeBaseId": "string, 知识库ID，'all'表示全部知识库",
  "modelId": "string, 模型ID"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| knowledgeBaseId | string | 是 | 知识库ID，"all"表示全部知识库 | "kb_001" |
| modelId | string | 是 | 模型ID | "qwen2-7b" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "创建成功",
  "body": {
    "id": "string, 会话ID",
    "title": "string, 会话标题",
    "createdAt": "string, 创建时间"
  }
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "创建成功",
  "body": {
    "id": "session_12345",
    "title": "新对话",
    "createdAt": "2025-10-01T15:20:00Z"
  }
}
```

**前端调用示例**:
```javascript
/**
 * 创建新会话
 * - 接口地址: /api/chat/session/create
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: {id, title, createdAt}
 */
export async function createSession(params) {
  return await apiRequest('/api/chat/session/create', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

---

### 4.5 发送消息

**功能描述**: 向指定会话发送用户问题，获取AI回答及引用来源。

**业务背景**: 用户在对话框中输入问题并发送时调用，实现智能问答的核心功能。

**接口地址**: `/api/chat/message/send`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 无

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "sessionId": "string, 会话ID",
  "question": "string, 用户问题",
  "knowledgeBaseId": "string, 知识库ID",
  "modelId": "string, 模型ID"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| sessionId | string | 是 | 会话ID | "session_001" |
| question | string | 是 | 用户问题，最大1000字符 | "如何设计RESTful API?" |
| knowledgeBaseId | string | 是 | 知识库ID | "kb_001" |
| modelId | string | 是 | 模型ID | "qwen2-7b" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "获取成功",
  "body": {
    "answer": "string, AI生成的回答",
    "references": [
      {
        "title": "string, 文档标题",
        "page": "number, 页码",
        "content": "string, 引用内容片段",
        "score": "number, 相关性得分(0-1)"
      }
    ]
  }
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "获取成功",
  "body": {
    "answer": "RESTful API 设计的最佳实践包括：\n\n1. 使用名词而非动词定义资源路径\n2. 使用HTTP方法表示操作\n3. 使用复数形式命名资源集合\n4. 提供适当的状态码\n\n详细内容请参考引用文档。",
    "references": [
      {
        "title": "API设计规范.pdf",
        "page": 12,
        "content": "RESTful API设计原则...",
        "score": 0.95
      },
      {
        "title": "架构最佳实践.pdf",
        "page": 34,
        "content": "HTTP方法使用指南...",
        "score": 0.88
      }
    ]
  }
}
```

**失败响应示例**:
```json
{
  "error": 3001,
  "message": "会话不存在",
  "body": {}
}
```

**前端调用示例**:
```javascript
/**
 * 发送消息
 * - 接口地址: /api/chat/message/send
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: {answer, references}
 */
export async function sendChatMessage(params) {
  return await apiRequest('/api/chat/message/send', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

**注意事项**:
- 问题长度限制1000字符
- 回答可能需要5-15秒，前端需显示加载状态
- references数组可能为空，表示未找到相关引用
- score表示引用与问题的相关性得分，越接近1越相关
- 建议前端实现流式显示（Server-Sent Events），MVP阶段可以一次性返回

---

### 4.6 获取会话消息列表

**功能描述**: 获取指定会话的所有历史消息，用于加载历史对话。

**业务背景**: 用户点击会话历史记录时，需要加载该会话的完整对话内容。

**接口地址**: `/api/chat/session/messages`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 无

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "sessionId": "string, 会话ID"
}
```

**响应格式**: 
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    {
      "id": "string, 消息ID",
      "role": "string, 角色: user-用户, assistant-助手",
      "content": "string, 消息内容",
      "references": "Array, 引用来源（仅assistant消息有）",
      "createdAt": "string, 创建时间"
    }
  ]
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    {
      "id": "msg_001",
      "role": "user",
      "content": "如何设计RESTful API?",
      "createdAt": "2025-10-01T14:30:00Z"
    },
    {
      "id": "msg_002",
      "role": "assistant",
      "content": "RESTful API 设计的最佳实践...",
      "references": [
        {
          "title": "API设计规范.pdf",
          "page": 12,
          "content": "...",
          "score": 0.95
        }
      ],
      "createdAt": "2025-10-01T14:30:05Z"
    }
  ]
}
```

**前端调用示例**:
```javascript
/**
 * 获取会话消息列表
 * - 接口地址: /api/chat/session/messages
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: Array<Message>
 */
export async function getSessionMessages(params) {
  return await apiRequest('/api/chat/session/messages', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

---

## 5. 搜索模块

*待补充:当生成搜索相关前端界面时,此部分将被填充*

---

## 6. 用户管理模块

*待补充:当生成用户管理相关前端界面时,此部分将被填充*

---

## 7. 模型管理模块

*待补充:当生成模型管理相关前端界面时,此部分将被填充*

---

## 8. 权限管理模块

*待补充:当生成权限管理相关前端界面时,此部分将被填充*

---

## 附录

### A. 错误码汇总

| 错误码 | 说明 | 处理方式 |
|--------|------|---------|
| 0 | 成功 | 正常处理业务逻辑 |
| 401 | 未登录或登录过期 | 跳转到登录页 |
| 403 | 权限不足 | 提示用户无权限 |
| 500 | 系统异常 | 弹出系统错误提示 |
| 1001 | 用户名或密码错误 | 提示用户检查输入 |
| 1002 | 账号已被禁用 | 提示联系管理员 |
| 1003 | 原密码错误 | 提示用户重新输入 |
| 1004 | 密码格式不符合要求 | 提示密码规则 |
| 2001 | 知识库不存在 | 提示知识库已删除或不存在 |
| 2002 | 知识库名称已存在 | 提示修改知识库名称 |
| 3001 | 会话不存在 | 提示会话已删除或不存在 |
| 3002 | 问题内容为空 | 提示输入问题 |
| 3003 | 问题长度超限 | 提示问题不能超过1000字符 |
| 3004 | 模型不可用 | 提示选择其他模型 |

*更多错误码将随着接口的增加而补充*

### B. 数据字典

#### 用户角色 (role)
- `user`: 普通用户
- `admin`: 管理员

#### 用户状态 (status)
- `active`: 正常
- `disabled`: 已禁用

#### 知识库可见范围 (visible)
- `all`: 所有用户可见
- `authorized`: 仅授权用户可见
- `private`: 私有(仅创建者可见)

#### 知识库状态 (status)
- `active`: 活跃(正常使用中)
- `processing`: 处理中(正在导入文档)
- `inactive`: 未激活(已创建但未使用)

#### 用户权限级别 (permission)
- `view`: 查看权限(可查看知识库和文档)
- `manage`: 管理权限(可上传/删除文档、修改配置)

*更多数据字典将随着功能开发而补充*

### C. 更新日志

| 日期 | 版本 | 更新内容 | 更新人 |
|------|------|---------|--------|
| 2025-10-01 | v1.0 | 初始化文档,添加用户认证模块接口 | AI Assistant |
| 2025-10-01 | v1.1 | 添加知识库管理模块接口(统计、列表、详情) | AI Assistant |
| 2025-10-01 | v1.2 | 添加RAG智能问答模块接口(会话、消息、模型) | AI Assistant |

---

**文档维护说明**:
- 每次前端新增或修改界面涉及 API 调用时,必须同步更新本文档
- 接口文档应包含完整的请求/响应示例和数据说明
- 保持文档与代码的一致性,确保后端可以直接参考实现

