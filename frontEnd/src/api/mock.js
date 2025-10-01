/**
 * 模拟数据
 * 用于开发环境的接口模拟
 */

/**
 * 模拟登录接口
 * @param {object} params - 登录参数
 * @returns {object} 模拟响应
 */
export function mockLogin(params) {
  const { username, password } = params

  // 模拟登录验证
  if (username === 'admin' && password === 'admin123') {
    return {
      success: true,
      data: {
        token: 'mock_token_admin_' + Date.now(),
        user: {
          id: 'user_001',
          username: 'admin',
          name: '张三',
          role: 'admin',
          email: 'admin@company.com',
          phone: '13800138000'
        }
      },
      message: '登录成功'
    }
  } else if (username === 'user' && password === 'user123') {
    return {
      success: true,
      data: {
        token: 'mock_token_user_' + Date.now(),
        user: {
          id: 'user_002',
          username: 'user',
          name: '李四',
          role: 'user',
          email: 'user@company.com',
          phone: '13900139000'
        }
      },
      message: '登录成功'
    }
  } else {
    throw new Error('用户名或密码错误')
  }
}

/**
 * 模拟获取知识库统计数据
 * @returns {object} 模拟响应
 */
export function mockGetKnowledgeBaseStats() {
  return {
    success: true,
    data: {
      accessibleKnowledgeBase: 3,
      accessibleDocuments: 312,
      todayQuestions: 15
    },
    message: '获取成功'
  }
}

/**
 * 模拟获取知识库列表
 * @returns {object} 模拟响应
 */
export function mockGetKnowledgeBaseList() {
  return {
    success: true,
    data: [
      {
        id: 'kb_001',
        name: '技术规范库',
        code: 'tech-standards',
        description: '包含编程规范、API设计、架构指南等技术文档',
        icon: 'icon-code',
        iconColor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        documentCount: 156,
        storageSize: '2.3 GB',
        lastUpdate: '2小时前',
        status: 'active',
        progress: 100,
        viewers: 1200
      },
      {
        id: 'kb_002',
        name: '产品手册',
        code: 'product-manual',
        description: '产品功能介绍、使用指南、常见问题等',
        icon: 'icon-book',
        iconColor: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
        documentCount: 89,
        storageSize: '1.5 GB',
        lastUpdate: '1天前',
        status: 'active',
        progress: 100,
        viewers: 892
      },
      {
        id: 'kb_003',
        name: '运维文档',
        code: 'ops-docs',
        description: '系统部署、监控、故障处理等运维类文档',
        icon: 'icon-gear',
        iconColor: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        documentCount: 67,
        storageSize: '890 MB',
        lastUpdate: '3天前',
        status: 'processing',
        progress: 85,
        viewers: 456
      }
    ],
    message: '获取成功'
  }
}

/**
 * 模拟获取知识库简化列表（用于对话页面）
 * @returns {object} 模拟响应
 */
export function mockGetChatKnowledgeBaseList() {
  return {
    success: true,
    data: [
      { id: 'kb_001', name: '技术规范库' },
      { id: 'kb_002', name: '产品手册' },
      { id: 'kb_003', name: '运维文档' }
    ],
    message: '获取成功'
  }
}

/**
 * 模拟获取模型列表
 * @returns {object} 模拟响应
 */
export function mockGetModelList() {
  return {
    success: true,
    data: [
      {
        id: 'qwen2-7b',
        name: 'Qwen2-7B',
        description: '通义千问2 7B版本，适合日常问答'
      },
      {
        id: 'qwen2-14b',
        name: 'Qwen2-14B',
        description: '通义千问2 14B版本，性能更强'
      },
      {
        id: 'llama3-8b',
        name: 'Llama3-8B',
        description: 'Meta Llama3 8B版本'
      }
    ],
    message: '获取成功'
  }
}

/**
 * 模拟获取会话历史
 * @returns {object} 模拟响应
 */
export function mockGetSessionHistory() {
  return {
    success: true,
    data: [
      {
        id: 'session_001',
        title: 'API设计最佳实践',
        time: '今天 14:30',
        createdAt: '2025-10-01T14:30:00Z'
      },
      {
        id: 'session_002',
        title: '数据库连接池配置',
        time: '今天 10:15',
        createdAt: '2025-10-01T10:15:00Z'
      },
      {
        id: 'session_003',
        title: 'Redis缓存策略',
        time: '昨天 16:45',
        createdAt: '2025-09-30T16:45:00Z'
      }
    ],
    message: '获取成功'
  }
}

/**
 * 模拟创建会话
 * @param {object} params - 创建参数
 * @returns {object} 模拟响应
 */
export function mockCreateSession(params) {
  return {
    success: true,
    data: {
      id: 'session_' + Date.now(),
      title: '新对话',
      createdAt: new Date().toISOString()
    },
    message: '创建成功'
  }
}

/**
 * 模拟发送消息
 * @param {object} params - 消息参数
 * @returns {object} 模拟响应
 */
export function mockSendChatMessage(params) {
  const { question } = params
  
  // 根据不同问题返回不同的模拟回答
  const responses = {
    '如何设计RESTful API?': {
      answer: 'RESTful API 设计的最佳实践包括：\n\n1. 使用名词而非动词定义资源路径，如 /users 而不是 /getUsers\n2. 使用HTTP方法表示操作：GET(查询)、POST(创建)、PUT(更新)、DELETE(删除)\n3. 使用复数形式命名资源集合，如 /users 而不是 /user\n4. 使用嵌套路径表示关系，如 /users/{userId}/orders\n5. 提供适当的状态码：200(成功)、201(创建成功)、404(未找到)、500(服务器错误)等\n6. 支持过滤、排序和分页参数\n7. 使用版本控制，如 /v1/users\n8. 提供清晰的错误消息\n\n遵循这些原则可以让API更加直观和易用。',
      references: [
        {
          title: 'API设计规范.pdf',
          page: 12,
          content: 'RESTful API设计原则...',
          score: 0.95
        },
        {
          title: '架构最佳实践.pdf',
          page: 34,
          content: 'HTTP方法使用指南...',
          score: 0.88
        }
      ]
    },
    '数据库连接池最佳实践?': {
      answer: '数据库连接池配置的最佳实践：\n\n1. 连接池大小设置：\n   - 最小连接数：通常设置为5-10\n   - 最大连接数：根据并发量设置，一般为20-50\n   - 公式参考：连接数 = (核心数 × 2) + 有效磁盘数\n\n2. 超时设置：\n   - 连接超时：5-10秒\n   - 空闲超时：30-60分钟\n   - 最大生存时间：不超过数据库的wait_timeout\n\n3. 连接验证：\n   - 启用连接有效性检查\n   - 使用SELECT 1等轻量级SQL验证\n   - 设置合适的检查间隔\n\n4. 监控和调优：\n   - 监控活跃连接数\n   - 监控等待时间\n   - 根据实际负载调整参数',
      references: [
        {
          title: '数据库性能优化.pdf',
          page: 23,
          content: '连接池配置参数...',
          score: 0.92
        }
      ]
    },
    'Redis缓存如何优化?': {
      answer: 'Redis缓存优化策略：\n\n1. 数据结构选择：\n   - String：简单key-value\n   - Hash：对象存储\n   - List：队列、时间线\n   - Set：去重、交集\n   - ZSet：排行榜\n\n2. 过期策略：\n   - 设置合理的TTL\n   - 使用EXPIRE命令\n   - 避免大量key同时过期\n\n3. 内存优化：\n   - 启用内存淘汰策略\n   - 控制单个key大小\n   - 使用压缩\n\n4. 性能优化：\n   - 使用pipeline批量操作\n   - 避免使用KEYS命令\n   - 使用连接池\n\n5. 高可用：\n   - 主从复制\n   - 哨兵模式\n   - 集群模式',
      references: [
        {
          title: 'Redis最佳实践.pdf',
          page: 45,
          content: 'Redis缓存策略...',
          score: 0.90
        }
      ]
    },
    '微服务架构注意事项?': {
      answer: '微服务架构的关键注意事项：\n\n1. 服务拆分：\n   - 按业务领域拆分\n   - 单一职责原则\n   - 高内聚低耦合\n\n2. 服务通信：\n   - 使用RESTful或gRPC\n   - 考虑异步消息队列\n   - 实现服务熔断和降级\n\n3. 数据管理：\n   - 每个服务独立数据库\n   - 使用分布式事务（Saga模式）\n   - 数据一致性处理\n\n4. 服务治理：\n   - 服务注册与发现\n   - 负载均衡\n   - 配置中心\n   - API网关\n\n5. 监控和日志：\n   - 分布式链路追踪\n   - 集中式日志\n   - 健康检查\n\n6. 部署和运维：\n   - 容器化（Docker）\n   - 编排工具（Kubernetes）\n   - CI/CD自动化',
      references: [
        {
          title: '微服务架构实践.pdf',
          page: 78,
          content: '微服务设计原则...',
          score: 0.93
        },
        {
          title: '分布式系统指南.pdf',
          page: 56,
          content: '服务治理策略...',
          score: 0.87
        }
      ]
    }
  }

  // 默认回答
  const defaultResponse = {
    answer: `关于"${question}"的问题，我已经帮您在知识库中搜索到了相关信息。\n\n根据技术文档的内容，这个问题需要考虑多个方面。建议您查看引用的文档获取更详细的信息。\n\n如果您需要更具体的解答，欢迎继续提问！`,
    references: [
      {
        title: '技术参考文档.pdf',
        page: 15,
        content: '相关技术说明...',
        score: 0.85
      }
    ]
  }

  const response = responses[question] || defaultResponse

  return {
    success: true,
    data: response,
    message: '获取成功'
  }
}

/**
 * 模拟搜索文档
 * @param {object} params - 搜索参数
 * @returns {object} 模拟响应
 */
export function mockSearchDocuments(params) {
  const { keyword, page = 1, pageSize = 10 } = params
  
  // 如果没有关键词，返回空结果
  if (!keyword) {
    return {
      success: true,
      data: {
        list: [],
        total: 0,
        page: 1,
        pageSize: 10
      },
      message: '请输入搜索关键词'
    }
  }

  // 模拟搜索结果
  const allResults = [
    {
      id: 'doc_001',
      title: 'RESTful API设计规范v2.0.pdf',
      knowledgeBase: '技术规范库',
      docType: 'PDF',
      excerpt: '...完整的<em>API设计</em>规范文档，包括命名规则、HTTP方法使用、状态码定义等内容...',
      score: 0.95,
      pageNumber: 12,
      updateTime: '2025-09-28',
      size: '2.3 MB'
    },
    {
      id: 'doc_002',
      title: '数据库连接池配置指南.pdf',
      knowledgeBase: '技术规范库',
      docType: 'PDF',
      excerpt: '...详细介绍了<em>数据库连接池</em>的配置方法和最佳实践，包括连接数设置、超时配置等...',
      score: 0.92,
      pageNumber: 23,
      updateTime: '2025-09-25',
      size: '1.8 MB'
    },
    {
      id: 'doc_003',
      title: 'Redis缓存使用手册.pdf',
      knowledgeBase: '技术规范库',
      docType: 'PDF',
      excerpt: '...全面的<em>Redis</em>缓存使用指南，涵盖数据结构选择、过期策略、性能优化等内容...',
      score: 0.90,
      pageNumber: 45,
      updateTime: '2025-09-20',
      size: '3.1 MB'
    },
    {
      id: 'doc_004',
      title: '微服务架构设计手册.pdf',
      knowledgeBase: '技术规范库',
      docType: 'PDF',
      excerpt: '...介绍<em>微服务架构</em>的设计原则、服务拆分、通信方式、数据管理等核心内容...',
      score: 0.88,
      pageNumber: 78,
      updateTime: '2025-09-15',
      size: '4.5 MB'
    },
    {
      id: 'doc_005',
      title: 'MySQL性能优化实战.pdf',
      knowledgeBase: '技术规范库',
      docType: 'PDF',
      excerpt: '...深入讲解MySQL<em>性能优化</em>技巧，包括索引优化、查询优化、配置调优等内容...',
      score: 0.85,
      pageNumber: 56,
      updateTime: '2025-09-10',
      size: '2.7 MB'
    },
    {
      id: 'doc_006',
      title: 'Docker容器化部署指南.pdf',
      knowledgeBase: '运维文档',
      docType: 'PDF',
      excerpt: '...详细说明如何使用<em>Docker</em>进行应用容器化，包括镜像构建、容器编排等内容...',
      score: 0.82,
      pageNumber: 34,
      updateTime: '2025-09-05',
      size: '3.2 MB'
    },
    {
      id: 'doc_007',
      title: 'Nginx配置最佳实践.pdf',
      knowledgeBase: '运维文档',
      docType: 'PDF',
      excerpt: '...介绍<em>Nginx</em>的配置技巧和最佳实践，包括负载均衡、反向代理、缓存配置等...',
      score: 0.80,
      pageNumber: 28,
      updateTime: '2025-08-30',
      size: '1.5 MB'
    },
    {
      id: 'doc_008',
      title: '产品功能使用手册v3.0.pdf',
      knowledgeBase: '产品手册',
      docType: 'PDF',
      excerpt: '...全面的产品<em>功能介绍</em>和使用指南，帮助用户快速上手使用系统各项功能...',
      score: 0.78,
      pageNumber: 15,
      updateTime: '2025-08-25',
      size: '5.2 MB'
    }
  ]

  // 根据关键词过滤
  const filteredResults = allResults.filter(doc => 
    doc.title.toLowerCase().includes(keyword.toLowerCase()) ||
    doc.excerpt.toLowerCase().includes(keyword.toLowerCase())
  )

  // 分页
  const start = (page - 1) * pageSize
  const end = start + pageSize
  const pagedResults = filteredResults.slice(start, end)

  return {
    success: true,
    data: {
      list: pagedResults,
      total: filteredResults.length,
      page: page,
      pageSize: pageSize
    },
    message: '搜索成功'
  }
}

/**
 * 模拟获取热门搜索关键词
 * @returns {object} 模拟响应
 */
export function mockGetHotKeywords() {
  return {
    success: true,
    data: [
      { keyword: 'API设计规范', count: 156 },
      { keyword: '数据库连接池', count: 132 },
      { keyword: 'Redis缓存', count: 128 },
      { keyword: '微服务架构', count: 115 },
      { keyword: '性能优化', count: 98 }
    ],
    message: '获取成功'
  }
}

/**
 * 模拟获取文档类型列表
 * @returns {object} 模拟响应
 */
export function mockGetDocTypes() {
  return {
    success: true,
    data: [
      { value: 'all', label: '全部类型' },
      { value: 'pdf', label: 'PDF文档' },
      { value: 'word', label: 'Word文档' },
      { value: 'markdown', label: 'Markdown文档' },
      { value: 'text', label: '文本文档' }
    ],
    message: '获取成功'
  }
}

/**
 * 模拟导出搜索结果
 * @param {object} params - 导出参数
 * @returns {object} 模拟响应
 */
export function mockExportSearchResults(params) {
  return {
    success: true,
    data: {
      downloadUrl: '/downloads/search-results-' + Date.now() + '.csv',
      fileName: 'search-results-' + new Date().toISOString().split('T')[0] + '.csv',
      expiresIn: 3600
    },
    message: '导出成功'
  }
}

/**
 * 模拟获取用户个人信息
 * @returns {object} 模拟响应
 */
export function mockGetUserProfile() {
  return {
    success: true,
    data: {
      id: 'user_001',
      username: 'zhangsan',
      name: '张三',
      email: 'zhangsan@company.com',
      phone: '138****1234',
      department: 'tech',
      position: '高级工程师',
      avatar: '/avatars/default-avatar.png',
      bio: '专注于后端开发和系统架构设计，有多年互联网开发经验。',
      role: 'user',
      createdAt: '2024-01-15T08:30:00Z',
      lastLoginAt: '2024-09-25T09:30:00Z'
    },
    message: '获取成功'
  }
}

/**
 * 模拟更新用户信息
 * @param {object} params - 更新参数
 * @returns {object} 模拟响应
 */
export function mockUpdateUserProfile(params) {
  return {
    success: true,
    data: {
      id: 'user_001',
      ...params,
      updatedAt: new Date().toISOString()
    },
    message: '更新成功'
  }
}

/**
 * 模拟上传头像
 * @param {FormData} formData - 文件数据
 * @returns {object} 模拟响应
 */
export function mockUploadUserAvatar(formData) {
  return {
    success: true,
    data: {
      avatarUrl: '/avatars/user-avatar-' + Date.now() + '.png'
    },
    message: '头像上传成功'
  }
}

/**
 * 模拟获取部门列表
 * @returns {object} 模拟响应
 */
export function mockGetDepartmentList() {
  return {
    success: true,
    data: [
      { value: 'tech', label: '技术部' },
      { value: 'product', label: '产品部' },
      { value: 'design', label: '设计部' },
      { value: 'marketing', label: '市场部' },
      { value: 'sales', label: '销售部' },
      { value: 'hr', label: '人力资源部' },
      { value: 'finance', label: '财务部' },
      { value: 'admin', label: '行政部' }
    ],
    message: '获取成功'
  }
}

/**
 * 模拟获取登录记录
 * @param {object} params - 查询参数
 * @returns {object} 模拟响应
 */
export function mockGetLoginRecords(params) {
  return {
    success: true,
    data: [
      {
        id: 'login_001',
        device: 'Windows Chrome',
        ip: '192.168.1.100',
        location: '北京',
        loginTime: '2024-09-25T09:30:00Z',
        status: 'current',
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      },
      {
        id: 'login_002',
        device: 'iPhone Safari',
        ip: '192.168.1.101',
        location: '北京',
        loginTime: '2024-09-24T18:45:00Z',
        status: 'ended',
        userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'
      },
      {
        id: 'login_003',
        device: 'MacBook Chrome',
        ip: '192.168.1.102',
        location: '上海',
        loginTime: '2024-09-23T14:20:00Z',
        status: 'ended',
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
      }
    ],
    message: '获取成功'
  }
}

/**
 * 模拟修改密码
 * @param {object} params - 修改参数
 * @returns {object} 模拟响应
 */
export function mockChangeUserPassword(params) {
  const { currentPassword, newPassword, confirmPassword } = params

  // 模拟密码验证
  if (currentPassword !== 'user123') {
    throw new Error('当前密码错误')
  }

  if (newPassword !== confirmPassword) {
    throw new Error('新密码和确认密码不一致')
  }

  if (newPassword.length < 6) {
    throw new Error('密码长度不能少于6位')
  }

  return {
    success: true,
    data: {},
    message: '密码修改成功'
  }
}

