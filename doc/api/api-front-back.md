# 前后端接口文档

> **文档说明**: 本文档汇总所有前端需要调用的后端接口,供后端开发参考实现。
> 
> **更新日期**: 2025-10-01  
> **版本**: v1.0  
> **维护者**: 前端开发团队

---

## 目录

- [1. 用户认证模块](#1-用户认证模块)
- [2. 个人中心模块](#2-个人中心模块)
- [3. 仪表板模块](#3-仪表板模块)
- [4. 知识库管理模块](#4-知识库管理模块)
- [5. 文档管理模块](#5-文档管理模块)
- [6. 智能问答模块](#6-智能问答模块)
- [7. 搜索模块](#7-搜索模块)
- [8. 用户管理模块](#8-用户管理模块)
- [9. 模型管理模块](#9-模型管理模块)
- [10. 权限管理模块](#10-权限管理模块)

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

## 2. 个人中心模块

### 2.1 获取个人信息

**功能描述**: 获取当前登录用户的详细个人信息，包括基本资料、联系方式、头像等，用于个人设置页面展示。

**业务背景**: 用户访问个人设置页面时需要展示当前用户的详细信息，包括可编辑和只读的字段。

**接口地址**: `/api/user/profile`

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
    "id": "string, 用户ID",
    "username": "string, 用户名（不可修改）",
    "name": "string, 真实姓名",
    "email": "string, 邮箱地址",
    "phone": "string, 手机号码",
    "department": "string, 部门代码",
    "position": "string, 职位",
    "avatar": "string, 头像URL",
    "bio": "string, 个人简介",
    "role": "string, 用户角色",
    "createdAt": "string, 注册时间",
    "lastLoginAt": "string, 最后登录时间"
  }
}
```

**Body 数据结构说明**:
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| id | string | 用户唯一标识 | "user_001" |
| username | string | 用户名（只读） | "zhangsan" |
| name | string | 真实姓名 | "张三" |
| email | string | 邮箱地址 | "zhangsan@company.com" |
| phone | string | 手机号码（脱敏显示） | "138****1234" |
| department | string | 部门代码 | "tech" |
| position | string | 职位 | "高级工程师" |
| avatar | string | 头像URL，空值表示使用默认头像 | "/avatars/user-avatar.png" |
| bio | string | 个人简介 | "专注于后端开发和系统架构设计" |
| role | string | 用户角色 | "user" |
| createdAt | string | 账号注册时间 | "2024-01-15T08:30:00Z" |
| lastLoginAt | string | 最后登录时间 | "2024-09-25T09:30:00Z" |

**请求示例**:
```
POST /api/user/profile
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
    "id": "user_001",
    "username": "zhangsan",
    "name": "张三",
    "email": "zhangsan@company.com",
    "phone": "138****1234",
    "department": "tech",
    "position": "高级工程师",
    "avatar": "/avatars/default-avatar.png",
    "bio": "专注于后端开发和系统架构设计，有多年互联网开发经验。",
    "role": "user",
    "createdAt": "2024-01-15T08:30:00Z",
    "lastLoginAt": "2024-09-25T09:30:00Z"
  }
}
```

**前端调用示例**:
```javascript
/**
 * 获取个人信息
 * - 接口地址: /api/user/profile
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: UserProfile对象
 */
export async function getUserProfile() {
  return await apiRequest('/api/user/profile', {
    method: 'POST',
    body: {},
    needAuth: true
  });
}
```

**注意事项**:
- 手机号码在返回时进行脱敏处理
- avatar字段为空时前端使用默认头像
- 个人简介最大长度200字符

---

### 2.2 更新个人信息

**功能描述**: 更新用户的基本信息，如姓名、邮箱、手机、部门、职位、个人简介等可编辑字段。

**业务背景**: 用户在个人设置页面修改基本信息时调用。

**接口地址**: `/api/user/profile/update`

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
  "name": "string, 真实姓名",
  "email": "string, 邮箱地址",
  "phone": "string, 手机号码",
  "department": "string, 部门代码",
  "position": "string, 职位",
  "bio": "string, 个人简介，最大200字符"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| name | string | 是 | 真实姓名，2-20字符 | "张三" |
| email | string | 是 | 邮箱地址，需符合邮箱格式 | "zhangsan@company.com" |
| phone | string | 否 | 手机号码，11位数字 | "13800138000" |
| department | string | 否 | 部门代码 | "tech" |
| position | string | 否 | 职位名称 | "高级工程师" |
| bio | string | 否 | 个人简介，最大200字符 | "专注于后端开发..." |

**响应格式**: 
```json
{
  "error": 0,
  "message": "更新成功",
  "body": {
    "id": "string, 用户ID",
    "name": "string, 更新后的姓名",
    "email": "string, 更新后的邮箱",
    "phone": "string, 更新后的手机号",
    "department": "string, 更新后的部门",
    "position": "string, 更新后的职位",
    "bio": "string, 更新后的个人简介",
    "updatedAt": "string, 更新时间"
  }
}
```

**请求示例**:
```
POST /api/user/profile/update
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "name": "张三",
  "email": "zhangsan@company.com",
  "phone": "13800138000",
  "department": "tech",
  "position": "高级工程师",
  "bio": "专注于后端开发和系统架构设计，有多年互联网开发经验。"
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "更新成功",
  "body": {
    "id": "user_001",
    "name": "张三",
    "email": "zhangsan@company.com",
    "phone": "138****1234",
    "department": "tech",
    "position": "高级工程师",
    "bio": "专注于后端开发和系统架构设计，有多年互联网开发经验。",
    "updatedAt": "2025-10-01T15:30:00Z"
  }
}
```

**失败响应示例**:
```json
{
  "error": 5001,
  "message": "邮箱格式不正确",
  "body": {}
}
```

```json
{
  "error": 5002,
  "message": "手机号码格式不正确",
  "body": {}
}
```

**前端调用示例**:
```javascript
/**
 * 更新个人信息
 * - 接口地址: /api/user/profile/update
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: 更新后的用户信息
 */
export async function updateUserProfile(params) {
  return await apiRequest('/api/user/profile/update', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

**注意事项**:
- 邮箱和姓名为必填字段
- 手机号码需要11位数字格式验证
- 个人简介最大长度200字符
- 部门代码需要在有效的部门列表中

---

### 2.3 上传头像

**功能描述**: 上传用户头像图片，支持JPG、PNG格式，文件大小不超过2MB。

**业务背景**: 用户在个人设置页面更换头像时调用。

**接口地址**: `/api/user/avatar/upload`

**请求方法**: POST

**需要登录**: 是

**需要权限**: 无

**请求头 (Headers)**:
```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**请求体 (Body)**:
FormData格式，包含以下字段：
- `avatar`: File对象，头像文件

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 限制 |
|--------|------|------|------|------|
| avatar | File | 是 | 头像文件 | JPG/PNG格式，≤2MB |

**响应格式**: 
```json
{
  "error": 0,
  "message": "头像上传成功",
  "body": {
    "avatarUrl": "string, 新头像URL"
  }
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "头像上传成功",
  "body": {
    "avatarUrl": "/avatars/user-avatar-1696156800000.png"
  }
}
```

**失败响应示例**:
```json
{
  "error": 5003,
  "message": "文件大小不能超过2MB",
  "body": {}
}
```

```json
{
  "error": 5004,
  "message": "仅支持JPG、PNG格式的图片",
  "body": {}
}
```

**前端调用示例**:
```javascript
/**
 * 上传头像
 * - 接口地址: /api/user/avatar/upload
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: {avatarUrl}
 */
export async function uploadUserAvatar(file) {
  const formData = new FormData();
  formData.append('avatar', file);
  
  return await apiRequest('/api/user/avatar/upload', {
    method: 'POST',
    body: formData,
    needAuth: true,
    headers: {} // FormData会自动设置Content-Type
  });
}
```

**注意事项**:
- 支持的图片格式：JPG、JPEG、PNG
- 文件大小限制：2MB
- 上传成功后返回新的头像URL
- 旧头像文件会被自动清理

---

### 2.4 获取部门列表

**功能描述**: 获取公司部门列表，用于个人信息编辑时的部门选择下拉框。

**业务背景**: 用户在编辑个人信息时需要选择所属部门。

**接口地址**: `/api/user/departments`

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
      "value": "string, 部门代码",
      "label": "string, 部门名称"
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
    { "value": "tech", "label": "技术部" },
    { "value": "product", "label": "产品部" },
    { "value": "design", "label": "设计部" },
    { "value": "marketing", "label": "市场部" },
    { "value": "sales", "label": "销售部" },
    { "value": "hr", "label": "人力资源部" },
    { "value": "finance", "label": "财务部" },
    { "value": "admin", "label": "行政部" }
  ]
}
```

**前端调用示例**:
```javascript
/**
 * 获取部门列表
 * - 接口地址: /api/user/departments
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: Array<{value, label}>
 */
export async function getDepartmentList() {
  return await apiRequest('/api/user/departments', {
    method: 'POST',
    body: {},
    needAuth: true
  });
}
```

---

### 2.5 获取登录记录

**功能描述**: 获取用户最近的登录记录，包括设备信息、IP地址、登录时间等，用于安全设置页面展示。

**业务背景**: 用户可以查看自己账号的登录历史，及时发现异常登录行为。

**接口地址**: `/api/user/login-records`

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
  "limit": "number, 返回数量，默认10"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| limit | number | 否 | 返回数量，默认10，最大50 | 10 |

**响应格式**: 
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    {
      "id": "string, 记录ID",
      "device": "string, 设备信息",
      "ip": "string, IP地址",
      "location": "string, 登录地点",
      "loginTime": "string, 登录时间",
      "status": "string, 状态: current-当前会话, ended-已结束",
      "userAgent": "string, 浏览器标识"
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
      "id": "login_001",
      "device": "Windows Chrome",
      "ip": "192.168.1.100",
      "location": "北京",
      "loginTime": "2024-09-25T09:30:00Z",
      "status": "current",
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    },
    {
      "id": "login_002",
      "device": "iPhone Safari",
      "ip": "192.168.1.101",
      "location": "北京",
      "loginTime": "2024-09-24T18:45:00Z",
      "status": "ended",
      "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
    }
  ]
}
```

**前端调用示例**:
```javascript
/**
 * 获取登录记录
 * - 接口地址: /api/user/login-records
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: Array<LoginRecord>
 */
export async function getLoginRecords(params = {}) {
  return await apiRequest('/api/user/login-records', {
    method: 'POST',
    body: { limit: 10, ...params },
    needAuth: true
  });
}
```

**注意事项**:
- 记录按登录时间倒序排列
- status为current的表示当前活跃会话
- location基于IP地址解析，可能不完全准确
- device信息从User-Agent解析获得

---

### 2.6 修改密码（个人中心）

**功能描述**: 在个人中心页面修改密码，需要验证当前密码。

**业务背景**: 用户在安全设置页面主动修改密码，增强账号安全性。

**接口地址**: `/api/user/change-password`

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
  "currentPassword": "string, 当前密码",
  "newPassword": "string, 新密码",
  "confirmPassword": "string, 确认新密码"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| currentPassword | string | 是 | 当前密码 | "OldPass@123" |
| newPassword | string | 是 | 新密码，8-20位，包含大小写字母和数字 | "NewPass@456" |
| confirmPassword | string | 是 | 确认新密码，需与newPassword一致 | "NewPass@456" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "密码修改成功",
  "body": {}
}
```

**请求示例**:
```
POST /api/user/change-password
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "currentPassword": "OldPass@123",
  "newPassword": "NewPass@456",
  "confirmPassword": "NewPass@456"
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "密码修改成功",
  "body": {}
}
```

**失败响应示例**:
```json
{
  "error": 5005,
  "message": "当前密码错误",
  "body": {}
}
```

```json
{
  "error": 5006,
  "message": "新密码和确认密码不一致",
  "body": {}
}
```

```json
{
  "error": 5007,
  "message": "密码长度不能少于6位",
  "body": {}
}
```

**前端调用示例**:
```javascript
/**
 * 修改密码（个人中心）
 * - 接口地址: /api/user/change-password
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: 修改结果
 */
export async function changeUserPassword(params) {
  return await apiRequest('/api/user/change-password', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

**注意事项**:
- 密码强度要求：最少6位，建议8-20位并包含大小写字母、数字
- 新密码和确认密码必须一致
- 修改成功后用户无需重新登录（与认证模块的修改密码接口不同）
- 新密码不能与最近3次使用过的密码相同

---

## 3. 仪表板模块

### 3.1 获取仪表板统计数据

**功能描述**: 获取管理员仪表板首页的关键统计指标，包括今日问答、搜索次数、知识库数量、文档总数等核心数据及其变化趋势。

**业务背景**: 管理员登录后进入仪表板，需要一目了然地查看系统整体运行情况和关键指标，帮助管理员快速了解系统使用状况。

**接口地址**: `/api/dashboard/stats`

**请求方法**: POST

**需要登录**: 是

**需要权限**: admin

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
    "todayQuestions": {
      "count": "number, 今日问答次数",
      "change": "number, 变化百分比",
      "changeType": "string, 变化类型: increase/decrease"
    },
    "searchCount": {
      "count": "number, 搜索次数",
      "change": "number, 变化百分比",
      "changeType": "string, 变化类型"
    },
    "knowledgeBaseCount": {
      "count": "number, 知识库数量",
      "newCount": "number, 本周新增数量"
    },
    "documentCount": {
      "count": "number, 文档总数",
      "newCount": "number, 本周新增数量"
    }
  }
}
```

**Body 数据结构说明**:
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| todayQuestions.count | number | 今日系统问答总次数 | 156 |
| todayQuestions.change | number | 较昨日变化百分比 | 12 |
| todayQuestions.changeType | string | 变化类型 | "increase" |
| searchCount.count | number | 今日搜索总次数 | 89 |
| searchCount.change | number | 较昨日变化百分比 | 8 |
| knowledgeBaseCount.count | number | 系统知识库总数 | 12 |
| knowledgeBaseCount.newCount | number | 本周新增知识库数 | 2 |
| documentCount.count | number | 系统文档总数 | 1234 |
| documentCount.newCount | number | 本周新增文档数 | 15 |

**请求示例**:
```
POST /api/dashboard/stats
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
    "todayQuestions": {
      "count": 156,
      "change": 12,
      "changeType": "increase"
    },
    "searchCount": {
      "count": 89,
      "change": 8,
      "changeType": "increase"
    },
    "knowledgeBaseCount": {
      "count": 12,
      "newCount": 2
    },
    "documentCount": {
      "count": 1234,
      "newCount": 15
    }
  }
}
```

**前端调用示例**:
```javascript
/**
 * 获取仪表板统计数据
 * - 接口地址: /api/dashboard/stats
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 返回值: 统计数据对象
 */
export async function getDashboardStats() {
  return await apiRequest('/api/dashboard/stats', {
    method: 'POST',
    body: {},
    needAuth: true
  });
}
```

**注意事项**:
- 仅管理员可访问此接口
- 统计数据实时计算，可能有1-2分钟延迟
- changeType 仅有 increase/decrease 两种值
- change 为正数表示增长，负数表示下降

---

### 3.2 获取系统状态

**功能描述**: 获取系统各个服务的运行状态，包括LLM模型、向量模型、向量数据库、关系数据库等核心服务的在线状态和健康情况。

**业务背景**: 管理员需要实时监控系统各个服务的运行状态，及时发现和处理服务异常，确保系统稳定运行。

**接口地址**: `/api/dashboard/system-status`

**请求方法**: POST

**需要登录**: 是

**需要权限**: admin

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
  "body": {
    "llmModel": {
      "name": "string, 服务名称",
      "description": "string, 服务描述",
      "status": "string, 状态: online/offline",
      "online": "number, 在线数量",
      "total": "number, 总数量"
    },
    "vectorModel": {
      "name": "string, 服务名称",
      "description": "string, 服务描述",
      "status": "string, 状态",
      "online": "number, 在线数量",
      "total": "number, 总数量"
    },
    "vectorDb": {
      "name": "string, 服务名称",
      "description": "string, 服务描述",
      "status": "string, 状态: normal/error"
    },
    "relationalDb": {
      "name": "string, 服务名称",
      "description": "string, 服务描述",
      "status": "string, 状态"
    },
    "systemStatus": "string, 系统整体状态: normal/warning/error",
    "lastUpdate": "string, 最后更新时间"
  }
}
```

**Body 数据结构说明**:
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| llmModel.name | string | LLM模型服务名称 | "LLM 模型" |
| llmModel.description | string | 服务描述 | "大语言模型服务" |
| llmModel.status | string | 服务状态 | "online" |
| llmModel.online | number | 在线实例数 | 3 |
| llmModel.total | number | 总实例数 | 3 |
| vectorModel | object | 向量模型服务信息，字段同llmModel | - |
| vectorDb.name | string | 向量数据库服务名称 | "向量数据库" |
| vectorDb.status | string | 服务状态 | "normal" |
| relationalDb | object | 关系数据库服务信息，字段同vectorDb | - |
| systemStatus | string | 系统整体状态 | "normal" |
| lastUpdate | string | 最后更新时间 | "刚刚" |

**请求示例**:
```
POST /api/dashboard/system-status
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
    "llmModel": {
      "name": "LLM 模型",
      "description": "大语言模型服务",
      "status": "online",
      "online": 3,
      "total": 3
    },
    "vectorModel": {
      "name": "向量模型",
      "description": "嵌入向量服务",
      "status": "online",
      "online": 2,
      "total": 2
    },
    "vectorDb": {
      "name": "向量数据库",
      "description": "向量存储服务",
      "status": "normal"
    },
    "relationalDb": {
      "name": "关系数据库",
      "description": "业务数据存储",
      "status": "normal"
    },
    "systemStatus": "normal",
    "lastUpdate": "刚刚"
  }
}
```

**失败响应示例**:
```json
{
  "error": 403,
  "message": "权限不足，仅管理员可访问",
  "body": {}
}
```

**前端调用示例**:
```javascript
/**
 * 获取系统状态
 * - 接口地址: /api/dashboard/system-status
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 返回值: 系统状态对象
 */
export async function getSystemStatus() {
  return await apiRequest('/api/dashboard/system-status', {
    method: 'POST',
    body: {},
    needAuth: true
  });
}
```

**注意事项**:
- 仅管理员可访问此接口
- status 值: online-在线, offline-离线, normal-正常, error-错误
- systemStatus 为 error 时应进行告警提示
- lastUpdate 为前端友好的相对时间显示

---

### 3.3 刷新系统状态

**功能描述**: 手动触发刷新系统状态检查，获取最新的服务运行情况。

**业务背景**: 管理员发现系统状态异常时，可以手动刷新获取最新状态，或定期刷新监控系统健康。

**接口地址**: `/api/dashboard/refresh-status`

**请求方法**: POST

**需要登录**: 是

**需要权限**: admin

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
同 3.2 获取系统状态接口的响应格式

**请求示例**:
```
POST /api/dashboard/refresh-status
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "刷新成功",
  "body": {
    "llmModel": {
      "name": "LLM 模型",
      "description": "大语言模型服务",
      "status": "online",
      "online": 3,
      "total": 3
    },
    "vectorModel": {
      "name": "向量模型",
      "description": "嵌入向量服务",
      "status": "online",
      "online": 2,
      "total": 2
    },
    "vectorDb": {
      "name": "向量数据库",
      "description": "向量存储服务",
      "status": "normal"
    },
    "relationalDb": {
      "name": "关系数据库",
      "description": "业务数据存储",
      "status": "normal"
    },
    "systemStatus": "normal",
    "lastUpdate": "刚刚"
  }
}
```

**前端调用示例**:
```javascript
/**
 * 刷新系统状态
 * - 接口地址: /api/dashboard/refresh-status
 * - 方法: POST
 * - 需要登录: 是
 * - 需要权限: admin
 * - 返回值: 刷新后的系统状态
 */
export async function refreshSystemStatus() {
  return await apiRequest('/api/dashboard/refresh-status', {
    method: 'POST',
    body: {},
    needAuth: true
  });
}
```

**注意事项**:
- 仅管理员可访问此接口
- 刷新操作会触发所有服务的健康检查
- 避免频繁调用，建议间隔至少10秒
- 刷新可能需要2-3秒完成

---

## 4. 知识库管理模块

### 4.1 获取知识库统计数据

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

### 4.2 获取知识库列表

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

### 4.3 获取知识库详情

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

## 5. 文档管理模块

*待补充:当生成文档管理相关前端界面时,此部分将被填充*

---

## 6. 智能问答模块

### 6.1 获取知识库列表（对话页面）

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

### 6.2 获取可用模型列表

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

### 6.3 获取会话历史列表

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

### 6.4 创建新会话

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

### 6.5 发送消息

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

### 6.6 获取会话消息列表

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

## 7. 搜索模块

### 7.1 搜索文档

**功能描述**: 在知识库中搜索文档内容，支持关键词搜索和向量检索，返回相关文档列表及高亮摘要。

**业务背景**: 用户需要快速查找知识库中的特定文档或技术内容，通过关键词搜索能够精准定位到相关文档和段落。

**接口地址**: `/api/search/documents`

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
  "keyword": "string, 搜索关键词",
  "knowledgeBaseId": "string, 知识库ID，'all'表示全部知识库",
  "docType": "string, 文档类型，'all'表示全部类型",
  "sortBy": "string, 排序方式: relevance-相关度, time-时间, title-标题",
  "page": "number, 页码，从1开始，默认1",
  "pageSize": "number, 每页数量，默认10"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| keyword | string | 是 | 搜索关键词 | "API设计" |
| knowledgeBaseId | string | 否 | 知识库ID，"all"表示全部知识库 | "kb_001" |
| docType | string | 否 | 文档类型，"all"表示全部类型 | "pdf" |
| sortBy | string | 否 | 排序方式 | "relevance" |
| page | number | 否 | 页码 | 1 |
| pageSize | number | 否 | 每页数量 | 10 |

**响应格式**: 
```json
{
  "error": 0,
  "message": "搜索成功",
  "body": {
    "list": [
      {
        "id": "string, 文档ID",
        "title": "string, 文档标题",
        "knowledgeBase": "string, 所属知识库名称",
        "docType": "string, 文档类型",
        "excerpt": "string, 摘要片段（带HTML高亮标签<em>）",
        "score": "number, 相关性得分(0-1)",
        "pageNumber": "number, 页码",
        "updateTime": "string, 更新时间",
        "size": "string, 文件大小"
      }
    ],
    "total": "number, 总数",
    "page": "number, 当前页码",
    "pageSize": "number, 每页数量"
  }
}
```

**Body 数据结构说明**:
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| list | Array | 文档列表 | - |
| list[].id | string | 文档唯一标识 | "doc_001" |
| list[].title | string | 文档标题 | "RESTful API设计规范v2.0.pdf" |
| list[].knowledgeBase | string | 所属知识库 | "技术规范库" |
| list[].docType | string | 文档类型 | "PDF" |
| list[].excerpt | string | 摘要片段，关键词用`<em>`标签高亮 | "...完整的<em>API设计</em>规范..." |
| list[].score | number | 相关性得分 | 0.95 |
| list[].pageNumber | number | 文档页码 | 12 |
| list[].updateTime | string | 更新时间 | "2025-09-28" |
| list[].size | string | 文件大小 | "2.3 MB" |
| total | number | 符合条件的总记录数 | 8 |
| page | number | 当前页码 | 1 |
| pageSize | number | 每页数量 | 10 |

**请求示例**:
```
POST /api/search/documents
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "keyword": "API设计",
  "knowledgeBaseId": "all",
  "docType": "all",
  "sortBy": "relevance",
  "page": 1,
  "pageSize": 10
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "搜索成功",
  "body": {
    "list": [
      {
        "id": "doc_001",
        "title": "RESTful API设计规范v2.0.pdf",
        "knowledgeBase": "技术规范库",
        "docType": "PDF",
        "excerpt": "...完整的<em>API设计</em>规范文档，包括命名规则、HTTP方法使用、状态码定义等内容...",
        "score": 0.95,
        "pageNumber": 12,
        "updateTime": "2025-09-28",
        "size": "2.3 MB"
      },
      {
        "id": "doc_002",
        "title": "数据库连接池配置指南.pdf",
        "knowledgeBase": "技术规范库",
        "docType": "PDF",
        "excerpt": "...详细介绍了数据库连接池的配置方法和<em>API</em>调用示例...",
        "score": 0.88,
        "pageNumber": 23,
        "updateTime": "2025-09-25",
        "size": "1.8 MB"
      }
    ],
    "total": 8,
    "page": 1,
    "pageSize": 10
  }
}
```

**失败响应示例**:
```json
{
  "error": 4001,
  "message": "搜索关键词不能为空",
  "body": {
    "list": [],
    "total": 0,
    "page": 1,
    "pageSize": 10
  }
}
```

**前端调用示例**:
```javascript
/**
 * 搜索文档
 * - 接口地址: /api/search/documents
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: {list, total, page, pageSize}
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
  });
}
```

**注意事项**:
- 搜索结果中的excerpt字段包含HTML标签`<em>`用于高亮关键词
- score表示文档与关键词的相关性得分，越接近1越相关
- 搜索默认在用户有权访问的知识库范围内进行
- 支持分页，单次最多返回100条结果
- 搜索结果按相关度、时间或标题排序

---

### 7.2 获取热门搜索关键词

**功能描述**: 获取系统中的热门搜索关键词列表，基于搜索频率统计，用于搜索页面的热门搜索标签展示。

**业务背景**: 为用户提供搜索建议，展示系统中常见的搜索关键词，帮助用户快速找到常用内容。

**接口地址**: `/api/search/hot-keywords`

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
  "limit": "number, 返回数量，默认10"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| limit | number | 否 | 返回数量，默认10，最大20 | 10 |

**响应格式**: 
```json
{
  "error": 0,
  "message": "获取成功",
  "body": [
    {
      "keyword": "string, 关键词",
      "count": "number, 搜索次数"
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
    { "keyword": "API设计规范", "count": 156 },
    { "keyword": "数据库连接池", "count": 132 },
    { "keyword": "Redis缓存", "count": 128 },
    { "keyword": "微服务架构", "count": 115 },
    { "keyword": "性能优化", "count": 98 }
  ]
}
```

**前端调用示例**:
```javascript
/**
 * 获取热门搜索关键词
 * - 接口地址: /api/search/hot-keywords
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: Array<{keyword, count}>
 */
export async function getHotKeywords(params = {}) {
  return await apiRequest('/api/search/hot-keywords', {
    method: 'POST',
    body: { limit: 10, ...params },
    needAuth: true
  });
}
```

**注意事项**:
- 热门关键词基于最近30天的搜索统计
- 按搜索次数降序排列
- 统计数据每小时更新一次

---

### 7.3 获取文档类型列表

**功能描述**: 获取系统支持的文档类型列表，用于搜索页面筛选器的文档类型下拉选择。

**业务背景**: 用户可以根据文档类型筛选搜索结果，快速找到特定格式的文档。

**接口地址**: `/api/search/doc-types`

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
      "value": "string, 类型值",
      "label": "string, 类型显示名称"
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
    { "value": "all", "label": "全部类型" },
    { "value": "pdf", "label": "PDF文档" },
    { "value": "word", "label": "Word文档" },
    { "value": "markdown", "label": "Markdown文档" },
    { "value": "text", "label": "文本文档" }
  ]
}
```

**前端调用示例**:
```javascript
/**
 * 获取文档类型列表
 * - 接口地址: /api/search/doc-types
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: Array<{value, label}>
 */
export async function getDocTypes() {
  return await apiRequest('/api/search/doc-types', {
    method: 'POST',
    body: {},
    needAuth: true
  });
}
```

---

### 7.4 导出搜索结果

**功能描述**: 将当前搜索结果导出为CSV文件，包含文档标题、知识库、类型、页码、更新时间等信息。

**业务背景**: 用户需要保存搜索结果用于离线查看或分享给他人。

**接口地址**: `/api/search/export`

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
  "keyword": "string, 搜索关键词",
  "knowledgeBaseId": "string, 知识库ID",
  "docType": "string, 文档类型",
  "sortBy": "string, 排序方式"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| keyword | string | 是 | 搜索关键词 | "API设计" |
| knowledgeBaseId | string | 否 | 知识库ID | "kb_001" |
| docType | string | 否 | 文档类型 | "pdf" |
| sortBy | string | 否 | 排序方式 | "relevance" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "导出成功",
  "body": {
    "downloadUrl": "string, 下载链接",
    "fileName": "string, 文件名",
    "expiresIn": "number, 过期时间（秒）"
  }
}
```

**成功响应示例**:
```json
{
  "error": 0,
  "message": "导出成功",
  "body": {
    "downloadUrl": "/downloads/search-results-1696156800000.csv",
    "fileName": "search-results-2025-10-01.csv",
    "expiresIn": 3600
  }
}
```

**失败响应示例**:
```json
{
  "error": 4002,
  "message": "搜索结果为空，无法导出",
  "body": {}
}
```

**前端调用示例**:
```javascript
/**
 * 导出搜索结果
 * - 接口地址: /api/search/export
 * - 方法: POST
 * - 需要登录: 是
 * - 返回值: {downloadUrl, fileName, expiresIn}
 */
export async function exportSearchResults(params) {
  return await apiRequest('/api/search/export', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

**注意事项**:
- 导出文件为CSV格式，使用UTF-8编码
- 下载链接有效期为1小时（3600秒）
- 导出最多包含1000条记录
- 前端应使用`window.open(downloadUrl)`触发下载

---

## 8. 用户管理模块

### 8.1 获取用户统计数据

**功能描述**: 获取用户管理概览统计信息，包括总用户数、活跃用户数、管理员数、禁用用户数等关键指标。

**业务背景**: 用于管理员用户管理页面展示系统用户概况，快速了解系统用户状态分布。

**接口地址**: `/api/admin/users/stats`

**请求方法**: POST

**需要登录**: 是

**需要权限**: admin

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
    "totalUsers": 156,
    "activeUsers": 142,
    "adminUsers": 8,
    "disabledUsers": 6
  }
}
```

**Body 数据结构**:
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| totalUsers | number | 总用户数 | 156 |
| activeUsers | number | 活跃用户数 | 142 |
| adminUsers | number | 管理员数量 | 8 |
| disabledUsers | number | 禁用用户数 | 6 |

**前端调用示例**:
```javascript
export async function getUserStats() {
  return await apiRequest('/api/admin/users/stats', {
    method: 'POST',
    body: {},
    needAuth: true
  });
}
```

**注意事项**:
- 该接口仅管理员可访问
- 统计数据实时计算

---

### 8.2 获取用户列表

**功能描述**: 获取系统用户列表，支持关键词搜索、角色筛选、状态筛选和分页查询。

**业务背景**: 用于用户管理页面展示和管理所有系统用户，支持多维度筛选和搜索。

**接口地址**: `/api/admin/users/list`

**请求方法**: POST

**需要登录**: 是

**需要权限**: admin

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "keyword": "string, 搜索关键词（姓名/邮箱/手机号），可选",
  "role": "string, 角色筛选（admin/user），可选",
  "status": "string, 状态筛选（active/disabled），可选",
  "page": "number, 页码",
  "pageSize": "number, 每页数量"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| keyword | string | 否 | 搜索关键词 | "张三" |
| role | string | 否 | 角色筛选 | "admin" |
| status | string | 否 | 状态筛选 | "active" |
| page | number | 否 | 页码，默认1 | 1 |
| pageSize | number | 否 | 每页数量，默认10 | 10 |

**响应格式**: 
```json
{
  "error": 0,
  "message": "获取成功",
  "body": {
    "list": [
      {
        "id": "user_001",
        "name": "张三",
        "username": "zhangsan",
        "email": "zhangsan@company.com",
        "phone": "138****1234",
        "role": "admin",
        "status": "active",
        "avatarColor": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "lastLogin": "2024-09-25 09:30",
        "createdAt": "2024-01-15"
      }
    ],
    "total": 156,
    "page": 1,
    "pageSize": 10
  }
}
```

**Body 数据结构**:
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| list | array | 用户列表 | - |
| list[].id | string | 用户ID | "user_001" |
| list[].name | string | 姓名 | "张三" |
| list[].username | string | 用户名 | "zhangsan" |
| list[].email | string | 邮箱 | "zhangsan@company.com" |
| list[].phone | string | 手机号（部分隐藏） | "138****1234" |
| list[].role | string | 角色：admin/user | "admin" |
| list[].status | string | 状态：active/disabled | "active" |
| list[].avatarColor | string | 头像背景色 | "linear-gradient(...)" |
| list[].lastLogin | string | 最后登录时间 | "2024-09-25 09:30" |
| list[].createdAt | string | 创建时间 | "2024-01-15" |
| total | number | 总数 | 156 |

**前端调用示例**:
```javascript
export async function getUserList(params = {}) {
  return await apiRequest('/api/admin/users/list', {
    method: 'POST',
    body: {
      page: 1,
      pageSize: 10,
      ...params
    },
    needAuth: true
  });
}
```

**注意事项**:
- 手机号需要部分隐藏（中间4位用*代替）
- avatarColor用于前端展示用户头像背景色

---

### 8.3 创建用户

**功能描述**: 创建新用户账号，设置用户基本信息、角色和初始密码。

**业务背景**: 管理员添加新用户到系统中，分配相应角色和权限。

**接口地址**: `/api/admin/users/create`

**请求方法**: POST

**需要登录**: 是

**需要权限**: admin

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "name": "string, 姓名",
  "username": "string, 用户名",
  "email": "string, 邮箱",
  "phone": "string, 手机号",
  "role": "string, 角色（admin/user）",
  "password": "string, 初始密码"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| name | string | 是 | 姓名 | "李四" |
| username | string | 是 | 用户名（唯一） | "lisi" |
| email | string | 是 | 邮箱地址 | "lisi@company.com" |
| phone | string | 是 | 手机号 | "13900001234" |
| role | string | 是 | 角色 | "user" |
| password | string | 是 | 初始密码 | "Pass@123" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "创建成功",
  "body": {
    "id": "user_123",
    "username": "lisi",
    "createdAt": "2024-10-02T10:30:00Z"
  }
}
```

**失败响应示例**:
```json
{
  "error": 400,
  "message": "用户名已存在",
  "body": {}
}
```

**前端调用示例**:
```javascript
export async function createUser(params) {
  return await apiRequest('/api/admin/users/create', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

**注意事项**:
- 用户名必须唯一
- 密码需要符合复杂度要求（至少6位）
- 邮箱和手机号格式需要验证

---

### 8.4 更新用户信息

**功能描述**: 更新用户的基本信息，包括姓名、邮箱、手机号、角色等。

**业务背景**: 管理员修改用户资料或调整用户角色。

**接口地址**: `/api/admin/users/update`

**请求方法**: POST

**需要登录**: 是

**需要权限**: admin

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "id": "string, 用户ID",
  "name": "string, 姓名",
  "email": "string, 邮箱",
  "phone": "string, 手机号",
  "role": "string, 角色"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| id | string | 是 | 用户ID | "user_001" |
| name | string | 是 | 姓名 | "张三" |
| email | string | 是 | 邮箱 | "zhangsan@company.com" |
| phone | string | 是 | 手机号 | "13800001234" |
| role | string | 是 | 角色 | "admin" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "更新成功",
  "body": {}
}
```

**前端调用示例**:
```javascript
export async function updateUser(params) {
  return await apiRequest('/api/admin/users/update', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

---

### 8.5 删除用户

**功能描述**: 删除用户账号，此操作不可恢复。

**业务背景**: 管理员删除不再使用的用户账号。

**接口地址**: `/api/admin/users/delete`

**请求方法**: POST

**需要登录**: 是

**需要权限**: admin

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "userId": "string, 用户ID"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| userId | string | 是 | 要删除的用户ID | "user_001" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "删除成功",
  "body": {}
}
```

**前端调用示例**:
```javascript
export async function deleteUser(params) {
  return await apiRequest('/api/admin/users/delete', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

**注意事项**:
- 删除操作不可恢复，建议前端二次确认
- 不能删除当前登录的管理员

---

### 8.6 切换用户状态

**功能描述**: 启用或禁用用户账号。

**业务背景**: 管理员临时禁用或重新启用用户账号。

**接口地址**: `/api/admin/users/toggle-status`

**请求方法**: POST

**需要登录**: 是

**需要权限**: admin

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "userId": "string, 用户ID",
  "status": "string, 目标状态（active/disabled）"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| userId | string | 是 | 用户ID | "user_001" |
| status | string | 是 | 目标状态 | "disabled" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "禁用成功",
  "body": {}
}
```

**前端调用示例**:
```javascript
export async function toggleUserStatus(params) {
  return await apiRequest('/api/admin/users/toggle-status', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

**注意事项**:
- 禁用用户后，该用户无法登录系统
- 不能禁用当前登录的管理员

---

### 8.7 重置用户密码

**功能描述**: 重置用户密码为随机密码，并返回新密码。

**业务背景**: 用户忘记密码时，管理员帮助重置。

**接口地址**: `/api/admin/users/reset-password`

**请求方法**: POST

**需要登录**: 是

**需要权限**: admin

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "userId": "string, 用户ID"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| userId | string | 是 | 用户ID | "user_001" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "密码重置成功",
  "body": {
    "newPassword": "Temp8x9kl2"
  }
}
```

**Body 数据结构**:
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| newPassword | string | 新密码（明文，仅此次返回） | "Temp8x9kl2" |

**前端调用示例**:
```javascript
export async function resetUserPassword(params) {
  return await apiRequest('/api/admin/users/reset-password', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

**注意事项**:
- 新密码仅在响应中返回一次
- 建议用户首次登录后修改密码

---

### 8.8 导出用户列表

**功能描述**: 导出用户列表为CSV文件。

**业务背景**: 管理员需要导出用户数据进行统计分析。

**接口地址**: `/api/admin/users/export`

**请求方法**: POST

**需要登录**: 是

**需要权限**: admin

**请求头 (Headers)**:
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体 (Body)**:
```json
{
  "keyword": "string, 搜索关键词，可选",
  "role": "string, 角色筛选，可选",
  "status": "string, 状态筛选，可选"
}
```

**参数说明**:
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| keyword | string | 否 | 搜索关键词 | "张" |
| role | string | 否 | 角色筛选 | "admin" |
| status | string | 否 | 状态筛选 | "active" |

**响应格式**: 
```json
{
  "error": 0,
  "message": "导出成功",
  "body": {
    "downloadUrl": "/downloads/users-20241002.csv",
    "fileName": "users-2024-10-02.csv",
    "expiresIn": 3600
  }
}
```

**Body 数据结构**:
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| downloadUrl | string | 下载链接 | "/downloads/users-20241002.csv" |
| fileName | string | 文件名 | "users-2024-10-02.csv" |
| expiresIn | number | 过期时间（秒） | 3600 |

**前端调用示例**:
```javascript
export async function exportUsers(params = {}) {
  return await apiRequest('/api/admin/users/export', {
    method: 'POST',
    body: params,
    needAuth: true
  });
}
```

**注意事项**:
- 导出文件为CSV格式，UTF-8编码
- 文件链接有效期为1小时
- 手机号导出时保持部分隐藏

---

## 9. 模型管理模块

*待补充:当生成模型管理相关前端界面时,此部分将被填充*

---

## 10. 权限管理模块

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
| 4001 | 搜索关键词不能为空 | 提示用户输入搜索关键词 |
| 4002 | 搜索结果为空，无法导出 | 提示用户搜索结果为空 |

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
| 2025-10-01 | v1.2 | 添加智能问答模块接口(会话、消息、模型) | AI Assistant |
| 2025-10-01 | v1.3 | 添加搜索模块接口(搜索文档、热门关键词、文档类型、导出) | AI Assistant |
| 2025-10-01 | v1.4 | 添加个人中心模块(6个接口): 获取个人信息、更新个人信息、上传头像、获取部门列表、获取登录记录、修改密码 | AI Assistant |
| 2025-10-02 | v1.5 | 添加仪表板模块(3个接口): 获取仪表板统计数据、获取系统状态、刷新系统状态 | AI Assistant |

---

**文档维护说明**:
- 每次前端新增或修改界面涉及 API 调用时,必须同步更新本文档
- 接口文档应包含完整的请求/响应示例和数据说明
- 保持文档与代码的一致性,确保后端可以直接参考实现

