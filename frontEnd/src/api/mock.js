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
          name: '系统管理员',
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
          name: '普通用户',
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

