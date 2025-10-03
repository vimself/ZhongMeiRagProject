<template>
  <div class="dialog-overlay" @click.self="$emit('close')">
    <div class="dialog-container">
      <!-- 对话框标题 -->
      <div class="dialog-header">
        <h2 class="dialog-title">创建知识库</h2>
        <button class="btn-close" @click="$emit('close')">✕</button>
      </div>

      <!-- 步骤指示器 -->
      <div class="steps-indicator">
        <div 
          class="step-item" 
          v-for="(step, index) in steps" 
          :key="index"
          :class="{ active: currentStep === index + 1, completed: currentStep > index + 1 }"
        >
          <div class="step-circle">{{ index + 1 }}</div>
          <div class="step-text">{{ step }}</div>
        </div>
      </div>

      <!-- 对话框内容 -->
      <div class="dialog-body">
        <!-- 步骤 1: 基本信息 -->
        <div v-if="currentStep === 1" class="step-content">
          <div class="form-group">
            <label class="form-label required">知识库名称</label>
            <input 
              v-model="formData.name" 
              type="text" 
              class="form-input" 
              placeholder="请输入知识库名称"
            />
          </div>

          <div class="form-group">
            <label class="form-label">知识库描述</label>
            <textarea 
              v-model="formData.description" 
              class="form-textarea" 
              rows="3"
              placeholder="请输入知识库描述"
            ></textarea>
          </div>

          <div class="form-group">
            <label class="form-label">标签</label>
            <div class="tags-input-wrapper">
              <div class="tags-display">
                <span 
                  v-for="(tag, index) in formData.tags" 
                  :key="index" 
                  class="tag-chip"
                >
                  {{ tag }}
                  <span class="tag-close" @click="removeTag(index)">×</span>
                </span>
                <input 
                  v-model="newTag"
                  type="text" 
                  class="tag-input-field"
                  placeholder="输入标签并按Enter添加"
                  @keyup.enter="addTag"
                  @keydown.backspace="handleBackspace"
                  :disabled="formData.tags.length >= 5"
                />
              </div>
            </div>
            <div class="input-hint">{{ formData.tags.length }}/5 个标签</div>
          </div>
        </div>

        <!-- 步骤 2: 选择数据 -->
        <div v-if="currentStep === 2" class="step-content">
          <div class="form-group">
            <label class="form-label">数据来源</label>
            <div class="radio-group">
              <label class="radio-item">
                <input 
                  type="radio" 
                  v-model="formData.dataSource" 
                  value="upload"
                />
                <span>上传文件</span>
              </label>
              <label class="radio-item">
                <input 
                  type="radio" 
                  v-model="formData.dataSource" 
                  value="existing"
                />
                <span>选择已上传文件</span>
              </label>
            </div>
          </div>

          <!-- 上传文件 -->
          <div v-if="formData.dataSource === 'upload'" class="form-group">
            <label class="form-label">上传文件</label>
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
            <div v-if="selectedFiles.length > 0" class="file-list">
              <div 
                v-for="(file, index) in selectedFiles" 
                :key="index" 
                class="file-item"
              >
                <span class="file-name">{{ file.name }}</span>
                <span class="file-size">{{ formatFileSize(file.size) }}</span>
                <button class="file-remove" @click="removeFile(index)">删除</button>
              </div>
            </div>
          </div>

          <!-- 选择已有文件 -->
          <div v-if="formData.dataSource === 'existing'" class="form-group">
            <label class="form-label">选择文件</label>
            <div class="existing-files">
              <div 
                v-for="file in existingFiles" 
                :key="file.id" 
                class="existing-file-item"
                :class="{ selected: isFileSelected(file.id) }"
                @click="toggleFileSelection(file.id)"
              >
                <input type="checkbox" :checked="isFileSelected(file.id)" />
                <div class="file-info">
                  <div class="file-name">{{ file.name }}</div>
                  <div class="file-meta">
                    {{ file.size }} · 已用于: {{ file.usedBy.join(', ') }}
                  </div>
                </div>
              </div>
              <div v-if="existingFiles.length === 0" class="empty-files">
                暂无已上传文件
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤 3: 索引设置 -->
        <div v-if="currentStep === 3" class="step-content">
          <div class="form-group">
            <label class="form-label">切片方式</label>
            <div class="radio-group">
              <label class="radio-item">
                <input 
                  type="radio" 
                  v-model="formData.chunkMethod" 
                  value="smart"
                />
                <span>智能切片</span>
              </label>
              <label class="radio-item">
                <input 
                  type="radio" 
                  v-model="formData.chunkMethod" 
                  value="length"
                />
                <span>按长度切分</span>
              </label>
              <label class="radio-item">
                <input 
                  type="radio" 
                  v-model="formData.chunkMethod" 
                  value="page"
                />
                <span>按页切分</span>
              </label>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">最大分段长度</label>
            <input 
              v-model.number="formData.maxChunkLength" 
              type="number" 
              class="form-input" 
              placeholder="默认800"
            />
          </div>

          <div class="form-group">
            <label class="form-label">向量模型</label>
            <select v-model="formData.vectorModelId" class="form-select">
              <option value="">请选择向量模型</option>
              <option 
                v-for="model in vectorModels" 
                :key="model.id" 
                :value="model.id"
              >
                {{ model.name }} - {{ model.description }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">相似度阈值</label>
            <input 
              v-model.number="formData.similarityThreshold" 
              type="number" 
              step="0.1"
              min="0"
              max="1"
              class="form-input" 
              placeholder="0-1之间，默认0.7"
            />
          </div>

          <div class="form-group">
            <label class="form-label">最大召回数量</label>
            <input 
              v-model.number="formData.maxRecall" 
              type="number" 
              class="form-input" 
              placeholder="默认5"
            />
          </div>
        </div>
      </div>

      <!-- 对话框底部按钮 -->
      <div class="dialog-footer">
        <button 
          v-if="currentStep > 1" 
          class="btn-secondary" 
          @click="currentStep--"
        >
          上一步
        </button>
        <button 
          v-if="currentStep < 3" 
          class="btn-primary" 
          @click="nextStep"
          :disabled="!canProceed"
        >
          下一步
        </button>
        <button 
          v-if="currentStep === 3" 
          class="btn-primary" 
          @click="handleSubmit"
          :disabled="submitting || !canSubmit"
        >
          {{ submitting ? '创建中...' : '完成创建' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getUploadedFiles, getVectorModels, createKnowledgeBaseFull } from '@/api/knowledgeApi'

const emit = defineEmits(['close', 'created'])

// 步骤
const steps = ['基本信息', '选择数据', '索引设置']
const currentStep = ref(1)

// 表单数据
const formData = ref({
  name: '',
  description: '',
  tags: [],
  dataSource: 'upload',
  fileIds: [],
  chunkMethod: 'smart',
  maxChunkLength: 800,
  vectorModelId: '',
  similarityThreshold: 0.7,
  maxRecall: 5
})

// 其他状态
const newTag = ref('')
const selectedFiles = ref([])
const existingFiles = ref([])
const vectorModels = ref([])
const submitting = ref(false)
const fileInput = ref(null)

// 添加标签
const addTag = () => {
  const tag = newTag.value.trim()
  if (tag && !formData.value.tags.includes(tag) && formData.value.tags.length < 5) {
    formData.value.tags.push(tag)
    newTag.value = ''
  } else if (formData.value.tags.length >= 5) {
    alert('最多只能添加5个标签')
  }
}

// 移除标签
const removeTag = (index) => {
  formData.value.tags.splice(index, 1)
}

// 处理退格键删除标签
const handleBackspace = () => {
  if (newTag.value === '' && formData.value.tags.length > 0) {
    formData.value.tags.pop()
  }
}

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value?.click()
}

// 处理文件选择
const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  selectedFiles.value = [...selectedFiles.value, ...files]
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

// 切换文件选择
const toggleFileSelection = (fileId) => {
  const index = formData.value.fileIds.indexOf(fileId)
  if (index > -1) {
    formData.value.fileIds.splice(index, 1)
  } else {
    formData.value.fileIds.push(fileId)
  }
}

// 判断文件是否已选中
const isFileSelected = (fileId) => {
  return formData.value.fileIds.includes(fileId)
}

// 判断是否可以继续
const canProceed = computed(() => {
  if (currentStep.value === 1) {
    return formData.value.name.trim() !== ''
  }
  if (currentStep.value === 2) {
    if (formData.value.dataSource === 'upload') {
      return selectedFiles.value.length > 0
    } else {
      return formData.value.fileIds.length > 0
    }
  }
  return true
})

// 判断是否可以提交
const canSubmit = computed(() => {
  return formData.value.name.trim() !== '' && 
         formData.value.vectorModelId !== ''
})

// 下一步
const nextStep = () => {
  if (canProceed.value && currentStep.value < 3) {
    currentStep.value++
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!canSubmit.value || submitting.value) {
    return
  }

  try {
    submitting.value = true
    
    // 准备提交数据
    const submitData = {
      ...formData.value,
      files: formData.value.dataSource === 'upload' ? selectedFiles.value : undefined
    }

    const res = await createKnowledgeBaseFull(submitData)
    
    if (res.success) {
      alert('知识库创建成功！')
      emit('created')
    }
  } catch (error) {
    console.error('创建知识库失败:', error)
    alert(error.message || '创建失败')
  } finally {
    submitting.value = false
  }
}

// 获取已上传文件列表
const fetchExistingFiles = async () => {
  try {
    const res = await getUploadedFiles()
    if (res.success) {
      existingFiles.value = res.data.list
    }
  } catch (error) {
    console.error('获取已上传文件失败:', error)
  }
}

// 获取向量模型列表
const fetchVectorModels = async () => {
  try {
    const res = await getVectorModels()
    if (res.success) {
      vectorModels.value = res.data
      // 默认选择第一个模型
      if (vectorModels.value.length > 0 && !formData.value.vectorModelId) {
        formData.value.vectorModelId = vectorModels.value[0].id
      }
    }
  } catch (error) {
    console.error('获取向量模型失败:', error)
  }
}

// 初始化
onMounted(() => {
  fetchExistingFiles()
  fetchVectorModels()
})
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
  max-width: 800px;
  max-height: 90vh;
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

/* 步骤指示器 */
.steps-indicator {
  display: flex;
  justify-content: space-between;
  padding: 32px 64px;
  position: relative;
}

.steps-indicator::before {
  content: '';
  position: absolute;
  top: 50px;
  left: 120px;
  right: 120px;
  height: 2px;
  background: #e5e7eb;
  z-index: 0;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 1;
}

.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f5f7fa;
  color: #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  transition: all 0.3s;
}

.step-item.active .step-circle {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
}

.step-item.completed .step-circle {
  background: #10b981;
  color: #ffffff;
}

.step-text {
  font-size: 13px;
  color: #9ca3af;
  font-weight: 500;
}

.step-item.active .step-text {
  color: #667eea;
}

.step-item.completed .step-text {
  color: #10b981;
}

/* 对话框内容 */
.dialog-body {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

.step-content {
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 24px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #333333;
  margin-bottom: 8px;
}

.form-label.required::after {
  content: '*';
  color: #ef4444;
  margin-left: 4px;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  color: #333333;
  transition: all 0.2s;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.tags-input-wrapper {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 6px 12px;
  background: #ffffff;
  transition: all 0.2s;
  min-height: 42px;
}

.tags-input-wrapper:focus-within {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.tags-display {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.tag-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: #f3f4f6;
  color: #374151;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 400;
  line-height: 20px;
  transition: all 0.2s;
}

.tag-chip:hover {
  background: #e5e7eb;
}

.tag-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  margin-left: 2px;
  cursor: pointer;
  font-size: 16px;
  color: #6b7280;
  line-height: 1;
  transition: color 0.2s;
}

.tag-close:hover {
  color: #374151;
}

.tag-input-field {
  flex: 1;
  min-width: 150px;
  border: none;
  outline: none;
  padding: 4px 0;
  font-size: 14px;
  color: #1a1a1a;
  background: transparent;
}

.tag-input-field::placeholder {
  color: #9ca3af;
}

.tag-input-field:disabled {
  background: #f9fafb;
  cursor: not-allowed;
}

.input-hint {
  margin-top: 6px;
  font-size: 12px;
  color: #9ca3af;
  font-weight: 400;
}

.radio-group {
  display: flex;
  gap: 20px;
}

.radio-item {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #333333;
}

.radio-item input[type="radio"] {
  cursor: pointer;
}

/* 上传区域 */
.upload-area {
  border: 2px dashed #e5e7eb;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-area:hover {
  border-color: #667eea;
  background: #f9fafb;
}

.icon-upload {
  font-size: 48px;
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

.file-list {
  margin-top: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.file-item:last-child {
  border-bottom: none;
}

.file-name {
  flex: 1;
  font-size: 13px;
  color: #333333;
}

.file-size {
  font-size: 12px;
  color: #9ca3af;
  margin: 0 12px;
}

.file-remove {
  border: none;
  background: none;
  color: #ef4444;
  cursor: pointer;
  font-size: 12px;
}

/* 已有文件列表 */
.existing-files {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.existing-file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.2s;
}

.existing-file-item:last-child {
  border-bottom: none;
}

.existing-file-item:hover {
  background: #f9fafb;
}

.existing-file-item.selected {
  background: #eff6ff;
}

.file-info {
  flex: 1;
}

.file-info .file-name {
  font-size: 14px;
  color: #333333;
  margin-bottom: 4px;
}

.file-meta {
  font-size: 12px;
  color: #9ca3af;
}

.empty-files {
  padding: 40px;
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
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

.btn-secondary:hover {
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

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

