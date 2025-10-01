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

*待补充:当生成知识库相关前端界面时,此部分将被填充*

---

## 3. 文档管理模块

*待补充:当生成文档管理相关前端界面时,此部分将被填充*

---

## 4. RAG 智能问答模块

*待补充:当生成智能问答相关前端界面时,此部分将被填充*

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

*更多数据字典将随着功能开发而补充*

### C. 更新日志

| 日期 | 版本 | 更新内容 | 更新人 |
|------|------|---------|--------|
| 2025-10-01 | v1.0 | 初始化文档,添加用户认证模块接口 | AI Assistant |

---

**文档维护说明**:
- 每次前端新增或修改界面涉及 API 调用时,必须同步更新本文档
- 接口文档应包含完整的请求/响应示例和数据说明
- 保持文档与代码的一致性,确保后端可以直接参考实现

