<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Logo -->
      <div class="logo">
        <i class="logo-icon"></i>
      </div>

      <!-- 标题 -->
      <h1 class="title">HFUT-RAG</h1>
      <p class="subtitle">智能答案 · 精准问答 · 知识管理</p>

      <!-- 登录表单 -->
      <form class="login-form" @submit.prevent="handleLogin">
        <!-- 用户名 -->
        <div class="form-group">
          <label class="form-label">
            <i class="icon-user"></i>
            用户名
          </label>
          <input
            v-model="loginForm.username"
            type="text"
            class="form-input"
            placeholder="请输入用户名"
            required
          />
        </div>

        <!-- 密码 -->
        <div class="form-group">
          <label class="form-label">
            <i class="icon-lock"></i>
            密码
          </label>
          <div class="password-input-wrapper">
            <input
              v-model="loginForm.password"
              :type="showPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="请输入密码"
              required
            />
            <i 
              class="icon-eye" 
              :class="{ 'icon-eye-open': showPassword, 'icon-eye-close': !showPassword }"
              @click="togglePassword"
            ></i>
          </div>
        </div>

        <!-- 记住我 & 忘记密码 -->
        <div class="form-footer">
          <label class="remember-me">
            <input 
              v-model="loginForm.remember" 
              type="checkbox"
            />
            <span>记住我</span>
          </label>
          <a href="#" class="forgot-password" @click.prevent="handleForgotPassword">
            忘记密码?
          </a>
        </div>

        <!-- 登录按钮 -->
        <button 
          type="submit" 
          class="login-button"
          :disabled="loading"
        >
          <i v-if="loading" class="icon-loading"></i>
          <span>{{ loading ? '登录中...' : '登录' }}</span>
        </button>
      </form>

      <!-- 提示信息 -->
      <div class="info-tip">
        <i class="icon-info"></i>
        <span>企业内部系统，请使用公司账号登录</span>
      </div>

      <!-- 版权信息 -->
      <div class="copyright">
        © 2025 公司内部RAG知识问答系统 V1.0
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api/authApi'
import { setToken, setUserInfo } from '../utils/storage'

const router = useRouter()

// 表单数据
const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

// 显示密码
const showPassword = ref(false)

// 加载状态
const loading = ref(false)

/**
 * 切换密码显示/隐藏
 */
function togglePassword() {
  showPassword.value = !showPassword.value
}

/**
 * 处理登录
 */
async function handleLogin() {
  try {
    loading.value = true
    
    const { data } = await login({
      username: loginForm.username,
      password: loginForm.password
    })

    // 保存token和用户信息
    setToken(data.token, loginForm.remember)
    setUserInfo(data.user)

    // 根据用户角色跳转到不同页面
    if (data.user.role === 'admin') {
      router.push('/dashboard')
    } else {
      router.push('/knowledge')
    }
  } catch (error) {
    alert(error.message || '登录失败，请重试')
  } finally {
    loading.value = false
  }
}

/**
 * 处理忘记密码
 */
function handleForgotPassword() {
  alert('请联系系统管理员重置密码')
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: url('@/assets/images/login-bg.jpg') no-repeat center center;
  background-size: cover;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 500px;
  background: #ffffff;
  border-radius: 16px;
  padding: 48px 50px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.logo {
  text-align: center;
  margin-bottom: 24px;
}

.logo-icon {
  display: inline-block;
  width: 64px;
  height: 64px;
  background-image: url('@/assets/images/logo.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 12px;
}

.title {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  text-align: center;
  margin: 0 0 8px 0;
}

.subtitle {
  font-size: 14px;
  color: #666666;
  text-align: center;
  margin: 0 0 32px 0;
}

.login-form {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #333333;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-label i {
  margin-right: 6px;
  font-size: 16px;
}

.icon-user {
  width: 16px;
  height: 16px;
  background-image: url('@/assets/icons/icon-user.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-lock {
  width: 16px;
  height: 16px;
  background-image: url('@/assets/icons/icon-lock.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.form-input {
  width: 100%;
  height: 44px;
  padding: 0 16px;
  font-size: 14px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  outline: none;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #bdbdbd;
}

.password-input-wrapper {
  position: relative;
}

.password-input-wrapper .form-input {
  padding-right: 48px;
}

.icon-eye {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  width: 20px;
  height: 20px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  transition: opacity 0.3s;
}

.icon-eye:hover {
  opacity: 0.7;
}

.icon-eye-close {
  background-image: url('@/assets/icons/icon-eye-close.svg');
}

.icon-eye-open {
  background-image: url('@/assets/icons/icon-eye-open.svg');
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.remember-me {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #666666;
  cursor: pointer;
  user-select: none;
}

.remember-me input[type="checkbox"] {
  margin-right: 6px;
  cursor: pointer;
}

.forgot-password {
  font-size: 14px;
  color: #667eea;
  text-decoration: none;
  transition: color 0.3s;
}

.forgot-password:hover {
  color: #5568d3;
}

.login-button {
  width: 100%;
  height: 48px;
  background: #667eea;
  color: #ffffff;
  font-size: 16px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-button:hover:not(:disabled) {
  background: #5568d3;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.login-button:active:not(:disabled) {
  transform: translateY(0);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon-loading {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-image: url('@/assets/icons/icon-loading.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.info-tip {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.icon-info {
  width: 16px;
  height: 16px;
  background-image: url('@/assets/icons/icon-info.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.info-tip span {
  font-size: 13px;
  color: #666666;
}

.copyright {
  text-align: center;
  font-size: 12px;
  color: #999999;
}
</style>

