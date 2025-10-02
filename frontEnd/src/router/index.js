/**
 * 路由配置
 */

import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '../utils/storage'

const routes = [
  {
    path: '/',
    redirect: (to) => {
      // 根据用户角色重定向到不同页面
      const userInfo = localStorage.getItem('rag_user_info')
      if (userInfo) {
        const user = JSON.parse(userInfo)
        return user.role === 'admin' ? '/dashboard' : '/knowledge'
      }
      return '/knowledge'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        component: () => import('../views/DashboardAdmin.vue')
      }
    ]
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: () => import('../views/Knowledge.vue')
      }
    ]
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: () => import('../views/Chat.vue')
      }
    ]
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: () => import('../views/Search.vue')
      }
    ]
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: () => import('../views/Profile.vue')
      }
    ]
  },
  // 管理员功能路由
  {
    path: '/admin/users',
    name: 'UserManagement',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        component: () => import('../views/admin/UserManagement.vue')
      }
    ]
  },
  {
    path: '/admin/knowledge',
    name: 'KnowledgeManagement',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        component: () => import('../views/admin/KnowledgeManagement.vue')
      }
    ]
  },
  {
    path: '/admin/upload',
    name: 'FileUpload',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        component: () => import('../views/admin/FileUpload.vue')
      }
    ]
  },
  {
    path: '/admin/models',
    name: 'ModelManagement',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        component: () => import('../views/admin/ModelManagement.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = getToken()
  
  if (to.meta.requiresAuth && !token) {
    // 需要登录但未登录，跳转到登录页
    next('/login')
  } else if (to.path === '/login' && token) {
    // 已登录访问登录页，根据角色跳转
    const userInfo = localStorage.getItem('rag_user_info')
    if (userInfo) {
      const user = JSON.parse(userInfo)
      next(user.role === 'admin' ? '/dashboard' : '/knowledge')
    } else {
      next('/knowledge')
    }
  } else if (to.meta.requiresAdmin) {
    // 需要管理员权限
    const userInfo = localStorage.getItem('rag_user_info')
    if (userInfo) {
      const user = JSON.parse(userInfo)
      if (user.role === 'admin') {
        next()
      } else {
        // 非管理员，跳转到知识库页面
        next('/knowledge')
      }
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router

