<template>
  <div class="chat-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">智能问答</h1>
        <p class="page-subtitle">AI驱动的智能技术问答</p>
      </div>
      <div class="header-right">
        <div class="current-time">
          <i class="icon-time"></i>
          <span>{{ currentTime }}</span>
        </div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="chat-container">
      <!-- 左侧面板 -->
      <aside class="chat-sidebar">
        <!-- 选择知识库 -->
        <div class="selection-group">
          <label class="selection-label">选择知识库</label>
          <select v-model="selectedKnowledgeBase" class="selection-input">
            <option value="all">全部知识库</option>
            <option 
              v-for="kb in knowledgeBaseList" 
              :key="kb.id" 
              :value="kb.id"
            >
              {{ kb.name }}
            </option>
          </select>
        </div>

        <!-- 选择模型 -->
        <div class="selection-group">
          <label class="selection-label">选择模型</label>
          <select v-model="selectedModel" class="selection-input">
            <option 
              v-for="model in modelList" 
              :key="model.id" 
              :value="model.id"
            >
              {{ model.name }}
            </option>
          </select>
        </div>

        <!-- 会话历史 -->
        <div class="history-section">
          <label class="section-label">会话历史</label>
          <div class="history-list">
            <div 
              v-for="session in sessionHistory" 
              :key="session.id"
              class="history-item"
              :class="{ 'active': currentSessionId === session.id }"
              @click="loadSession(session.id)"
            >
              <div class="history-title">{{ session.title }}</div>
              <div class="history-time">{{ session.time }}</div>
            </div>
          </div>
        </div>

        <!-- 新建对话按钮 -->
        <button class="new-chat-btn" @click="createNewChat">
          <i class="icon-plus"></i>
          <span>新建对话</span>
        </button>
      </aside>

      <!-- 右侧对话区 -->
      <main class="chat-main">
        <!-- 对话区头部 -->
        <div class="chat-header">
          <div class="chat-header-left">
            <h2 class="chat-title">当前会话</h2>
            <div class="chat-meta">
              <i class="icon-kb"></i>
              <span>{{ getKnowledgeBaseName() }}</span>
              <span class="separator">·</span>
              <i class="icon-model"></i>
              <span>{{ getModelName() }}</span>
            </div>
          </div>
          <div class="chat-header-right">
            <button class="icon-btn" @click="toggleSidebar" title="收起侧边栏">
              <i class="icon-sidebar"></i>
            </button>
            <button class="icon-btn" @click="shareChat" title="分享对话">
              <i class="icon-share"></i>
            </button>
          </div>
        </div>

        <!-- 对话内容区 -->
        <div class="chat-content" ref="chatContentRef">
          <!-- 空状态 -->
          <div v-if="messages.length === 0" class="empty-state">
            <div class="assistant-avatar">
              <i class="icon-robot"></i>
            </div>
            <h3 class="assistant-title">RAG智能助手</h3>
            <p class="assistant-desc">我可以帮您快速搜索技术文档，回答技术问题</p>

            <!-- 推荐问题 -->
            <div class="suggestions-section">
              <h4 class="suggestions-title">推荐问题:</h4>
              <div class="suggestions-grid">
                <div 
                  v-for="(suggestion, index) in suggestions" 
                  :key="index"
                  class="suggestion-card"
                  @click="askQuestion(suggestion.question)"
                >
                  <i :class="suggestion.icon"></i>
                  <span>{{ suggestion.question }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 消息列表 -->
          <div v-else class="messages-list">
            <div 
              v-for="message in messages" 
              :key="message.id"
              class="message-item"
              :class="message.role"
            >
              <div class="message-avatar">
                <i :class="message.role === 'user' ? 'icon-user-msg' : 'icon-assistant-msg'"></i>
              </div>
              <div class="message-content">
                <div class="message-text">{{ message.content }}</div>
                <div v-if="message.references && message.references.length > 0" class="message-references">
                  <div class="references-title">引用来源:</div>
                  <div class="references-list">
                    <div 
                      v-for="(ref, idx) in message.references" 
                      :key="idx"
                      class="reference-item"
                    >
                      <i class="icon-document-ref"></i>
                      <span class="ref-title">{{ ref.title }}</span>
                      <span class="ref-page">第{{ ref.page }}页</span>
                    </div>
                  </div>
                </div>
                <div class="message-time">{{ message.time }}</div>
              </div>
            </div>

            <!-- 加载中 -->
            <div v-if="isLoading" class="message-item assistant">
              <div class="message-avatar">
                <i class="icon-assistant-msg"></i>
              </div>
              <div class="message-content">
                <div class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="chat-input-area">
          <div class="input-container">
            <textarea
              v-model="inputMessage"
              class="chat-textarea"
              placeholder="请输入您的问题..."
              :maxlength="1000"
              @keydown.enter="handleEnterKey"
              rows="1"
            ></textarea>
            <button 
              class="send-btn"
              :disabled="!inputMessage.trim() || isLoading"
              @click="sendMessage"
            >
              <i class="icon-send"></i>
              <span>发送</span>
            </button>
          </div>
          <div class="input-footer">
            <div class="input-tips">
              <i class="icon-keyboard"></i>
              <span>Shift+Enter 换行</span>
              <i class="icon-command"></i>
              <span>Enter 发送</span>
            </div>
            <div class="char-count">{{ inputMessage.length }} / 1000</div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { 
  getKnowledgeBaseList, 
  getModelList, 
  getSessionHistory,
  createSession,
  sendChatMessage
} from '../api/chatApi'

// 当前时间
const currentTime = ref('')

// 选择的知识库和模型
const selectedKnowledgeBase = ref('all')
const selectedModel = ref('qwen2-7b')

// 知识库列表
const knowledgeBaseList = ref([])

// 模型列表
const modelList = ref([])

// 会话历史
const sessionHistory = ref([])

// 当前会话ID
const currentSessionId = ref(null)

// 消息列表
const messages = ref([])

// 输入内容
const inputMessage = ref('')

// 加载状态
const isLoading = ref(false)

// 聊天内容容器引用
const chatContentRef = ref(null)

// 推荐问题
const suggestions = ref([
  {
    icon: 'icon-code-suggest',
    question: '如何设计RESTful API?'
  },
  {
    icon: 'icon-database-suggest',
    question: '数据库连接池最佳实践?'
  },
  {
    icon: 'icon-redis-suggest',
    question: 'Redis缓存如何优化?'
  },
  {
    icon: 'icon-microservice-suggest',
    question: '微服务架构注意事项?'
  }
])

// 定时器ID
let timeInterval = null

onMounted(async () => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  
  await loadInitialData()
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
 * 加载初始数据
 */
async function loadInitialData() {
  try {
    const [kbRes, modelRes, historyRes] = await Promise.all([
      getKnowledgeBaseList(),
      getModelList(),
      getSessionHistory()
    ])
    
    knowledgeBaseList.value = kbRes.data
    modelList.value = modelRes.data
    sessionHistory.value = historyRes.data
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

/**
 * 获取知识库名称
 */
function getKnowledgeBaseName() {
  if (selectedKnowledgeBase.value === 'all') {
    return '全部知识库'
  }
  const kb = knowledgeBaseList.value.find(k => k.id === selectedKnowledgeBase.value)
  return kb ? kb.name : '未知'
}

/**
 * 获取模型名称
 */
function getModelName() {
  const model = modelList.value.find(m => m.id === selectedModel.value)
  return model ? model.name : '未知'
}

/**
 * 新建对话
 */
async function createNewChat() {
  try {
    const res = await createSession({
      knowledgeBaseId: selectedKnowledgeBase.value,
      modelId: selectedModel.value
    })
    
    currentSessionId.value = res.data.id
    messages.value = []
    
    // 刷新会话历史
    const historyRes = await getSessionHistory()
    sessionHistory.value = historyRes.data
  } catch (error) {
    console.error('创建会话失败:', error)
    alert(error.message || '创建会话失败')
  }
}

/**
 * 加载会话
 */
function loadSession(sessionId) {
  currentSessionId.value = sessionId
  // TODO: 加载会话消息
  messages.value = []
}

/**
 * 提问（点击推荐问题）
 */
function askQuestion(question) {
  inputMessage.value = question
  sendMessage()
}

/**
 * 发送消息
 */
async function sendMessage() {
  if (!inputMessage.value.trim() || isLoading.value) {
    return
  }

  // 如果没有会话，先创建
  if (!currentSessionId.value) {
    await createNewChat()
  }

  const userMessage = {
    id: Date.now(),
    role: 'user',
    content: inputMessage.value,
    time: formatTime(new Date())
  }

  messages.value.push(userMessage)
  
  const question = inputMessage.value
  inputMessage.value = ''
  isLoading.value = true

  // 滚动到底部
  await nextTick()
  scrollToBottom()

  try {
    const res = await sendChatMessage({
      sessionId: currentSessionId.value,
      question: question,
      knowledgeBaseId: selectedKnowledgeBase.value,
      modelId: selectedModel.value
    })

    const assistantMessage = {
      id: Date.now() + 1,
      role: 'assistant',
      content: res.data.answer,
      references: res.data.references,
      time: formatTime(new Date())
    }

    messages.value.push(assistantMessage)

    // 滚动到底部
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('发送消息失败:', error)
    alert(error.message || '发送失败，请重试')
  } finally {
    isLoading.value = false
  }
}

/**
 * 处理Enter键
 */
function handleEnterKey(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

/**
 * 滚动到底部
 */
function scrollToBottom() {
  if (chatContentRef.value) {
    chatContentRef.value.scrollTop = chatContentRef.value.scrollHeight
  }
}

/**
 * 格式化时间
 */
function formatTime(date) {
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${hours}:${minutes}`
}

/**
 * 切换侧边栏
 */
function toggleSidebar() {
  // TODO: 实现侧边栏折叠
  console.log('切换侧边栏')
}

/**
 * 分享对话
 */
function shareChat() {
  // TODO: 实现分享功能
  console.log('分享对话')
}
</script>

<style scoped>
.chat-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 88px;
  padding: 0 32px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 4px 0;
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
  background: #f9fafb;
  border-radius: 8px;
}

.icon-time::before {
  content: '🕐';
  font-size: 16px;
}

/* 聊天容器 */
.chat-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 左侧面板 */
.chat-sidebar {
  width: 320px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  padding: 28px 20px;
}

.selection-group {
  margin-bottom: 20px;
}

.selection-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.selection-input {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  font-size: 14px;
  color: #1f2937;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  outline: none;
  cursor: pointer;
  transition: all 0.3s;
}

.selection-input:hover {
  border-color: #667eea;
}

.selection-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 会话历史 */
.history-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  overflow: hidden;
}

.section-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 12px;
}

.history-list {
  flex: 1;
  overflow-y: auto;
}

.history-item {
  padding: 12px;
  margin-bottom: 8px;
  background: #f9fafb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.history-item:hover {
  background: #f3f4f6;
}

.history-item.active {
  background: #ede9fe;
  border: 1px solid #667eea;
}

.history-title {
  font-size: 14px;
  color: #1f2937;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-time {
  font-size: 12px;
  color: #6b7280;
}

/* 新建对话按钮 */
.new-chat-btn {
  width: 100%;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: #667eea;
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.new-chat-btn:hover {
  background: #5568d3;
}

.icon-plus::before {
  content: '+';
  font-size: 18px;
  font-weight: 600;
}

/* 右侧对话区 */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #ffffff;
}

/* 对话区头部 */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.chat-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 4px 0;
}

.chat-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #6b7280;
}

.chat-meta i {
  font-size: 14px;
}

.separator {
  margin: 0 4px;
}

.icon-kb::before {
  content: '📚';
}

.icon-model::before {
  content: '🤖';
}

.chat-header-right {
  display: flex;
  gap: 8px;
}

.icon-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.icon-btn:hover {
  background: #f9fafb;
  border-color: #667eea;
}

.icon-sidebar::before {
  content: '📌';
  font-size: 16px;
}

.icon-share::before {
  content: '📤';
  font-size: 16px;
}

/* 对话内容区 */
.chat-content {
  flex: 1;
  overflow-y: auto;
  padding: 28px 24px;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.assistant-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.icon-robot::before {
  content: '🤖';
  font-size: 40px;
}

.assistant-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.assistant-desc {
  font-size: 15px;
  color: #6b7280;
  margin: 0 0 40px 0;
}

/* 推荐问题 */
.suggestions-section {
  width: 100%;
  max-width: 800px;
}

.suggestions-title {
  font-size: 16px;
  font-weight: 500;
  color: #374151;
  margin: 0 0 16px 0;
}

.suggestions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.suggestion-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.suggestion-card:hover {
  background: #ffffff;
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
}

.suggestion-card i {
  font-size: 20px;
}

.icon-code-suggest::before {
  content: '⚡';
}

.icon-database-suggest::before {
  content: '🗄️';
}

.icon-redis-suggest::before {
  content: '🔴';
}

.icon-microservice-suggest::before {
  content: '🎯';
}

.suggestion-card span {
  font-size: 14px;
  color: #374151;
}

/* 消息列表 */
.messages-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.message-item {
  display: flex;
  gap: 12px;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-item.user .message-avatar {
  background: #dbeafe;
}

.message-item.assistant .message-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.icon-user-msg::before {
  content: '👤';
  font-size: 18px;
}

.icon-assistant-msg::before {
  content: '🤖';
  font-size: 18px;
}

.message-content {
  flex: 1;
  max-width: 100%;
}

.message-text {
  font-size: 15px;
  line-height: 1.6;
  color: #1f2937;
  white-space: pre-wrap;
  word-break: break-word;
}

/* 引用来源 */
.message-references {
  margin-top: 16px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  border-left: 3px solid #667eea;
}

.references-title {
  font-size: 13px;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 8px;
}

.references-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.reference-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #374151;
}

.icon-document-ref::before {
  content: '📄';
  font-size: 14px;
}

.ref-title {
  color: #667eea;
  cursor: pointer;
}

.ref-title:hover {
  text-decoration: underline;
}

.ref-page {
  color: #6b7280;
}

.message-time {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 8px;
}

/* 打字指示器 */
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #9ca3af;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    opacity: 0.3;
    transform: translateY(0);
  }
  30% {
    opacity: 1;
    transform: translateY(-8px);
  }
}

/* 输入区域 */
.chat-input-area {
  padding: 20px 24px;
  border-top: 1px solid #e5e7eb;
  background: #ffffff;
}

.input-container {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.chat-textarea {
  flex: 1;
  min-height: 44px;
  max-height: 120px;
  padding: 12px 16px;
  font-size: 14px;
  line-height: 1.5;
  color: #1f2937;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  outline: none;
  resize: none;
  font-family: inherit;
  transition: all 0.3s;
}

.chat-textarea:focus {
  background: #ffffff;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.chat-textarea::placeholder {
  color: #9ca3af;
}

.send-btn {
  height: 44px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #667eea;
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  background: #5568d3;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.icon-send::before {
  content: '✈️';
  font-size: 16px;
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.input-tips {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #9ca3af;
}

.input-tips i {
  font-size: 14px;
}

.icon-keyboard::before {
  content: '⌨️';
}

.icon-command::before {
  content: '⌘';
}

.char-count {
  font-size: 12px;
  color: #9ca3af;
}
</style>

