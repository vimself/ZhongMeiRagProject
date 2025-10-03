<template>
  <div class="document-preview-page">
    <!-- 页面标题区域 -->
    <div class="page-header">
      <div class="header-left">
        <button class="btn-back" @click="goBack">
          <span class="icon-back">←</span>
        </button>
        <div class="header-info">
          <h1 class="page-title">{{ document.name || '文档预览' }}</h1>
          <p class="page-subtitle">{{ document.type || 'PDF' }} 文档</p>
        </div>
      </div>
      <div class="header-right">
        <button class="btn-secondary" @click="downloadDocument" v-if="document.previewUrl">
          <span class="icon-download">📥</span>
          下载文档
        </button>
      </div>
    </div>

    <!-- 文档预览区域 -->
    <div class="preview-container">
      <div class="preview-wrapper" v-if="!loading && document.previewUrl">
        <!-- PDF预览 -->
        <iframe 
          v-if="document.type === 'pdf'"
          :src="document.previewUrl" 
          class="pdf-viewer"
          frameborder="0"
        ></iframe>
        
        <!-- 其他类型文档暂不支持 -->
        <div v-else class="unsupported-type">
          <span class="icon-warning">⚠️</span>
          <h3>暂不支持此类型文档的在线预览</h3>
          <p>请下载文档后使用本地应用查看</p>
        </div>
      </div>

      <!-- 加载状态 -->
      <div class="loading-state" v-if="loading">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- 错误状态 -->
      <div class="error-state" v-if="!loading && !document.previewUrl">
        <span class="icon-error">❌</span>
        <h3>文档加载失败</h3>
        <p>无法找到文档或文档已被删除</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getDocumentPreview } from '@/api/knowledgeApi'

const router = useRouter()
const route = useRoute()

// 文档ID
const documentId = ref(route.params.documentId)
const knowledgeBaseId = ref(route.params.id)

// 状态
const loading = ref(false)
const document = ref({})

// 返回上一页
const goBack = () => {
  router.back()
}

// 获取文档预览信息
const fetchDocumentPreview = async () => {
  try {
    loading.value = true
    const res = await getDocumentPreview({ documentId: documentId.value })
    if (res.success) {
      document.value = res.data
    }
  } catch (error) {
    console.error('获取文档预览失败:', error)
    alert(error.message || '获取文档预览失败')
  } finally {
    loading.value = false
  }
}

// 下载文档
const downloadDocument = () => {
  if (document.value.previewUrl) {
    window.open(document.value.previewUrl, '_blank')
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchDocumentPreview()
})
</script>

<style scoped>
.document-preview-page {
  padding: 32px 48px;
  max-width: 1800px;
  margin: 0 auto;
  background: #f5f7fa;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
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
}

.header-info {
  flex: 1;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 4px 0;
}

.page-subtitle {
  font-size: 13px;
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

/* 预览容器 */
.preview-container {
  flex: 1;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 600px;
}

.preview-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.pdf-viewer {
  width: 100%;
  flex: 1;
  border: none;
  min-height: 600px;
}

/* 不支持的类型 */
.unsupported-type {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
}

.icon-warning {
  font-size: 64px;
  display: block;
  margin-bottom: 24px;
}

.unsupported-type h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.unsupported-type p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

/* 加载状态 */
.loading-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f0f0f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  color: #666666;
  font-size: 14px;
  margin: 0;
}

/* 错误状态 */
.error-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
}

.icon-error {
  font-size: 64px;
  display: block;
  margin-bottom: 24px;
}

.error-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.error-state p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}
</style>

