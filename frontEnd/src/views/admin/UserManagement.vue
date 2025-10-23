<template>
  <div class="user-management-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">用户管理</h1>
        <p class="page-subtitle">管理系统用户产账号和权限</p>
      </div>
      <div class="header-right">
        <i class="icon-time"></i>
        <span class="current-time">{{ currentTime }}</span>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="card-icon blue">
          <i class="icon-users-total"></i>
        </div>
        <div class="card-content">
          <div class="card-label">总用户数</div>
          <div class="card-value">{{ stats.totalUsers }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="card-icon green">
          <i class="icon-users-active"></i>
        </div>
        <div class="card-content">
          <div class="card-label">活跃用户</div>
          <div class="card-value">{{ stats.activeUsers }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="card-icon yellow">
          <i class="icon-users-admin"></i>
        </div>
        <div class="card-content">
          <div class="card-label">管理员</div>
          <div class="card-value">{{ stats.adminUsers }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="card-icon red">
          <i class="icon-users-disabled"></i>
        </div>
        <div class="card-content">
          <div class="card-label">禁用用户</div>
          <div class="card-value">{{ stats.disabledUsers }}</div>
        </div>
      </div>
    </div>

    <!-- 搜索和操作区 -->
    <div class="search-bar">
      <div class="search-left">
        <div class="search-input-wrapper">
          <i class="icon-search-input"></i>
          <input
            v-model="searchForm.keyword"
            type="text"
            class="search-input"
            placeholder="搜索用户姓名、邮箱或手机号..."
            @keyup.enter="handleSearch"
          />
        </div>

        <select v-model="searchForm.role" class="filter-select" @change="handleSearch">
          <option value="">全部角色</option>
          <option value="admin">管理员</option>
          <option value="user">普通用户</option>
        </select>

        <select v-model="searchForm.status" class="filter-select" @change="handleSearch">
          <option value="">全部状态</option>
          <option value="active">活跃</option>
          <option value="disabled">禁用</option>
        </select>

        <button class="btn-export" @click="handleExport">
          <i class="icon-export"></i>
          导出
        </button>
      </div>

      <button class="btn-add" @click="showAddUserDialog = true">
        <i class="icon-add"></i>
        添加用户
      </button>
    </div>

    <!-- 用户列表表格 -->
    <div class="table-container">
      <table class="user-table">
        <thead>
          <tr>
            <th class="col-checkbox">
              <input type="checkbox" v-model="selectAll" @change="handleSelectAll" />
            </th>
            <th class="col-user">用户信息</th>
            <th class="col-role">角色</th>
            <th class="col-status">状态</th>
            <th class="col-login">最后登录</th>
            <th class="col-time">创建时间</th>
            <th class="col-actions">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in userList" :key="user.id">
            <td class="col-checkbox">
              <input type="checkbox" v-model="selectedUsers" :value="user.id" />
            </td>
            <td class="col-user">
              <div class="user-info">
                <div class="user-avatar">
                  <i class="icon-user-avatar"></i>
                </div>
                <div class="user-details">
                  <div class="user-name">{{ user.name }}</div>
                  <div class="user-email">{{ user.email }}</div>
                  <div class="user-phone">{{ user.phone }}</div>
                </div>
              </div>
            </td>
            <td class="col-role">
              <span class="role-badge" :class="user.role">
                <i :class="user.role === 'admin' ? 'icon-role-admin' : 'icon-role-user'"></i>
                {{ user.role === 'admin' ? '管理员' : '普通用户' }}
              </span>
            </td>
            <td class="col-status">
              <span class="status-badge" :class="user.status">
                <i class="status-dot"></i>
                {{ user.status === 'active' ? '活跃' : '禁用' }}
              </span>
            </td>
            <td class="col-login">{{ user.lastLogin }}</td>
            <td class="col-time">{{ user.createdAt }}</td>
            <td class="col-actions">
              <div class="action-buttons">
                <button class="action-btn" title="编辑" @click="handleEdit(user)">
                  <i class="icon-edit"></i>
                </button>
                <button class="action-btn" title="重置密码" @click="handleResetPassword(user)">
                  <i class="icon-reset-pwd"></i>
                </button>
                <button 
                  v-if="user.status === 'disabled'" 
                  class="action-btn enable" 
                  title="启用"
                  @click="handleToggleStatus(user)"
                >
                  <i class="icon-enable"></i>
                </button>
                <button 
                  v-else
                  class="action-btn" 
                  title="禁用"
                  @click="handleToggleStatus(user)"
                >
                  <i class="icon-disable"></i>
                </button>
                <button class="action-btn delete" title="删除" @click="handleDelete(user)">
                  <i class="icon-delete"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 空状态 -->
      <div v-if="userList.length === 0" class="empty-state">
        <i class="icon-empty"></i>
        <p>暂无用户数据</p>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <div class="pagination-info">
        显示第 {{ (pagination.page - 1) * pagination.pageSize + 1 }}-{{ Math.min(pagination.page * pagination.pageSize, pagination.total) }} 项，共 {{ pagination.total }} 项
      </div>
      <div class="pagination-buttons">
        <button 
          class="page-btn" 
          :disabled="pagination.page === 1"
          @click="handlePageChange(pagination.page - 1)"
        >
          上一页
        </button>
        <button 
          v-for="page in visiblePages" 
          :key="page"
          class="page-btn" 
          :class="{ active: page === pagination.page }"
          @click="handlePageChange(page)"
        >
          {{ page }}
        </button>
        <button 
          class="page-btn"
          :disabled="pagination.page >= totalPages"
          @click="handlePageChange(pagination.page + 1)"
        >
          下一页
        </button>
      </div>
    </div>

    <!-- 添加/编辑用户对话框 -->
    <div v-if="showAddUserDialog || showEditUserDialog" class="dialog-overlay" @click.self="closeDialog">
      <div class="dialog">
        <div class="dialog-header">
          <h3>{{ showAddUserDialog ? '添加用户' : '编辑用户' }}</h3>
          <button class="dialog-close" @click="closeDialog">
            <i class="icon-close"></i>
          </button>
        </div>
        <div class="dialog-body">
          <div class="form-group">
            <label>姓名 <span class="required">*</span></label>
            <input v-model="userForm.name" type="text" placeholder="请输入姓名" />
          </div>
          <div class="form-group">
            <label>用户名 <span class="required">*</span></label>
            <input v-model="userForm.username" type="text" placeholder="请输入用户名" :disabled="showEditUserDialog" />
          </div>
          <div class="form-group">
            <label>邮箱 <span class="required">*</span></label>
            <input v-model="userForm.email" type="email" placeholder="请输入邮箱" />
          </div>
          <div class="form-group">
            <label>手机号 <span class="required">*</span></label>
            <input v-model="userForm.phone" type="tel" placeholder="请输入手机号" />
          </div>
          <div class="form-group">
            <label>角色 <span class="required">*</span></label>
            <select v-model="userForm.role">
              <option value="user">普通用户</option>
              <option value="admin">管理员</option>
            </select>
          </div>
          <div v-if="showAddUserDialog" class="form-group">
            <label>初始密码 <span class="required">*</span></label>
            <input v-model="userForm.password" type="password" placeholder="请输入初始密码" />
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn-cancel" @click="closeDialog">取消</button>
          <button class="btn-confirm" @click="handleSubmitUser" :disabled="isSubmitting">
            <i v-if="isSubmitting" class="icon-loading"></i>
            {{ isSubmitting ? '提交中...' : '确定' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  getUserStats, 
  getUserList, 
  createUser, 
  updateUser, 
  deleteUser, 
  toggleUserStatus, 
  resetUserPassword,
  exportUsers
} from '../../api/userManagementApi'

// 当前时间
const currentTime = ref('')
let timeInterval = null

// 统计数据
const stats = ref({
  totalUsers: 0,
  activeUsers: 0,
  adminUsers: 0,
  disabledUsers: 0
})

// 搜索表单
const searchForm = ref({
  keyword: '',
  role: '',
  status: ''
})

// 用户列表
const userList = ref([])
const selectedUsers = ref([])
const selectAll = ref(false)

// 分页
const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

// 对话框
const showAddUserDialog = ref(false)
const showEditUserDialog = ref(false)
const isSubmitting = ref(false)

// 用户表单
const userForm = ref({
  id: '',
  name: '',
  username: '',
  email: '',
  phone: '',
  role: 'user',
  password: ''
})

// 计算属性
const totalPages = computed(() => {
  return Math.ceil(pagination.value.total / pagination.value.pageSize)
})

const visiblePages = computed(() => {
  const current = pagination.value.page
  const total = totalPages.value
  const pages = []
  
  if (total <= 5) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 3) {
      pages.push(1, 2, 3, 4, 5)
    } else if (current >= total - 2) {
      for (let i = total - 4; i <= total; i++) {
        pages.push(i)
      }
    } else {
      for (let i = current - 2; i <= current + 2; i++) {
        pages.push(i)
      }
    }
  }
  
  return pages
})

// 生命周期
onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  loadStats()
  loadUserList()
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})

// 更新时间
function updateTime() {
  const now = new Date()
  const month = now.getMonth() + 1
  const day = now.getDate()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  currentTime.value = `${month}/${day} ${hours}:${minutes}`
}

// 加载统计数据
async function loadStats() {
  try {
    const res = await getUserStats()
    if (res.success) {
      stats.value = res.data
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 加载用户列表
async function loadUserList() {
  try {
    const res = await getUserList({
      ...searchForm.value,
      page: pagination.value.page,
      pageSize: pagination.value.pageSize
    })
    
    if (res.success) {
      userList.value = res.data.list
      pagination.value.total = res.data.total
    }
  } catch (error) {
    console.error('加载用户列表失败:', error)
  }
}

// 搜索
function handleSearch() {
  pagination.value.page = 1
  loadUserList()
}

// 全选
function handleSelectAll() {
  if (selectAll.value) {
    selectedUsers.value = userList.value.map(user => user.id)
  } else {
    selectedUsers.value = []
  }
}

// 分页
function handlePageChange(page) {
  pagination.value.page = page
  loadUserList()
}

// 导出
async function handleExport() {
  try {
    const res = await exportUsers(searchForm.value)
    if (res.success) {
      // 触发下载
      window.open(res.data.downloadUrl, '_blank')
      alert('导出成功！')
    }
  } catch (error) {
    alert(error.message || '导出失败')
  }
}

// 编辑
function handleEdit(user) {
  userForm.value = {
    id: user.id,
    name: user.name,
    username: user.username,
    email: user.email,
    phone: user.phone,
    role: user.role,
    password: ''
  }
  showEditUserDialog.value = true
}

// 重置密码
async function handleResetPassword(user) {
  if (confirm(`确定要重置 ${user.name} 的密码吗？`)) {
    try {
      const res = await resetUserPassword({ userId: user.id })
      if (res.success) {
        alert(`密码已重置为: ${res.data.newPassword}`)
      }
    } catch (error) {
      alert(error.message || '重置密码失败')
    }
  }
}

// 切换状态
async function handleToggleStatus(user) {
  const action = user.status === 'active' ? '禁用' : '启用'
  if (confirm(`确定要${action} ${user.name} 吗？`)) {
    try {
      const res = await toggleUserStatus({ 
        userId: user.id,
        status: user.status === 'active' ? 'disabled' : 'active'
      })
      if (res.success) {
        alert(`${action}成功`)
        loadUserList()
        loadStats()
      }
    } catch (error) {
      alert(error.message || `${action}失败`)
    }
  }
}

// 删除
async function handleDelete(user) {
  if (confirm(`确定要删除用户 ${user.name} 吗？此操作不可恢复！`)) {
    try {
      const res = await deleteUser({ userId: user.id })
      if (res.success) {
        alert('删除成功')
        loadUserList()
        loadStats()
      }
    } catch (error) {
      alert(error.message || '删除失败')
    }
  }
}

// 提交用户
async function handleSubmitUser() {
  // 表单验证
  if (!userForm.value.name || !userForm.value.username || !userForm.value.email || !userForm.value.phone) {
    alert('请填写完整信息')
    return
  }

  if (showAddUserDialog.value && !userForm.value.password) {
    alert('请输入初始密码')
    return
  }

  isSubmitting.value = true
  
  try {
    let res
    if (showAddUserDialog.value) {
      res = await createUser(userForm.value)
    } else {
      res = await updateUser(userForm.value)
    }
    
    if (res.success) {
      alert(showAddUserDialog.value ? '添加成功' : '更新成功')
      closeDialog()
      loadUserList()
      loadStats()
    }
  } catch (error) {
    alert(error.message || '操作失败')
  } finally {
    isSubmitting.value = false
  }
}

// 关闭对话框
function closeDialog() {
  showAddUserDialog.value = false
  showEditUserDialog.value = false
  userForm.value = {
    id: '',
    name: '',
    username: '',
    email: '',
    phone: '',
    role: 'user',
    password: ''
  }
}
</script>

<style scoped>
.user-management-page {
  padding: 32px 48px;
  max-width: 1800px;
  margin: 0 auto;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #666666;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6b7280;
  font-size: 14px;
}

.icon-time {
  width: 16px;
  height: 16px;
  background-image: url('@/assets/icons/icon-time.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.card-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.card-icon.blue {
  background: #dbeafe;
}

.card-icon.green {
  background: #d1fae5;
}

.card-icon.yellow {
  background: #fef3c7;
}

.card-icon.red {
  background: #fee2e2;
}

.card-content {
  flex: 1;
}

.card-label {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.card-value {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
}

/* 搜索栏 */
.search-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 16px;
}

.search-left {
  display: flex;
  gap: 12px;
  flex: 1;
}

.search-input-wrapper {
  position: relative;
  flex: 1;
  max-width: 400px;
}

.icon-search-input {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
}

.icon-search-input {
  width: 18px;
  height: 18px;
  background-image: url('@/assets/icons/icon-search-btn.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.search-input {
  width: 100%;
  height: 44px;
  padding: 0 16px 0 48px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #667eea;
}

.filter-select {
  height: 44px;
  padding: 0 36px 0 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  color: #374151;
  background: #ffffff;
  cursor: pointer;
  outline: none;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236b7280' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
}

.btn-export {
  height: 44px;
  padding: 0 20px;
  border: 1px solid #10b981;
  background: #ffffff;
  color: #10b981;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-export:hover {
  background: #10b981;
  color: #ffffff;
}

.icon-export {
  width: 16px;
  height: 16px;
  background-image: url('@/assets/icons/icon-download.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.btn-add {
  height: 44px;
  padding: 0 24px;
  background: #667eea;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.3s;
}

.btn-add:hover {
  background: #5568d3;
}

.icon-add {
  width: 20px;
  height: 20px;
  background-image: url('@/assets/icons/icon-plus.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

/* 表格 */
.table-container {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 20px;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table thead {
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.user-table th {
  padding: 16px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.user-table td {
  padding: 16px;
  border-bottom: 1px solid #f3f4f6;
}

.user-table tbody tr:last-child td {
  border-bottom: none;
}

.user-table tbody tr:hover {
  background: #f9fafb;
}

.col-checkbox {
  width: 48px;
}

.col-user {
  min-width: 280px;
}

.col-role {
  width: 140px;
}

.col-status {
  width: 100px;
}

.col-login {
  width: 160px;
}

.col-time {
  width: 120px;
}

.col-actions {
  width: 200px;
}

/* 用户信息 */
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-user-avatar {
  width: 40px;
  height: 40px;
  background-image: url('@/assets/icons/icon-user-avatar-default.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.user-email {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 2px;
}

.user-phone {
  font-size: 13px;
  color: #9ca3af;
}

/* 角色标签 */
.role-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}

.role-badge.admin {
  background: #ede9fe;
  color: #7c3aed;
}

.role-badge.user {
  background: #dbeafe;
  color: #2563eb;
}

.icon-role-admin {
  width: 14px;
  height: 14px;
  background-image: url('@/assets/icons/icon-users-admin.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-role-user {
  width: 14px;
  height: 14px;
  background-image: url('@/assets/icons/icon-role-user.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

/* 状态标签 */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
}

.status-badge.active {
  color: #10b981;
}

.status-badge.disabled {
  color: #ef4444;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-badge.active .status-dot {
  background: #10b981;
}

.status-badge.disabled .status-dot {
  background: #ef4444;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: #f3f4f6;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.action-btn:hover {
  background: #667eea;
  color: #ffffff;
}

.action-btn.enable:hover {
  background: #10b981;
  color: #ffffff;
}

.action-btn.delete:hover {
  background: #ef4444;
  color: #ffffff;
}

.icon-edit {
  width: 16px;
  height: 16px;
  background-image: url('@/assets/icons/icon-edit-user.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-reset-pwd {
  width: 16px;
  height: 16px;
  background-image: url('@/assets/icons/icon-reset-password.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-enable {
  width: 16px;
  height: 16px;
  background-image: url('@/assets/icons/icon-enable-user.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-disable {
  width: 16px;
  height: 16px;
  background-image: url('@/assets/icons/icon-disable-user.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-delete {
  width: 16px;
  height: 16px;
  background-image: url('@/assets/icons/icon-delete-user.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
}

.pagination-info {
  font-size: 14px;
  color: #6b7280;
}

.pagination-buttons {
  display: flex;
  gap: 8px;
}

.page-btn {
  min-width: 80px;
  height: 36px;
  padding: 0 16px;
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #374151;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  border-color: #667eea;
  color: #667eea;
}

.page-btn.active {
  background: #667eea;
  border-color: #667eea;
  color: #ffffff;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.icon-empty::before {
  content: '📭';
  font-size: 64px;
  display: block;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 14px;
  color: #6b7280;
}

/* 对话框 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  background: #ffffff;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: auto;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.dialog-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.dialog-close {
  width: 32px;
  height: 32px;
  border: none;
  background: #f3f4f6;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}

.dialog-close:hover {
  background: #e5e7eb;
}

.icon-close {
  width: 18px;
  height: 18px;
  background-image: url('@/assets/icons/icon-plus.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  transform: rotate(45deg);
}

.dialog-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.required {
  color: #ef4444;
}

.form-group input,
.form-group select {
  width: 100%;
  height: 44px;
  padding: 0 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #667eea;
}

.form-group input:disabled {
  background: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
}

.btn-cancel {
  height: 40px;
  padding: 0 24px;
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #374151;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cancel:hover {
  background: #f3f4f6;
}

.btn-confirm {
  height: 40px;
  padding: 0 24px;
  border: none;
  background: #667eea;
  color: #ffffff;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.3s;
}

.btn-confirm:hover:not(:disabled) {
  background: #5568d3;
}

.btn-confirm:disabled {
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

/* 统计卡片图标 */
.icon-users-total {
  width: 28px;
  height: 28px;
  background-image: url('@/assets/icons/icon-users-total.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-users-active {
  width: 28px;
  height: 28px;
  background-image: url('@/assets/icons/icon-users-active.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-users-admin {
  width: 28px;
  height: 28px;
  background-image: url('@/assets/icons/icon-users-admin.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-users-disabled {
  width: 28px;
  height: 28px;
  background-image: url('@/assets/icons/icon-users-disabled.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}
</style>

