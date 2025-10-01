<template>
  <div class="profile-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-info">
          <h1 class="page-title">个人设置</h1>
        </div>
      </div>
    </div>

    <!-- 标签页导航 -->
    <div class="tabs-nav">
      <button 
        class="tab-btn"
        :class="{ 'active': activeTab === 'basic' }"
        @click="switchTab('basic')"
      >
        <i class="icon-user-info"></i>
        基本信息
      </button>
      <button 
        class="tab-btn"
        :class="{ 'active': activeTab === 'security' }"
        @click="switchTab('security')"
      >
        <i class="icon-security"></i>
        安全设置
      </button>
    </div>
    
    <!-- 标签页内容 -->
    <div class="tab-content">
      <!-- 基本信息标签页 -->
      <div v-if="activeTab === 'basic'" class="basic-info-tab">
        <div class="profile-container">
          <!-- 左侧头像区域 -->
          <div class="avatar-section">
            <div class="avatar-container">
              <div class="user-avatar-large">
                <img v-if="userProfile.avatar" :src="userProfile.avatar" :alt="userProfile.name" />
                <i v-else class="icon-user-avatar-default"></i>
              </div>
              <div class="avatar-upload">
                <button class="upload-btn" @click="triggerFileUpload">
                  <i class="icon-camera"></i>
                  点击上传新头像
                </button>
                <p class="upload-hint">
                  支持 JPG、PNG 格式，文件大小不超过 2MB
                </p>
                <input 
                  ref="fileInput" 
                  type="file" 
                  accept="image/jpg,image/jpeg,image/png"
                  @change="handleAvatarUpload"
                  style="display: none"
                />
              </div>
            </div>
          </div>

          <!-- 右侧表单区域 -->
          <div class="form-section">
            <form class="profile-form" @submit.prevent="handleUpdateProfile">
              <!-- 姓名 -->
              <div class="form-group">
                <label class="form-label">姓名</label>
                <input
                  v-model="profileForm.name"
                  type="text"
                  class="form-input"
                  placeholder="请输入姓名"
                  required
                />
              </div>

              <!-- 用户名（只读） -->
              <div class="form-group">
                <label class="form-label">用户名</label>
                <input
                  v-model="userProfile.username"
                  type="text"
                  class="form-input readonly"
                  readonly
                />
                <p class="form-help">用户名不能修改</p>
              </div>

              <!-- 邮箱地址 -->
              <div class="form-group">
                <label class="form-label">邮箱地址</label>
                <input
                  v-model="profileForm.email"
                  type="email"
                  class="form-input"
                  placeholder="请输入邮箱地址"
                  required
                />
              </div>

              <!-- 手机号码 -->
              <div class="form-group">
                <label class="form-label">手机号码</label>
                <input
                  v-model="profileForm.phone"
                  type="tel"
                  class="form-input"
                  placeholder="请输入手机号码"
                />
              </div>

              <!-- 部门 -->
              <div class="form-group">
                <label class="form-label">部门</label>
                <select v-model="profileForm.department" class="form-select">
                  <option value="">请选择部门</option>
                  <option 
                    v-for="dept in departmentList" 
                    :key="dept.value" 
                    :value="dept.value"
                  >
                    {{ dept.label }}
                  </option>
                </select>
              </div>

              <!-- 职位 -->
              <div class="form-group">
                <label class="form-label">职位</label>
                <input
                  v-model="profileForm.position"
                  type="text"
                  class="form-input"
                  placeholder="请输入职位"
                />
              </div>

              <!-- 个人简介 -->
              <div class="form-group">
                <label class="form-label">个人简介</label>
                <textarea
                  v-model="profileForm.bio"
                  class="form-textarea"
                  rows="4"
                  placeholder="请介绍一下自己..."
                  maxlength="200"
                ></textarea>
                <div class="char-count">{{ profileForm.bio.length }} / 200</div>
              </div>

              <!-- 提交按钮 -->
              <div class="form-actions">
                <button 
                  type="submit" 
                  class="save-btn"
                  :disabled="profileLoading"
                >
                  <i v-if="profileLoading" class="icon-loading"></i>
                  <span>{{ profileLoading ? '保存中...' : '保存更改' }}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- 安全设置标签页 -->
      <div v-if="activeTab === 'security'" class="security-tab">
        <div class="security-container">
          <!-- 修改密码 -->
          <div class="password-section">
            <h3 class="section-title">修改密码</h3>
            <form class="password-form" @submit.prevent="handleChangePassword">
              <!-- 当前密码 -->
              <div class="form-group">
                <label class="form-label">当前密码</label>
                <div class="password-input-wrapper">
                  <input
                    v-model="passwordForm.currentPassword"
                    :type="showCurrentPassword ? 'text' : 'password'"
                    class="form-input"
                    placeholder="请输入当前密码"
                    required
                  />
                  <i 
                    class="icon-eye"
                    :class="{ 'icon-eye-open': showCurrentPassword, 'icon-eye-close': !showCurrentPassword }"
                    @click="showCurrentPassword = !showCurrentPassword"
                  ></i>
                </div>
              </div>

              <!-- 新密码 -->
              <div class="form-group">
                <label class="form-label">新密码</label>
                <div class="password-input-wrapper">
                  <input
                    v-model="passwordForm.newPassword"
                    :type="showNewPassword ? 'text' : 'password'"
                    class="form-input"
                    placeholder="请输入新密码"
                    required
                  />
                  <i 
                    class="icon-eye"
                    :class="{ 'icon-eye-open': showNewPassword, 'icon-eye-close': !showNewPassword }"
                    @click="showNewPassword = !showNewPassword"
                  ></i>
                </div>
              </div>

              <!-- 确认新密码 -->
              <div class="form-group">
                <label class="form-label">确认新密码</label>
                <div class="password-input-wrapper">
                  <input
                    v-model="passwordForm.confirmPassword"
                    :type="showConfirmPassword ? 'text' : 'password'"
                    class="form-input"
                    placeholder="请再次输入新密码"
                    required
                  />
                  <i 
                    class="icon-eye"
                    :class="{ 'icon-eye-open': showConfirmPassword, 'icon-eye-close': !showConfirmPassword }"
                    @click="showConfirmPassword = !showConfirmPassword"
                  ></i>
                </div>
              </div>

              <!-- 提交按钮 -->
              <div class="form-actions">
                <button 
                  type="submit" 
                  class="update-btn"
                  :disabled="passwordLoading"
                >
                  <i v-if="passwordLoading" class="icon-loading"></i>
                  <span>{{ passwordLoading ? '更新中...' : '更新密码' }}</span>
                </button>
              </div>
            </form>
          </div>

          <!-- 最近登录记录 -->
          <div class="records-section">
            <h3 class="section-title">最近登录记录</h3>
            <div class="login-records">
              <div 
                v-for="record in loginRecords" 
                :key="record.id"
                class="record-item"
              >
                <div class="record-info">
                  <div class="record-device">
                    <i class="icon-device" :class="getDeviceIcon(record.device)"></i>
                    <span class="device-name">{{ record.device }}</span>
                    <span class="device-ip">{{ record.ip }}</span>
                  </div>
                  <div class="record-meta">
                    <span class="login-time">{{ formatLoginTime(record.loginTime) }}</span>
                    <span class="login-status" :class="getStatusClass(record.status)">
                      {{ getStatusText(record.status) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
      
            <!-- 加载状态 -->
            <div v-if="recordsLoading" class="loading-records">
              <i class="icon-loading"></i>
              <span>加载中...</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { 
  getUserProfile, 
  updateUserProfile, 
  uploadUserAvatar,
  getDepartmentList,
  getLoginRecords,
  changeUserPassword
} from '../api/userApi'

// 当前激活的标签页
const activeTab = ref('basic')

// 用户信息
const userProfile = ref({
  id: '',
  username: '',
  name: '',
  email: '',
  phone: '',
  department: '',
  position: '',
  avatar: '',
  bio: '',
  role: ''
})

// 个人信息表单
const profileForm = reactive({
  name: '',
  email: '',
  phone: '',
  department: '',
  position: '',
  bio: ''
})

// 修改密码表单
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 部门列表
const departmentList = ref([])

// 登录记录
const loginRecords = ref([])

// 文件上传引用
const fileInput = ref(null)

// 加载状态
const profileLoading = ref(false)
const passwordLoading = ref(false)
const recordsLoading = ref(false)

// 密码显示状态
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

onMounted(async () => {
  await loadUserProfile()
  await loadDepartmentList()
  await loadLoginRecords()
})

/**
 * 切换标签页
 */
function switchTab(tab) {
  activeTab.value = tab
  
  // 切换到安全设置时加载登录记录
  if (tab === 'security' && loginRecords.value.length === 0) {
    loadLoginRecords()
  }
}

/**
 * 加载用户信息
 */
async function loadUserProfile() {
  try {
    const res = await getUserProfile()
    userProfile.value = res.data
    
    // 填充表单
    profileForm.name = res.data.name
    profileForm.email = res.data.email
    profileForm.phone = res.data.phone
    profileForm.department = res.data.department
    profileForm.position = res.data.position
    profileForm.bio = res.data.bio || ''
  } catch (error) {
    console.error('加载用户信息失败:', error)
    alert(error.message || '加载用户信息失败')
  }
}

/**
 * 加载部门列表
 */
async function loadDepartmentList() {
  try {
    const res = await getDepartmentList()
    departmentList.value = res.data
  } catch (error) {
    console.error('加载部门列表失败:', error)
  }
}

/**
 * 加载登录记录
 */
async function loadLoginRecords() {
  recordsLoading.value = true
  try {
    const res = await getLoginRecords({ limit: 10 })
    loginRecords.value = res.data
  } catch (error) {
    console.error('加载登录记录失败:', error)
  } finally {
    recordsLoading.value = false
  }
}

/**
 * 触发文件上传
 */
function triggerFileUpload() {
  fileInput.value?.click()
}

/**
 * 处理头像上传
 */
async function handleAvatarUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  // 文件大小验证（2MB）
  if (file.size > 2 * 1024 * 1024) {
    alert('文件大小不能超过 2MB')
    return
  }

  // 文件类型验证
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png']
  if (!allowedTypes.includes(file.type)) {
    alert('只支持 JPG、PNG 格式的图片')
    return
  }

  try {
    const formData = new FormData()
    formData.append('avatar', file)

    const res = await uploadUserAvatar(formData)
    userProfile.value.avatar = res.data.avatarUrl
    alert('头像上传成功')
  } catch (error) {
    console.error('头像上传失败:', error)
    alert(error.message || '头像上传失败')
  }

  // 重置文件输入
  event.target.value = ''
}

/**
 * 更新个人信息
 */
async function handleUpdateProfile() {
  profileLoading.value = true
  
  try {
    await updateUserProfile(profileForm)
    
    // 更新本地用户信息
    Object.assign(userProfile.value, profileForm)
    
    alert('个人信息更新成功')
  } catch (error) {
    console.error('更新个人信息失败:', error)
    alert(error.message || '更新失败，请重试')
  } finally {
    profileLoading.value = false
  }
}

/**
 * 修改密码
 */
async function handleChangePassword() {
  // 密码确认验证
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    alert('新密码和确认密码不一致')
    return
  }

  if (passwordForm.newPassword.length < 6) {
    alert('密码长度不能少于6位')
    return
  }

  passwordLoading.value = true
  
  try {
    await changeUserPassword(passwordForm)
    
    // 清空表单
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
    
    alert('密码修改成功')
  } catch (error) {
    console.error('修改密码失败:', error)
    alert(error.message || '修改密码失败')
  } finally {
    passwordLoading.value = false
  }
}

/**
 * 获取设备图标类名
 */
function getDeviceIcon(device) {
  if (device.includes('Windows')) return 'icon-device-windows'
  if (device.includes('iPhone')) return 'icon-device-iphone'
  if (device.includes('MacBook') || device.includes('Mac')) return 'icon-device-mac'
  if (device.includes('Android')) return 'icon-device-android'
  return 'icon-device-computer'
}

/**
 * 获取状态样式类
 */
function getStatusClass(status) {
  return status === 'current' ? 'status-current' : 'status-ended'
}

/**
 * 获取状态文本
 */
function getStatusText(status) {
  return status === 'current' ? '当前会话' : '已结束'
}

/**
 * 格式化登录时间
 */
function formatLoginTime(timeStr) {
  const date = new Date(timeStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  
  return `${year}-${month}-${day} ${hours}:${minutes}`
}
</script>

<style scoped>
.profile-page {
  padding: 32px 64px;
  max-width: 1600px;
  margin: 0 auto;
  background: #f5f7fa;
  min-height: 100vh;
  width: 100%;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 32px;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-info {
  display: flex;
  flex-direction: column;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.2;
}


/* 标签页导航 */
.tabs-nav {
  display: flex;
  background: #ffffff;
  border-radius: 12px;
  padding: 8px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: transparent;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s;
  flex: 1;
  justify-content: center;
}

.tab-btn:hover {
  background: #f9fafb;
  color: #667eea;
}

.tab-btn.active {
  background: #667eea;
  color: #ffffff;
}

.tab-btn i {
  font-size: 18px;
}

/* 标签页内容 */
.tab-content {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* 基本信息标签页 */
.basic-info-tab {
  padding: 40px 60px;
}

.profile-container {
  display: flex;
  gap: 64px;
}

/* 头像区域 */
.avatar-section {
  flex-shrink: 0;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.user-avatar-large {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.user-avatar-large img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar-large .icon-user-avatar-default::before {
  content: '👤';
  font-size: 48px;
  color: white;
}

.avatar-upload {
  text-align: center;
  max-width: 200px;
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  font-size: 14px;
  color: #495057;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 12px;
}

.upload-btn:hover {
  background: #e9ecef;
  border-color: #dee2e6;
}

.icon-camera::before {
  content: '📷';
  font-size: 16px;
}

.upload-hint {
  font-size: 12px;
  color: #6c757d;
  line-height: 1.4;
  margin: 0;
}

/* 表单区域 */
.form-section {
  flex: 1;
}

.profile-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px 32px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group:nth-last-child(2) {
  grid-column: 1 / -1; /* 个人简介占满整行 */
}

.form-group:nth-last-child(1) {
  grid-column: 1 / -1; /* 提交按钮占满整行 */
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.form-input, .form-select {
  height: 44px;
  padding: 0 12px;
  font-size: 14px;
  color: #1f2937;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  outline: none;
  transition: all 0.3s;
}

.form-input:focus, .form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input.readonly {
  background: #f9fafb;
  color: #6b7280;
  cursor: not-allowed;
}

.form-textarea {
  min-height: 88px;
  padding: 12px;
  font-size: 14px;
  color: #1f2937;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  outline: none;
  resize: vertical;
  transition: all 0.3s;
  font-family: inherit;
  line-height: 1.5;
}

.form-textarea:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-help {
  font-size: 12px;
  color: #6b7280;
  margin: 4px 0 0 0;
}

.char-count {
  font-size: 12px;
  color: #9ca3af;
  text-align: right;
  margin-top: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.save-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 32px;
  background: #667eea;
  color: #ffffff;
  font-size: 15px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.save-btn:hover:not(:disabled) {
  background: #5568d3;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 安全设置标签页 */
.security-tab {
  padding: 40px 60px;
}

.security-container {
  display: flex;
  gap: 48px;
  align-items: flex-start;
}

.password-section {
  flex: 0 0 640px;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 40px;
  border: 1px solid #e9ecef;
}

.password-section .section-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.password-section .section-title::before {
  content: '🔐';
  font-size: 20px;
}

.records-section {
  flex: 1;
  min-width: 0;
}

.records-section .section-title {
  color: #374151;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.records-section .section-title::before {
  content: '📋';
  font-size: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 24px 0;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
}

.password-form .form-input {
  min-width: 400px;
  width: 100%;
  height: 48px;
  font-size: 15px;
}

.password-input-wrapper {
  position: relative;
}

.password-input-wrapper .form-input {
  padding-right: 48px;
}

.icon-eye {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 18px;
  color: #9ca3af;
  transition: color 0.3s;
}

.icon-eye:hover {
  color: #667eea;
}

.icon-eye-close::before {
  content: '👁️‍🗨️';
}

.icon-eye-open::before {
  content: '👁️';
}

.update-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: #667eea;
  color: #ffffff;
  font-size: 15px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  align-self: flex-start;
}

.update-btn:hover:not(:disabled) {
  background: #5568d3;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.update-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 登录记录 */
.login-records {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.record-item {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.record-item:hover {
  border-color: #d1d5db;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.record-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.record-device {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-device {
  font-size: 24px;
}

.icon-device-windows::before {
  content: '💻';
}

.icon-device-iphone::before {
  content: '📱';
}

.icon-device-mac::before {
  content: '🖥️';
}

.icon-device-android::before {
  content: '📱';
}

.icon-device-computer::before {
  content: '💻';
}

.device-name {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
}

.device-ip {
  font-size: 13px;
  color: #6b7280;
}

.record-meta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.login-time {
  font-size: 13px;
  color: #6b7280;
}

.login-status {
  font-size: 12px;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 12px;
}

.status-current {
  background: #d1fae5;
  color: #059669;
}

.status-ended {
  background: #f3f4f6;
  color: #6b7280;
}

.loading-records {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 20px;
  justify-content: center;
  color: #6b7280;
  font-size: 14px;
}

/* 加载动画 */
.icon-loading {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 图标占位符 */
.icon-user-info::before {
  content: '👤';
}

.icon-security::before {
  content: '🔒';
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .security-container {
    flex-direction: column;
    gap: 32px;
  }
  
  .password-section {
    flex: none;
    max-width: 720px;
    width: 100%;
  }
  
  .records-section {
    width: 100%;
  }
}
</style>