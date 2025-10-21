# RAG知识问答系统 - 后端项目

> **版本**: v1.0  
> **框架**: Flask + MySQL + Chroma  
> **Python**: 3.8+

---

## 📋 项目简介

这是一个基于RAG（Retrieval-Augmented Generation）技术的企业级知识问答系统后端服务，支持：

- ✅ 用户认证与权限管理
- ✅ 知识库管理（CRUD）
- ✅ 文档上传与向量化
- ✅ 智能问答（RAG）
- ✅ 语义搜索
- ✅ 模型管理
- ✅ 多用户协作

---

## 🚀 快速开始

### 1. 环境准备

**系统要求**:
- Python 3.8+
- MySQL 5.7+ 或 MariaDB 10.2+
- 2GB+ 内存
- 5GB+ 磁盘空间

**安装依赖**:

```bash
cd backEnd
pip install -r requirements.txt
```

### 2. 配置环境变量

复制环境变量示例文件：

```bash
cp env.example .env
```

编辑 `.env` 文件，配置数据库连接：

```ini
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=rag_knowledge_base

# JWT配置
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_EXPIRATION_HOURS=24
```

### 3. 初始化数据库

**方法一：使用SQL脚本**

```bash
# 创建数据库和表
mysql -u root -p < scripts/create_db.sql
```

**方法二：使用Python脚本**

```bash
# 初始化数据库（包含示例数据）
python scripts/init_db.py
```

输入 `yes` 确认初始化。

### 4. 启动服务

```bash
# 开发环境
python app.py

# 或使用Flask命令
flask run --host=0.0.0.0 --port=8000
```

服务将运行在 `http://localhost:8000`

### 5. 测试接口

```bash
# 健康检查
curl http://localhost:8000/health

# 登录测试
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

---

## 📁 项目结构

```
backEnd/
├── api/                      # API接口模块
│   ├── auth.py              # 用户认证
│   ├── user.py              # 个人中心
│   ├── dashboard.py         # 仪表板
│   ├── knowledge_base.py    # 知识库管理
│   ├── chat.py              # 智能问答
│   ├── search.py            # 搜索
│   ├── admin_users.py       # 用户管理
│   └── models.py            # 模型管理
├── models/                   # 数据库模型
│   ├── user.py              # 用户模型
│   ├── knowledge_base.py    # 知识库模型
│   ├── chat.py              # 会话模型
│   ├── model.py             # 模型配置
│   └── login_record.py      # 登录记录
├── services/                 # 业务逻辑服务（待实现）
│   ├── chroma_service.py    # 向量数据库服务
│   ├── embedding_service.py # 向量化服务
│   └── rag_service.py       # RAG服务
├── utils/                    # 工具函数
│   ├── auth.py              # 认证工具
│   ├── response.py          # 响应格式
│   ├── helpers.py           # 辅助函数
│   └── validators.py        # 数据验证
├── scripts/                  # 脚本工具
│   ├── init_db.py           # 数据库初始化
│   ├── migrate_db.py        # 数据库迁移
│   └── create_db.sql        # SQL建表脚本
├── docs/                     # 文档
│   └── ChromaDB使用说明.md
├── app.py                    # 应用入口
├── config.py                 # 配置文件
├── requirements.txt          # Python依赖
├── env.example               # 环境变量示例
└── README.md                 # 本文件
```

---

## 🔧 配置说明

### 开发环境 vs 生产环境

在 `.env` 文件中设置：

```ini
# 开发环境
FLASK_ENV=development
FLASK_DEBUG=True

# 生产环境
FLASK_ENV=production
FLASK_DEBUG=False
```

### 数据库配置

支持MySQL和MariaDB：

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=rag_knowledge_base
```

### 向量数据库配置

```ini
CHROMA_PERSIST_DIRECTORY=./chroma_db
EMBEDDING_MODEL_NAME=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### LLM配置

```ini
LLM_API_BASE=http://localhost:8001/v1
LLM_API_KEY=your-llm-api-key
LLM_MODEL_NAME=qwen2-7b-instruct
```

---

## 📚 API文档

完整的API接口文档请参考：

- **接口文档**: `doc/api/api-front-back.md`
- **开发指南**: `doc/api/backEndDev.md`

### 主要接口模块

| 模块 | 前缀 | 说明 |
|------|------|------|
| 用户认证 | `/api/auth` | 登录、登出、修改密码 |
| 个人中心 | `/api/user` | 个人信息管理 |
| 仪表板 | `/api/dashboard` | 统计数据（管理员） |
| 知识库 | `/api/knowledge-base` | 知识库管理 |
| 智能问答 | `/api/chat` | 会话和消息 |
| 搜索 | `/api/search` | 文档搜索 |
| 用户管理 | `/api/admin/users` | 用户管理（管理员） |
| 模型管理 | `/api/models` | 模型配置（管理员） |

### 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| user | user123 | 普通用户 |

---

## 🛠️ 开发指南

### 添加新接口

1. 在 `api/` 目录创建或编辑蓝图文件
2. 使用装饰器实现权限控制
3. 遵循统一响应格式

```python
from flask import Blueprint, request
from utils.auth import require_auth
from utils.response import success_response, error_response

my_bp = Blueprint('my_module', __name__)

@my_bp.route('/my-endpoint', methods=['POST'])
@require_auth
def my_endpoint():
    """接口说明"""
    try:
        data = request.get_json()
        # 业务逻辑
        return success_response({'result': 'success'})
    except Exception as e:
        return error_response(500, '操作失败')
```

### 数据库迁移

使用Flask-Migrate管理数据库变更：

```bash
# 初始化迁移环境（首次）
flask db init

# 生成迁移脚本
flask db migrate -m "描述"

# 应用迁移
flask db upgrade
```

### 日志记录

使用Flask的日志系统：

```python
from flask import current_app

current_app.logger.info('信息日志')
current_app.logger.warning('警告日志')
current_app.logger.error('错误日志')
```

---

## 🧪 测试

### 单元测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_auth.py

# 查看覆盖率
pytest --cov=api tests/
```

### API测试

使用Postman或curl测试接口：

```bash
# 登录获取token
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' \
  | jq -r '.body.token')

# 使用token访问受保护接口
curl -X POST http://localhost:8000/api/user/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## 🚀 生产部署

### 使用Gunicorn

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务（4个工作进程）
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# 或使用配置文件
gunicorn -c gunicorn_config.py app:app
```

### 使用Docker

```bash
# 构建镜像
docker build -t rag-backend .

# 运行容器
docker run -d -p 8000:8000 \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/uploads:/app/uploads \
  --env-file .env \
  rag-backend
```

### 使用Nginx反向代理

```nginx
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.example.com;
    
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 性能优化

### 数据库优化

- 为高频查询字段添加索引
- 使用连接池（已配置）
- 定期清理日志表

### 缓存策略

建议使用Redis缓存热点数据：

```python
# 缓存用户信息
redis_client.setex(f'user:{user_id}', 3600, json.dumps(user_data))

# 缓存知识库列表
redis_client.setex('kb:list', 300, json.dumps(kb_list))
```

### 异步任务

使用Celery处理耗时操作：

- 文档解析和向量化
- 批量数据处理
- 邮件发送

---

## 🔒 安全建议

1. **生产环境必须**:
   - 修改默认密钥 `JWT_SECRET_KEY`
   - 使用HTTPS协议
   - 配置防火墙规则

2. **数据库安全**:
   - 使用强密码
   - 限制远程访问
   - 定期备份数据

3. **日志审计**:
   - 记录所有敏感操作
   - 定期审查日志
   - 监控异常登录

---

## 📈 监控和日志

### 日志文件

日志存储在 `logs/app.log`：

```bash
# 查看实时日志
tail -f logs/app.log

# 搜索错误日志
grep ERROR logs/app.log
```

### 健康检查

```bash
# 检查服务状态
curl http://localhost:8000/health
```

---

## 🤝 贡献指南

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

---

## 📝 更新日志

### v1.0.0 (2025-10-17)

- ✅ 完成基础框架搭建
- ✅ 实现所有API接口
- ✅ 完成数据库设计
- ✅ 集成Chroma向量数据库
- ✅ 完善文档和示例

---

## 📄 许可证

本项目采用 MIT 许可证。

---

## 🆘 常见问题

### Q: 如何重置管理员密码？

```sql
UPDATE users 
SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eWb5wrq6OGFq'
WHERE username = 'admin';
-- 密码重置为: admin123
```

### Q: 数据库连接失败怎么办？

1. 检查MySQL服务是否启动
2. 验证 `.env` 中的数据库配置
3. 确认防火墙规则
4. 查看日志文件 `logs/app.log`

### Q: 如何清空所有数据？

```bash
# 重新初始化数据库
python scripts/init_db.py

# 或手动删除
rm -rf chroma_db/
mysql -u root -p rag_knowledge_base < scripts/create_db.sql
```

---

## 📧 联系方式

- **问题反馈**: [提交Issue](https://github.com/your-repo/issues)
- **技术支持**: support@example.com

---

**祝开发愉快！** 🎉

