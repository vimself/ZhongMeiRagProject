<template>
  <div class="model-management-page">
    <!-- 页面标题区 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">模型管理</h1>
        <p class="page-subtitle">管理AI模型和推理服务</p>
      </div>
      <div class="header-right">
        <span class="current-time">
          <i class="icon-time"></i>
          {{ currentTime }}
        </span>
      </div>
    </div>

    <!-- 统计卡片区 -->
    <div class="stats-section">
      <div class="stat-card stat-card-blue">
        <div class="stat-icon">
          <i class="icon-llm"></i>
        </div>
        <div class="stat-content">
          <div class="stat-label">LLM模型</div>
          <div class="stat-value">{{ stats.llmCount }}</div>
        </div>
      </div>

      <div class="stat-card stat-card-green">
        <div class="stat-icon">
          <i class="icon-embedding"></i>
        </div>
        <div class="stat-content">
          <div class="stat-label">向量模型</div>
          <div class="stat-value">{{ stats.embeddingCount }}</div>
        </div>
      </div>

      <div class="stat-card stat-card-yellow">
        <div class="stat-icon">
          <i class="icon-online"></i>
        </div>
        <div class="stat-content">
          <div class="stat-label">在线服务</div>
          <div class="stat-value">{{ stats.onlineCount }}</div>
        </div>
      </div>

      <div class="stat-card stat-card-red">
        <div class="stat-icon">
          <i class="icon-offline"></i>
        </div>
        <div class="stat-content">
          <div class="stat-label">离线服务</div>
          <div class="stat-value">{{ stats.offlineCount }}</div>
        </div>
      </div>
    </div>

    <!-- 模型列表标题和操作按钮区 -->
    <div class="action-bar">
      <div class="action-bar-left">
        <h2 class="list-title">模型列表</h2>
      </div>
      <div class="action-bar-right">
        <button class="btn btn-add" @click="handleAddModel">
          <i class="icon-plus"></i>
          添加模型
        </button>
        <button class="btn btn-health" @click="handleHealthCheck" :disabled="healthCheckLoading">
          <i class="icon-health" :class="{ 'rotating': healthCheckLoading }"></i>
          {{ healthCheckLoading ? '检查中...' : '健康检查' }}
        </button>
      </div>
    </div>

    <!-- 模型列表 - LLM模型 -->
    <div class="model-section">
      <div class="section-header">
        <h2 class="section-title">大语言模型 (LLM)</h2>
      </div>
      <div class="model-list">
        <div
          v-for="model in llmModels"
          :key="model.id"
          class="model-card"
          :class="{ 'model-card-offline': model.status === 'offline' }"
        >
          <!-- 模型状态指示器 -->
          <div class="model-status" :class="`status-${model.status}`">
            <span class="status-dot"></span>
            <span class="status-text">{{ getStatusText(model.status) }}</span>
          </div>

          <!-- 默认标记 -->
          <div v-if="model.isDefault" class="model-default-badge">
            <i class="icon-star"></i>
            默认
          </div>

          <!-- 模型信息 -->
          <div class="model-info">
            <div class="model-header">
              <div class="model-icon">
                <i class="icon-model-llm"></i>
              </div>
              <div class="model-title-area">
                <h3 class="model-name">{{ model.name }}</h3>
                <p class="model-description">{{ model.description }}</p>
              </div>
            </div>

            <!-- 模型参数 -->
            <div class="model-params">
              <div class="param-item">
                <span class="param-label">模型大小</span>
                <span class="param-value">{{ model.modelSize }}</span>
              </div>
              <div class="param-item">
                <span class="param-label">上下文长度</span>
                <span class="param-value">{{ formatNumber(model.contextLength) }} tokens</span>
              </div>
              <div class="param-item">
                <span class="param-label">推理延迟</span>
                <span class="param-value">{{ model.latency }}</span>
              </div>
              <div class="param-item">
                <span class="param-label">GPU显存</span>
                <span class="param-value">{{ model.gpuMemory }}</span>
              </div>
            </div>

            <!-- 服务地址 -->
            <div class="model-endpoint">
              <span class="endpoint-label">服务地址</span>
              <span class="endpoint-value">{{ model.endpoint }}</span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="model-actions">
            <button
              class="action-btn action-btn-test"
              @click="handleTestModel(model)"
              :disabled="testingModelId === model.id"
            >
              <i class="icon-test"></i>
              {{ testingModelId === model.id ? '测试中...' : '测试' }}
            </button>
            <button class="action-btn action-btn-config" @click="handleConfigModel(model)">
              <i class="icon-config"></i>
              配置
            </button>
            <button
              v-if="!model.isDefault"
              class="action-btn action-btn-default"
              @click="handleSetDefault(model)"
            >
              <i class="icon-star"></i>
              设为默认
            </button>
            <button class="action-btn action-btn-delete" @click="handleDeleteModel(model)">
              <i class="icon-delete"></i>
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 模型列表 - 向量模型 -->
    <div class="model-section">
      <div class="section-header">
        <h2 class="section-title">向量模型 (Embedding)</h2>
      </div>
      <div class="model-list">
        <div
          v-for="model in embeddingModels"
          :key="model.id"
          class="model-card"
          :class="{ 'model-card-offline': model.status === 'offline' }"
        >
          <!-- 模型状态指示器 -->
          <div class="model-status" :class="`status-${model.status}`">
            <span class="status-dot"></span>
            <span class="status-text">{{ getStatusText(model.status) }}</span>
          </div>

          <!-- 默认标记 -->
          <div v-if="model.isDefault" class="model-default-badge">
            <i class="icon-star"></i>
            默认
          </div>

          <!-- 模型信息 -->
          <div class="model-info">
            <div class="model-header">
              <div class="model-icon model-icon-embedding">
                <i class="icon-model-embedding"></i>
              </div>
              <div class="model-title-area">
                <h3 class="model-name">{{ model.name }}</h3>
                <p class="model-description">{{ model.description }}</p>
              </div>
            </div>

            <!-- 模型参数 -->
            <div class="model-params">
              <div class="param-item">
                <span class="param-label">模型大小</span>
                <span class="param-value">{{ model.modelSize }}</span>
              </div>
              <div class="param-item">
                <span class="param-label">向量维度</span>
                <span class="param-value">{{ model.config.dimension }}</span>
              </div>
              <div class="param-item">
                <span class="param-label">推理延迟</span>
                <span class="param-value">{{ model.latency }}</span>
              </div>
              <div class="param-item">
                <span class="param-label">GPU显存</span>
                <span class="param-value">{{ model.gpuMemory }}</span>
              </div>
            </div>

            <!-- 服务地址 -->
            <div class="model-endpoint">
              <span class="endpoint-label">服务地址</span>
              <span class="endpoint-value">{{ model.endpoint }}</span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="model-actions">
            <button
              class="action-btn action-btn-test"
              @click="handleTestModel(model)"
              :disabled="testingModelId === model.id"
            >
              <i class="icon-test"></i>
              {{ testingModelId === model.id ? '测试中...' : '测试' }}
            </button>
            <button class="action-btn action-btn-config" @click="handleConfigModel(model)">
              <i class="icon-config"></i>
              配置
            </button>
            <button
              v-if="!model.isDefault"
              class="action-btn action-btn-default"
              @click="handleSetDefault(model)"
            >
              <i class="icon-star"></i>
              设为默认
            </button>
            <button class="action-btn action-btn-delete" @click="handleDeleteModel(model)">
              <i class="icon-delete"></i>
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加/编辑模型对话框 -->
    <ModelDialog
      v-if="showModelDialog"
      :visible="showModelDialog"
      :model="currentModel"
      @close="showModelDialog = false"
      @success="handleModelSaved"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getModelStats, getModelList, testModel, setDefaultModel, deleteModel, healthCheckModels } from '@/api/modelApi'
import ModelDialog from './components/ModelDialog.vue'

// 响应式数据
const currentTime = ref('')
const stats = ref({
  llmCount: 0,
  embeddingCount: 0,
  onlineCount: 0,
  offlineCount: 0
})
const modelList = ref([])
const testingModelId = ref(null)
const healthCheckLoading = ref(false)
const showModelDialog = ref(false)
const currentModel = ref(null)

// 计算属性
const llmModels = computed(() => {
  return modelList.value.filter(m => m.type === 'llm')
})

const embeddingModels = computed(() => {
  return modelList.value.filter(m => m.type === 'embedding')
})

// 更新时间
function updateTime() {
  const now = new Date()
  const month = now.getMonth() + 1
  const day = now.getDate()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  currentTime.value = `${month}/${day} ${hours}:${minutes}`
}

// 格式化数字
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// 获取状态文本
function getStatusText(status) {
  const statusMap = {
    online: '在线',
    offline: '离线',
    error: '错误'
  }
  return statusMap[status] || '未知'
}

// 加载统计数据
async function loadStats() {
  try {
    const res = await getModelStats()
    stats.value = res.data
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 加载模型列表
async function loadModelList() {
  try {
    const res = await getModelList({ type: 'all', status: 'all' })
    modelList.value = res.data.list
  } catch (error) {
    console.error('加载模型列表失败:', error)
  }
}

// 添加模型
function handleAddModel() {
  currentModel.value = null
  showModelDialog.value = true
}

// 测试模型
async function handleTestModel(model) {
  testingModelId.value = model.id
  try {
    const res = await testModel({ id: model.id })
    alert(`测试结果:\n状态: ${res.data.status}\n响应时间: ${res.data.responseTime}ms\n消息: ${res.data.message}`)
    // 刷新列表
    await loadModelList()
  } catch (error) {
    console.error('测试模型失败:', error)
    alert('测试失败: ' + error.message)
  } finally {
    testingModelId.value = null
  }
}

// 配置模型
function handleConfigModel(model) {
  currentModel.value = model
  showModelDialog.value = true
}

// 设为默认
async function handleSetDefault(model) {
  try {
    await setDefaultModel({ id: model.id, type: model.type })
    alert('设置成功')
    // 刷新列表
    await loadModelList()
    await loadStats()
  } catch (error) {
    console.error('设置默认模型失败:', error)
    alert('设置失败: ' + error.message)
  }
}

// 删除模型
async function handleDeleteModel(model) {
  if (!confirm(`确定要删除模型 "${model.name}" 吗？`)) {
    return
  }

  try {
    await deleteModel({ id: model.id })
    alert('删除成功')
    // 刷新列表
    await loadModelList()
    await loadStats()
  } catch (error) {
    console.error('删除模型失败:', error)
    alert('删除失败: ' + error.message)
  }
}

// 健康检查
async function handleHealthCheck() {
  healthCheckLoading.value = true
  try {
    const res = await healthCheckModels()
    alert(`健康检查完成:\n总数: ${res.data.total}\n成功: ${res.data.success}\n失败: ${res.data.failed}`)
    // 刷新列表
    await loadModelList()
    await loadStats()
  } catch (error) {
    console.error('健康检查失败:', error)
    alert('健康检查失败: ' + error.message)
  } finally {
    healthCheckLoading.value = false
  }
}

// 模型保存成功回调
async function handleModelSaved() {
  showModelDialog.value = false
  await loadModelList()
  await loadStats()
}

// 生命周期
let timer = null
onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 30000) // 每30秒更新一次时间
  loadStats()
  loadModelList()
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.model-management-page {
  padding: 32px 48px;
  max-width: 1800px;
  margin: 0 auto;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 页面标题区 */
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
  align-items: center;
}

.current-time {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #6b7280;
}

.icon-time::before {
  content: '🕐';
  font-size: 16px;
}

/* 统计卡片区 */
.stats-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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

.stat-card-red .stat-icon {
  background: #fee2e2;
}

.icon-llm::before {
  content: '🔥';
}

.icon-embedding::before {
  content: '📊';
}

.icon-online::before {
  content: '✅';
}

.icon-offline::before {
  content: '🚫';
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
}

/* 操作按钮区 */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding: 20px 0;
  border-bottom: 1px solid #e5e7eb;
}

.action-bar-left .list-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.action-bar-right {
  display: flex;
  gap: 16px;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-add {
  background: #3b82f6;
  color: #ffffff;
}

.btn-add:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-health {
  background: #10b981;
  color: #ffffff;
}

.btn-health:hover {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.icon-plus::before {
  content: '+';
  font-size: 18px;
}

.icon-health::before {
  content: '🔄';
}

.icon-health.rotating {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 模型列表区 */
.model-section {
  margin-bottom: 32px;
}

.section-header {
  margin-bottom: 20px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.model-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

/* 模型卡片 */
.model-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: relative;
  transition: all 0.2s;
}

.model-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.model-card-offline {
  opacity: 0.7;
}

/* 模型状态 */
.model-status {
  position: absolute;
  top: 24px;
  right: 24px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-online {
  background: #d1fae5;
  color: #10b981;
}

.status-offline {
  background: #fee2e2;
  color: #ef4444;
}

.status-error {
  background: #fee2e2;
  color: #ef4444;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

/* 默认标记 */
.model-default-badge {
  position: absolute;
  top: 24px;
  right: 110px;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border-radius: 20px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: #ffffff;
  font-size: 12px;
  font-weight: 500;
}

.icon-star::before {
  content: '⭐';
  font-size: 12px;
}

/* 模型信息 */
.model-info {
  margin-bottom: 24px;
}

.model-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.model-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.model-icon-embedding {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.icon-model-llm::before,
.icon-model-embedding::before {
  content: '🤖';
  font-size: 24px;
}

.model-title-area {
  flex: 1;
  min-width: 0;
}

.model-name {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 6px 0;
  padding-right: 140px;
}

.model-description {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

/* 模型参数 */
.model-params {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.param-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.param-label {
  font-size: 12px;
  color: #9ca3af;
}

.param-value {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
}

/* 服务地址 */
.model-endpoint {
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.endpoint-label {
  font-size: 12px;
  color: #9ca3af;
}

.endpoint-value {
  font-size: 13px;
  font-family: 'Courier New', monospace;
  color: #667eea;
  word-break: break-all;
}

/* 操作按钮 */
.model-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.action-btn {
  padding: 8px 16px;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
  color: #6b7280;
}

.action-btn:hover {
  border-color: #667eea;
  color: #667eea;
  background: #f5f5ff;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.action-btn-test .icon-test::before {
  content: '🔬';
}

.action-btn-config .icon-config::before {
  content: '⚙️';
}

.action-btn-default:hover {
  border-color: #fbbf24;
  color: #fbbf24;
  background: #fffbeb;
}

.action-btn-delete:hover {
  border-color: #ef4444;
  color: #ef4444;
  background: #fef2f2;
}

.icon-delete::before {
  content: '🗑️';
}

/* 响应式 */
@media (max-width: 1400px) {
  .model-list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }

  .model-params {
    grid-template-columns: 1fr;
  }
}
</style>
