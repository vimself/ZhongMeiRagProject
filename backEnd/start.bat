@echo off
chcp 65001 >nul
echo ====================================
echo  RAG知识问答系统 - 后端服务启动
echo ====================================
echo.

REM 检查虚拟环境
if not exist "venv\" (
    echo 虚拟环境不存在，正在创建...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 检查.env文件
if not exist ".env" (
    echo 警告: .env文件不存在，从env.example复制...
    copy env.example .env
    echo 请编辑.env文件配置数据库连接后再次运行此脚本
    echo notepad .env
    pause
    exit /b 1
)

REM 安装依赖
echo 检查Python依赖...
pip install -q -r requirements.txt

REM 设置环境变量
set FLASK_APP=app.py
set FLASK_ENV=development

REM 启动服务
echo.
echo ====================================
echo  🚀 正在启动后端服务...
echo ====================================
echo 访问地址: http://localhost:8000
echo 健康检查: http://localhost:8000/health
echo API文档: doc\api\api-front-back.md
echo.
echo 测试账号:
echo   管理员: admin / admin123
echo   用户: user / user123
echo.
echo 按 Ctrl+C 停止服务
echo ====================================
echo.

python app.py

pause

