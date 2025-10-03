<template>
  <div class="dialog-overlay" @click.self="handleClose">
    <div class="dialog-container">
      <div class="dialog-header">
        <h2 class="dialog-title">编辑知识库</h2>
        <button class="btn-close" @click="handleClose">
          <span class="icon-close">✕</span>
        </button>
      </div>

      <div class="dialog-body">
        <!-- 知识库名称 -->
        <div class="form-group">
          <label class="form-label">
            知识库名称
            <span class="required">*</span>
          </label>
          <input 
            type="text" 
            v-model="formData.name"
            class="form-input"
            placeholder="请输入知识库名称"
            maxlength="50"
          />
          <div class="input-hint">{{ formData.name.length }}/50</div>
        </div>

        <!-- 知识库描述 -->
        <div class="form-group">
          <label class="form-label">
            知识库描述
            <span class="required">*</span>
          </label>
          <textarea 
            v-model="formData.description"
            class="form-textarea"
            placeholder="请简要描述知识库的内容和用途"
            rows="4"
            maxlength="200"
          ></textarea>
          <div class="input-hint">{{ formData.description.length }}/200</div>
        </div>

        <!-- 标签 -->
        <div class="form-group">
          <label class="form-label">标签</label>
          <div class="tags-input-wrapper">
            <div class="tags-display-area">
              <span 
                class="tag-chip" 
                v-for="(tag, index) in formData.tags" 
                :key="index"
              >
                {{ tag }}
                <span class="tag-close" @click="removeTag(index)">×</span>
              </span>
              <input 
                type="text" 
                v-model="tagInput"
                class="tag-input-field"
                placeholder="输入标签并按Enter添加"
                @keydown.enter.prevent="addTag"
                @keydown.backspace="handleBackspace"
              />
            </div>
          </div>
          <div class="input-hint">最多添加5个标签，按Enter键添加</div>
        </div>

        <!-- 相似度阈值 -->
        <div class="form-group">
          <label class="form-label">
            相似度阈值
            <span class="tooltip-icon" title="设置文档检索时的最低相似度要求，范围0-1，值越大要求越严格">?</span>
          </label>
          <div class="threshold-container">
            <input 
              type="range" 
              v-model.number="formData.similarityThreshold"
              class="threshold-slider"
              min="0"
              max="1"
              step="0.01"
            />
            <div class="threshold-value">{{ formData.similarityThreshold.toFixed(2) }}</div>
          </div>
          <div class="threshold-labels">
            <span>宽松 (0.0)</span>
            <span>适中 (0.5)</span>
            <span>严格 (1.0)</span>
          </div>
        </div>
      </div>

      <div class="dialog-footer">
        <button class="btn-cancel" @click="handleClose">取消</button>
        <button class="btn-submit" @click="handleSubmit" :disabled="!isFormValid || submitting">
          {{ submitting ? '保存中...' : '保存' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { updateKnowledgeBase } from '@/api/knowledgeApi'

// Props
const props = defineProps({
  knowledgeBase: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits(['close', 'updated'])

// 表单数据
const formData = ref({
  name: '',
  description: '',
  tags: [],
  similarityThreshold: 0.7
})

// 标签输入
const tagInput = ref('')

// 提交状态
const submitting = ref(false)

// 表单验证
const isFormValid = computed(() => {
  return formData.value.name.trim() !== '' && 
         formData.value.description.trim() !== ''
})

// 初始化表单数据
onMounted(() => {
  formData.value = {
    name: props.knowledgeBase.name || '',
    description: props.knowledgeBase.description || '',
    tags: props.knowledgeBase.tags || [],
    similarityThreshold: props.knowledgeBase.similarityThreshold || 0.7
  }
})

// 添加标签
const addTag = () => {
  const tag = tagInput.value.trim()
  if (tag && !formData.value.tags.includes(tag) && formData.value.tags.length < 5) {
    formData.value.tags.push(tag)
    tagInput.value = ''
  }
}

// 移除标签
const removeTag = (index) => {
  formData.value.tags.splice(index, 1)
}

// 处理退格键删除标签
const handleBackspace = () => {
  if (tagInput.value === '' && formData.value.tags.length > 0) {
    formData.value.tags.pop()
  }
}

// 关闭对话框
const handleClose = () => {
  emit('close')
}

// 提交表单
const handleSubmit = async () => {
  if (!isFormValid.value || submitting.value) {
    return
  }

  try {
    submitting.value = true
    const res = await updateKnowledgeBase({
      id: props.knowledgeBase.id,
      name: formData.value.name,
      description: formData.value.description,
      tags: formData.value.tags,
      similarityThreshold: formData.value.similarityThreshold
    })

    if (res.success) {
      alert('更新成功')
      emit('updated')
    }
  } catch (error) {
    console.error('更新知识库失败:', error)
    alert(error.message || '更新失败')
  } finally {
    submitting.value = false
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
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #e5e7eb;
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
  transition: all 0.2s;
}

.btn-close:hover {
  background: #e5e7eb;
}

.icon-close {
  font-size: 20px;
  color: #666666;
}

.dialog-body {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #333333;
  margin-bottom: 8px;
}

.required {
  color: #ef4444;
  margin-left: 4px;
}

.tooltip-icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  line-height: 16px;
  text-align: center;
  background: #e5e7eb;
  color: #666666;
  border-radius: 50%;
  font-size: 12px;
  margin-left: 4px;
  cursor: help;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  color: #1a1a1a;
  transition: all 0.2s;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  color: #1a1a1a;
  resize: vertical;
  font-family: inherit;
  transition: all 0.2s;
  box-sizing: border-box;
}

.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input-hint {
  margin-top: 6px;
  font-size: 12px;
  color: #999999;
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

.tags-display-area {
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

.threshold-container {
  display: flex;
  align-items: center;
  gap: 16px;
}

.threshold-slider {
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: #e5e7eb;
  outline: none;
  -webkit-appearance: none;
}

.threshold-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
}

.threshold-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
}

.threshold-value {
  min-width: 50px;
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #667eea;
  text-align: center;
}

.threshold-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 12px;
  color: #999999;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 24px 32px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.btn-cancel {
  padding: 10px 24px;
  background: #ffffff;
  color: #666666;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #f5f7fa;
  border-color: #d1d5db;
}

.btn-submit {
  padding: 10px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

