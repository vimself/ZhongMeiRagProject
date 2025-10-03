<template>
  <div class="knowledge-management-page">
    <!-- 页面标题区域 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">知识库管理</h1>
        <p class="page-subtitle">管理知识库配置和文档内容</p>
      </div>
      <div class="header-right">
        <button class="btn-primary" @click="showCreateDialog = true">
          <span class="icon-add">+</span>
          创建知识库
        </button>
      </div>
    </div>

    <!-- 知识库列表 -->
    <div class="knowledge-list" v-if="!loading && knowledgeList.length > 0">
      <div 
        class="knowledge-card" 
        v-for="kb in knowledgeList" 
        :key="kb.id"
        @click="navigateToDetail(kb.id)"
      >
        <div class="card-header">
          <div class="kb-icon" :style="{ background: kb.iconColor }">
            <span class="icon-kb">📚</span>
          </div>
          <div class="kb-info">
            <h3 class="kb-name">{{ kb.name }}</h3>
            <p class="kb-description">{{ kb.description }}</p>
          </div>
          <div class="kb-actions" @click.stop>
            <button class="btn-icon" @click="handleEdit(kb)">
              <span class="icon-edit">✏️</span>
            </button>
            <button class="btn-icon" @click="handleDelete(kb)">
              <span class="icon-delete">🗑️</span>
            </button>
          </div>
        </div>
        
        <div class="card-body">
          <div class="kb-stats">
            <div class="stat-item">
              <span class="stat-label">文档数量</span>
              <span class="stat-value">{{ kb.documentCount }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">存储大小</span>
              <span class="stat-value">{{ kb.storageSize }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">查看人数</span>
              <span class="stat-value">{{ kb.viewers }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">最后更新</span>
              <span class="stat-value">{{ kb.lastUpdate }}</span>
            </div>
          </div>

          <!-- 处理进度条 -->
          <div class="kb-progress" v-if="kb.status === 'processing'">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: kb.progress + '%' }"></div>
            </div>
            <span class="progress-text">处理中 {{ kb.progress }}%</span>
          </div>

          <!-- 标签区域 -->
          <div class="kb-tags" v-if="kb.tags && kb.tags.length > 0">
            <span 
              class="kb-tag" 
              v-for="(tag, index) in kb.tags.slice(0, 5)" 
              :key="index"
            >
              {{ tag }}
            </span>
          </div>

          <!-- 状态标签 -->
          <div class="kb-status">
            <span class="status-badge" :class="'status-' + kb.status">
              {{ getStatusText(kb.status) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div class="loading-state" v-if="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 空状态 -->
    <div class="empty-state" v-if="!loading && knowledgeList.length === 0">
      <span class="icon-empty">📭</span>
      <h3>暂无知识库</h3>
      <p>点击"创建知识库"按钮开始创建第一个知识库</p>
    </div>

    <!-- 创建知识库对话框 -->
    <CreateKnowledgeBaseDialog 
      v-if="showCreateDialog" 
      @close="showCreateDialog = false"
      @created="handleCreated"
    />

    <!-- 编辑知识库对话框 -->
    <EditKnowledgeBaseDialog 
      v-if="showEditDialog" 
      :knowledgeBase="currentKnowledgeBase"
      @close="showEditDialog = false"
      @updated="handleUpdated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getKnowledgeBaseList, deleteKnowledgeBase } from '@/api/knowledgeApi'
import CreateKnowledgeBaseDialog from './components/CreateKnowledgeBaseDialog.vue'
import EditKnowledgeBaseDialog from './components/EditKnowledgeBaseDialog.vue'

const router = useRouter()

// 状态
const loading = ref(false)
const knowledgeList = ref([])
const showCreateDialog = ref(false)
const showEditDialog = ref(false)
const currentKnowledgeBase = ref(null)

// 获取知识库列表
const fetchKnowledgeList = async () => {
  try {
    loading.value = true
    const res = await getKnowledgeBaseList()
    if (res.success) {
      knowledgeList.value = res.data
    }
  } catch (error) {
    console.error('获取知识库列表失败:', error)
    alert(error.message || '获取知识库列表失败')
  } finally {
    loading.value = false
  }
}

// 导航到知识库详情
const navigateToDetail = (id) => {
  router.push(`/admin/knowledge-management/${id}`)
}

// 编辑知识库
const handleEdit = (kb) => {
  currentKnowledgeBase.value = kb
  showEditDialog.value = true
}

// 删除知识库
const handleDelete = async (kb) => {
  if (!confirm(`确定要删除知识库"${kb.name}"吗？此操作不可恢复。`)) {
    return
  }

  try {
    const res = await deleteKnowledgeBase({ id: kb.id })
    if (res.success) {
      alert('删除成功')
      await fetchKnowledgeList()
    }
  } catch (error) {
    console.error('删除知识库失败:', error)
    alert(error.message || '删除失败')
  }
}

// 创建成功回调
const handleCreated = () => {
  showCreateDialog.value = false
  fetchKnowledgeList()
}

// 更新成功回调
const handleUpdated = () => {
  showEditDialog.value = false
  fetchKnowledgeList()
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'active': '活跃',
    'processing': '处理中',
    'inactive': '未激活'
  }
  return statusMap[status] || status
}

// 页面加载时获取数据
onMounted(() => {
  fetchKnowledgeList()
})
</script>

<style scoped>
.knowledge-management-page {
  padding: 32px 48px;
  max-width: 1800px;
  margin: 0 auto;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.header-left {
  flex: 1;
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
  gap: 12px;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.icon-add {
  font-size: 18px;
  font-weight: 600;
}

/* 知识库列表 */
.knowledge-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 24px;
}

.knowledge-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
  cursor: pointer;
}

.knowledge-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.kb-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
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
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.kb-description {
  font-size: 13px;
  color: #666666;
  margin: 0;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.kb-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border: none;
  background: #f5f7fa;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: #e5e7eb;
}

.card-body {
  border-top: 1px solid #f0f0f0;
  padding-top: 16px;
}

.kb-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stat-label {
  font-size: 12px;
  color: #999999;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #333333;
}

.kb-progress {
  margin-bottom: 12px;
}

.progress-bar {
  height: 6px;
  background: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.progress-text {
  font-size: 12px;
  color: #667eea;
  font-weight: 500;
}

.kb-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
  min-height: 28px;
}

.kb-tag {
  display: inline-block;
  padding: 4px 10px;
  background: #f3f4f6;
  color: #6b7280;
  border-radius: 4px;
  font-size: 12px;
  line-height: 20px;
  font-weight: 400;
}

.kb-status {
  display: flex;
  justify-content: flex-end;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-active {
  background: #d1fae5;
  color: #10b981;
}

.status-processing {
  background: #fef3c7;
  color: #f59e0b;
}

.status-inactive {
  background: #fee2e2;
  color: #ef4444;
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f0f0f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  color: #666666;
  font-size: 14px;
  margin: 0;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 120px 40px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.icon-empty {
  font-size: 64px;
  display: block;
  margin-bottom: 24px;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.empty-state p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}
</style>
