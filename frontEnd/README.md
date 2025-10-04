# RAG知识问答系统 - 前端

基于 Vue 3 + Vite 的企业级知识问答系统前端。

## 技术栈

- Vue 3.5 + Composition API
- Vue Router 4
- Vite 7.1
- 原生 CSS3（无UI框架）

## 项目结构

```
frontEnd/
├── src/
│   ├── api/                    # API接口
│   │   ├── authApi.js          # 认证
│   │   ├── chatApi.js          # 智能问答
│   │   ├── knowledgeApi.js     # 知识库
│   │   ├── userApi.js          # 个人中心
│   │   ├── userManagementApi.js # 用户管理
│   │   ├── dashboardApi.js     # 仪表盘
│   │   ├── modelApi.js         # 模型管理
│   │   ├── searchApi.js        # 文档搜索
│   │   └── mock.js             # Mock数据
│   ├── views/                  # 页面
│   │   ├── Login.vue           # 登录
│   │   ├── Knowledge.vue       # 我的知识库
│   │   ├── Chat.vue            # 智能问答
│   │   ├── Search.vue          # 文档搜索
│   │   ├── Profile.vue         # 个人中心
│   │   ├── DashboardAdmin.vue  # 管理员仪表盘
│   │   └── admin/              # 管理员页面
│   │       ├── UserManagement.vue          # 用户管理
│   │       ├── KnowledgeManagement.vue     # 知识库管理
│   │       ├── KnowledgeBaseDetail.vue     # 知识库详情
│   │       ├── DocumentPreview.vue         # 文档预览
│   │       ├── ModelManagement.vue         # 模型管理
│   │       └── components/                 # 管理页面组件
│   ├── layouts/                # 布局
│   │   └── MainLayout.vue      # 主布局
│   ├── router/                 # 路由
│   ├── utils/                  # 工具
│   │   ├── env.js              # 环境配置
│   │   ├── request.js          # 请求封装
│   │   └── storage.js          # 本地存储
│   └── assets/                 # 静态资源
├── vite.config.js              # Vite配置
└── package.json
```

## 快速开始

### 安装依赖
```bash
npm install
```

### 开发模式（使用Mock数据）
```bash
npm run dev
```
访问 `http://localhost:5173`

### 生产构建
```bash
npm run build
```

## 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| user | user123 | 普通用户 |

## 后端联调

### 1. 修改配置
编辑 `src/utils/env.js` 第19行：
```javascript
export const USE_MOCK = false  // 改为 false
```

### 2. 配置后端地址（可选）
如后端端口不是8000，编辑 `vite.config.js` 第25行：
```javascript
target: 'http://localhost:8000'  // 改为实际地址
```

### 3. 启动
```bash
npm run dev
```

详细说明：`../doc/api/backEndDev.md`

## 已完成功能

### 普通用户功能
- ✅ 登录/登出
- ✅ 我的知识库（查看列表、统计数据）
- ✅ 智能问答（对话、引用来源、推荐问题）
- ✅ 文档搜索（关键词搜索、高级筛选）
- ✅ 个人中心（信息编辑、修改密码、登录记录）

### 管理员功能
- ✅ 仪表盘（统计数据、系统状态）
- ✅ 用户管理（增删改查、状态管理、密码重置）
- ✅ 知识库管理（创建、编辑、文档管理、批量导出）
- ✅ 模型管理（LLM/向量模型配置、健康检查）

### 技术实现
- ✅ 路由守卫（登录验证、权限控制）
- ✅ API封装（统一请求、错误处理、Mock数据）
- ✅ Token认证
- ✅ 响应式布局

## 待完善功能

- [ ] 流式回答显示（智能问答）
- [ ] 文档在线预览（PDF/Word）
- [ ] 历史会话加载
- [ ] 使用统计图表

## 生产部署

### 前端打包
```bash
npm run build
```
构建产物在 `dist/` 目录

### 后端集成

**Python Flask**
```python
from flask import Flask, send_from_directory
app = Flask(__name__, static_folder='dist')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')
```

**Node.js Express**
```javascript
const express = require('express');
const path = require('path');
const app = express();

app.use(express.static('dist'));
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});
```

## 开发规范

- 组件文件: PascalCase (`UserProfile.vue`)
- 变量/函数: camelCase (`getUserInfo`)
- 常量: UPPER_CASE (`API_BASE_URL`)
- CSS类名: kebab-case (`login-container`)

## 相关文档

- [后端开发指南](../doc/api/backEndDev.md) - 后端联调必读
- [接口文档](../doc/api/api-front-back.md) - 完整API规范
- [需求文档](../doc/Rag-MVP.md) - 产品需求

---

**维护**: 前端开发组 | **更新**: 2025-10-04
