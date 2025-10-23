# 图标和图片资源汇总

> **说明**: 本文档汇总前端开发中需要的所有图标和图片资源，方便设计师和开发人员统一制作和替换。
> 
> **更新日期**: 2025-10-01  
> **版本**: v1.0

---

## 登录页面 (Login.vue)

### 1. Logo图标
- **文件名**: `logo.png` 或 `logo.svg`
- **位置**: `frontEnd/src/assets/images/logo.png`
- **尺寸**: 64x64 px
- **用途**: 登录页面顶部的系统Logo
- **样式**: 圆角矩形背景(12px圆角)，品牌色背景(#667eea)
- **当前状态**: 使用CSS占位符(需要替换为实际Logo)
- **设计要求**: 
  - 简洁现代的设计风格
  - 能代表RAG知识问答系统的含义
  - 支持SVG格式以便缩放

### 2. 用户图标 (User Icon)
- **文件名**: `icon-user.svg`
- **位置**: `frontEnd/src/assets/icons/icon-user.svg`
- **尺寸**: 16x16 px
- **用途**: 用户名输入框前的图标
- **当前状态**: 使用Emoji占位符 "👤" (需要替换为图标字体或SVG)
- **设计要求**: 
  - 线条风格图标
  - 颜色: #333333

### 3. 锁定图标 (Lock Icon)
- **文件名**: `icon-lock.svg`
- **位置**: `frontEnd/src/assets/icons/icon-lock.svg`
- **尺寸**: 16x16 px
- **用途**: 密码输入框前的图标
- **当前状态**: 使用Emoji占位符 "🔒" (需要替换为图标字体或SVG)
- **设计要求**: 
  - 线条风格图标
  - 颜色: #333333

### 4. 眼睛图标 - 关闭状态 (Eye Close Icon)
- **文件名**: `icon-eye-close.svg`
- **位置**: `frontEnd/src/assets/icons/icon-eye-close.svg`
- **尺寸**: 20x20 px
- **用途**: 密码输入框显示/隐藏密码按钮 - 隐藏状态
- **当前状态**: 使用Emoji占位符 "👁️" (需要替换为图标字体或SVG)
- **设计要求**: 
  - 线条风格图标，带斜线表示关闭
  - 颜色: #999999
  - Hover颜色: #667eea

### 5. 眼睛图标 - 打开状态 (Eye Open Icon)
- **文件名**: `icon-eye-open.svg`
- **位置**: `frontEnd/src/assets/icons/icon-eye-open.svg`
- **尺寸**: 20x20 px
- **用途**: 密码输入框显示/隐藏密码按钮 - 显示状态
- **当前状态**: 使用Emoji占位符 "👁️" (需要替换为图标字体或SVG)
- **设计要求**: 
  - 线条风格图标
  - 颜色: #999999
  - Hover颜色: #667eea

### 6. 信息图标 (Info Icon)
- **文件名**: `icon-info.svg`
- **位置**: `frontEnd/src/assets/icons/icon-info.svg`
- **尺寸**: 16x16 px
- **用途**: 提示信息前的图标
- **当前状态**: 使用Emoji占位符 "ℹ️" (需要替换为图标字体或SVG)
- **设计要求**: 
  - 圆形内带字母"i"的图标
  - 颜色: #666666

### 7. 加载动画图标 (Loading Icon)
- **文件名**: `icon-loading.svg`
- **位置**: `frontEnd/src/assets/icons/icon-loading.svg`
- **尺寸**: 16x16 px
- **用途**: 登录按钮加载状态
- **当前状态**: 使用CSS动画实现的旋转圆圈 (可保留或替换)
- **设计要求**: 
  - 圆形旋转动画
  - 颜色: #ffffff (白色)
  - 动画: 顺时针旋转，0.6s循环

---

## 背景图片

### 1. 登录页面渐变背景
- **当前实现**: CSS渐变 `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **可选替换**: 可以使用背景图片增强视觉效果
- **文件名**: `login-bg.jpg` (如果需要使用图片)
- **位置**: `frontEnd/src/assets/images/login-bg.jpg`
- **尺寸**: 1920x1080 px (全屏背景)
- **设计要求**: 
  - 科技感/知识/AI相关的背景图
  - 颜色倾向紫色/蓝色渐变
  - 不要过于复杂，不影响登录表单的可读性

---

## 推荐的图标库

建议使用以下图标库之一来统一管理图标：

### 1. Iconfont (阿里巴巴矢量图标库)
- **网址**: https://www.iconfont.cn/
- **优势**: 免费、中文支持好、图标丰富
- **使用方式**: 
  1. 在Iconfont上搜索并添加所需图标到项目
  2. 生成在线链接或下载本地文件
  3. 引入到项目中使用

### 2. Font Awesome
- **网址**: https://fontawesome.com/
- **优势**: 图标质量高、更新及时
- **使用方式**: 
  ```bash
  npm install @fortawesome/fontawesome-free
  ```

### 3. Element Plus Icons
- **网址**: https://element-plus.org/zh-CN/component/icon.html
- **优势**: 如果项目使用Element Plus组件库，图标风格统一
- **使用方式**: 
  ```bash
  npm install @element-plus/icons-vue
  ```

---

## 图标使用规范

### CSS Class命名规范
- 使用 `icon-` 前缀
- 使用小写字母和连字符
- 示例: `icon-user`, `icon-lock`, `icon-eye-open`

### SVG图标使用建议
1. **优先使用SVG格式**，便于缩放和自定义颜色
2. **图标颜色**使用 `currentColor`，便于CSS控制
3. **统一尺寸**，使用CSS的 `width` 和 `height` 控制

### 图标颜色规范
- **主要图标**: #333333 (深灰)
- **次要图标**: #666666 (中灰)
- **辅助图标**: #999999 (浅灰)
- **强调图标**: #667eea (品牌色)
- **白色图标**: #ffffff (用于深色背景)

---

## 主布局导航栏 (MainLayout.vue)

### 1. 系统Logo图标
- **文件名**: `logo-main.svg`
- **位置**: `frontEnd/src/assets/images/logo-main.svg`
- **尺寸**: 40x40 px
- **用途**: 主布局左侧导航栏顶部Logo
- **样式**: 紫色渐变背景，圆角8px
- **当前状态**: 使用CSS渐变占位符(需要替换为实际Logo)
- **设计要求**: 与登录页Logo风格一致

### 2. 导航菜单图标

#### 2.1 我的知识库图标 (Knowledge Icon)
- **文件名**: `icon-knowledge.svg`
- **位置**: `frontEnd/src/assets/icons/icon-knowledge.svg`
- **尺寸**: 20x20 px
- **用途**: 导航菜单"我的知识库"项
- **当前状态**: 使用Emoji占位符 "📚" (需要替换)
- **设计要求**: 书籍/图书馆风格的图标

#### 2.2 智能问答图标 (Chat Icon)
- **文件名**: `icon-chat.svg`
- **位置**: `frontEnd/src/assets/icons/icon-chat.svg`
- **尺寸**: 20x20 px
- **用途**: 导航菜单"智能问答"项
- **当前状态**: 使用Emoji占位符 "💬" (需要替换)
- **设计要求**: 对话气泡风格的图标

#### 2.3 文档搜索图标 (Search Icon)
- **文件名**: `icon-search.svg`
- **位置**: `frontEnd/src/assets/icons/icon-search.svg`
- **尺寸**: 20x20 px
- **用途**: 导航菜单"文档搜索"项
- **当前状态**: 使用Emoji占位符 "🔍" (需要替换)
- **设计要求**: 放大镜风格的图标

### 3. 用户菜单图标

#### 3.1 用户头像图标 (User Avatar Icon)
- **文件名**: `icon-user-avatar.svg`
- **位置**: `frontEnd/src/assets/icons/icon-user-avatar.svg`
- **尺寸**: 20x20 px
- **用途**: 底部用户信息区域头像
- **当前状态**: 使用Emoji占位符 "👤" (需要替换)
- **设计要求**: 人像轮廓风格

#### 3.2 更多操作图标 (More Icon)
- **文件名**: `icon-more.svg`
- **位置**: `frontEnd/src/assets/icons/icon-more.svg`
- **尺寸**: 18x18 px
- **用途**: 用户信息区域更多操作按钮
- **当前状态**: 使用文本符号 "⋮" (需要替换)
- **设计要求**: 竖向三点图标

#### 3.3 个人中心图标 (Profile Icon)
- **文件名**: `icon-profile.svg`
- **位置**: `frontEnd/src/assets/icons/icon-profile.svg`
- **尺寸**: 18x18 px
- **用途**: 用户菜单"个人中心"项
- **当前状态**: 使用Emoji占位符 "👤" (需要替换)
- **设计要求**: 用户设置风格图标

#### 3.4 退出登录图标 (Logout Icon)
- **文件名**: `icon-logout.svg`
- **位置**: `frontEnd/src/assets/icons/icon-logout.svg`
- **尺寸**: 18x18 px
- **用途**: 用户菜单"退出登录"项
- **当前状态**: 使用Emoji占位符 "🚪" (需要替换)
- **设计要求**: 退出/登出门的图标

---

## 我的知识库页面 (Knowledge.vue)

### 1. 页面功能图标

#### 1.1 时间图标 (Time Icon)
- **文件名**: `icon-time.svg`
- **位置**: `frontEnd/src/assets/icons/icon-time.svg`
- **尺寸**: 16x16 px
- **用途**: 页面右上角当前时间显示
- **当前状态**: 使用Emoji占位符 "🕐" (需要替换)
- **设计要求**: 时钟风格图标

### 2. 统计卡片图标

#### 2.1 知识库图标 (Database Icon)
- **文件名**: `icon-database.svg`
- **位置**: `frontEnd/src/assets/icons/icon-database.svg`
- **尺寸**: 28x28 px
- **用途**: "可访问知识库"统计卡片
- **当前状态**: 使用Emoji占位符 "📚" (需要替换)
- **设计要求**: 数据库/书架风格图标
- **颜色**: 蓝色系 (#dbeafe背景)

#### 2.2 文档图标 (Document Icon)
- **文件名**: `icon-document.svg`
- **位置**: `frontEnd/src/assets/icons/icon-document.svg`
- **尺寸**: 28x28 px
- **用途**: "可查阅文档"统计卡片
- **当前状态**: 使用Emoji占位符 "📄" (需要替换)
- **设计要求**: 文档/文件风格图标
- **颜色**: 绿色系 (#d1fae5背景)

#### 2.3 消息图标 (Message Icon)
- **文件名**: `icon-message.svg`
- **位置**: `frontEnd/src/assets/icons/icon-message.svg`
- **尺寸**: 28x28 px
- **用途**: "今日问答"统计卡片
- **当前状态**: 使用Emoji占位符 "💬" (需要替换)
- **设计要求**: 对话/消息风格图标
- **颜色**: 紫色系 (#e9d5ff背景)

### 3. 提示信息图标

#### 3.1 信息提示图标 (Info Tip Icon)
- **文件名**: `icon-info-tip.svg`
- **位置**: `frontEnd/src/assets/icons/icon-info-tip.svg`
- **尺寸**: 14x14 px
- **用途**: 知识库列表标题右侧提示
- **当前状态**: 使用Emoji占位符 "ℹ️" (需要替换)
- **设计要求**: 圆形带"i"字母的图标

### 4. 知识库卡片图标

#### 4.1 技术规范库图标 (Code Icon)
- **文件名**: `icon-code.svg`
- **位置**: `frontEnd/src/assets/icons/icon-code.svg`
- **尺寸**: 24x24 px
- **用途**: 技术规范库卡片图标
- **当前状态**: 需要创建(使用CSS渐变背景)
- **设计要求**: 代码/编程风格图标
- **颜色**: 紫色渐变背景

#### 4.2 产品手册图标 (Book Icon)
- **文件名**: `icon-code.svg`
- **位置**: `frontEnd/src/assets/icons/icon-code.svg`
- **尺寸**: 24x24 px
- **用途**: 产品手册卡片图标
- **当前状态**: 需要创建(使用CSS渐变背景)
- **设计要求**: 书本/手册风格图标
- **颜色**: 绿色渐变背景

#### 4.3 运维文档图标 (Gear Icon)
- **文件名**: `icon-code.svg`
- **位置**: `frontEnd/src/assets/icons/icon-code.svg`
- **尺寸**: 24x24 px
- **用途**: 运维文档卡片图标
- **当前状态**: 需要创建(使用CSS渐变背景)
- **设计要求**: 齿轮/设置风格图标
- **颜色**: 粉红色渐变背景

#### 4.4 更多操作图标 (More Dot Icon)
- **文件名**: `icon-more-dot.svg`
- **位置**: `frontEnd/src/assets/icons/icon-more-dot.svg`
- **尺寸**: 18x18 px
- **用途**: 知识库卡片更多操作按钮
- **当前状态**: 使用文本符号 "⋮" (需要替换)
- **设计要求**: 竖向三点图标

#### 4.5 查看图标 (Eye Icon)
- **文件名**: `icon-eye-view.svg`
- **位置**: `frontEnd/src/assets/icons/icon-eye-view.svg`
- **尺寸**: 14x14 px
- **用途**: 知识库卡片查看人数标识
- **当前状态**: 使用Emoji占位符 "👁️" (需要替换)
- **设计要求**: 眼睛风格图标

### 5. 状态指示图标

#### 5.1 加载动画图标 (Loading Spinner)
- **文件名**: `icon-loading.svg`
- **位置**: `frontEnd/src/assets/icons/icon-loading.svg`
- **尺寸**: 32x32 px
- **用途**: 页面加载中状态
- **当前状态**: 使用CSS动画实现的旋转圆圈 (可保留或替换)
- **设计要求**: 圆形旋转动画

---

## 智能问答页面 (Chat.vue)

### 1. 页面功能图标

#### 1.1 时间图标 (Time Icon)
- **文件名**: `icon-time.svg`
- **位置**: `frontEnd/src/assets/icons/icon-time.svg`
- **尺寸**: 16x16 px
- **用途**: 页面右上角当前时间显示
- **当前状态**: 使用Emoji占位符 "🕐" (需要替换)
- **设计要求**: 时钟风格图标

### 2. 左侧面板图标

#### 2.1 加号图标 (Plus Icon)
- **文件名**: `icon-plus.svg`
- **位置**: `frontEnd/src/assets/icons/icon-plus.svg`
- **尺寸**: 18x18 px
- **用途**: "新建对话"按钮图标
- **当前状态**: 使用文本符号 "+" (需要替换)
- **设计要求**: 简洁的加号图标
- **颜色**: 白色 (#ffffff)

### 3. 对话区头部图标

#### 3.1 模型图标 (Model Icon)
- **文件名**: `icon-model.svg`
- **位置**: `frontEnd/src/assets/icons/icon-model.svg`
- **尺寸**: 14x14 px
- **用途**: 对话区显示当前模型
- **当前状态**: 使用Emoji占位符 "🤖" (需要替换)
- **设计要求**: 机器人/AI风格图标

#### 3.3 收起侧边栏图标 (Sidebar Icon)
- **文件名**: `icon-sidebar.svg`
- **位置**: `frontEnd/src/assets/icons/icon-sidebar.svg`
- **尺寸**: 16x16 px
- **用途**: 收起/展开左侧面板按钮
- **当前状态**: 使用Emoji占位符 "📌" (需要替换)
- **设计要求**: 侧边栏/固定图标

### 4. 空状态图标

#### 4.1 机器人头像图标 (Robot Icon)
- **文件名**: `icon-model.svg`
- **位置**: `frontEnd/src/assets/icons/icon-model.svg`
- **尺寸**: 40x40 px
- **用途**: 空状态中央的RAG智能助手图标
- **当前状态**: 使用Emoji占位符 "🤖" (需要替换)
- **设计要求**: 友好的机器人头像
- **颜色**: 白色 (#ffffff)，用于紫色渐变背景

### 5. 推荐问题图标

#### 5.1 代码建议图标 (Code Suggest Icon)
- **文件名**: `icon-code-suggest.svg`
- **位置**: `frontEnd/src/assets/icons/icon-code-suggest.svg`
- **尺寸**: 20x20 px
- **用途**: 推荐问题"如何设计RESTful API?"
- **当前状态**: 使用Emoji占位符 "⚡" (需要替换)
- **设计要求**: 代码/闪电风格图标

#### 5.2 数据库建议图标 (Database Suggest Icon)
- **文件名**: `icon-database-suggest.svg`
- **位置**: `frontEnd/src/assets/icons/icon-database-suggest.svg`
- **尺寸**: 20x20 px
- **用途**: 推荐问题"数据库连接池最佳实践?"
- **当前状态**: 使用Emoji占位符 "🗄️" (需要替换)
- **设计要求**: 数据库/服务器风格图标

#### 5.3 Redis建议图标 (Redis Suggest Icon)
- **文件名**: `icon-redis-suggest.svg`
- **位置**: `frontEnd/src/assets/icons/icon-redis-suggest.svg`
- **尺寸**: 20x20 px
- **用途**: 推荐问题"Redis缓存如何优化?"
- **当前状态**: 使用Emoji占位符 "🔴" (需要替换)
- **设计要求**: Redis标志或红色圆形图标

#### 5.4 微服务建议图标 (Microservice Suggest Icon)
- **文件名**: `icon-microservice-suggest.svg`
- **位置**: `frontEnd/src/assets/icons/icon-microservice-suggest.svg`
- **尺寸**: 20x20 px
- **用途**: 推荐问题"微服务架构注意事项?"
- **当前状态**: 使用Emoji占位符 "🎯" (需要替换)
- **设计要求**: 目标/架构风格图标

### 6. 消息头像图标

#### 6.1 用户消息头像 (User Message Icon)
- **文件名**: `icon-user-msg.svg`
- **位置**: `frontEnd/src/assets/icons/icon-user-msg.svg`
- **尺寸**: 18x18 px
- **用途**: 用户消息的头像图标
- **当前状态**: 使用Emoji占位符 "👤" (需要替换)
- **设计要求**: 用户轮廓图标
- **颜色**: 深色系（用于浅蓝色背景）

#### 6.2 助手消息头像 (Assistant Message Icon)
- **文件名**: `icon-model.svg.svg`
- **位置**: `frontEnd/src/assets/icons/icon-model.svg.svg`
- **尺寸**: 18x18 px
- **用途**: AI助手消息的头像图标
- **当前状态**: 使用Emoji占位符 "🤖" (需要替换)
- **设计要求**: 机器人/AI图标
- **颜色**: 白色（用于紫色渐变背景）

#### 6.3 文档引用图标 (Document Reference Icon)
- **文件名**: `icon-document-ref.svg`
- **位置**: `frontEnd/src/assets/icons/icon-document-ref.svg`
- **尺寸**: 14x14 px
- **用途**: 引用来源列表中的文档图标
- **当前状态**: 使用Emoji占位符 "📄" (需要替换)
- **设计要求**: 文档/文件风格图标

### 7. 输入区图标

#### 7.1 发送图标 (Send Icon)
- **文件名**: `icon-send.svg`
- **位置**: `frontEnd/src/assets/icons/icon-send.svg`
- **尺寸**: 16x16 px
- **用途**: 发送消息按钮
- **当前状态**: 使用Emoji占位符 "✈️" (需要替换)
- **设计要求**: 纸飞机/发送风格图标
- **颜色**: 白色 (#ffffff)

#### 7.2 键盘图标 (Keyboard Icon)
- **文件名**: `icon-keyboard.svg`
- **位置**: `frontEnd/src/assets/icons/icon-keyboard.svg`
- **尺寸**: 14x14 px
- **用途**: 输入提示区域
- **当前状态**: 使用Emoji占位符 "⌨️" (需要替换)
- **设计要求**: 键盘风格图标

#### 7.3 快捷键图标 (Command Icon)
- **文件名**: `icon-command.svg`
- **位置**: `frontEnd/src/assets/icons/icon-command.svg`
- **尺寸**: 14x14 px
- **用途**: 输入提示区域快捷键标识
- **当前状态**: 使用文本符号 "⌘" (需要替换)
- **设计要求**: Command键符号图标

---

## 文档搜索页面 (Search.vue)

### 1. 页面功能图标

#### 1.1 时间图标 (Time Icon)
- **文件名**: `icon-time.svg`
- **位置**: `frontEnd/src/assets/icons/icon-time.svg`
- **尺寸**: 16x16 px
- **用途**: 页面右上角当前时间显示
- **当前状态**: 使用Emoji占位符 "🕐" (需要替换)
- **设计要求**: 时钟风格图标

#### 1.2 搜索按钮图标 (Search Button Icon)
- **文件名**: `icon-search-btn.svg`
- **位置**: `frontEnd/src/assets/icons/icon-search-btn.svg`
- **尺寸**: 18x18 px
- **用途**: 搜索按钮图标
- **当前状态**: 使用Emoji占位符 "🔍" (需要替换)
- **设计要求**: 放大镜风格图标
- **颜色**: 白色 (#ffffff)

#### 1.3 导出按钮图标 (Download Icon)
- **文件名**: `icon-download.svg`
- **位置**: `frontEnd/src/assets/icons/icon-download.svg`
- **尺寸**: 16x16 px
- **用途**: 导出结果按钮图标
- **当前状态**: 使用Emoji占位符 "📥" (需要替换)
- **设计要求**: 下载/导出风格图标
- **颜色**: 蓝色 (#667eea)

### 2. 空状态图标

#### 2.1 搜索空状态图标 (Search Empty Icon)
- **文件名**: `icon-search-empty.svg`
- **位置**: `frontEnd/src/assets/icons/icon-search-empty.svg`
- **尺寸**: 80x80 px
- **用途**: 搜索页面未搜索时的空状态图标
- **当前状态**: 使用Emoji占位符 "🔍" (需要替换)
- **设计要求**: 放大镜风格图标，半透明
- **颜色**: 灰色系，透明度50%

#### 2.2 无结果图标 (No Results Icon)
- **文件名**: `icon-no-results.svg`
- **位置**: `frontEnd/src/assets/icons/icon-no-results.svg`
- **尺寸**: 80x80 px
- **用途**: 搜索无结果时的占位图标
- **当前状态**: 使用Emoji占位符 "📭" (需要替换)
- **设计要求**: 空邮箱/无结果风格图标
- **颜色**: 灰色系，透明度50%

### 3. 加载状态图标

#### 3.1 搜索加载图标 (Search Loading Icon)
- **文件名**: `icon-loading-search.svg`
- **位置**: `frontEnd/src/assets/icons/icon-loading-search.svg`
- **尺寸**: 40x40 px
- **用途**: 搜索中的加载动画
- **当前状态**: 使用CSS动画实现的旋转圆圈 (可保留或替换)
- **设计要求**: 圆形旋转动画
- **颜色**: 蓝色 (#667eea)

### 4. 搜索结果元数据图标

#### 4.1 知识库小图标 (KB Small Icon)
- **文件名**: `icon-code.svg`
- **位置**: `frontEnd/src/assets/icons/icon-code.svg`
- **尺寸**: 14x14 px
- **用途**: 搜索结果中显示所属知识库
- **当前状态**: 使用Emoji占位符 "📚" (需要替换)
- **设计要求**: 书本/知识库风格图标
- **颜色**: 灰色 (#6b7280)

#### 4.2 文件类型图标 (File Type Icon)
- **文件名**: `icon-file-type.svg`
- **位置**: `frontEnd/src/assets/icons/icon-file-type.svg`
- **尺寸**: 14x14 px
- **用途**: 搜索结果中显示文档类型
- **当前状态**: 使用Emoji占位符 "📄" (需要替换)
- **设计要求**: 文档/文件风格图标
- **颜色**: 灰色 (#6b7280)

#### 4.3 页码图标 (Page Icon)
- **文件名**: `icon-page.svg`
- **位置**: `frontEnd/src/assets/icons/icon-page.svg`
- **尺寸**: 14x14 px
- **用途**: 搜索结果中显示文档页码
- **当前状态**: 使用Emoji占位符 "📃" (需要替换)
- **设计要求**: 页面/文档页码风格图标
- **颜色**: 灰色 (#6b7280)

#### 4.4 时间小图标 (Time Small Icon)
- **文件名**: `icon-time-small.svg`
- **位置**: `frontEnd/src/assets/icons/icon-time-small.svg`
- **尺寸**: 14x14 px
- **用途**: 搜索结果中显示更新时间
- **当前状态**: 使用Emoji占位符 "🕐" (需要替换)
- **设计要求**: 时钟风格图标
- **颜色**: 灰色 (#6b7280)

#### 4.5 文件大小图标 (Size Icon)
- **文件名**: `icon-storage-size.svg`
- **位置**: `frontEnd/src/assets/icons/icon-storage-size.svg`
- **尺寸**: 14x14 px
- **用途**: 搜索结果中显示文件大小
- **当前状态**: 使用Emoji占位符 "💾" (需要替换)
- **设计要求**: 磁盘/存储风格图标
- **颜色**: 灰色 (#6b7280)

---

## 个人设置页面 (Profile.vue)

### 1. 页面功能图标

#### 1.1 基本信息标签图标 (User Info Icon)
- **文件名**: `icon-user-info.svg`
- **位置**: `frontEnd/src/assets/icons/icon-user-info.svg`
- **尺寸**: 18x18 px
- **用途**: 基本信息标签页图标
- **当前状态**: 使用Emoji占位符 "👤" (需要替换)
- **设计要求**: 用户资料风格图标
- **颜色**: 标签激活时为白色，未激活时为 #6b7280

#### 1.2 安全设置标签图标 (Security Icon)
- **文件名**: `icon-security.svg`
- **位置**: `frontEnd/src/assets/icons/icon-security.svg`
- **尺寸**: 18x18 px
- **用途**: 安全设置标签页图标
- **当前状态**: 使用Emoji占位符 "🔒" (需要替换)
- **设计要求**: 安全/锁定风格图标
- **颜色**: 标签激活时为白色，未激活时为 #6b7280

### 2. 头像相关图标

#### 2.1 默认头像图标 (User Avatar Default Icon)
- **文件名**: `icon-user-avatar-default.svg`
- **位置**: `frontEnd/src/assets/icons/icon-user-avatar-default.svg`
- **尺寸**: 24x24 px (小头像), 48x48 px (大头像)
- **用途**: 用户未上传头像时的默认图标
- **当前状态**: 使用Emoji占位符 "👤" (需要替换)
- **设计要求**: 用户头像轮廓图标
- **颜色**: 白色 (#ffffff)，用于渐变背景

#### 2.2 相机图标 (Camera Icon)
- **文件名**: `icon-camera.svg`
- **位置**: `frontEnd/src/assets/icons/icon-camera.svg`
- **尺寸**: 16x16 px
- **用途**: 头像上传按钮图标
- **当前状态**: 使用Emoji占位符 "📷" (需要替换)
- **设计要求**: 相机风格图标
- **颜色**: #495057

### 3. 密码显示/隐藏图标

#### 3.1 眼睛图标 - 关闭状态 (Eye Close Icon)
- **文件名**: `icon-eye-close.svg`
- **位置**: `frontEnd/src/assets/icons/icon-eye-close.svg`
- **尺寸**: 18x18 px
- **用途**: 密码输入框隐藏密码状态
- **当前状态**: 使用Emoji占位符 "👁️‍🗨️" (需要替换)
- **设计要求**: 眼睛带斜线图标
- **颜色**: #9ca3af，Hover时 #667eea

#### 3.2 眼睛图标 - 打开状态 (Eye Open Icon)
- **文件名**: `icon-eye-open.svg`
- **位置**: `frontEnd/src/assets/icons/icon-eye-open.svg`
- **尺寸**: 18x18 px
- **用途**: 密码输入框显示密码状态
- **当前状态**: 使用Emoji占位符 "👁️" (需要替换)
- **设计要求**: 眼睛风格图标
- **颜色**: #9ca3af，Hover时 #667eea

### 4. 设备图标（登录记录）

#### 4.1 Windows设备图标 (Windows Icon)
- **文件名**: `icon-device-windows.svg`
- **位置**: `frontEnd/src/assets/icons/icon-device-windows.svg`
- **尺寸**: 24x24 px
- **用途**: 登录记录中的Windows设备标识
- **当前状态**: 使用Emoji占位符 "💻" (需要替换)
- **设计要求**: Windows电脑图标
- **颜色**: #6b7280

#### 4.2 iPhone设备图标 (iPhone Icon)
- **文件名**: `icon-device-iphone.svg`
- **位置**: `frontEnd/src/assets/icons/icon-device-iphone.svg`
- **尺寸**: 24x24 px
- **用途**: 登录记录中的iPhone设备标识
- **当前状态**: 使用Emoji占位符 "📱" (需要替换)
- **设计要求**: 手机风格图标
- **颜色**: #6b7280

#### 4.3 Mac设备图标 (Mac Icon)
- **文件名**: `icon-device-mac.svg`
- **位置**: `frontEnd/src/assets/icons/icon-device-mac.svg`
- **尺寸**: 24x24 px
- **用途**: 登录记录中的Mac设备标识
- **当前状态**: 使用Emoji占位符 "🖥️" (需要替换)
- **设计要求**: Mac电脑图标
- **颜色**: #6b7280

#### 4.4 Android设备图标 (Android Icon)
- **文件名**: `icon-device-android.svg`
- **位置**: `frontEnd/src/assets/icons/icon-device-android.svg`
- **尺寸**: 24x24 px
- **用途**: 登录记录中的Android设备标识
- **当前状态**: 使用Emoji占位符 "📱" (需要替换)
- **设计要求**: Android手机图标
- **颜色**: #6b7280

#### 4.5 通用设备图标 (Computer Icon)
- **文件名**: `icon-device-computer.svg`
- **位置**: `frontEnd/src/assets/icons/icon-device-computer.svg`
- **尺寸**: 24x24 px
- **用途**: 登录记录中无法识别设备时的通用图标
- **当前状态**: 使用Emoji占位符 "💻" (需要替换)
- **设计要求**: 通用电脑图标
- **颜色**: #6b7280

### 5. 加载动画图标

#### 5.1 加载图标 (Loading Icon)
- **文件名**: `icon-loading.svg`
- **位置**: `frontEnd/src/assets/icons/icon-loading.svg`
- **尺寸**: 16x16 px
- **用途**: 保存个人信息和修改密码时的加载状态
- **当前状态**: 使用CSS动画实现的旋转圆圈 (可保留或替换)
- **设计要求**: 圆形旋转动画
- **颜色**: #e5e7eb 边框，#667eea 顶部
- **动画**: 顺时针旋转，0.8s循环

---

## 仪表板页面 (DashboardNew.vue)

### 1. 统计卡片图标

#### 1.1 今日问答图标 (Chat Stat Icon)
- **文件名**: `icon-chat-stat.svg`
- **位置**: `frontEnd/src/assets/icons/icon-chat-stat.svg`
- **尺寸**: 28x28 px
- **用途**: 今日问答统计卡片
- **当前状态**: 使用Emoji占位符 "💬" (需要替换)
- **设计要求**: 对话气泡风格图标
- **颜色**: 蓝色系 (#dbeafe背景)

#### 1.2 搜索统计图标 (Search Stat Icon)
- **文件名**: `icon-search-btn.svg`
- **位置**: `frontEnd/src/assets/icons/icon-search-btn.svg`
- **尺寸**: 28x28 px
- **用途**: 搜索次数统计卡片
- **当前状态**: 使用Emoji占位符 "🔍" (需要替换)
- **设计要求**: 放大镜风格图标
- **颜色**: 绿色系 (#d1fae5背景)

#### 1.3 知识库统计图标 (KB Stat Icon)
- **文件名**: `icon-code.svg`
- **位置**: `frontEnd/src/assets/icons/icon-code.svg`
- **尺寸**: 28x28 px
- **用途**: 知识库数量统计卡片
- **当前状态**: 使用Emoji占位符 "💾" (需要替换)
- **设计要求**: 数据库/存储风格图标
- **颜色**: 黄色系 (#fef3c7背景)

#### 1.4 文档统计图标 (Doc Stat Icon)
- **文件名**: `icon-doc-type-pdf.svg`
- **位置**: `frontEnd/src/assets/icons/icon-doc-type-pdf.svg`
- **尺寸**: 28x28 px
- **用途**: 文档总数统计卡片
- **当前状态**: 使用Emoji占位符 "📄" (需要替换)
- **设计要求**: 文档/文件风格图标
- **颜色**: 紫色系 (#e9d5ff背景)

### 2. 说明文档卡片图标

#### 2.1 RAG系统图标 (RAG Icon)
- **文件名**: `icon-rag.svg`
- **位置**: `frontEnd/src/assets/icons/icon-rag.svg`
- **尺寸**: 24x24 px
- **用途**: RAG系统说明文档卡片
- **当前状态**: 使用Emoji占位符 "📚" (需要替换)
- **设计要求**: 书籍/知识风格图标
- **颜色**: 白色，用于橙色渐变背景

#### 2.2 知识库管理文档图标 (Knowledge Doc Icon)
- **文件名**: `icon-rag.svg`
- **位置**: `frontEnd/src/assets/icons/icon-rag.svg`
- **尺寸**: 24x24 px
- **用途**: 知识库管理说明文档卡片
- **当前状态**: 使用Emoji占位符 "📂" (需要替换)
- **设计要求**: 文件夹风格图标
- **颜色**: 白色，用于蓝色渐变背景

#### 2.3 文件上传文档图标 (Upload Doc Icon)
- **文件名**: `icon-rag.svg`
- **位置**: `frontEnd/src/assets/icons/icon-rag.svg`
- **尺寸**: 24x24 px
- **用途**: 文件上传说明文档卡片
- **当前状态**: 使用Emoji占位符 "📤" (需要替换)
- **设计要求**: 上传/导出风格图标
- **颜色**: 白色，用于绿色渐变背景

#### 2.4 模型管理文档图标 (Model Doc Icon)
- **文件名**: `icon-rag.svg`
- **位置**: `frontEnd/src/assets/icons/icon-rag.svg`
- **尺寸**: 24x24 px
- **用途**: 模型管理说明文档卡片
- **当前状态**: 使用Emoji占位符 "🤖" (需要替换)
- **设计要求**: AI/机器人风格图标
- **颜色**: 白色，用于棕色渐变背景

#### 2.5 用户管理文档图标 (User Doc Icon)
- **文件名**: `icon-rag.svg`
- **位置**: `frontEnd/src/assets/icons/icon-rag.svg`
- **尺寸**: 24x24 px
- **用途**: 用户管理说明文档卡片
- **当前状态**: 使用Emoji占位符 "👥" (需要替换)
- **设计要求**: 多用户/团队风格图标
- **颜色**: 白色，用于紫色渐变背景

#### 2.6 箭头图标 (Arrow Right Icon)
- **文件名**: `icon-arrow-right.svg`
- **位置**: `frontEnd/src/assets/icons/icon-arrow-right.svg`
- **尺寸**: 18x18 px
- **用途**: 说明文档卡片右侧箭头
- **当前状态**: 使用文本符号 "→" (需要替换)
- **设计要求**: 简洁箭头图标
- **颜色**: #d1d5db，Hover时 #667eea

### 3. 系统状态卡片图标

#### 3.1 LLM模型图标 (LLM Icon)
- **文件名**: `icon-llm.svg`
- **位置**: `frontEnd/src/assets/icons/icon-llm.svg`
- **尺寸**: 22x22 px
- **用途**: LLM模型状态卡片
- **当前状态**: 使用Emoji占位符 "🔥" (需要替换)
- **设计要求**: 火焰/AI风格图标
- **颜色**: 深色，用于白色背景

#### 3.2 向量模型图标 (Vector Icon)
- **文件名**: `icon-vector.svg`
- **位置**: `frontEnd/src/assets/icons/icon-vector.svg`
- **尺寸**: 22x22 px
- **用途**: 向量模型状态卡片
- **当前状态**: 使用Emoji占位符 "📊" (需要替换)
- **设计要求**: 图表/向量风格图标
- **颜色**: 深色，用于白色背景

#### 3.3 向量数据库图标 (Vector DB Icon)
- **文件名**: `icon-vector-db.svg`
- **位置**: `frontEnd/src/assets/icons/icon-vector-db.svg`
- **尺寸**: 22x22 px
- **用途**: 向量数据库状态卡片
- **当前状态**: 使用Emoji占位符 "💾" (需要替换)
- **设计要求**: 数据库风格图标
- **颜色**: 深色，用于白色背景

#### 3.4 关系数据库图标 (Relation DB Icon)
- **文件名**: `icon-relation-db.svg`
- **位置**: `frontEnd/src/assets/icons/icon-relation-db.svg`
- **尺寸**: 22x22 px
- **用途**: 关系数据库状态卡片
- **当前状态**: 使用Emoji占位符 "🗄️" (需要替换)
- **设计要求**: 服务器/数据库风格图标
- **颜色**: 深色，用于白色背景

#### 3.5 刷新图标 (Refresh Icon)
- **文件名**: `icon-refresh.svg`
- **位置**: `frontEnd/src/assets/icons/icon-refresh.svg`
- **尺寸**: 18x18 px
- **用途**: 系统状态刷新按钮
- **当前状态**: 使用文本符号 "↻" (需要替换)
- **设计要求**: 循环箭头风格图标
- **颜色**: #6b7280

#### 3.6 检查圆圈图标 (Check Circle Icon)
- **文件名**: `icon-check-circle.svg`
- **位置**: `frontEnd/src/assets/icons/icon-check-circle.svg`
- **尺寸**: 12x12 px
- **用途**: 系统运行正常指示器
- **当前状态**: 使用文本符号 "●" (需要替换)
- **设计要求**: 实心圆点图标
- **颜色**: #10b981（绿色）

---

## 主布局导航栏 - 管理员菜单图标

### 1. 仪表板图标 (Dashboard Icon)
- **文件名**: `icon-dashboard.svg`
- **位置**: `frontEnd/src/assets/icons/icon-dashboard.svg`
- **尺寸**: 20x20 px
- **用途**: 导航菜单"仪表板"项（管理员）
- **当前状态**: 使用Emoji占位符 "📊" (需要替换)
- **设计要求**: 仪表盘/图表风格图标

### 2. 用户管理图标 (User Management Icon)
- **文件名**: `icon-user-mgmt.svg`
- **位置**: `frontEnd/src/assets/icons/icon-user-mgmt.svg`
- **尺寸**: 20x20 px
- **用途**: 导航菜单"用户管理"项（管理员）
- **当前状态**: 使用Emoji占位符 "👥" (需要替换)
- **设计要求**: 多用户/团队风格图标

### 3. 知识库管理图标 (KB Management Icon)
- **文件名**: `icon-kb-mgmt.svg`
- **位置**: `frontEnd/src/assets/icons/icon-kb-mgmt.svg`
- **尺寸**: 20x20 px
- **用途**: 导航菜单"知识库管理"项（管理员）
- **当前状态**: 使用Emoji占位符 "📁" (需要替换)
- **设计要求**: 文件夹/知识库风格图标

### 4. 模型管理图标 (Model Management Icon)
- **文件名**: `icon-model-mgmt.svg`
- **位置**: `frontEnd/src/assets/icons/icon-model-mgmt.svg`
- **尺寸**: 20x20 px
- **用途**: 导航菜单"模型管理"项（管理员）
- **当前状态**: 使用Emoji占位符 "🤖" (需要替换)
- **设计要求**: AI/机器人风格图标

---

---

## 用户管理页面 (UserManagement.vue)

### 1. 页面标题区域图标

#### 1.1 时间图标 (Time Icon)
- **文件名**: `icon-time.svg`
- **位置**: `frontEnd/src/assets/icons/icon-time.svg`
- **尺寸**: 16x16 px
- **用途**: 页面右上角当前时间显示
- **当前状态**: 使用Emoji占位符 "🕐" (需要替换)
- **设计要求**: 时钟风格图标
- **颜色**: #6b7280

### 2. 统计卡片图标

#### 2.1 总用户数图标 (Users Total Icon)
- **文件名**: `icon-users-total.svg`
- **位置**: `frontEnd/src/assets/icons/icon-users-total.svg`
- **尺寸**: 28x28 px
- **用途**: 总用户数统计卡片
- **当前状态**: 使用Emoji占位符 "👥" (需要替换)
- **设计要求**: 多用户/团队风格图标
- **颜色**: 蓝色系 (#2563eb)，卡片背景 #dbeafe

#### 2.2 活跃用户图标 (Users Active Icon)
- **文件名**: `icon-users-active.svg`
- **位置**: `frontEnd/src/assets/icons/icon-users-active.svg`
- **尺寸**: 28x28 px
- **用途**: 活跃用户统计卡片
- **当前状态**: 使用Emoji占位符 "✅" (需要替换)
- **设计要求**: 勾选/激活风格图标
- **颜色**: 绿色系 (#10b981)，卡片背景 #d1fae5

#### 2.3 管理员图标 (Admin Users Icon)
- **文件名**: `icon-users-admin.svg`
- **位置**: `frontEnd/src/assets/icons/icon-users-admin.svg`
- **尺寸**: 28x28 px
- **用途**: 管理员数量统计卡片
- **当前状态**: 使用Emoji占位符 "👑" (需要替换)
- **设计要求**: 皇冠/管理员风格图标
- **颜色**: 黄色系 (#f59e0b)，卡片背景 #fef3c7

#### 2.4 禁用用户图标 (Disabled Users Icon)
- **文件名**: `icon-users-disabled.svg`
- **位置**: `frontEnd/src/assets/icons/icon-users-disabled.svg`
- **尺寸**: 28x28 px
- **用途**: 禁用用户统计卡片
- **当前状态**: 使用Emoji占位符 "🚫" (需要替换)
- **设计要求**: 禁止/禁用风格图标
- **颜色**: 红色系 (#ef4444)，卡片背景 #fee2e2

### 3. 搜索和操作区图标

#### 3.1 搜索输入框图标 (Search Input Icon)
- **文件名**: `icon-search-btn.svg`
- **位置**: `frontEnd/src/assets/icons/icon-search-btn.svg`
- **尺寸**: 18x18 px
- **用途**: 搜索输入框前的图标
- **当前状态**: 使用Emoji占位符 "🔍" (需要替换)
- **设计要求**: 放大镜风格图标
- **颜色**: #6b7280

#### 3.2 导出图标 (Export Icon)
- **文件名**: `icon-download.svg`
- **位置**: `frontEnd/src/assets/icons/icon-download.svg`
- **尺寸**: 16x16 px
- **用途**: 导出用户列表按钮
- **当前状态**: 使用Emoji占位符 "📥" (需要替换)
- **设计要求**: 下载/导出风格图标
- **颜色**: #10b981 (按钮文字色)

#### 3.3 添加用户图标 (Add User Icon)
- **文件名**: `icon-plus.svg`
- **位置**: `frontEnd/src/assets/icons/icon-pkus.svg`
- **尺寸**: 20x20 px
- **用途**: 添加用户按钮
- **当前状态**: 使用文本符号 "+" (需要替换)
- **设计要求**: 加号图标
- **颜色**: #ffffff (白色，用于蓝色按钮)

### 4. 用户表格角色和状态图标

#### 4.1 管理员角色图标 (Role Admin Icon)
- **文件名**: `icon-users-admin.svg`
- **位置**: `frontEnd/src/assets/icons/icon-users-admin.svg`
- **尺寸**: 14x14 px
- **用途**: 角色标签中的管理员图标
- **当前状态**: 使用Emoji占位符 "👑" (需要替换)
- **设计要求**: 皇冠风格图标
- **颜色**: #7c3aed (紫色)

#### 4.2 普通用户角色图标 (Role User Icon)
- **文件名**: `icon-role-user.svg`
- **位置**: `frontEnd/src/assets/icons/icon-role-user.svg`
- **尺寸**: 14x14 px
- **用途**: 角色标签中的普通用户图标
- **当前状态**: 使用Emoji占位符 "👤" (需要替换)
- **设计要求**: 用户轮廓风格图标
- **颜色**: #2563eb (蓝色)

### 5. 操作按钮图标

#### 5.1 编辑图标 (Edit Icon)
- **文件名**: `icon-edit-user.svg`
- **位置**: `frontEnd/src/assets/icons/icon-edit-user.svg`
- **尺寸**: 16x16 px
- **用途**: 编辑用户按钮
- **当前状态**: 使用Emoji占位符 "✏️" (需要替换)
- **设计要求**: 铅笔/编辑风格图标
- **颜色**: #6b7280，Hover时 #ffffff

#### 5.2 重置密码图标 (Reset Password Icon)
- **文件名**: `icon-reset-password.svg`
- **位置**: `frontEnd/src/assets/icons/icon-reset-password.svg`
- **尺寸**: 16x16 px
- **用途**: 重置用户密码按钮
- **当前状态**: 使用Emoji占位符 "🔑" (需要替换)
- **设计要求**: 钥匙/密码风格图标
- **颜色**: #6b7280，Hover时 #ffffff

#### 5.3 启用图标 (Enable Icon)
- **文件名**: `icon-enable-user.svg`
- **位置**: `frontEnd/src/assets/icons/icon-enable-user.svg`
- **尺寸**: 16x16 px
- **用途**: 启用用户按钮
- **当前状态**: 使用Emoji占位符 "▶️" (需要替换)
- **设计要求**: 播放/启用风格图标
- **颜色**: #6b7280，Hover时 #ffffff (绿色按钮背景 #10b981)

#### 5.4 禁用图标 (Disable Icon)
- **文件名**: `icon-disable-user.svg`
- **位置**: `frontEnd/src/assets/icons/icon-disable-user.svg`
- **尺寸**: 16x16 px
- **用途**: 禁用用户按钮
- **当前状态**: 使用Emoji占位符 "⏸️" (需要替换)
- **设计要求**: 暂停/禁用风格图标
- **颜色**: #6b7280，Hover时 #ffffff

#### 5.5 删除图标 (Delete Icon)
- **文件名**: `icon-delete-user.svg`
- **位置**: `frontEnd/src/assets/icons/icon-delete-user.svg`
- **尺寸**: 16x16 px
- **用途**: 删除用户按钮
- **当前状态**: 使用Emoji占位符 "🗑️" (需要替换)
- **设计要求**: 垃圾桶风格图标
- **颜色**: #6b7280，Hover时 #ffffff (红色按钮背景 #ef4444)

---

## 知识库管理页面 (KnowledgeManagement.vue)

### 1. 页面功能图标

#### 1.1 添加图标 (Add Icon)
- **文件名**: `icon-plus.svg`
- **位置**: `frontEnd/src/assets/icons/icon-plus.svg`
- **尺寸**: 18x18 px
- **用途**: 创建知识库按钮图标
- **当前状态**: 使用文本符号 "+" (需要替换)
- **设计要求**: 加号图标
- **颜色**: 白色 (#ffffff)，用于紫色渐变按钮

#### 1.2 编辑知识库图标 (Edit KB Icon)
- **文件名**: `icon-edit-user.svg`
- **位置**: `frontEnd/src/assets/icons/icon-edit-user.svg`
- **尺寸**: 16x16 px
- **用途**: 知识库卡片编辑按钮
- **当前状态**: 使用Emoji占位符 "✏️" (需要替换)
- **设计要求**: 铅笔/编辑风格图标
- **颜色**: 深灰色

#### 1.3 删除知识库图标 (Delete KB Icon)
- **文件名**: `icon-delete-doc.svg`
- **位置**: `frontEnd/src/assets/icons/icon-delete-doc.svg`
- **尺寸**: 16x16 px
- **用途**: 知识库卡片删除按钮
- **当前状态**: 使用Emoji占位符 "🗑️" (需要替换)
- **设计要求**: 垃圾桶风格图标
- **颜色**: 深灰色

### 2. 知识库卡片图标

#### 2.1 知识库主图标 (KB Main Icon)
- **文件名**: `icon-code.svg`
- **位置**: `frontEnd/src/assets/icons/icon-code.svg`
- **尺寸**: 24x24 px
- **用途**: 知识库卡片主图标
- **当前状态**: 使用Emoji占位符 "📚" (需要替换)
- **设计要求**: 书籍/知识库风格图标
- **颜色**: 不需要背景色

---

## 创建知识库对话框 (CreateKnowledgeBaseDialog.vue)

### 1. 步骤指示器图标

#### 1.1 关闭对话框图标 (Close Dialog Icon)
- **文件名**: `icon-close-dialog-kb.svg`
- **位置**: `frontEnd/src/assets/icons/icon-close-dialog-kb.svg`
- **尺寸**: 18x18 px
- **用途**: 对话框关闭按钮
- **当前状态**: 使用文本符号 "✕" (需要替换)
- **设计要求**: 叉号风格图标
- **颜色**: #666666

### 2. 标签输入图标

#### 2.1 标签删除图标 (Tag Remove Icon)
- **文件名**: `icon-tag-remove.svg`
- **位置**: `frontEnd/src/assets/icons/icon-tag-remove.svg`
- **尺寸**: 14x14 px
- **用途**: 标签删除按钮
- **当前状态**: 使用文本符号 "✕" (需要替换)
- **设计要求**: 小叉号图标
- **颜色**: #9ca3af

### 3. 文件上传图标

#### 3.1 上传区域图标 (Upload Area Icon)
- **文件名**: `icon-upload-area.svg`
- **位置**: `frontEnd/src/assets/icons/icon-upload-area.svg`
- **尺寸**: 48x48 px
- **用途**: 上传区域占位图标
- **当前状态**: 使用Emoji占位符 "📤" (需要替换)
- **设计要求**: 上传/箭头向上风格图标
- **颜色**: #9ca3af

---

## 知识库详情页面 (KnowledgeBaseDetail.vue)

### 1. 页面导航图标

#### 1.1 返回按钮图标 (Back Icon)
- **文件名**: `icon-back-arrow.svg`
- **位置**: `frontEnd/src/assets/icons/icon-back-arrow.svg`
- **尺寸**: 20x20 px
- **用途**: 返回按钮
- **当前状态**: 使用文本符号 "←" (需要替换)
- **设计要求**: 左箭头风格图标
- **颜色**: #666666

#### 1.2 上传文档图标 (Upload Doc Icon)
- **文件名**: `icon-upload-doc-btn.svg`
- **位置**: `frontEnd/src/assets/icons/icon-upload-doc-btn.svg`
- **尺寸**: 18x18 px
- **用途**: 上传文档按钮
- **当前状态**: 使用Emoji占位符 "📤" (需要替换)
- **设计要求**: 上传/导入风格图标
- **颜色**: #333333

### 2. 统计卡片图标

#### 2.1 文档总数图标 (Doc Count Icon)
- **文件名**: `icon-doc-count.svg`
- **位置**: `frontEnd/src/assets/icons/icon-doc-count.svg`
- **尺寸**: 28x28 px
- **用途**: 文档总数统计卡片
- **当前状态**: 使用Emoji占位符 "📄" (需要替换)
- **设计要求**: 文档/文件风格图标
- **颜色**: 蓝色系

#### 2.2 存储大小图标 (Storage Size Icon)
- **文件名**: `icon-storage-size.svg`
- **位置**: `frontEnd/src/assets/icons/icon-storage-size.svg`
- **尺寸**: 28x28 px
- **用途**: 存储大小统计卡片
- **当前状态**: 使用Emoji占位符 "💾" (需要替换)
- **设计要求**: 磁盘/存储风格图标
- **颜色**: 绿色系

#### 2.3 查看人数图标 (Viewers Icon)
- **文件名**: `icon-viewers-count.svg`
- **位置**: `frontEnd/src/assets/icons/icon-viewers-count.svg`
- **尺寸**: 28x28 px
- **用途**: 查看人数统计卡片
- **当前状态**: 使用Emoji占位符 "👁️" (需要替换)
- **设计要求**: 眼睛/查看风格图标
- **颜色**: 黄色系

### 3. 文档表格图标

#### 3.1 文档类型图标 (Doc Type Icon)
- **文件名**: `icon-doc-type-pdf.svg`
- **位置**: `frontEnd/src/assets/icons/icon-doc-type-pdf.svg`
- **尺寸**: 20x20 px
- **用途**: 文档列表中的PDF文件图标
- **当前状态**: 使用Emoji占位符 "📄" (需要替换)
- **设计要求**: PDF文档风格图标
- **颜色**: #ef4444 (红色)

#### 3.2 查看文档图标 (View Doc Icon)
- **文件名**: `icon-eye-open.svg`
- **位置**: `frontEnd/src/assets/icons/icon-eye-open.svg`
- **尺寸**: 18x18 px
- **用途**: 文档操作-查看按钮
- **当前状态**: 使用Emoji占位符 "👁️" (需要替换)
- **设计要求**: 眼睛风格图标
- **颜色**: #666666

#### 3.3 删除文档图标 (Delete Doc Icon)
- **文件名**: `icon-delete-doc.svg`
- **位置**: `frontEnd/src/assets/icons/icon-delete-doc.svg`
- **尺寸**: 18x18 px
- **用途**: 文档操作-删除按钮
- **当前状态**: 使用Emoji占位符 "🗑️" (需要替换)
- **设计要求**: 垃圾桶风格图标
- **颜色**: #666666

---

## 上传文档对话框 (UploadDocumentDialog.vue)

### 1. 上传区域图标

#### 1.1 上传占位图标 (Upload Placeholder Icon)
- **文件名**: `icon-upload-placeholder.svg`
- **位置**: `frontEnd/src/assets/icons/icon-upload-placeholder.svg`
- **尺寸**: 56x56 px
- **用途**: 上传区域中央占位图标
- **当前状态**: 使用Emoji占位符 "📤" (需要替换)
- **设计要求**: 上传/箭头向上风格图标
- **颜色**: #9ca3af

### 2. 文件列表图标

#### 2.1 文件图标 (File Icon)
- **文件名**: `icon-file-item.svg`
- **位置**: `frontEnd/src/assets/icons/icon-file-item.svg`
- **尺寸**: 24x24 px
- **用途**: 文件列表项图标
- **当前状态**: 使用Emoji占位符 "📄" (需要替换)
- **设计要求**: 文档风格图标
- **颜色**: #667eea

#### 2.2 移除文件图标 (Remove File Icon)
- **文件名**: `icon-remove-file.svg`
- **位置**: `frontEnd/src/assets/icons/icon-remove-file.svg`
- **尺寸**: 16x16 px
- **用途**: 移除文件按钮
- **当前状态**: 使用文本符号 "✕" (需要替换)
- **设计要求**: 叉号风格图标
- **颜色**: #666666

---

## 文档预览页面 (DocumentPreview.vue)

### 1. 页面功能图标

#### 1.1 返回图标 (Back Icon)
- **文件名**: `icon-back-arrow.svg`
- **位置**: `frontEnd/src/assets/icons/icon-back-arrow.svg`
- **尺寸**: 20x20 px
- **用途**: 返回按钮
- **当前状态**: 使用文本符号 "←" (需要替换)
- **设计要求**: 左箭头风格图标
- **颜色**: #666666

#### 1.2 下载文档图标 (Download Doc Icon)
- **文件名**: `icon-download.svg`
- **位置**: `frontEnd/src/assets/icons/icon-download.svg`
- **尺寸**: 18x18 px
- **用途**: 下载文档按钮
- **当前状态**: 使用Emoji占位符 "📥" (需要替换)
- **设计要求**: 下载/箭头向下风格图标
- **颜色**: #333333

### 2. 状态提示图标

#### 2.1 警告图标 (Warning Icon)
- **文件名**: `icon-warning-preview.svg`
- **位置**: `frontEnd/src/assets/icons/icon-warning-preview.svg`
- **尺寸**: 64x64 px
- **用途**: 不支持预览类型的警告提示
- **当前状态**: 使用Emoji占位符 "⚠️" (需要替换)
- **设计要求**: 警告/感叹号风格图标
- **颜色**: #f59e0b

#### 2.2 错误图标 (Error Icon)
- **文件名**: `icon-error-preview.svg`
- **位置**: `frontEnd/src/assets/icons/icon-error-preview.svg`
- **尺寸**: 64x64 px
- **用途**: 文档加载失败的错误提示
- **当前状态**: 使用Emoji占位符 "❌" (需要替换)
- **设计要求**: 错误/叉号风格图标
- **颜色**: #ef4444

---

## 编辑知识库对话框 (EditKnowledgeBaseDialog.vue)

### 1. 对话框功能图标

#### 1.1 关闭图标 (Close Icon)
- **文件名**: `icon-close-dialog.svg`
- **位置**: `frontEnd/src/assets/icons/icon-close-dialog.svg`
- **尺寸**: 20x20 px
- **用途**: 对话框关闭按钮
- **当前状态**: 使用文本符号 "✕" (需要替换)
- **设计要求**: 叉号/关闭风格图标
- **颜色**: #666666

#### 1.2 帮助提示图标 (Help Icon)
- **文件名**: `icon-help-tooltip.svg`
- **位置**: `frontEnd/src/assets/icons/icon-help-tooltip.svg`
- **尺寸**: 16x16 px
- **用途**: 相似度阈值字段的帮助提示图标
- **当前状态**: 使用文本符号 "?" (需要替换)
- **设计要求**: 问号/帮助风格图标，圆形背景
- **颜色**: #666666 (问号), #e5e7eb (背景)

### 2. 标签相关图标

#### 2.1 移除标签图标 (Remove Tag Icon)
- **文件名**: `icon-remove-tag.svg`
- **位置**: `frontEnd/src/assets/icons/icon-remove-tag.svg`
- **尺寸**: 14x14 px
- **用途**: 标签的删除按钮
- **当前状态**: 使用文本符号 "✕" (需要替换)
- **设计要求**: 小叉号风格图标
- **颜色**: 白色 (#ffffff)，用于紫色渐变标签背景

### 说明
- **复用图标**: EditKnowledgeBaseDialog 主要复用了现有的图标设计，如关闭按钮和删除标签图标
- **无新增图标**: 该组件不需要特殊的新图标，所有图标都可以使用已有的通用图标或简单符号

---

## 模型管理页面 (ModelManagement.vue)

### 1. 页面标题区域图标

#### 1.1 时间图标 (Time Icon)
- **文件名**: `icon-time.svg`
- **位置**: `frontEnd/src/assets/icons/icon-time.svg`
- **尺寸**: 16x16 px
- **用途**: 页面右上角当前时间显示
- **当前状态**: 使用Emoji占位符 "🕐" (需要替换)
- **设计要求**: 时钟风格图标
- **颜色**: #6b7280

### 2. 统计卡片图标

#### 2.1 LLM模型图标 (LLM Model Icon)
- **文件名**: `icon-llm.svg`
- **位置**: `frontEnd/src/assets/icons/icon-llm-stat.svg`
- **尺寸**: 28x28 px
- **用途**: LLM模型统计卡片
- **当前状态**: 使用Emoji占位符 "🔥" (需要替换)
- **设计要求**: 火焰/AI风格图标
- **颜色**: 蓝色系，卡片背景 #dbeafe

#### 2.2 向量模型图标 (Embedding Model Icon)
- **文件名**: `icon-vector.svg`
- **位置**: `frontEnd/src/assets/icons/icon-embedding-stat.svg`
- **尺寸**: 28x28 px
- **用途**: 向量模型统计卡片
- **当前状态**: 使用Emoji占位符 "📊" (需要替换)
- **设计要求**: 图表/向量风格图标
- **颜色**: 绿色系，卡片背景 #d1fae5

#### 2.3 在线服务图标 (Online Service Icon)
- **文件名**: `icon-online-service.svg`
- **位置**: `frontEnd/src/assets/icons/icon-online-service.svg`
- **尺寸**: 28x28 px
- **用途**: 在线服务统计卡片
- **当前状态**: 使用Emoji占位符 "✅" (需要替换)
- **设计要求**: 勾选/在线风格图标
- **颜色**: 黄色系，卡片背景 #fef3c7

#### 2.4 离线服务图标 (Offline Service Icon)
- **文件名**: `icon-offline-service.svg`
- **位置**: `frontEnd/src/assets/icons/icon-offline-service.svg`
- **尺寸**: 28x28 px
- **用途**: 离线服务统计卡片
- **当前状态**: 使用Emoji占位符 "🚫" (需要替换)
- **设计要求**: 禁止/离线风格图标
- **颜色**: 红色系，卡片背景 #fee2e2

### 3. 操作按钮图标

#### 3.1 添加模型图标 (Add Model Icon)
- **文件名**: `icon-plus.svg`
- **位置**: `frontEnd/src/assets/icons/icon-plus.svg`
- **尺寸**: 18x18 px
- **用途**: 添加模型按钮
- **当前状态**: 使用文本符号 "+" (需要替换)
- **设计要求**: 加号图标
- **颜色**: 白色 (#ffffff)，用于紫色渐变按钮

#### 3.2 健康检查图标 (Health Check Icon)
- **文件名**: `icon-health-check.svg`
- **位置**: `frontEnd/src/assets/icons/icon-health-check.svg`
- **尺寸**: 18x18 px
- **用途**: 健康检查按钮
- **当前状态**: 使用Emoji占位符 "🔄" (需要替换)
- **设计要求**: 循环/刷新风格图标，支持旋转动画
- **颜色**: #667eea

### 4. 模型卡片图标

#### 4.1 模型状态在线图标 (Model Online Icon)
- **文件名**: `icon-model-online.svg`
- **位置**: `frontEnd/src/assets/icons/icon-model-online.svg`
- **尺寸**: 8x8 px
- **用途**: 模型在线状态指示点
- **当前状态**: 使用CSS绘制的圆点 (可保留或替换)
- **设计要求**: 实心圆点
- **颜色**: #10b981（绿色）

#### 4.2 模型状态离线图标 (Model Offline Icon)
- **文件名**: `icon-model-offline.svg`
- **位置**: `frontEnd/src/assets/icons/icon-model-offline.svg`
- **尺寸**: 8x8 px
- **用途**: 模型离线状态指示点
- **当前状态**: 使用CSS绘制的圆点 (可保留或替换)
- **设计要求**: 实心圆点
- **颜色**: #ef4444（红色）

#### 4.3 默认标记图标 (Default Badge Icon)
- **文件名**: `icon-microservice-suggest.svg`
- **位置**: `frontEnd/src/assets/icons/icon-microservice-suggest.svg`
- **尺寸**: 12x12 px
- **用途**: 默认模型标记
- **当前状态**: 使用Emoji占位符 "⭐" (需要替换)
- **设计要求**: 星星风格图标
- **颜色**: 白色，用于黄色渐变背景

#### 4.4 LLM模型主图标 (LLM Model Main Icon)
- **文件名**: `icon-llm.svg`
- **位置**: `frontEnd/src/assets/icons/icon-llm.svg`
- **尺寸**: 24x24 px
- **用途**: LLM模型卡片主图标
- **当前状态**: 使用Emoji占位符 "🤖" (需要替换)
- **设计要求**: 机器人/AI风格图标
- **颜色**: 白色，用于紫色渐变背景

#### 4.5 向量模型主图标 (Embedding Model Main Icon)
- **文件名**: `icon-vector.svg`
- **位置**: `frontEnd/src/assets/icons/icon-vector.svg`
- **尺寸**: 24x24 px
- **用途**: 向量模型卡片主图标
- **当前状态**: 使用Emoji占位符 "🤖" (需要替换)
- **设计要求**: 机器人/向量风格图标
- **颜色**: 白色，用于绿色渐变背景

### 5. 模型操作图标

#### 5.1 测试模型图标 (Test Model Icon)
- **文件名**: `icon-test-model.svg`
- **位置**: `frontEnd/src/assets/icons/icon-test-model.svg`
- **尺寸**: 16x16 px
- **用途**: 测试模型连接按钮
- **当前状态**: 使用Emoji占位符 "🔬" (需要替换)
- **设计要求**: 实验/测试风格图标
- **颜色**: #6b7280

#### 5.2 配置模型图标 (Config Model Icon)
- **文件名**: `icon-config-model.svg`
- **位置**: `frontEnd/src/assets/icons/icon-config-model.svg`
- **尺寸**: 16x16 px
- **用途**: 配置/编辑模型按钮
- **当前状态**: 使用Emoji占位符 "⚙️" (需要替换)
- **设计要求**: 齿轮/设置风格图标
- **颜色**: #6b7280

#### 5.3 设为默认图标 (Set Default Icon)
- **文件名**: `icon-microservice-suggest.svg`
- **位置**: `frontEnd/src/assets/icons/icon-microservice-suggest.svg`
- **尺寸**: 16x16 px
- **用途**: 设为默认模型按钮
- **当前状态**: 使用Emoji占位符 "⭐" (需要替换)
- **设计要求**: 星星风格图标
- **颜色**: #6b7280

#### 5.4 删除模型图标 (Delete Model Icon)
- **文件名**: `icon-delete-doc.svg`
- **位置**: `frontEnd/src/assets/icons/icon-delete-doc.svg`
- **尺寸**: 16x16 px
- **用途**: 删除模型按钮
- **当前状态**: 使用Emoji占位符 "🗑️" (需要替换)
- **设计要求**: 垃圾桶风格图标
- **颜色**: #6b7280

---

## 模型对话框 (ModelDialog.vue)

### 1. 对话框控制图标

#### 1.1 关闭对话框图标 (Close Dialog Icon)
- **文件名**: `icon-close-model-dialog.svg`
- **位置**: `frontEnd/src/assets/icons/icon-close-model-dialog.svg`
- **尺寸**: 18x18 px
- **用途**: 模型对话框关闭按钮
- **当前状态**: 使用文本符号 "✕" (需要替换)
- **设计要求**: 叉号风格图标
- **颜色**: #6b7280

### 2. 表单辅助图标

#### 2.1 必填标记图标 (Required Icon)
- **当前状态**: 使用CSS星号 "*" (可保留)
- **设计要求**: 简单的星号标记
- **颜色**: #ef4444（红色）

#### 2.2 加载图标 (Loading Icon)
- **文件名**: `icon-loading-model.svg`
- **位置**: `frontEnd/src/assets/icons/icon-loading-model.svg`
- **尺寸**: 14x14 px
- **用途**: 对话框提交按钮加载状态
- **当前状态**: 使用CSS动画实现的旋转圆圈 (可保留或替换)
- **设计要求**: 圆形旋转动画
- **颜色**: 白色，用于紫色渐变按钮
- **动画**: 顺时针旋转，0.6s循环

---

## 待补充的图标

随着项目开发进度，其他页面需要的图标将在此处补充：

- [x] 知识库详情页面图标
- [x] 知识库管理页面图标
- [x] 编辑知识库对话框图标
- [x] 模型管理页面图标

**备注**: 文件上传功能已集成到知识库管理页面中，不再需要独立的文件上传页面和相关图标。

---

## 更新日志

| 日期 | 版本 | 更新内容 | 更新人 |
|------|------|---------|--------|
| 2025-10-01 | v1.0 | 创建文档，添加登录页面所需图标 | AI Assistant |
| 2025-10-01 | v1.1 | 添加主布局和我的知识库页面所需图标 | AI Assistant |
| 2025-10-01 | v1.2 | 添加智能问答页面所需图标(15个) | AI Assistant |
| 2025-10-01 | v1.3 | 添加文档搜索页面所需图标(10个) | AI Assistant |
| 2025-10-01 | v1.4 | 添加个人设置页面所需图标(11个) | AI Assistant |
| 2025-10-02 | v1.5 | 添加仪表板页面所需图标(17个)和管理员菜单图标(5个) | AI Assistant |
| 2025-10-02 | v1.6 | 添加用户管理页面所需图标(17个，移除数据统计图标) | AI Assistant |
| 2025-10-03 | v1.7 | 添加知识库管理相关页面图标(20个)：知识库管理主页、创建知识库对话框、知识库详情页、上传文档对话框、文档预览页 | AI Assistant |
| 2025-10-03 | v1.8 | 添加编辑知识库对话框图标(3个)：关闭按钮、帮助提示、标签移除 | AI Assistant |
| 2025-10-04 | v1.9 | 添加模型管理页面所需图标(17个)：统计卡片图标、模型卡片图标、操作按钮图标、状态指示图标、模型对话框图标 | AI Assistant |

---

**注意事项**:
1. 所有图标资源应放在 `frontEnd/src/assets/icons/` 目录下
2. 所有图片资源应放在 `frontEnd/src/assets/images/` 目录下
3. 使用图标前请确保已获得相应的使用授权
4. 建议使用SVG格式以保证在高分辨率屏幕上的清晰度
5. 图标更新后需同步更新本文档

