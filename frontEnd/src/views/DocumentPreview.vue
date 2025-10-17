<template>
  <div class="document-preview-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <button class="btn-back" @click="goBack">
          <span class="icon-back">←</span>
        </button>
        <div class="header-info">
          <h1 class="page-title">{{ documentInfo.name || '文档预览' }}</h1>
          <p class="page-subtitle">文档查看</p>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载文档中...</p>
    </div>

    <!-- 文档预览区域 -->
    <div v-else-if="documentInfo.previewUrl" class="preview-container">
      <iframe 
        :src="documentInfo.previewUrl" 
        class="preview-iframe"
        frameborder="0"
      ></iframe>
    </div>

    <!-- 错误状态 -->
    <div v-else class="error-state">
      <span class="icon-error">⚠️</span>
      <h3>无法加载文档</h3>
      <p>{{ errorMessage || '文档加载失败，请稍后重试' }}</p>
      <button class="btn-retry" @click="fetchDocumentPreview">重试</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getDocumentPreview } from '@/api/knowledgeApi'

const router = useRouter()
const route = useRoute()

// 文档ID和知识库ID
const documentId = ref(route.params.documentId)
const knowledgeBaseId = ref(route.params.id)

// 状态
const loading = ref(false)
const documentInfo = ref({})
const errorMessage = ref('')

// 返回上一页
const goBack = () => {
  router.push(`/knowledge/${knowledgeBaseId.value}`)
}

// 获取文档预览信息
const fetchDocumentPreview = async () => {
  try {
    loading.value = true
    errorMessage.value = ''
    const res = await getDocumentPreview({ documentId: documentId.value })
    
    if (res.success) {
      documentInfo.value = res.data
    }
  } catch (error) {
    console.error('获取文档预览失败:', error)
    errorMessage.value = error.message || '获取文档预览失败'
    if (error.code === 403) {
      errorMessage.value = '您没有权限查看该文档'
    }
  } finally {
    loading.value = false
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchDocumentPreview()
})
</script>

<style scoped>
.document-preview-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 32px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-back {
  width: 40px;
  height: 40px;
  border: none;
  background: #f5f7fa;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #666666;
  transition: all 0.2s;
}

.btn-back:hover {
  background: #e5e7eb;
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

/* 加载状态 */
.loading-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #666666;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f0f0f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-container p {
  font-size: 14px;
  margin: 0;
}

/* 预览区域 */
.preview-container {
  flex: 1;
  padding: 24px 32px;
  overflow: hidden;
}

.preview-iframe {
  width: 100%;
  height: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

/* 错误状态 */
.error-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
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
  margin: 0 0 24px 0;
}

.btn-retry {
  padding: 10px 24px;
  background: #667eea;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-retry:hover {
  background: #5568d3;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-retry:active {
  transform: translateY(0);
}
</style>

