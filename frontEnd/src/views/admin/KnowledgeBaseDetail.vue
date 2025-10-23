<template>
  <div class="knowledge-detail-page">
    <!-- 页面标题区域 -->
    <div class="page-header">
      <div class="header-left">
        <button class="btn-back" @click="goBack">
          <span class="icon-back"></span>
        </button>
        <div class="header-info">
          <h1 class="page-title">{{ knowledgeBase.name || '知识库详情' }}</h1>
          <p class="page-subtitle">{{ knowledgeBase.description }}</p>
        </div>
      </div>
      <div class="header-right">
        <button class="btn-secondary" @click="showUploadDialog = true">
          <span class="icon-upload"></span>
          上传文档
        </button>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="stats-cards" v-if="!loading">
      <div class="stat-card">
        <div class="stat-icon stat-icon-blue">
          <i class="icon-doc-count"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ documents.total || 0 }}</div>
          <div class="stat-label">文档总数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon stat-icon-green">
          <i class="icon-storage-size"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ knowledgeBase.storageSize || '0 MB' }}</div>
          <div class="stat-label">存储大小</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon stat-icon-yellow">
          <i class="icon-viewers"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ knowledgeBase.viewers || 0 }}</div>
          <div class="stat-label">查看人数</div>
        </div>
      </div>
    </div>

    <!-- 文档列表 -->
    <div class="documents-section">
      <div class="section-header">
        <h2 class="section-title">文档列表</h2>
        <div class="section-actions">
          <button 
            v-if="selectedDocIds.length > 0" 
            class="btn-export"
            @click="handleBatchExport"
            :disabled="exporting"
          >
            <span class="icon-export">📦</span>
            {{ exporting ? 'ZIP打包中...' : `导出为ZIP (${selectedDocIds.length}个文件)` }}
          </button>
          <input 
            type="text" 
            class="search-input" 
            placeholder="搜索文档..."
            v-model="searchKeyword"
          />
        </div>
      </div>

      <!-- 文档表格 -->
      <div class="documents-table" v-if="!loading && filteredDocuments.length > 0">
        <table>
          <thead>
            <tr>
              <th style="width: 50px;">
                <input 
                  type="checkbox" 
                  class="doc-checkbox"
                  :checked="isAllSelected"
                  @change="handleSelectAll"
                />
              </th>
              <th>文件名称</th>
              <th>大小</th>
              <th>导入时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in filteredDocuments" :key="doc.id">
              <td>
                <input 
                  type="checkbox" 
                  class="doc-checkbox"
                  :checked="selectedDocIds.includes(doc.id)"
                  @change="handleSelectDoc(doc.id)"
                />
              </td>
              <td>
                <div class="doc-name-cell">
                  <span class="doc-icon"></span>
                  <span class="doc-name" @click="handlePreview(doc)">{{ doc.name }}</span>
                </div>
              </td>
              <td>{{ doc.size }}</td>
              <td>{{ doc.uploadTime }}</td>
              <td>
                <div class="table-actions">
                  <button class="btn-action" @click="handlePreview(doc)" title="查看">
                    <span class="icon-view"></span>
                  </button>
                  <button class="btn-action" @click="handleDelete(doc)" title="删除">
                    <span class="icon-delete-doc"></span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 加载状态 -->
      <div class="loading-state" v-if="loading">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- 空状态 -->
      <div class="empty-state" v-if="!loading && filteredDocuments.length === 0">
        <span class="icon-empty">📭</span>
        <h3>暂无文档</h3>
        <p>点击"上传文档"按钮添加文档</p>
      </div>
    </div>

    <!-- 上传文档对话框 -->
    <UploadDocumentDialog 
      v-if="showUploadDialog"
      :knowledgeBaseId="knowledgeBaseId"
      @close="showUploadDialog = false"
      @uploaded="handleUploaded"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getKnowledgeBaseDetail, getKnowledgeBaseDocuments, deleteDocument, exportDocuments } from '@/api/knowledgeApi'
import UploadDocumentDialog from './components/UploadDocumentDialog.vue'

const router = useRouter()
const route = useRoute()

// 知识库ID
const knowledgeBaseId = ref(route.params.id)

// 状态
const loading = ref(false)
const knowledgeBase = ref({})
const documents = ref({ list: [], total: 0 })
const searchKeyword = ref('')
const showUploadDialog = ref(false)
const selectedDocIds = ref([])
const exporting = ref(false)

// 过滤后的文档列表
const filteredDocuments = computed(() => {
  if (!searchKeyword.value) {
    return documents.value.list
  }
  return documents.value.list.filter(doc => 
    doc.name.toLowerCase().includes(searchKeyword.value.toLowerCase())
  )
})

// 是否全选
const isAllSelected = computed(() => {
  return filteredDocuments.value.length > 0 && 
         selectedDocIds.value.length === filteredDocuments.value.length
})

// 返回上一页
const goBack = () => {
  router.back()
}

// 获取知识库详情
const fetchKnowledgeBaseDetail = async () => {
  try {
    const res = await getKnowledgeBaseDetail({ id: knowledgeBaseId.value })
    if (res.success) {
      knowledgeBase.value = res.data
    }
  } catch (error) {
    console.error('获取知识库详情失败:', error)
  }
}

// 获取文档列表
const fetchDocuments = async () => {
  try {
    loading.value = true
    const res = await getKnowledgeBaseDocuments({ 
      knowledgeBaseId: knowledgeBaseId.value 
    })
    if (res.success) {
      documents.value = res.data
    }
  } catch (error) {
    console.error('获取文档列表失败:', error)
    alert(error.message || '获取文档列表失败')
  } finally {
    loading.value = false
  }
}

// 预览文档
const handlePreview = (doc) => {
  router.push(`/admin/knowledge-management/${knowledgeBaseId.value}/document/${doc.id}`)
}

// 删除文档
const handleDelete = async (doc) => {
  if (!confirm(`确定要删除文档"${doc.name}"吗？此操作不可恢复。`)) {
    return
  }

  try {
    const res = await deleteDocument({ 
      knowledgeBaseId: knowledgeBaseId.value,
      documentId: doc.id 
    })
    if (res.success) {
      alert('删除成功')
      await fetchDocuments()
    }
  } catch (error) {
    console.error('删除文档失败:', error)
    alert(error.message || '删除失败')
  }
}

// 上传成功回调
const handleUploaded = () => {
  showUploadDialog.value = false
  fetchDocuments()
}

// 选择文档
const handleSelectDoc = (docId) => {
  const index = selectedDocIds.value.indexOf(docId)
  if (index > -1) {
    selectedDocIds.value.splice(index, 1)
  } else {
    selectedDocIds.value.push(docId)
  }
}

// 全选/取消全选
const handleSelectAll = () => {
  if (isAllSelected.value) {
    selectedDocIds.value = []
  } else {
    selectedDocIds.value = filteredDocuments.value.map(doc => doc.id)
  }
}

// 批量导出文档
const handleBatchExport = async () => {
  if (selectedDocIds.value.length === 0 || exporting.value) {
    return
  }

  try {
    exporting.value = true
    const res = await exportDocuments({
      knowledgeBaseId: knowledgeBaseId.value,
      documentIds: selectedDocIds.value
    })
    
    if (res.success) {
      // 触发浏览器下载
      const downloadUrl = res.data.downloadUrl
      window.open(downloadUrl, '_blank')
      
      alert(`已将 ${selectedDocIds.value.length} 个文档打包为ZIP并下载到本地`)
      selectedDocIds.value = []
    }
  } catch (error) {
    console.error('导出失败:', error)
    alert(error.message || '导出失败')
  } finally {
    exporting.value = false
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchKnowledgeBaseDetail()
  fetchDocuments()
})
</script>

<style scoped>
.knowledge-detail-page {
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
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.btn-back {
  width: 40px;
  height: 40px;
  border: none;
  background: #ffffff;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #666666;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.btn-back:hover {
  background: #f5f7fa;
}

.icon-back {
  display: block;
  width: 20px;
  height: 20px;
  background-image: url('@/assets/icons/icon-back-arrow.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.header-info {
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

.btn-secondary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #ffffff;
  color: #333333;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #f9fafb;
}

.icon-upload {
  width: 18px;
  height: 18px;
  background-image: url('@/assets/icons/icon-upload-doc-btn.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon-blue {
  background: #dbeafe;
}

.stat-icon-green {
  background: #d1fae5;
}

.stat-icon-yellow {
  background: #fef3c7;
}

.icon-doc-count {
  width: 28px;
  height: 28px;
  background-image: url('@/assets/icons/icon-doc-count.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-storage-size {
  width: 28px;
  height: 28px;
  background-image: url('@/assets/icons/icon-storage-size.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-viewers {
  width: 28px;
  height: 28px;
  background-image: url('@/assets/icons/icon-viewers-count.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #666666;
}

/* 文档列表部分 */
.documents-section {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.section-actions {
  display: flex;
  gap: 12px;
}

.search-input {
  width: 300px;
  padding: 8px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

/* 文档表格 */
.documents-table {
  overflow-x: auto;
}

.documents-table table {
  width: 100%;
  border-collapse: collapse;
}

.documents-table th {
  text-align: left;
  padding: 12px;
  background: #f9fafb;
  color: #666666;
  font-size: 13px;
  font-weight: 500;
  border-bottom: 1px solid #e5e7eb;
}

.documents-table td {
  padding: 14px 12px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
  color: #333333;
}

.documents-table tr:hover td {
  background: #f9fafb;
}

.doc-name-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.doc-icon {
  width: 20px;
  height: 20px;
  background-image: url('@/assets/icons/icon-doc-type-pdf.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.doc-name {
  color: #667eea;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
}

.doc-name:hover {
  text-decoration: underline;
}

.doc-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.btn-export {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #f0f9ff;
  color: #0369a1;
  border: 1px solid #bae6fd;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-export:hover:not(:disabled) {
  background: #e0f2fe;
  border-color: #7dd3fc;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(3, 105, 161, 0.15);
}

.btn-export:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f0f9ff;
}

.icon-export {
  font-size: 16px;
}

.table-actions {
  display: flex;
  gap: 8px;
}

.btn-action {
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

.btn-action:hover {
  background: #e5e7eb;
}

.icon-view {
  width: 18px;
  height: 18px;
  background-image: url('@/assets/icons/icon-eye-open.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-delete-doc {
  width: 18px;
  height: 18px;
  background-image: url('@/assets/icons/icon-delete-doc.svg');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
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
  padding: 80px 40px;
}

.icon-empty {
  font-size: 64px;
  display: block;
  margin-bottom: 24px;
}

.empty-state h3 {
  font-size: 18px;
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

