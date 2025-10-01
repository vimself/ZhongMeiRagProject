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

## 待补充的图标

随着项目开发进度，其他页面需要的图标将在此处补充：

- [ ] 知识库管理页面图标
- [ ] 文档上传页面图标
- [ ] 智能问答页面图标
- [ ] 搜索页面图标
- [ ] 用户管理页面图标
- [ ] 模型管理页面图标
- [ ] 个人中心页面图标
- [ ] 导航菜单图标

---

## 更新日志

| 日期 | 版本 | 更新内容 | 更新人 |
|------|------|---------|--------|
| 2025-10-01 | v1.0 | 创建文档，添加登录页面所需图标 | AI Assistant |

---

**注意事项**:
1. 所有图标资源应放在 `frontEnd/src/assets/icons/` 目录下
2. 所有图片资源应放在 `frontEnd/src/assets/images/` 目录下
3. 使用图标前请确保已获得相应的使用授权
4. 建议使用SVG格式以保证在高分辨率屏幕上的清晰度
5. 图标更新后需同步更新本文档

