<template>
  <div class="dashboard-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">仪表板</h1>
        <p class="page-subtitle">欢迎使用RAG知识问答系统</p>
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
      <!-- 今日问答 -->
      <div class="stat-card stat-card-blue">
        <div class="stat-icon">
          <i class="icon-chat-stat"></i>
        </div>
        <div class="stat-content">
          <div class="stat-label">今日问答</div>
          <div class="stat-value">{{ stats.todayQuestions.count }}</div>
          <div class="stat-change stat-increase">
            +{{ stats.todayQuestions.change }}% 较昨日
          </div>
        </div>
      </div>

      <!-- 搜索次数 -->
      <div class="stat-card stat-card-green">
        <div class="stat-icon">
          <i class="icon-search-stat"></i>
        </div>
        <div class="stat-content">
          <div class="stat-label">搜索次数</div>
          <div class="stat-value">{{ stats.searchCount.count }}</div>
          <div class="stat-change stat-increase">
            +{{ stats.searchCount.change }}% 较昨日
          </div>
        </div>
      </div>

      <!-- 知识库数量 -->
      <div class="stat-card stat-card-yellow">
        <div class="stat-icon">
          <i class="icon-kb-stat"></i>
        </div>
        <div class="stat-content">
          <div class="stat-label">知识库数量</div>
          <div class="stat-value">{{ stats.knowledgeBaseCount.count }}</div>
          <div class="stat-change stat-new">
            +{{ stats.knowledgeBaseCount.newCount }} 本周新增
          </div>
        </div>
      </div>

      <!-- 文档总数 -->
      <div class="stat-card stat-card-purple">
        <div class="stat-icon">
          <i class="icon-doc-stat"></i>
        </div>
        <div class="stat-content">
          <div class="stat-label">文档总数</div>
          <div class="stat-value">{{ stats.documentCount.count.toLocaleString() }}</div>
          <div class="stat-change stat-new">
            +{{ stats.documentCount.newCount }} 本周新增
          </div>
        </div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-grid">
      <!-- 左侧：说明文档 -->
      <div class="left-section">
        <h2 class="section-title">说明文档</h2>
        <div class="doc-cards">
          <!-- RAG系统 -->
          <!-- <div class="doc-card" @click="goToDoc('rag')">
            <div class="doc-icon doc-icon-orange">
              <i class="icon-rag"></i>
            </div>
            <div class="doc-content">
              <h3 class="doc-title">RAG系统</h3>
              <p class="doc-desc">了解该系统的RAG技术原理和功能特性</p>
            </div>
            <div class="doc-arrow">
              <i class="icon-arrow-right"></i>
            </div>
          </div> -->

          <!-- 知识库管理 -->
          <div class="doc-card" @click="goToDoc('knowledge')">
            <div class="doc-icon doc-icon-blue">
              <i class="icon-knowledge-doc"></i>
            </div>
            <div class="doc-content">
              <h3 class="doc-title">知识库管理</h3>
              <p class="doc-desc">设置文件上传大小规则，分片长度，策略等</p>
            </div>
            <div class="doc-arrow">
              <i class="icon-arrow-right"></i>
            </div>
          </div>

          <!-- 文件上传 -->
          <div class="doc-card" @click="goToDoc('upload')">
            <div class="doc-icon doc-icon-green">
              <i class="icon-upload-doc"></i>
            </div>
            <div class="doc-content">
              <h3 class="doc-title">文件上传</h3>
              <p class="doc-desc">快速文件上传教程指南</p>
            </div>
            <div class="doc-arrow">
              <i class="icon-arrow-right"></i>
            </div>
          </div>

          <!-- 模型管理 -->
          <div class="doc-card" @click="goToDoc('model')">
            <div class="doc-icon doc-icon-brown">
              <i class="icon-model-doc"></i>
            </div>
            <div class="doc-content">
              <h3 class="doc-title">模型管理</h3>
              <p class="doc-desc">添加新的模型教程指南</p>
            </div>
            <div class="doc-arrow">
              <i class="icon-arrow-right"></i>
            </div>
          </div>

          <!-- 用户管理 -->
          <div class="doc-card" @click="goToDoc('user')">
            <div class="doc-icon doc-icon-purple">
              <i class="icon-user-doc"></i>
            </div>
            <div class="doc-content">
              <h3 class="doc-title">用户管理</h3>
              <p class="doc-desc">用户权限管理和账号设置指南</p>
            </div>
            <div class="doc-arrow">
              <i class="icon-arrow-right"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：系统状态 -->
      <div class="right-section">
        <div class="section-header">
          <h2 class="section-title">系统状态</h2>
        </div>

        <div class="status-cards">
          <!-- LLM 模型 -->
          <div class="status-card status-card-blue">
            <div class="status-icon">
              <i class="icon-llm"></i>
            </div>
            <div class="status-content">
              <h3 class="status-name">{{ systemStatus.llmModel.name }}</h3>
              <p class="status-desc">{{ systemStatus.llmModel.description }}</p>
            </div>
            <div class="status-indicator">
              <span class="status-badge status-online">
                <i class="status-dot"></i>
                在线 {{ systemStatus.llmModel.online }}/{{ systemStatus.llmModel.total }}
              </span>
            </div>
          </div>

          <!-- 向量模型 -->
          <div class="status-card status-card-green">
            <div class="status-icon">
              <i class="icon-vector"></i>
            </div>
            <div class="status-content">
              <h3 class="status-name">{{ systemStatus.vectorModel.name }}</h3>
              <p class="status-desc">{{ systemStatus.vectorModel.description }}</p>
            </div>
            <div class="status-indicator">
              <span class="status-badge status-online">
                <i class="status-dot"></i>
                在线 {{ systemStatus.vectorModel.online }}/{{ systemStatus.vectorModel.total }}
              </span>
            </div>
          </div>

          <!-- 向量数据库 -->
          <div class="status-card status-card-purple">
            <div class="status-icon">
              <i class="icon-vector-db"></i>
            </div>
            <div class="status-content">
              <h3 class="status-name">{{ systemStatus.vectorDb.name }}</h3>
              <p class="status-desc">{{ systemStatus.vectorDb.description }}</p>
            </div>
            <div class="status-indicator">
              <span class="status-badge status-normal">
                <i class="status-dot"></i>
                正常
              </span>
            </div>
          </div>

          <!-- 关系数据库 -->
          <div class="status-card status-card-yellow">
            <div class="status-icon">
              <i class="icon-relation-db"></i>
            </div>
            <div class="status-content">
              <h3 class="status-name">{{ systemStatus.relationalDb.name }}</h3>
              <p class="status-desc">{{ systemStatus.relationalDb.description }}</p>
            </div>
            <div class="status-indicator">
              <span class="status-badge status-normal">
                <i class="status-dot"></i>
                正常
              </span>
            </div>
          </div>
        </div>

        <!-- 系统状态底部 -->
        <div class="system-footer">
          <div class="system-overall">
            <i class="icon-check-circle"></i>
            <span>系统运行正常</span>
          </div>
          <div class="footer-right">
            <button class="refresh-btn" @click="refreshStatus" :disabled="refreshing">
              <i class="icon-refresh" :class="{ 'spinning': refreshing }"></i>
            </button>
            <div class="last-update">
              最后更新：{{ systemStatus.lastUpdate }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { getDashboardStats, getSystemStatus, refreshSystemStatus } from '../api/dashboardApi'

const router = useRouter()

// 当前时间
const currentTime = ref('')

// 统计数据
const stats = ref({
  todayQuestions: {
    count: 0,
    change: 0,
    changeType: 'increase'
  },
  searchCount: {
    count: 0,
    change: 0,
    changeType: 'increase'
  },
  knowledgeBaseCount: {
    count: 0,
    newCount: 0
  },
  documentCount: {
    count: 0,
    newCount: 0
  }
})

// 系统状态
const systemStatus = ref({
  llmModel: {
    name: 'LLM 模型',
    description: '大语言模型服务',
    status: 'online',
    online: 0,
    total: 0
  },
  vectorModel: {
    name: '向量模型',
    description: '嵌入向量服务',
    status: 'online',
    online: 0,
    total: 0
  },
  vectorDb: {
    name: '向量数据库',
    description: '向量存储服务',
    status: 'normal'
  },
  relationalDb: {
    name: '关系数据库',
    description: '业务数据存储',
    status: 'normal'
  },
  systemStatus: 'normal',
  lastUpdate: ''
})

// 刷新状态
const refreshing = ref(false)

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
  try {
    const [statsRes, statusRes] = await Promise.all([
      getDashboardStats(),
      getSystemStatus()
    ])
    
    stats.value = statsRes.data
    systemStatus.value = statusRes.data
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

/**
 * 刷新系统状态
 */
async function refreshStatus() {
  refreshing.value = true
  
  try {
    const res = await refreshSystemStatus()
    systemStatus.value = res.data
  } catch (error) {
    console.error('刷新失败:', error)
  } finally {
    setTimeout(() => {
      refreshing.value = false
    }, 500)
  }
}

/**
 * 前往文档页面
 */
function goToDoc(type) {
  // 这里可以跳转到对应的文档页面或打开文档链接
  console.log('查看文档:', type)
}
</script>

<style scoped>
.dashboard-page {
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
  align-items: center;
  height: 88px;
  margin-bottom: 20px;
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
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
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

.stat-card-yellow .stat-icon {
  background: #fef3c7;
}

.stat-card-purple .stat-icon {
  background: #e9d5ff;
}

.icon-chat-stat {
  width: 28px;
  height: 28px;
  background-image: url('@/assets/icons/icon-chat-stat.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-search-stat {
  width: 28px;
  height: 28px;
  background-image: url('@/assets/icons/icon-search-btn.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-kb-stat {
  width: 28px;
  height: 28px;
  background-image: url('@/assets/icons/icon-database.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-doc-stat {
  width: 28px;
  height: 28px;
  background-image: url('@/assets/icons/icon-doc-type-pdf.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #1a1a1a;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-change {
  font-size: 13px;
  font-weight: 500;
}

.stat-increase {
  color: #10b981;
}

.stat-new {
  color: #6b7280;
}

/* 内容区域 */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  align-items: start;
}

/* 左侧：说明文档 */
.left-section {
  background: transparent;
}

.left-section .section-title {
  height: 40px;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
}

/* 右侧：系统状态 */
.right-section {
  background: transparent;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 16px 0;
}

.doc-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.doc-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 18px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.doc-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateX(4px);
}

.doc-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: linear-gradient(135deg, rgba(147, 197, 253, 0.25) 0%, rgba(96, 165, 250, 0.35) 100%);
  backdrop-filter: blur(10px);
}

.doc-icon-orange {
  background: linear-gradient(135deg, rgba(147, 197, 253, 0.25) 0%, rgba(96, 165, 250, 0.35) 100%);
}

.doc-icon-blue {
  background: linear-gradient(135deg, rgba(147, 197, 253, 0.25) 0%, rgba(96, 165, 250, 0.35) 100%);
}

.doc-icon-green {
  background: linear-gradient(135deg, rgba(147, 197, 253, 0.25) 0%, rgba(96, 165, 250, 0.35) 100%);
}

.doc-icon-brown {
  background: linear-gradient(135deg, rgba(147, 197, 253, 0.25) 0%, rgba(96, 165, 250, 0.35) 100%);
}

.doc-icon-purple {
  background: linear-gradient(135deg, rgba(147, 197, 253, 0.25) 0%, rgba(96, 165, 250, 0.35) 100%);
}

.doc-icon i {
  width: 26px;
  height: 26px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  filter: brightness(0) saturate(100%) invert(25%) sepia(8%) saturate(820%) hue-rotate(182deg) brightness(95%) contrast(90%);
}

.icon-rag {
  background-image: url('@/assets/icons/icon-rag.svg');
}

.icon-knowledge-doc {
  background-image: url('@/assets/icons/icon-rag.svg');
}

.icon-upload-doc {
  background-image: url('@/assets/icons/icon-upload-doc-btn.svg');
}

.icon-model-doc {
  background-image: url('@/assets/icons/icon-model.svg');
}

.icon-user-doc {
  background-image: url('@/assets/icons/icon-user.svg');
}

.doc-content {
  flex: 1;
  min-width: 0;
}

.doc-title {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 4px 0;
}

.doc-desc {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
  line-height: 1.4;
}

.doc-arrow {
  color: #d1d5db;
  font-size: 18px;
  transition: all 0.3s;
}

.doc-card:hover .doc-arrow {
  color: #667eea;
  transform: translateX(4px);
}

.icon-arrow-right {
  width: 18px;
  height: 18px;
  background-image: url('@/assets/icons/icon-arrow-right.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

/* 右侧：系统状态 */
.right-section {
  background: transparent;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  height: 40px;
}

.refresh-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.refresh-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #667eea;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon-refresh {
  width: 18px;
  height: 18px;
  background-image: url('@/assets/icons/icon-refresh.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-refresh.spinning {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.status-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.status-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s;
}

.status-card-blue {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
}

.status-card-green {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
}

.status-card-purple {
  background: linear-gradient(135deg, #e9d5ff 0%, #d8b4fe 100%);
}

.status-card-yellow {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
}

.status-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
}

.icon-llm {
  width: 22px;
  height: 22px;
  background-image: url('@/assets/icons/icon-llm.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-vector {
  width: 22px;
  height: 22px;
  background-image: url('@/assets/icons/icon-vector.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-vector-db {
  width: 22px;
  height: 22px;
  background-image: url('@/assets/icons/icon-vector-db.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-relation-db {
  width: 22px;
  height: 22px;
  background-image: url('@/assets/icons/icon-relation-db.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.status-content {
  flex: 1;
  min-width: 0;
}

.status-name {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 4px 0;
}

.status-desc {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
}

.status-indicator {
  flex-shrink: 0;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.9);
}

.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-online {
  color: #059669;
}

.status-online .status-dot {
  background: #10b981;
}

.status-normal {
  color: #059669;
}

.status-normal .status-dot {
  background: #10b981;
}

/* 系统状态底部 */
.system-footer {
  background: #ffffff;
  border-radius: 12px;
  padding: 14px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  margin-top: 4px;
}

.system-overall {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #059669;
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-check-circle {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #10b981;
}

.last-update {
  font-size: 13px;
  color: #6b7280;
}

/* 响应式 */
@media (max-width: 1400px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>

