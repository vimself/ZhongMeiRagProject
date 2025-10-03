<template>
  <div class="dialog-overlay" @click.self="$emit('close')">
    <div class="dialog-container">
      <!-- 对话框标题 -->
      <div class="dialog-header">
        <h2 class="dialog-title">上传文档</h2>
        <button class="btn-close" @click="$emit('close')">✕</button>
      </div>

      <!-- 对话框内容 -->
      <div class="dialog-body">
        <!-- 上传区域 -->
        <div class="upload-area" @click="triggerFileInput">
          <input 
            ref="fileInput"
            type="file" 
            multiple
            accept=".pdf"
            style="display: none;"
            @change="handleFileSelect"
          />
          <div class="upload-placeholder">
            <span class="icon-upload">📤</span>
            <p>点击或拖拽文件到此处上传</p>
            <p class="upload-tip">支持PDF格式，单个文件最大200MB</p>
          </div>
        </div>

        <!-- 文件列表 -->
        <div v-if="selectedFiles.length > 0" class="file-list">
          <h3 class="file-list-title">待上传文件（{{ selectedFiles.length }}）</h3>
          <div 
            v-for="(file, index) in selectedFiles" 
            :key="index" 
            class="file-item"
          >
            <div class="file-icon">📄</div>
            <div class="file-info">
              <div class="file-name">{{ file.name }}</div>
              <div class="file-size">{{ formatFileSize(file.size) }}</div>
            </div>
            <button class="file-remove" @click="removeFile(index)">
              <span>✕</span>
            </button>
          </div>
        </div>

        <!-- 上传进度 -->
        <div v-if="uploading" class="upload-progress">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
          </div>
          <div class="progress-text">上传中 {{ uploadProgress }}%</div>
        </div>
      </div>

      <!-- 对话框底部按钮 -->
      <div class="dialog-footer">
        <button class="btn-secondary" @click="$emit('close')" :disabled="uploading">
          取消
        </button>
        <button 
          class="btn-primary" 
          @click="handleUpload"
          :disabled="selectedFiles.length === 0 || uploading"
        >
          {{ uploading ? '上传中...' : '开始上传' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { uploadDocument } from '@/api/knowledgeApi'

const props = defineProps({
  knowledgeBaseId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close', 'uploaded'])

// 状态
const fileInput = ref(null)
const selectedFiles = ref([])
const uploading = ref(false)
const uploadProgress = ref(0)

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value?.click()
}

// 处理文件选择
const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  
  // 验证文件
  const validFiles = files.filter(file => {
    if (file.size > 200 * 1024 * 1024) {
      alert(`文件 ${file.name} 超过200MB，已忽略`)
      return false
    }
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      alert(`文件 ${file.name} 不是PDF格式，已忽略`)
      return false
    }
    return true
  })
  
  selectedFiles.value = [...selectedFiles.value, ...validFiles]
  
  // 清空input值，允许重复选择同一文件
  event.target.value = ''
}

// 移除文件
const removeFile = (index) => {
  selectedFiles.value.splice(index, 1)
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

// 处理上传
const handleUpload = async () => {
  if (selectedFiles.value.length === 0 || uploading.value) {
    return
  }

  try {
    uploading.value = true
    uploadProgress.value = 0

    // 创建FormData
    const formData = new FormData()
    formData.append('knowledgeBaseId', props.knowledgeBaseId)
    
    selectedFiles.value.forEach(file => {
      formData.append('files', file)
    })

    // 模拟进度（实际项目中应从xhr.upload.onprogress获取真实进度）
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 10
      }
    }, 200)

    const res = await uploadDocument(formData)
    
    clearInterval(progressInterval)
    uploadProgress.value = 100

    if (res.success) {
      setTimeout(() => {
        alert('上传成功！文档正在处理中')
        emit('uploaded')
      }, 300)
    }
  } catch (error) {
    console.error('上传失败:', error)
    alert(error.message || '上传失败')
    uploadProgress.value = 0
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
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

.dialog-container {
  background: #ffffff;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #f0f0f0;
}

.dialog-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.btn-close {
  width: 32px;
  height: 32px;
  border: none;
  background: #f5f7fa;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #666666;
  transition: all 0.2s;
}

.btn-close:hover {
  background: #e5e7eb;
}

.dialog-body {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

/* 上传区域 */
.upload-area {
  border: 2px dashed #e5e7eb;
  border-radius: 12px;
  padding: 48px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 24px;
}

.upload-area:hover {
  border-color: #667eea;
  background: #f9fafb;
}

.icon-upload {
  font-size: 56px;
  display: block;
  margin-bottom: 16px;
}

.upload-placeholder p {
  margin: 8px 0;
  font-size: 14px;
  color: #333333;
}

.upload-tip {
  color: #9ca3af !important;
  font-size: 12px !important;
}

/* 文件列表 */
.file-list {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
}

.file-list-title {
  font-size: 14px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 12px 0;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  margin-bottom: 8px;
}

.file-item:last-child {
  margin-bottom: 0;
}

.file-icon {
  font-size: 24px;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 14px;
  color: #333333;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  font-size: 12px;
  color: #9ca3af;
}

.file-remove {
  width: 28px;
  height: 28px;
  border: none;
  background: #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666666;
  transition: all 0.2s;
}

.file-remove:hover {
  background: #d1d5db;
  color: #ef4444;
}

/* 上传进度 */
.upload-progress {
  margin-top: 24px;
}

.progress-bar {
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.progress-text {
  font-size: 13px;
  color: #667eea;
  font-weight: 500;
  text-align: center;
}

/* 对话框底部 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 32px;
  border-top: 1px solid #f0f0f0;
}

.btn-secondary,
.btn-primary {
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary {
  background: #f5f7fa;
  color: #333333;
}

.btn-secondary:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

