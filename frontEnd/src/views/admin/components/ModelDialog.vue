<template>
  <div v-if="visible" class="model-dialog-overlay" @click.self="handleClose">
    <div class="model-dialog">
      <!-- 对话框头部 -->
      <div class="dialog-header">
        <h2 class="dialog-title">{{ isEdit ? '编辑模型' : '添加模型' }}</h2>
        <button class="close-btn" @click="handleClose">
          <i class="icon-close"></i>
        </button>
      </div>

      <!-- 对话框内容 -->
      <div class="dialog-body">
        <form @submit.prevent="handleSubmit">
          <!-- 基本信息 -->
          <div class="form-section">
            <h3 class="section-title">基本信息</h3>

            <div class="form-group">
              <label class="form-label" for="modelName">
                模型名称 <span class="required">*</span>
              </label>
              <input
                id="modelName"
                v-model="formData.name"
                type="text"
                class="form-input"
                placeholder="例如: Qwen2-7B-Instruct"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label" for="modelType">
                模型类型 <span class="required">*</span>
              </label>
              <select
                id="modelType"
                v-model="formData.type"
                class="form-select"
                required
                :disabled="isEdit"
              >
                <option value="">请选择</option>
                <option value="llm">大语言模型 (LLM)</option>
                <option value="embedding">向量模型 (Embedding)</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="modelDescription">
                模型描述
              </label>
              <textarea
                id="modelDescription"
                v-model="formData.description"
                class="form-textarea"
                rows="3"
                placeholder="简要描述模型的特点和用途"
              ></textarea>
            </div>

            <div class="form-group">
              <label class="form-label" for="modelProvider">
                提供方 <span class="required">*</span>
              </label>
              <input
                id="modelProvider"
                v-model="formData.provider"
                type="text"
                class="form-input"
                placeholder="例如: 本地部署"
                required
              />
            </div>
          </div>

          <!-- 服务配置 -->
          <div class="form-section">
            <h3 class="section-title">服务配置</h3>

            <div class="form-group">
              <label class="form-label" for="modelEndpoint">
                服务地址 <span class="required">*</span>
              </label>
              <input
                id="modelEndpoint"
                v-model="formData.endpoint"
                type="url"
                class="form-input"
                placeholder="例如: http://localhost:8000/v1"
                required
              />
              <p class="form-hint">模型的API服务地址</p>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label" for="modelSize">
                  模型大小
                </label>
                <input
                  id="modelSize"
                  v-model="formData.modelSize"
                  type="text"
                  class="form-input"
                  placeholder="例如: 7B 参数"
                />
              </div>

              <div class="form-group">
                <label class="form-label" for="gpuMemory">
                  GPU显存
                </label>
                <input
                  id="gpuMemory"
                  v-model="formData.gpuMemory"
                  type="text"
                  class="form-input"
                  placeholder="例如: 14GB"
                />
              </div>
            </div>

            <div class="form-group" v-if="formData.type === 'llm'">
              <label class="form-label" for="contextLength">
                上下文长度
              </label>
              <input
                id="contextLength"
                v-model.number="formData.contextLength"
                type="number"
                class="form-input"
                placeholder="例如: 8192"
                min="0"
              />
              <p class="form-hint">模型支持的最大token数</p>
            </div>
          </div>

          <!-- LLM参数配置 -->
          <div v-if="formData.type === 'llm'" class="form-section">
            <h3 class="section-title">模型参数</h3>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label" for="temperature">
                  Temperature
                </label>
                <input
                  id="temperature"
                  v-model.number="formData.config.temperature"
                  type="number"
                  class="form-input"
                  step="0.1"
                  min="0"
                  max="2"
                  placeholder="0.7"
                />
                <p class="form-hint">控制输出随机性 (0-2)</p>
              </div>

              <div class="form-group">
                <label class="form-label" for="topP">
                  Top P
                </label>
                <input
                  id="topP"
                  v-model.number="formData.config.topP"
                  type="number"
                  class="form-input"
                  step="0.1"
                  min="0"
                  max="1"
                  placeholder="0.9"
                />
                <p class="form-hint">核采样参数 (0-1)</p>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label" for="topK">
                  Top K
                </label>
                <input
                  id="topK"
                  v-model.number="formData.config.topK"
                  type="number"
                  class="form-input"
                  min="0"
                  placeholder="50"
                />
                <p class="form-hint">采样候选数量</p>
              </div>

              <div class="form-group">
                <label class="form-label" for="maxTokens">
                  Max Tokens
                </label>
                <input
                  id="maxTokens"
                  v-model.number="formData.config.maxTokens"
                  type="number"
                  class="form-input"
                  min="0"
                  placeholder="2048"
                />
                <p class="form-hint">最大生成长度</p>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label" for="frequencyPenalty">
                  Frequency Penalty
                </label>
                <input
                  id="frequencyPenalty"
                  v-model.number="formData.config.frequencyPenalty"
                  type="number"
                  class="form-input"
                  step="0.1"
                  min="-2"
                  max="2"
                  placeholder="0.0"
                />
                <p class="form-hint">频率惩罚 (-2 to 2)</p>
              </div>

              <div class="form-group">
                <label class="form-label" for="presencePenalty">
                  Presence Penalty
                </label>
                <input
                  id="presencePenalty"
                  v-model.number="formData.config.presencePenalty"
                  type="number"
                  class="form-input"
                  step="0.1"
                  min="-2"
                  max="2"
                  placeholder="0.0"
                />
                <p class="form-hint">存在惩罚 (-2 to 2)</p>
              </div>
            </div>
          </div>

          <!-- Embedding参数配置 -->
          <div v-if="formData.type === 'embedding'" class="form-section">
            <h3 class="section-title">向量参数</h3>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label" for="dimension">
                  向量维度
                </label>
                <input
                  id="dimension"
                  v-model.number="formData.config.dimension"
                  type="number"
                  class="form-input"
                  placeholder="768"
                  min="0"
                />
                <p class="form-hint">输出向量的维度</p>
              </div>

              <div class="form-group">
                <label class="form-label">
                  归一化
                </label>
                <div class="checkbox-group">
                  <label class="checkbox-label">
                    <input
                      v-model="formData.config.normalize"
                      type="checkbox"
                      class="form-checkbox"
                    />
                    <span>启用向量归一化</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- 按钮组 -->
          <div class="dialog-footer">
            <button type="button" class="btn btn-cancel" @click="handleClose">
              取消
            </button>
            <button type="submit" class="btn btn-submit" :disabled="submitting">
              <i v-if="submitting" class="icon-loading"></i>
              {{ submitting ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { createModel, updateModel } from '@/api/modelApi'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  model: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'success'])

// 是否为编辑模式
const isEdit = computed(() => !!props.model)

// 表单数据
const formData = ref({
  name: '',
  type: '',
  description: '',
  provider: '本地部署',
  endpoint: '',
  modelSize: '',
  contextLength: null,
  gpuMemory: '',
  config: {
    temperature: 0.7,
    topP: 0.9,
    topK: 50,
    maxTokens: 2048,
    frequencyPenalty: 0.0,
    presencePenalty: 0.0,
    dimension: 768,
    normalize: true
  }
})

// 提交状态
const submitting = ref(false)

// 监听props变化,初始化表单
watch(
  () => props.model,
  (newModel) => {
    if (newModel) {
      formData.value = {
        id: newModel.id,
        name: newModel.name,
        type: newModel.type,
        description: newModel.description || '',
        provider: newModel.provider || '本地部署',
        endpoint: newModel.endpoint,
        modelSize: newModel.modelSize || '',
        contextLength: newModel.contextLength || null,
        gpuMemory: newModel.gpuMemory || '',
        config: { ...newModel.config }
      }
    } else {
      // 重置表单
      formData.value = {
        name: '',
        type: '',
        description: '',
        provider: '本地部署',
        endpoint: '',
        modelSize: '',
        contextLength: null,
        gpuMemory: '',
        config: {
          temperature: 0.7,
          topP: 0.9,
          topK: 50,
          maxTokens: 2048,
          frequencyPenalty: 0.0,
          presencePenalty: 0.0,
          dimension: 768,
          normalize: true
        }
      }
    }
  },
  { immediate: true }
)

// 关闭对话框
function handleClose() {
  emit('close')
}

// 提交表单
async function handleSubmit() {
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateModel(formData.value)
      alert('更新成功')
    } else {
      await createModel(formData.value)
      alert('创建成功')
    }
    emit('success')
  } catch (error) {
    console.error('保存模型失败:', error)
    alert('保存失败: ' + error.message)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.model-dialog-overlay {
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
  padding: 20px;
}

.model-dialog {
  background: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* 对话框头部 */
.dialog-header {
  padding: 24px 32px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.dialog-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
}

.icon-close::before {
  content: '✕';
  font-size: 18px;
  color: #6b7280;
}

/* 对话框内容 */
.dialog-body {
  padding: 32px;
  overflow-y: auto;
  flex: 1;
}

.form-section {
  margin-bottom: 32px;
}

.form-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 20px 0;
  padding-bottom: 12px;
  border-bottom: 1px solid #e5e7eb;
}

/* 表单元素 */
.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.required {
  color: #ef4444;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  color: #1a1a1a;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-input:disabled,
.form-select:disabled {
  background: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
}

.form-textarea {
  resize: vertical;
  font-family: inherit;
}

.form-hint {
  font-size: 12px;
  color: #9ca3af;
  margin: 6px 0 0 0;
}

.checkbox-group {
  padding-top: 8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #374151;
}

.form-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* 对话框底部 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
  margin-top: 24px;
}

.btn {
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-cancel {
  background: #f3f4f6;
  color: #6b7280;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.icon-loading {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .model-dialog {
    max-width: 100%;
  }

  .dialog-header,
  .dialog-body {
    padding: 20px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>

