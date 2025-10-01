<template>
  <div class="dashboard">
    <h1>欢迎来到RAG知识问答系统</h1>
    <p>用户: {{ userInfo?.name }}</p>
    <p>角色: {{ userInfo?.role === 'admin' ? '管理员' : '普通用户' }}</p>
    <button @click="handleLogout">退出登录</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getUserInfo, clearAll } from '../utils/storage'
import { logout } from '../api/authApi'

const router = useRouter()
const userInfo = ref(null)

onMounted(() => {
  userInfo.value = getUserInfo()
})

async function handleLogout() {
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
.dashboard {
  padding: 40px;
  text-align: center;
}

button {
  margin-top: 20px;
  padding: 10px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background: #5568d3;
}
</style>

