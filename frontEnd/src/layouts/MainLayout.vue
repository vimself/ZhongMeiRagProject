<template>
  <div class="main-layout">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <!-- Logo -->
      <div class="sidebar-logo">
        <i class="logo-icon"></i>
        <div class="logo-text">
          <div class="system-name">RAG系统</div>
          <div class="system-desc">知识问答</div>
        </div>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <template v-for="item in menuItems" :key="item.path || item.label">
          <!-- 分隔符 -->
          <div v-if="item.type === 'divider'" class="nav-divider">
            <span class="divider-label">{{ item.label }}</span>
          </div>
          <!-- 菜单项 -->
          <router-link 
            v-else
            :to="item.path"
            class="nav-item"
            :class="{ 'active': isActive(item.path) }"
          >
            <i :class="item.icon"></i>
            <span>{{ item.name }}</span>
          </router-link>
        </template>
      </nav>

      <!-- 底部用户信息 -->
      <div class="sidebar-footer">
        <div class="user-info" @click="toggleUserMenu">
          <div class="user-avatar">
            <i class="icon-user-avatar"></i>
          </div>
          <div class="user-details">
            <div class="user-name">{{ userInfo?.name }}</div>
            <div class="user-role">{{ userInfo?.role === 'admin' ? '管理员' : '普通用户' }}</div>
          </div>
          <i class="icon-more"></i>
        </div>
        
        <!-- 用户菜单 -->
        <div v-if="showUserMenu" class="user-menu">
          <div class="menu-item" @click="goToProfile">
            <i class="icon-profile"></i>
            <span>个人中心</span>
          </div>
          <div class="menu-item" @click="handleLogout">
            <i class="icon-logout"></i>
            <span>退出登录</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- 右侧内容区 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getUserInfo, clearAll } from '../utils/storage'
import { logout } from '../api/authApi'

const router = useRouter()
const route = useRoute()
const userInfo = ref(null)
const showUserMenu = ref(false)

// 基础菜单（普通用户）
const baseMenuItems = [
  {
    path: '/knowledge',
    name: '我的知识库',
    icon: 'icon-knowledge'
  },
  {
    path: '/chat',
    name: '智能问答',
    icon: 'icon-chat'
  },
  {
    path: '/search',
    name: '文档搜索',
    icon: 'icon-search'
  }
]

// 管理员菜单
const adminMenuItems = [
  {
    path: '/dashboard',
    name: '仪表板',
    icon: 'icon-dashboard'
  },
  {
    path: '/chat',
    name: '智能问答',
    icon: 'icon-chat'
  },
  {
    path: '/search',
    name: '文档搜索',
    icon: 'icon-search'
  },
  {
    type: 'divider',
    label: '管理功能'
  },
  {
    path: '/admin/users',
    name: '用户管理',
    icon: 'icon-user-mgmt'
  },
  {
    path: '/admin/knowledge',
    name: '知识库管理',
    icon: 'icon-kb-mgmt'
  },
  {
    path: '/admin/upload',
    name: '文件上传',
    icon: 'icon-upload-mgmt'
  },
  {
    path: '/admin/models',
    name: '模型管理',
    icon: 'icon-model-mgmt'
  }
]

// 根据用户角色决定显示的菜单
const menuItems = computed(() => {
  return userInfo.value?.role === 'admin' ? adminMenuItems : baseMenuItems
})

onMounted(() => {
  userInfo.value = getUserInfo()
})

/**
 * 判断菜单项是否激活
 */
function isActive(path) {
  return route.path.startsWith(path)
}

/**
 * 切换用户菜单
 */
function toggleUserMenu() {
  showUserMenu.value = !showUserMenu.value
}

/**
 * 前往个人中心
 */
function goToProfile() {
  showUserMenu.value = false
  router.push('/profile')
}

/**
 * 退出登录
 */
async function handleLogout() {
  showUserMenu.value = false
  
  try {
    await logout()
  } catch (error) {
    console.error('登出失败:', error)
  } finally {
    clearAll()
    router.push('/login')
  }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
  background: #f5f7fa;
}

/* 左侧导航栏 */
.sidebar {
  width: 220px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 100;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 88px;
  padding: 0 24px;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.logo-icon {
  display: block;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  flex-shrink: 0;
}

.logo-text {
  flex: 1;
}

.system-name {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  line-height: 1.2;
}

.system-desc {
  font-size: 12px;
  color: #666666;
  line-height: 1.2;
  margin-top: 2px;
}

/* 导航菜单 */
.sidebar-nav {
  flex: 1;
  padding: 20px 16px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  margin-bottom: 4px;
  border-radius: 8px;
  color: #4b5563;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s;
  cursor: pointer;
}

.nav-item i {
  font-size: 20px;
  width: 20px;
  text-align: center;
}

.nav-item:hover {
  background: #f3f4f6;
  color: #667eea;
}

.nav-item.active {
  background: #ede9fe;
  color: #667eea;
  font-weight: 500;
}

/* 底部用户信息 */
.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #e5e7eb;
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.user-info:hover {
  background: #f3f4f6;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-user-avatar::before {
  content: '👤';
  font-size: 20px;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-role {
  font-size: 12px;
  color: #666666;
  line-height: 1.2;
  margin-top: 2px;
}

.icon-more::before {
  content: '⋮';
  font-size: 18px;
  color: #999999;
}

/* 用户菜单 */
.user-menu {
  position: absolute;
  bottom: 100%;
  left: 16px;
  right: 16px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 8px;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  font-size: 14px;
  color: #4b5563;
  cursor: pointer;
  transition: background 0.3s;
}

.menu-item:hover {
  background: #f3f4f6;
}

.menu-item i {
  font-size: 18px;
  width: 18px;
  text-align: center;
}

/* 右侧内容区 */
.main-content {
  flex: 1;
  margin-left: 220px;
  min-height: 100vh;
}

/* 导航分隔符 */
.nav-divider {
  margin: 16px 0 12px 0;
  padding: 0 18px;
}

.divider-label {
  font-size: 12px;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 图标占位符 */
.icon-dashboard::before {
  content: '📊';
}

.icon-knowledge::before {
  content: '📚';
}

.icon-chat::before {
  content: '💬';
}

.icon-search::before {
  content: '🔍';
}

.icon-user-mgmt::before {
  content: '👥';
}

.icon-kb-mgmt::before {
  content: '📁';
}

.icon-upload-mgmt::before {
  content: '📤';
}

.icon-model-mgmt::before {
  content: '🤖';
}

.icon-profile::before {
  content: '👤';
}

.icon-logout::before {
  content: '🚪';
}
</style>

