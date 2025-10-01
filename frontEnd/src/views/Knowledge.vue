<template>
  <div class="knowledge-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">我的知识库</h1>
        <p class="page-subtitle">查看和管理您有权访问的知识库</p>
      </div>
      <div class="header-right">
        <div class="current-time">
          <i class="icon-time"></i>
          <span>{{ currentTime }}</span>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card stat-card-blue">
        <div class="stat-icon">
          <i class="icon-database"></i>
        </div>
        <div class="stat-content">
          <div class="stat-label">可访问知识库</div>
          <div class="stat-value">{{ stats.accessibleKnowledgeBase }}</div>
        </div>
      </div>

      <div class="stat-card stat-card-green">
        <div class="stat-icon">
          <i class="icon-document"></i>
        </div>
        <div class="stat-content">
          <div class="stat-label">可查阅文档</div>
          <div class="stat-value">{{ stats.accessibleDocuments }}</div>
        </div>
      </div>

      <div class="stat-card stat-card-purple">
        <div class="stat-icon">
          <i class="icon-message"></i>
        </div>
        <div class="stat-content">
          <div class="stat-label">今日问答</div>
          <div class="stat-value">{{ stats.todayQuestions }}</div>
        </div>
      </div>
    </div>

    <!-- 知识库列表标题 -->
    <div class="section-header">
      <h2 class="section-title">知识库列表</h2>
      <div class="section-tip">
        <i class="icon-info-tip"></i>
        <span>显示您有权访问的知识库</span>
      </div>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="loading-container">
      <i class="icon-loading"></i>
      <span>加载中...</span>
    </div>

    <!-- 知识库卡片列表 -->
    <div v-else class="knowledge-list">
      <div 
        v-for="kb in knowledgeBaseList" 
        :key="kb.id"
        class="knowledge-card"
        @click="goToKnowledgeDetail(kb.id)"
      >
        <!-- 卡片头部 -->
        <div class="card-header">
          <div class="kb-icon" :style="{ background: kb.iconColor }">
            <i :class="kb.icon"></i>
          </div>
          <div class="kb-info">
            <h3 class="kb-name">{{ kb.name }}</h3>
            <p class="kb-code">{{ kb.code }}</p>
          </div>
          <div class="card-more">
            <i class="icon-more-dot"></i>
          </div>
        </div>

        <!-- 知识库描述 -->
        <p class="kb-description">{{ kb.description }}</p>

        <!-- 统计信息 -->
        <div class="kb-stats">
          <div class="kb-stat-item">
            <span class="stat-label">文档数量</span>
            <span class="stat-value">{{ kb.documentCount }} 个</span>
          </div>
          <div class="kb-stat-item">
            <span class="stat-label">存储大小</span>
            <span class="stat-value">{{ kb.storageSize }}</span>
          </div>
        </div>

        <!-- 最后更新 -->
        <div class="kb-meta">
          <span class="meta-label">最后更新</span>
          <span class="meta-value">{{ kb.lastUpdate }}</span>
        </div>

        <!-- 底部状态栏 -->
        <div class="kb-footer">
          <div class="kb-status">
            <span 
              class="status-badge" 
              :class="getStatusClass(kb.status)"
            >
              <i class="status-dot"></i>
              {{ getStatusText(kb.status, kb.progress) }}
            </span>
            <span class="viewers-badge">
              <i class="icon-eye"></i>
              {{ kb.viewers }} 查看
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!loading && knowledgeBaseList.length === 0" class="empty-state">
      <i class="icon-empty"></i>
      <p class="empty-text">暂无可访问的知识库</p>
      <p class="empty-hint">请联系管理员为您授权</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { getKnowledgeBaseList, getKnowledgeBaseStats } from '../api/knowledgeApi'

const router = useRouter()

// 当前时间
const currentTime = ref('')

// 统计数据
const stats = ref({
  accessibleKnowledgeBase: 0,
  accessibleDocuments: 0,
  todayQuestions: 0
})

// 知识库列表
const knowledgeBaseList = ref([])

// 加载状态
const loading = ref(false)

// 定时器ID
let timeInterval = null

onMounted(async () => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  
  await loadData()
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})

/**
 * 更新当前时间
 */
function updateTime() {
  const now = new Date()
  const month = now.getMonth() + 1
  const day = now.getDate()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  currentTime.value = `${month}/${day} ${hours}:${minutes}`
}

/**
 * 加载数据
 */
async function loadData() {
  loading.value = true
  
  try {
    // 并发请求统计数据和知识库列表
    const [statsRes, listRes] = await Promise.all([
      getKnowledgeBaseStats(),
      getKnowledgeBaseList()
    ])
    
    stats.value = statsRes.data
    knowledgeBaseList.value = listRes.data
  } catch (error) {
    console.error('加载数据失败:', error)
    alert(error.message || '加载失败，请重试')
  } finally {
    loading.value = false
  }
}

/**
 * 获取状态样式类
 */
function getStatusClass(status) {
  const classMap = {
    'active': 'status-active',
    'processing': 'status-processing',
    'inactive': 'status-inactive'
  }
  return classMap[status] || ''
}

/**
 * 获取状态文本
 */
function getStatusText(status, progress) {
  if (status === 'active') {
    return '活跃'
  } else if (status === 'processing') {
    return `处理中 ${progress}%`
  } else if (status === 'inactive') {
    return '未激活'
  }
  return '未知'
}

/**
 * 前往知识库详情
 */
function goToKnowledgeDetail(id) {
  router.push(`/knowledge/${id}`)
}
</script>

<style scoped>
.knowledge-page {
  padding: 32px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 88px;
  margin-bottom: 32px;
  flex-shrink: 0;
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

.current-time {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666666;
  padding: 8px 16px;
  background: #ffffff;
  border-radius: 8px;
}

.icon-time::before {
  content: '🕐';
  font-size: 16px;
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 40px;
}

.stat-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s;
}

.stat-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.stat-card-blue .stat-icon {
  background: #dbeafe;
}

.stat-card-green .stat-icon {
  background: #d1fae5;
}

.stat-card-purple .stat-icon {
  background: #e9d5ff;
}

.icon-database::before {
  content: '📚';
}

.icon-document::before {
  content: '📄';
}

.icon-message::before {
  content: '💬';
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #666666;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #1a1a1a;
  line-height: 1;
}

/* 章节标题 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.section-tip {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #999999;
}

.icon-info-tip::before {
  content: 'ℹ️';
  font-size: 14px;
}

/* 加载中 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #666666;
  font-size: 14px;
}

.icon-loading {
  display: inline-block;
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 知识库列表 */
.knowledge-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.knowledge-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s;
  cursor: pointer;
}

.knowledge-card:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}

/* 卡片头部 */
.card-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.kb-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.kb-info {
  flex: 1;
  min-width: 0;
}

.kb-name {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.kb-code {
  font-size: 12px;
  color: #999999;
  margin: 0;
  font-family: 'Courier New', monospace;
}

.card-more {
  cursor: pointer;
  padding: 4px;
  color: #999999;
  transition: color 0.3s;
}

.card-more:hover {
  color: #667eea;
}

.icon-more-dot::before {
  content: '⋮';
  font-size: 18px;
}

/* 知识库描述 */
.kb-description {
  font-size: 13px;
  color: #666666;
  line-height: 1.6;
  margin: 0 0 16px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 统计信息 */
.kb-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.kb-stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.kb-stat-item .stat-label {
  font-size: 12px;
  color: #999999;
}

.kb-stat-item .stat-value {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
}

/* 最后更新 */
.kb-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  padding-bottom: 16px;
  margin-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.meta-label {
  color: #999999;
}

.meta-value {
  color: #666666;
  font-weight: 500;
}

/* 底部状态栏 */
.kb-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.kb-status {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-active {
  background: #d1fae5;
  color: #059669;
}

.status-active .status-dot {
  background: #059669;
}

.status-processing {
  background: #fef3c7;
  color: #d97706;
}

.status-processing .status-dot {
  background: #d97706;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
}

.status-inactive {
  background: #f3f4f6;
  color: #6b7280;
}

.status-inactive .status-dot {
  background: #6b7280;
}

.viewers-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #666666;
}

.icon-eye::before {
  content: '👁️';
  font-size: 14px;
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

.empty-text {
  font-size: 16px;
  color: #666666;
  margin: 0 0 8px 0;
}

.empty-hint {
  font-size: 14px;
  color: #999999;
  margin: 0;
}

/* 响应式 */
@media (max-width: 1200px) {
  .knowledge-list {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .knowledge-list {
    grid-template-columns: 1fr;
  }
}
</style>

