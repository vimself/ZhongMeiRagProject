<template>
  <div class="search-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">文档搜索</h1>
        <p class="page-subtitle">快速查找相关全文档内容</p>
      </div>
      <div class="header-right">
        <div class="current-time">
          <i class="icon-time"></i>
          <span>{{ currentTime }}</span>
        </div>
      </div>
    </div>

    <!-- 搜索区域 -->
    <div class="search-section">
      <!-- 搜索框 -->
      <div class="search-bar">
        <input
          v-model="searchKeyword"
          type="text"
          class="search-input"
          placeholder="搜索文档内容、技术问题、API接口..."
          @keydown.enter="handleSearch"
        />
        <button class="search-btn" @click="handleSearch">
          <i class="icon-search-btn"></i>
          <span>搜索</span>
        </button>
      </div>

      <!-- 筛选器 -->
      <div class="filter-bar">
        <div class="filter-left">
          <div class="filter-item">
            <label class="filter-label">知识库:</label>
            <select v-model="filters.knowledgeBaseId" class="filter-select">
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

          <div class="filter-item">
            <label class="filter-label">文档类型:</label>
            <select v-model="filters.docType" class="filter-select">
              <option 
                v-for="type in docTypes" 
                :key="type.value" 
                :value="type.value"
              >
                {{ type.label }}
              </option>
            </select>
          </div>

          <div class="filter-item">
            <label class="filter-label">排序:</label>
            <select v-model="filters.sortBy" class="filter-select">
              <option value="relevance">相关度</option>
              <option value="time">时间</option>
              <option value="title">标题</option>
            </select>
          </div>
        </div>

        <div class="filter-right">
          <button class="export-btn" @click="handleExport" :disabled="!hasSearched || results.length === 0">
            <i class="icon-download"></i>
            <span>导出结果</span>
          </button>
        </div>
      </div>

      <!-- 热门搜索 -->
      <div class="hot-keywords-section">
        <span class="hot-keywords-label">热门搜索:</span>
        <div class="hot-keywords-list">
          <span 
            v-for="item in hotKeywords" 
            :key="item.keyword"
            class="keyword-tag"
            @click="searchByKeyword(item.keyword)"
          >
            {{ item.keyword }}
          </span>
        </div>
      </div>
    </div>

    <!-- 搜索结果区域 -->
    <div class="results-section">
      <!-- 空状态 -->
      <div v-if="!hasSearched" class="empty-state">
        <i class="icon-search-empty"></i>
        <h3 class="empty-title">开始搜索文档</h3>
        <p class="empty-desc">输入关键词或问题查找相关文档和规范</p>
      </div>

      <!-- 加载中 -->
      <div v-else-if="loading" class="loading-state">
        <i class="icon-loading"></i>
        <span>搜索中...</span>
      </div>

      <!-- 搜索结果 -->
      <div v-else-if="results.length > 0" class="results-container">
        <!-- 结果统计 -->
        <div class="results-header">
          <span class="results-count">找到 <strong>{{ total }}</strong> 个相关结果</span>
          <span class="search-time">搜索耗时: {{ searchTime }}ms</span>
        </div>

        <!-- 结果列表 -->
        <div class="results-list">
          <div 
            v-for="doc in results" 
            :key="doc.id"
            class="result-item"
            @click="viewDocument(doc)"
          >
            <div class="result-header">
              <h3 class="result-title">{{ doc.title }}</h3>
              <span class="result-score">{{ Math.round(doc.score * 100) }}% 匹配</span>
            </div>
            
            <div class="result-excerpt" v-html="doc.excerpt"></div>
            
            <div class="result-meta">
              <span class="meta-item">
                <i class="icon-kb-small"></i>
                {{ doc.knowledgeBase }}
              </span>
              <span class="meta-item">
                <i class="icon-file-type"></i>
                {{ doc.docType }}
              </span>
              <span class="meta-item">
                <i class="icon-page"></i>
                第 {{ doc.pageNumber }} 页
              </span>
              <span class="meta-item">
                <i class="icon-time-small"></i>
                {{ doc.updateTime }}
              </span>
              <span class="meta-item">
                <i class="icon-size"></i>
                {{ doc.size }}
              </span>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div v-if="total > pageSize" class="pagination">
          <button 
            class="page-btn" 
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
          >
            上一页
          </button>
          <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
          <button 
            class="page-btn" 
            :disabled="currentPage === totalPages"
            @click="changePage(currentPage + 1)"
          >
            下一页
          </button>
        </div>
      </div>

      <!-- 无结果 -->
      <div v-else class="no-results">
        <i class="icon-no-results"></i>
        <h3 class="no-results-title">未找到相关结果</h3>
        <p class="no-results-desc">换个关键词试试，或浏览热门搜索</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  searchDocuments, 
  getHotKeywords, 
  getDocTypes,
  exportSearchResults 
} from '../api/searchApi'
import { getKnowledgeBaseList } from '../api/chatApi'

const router = useRouter()

// 当前时间
const currentTime = ref('')

// 搜索关键词
const searchKeyword = ref('')

// 筛选器
const filters = ref({
  knowledgeBaseId: 'all',
  docType: 'all',
  sortBy: 'relevance'
})

// 知识库列表
const knowledgeBaseList = ref([])

// 文档类型列表
const docTypes = ref([])

// 热门搜索关键词
const hotKeywords = ref([])

// 搜索结果
const results = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchTime = ref(0)

// 加载状态
const loading = ref(false)

// 是否已搜索
const hasSearched = ref(false)

// 定时器ID
let timeInterval = null

// 计算总页数
const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value)
})

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
    const [kbRes, typesRes, hotRes] = await Promise.all([
      getKnowledgeBaseList(),
      getDocTypes(),
      getHotKeywords()
    ])
    
    knowledgeBaseList.value = kbRes.data
    docTypes.value = typesRes.data
    hotKeywords.value = hotRes.data
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

/**
 * 执行搜索
 */
async function handleSearch() {
  if (!searchKeyword.value.trim()) {
    alert('请输入搜索关键词')
    return
  }

  loading.value = true
  hasSearched.value = true
  currentPage.value = 1

  const startTime = Date.now()

  try {
    const res = await searchDocuments({
      keyword: searchKeyword.value,
      knowledgeBaseId: filters.value.knowledgeBaseId,
      docType: filters.value.docType,
      sortBy: filters.value.sortBy,
      page: currentPage.value,
      pageSize: pageSize.value
    })

    results.value = res.data.list
    total.value = res.data.total
    searchTime.value = Date.now() - startTime
  } catch (error) {
    console.error('搜索失败:', error)
    alert(error.message || '搜索失败，请重试')
  } finally {
    loading.value = false
  }
}

/**
 * 点击热门关键词搜索
 */
function searchByKeyword(keyword) {
  searchKeyword.value = keyword
  handleSearch()
}

/**
 * 翻页
 */
async function changePage(page) {
  if (page < 1 || page > totalPages.value) {
    return
  }

  currentPage.value = page
  loading.value = true

  try {
    const res = await searchDocuments({
      keyword: searchKeyword.value,
      knowledgeBaseId: filters.value.knowledgeBaseId,
      docType: filters.value.docType,
      sortBy: filters.value.sortBy,
      page: currentPage.value,
      pageSize: pageSize.value
    })

    results.value = res.data.list
    total.value = res.data.total
    
    // 滚动到顶部
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (error) {
    console.error('加载失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 查看文档
 */
function viewDocument(doc) {
  // TODO: 实现文档预览功能
  console.log('查看文档:', doc)
  alert(`查看文档: ${doc.title}\n功能开发中...`)
}

/**
 * 导出搜索结果
 */
async function handleExport() {
  try {
    const res = await exportSearchResults({
      keyword: searchKeyword.value,
      knowledgeBaseId: filters.value.knowledgeBaseId,
      docType: filters.value.docType,
      sortBy: filters.value.sortBy
    })

    // 提示用户
    alert(`导出成功！\n文件名: ${res.data.fileName}\n下载链接: ${res.data.downloadUrl}`)
    
    // TODO: 实际下载文件
    // window.open(res.data.downloadUrl, '_blank')
  } catch (error) {
    console.error('导出失败:', error)
    alert(error.message || '导出失败，请重试')
  }
}
</script>

<style scoped>
.search-page {
  padding: 32px 48px;
  max-width: 1800px;
  margin: 0 auto;
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

/* 搜索区域 */
.search-section {
  background: #ffffff;
  border-radius: 12px;
  padding: 28px;
  margin-bottom: 28px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* 搜索框 */
.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  height: 48px;
  padding: 0 20px;
  font-size: 15px;
  color: #1a1a1a;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  outline: none;
  transition: all 0.3s;
}

.search-input:focus {
  background: #ffffff;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-input::placeholder {
  color: #9ca3af;
}

.search-btn {
  height: 48px;
  padding: 0 32px;
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

.search-btn:hover {
  background: #5568d3;
}

.icon-search-btn::before {
  content: '🔍';
  font-size: 18px;
}

/* 筛选器 */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-left {
  display: flex;
  gap: 20px;
  align-items: center;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #666666;
  white-space: nowrap;
}

.filter-select {
  height: 36px;
  padding: 0 12px;
  font-size: 14px;
  color: #1a1a1a;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  outline: none;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-select:hover {
  border-color: #667eea;
}

.filter-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.export-btn {
  height: 36px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 6px;
  background: #ffffff;
  color: #667eea;
  font-size: 14px;
  font-weight: 500;
  border: 1px solid #667eea;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.export-btn:hover:not(:disabled) {
  background: #667eea;
  color: #ffffff;
}

.export-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.icon-download::before {
  content: '📥';
  font-size: 16px;
}

/* 热门搜索 */
.hot-keywords-section {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.hot-keywords-label {
  font-size: 14px;
  color: #666666;
}

.hot-keywords-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.keyword-tag {
  padding: 6px 16px;
  background: #f3f4f6;
  color: #4b5563;
  font-size: 13px;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.keyword-tag:hover {
  background: #ede9fe;
  color: #667eea;
}

/* 搜索结果区域 */
.results-section {
  min-height: 400px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 100px 20px;
}

.icon-search-empty::before {
  content: '🔍';
  font-size: 80px;
  display: block;
  margin-bottom: 24px;
  opacity: 0.5;
}

.empty-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.empty-desc {
  font-size: 15px;
  color: #666666;
  margin: 0;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 20px;
  color: #666666;
  font-size: 15px;
}

.icon-loading {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 搜索结果 */
.results-container {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.results-count {
  font-size: 15px;
  color: #666666;
}

.results-count strong {
  color: #667eea;
  font-weight: 600;
}

.search-time {
  font-size: 13px;
  color: #999999;
}

/* 结果列表 */
.results-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-item {
  padding: 20px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.result-item:hover {
  background: #ffffff;
  border-color: #667eea;
  box-shadow: 0 2px 12px rgba(102, 126, 234, 0.1);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.result-title {
  flex: 1;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.4;
}

.result-score {
  padding: 4px 12px;
  background: #d1fae5;
  color: #059669;
  font-size: 12px;
  font-weight: 500;
  border-radius: 12px;
  margin-left: 12px;
  flex-shrink: 0;
}

.result-excerpt {
  font-size: 14px;
  line-height: 1.6;
  color: #4b5563;
  margin-bottom: 16px;
}

.result-excerpt :deep(em) {
  color: #667eea;
  font-style: normal;
  font-weight: 600;
  background: rgba(102, 126, 234, 0.1);
  padding: 2px 4px;
  border-radius: 3px;
}

.result-meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #6b7280;
}

.meta-item i {
  font-size: 14px;
}

.icon-kb-small::before {
  content: '📚';
}

.icon-file-type::before {
  content: '📄';
}

.icon-page::before {
  content: '📃';
}

.icon-time-small::before {
  content: '🕐';
}

.icon-size::before {
  content: '💾';
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.page-btn {
  height: 36px;
  padding: 0 20px;
  background: #ffffff;
  color: #667eea;
  font-size: 14px;
  border: 1px solid #667eea;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  background: #667eea;
  color: #ffffff;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #666666;
}

/* 无结果 */
.no-results {
  text-align: center;
  padding: 100px 20px;
}

.icon-no-results::before {
  content: '📭';
  font-size: 80px;
  display: block;
  margin-bottom: 24px;
  opacity: 0.5;
}

.no-results-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.no-results-desc {
  font-size: 15px;
  color: #666666;
  margin: 0;
}
</style>
