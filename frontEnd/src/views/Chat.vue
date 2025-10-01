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
      <aside class="chat-sidebar" :class="{ 'collapsed': sidebarCollapsed }">
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
      <main class="chat-main" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
        <!-- 对话区头部 -->
        <div class="chat-header">
          <div class="chat-header-right">
            <button class="icon-btn" @click="toggleSidebar" :title="sidebarCollapsed ? '展开侧边栏' : '收起侧边栏'">
              <i :class="sidebarCollapsed ? 'icon-sidebar-expand' : 'icon-sidebar-collapse'"></i>
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

// 所有会话的消息存储
const allSessionMessages = ref(new Map())

// 输入内容
const inputMessage = ref('')

// 加载状态
const isLoading = ref(false)

// 聊天内容容器引用
const chatContentRef = ref(null)

// 侧边栏收起状态
const sidebarCollapsed = ref(false)

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
    // 开发阶段使用模拟数据
    if (import.meta.env.MODE === 'development') {
      loadMockData()
    } else {
      const [kbRes, modelRes, historyRes] = await Promise.all([
        getKnowledgeBaseList(),
        getModelList(),
        getSessionHistory()
      ])
      
      knowledgeBaseList.value = kbRes.data
      modelList.value = modelRes.data
      sessionHistory.value = historyRes.data
    }
  } catch (error) {
    console.error('加载数据失败:', error)
    // 失败时也使用模拟数据
    loadMockData()
  }
}

/**
 * 加载模拟数据
 */
function loadMockData() {
  // 模拟知识库数据
  knowledgeBaseList.value = [
    { id: 'tech', name: '技术规范库' },
    { id: 'product', name: '产品手册' },
    { id: 'api', name: 'API文档' }
  ]
  
  // 模拟模型数据
  modelList.value = [
    { id: 'qwen2-7b', name: 'Qwen2-7B' },
    { id: 'gpt-4', name: 'GPT-4' }
  ]
  
  // 模拟会话历史数据
  const mockSessions = [
    {
      id: 'session1',
      title: 'API设计最佳实践',
      time: '今天 14:30'
    },
    {
      id: 'session2', 
      title: '数据库连接池配置',
      time: '今天 10:15'
    },
    {
      id: 'session3',
      title: 'Redis缓存策略',
      time: '昨天 16:45'
    },
    {
      id: 'session4',
      title: '微服务架构设计',
      time: '昨天 09:20'
    }
  ]
  
  sessionHistory.value = mockSessions
  
  // 模拟每个会话的消息数据
  const mockMessages = new Map()
  
  mockMessages.set('session1', [
    {
      id: 1,
      role: 'user',
      content: '如何设计RESTful API?',
      time: '14:28'
    },
    {
      id: 2,
      role: 'assistant', 
      content: 'RESTful API设计需要遵循以下原则：\n\n1. 使用HTTP方法：GET用于查询，POST用于创建，PUT用于更新，DELETE用于删除\n2. 资源导向的URL设计\n3. 使用合适的HTTP状态码\n4. 统一的响应格式\n5. 版本控制策略',
      references: [
        { title: 'REST API设计规范', page: 12 },
        { title: 'HTTP状态码参考', page: 5 }
      ],
      time: '14:29'
    },
    {
      id: 3,
      role: 'user',
      content: '能详细说说HTTP状态码的使用吗？',
      time: '14:30'
    },
    {
      id: 4,
      role: 'assistant',
      content: '常用的HTTP状态码包括：\n\n• 200 OK - 请求成功\n• 201 Created - 资源创建成功\n• 400 Bad Request - 请求参数错误\n• 401 Unauthorized - 未认证\n• 403 Forbidden - 权限不足\n• 404 Not Found - 资源不存在\n• 500 Internal Server Error - 服务器错误',
      time: '14:30'
    }
  ])
  
  mockMessages.set('session2', [
    {
      id: 1,
      role: 'user',
      content: '数据库连接池应该如何配置？',
      time: '10:12'
    },
    {
      id: 2,
      role: 'assistant',
      content: '数据库连接池配置需要考虑以下参数：\n\n1. **初始连接数** - 应用启动时创建的连接数\n2. **最大连接数** - 池中最多可创建的连接数\n3. **最小空闲连接数** - 池中保持的最少空闲连接\n4. **连接超时时间** - 获取连接的最大等待时间\n5. **连接有效性检测** - 定期检查连接是否可用',
      references: [
        { title: '数据库连接池最佳实践', page: 23 }
      ],
      time: '10:15'
    }
  ])
  
  mockMessages.set('session3', [
    {
      id: 1,
      role: 'user',
      content: 'Redis缓存如何优化？',
      time: '16:42'
    },
    {
      id: 2,
      role: 'assistant',
      content: 'Redis缓存优化策略包括：\n\n1. **选择合适的数据结构**\n2. **设置合理的过期时间**\n3. **使用管道批量操作**\n4. **避免大key问题**\n5. **监控内存使用情况**',
      time: '16:45'
    }
  ])
  
  mockMessages.set('session4', [
    {
      id: 1,
      role: 'user', 
      content: '微服务架构有什么注意事项？',
      time: '09:18'
    },
    {
      id: 2,
      role: 'assistant',
      content: '微服务架构需要注意：\n\n1. **服务拆分粒度**\n2. **服务间通信**\n3. **数据一致性**\n4. **服务治理**\n5. **监控和链路追踪**',
      time: '09:20'
    }
  ])
  
  allSessionMessages.value = mockMessages
  
  // 设置默认当前会话
  if (mockSessions.length > 0) {
    currentSessionId.value = mockSessions[0].id
    messages.value = mockMessages.get(mockSessions[0].id) || []
  }
}


/**
 * 新建对话
 */
async function createNewChat() {
  try {
    // 开发阶段使用模拟数据
    if (import.meta.env.MODE === 'development') {
      createMockSession()
    } else {
      const res = await createSession({
        knowledgeBaseId: selectedKnowledgeBase.value,
        modelId: selectedModel.value
      })
      
      currentSessionId.value = res.data.id
      messages.value = []
      
      // 刷新会话历史
      const historyRes = await getSessionHistory()
      sessionHistory.value = historyRes.data
    }
  } catch (error) {
    console.error('创建会话失败:', error)
    // 失败时使用模拟数据
    createMockSession()
  }
}

/**
 * 创建模拟会话
 */
function createMockSession() {
  const newSessionId = `session${Date.now()}`
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  
  const newSession = {
    id: newSessionId,
    title: '新会话',
    time: `今天 ${hours}:${minutes}`
  }
  
  // 添加到会话历史列表顶部
  sessionHistory.value.unshift(newSession)
  
  // 初始化空消息列表
  allSessionMessages.value.set(newSessionId, [])
  
  // 切换到新会话
  currentSessionId.value = newSessionId
  messages.value = []
  
  console.log('创建新会话成功:', newSession)
}

/**
 * 加载会话
 */
function loadSession(sessionId) {
  console.log('切换到会话:', sessionId)
  
  // 设置当前会话ID
  currentSessionId.value = sessionId
  
  // 加载对应的消息
  const sessionMessages = allSessionMessages.value.get(sessionId) || []
  messages.value = [...sessionMessages]
  
  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
  
  console.log('加载会话消息:', messages.value.length, '条')
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
  
  // 更新会话存储
  allSessionMessages.value.set(currentSessionId.value, [...messages.value])
  
  const question = inputMessage.value
  inputMessage.value = ''
  isLoading.value = true

  // 滚动到底部
  await nextTick()
  scrollToBottom()

  try {
    let assistantMessage
    
    // 开发阶段使用模拟响应
    if (import.meta.env.MODE === 'development') {
      assistantMessage = await getMockResponse(question)
    } else {
      const res = await sendChatMessage({
        sessionId: currentSessionId.value,
        question: question,
        knowledgeBaseId: selectedKnowledgeBase.value,
        modelId: selectedModel.value
      })

      assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: res.data.answer,
        references: res.data.references,
        time: formatTime(new Date())
      }
    }

    messages.value.push(assistantMessage)
    
    // 更新会话存储
    allSessionMessages.value.set(currentSessionId.value, [...messages.value])
    
    // 更新会话标题（如果是新会话的第一条消息）
    updateSessionTitle(currentSessionId.value, question)

    // 滚动到底部
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('发送消息失败:', error)
    
    // 失败时使用模拟响应
    try {
      const assistantMessage = await getMockResponse(question)
      messages.value.push(assistantMessage)
      allSessionMessages.value.set(currentSessionId.value, [...messages.value])
      updateSessionTitle(currentSessionId.value, question)
      await nextTick()
      scrollToBottom()
    } catch (mockError) {
      alert(error.message || '发送失败，请重试')
    }
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
 * 获取模拟响应
 */
async function getMockResponse(question) {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))
  
  // 根据问题关键词返回不同的模拟回答
  let content = ''
  let references = []
  
  const lowerQuestion = question.toLowerCase()
  
  if (lowerQuestion.includes('api') || lowerQuestion.includes('接口')) {
    content = '关于API设计，我建议遵循RESTful原则：\n\n1. 使用HTTP动词（GET、POST、PUT、DELETE）表示操作\n2. URL应该表示资源而不是操作\n3. 使用合适的HTTP状态码\n4. 提供一致的错误处理\n5. 考虑API版本管理\n\n这样可以让API更易于理解和使用。'
    references = [
      { title: 'REST API设计指南', page: 15 },
      { title: 'HTTP状态码规范', page: 8 }
    ]
  } else if (lowerQuestion.includes('数据库') || lowerQuestion.includes('database')) {
    content = '数据库优化建议：\n\n1. **索引优化** - 为常用查询字段添加索引\n2. **查询优化** - 避免SELECT *，使用具体字段\n3. **连接池配置** - 合理设置连接池大小\n4. **缓存策略** - 使用Redis等缓存热点数据\n5. **分库分表** - 数据量大时考虑水平拆分\n\n需要根据具体业务场景来选择合适的优化策略。'
    references = [
      { title: '数据库性能优化实战', page: 42 }
    ]
  } else if (lowerQuestion.includes('redis') || lowerQuestion.includes('缓存')) {
    content = 'Redis缓存最佳实践：\n\n1. **合理设置过期时间** - 避免内存泄漏\n2. **选择合适的数据结构** - String、Hash、List、Set、ZSet\n3. **使用Pipeline** - 批量操作减少网络往返\n4. **监控内存使用** - 设置内存上限和淘汰策略\n5. **主从复制** - 提高可用性\n\n记住，缓存不是万能的，要根据业务特点合理使用。'
  } else if (lowerQuestion.includes('微服务') || lowerQuestion.includes('架构')) {
    content = '微服务架构关键点：\n\n1. **服务拆分** - 按业务边界拆分，保持单一职责\n2. **服务通信** - 使用HTTP/gRPC进行服务间调用\n3. **配置管理** - 统一配置中心管理配置\n4. **服务治理** - 服务注册发现、负载均衡\n5. **监控告警** - 全链路监控，及时发现问题\n\n要权衡复杂度和收益，不是所有项目都适合微服务。'
  } else {
    // 默认通用回答
    content = `关于"${question}"这个问题，我来为您详细解答：\n\n根据我的知识库搜索，这是一个很好的技术问题。建议您：\n\n1. 首先理解问题的本质和背景\n2. 查阅相关的技术文档和最佳实践\n3. 结合实际项目需求进行选择\n4. 在测试环境中验证方案可行性\n5. 持续优化和改进\n\n如果需要更具体的建议，请提供更多上下文信息。`
    references = [
      { title: '技术架构设计指南', page: 23 }
    ]
  }
  
  return {
    id: Date.now() + 1,
    role: 'assistant',
    content,
    references: references.length > 0 ? references : undefined,
    time: formatTime(new Date())
  }
}

/**
 * 更新会话标题
 */
function updateSessionTitle(sessionId, question) {
  const session = sessionHistory.value.find(s => s.id === sessionId)
  if (session && session.title === '新会话') {
    // 截取问题的前15个字符作为标题
    session.title = question.length > 15 ? question.substring(0, 15) + '...' : question
  }
}

/**
 * 切换侧边栏
 */
function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

</script>

<style scoped>
.chat-page {
  padding: 32px 48px;
  max-width: 1800px;
  margin: 0 auto;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 88px;
  margin-bottom: 20px;
  flex-shrink: 0;
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

.current-time {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666666;
  padding: 8px 16px;
  background: #ffffff;
  border-radius: 8px;
}

.icon-time::before {
  content: '🕐';
  font-size: 16px;
}

/* 聊天容器 */
.chat-container {
  display: flex;
  gap: 28px;
  align-items: flex-start;
}

/* 左侧面板 */
.chat-sidebar {
  width: 300px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  padding: 28px 20px;
  flex-shrink: 0;
  height: calc(100vh - 152px);
  transition: all 0.3s ease;
  overflow: hidden;
}

.chat-sidebar.collapsed {
  width: 0;
  padding: 0;
  margin-right: -28px;
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
  min-height: 200px;
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
  min-height: 180px;
}

.history-item {
  padding: 12px;
  margin-bottom: 8px;
  background: #ffffff;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.history-item:hover {
  background: #f9fafb;
  border-color: #e5e7eb;
}

.history-item.active {
  background: #ede9fe;
  border-color: #667eea;
  position: relative;
}

.history-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #667eea;
  border-radius: 0 3px 3px 0;
}

.history-item.active .history-title {
  color: #667eea;
  font-weight: 600;
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
  margin-top: auto;
  flex-shrink: 0;
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
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  height: calc(100vh - 152px);
  transition: all 0.3s ease;
}

.chat-main.sidebar-collapsed {
  width: calc(100% + 328px);
}

/* 对话区头部 */
.chat-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 16px 28px;
  border-bottom: 1px solid #f0f0f0;
  flex-shrink: 0;
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

.icon-sidebar-collapse::before {
  content: '◀';
  font-size: 14px;
  color: #667eea;
}

.icon-sidebar-expand::before {
  content: '▶';
  font-size: 14px;
  color: #667eea;
}

/* 对话内容区 */
.chat-content {
  flex: 1;
  overflow-y: auto;
  padding: 0;
  background: #ffffff;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px 40px 40px;
  height: 100%;
  min-height: 500px;
}

.assistant-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #667eea;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.icon-robot::before {
  content: '🤖';
  font-size: 36px;
}

.assistant-title {
  font-size: 22px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.assistant-desc {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 48px 0;
  text-align: center;
}

/* 推荐问题 */
.suggestions-section {
  width: 100%;
  max-width: 900px;
}

.suggestions-title {
  font-size: 15px;
  font-weight: 500;
  color: #374151;
  margin: 0 0 20px 0;
  text-align: left;
  align-self: flex-start;
}

.suggestions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  width: 100%;
}

.suggestion-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 20px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  min-height: 60px;
}

.suggestion-card:hover {
  background: #ffffff;
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.12);
  transform: translateY(-1px);
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
  line-height: 1.4;
}

/* 消息列表 */
.messages-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 28px;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.message-item.assistant .message-avatar {
  background: #dbeafe;
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
  padding: 16px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
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
  padding: 24px 28px;
  border-top: 1px solid #f0f0f0;
  background: #ffffff;
  flex-shrink: 0;
}

.input-container {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.chat-textarea {
  flex: 1;
  min-height: 48px;
  max-height: 120px;
  padding: 12px 16px;
  font-size: 14px;
  line-height: 1.5;
  color: #1f2937;
  background: #ffffff;
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
  height: 48px;
  padding: 0 28px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #667eea;
  color: #ffffff;
  font-size: 15px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  background: #5568d3;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
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
  gap: 16px;
  font-size: 12px;
  color: #9ca3af;
}

.input-tips i {
  font-size: 14px;
}

.input-tips span {
  display: flex;
  align-items: center;
  gap: 4px;
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

