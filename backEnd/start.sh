#!/bin/bash

echo "===================================="
echo " RAG知识问答系统 - 后端服务启动"
echo "===================================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "虚拟环境不存在，正在创建..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "警告: .env文件不存在，从env.example复制..."
    cp env.example .env
    echo "请编辑.env文件配置数据库连接后再次运行此脚本"
    echo "vi .env"
    exit 1
fi

# 安装依赖
echo "检查Python依赖..."
pip install -q -r requirements.txt

# 检查数据库连接
echo "检查数据库连接..."
python3 -c "
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '')
    )
    print('✅ 数据库连接成功')
    conn.close()
except Exception as e:
    print(f'❌ 数据库连接失败: {e}')
    print('请检查.env文件中的数据库配置')
    exit(1)
"

if [ $? -ne 0 ]; then
    exit 1
fi

# 检查数据库是否已初始化
echo "检查数据库初始化状态..."
INIT_CHECK=$(python3 -c "
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'rag_knowledge_base')
    )
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    print(len(tables))
except:
    print(0)
")

if [ "$INIT_CHECK" -eq "0" ]; then
    echo ""
    echo "⚠️  数据库未初始化，是否立即初始化？(yes/no)"
    read -p "请输入: " CONFIRM
    if [ "$CONFIRM" == "yes" ]; then
        python scripts/init_db.py
        if [ $? -ne 0 ]; then
            echo "❌ 数据库初始化失败"
            exit 1
        fi
    else
        echo "请手动运行: python scripts/init_db.py"
        exit 1
    fi
fi

# 设置环境变量
export FLASK_APP=app.py
export FLASK_ENV=development

# 启动服务
echo ""
echo "===================================="
echo " 🚀 正在启动后端服务..."
echo "===================================="
echo "访问地址: http://localhost:8000"
echo "健康检查: http://localhost:8000/health"
echo "API文档: doc/api/api-front-back.md"
echo ""
echo "测试账号:"
echo "  管理员: admin / admin123"
echo "  用户: user / user123"
echo ""
echo "按 Ctrl+C 停止服务"
echo "===================================="
echo ""

python app.py

