# RAG 知识问答系统

基于检索增强生成(RAG)技术的企业级智能问答系统。

**状态**: 前端已完成 ✅ | 后端开发中 ⏳

## 项目结构

```
ZhongMeiRagProject/
├── frontEnd/                      # 前端（已完成）
│   ├── src/
│   │   ├── api/                   # API接口（9个模块）
│   │   ├── views/                 # 页面组件（7个页面+5个管理页面）
│   │   ├── layouts/               # 布局组件
│   │   ├── router/                # 路由配置
│   │   └── utils/                 # 工具函数
│   └── README.md                  # 前端说明
├── backEnd/                       # 后端（待开发）
├── doc/
│   ├── api/
│   │   ├── api-front-back.md     # 接口文档 ⭐⭐⭐⭐⭐
│   │   └── backEndDev.md         # 后端开发指南 ⭐⭐⭐⭐⭐
│   ├── Rag-MVP.md                # 产品需求
│   └── iconfont.md               # 图标需求
└── README.md
```

## 快速开始

### 前端开发
```bash
cd frontEnd
npm install
npm run dev  # http://localhost:5173
```
使用Mock数据，无需后端。详见 [frontEnd/README.md](frontEnd/README.md)

### 后端开发

**必读文档**：
1. [doc/api/backEndDev.md](doc/api/backEndDev.md) - 开发流程和示例
2. [doc/api/api-front-back.md](doc/api/api-front-back.md) - 接口规范
3. [doc/Rag-MVP.md](doc/Rag-MVP.md) - 产品需求

**联调步骤**：
```bash
# 1. 启动后端（端口8000）
cd backEnd
python app.py

# 2. 修改前端配置 frontEnd/src/utils/env.js
export const USE_MOCK = false

# 3. 启动前端
cd frontEnd
npm run dev
```

## 技术栈

**前端**：Vue 3.5 + Vite 7.1 + Vue Router 4  
**后端**：Python + LLM + 向量数据库 + MySQL

## 已完成功能

### 普通用户
- ✅ 登录/登出
- ✅ 我的知识库（查看列表、统计）
- ✅ 智能问答（对话、引用、推荐问题）
- ✅ 文档搜索（关键词、筛选）
- ✅ 个人中心（信息编辑、密码修改、登录记录）

### 管理员
- ✅ 仪表盘（统计数据、系统状态）
- ✅ 用户管理（增删改查、状态、密码重置）
- ✅ 知识库管理（创建、编辑、文档管理、批量导出）
- ✅ 模型管理（LLM/向量模型、健康检查）

## 后端待开发

**第一阶段**（核心）：
- [ ] 用户认证（登录/Token）
- [ ] 知识库查询
- [ ] 智能问答（RAG检索+LLM）

**第二阶段**（管理）：
- [ ] 文档上传/解析/向量化
- [ ] 用户管理
- [ ] 系统监控

## 接口规范

**统一响应格式**：
```json
{
  "error": 0,           // 0=成功, 401=未登录, 403=无权限, 500=系统错误
  "message": "提示信息",
  "body": {}            // 业务数据
}
```

完整规范：[doc/api/api-front-back.md](doc/api/api-front-back.md)

## 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| user | user123 | 普通用户 |

## 文档导航

- [后端开发指南](doc/api/backEndDev.md) - 开发流程、示例代码
- [接口文档](doc/api/api-front-back.md) - 完整API规范
- [产品需求](doc/Rag-MVP.md) - 业务需求
- [前端README](frontEnd/README.md) - 前端详细说明

---

**维护**: 前端开发组 | **更新**: 2025-10-04

