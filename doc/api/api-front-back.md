# 前后端接口文档

> **版本**: v2.0 | **更新**: 2025-10-04 | **维护**: jiangqin

---

## 通用规范

### 请求格式
- **默认方法**: POST
- **Content-Type**: `application/json`
- **认证头**: `Authorization: Bearer {token}` (需要登录的接口)

### 响应格式
```json
{
  "error": 0,          // 0=成功, 401=未登录, 403=无权限, 500=系统错误, 其他=业务错误
  "message": "提示信息",
  "body": {}           // 业务数据
}
```

### 错误码
| 错误码 | 说明 | 处理方式 |
|--------|------|---------|
| 0 | 成功 | 正常处理 |
| 401 | 未登录或登录过期 | 跳转登录页 |
| 403 | 权限不足 | 提示无权限 |
| 500 | 系统异常 | 显示错误提示 |
| 1001-1004 | 认证相关错误 | 显示message |
| 2001-2004 | 知识库相关错误 | 显示message |
| 3001-3004 | 对话相关错误 | 显示message |
| 4001-4002 | 搜索相关错误 | 显示message |

---

## 1. 用户认证模块

### 1.1 用户登录
- **接口**: `POST /api/auth/login`
- **权限**: 无需登录

**请求参数:**
```json
{
  "username": "string, 用户名",
  "password": "string, 密码"
}
```

**响应数据:**
```json
{
  "token": "string, JWT令牌(24小时有效)",
  "user": {
    "id": "string",
    "username": "string",
    "name": "string",
    "role": "string, user|admin",
    "email": "string",
    "phone": "string"
  }
}
```

### 1.2 用户登出
- **接口**: `POST /api/auth/logout`
- **权限**: 需要登录
- **请求参数**: `{}`
- **响应数据**: `{}`

### 1.3 修改密码
- **接口**: `POST /api/auth/change-password`
- **权限**: 需要登录

**请求参数:**
```json
{
  "oldPassword": "string, 原密码",
  "newPassword": "string, 新密码(8-20位,含大小写字母和数字)"
}
```

### 1.4 重置密码
- **接口**: `POST /api/auth/reset-password`
- **权限**: 无需登录

**请求参数:**
```json
{
  "account": "string, 邮箱或手机号",
  "code": "string, 验证码",
  "newPassword": "string, 新密码"
}
```

---

## 2. 个人中心模块

### 2.1 获取个人信息
- **接口**: `POST /api/user/profile`
- **权限**: 需要登录
- **请求参数**: `{}`

**响应数据:**
```json
{
  "id": "string",
  "username": "string, 只读",
  "name": "string",
  "email": "string",
  "phone": "string, 脱敏显示",
  "department": "string",
  "position": "string",
  "avatar": "string, URL",
  "bio": "string, 最大200字符",
  "role": "string",
  "createdAt": "string",
  "lastLoginAt": "string"
}
```

### 2.2 更新个人信息
- **接口**: `POST /api/user/profile/update`
- **权限**: 需要登录

**请求参数:**
```json
{
  "name": "string, 必填",
  "email": "string, 必填",
  "phone": "string, 可选",
  "department": "string, 可选",
  "position": "string, 可选",
  "bio": "string, 可选,最大200字符"
}
```

### 2.3 上传头像
- **接口**: `POST /api/user/avatar/upload`
- **权限**: 需要登录
- **Content-Type**: `multipart/form-data`
- **请求参数**: `avatar: File (JPG/PNG, ≤2MB)`

**响应数据:**
```json
{
  "avatarUrl": "string, 新头像URL"
}
```

### 2.4 获取部门列表
- **接口**: `POST /api/user/departments`
- **权限**: 需要登录

**响应数据:**
```json
[
  { "value": "tech", "label": "技术部" },
  { "value": "product", "label": "产品部" }
]
```

### 2.5 获取登录记录
- **接口**: `POST /api/user/login-records`
- **权限**: 需要登录

**请求参数:**
```json
{
  "limit": "number, 可选,默认10,最大50"
}
```

**响应数据:**
```json
[
  {
    "id": "string",
    "device": "string",
    "ip": "string",
    "location": "string",
    "loginTime": "string",
    "status": "string, current|ended",
    "userAgent": "string"
  }
]
```

### 2.6 修改密码
- **接口**: `POST /api/user/change-password`
- **权限**: 需要登录

**请求参数:**
```json
{
  "currentPassword": "string",
  "newPassword": "string, 最少6位",
  "confirmPassword": "string"
}
```

---

## 3. 仪表板模块

### 3.1 获取统计数据
- **接口**: `POST /api/dashboard/stats`
- **权限**: admin

**响应数据:**
```json
{
  "todayQuestions": {
    "count": "number",
    "change": "number, 百分比",
    "changeType": "string, increase|decrease"
  },
  "searchCount": { "count": "number", "change": "number", "changeType": "string" },
  "knowledgeBaseCount": { "count": "number", "newCount": "number, 本周新增" },
  "documentCount": { "count": "number", "newCount": "number" }
}
```

### 3.2 获取系统状态
- **接口**: `POST /api/dashboard/system-status`
- **权限**: admin

**响应数据:**
```json
{
  "llmModel": {
    "name": "string",
    "description": "string",
    "status": "string, online|offline",
    "online": "number",
    "total": "number"
  },
  "vectorModel": { /* 同llmModel */ },
  "vectorDb": { "name": "string", "description": "string", "status": "string, normal|error" },
  "relationalDb": { /* 同vectorDb */ },
  "systemStatus": "string, normal|warning|error",
  "lastUpdate": "string"
}
```

### 3.3 刷新系统状态
- **接口**: `POST /api/dashboard/refresh-status`
- **权限**: admin
- **响应数据**: 同3.2

---

## 4. 知识库管理模块

### 4.1 获取知识库统计
- **接口**: `POST /api/knowledge-base/stats`
- **权限**: 需要登录

**响应数据:**
```json
{
  "accessibleKnowledgeBase": "number",
  "accessibleDocuments": "number",
  "todayQuestions": "number"
}
```

### 4.2 获取知识库列表
- **接口**: `POST /api/knowledge-base/list`
- **权限**: 需要登录

**请求参数:**
```json
{
  "page": "number, 可选,默认1",
  "pageSize": "number, 可选,默认20",
  "keyword": "string, 可选"
}
```

**响应数据:**
```json
[
  {
    "id": "string",
    "name": "string",
    "code": "string",
    "description": "string",
    "icon": "string",
    "iconColor": "string, CSS渐变",
    "documentCount": "number",
    "storageSize": "string",
    "lastUpdate": "string, 相对时间",
    "status": "string, active|processing|inactive",
    "progress": "number, 0-100",
    "viewers": "number",
    "tags": ["string"]
  }
]
```

### 4.3 获取知识库详情
- **接口**: `POST /api/knowledge-base/detail`
- **权限**: 对该知识库有查看权限

**请求参数:**
```json
{
  "id": "string, 知识库ID"
}
```

**响应数据:**
```json
{
  "id": "string",
  "name": "string",
  "code": "string",
  "description": "string",
  "visible": "string, all|authorized|private",
  "createdAt": "string",
  "createdBy": "string",
  "permission": "string, view|manage"
}
```

### 4.4 创建知识库(简化版)
- **接口**: `POST /api/knowledge-base/create`
- **权限**: admin

**请求参数:**
```json
{
  "name": "string",
  "code": "string",
  "description": "string",
  "visible": "string, all|authorized|private"
}
```

### 4.5 创建知识库(完整流程)
- **接口**: `POST /api/knowledge-base/create-full`
- **权限**: admin

**请求参数:**
```json
{
  "name": "string",
  "description": "string",
  "tags": ["string"],
  "dataSource": "string, upload|existing",
  "fileIds": ["string"], 
  "files": ["File"],
  "chunkMethod": "string, smart|length|page",
  "maxChunkLength": "number",
  "vectorModelId": "string",
  "similarityThreshold": "number, 0-1",
  "maxRecall": "number"
}
```

### 4.6 更新知识库
- **接口**: `POST /api/knowledge-base/update`
- **权限**: 对该知识库有管理权限

**请求参数:**
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "tags": ["string"],
  "similarityThreshold": "number, 0-1"
}
```

### 4.7 删除知识库
- **接口**: `POST /api/knowledge-base/delete`
- **权限**: admin

**请求参数:**
```json
{
  "id": "string"
}
```

### 4.8 获取文档列表
- **接口**: `POST /api/knowledge-base/documents`
- **权限**: 对该知识库有查看权限

**请求参数:**
```json
{
  "knowledgeBaseId": "string",
  "page": "number, 可选,默认1",
  "pageSize": "number, 可选,默认20"
}
```

**响应数据:**
```json
{
  "list": [
    {
      "id": "string",
      "name": "string",
      "fileName": "string",
      "size": "string",
      "uploadTime": "string",
      "tags": ["string"],
      "status": "string, processed|processing"
    }
  ],
  "total": "number",
  "page": "number",
  "pageSize": "number"
}
```

### 4.9 上传文档
- **接口**: `POST /api/knowledge-base/upload-document`
- **权限**: 对该知识库有管理权限
- **Content-Type**: `multipart/form-data`

**请求参数:**
- `knowledgeBaseId`: string
- `files`: File[] (最多50个,单个≤100MB)

**响应数据:**
```json
{
  "documentId": "string",
  "status": "string, processing"
}
```

### 4.10 删除文档
- **接口**: `POST /api/knowledge-base/delete-document`
- **权限**: 对该知识库有管理权限

**请求参数:**
```json
{
  "knowledgeBaseId": "string",
  "documentId": "string"
}
```

### 4.11 获取文档预览
- **接口**: `POST /api/knowledge-base/document-preview`
- **权限**: 对该文档所属知识库有查看权限

**请求参数:**
```json
{
  "documentId": "string"
}
```

**响应数据:**
```json
{
  "documentId": "string",
  "name": "string",
  "previewUrl": "string",
  "type": "string, pdf"
}
```

### 4.12 批量导出文档
- **接口**: `POST /api/knowledge-base/export-documents`
- **权限**: 对该知识库有查看权限

**请求参数:**
```json
{
  "knowledgeBaseId": "string",
  "documentIds": ["string"], 
}
```

**响应数据:**
```json
{
  "downloadUrl": "string",
  "fileName": "string",
  "expiresIn": "number, 秒,默认3600"
}
```

**注意**: 单次最多50个文档,总大小≤500MB

### 4.13 获取已上传文件列表
- **接口**: `POST /api/knowledge-base/uploaded-files`
- **权限**: admin

**请求参数:**
```json
{
  "keyword": "string, 可选",
  "page": "number, 可选,默认1",
  "pageSize": "number, 可选,默认20"
}
```

**响应数据:**
```json
{
  "list": [
    {
      "id": "string",
      "name": "string",
      "size": "string",
      "uploadTime": "string",
      "usedBy": ["string, 知识库名称"]
    }
  ],
  "total": "number",
  "page": "number",
  "pageSize": "number"
}
```

### 4.14 获取向量模型列表
- **接口**: `POST /api/knowledge-base/vector-models`
- **权限**: admin

**响应数据:**
```json
[
  {
    "id": "string",
    "name": "string",
    "description": "string",
    "dimension": "number"
  }
]
```

---

## 5. 智能问答模块

### 5.1 获取知识库列表(对话用)
- **接口**: `POST /api/chat/knowledge-bases`
- **权限**: 需要登录

**响应数据:**
```json
[
  { "id": "string", "name": "string" }
]
```

### 5.2 获取模型列表
- **接口**: `POST /api/chat/models`
- **权限**: 需要登录

**响应数据:**
```json
[
  {
    "id": "string",
    "name": "string",
    "description": "string"
  }
]
```

### 5.3 获取会话历史
- **接口**: `POST /api/chat/sessions`
- **权限**: 需要登录

**请求参数:**
```json
{
  "limit": "number, 可选,默认20"
}
```

**响应数据:**
```json
[
  {
    "id": "string",
    "title": "string",
    "time": "string, 如'今天 14:30'",
    "createdAt": "string"
  }
]
```

### 5.4 创建会话
- **接口**: `POST /api/chat/session/create`
- **权限**: 需要登录

**请求参数:**
```json
{
  "knowledgeBaseId": "string, 'all'表示全部",
  "modelId": "string"
}
```

**响应数据:**
```json
{
  "id": "string",
  "title": "string",
  "createdAt": "string"
}
```

### 5.5 发送消息
- **接口**: `POST /api/chat/message/send`
- **权限**: 需要登录

**请求参数:**
```json
{
  "sessionId": "string",
  "question": "string, 最大1000字符",
  "knowledgeBaseId": "string",
  "modelId": "string"
}
```

**响应数据:**
```json
{
  "answer": "string",
  "references": [
    {
      "title": "string",
      "page": "number",
      "content": "string",
      "score": "number, 0-1"
    }
  ]
}
```

### 5.6 获取会话消息
- **接口**: `POST /api/chat/session/messages`
- **权限**: 需要登录

**请求参数:**
```json
{
  "sessionId": "string"
}
```

**响应数据:**
```json
[
  {
    "id": "string",
    "role": "string, user|assistant",
    "content": "string",
    "references": ["..."], 
    "createdAt": "string"
  }
]
```

### 5.7 删除会话
- **接口**: `POST /api/chat/session/delete`
- **权限**: 需要登录

**请求参数:**
```json
{
  "sessionId": "string"
}
```

### 5.8 重命名会话
- **接口**: `POST /api/chat/session/rename`
- **权限**: 需要登录

**请求参数:**
```json
{
  "sessionId": "string",
  "title": "string"
}
```

---

## 6. 搜索模块

### 6.1 搜索文档
- **接口**: `POST /api/search/documents`
- **权限**: 需要登录

**请求参数:**
```json
{
  "keyword": "string, 必填",
  "knowledgeBaseId": "string, 可选,'all'表示全部",
  "docType": "string, 可选,'all'表示全部",
  "sortBy": "string, 可选,relevance|time|title",
  "page": "number, 可选,默认1",
  "pageSize": "number, 可选,默认10"
}
```

**响应数据:**
```json
{
  "list": [
    {
      "id": "string",
      "title": "string",
      "knowledgeBase": "string",
      "docType": "string",
      "excerpt": "string, 含<em>高亮标签",
      "score": "number, 0-1",
      "pageNumber": "number",
      "updateTime": "string",
      "size": "string"
    }
  ],
  "total": "number",
  "page": "number",
  "pageSize": "number"
}
```

### 6.2 获取热门关键词
- **接口**: `POST /api/search/hot-keywords`
- **权限**: 需要登录

**请求参数:**
```json
{
  "limit": "number, 可选,默认10,最大20"
}
```

**响应数据:**
```json
[
  { "keyword": "string", "count": "number" }
]
```

### 6.3 获取文档类型列表
- **接口**: `POST /api/search/doc-types`
- **权限**: 需要登录

**响应数据:**
```json
[
  { "value": "all", "label": "全部类型" },
  { "value": "pdf", "label": "PDF文档" }
]
```

### 6.4 导出搜索结果
- **接口**: `POST /api/search/export`
- **权限**: 需要登录

**请求参数:**
```json
{
  "keyword": "string",
  "knowledgeBaseId": "string, 可选",
  "docType": "string, 可选",
  "sortBy": "string, 可选"
}
```

**响应数据:**
```json
{
  "downloadUrl": "string",
  "fileName": "string",
  "expiresIn": "number, 秒,默认3600"
}
```

**注意**: 最多导出1000条记录,CSV格式,UTF-8编码

---

## 7. 用户管理模块

### 7.1 获取用户统计
- **接口**: `POST /api/admin/users/stats`
- **权限**: admin

**响应数据:**
```json
{
  "totalUsers": "number",
  "activeUsers": "number",
  "adminUsers": "number",
  "disabledUsers": "number"
}
```

### 7.2 获取用户列表
- **接口**: `POST /api/admin/users/list`
- **权限**: admin

**请求参数:**
```json
{
  "keyword": "string, 可选",
  "role": "string, 可选,admin|user",
  "status": "string, 可选,active|disabled",
  "page": "number, 可选,默认1",
  "pageSize": "number, 可选,默认10"
}
```

**响应数据:**
```json
{
  "list": [
    {
      "id": "string",
      "name": "string",
      "username": "string",
      "email": "string",
      "phone": "string, 脱敏",
      "role": "string, admin|user",
      "status": "string, active|disabled",
      "avatarColor": "string, CSS渐变",
      "lastLogin": "string",
      "createdAt": "string"
    }
  ],
  "total": "number",
  "page": "number",
  "pageSize": "number"
}
```

### 7.3 创建用户
- **接口**: `POST /api/admin/users/create`
- **权限**: admin

**请求参数:**
```json
{
  "name": "string",
  "username": "string, 唯一",
  "email": "string",
  "phone": "string, 11位",
  "role": "string, admin|user",
  "password": "string, 最少6位"
}
```

### 7.4 更新用户
- **接口**: `POST /api/admin/users/update`
- **权限**: admin

**请求参数:**
```json
{
  "id": "string",
  "name": "string",
  "email": "string",
  "phone": "string",
  "role": "string"
}
```

### 7.5 删除用户
- **接口**: `POST /api/admin/users/delete`
- **权限**: admin

**请求参数:**
```json
{
  "userId": "string"
}
```

**注意**: 不可删除当前登录管理员

### 7.6 切换用户状态
- **接口**: `POST /api/admin/users/toggle-status`
- **权限**: admin

**请求参数:**
```json
{
  "userId": "string",
  "status": "string, active|disabled"
}
```

### 7.7 重置用户密码
- **接口**: `POST /api/admin/users/reset-password`
- **权限**: admin

**请求参数:**
```json
{
  "userId": "string"
}
```

**响应数据:**
```json
{
  "newPassword": "string, 明文,仅此次返回"
}
```

### 7.8 导出用户列表
- **接口**: `POST /api/admin/users/export`
- **权限**: admin

**请求参数:**
```json
{
  "keyword": "string, 可选",
  "role": "string, 可选",
  "status": "string, 可选"
}
```

**响应数据:**
```json
{
  "downloadUrl": "string",
  "fileName": "string",
  "expiresIn": "number, 秒,默认3600"
}
```

**注意**: CSV格式,UTF-8编码,手机号保持脱敏

---

## 8. 模型管理模块

### 8.1 获取模型统计
- **接口**: `GET /api/models/stats`
- **权限**: admin

**响应数据:**
```json
{
  "llmCount": "number",
  "embeddingCount": "number",
  "onlineCount": "number",
  "offlineCount": "number"
}
```

### 8.2 获取模型列表
- **接口**: `POST /api/models/list`
- **权限**: admin

**请求参数:**
```json
{
  "type": "string, 可选,llm|embedding|all",
  "status": "string, 可选,online|offline|all",
  "page": "number, 可选,默认1",
  "pageSize": "number, 可选,默认20"
}
```

**响应数据:**
```json
{
  "total": "number",
  "list": [
    {
      "id": "string",
      "name": "string",
      "type": "string, llm|embedding",
      "description": "string",
      "provider": "string",
      "status": "string, online|offline|error",
      "isDefault": "boolean",
      "modelSize": "string",
      "contextLength": "number",
      "latency": "string",
      "gpuMemory": "string",
      "endpoint": "string",
      "config": {
        "temperature": "number",
        "topP": "number",
        "topK": "number",
        "maxTokens": "number"
      },
      "healthCheck": {
        "lastCheckTime": "string",
        "responseTime": "number, ms",
        "status": "string",
        "message": "string"
      },
      "createdAt": "string",
      "updatedAt": "string"
    }
  ]
}
```

### 8.3 获取模型详情
- **接口**: `POST /api/models/detail`
- **权限**: admin

**请求参数:**
```json
{
  "id": "string"
}
```

**响应数据**: 同8.2中的单个模型对象

### 8.4 创建模型
- **接口**: `POST /api/models/create`
- **权限**: admin

**请求参数:**
```json
{
  "name": "string, 唯一",
  "type": "string, llm|embedding",
  "description": "string, 可选",
  "provider": "string",
  "endpoint": "string, URL",
  "modelSize": "string, 可选",
  "contextLength": "number, 可选",
  "gpuMemory": "string, 可选",
  "config": {
    "temperature": "number",
    "topP": "number",
    "topK": "number",
    "maxTokens": "number"
  }
}
```

**注意**: 创建后自动执行一次健康检查

### 8.5 更新模型
- **接口**: `POST /api/models/update`
- **权限**: admin

**请求参数:**
```json
{
  "id": "string",
  "name": "string, 可选",
  "description": "string, 可选",
  "endpoint": "string, 可选",
  "config": { /* 部分更新 */ }
}
```

**注意**: type创建后不可修改,更新后自动触发健康检查

### 8.6 删除模型
- **接口**: `POST /api/models/delete`
- **权限**: admin

**请求参数:**
```json
{
  "id": "string"
}
```

**注意**: 默认模型和正在使用的模型不可删除

### 8.7 设置默认模型
- **接口**: `POST /api/models/set-default`
- **权限**: admin

**请求参数:**
```json
{
  "id": "string",
  "type": "string, llm|embedding"
}
```

**注意**: 每种类型只能有一个默认模型,离线状态不可设为默认

### 8.8 测试模型连接
- **接口**: `POST /api/models/test`
- **权限**: admin

**请求参数:**
```json
{
  "id": "string"
}
```

**响应数据:**
```json
{
  "status": "string, online|offline|error",
  "responseTime": "number, ms",
  "message": "string",
  "timestamp": "string"
}
```

**注意**: 超时时间10秒

### 8.9 批量健康检查
- **接口**: `POST /api/models/health-check`
- **权限**: admin

**响应数据:**
```json
{
  "total": "number",
  "success": "number",
  "failed": "number",
  "results": [
    {
      "id": "string",
      "name": "string",
      "status": "string",
      "responseTime": "number",
      "message": "string"
    }
  ]
}
```

### 8.10 更新模型状态
- **接口**: `POST /api/models/update-status`
- **权限**: admin

**请求参数:**
```json
{
  "id": "string",
  "status": "string, online|offline"
}
```

**注意**: 手动设置的状态会被下次健康检查覆盖

---

## 附录

### 数据字典

**用户角色 (role)**
- `user`: 普通用户
- `admin`: 管理员

**用户状态 (status)**
- `active`: 正常
- `disabled`: 已禁用

**知识库可见范围 (visible)**
- `all`: 所有用户可见
- `authorized`: 仅授权用户可见
- `private`: 私有

**知识库状态 (status)**
- `active`: 活跃
- `processing`: 处理中
- `inactive`: 未激活

**文档处理状态**
- `processed`: 已处理
- `processing`: 处理中

**模型类型 (type)**
- `llm`: 大语言模型
- `embedding`: 向量模型

**模型状态 (status)**
- `online`: 在线
- `offline`: 离线
- `error`: 错误

**系统状态 (systemStatus)**
- `normal`: 正常
- `warning`: 警告
- `error`: 错误

---

**更新日志**

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2025-10-04 | v2.0 | 精简文档,优化格式 |
| 2025-10-01 | v1.0 | 初始版本 |

