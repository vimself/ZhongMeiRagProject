# RAG知识问答系统 - 前端项目

基于 Vue 3 + Vite 开发的企业级知识问答系统前端应用。

## 技术栈

- **框架**: Vue 3.5
- **构建工具**: Vite 7.1
- **路由**: Vue Router 4
- **开发工具**: Vite DevTools
- **样式**: CSS3 (Scoped Style)
- **包管理**: npm

## 项目结构

```
frontEnd/
├── src/
│   ├── api/              # API接口定义
│   │   ├── authApi.js    # 用户认证接口
│   │   └── mock.js       # 模拟数据
│   ├── assets/           # 静态资源
│   │   ├── icons/        # 图标资源 (待添加)
│   │   └── images/       # 图片资源 (待添加)
│   ├── router/           # 路由配置
│   │   └── index.js      # 路由定义和守卫
│   ├── utils/            # 工具函数
│   │   ├── env.js        # 环境配置
│   │   ├── request.js    # API请求封装
│   │   └── storage.js    # 本地存储工具
│   ├── views/            # 页面组件
│   │   ├── Login.vue     # 登录页面
│   │   └── Dashboard.vue # 首页(临时)
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── public/               # 公共资源
├── index.html            # HTML模板
├── vite.config.js        # Vite配置
├── jsconfig.json         # JS配置
└── package.json          # 依赖配置
```

## 环境要求

- Node.js: `^20.19.0 || >=22.12.0`
- npm: 最新版本

## 快速开始

### 1. 安装依赖

```bash
cd frontEnd
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

开发服务器将在 `http://localhost:5173` 启动

### 3. 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist/` 目录

### 4. 预览生产版本

```bash
npm run preview
```

## 开发环境配置

### 当前环境
- **开发环境**: 自动使用模拟数据，无需后端服务
- **生产环境**: 需要配置实际的后端API地址

### 模拟数据测试账号

开发环境下可以使用以下测试账号登录：

**管理员账号**:
- 用户名: `admin`
- 密码: `admin123`

**普通用户账号**:
- 用户名: `user`
- 密码: `user123`

## 已完成功能

### ✅ 登录页面
- 用户名/密码登录
- 密码显示/隐藏切换
- 记住我功能
- 忘记密码提示
- 表单验证
- 加载状态
- 错误提示
- 响应式设计

### ✅ 路由配置
- 路由守卫(登录验证)
- 页面跳转
- 已登录自动跳转

### ✅ API接口封装
- 统一请求处理
- 错误处理
- Token认证
- 开发环境模拟数据

### ✅ 工具函数
- 环境配置
- 本地存储管理
- Token管理

## 待开发功能

- [ ] 首页/工作台
- [ ] 智能问答页面
- [ ] 知识库管理
- [ ] 文档上传
- [ ] 搜索功能
- [ ] 用户管理(管理员)
- [ ] 模型管理(管理员)
- [ ] 个人中心
- [ ] 修改密码

## 图标资源

当前页面使用Emoji作为图标占位符，需要替换为专业图标。

详细的图标需求请查看: [图标资源文档](../doc/iconfont.md)

推荐使用以下图标库:
- Iconfont (阿里巴巴矢量图标库)
- Font Awesome
- Element Plus Icons

## API接口文档

完整的前后端接口文档请查看: [API文档](../doc/api/api-front-back.md)

## 开发规范

### 命名规范
- 组件文件: PascalCase (如 `UserProfile.vue`)
- 变量/函数: camelCase (如 `userName`, `getUserInfo`)
- 常量: UPPER_CASE (如 `API_BASE_URL`)
- CSS类名: kebab-case (如 `login-container`)

### 代码风格
- 使用 ES6+ 语法
- 使用 Composition API
- 组件使用 `<script setup>`
- 样式使用 scoped
- 保持代码简洁和可读性

### Git提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具链相关

## 浏览器支持

- Chrome (推荐)
- Edge
- Firefox
- Safari

## 相关文档

- [需求文档](../doc/Rag-MVP.md)
- [Vue3开发规范](../.cursor/rules/vue3.mdc)
- [API开发规范](../.cursor/rules/api-js.mdc)
- [API接口文档](../doc/api/api-front-back.md)
- [图标资源文档](../doc/iconfont.md)

## 许可证

内部项目，仅供公司内部使用。

## 更新日志

### v0.1.0 (2025-10-01)
- ✅ 初始化项目
- ✅ 完成登录页面UI和功能
- ✅ 配置路由和路由守卫
- ✅ 封装API请求工具
- ✅ 实现开发环境模拟数据
- ✅ 完成API文档(用户认证模块)
- ✅ 完成图标资源需求文档

---

**维护团队**: 前端开发组  
**最后更新**: 2025-10-01
