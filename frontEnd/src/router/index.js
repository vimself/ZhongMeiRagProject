/**
 * 路由配置
 */

import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '../utils/storage'

const routes = [
  {
    path: '/',
    redirect: '/knowledge'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
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
  // 临时保留的旧路由
  {
    path: '/dashboard',
    redirect: '/knowledge'
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
    // 已登录访问登录页，跳转到知识库页面
    next('/knowledge')
  } else {
    next()
  }
})

export default router

