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
- **文件名**: `icon-book.svg`
- **位置**: `frontEnd/src/assets/icons/icon-book.svg`
- **尺寸**: 24x24 px
- **用途**: 产品手册卡片图标
- **当前状态**: 需要创建(使用CSS渐变背景)
- **设计要求**: 书本/手册风格图标
- **颜色**: 绿色渐变背景

#### 4.3 运维文档图标 (Gear Icon)
- **文件名**: `icon-gear.svg`
- **位置**: `frontEnd/src/assets/icons/icon-gear.svg`
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
- **文件名**: `icon-loading-spinner.svg`
- **位置**: `frontEnd/src/assets/icons/icon-loading-spinner.svg`
- **尺寸**: 32x32 px
- **用途**: 页面加载中状态
- **当前状态**: 使用CSS动画实现的旋转圆圈 (可保留或替换)
- **设计要求**: 圆形旋转动画

#### 5.2 空状态图标 (Empty Icon)
- **文件名**: `icon-empty.svg`
- **位置**: `frontEnd/src/assets/icons/icon-empty.svg`
- **尺寸**: 64x64 px
- **用途**: 知识库列表为空时的占位图标
- **当前状态**: 使用Emoji占位符 "📭" (需要替换)
- **设计要求**: 空文件夹/空盒子风格

### 6. 开发中占位图标

#### 6.1 施工图标 (Construction Icon)
- **文件名**: `icon-construction.svg`
- **位置**: `frontEnd/src/assets/icons/icon-construction.svg`
- **尺寸**: 80x80 px
- **用途**: 功能开发中页面占位
- **当前状态**: 使用Emoji占位符 "🚧" (需要替换)
- **设计要求**: 施工/建设中风格图标

---

## 待补充的图标

随着项目开发进度，其他页面需要的图标将在此处补充：

- [ ] 文档上传页面图标
- [ ] 用户管理页面图标
- [ ] 模型管理页面图标
- [ ] 知识库详情页面图标
- [ ] 智能问答对话页面图标
- [ ] 搜索结果页面图标

---

## 更新日志

| 日期 | 版本 | 更新内容 | 更新人 |
|------|------|---------|--------|
| 2025-10-01 | v1.0 | 创建文档，添加登录页面所需图标 | AI Assistant |
| 2025-10-01 | v1.1 | 添加主布局和我的知识库页面所需图标 | AI Assistant |

---

**注意事项**:
1. 所有图标资源应放在 `frontEnd/src/assets/icons/` 目录下
2. 所有图片资源应放在 `frontEnd/src/assets/images/` 目录下
3. 使用图标前请确保已获得相应的使用授权
4. 建议使用SVG格式以保证在高分辨率屏幕上的清晰度
5. 图标更新后需同步更新本文档

