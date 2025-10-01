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

