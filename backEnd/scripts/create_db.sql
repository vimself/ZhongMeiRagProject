-- RAG知识问答系统数据库创建脚本
-- MySQL 5.7+ / MariaDB 10.2+

-- 创建数据库
CREATE DATABASE IF NOT EXISTS rag_knowledge_base 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

USE rag_knowledge_base;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(50) PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    role VARCHAR(20) NOT NULL DEFAULT 'user' COMMENT '角色：user, admin',
    email VARCHAR(100) COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '手机号',
    avatar VARCHAR(255) COMMENT '头像URL',
    department VARCHAR(100) COMMENT '部门',
    position VARCHAR(100) COMMENT '职位',
    bio VARCHAR(200) COMMENT '个人简介',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态：active, disabled',
    last_login_at DATETIME COMMENT '最后登录时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 知识库表
CREATE TABLE IF NOT EXISTS knowledge_bases (
    id VARCHAR(50) PRIMARY KEY COMMENT '知识库ID',
    name VARCHAR(100) NOT NULL COMMENT '知识库名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '知识库编码',
    description TEXT COMMENT '描述',
    icon VARCHAR(50) COMMENT '图标',
    icon_color VARCHAR(100) COMMENT '图标颜色',
    visible VARCHAR(20) DEFAULT 'all' COMMENT '可见范围：all, authorized, private',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态：active, processing, inactive',
    progress INT DEFAULT 0 COMMENT '处理进度',
    chunk_size INT DEFAULT 500 COMMENT '文本切片大小',
    chunk_overlap INT DEFAULT 50 COMMENT '切片重叠大小',
    similarity_threshold FLOAT DEFAULT 0.7 COMMENT '相似度阈值',
    top_k INT DEFAULT 5 COMMENT '检索TopK',
    vector_model_id VARCHAR(50) COMMENT '向量模型ID',
    created_by VARCHAR(50) COMMENT '创建人ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_code (code),
    INDEX idx_status (status),
    FOREIGN KEY (created_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='知识库表';

-- 文档表
CREATE TABLE IF NOT EXISTS documents (
    id VARCHAR(50) PRIMARY KEY COMMENT '文档ID',
    knowledge_base_id VARCHAR(50) NOT NULL COMMENT '知识库ID',
    name VARCHAR(255) NOT NULL COMMENT '文档名称',
    file_name VARCHAR(255) NOT NULL COMMENT '文件名',
    file_path VARCHAR(500) NOT NULL COMMENT '文件路径',
    file_size BIGINT COMMENT '文件大小（字节）',
    file_type VARCHAR(20) COMMENT '文件类型：pdf, doc, docx, txt',
    page_count INT COMMENT '页数',
    chunk_count INT DEFAULT 0 COMMENT '切片数量',
    status VARCHAR(20) DEFAULT 'processing' COMMENT '状态：processing, processed, failed',
    error_message TEXT COMMENT '错误信息',
    tags JSON COMMENT '标签',
    uploaded_by VARCHAR(50) COMMENT '上传人ID',
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
    processed_at DATETIME COMMENT '处理完成时间',
    INDEX idx_kb_id (knowledge_base_id),
    INDEX idx_status (status),
    FOREIGN KEY (knowledge_base_id) REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文档表';

-- 知识库权限表
CREATE TABLE IF NOT EXISTS knowledge_base_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '权限ID',
    knowledge_base_id VARCHAR(50) NOT NULL COMMENT '知识库ID',
    user_id VARCHAR(50) NOT NULL COMMENT '用户ID',
    permission VARCHAR(20) NOT NULL COMMENT '权限：view, manage',
    granted_by VARCHAR(50) COMMENT '授权人ID',
    granted_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '授权时间',
    UNIQUE KEY uk_kb_user (knowledge_base_id, user_id),
    INDEX idx_kb_id (knowledge_base_id),
    INDEX idx_user_id (user_id),
    FOREIGN KEY (knowledge_base_id) REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (granted_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='知识库权限表';

-- 会话表
CREATE TABLE IF NOT EXISTS chat_sessions (
    id VARCHAR(50) PRIMARY KEY COMMENT '会话ID',
    user_id VARCHAR(50) NOT NULL COMMENT '用户ID',
    title VARCHAR(255) DEFAULT '新对话' COMMENT '会话标题',
    knowledge_base_id VARCHAR(50) COMMENT '知识库ID',
    model_id VARCHAR(50) COMMENT '模型ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (knowledge_base_id) REFERENCES knowledge_bases(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会话表';

-- 消息表
CREATE TABLE IF NOT EXISTS chat_messages (
    id VARCHAR(50) PRIMARY KEY COMMENT '消息ID',
    session_id VARCHAR(50) NOT NULL COMMENT '会话ID',
    role VARCHAR(20) NOT NULL COMMENT '角色：user, assistant',
    content TEXT NOT NULL COMMENT '消息内容',
    `references` JSON COMMENT '引用来源',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_session_id (session_id),
    FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息表';

-- 模型表
CREATE TABLE IF NOT EXISTS models (
    id VARCHAR(50) PRIMARY KEY COMMENT '模型ID',
    name VARCHAR(100) NOT NULL UNIQUE COMMENT '模型名称',
    type VARCHAR(20) NOT NULL COMMENT '类型：llm, embedding',
    description TEXT COMMENT '描述',
    provider VARCHAR(50) COMMENT '提供方：local, openai等',
    endpoint VARCHAR(500) COMMENT '接口地址',
    api_key VARCHAR(255) COMMENT 'API密钥',
    status VARCHAR(20) DEFAULT 'offline' COMMENT '状态：online, offline, error',
    is_default BOOLEAN DEFAULT FALSE COMMENT '是否默认',
    model_size VARCHAR(50) COMMENT '模型大小',
    context_length INT COMMENT '上下文长度',
    gpu_memory VARCHAR(50) COMMENT 'GPU显存需求',
    config JSON COMMENT '配置参数',
    last_check_time DATETIME COMMENT '最后检查时间',
    response_time INT COMMENT '响应时间（毫秒）',
    health_message VARCHAR(500) COMMENT '健康检查消息',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_name (name),
    INDEX idx_type (type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模型表';

-- 登录记录表
CREATE TABLE IF NOT EXISTS login_records (
    id VARCHAR(50) PRIMARY KEY COMMENT '记录ID',
    user_id VARCHAR(50) NOT NULL COMMENT '用户ID',
    ip VARCHAR(50) COMMENT 'IP地址',
    location VARCHAR(100) COMMENT '地理位置',
    device VARCHAR(100) COMMENT '设备类型',
    user_agent VARCHAR(500) COMMENT 'User Agent',
    status VARCHAR(20) DEFAULT 'current' COMMENT '状态：current, ended',
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '登录时间',
    logout_time DATETIME COMMENT '登出时间',
    INDEX idx_user_id (user_id),
    INDEX idx_login_time (login_time),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='登录记录表';

-- 插入初始管理员账号
-- 密码: admin123 (bcrypt加密后的哈希值)
INSERT INTO users (id, username, password_hash, name, role, email, phone, status) 
VALUES (
    'user_admin001',
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eWb5wrq6OGFq',
    '系统管理员',
    'admin',
    'admin@example.com',
    '13800138000',
    'active'
);

-- 插入测试用户
-- 密码: user123
INSERT INTO users (id, username, password_hash, name, role, email, phone, status) 
VALUES (
    'user_test001',
    'user',
    '$2b$12$rMeWqxq1K5sx8xJQj0wN4.N9i2/TKm6DqBYXJq6zLcP9kN1K5sQHG',
    '测试用户',
    'user',
    'user@example.com',
    '13900139000',
    'active'
);

