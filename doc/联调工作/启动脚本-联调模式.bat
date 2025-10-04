@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   RAG 前端 - 联调模式启动
echo ========================================
echo.
echo 正在检查配置...
echo.

REM 检查 Node.js
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

REM 检查 node_modules
if not exist "node_modules\" (
    echo [提示] 首次运行，正在安装依赖...
    echo.
    call npm install
    if %errorlevel% neq 0 (
        echo.
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo [配置] 检查 Mock 数据配置...
findstr /C:"USE_MOCK = false" src\utils\env.js >nul
if %errorlevel% neq 0 (
    echo [警告] 当前使用 Mock 数据模式
    echo.
    echo 要连接真实后端，请修改 src\utils\env.js 第19行:
    echo   export const USE_MOCK = false
    echo.
    choice /C YN /M "是否继续启动（Mock模式）"
    if errorlevel 2 exit /b 0
) else (
    echo [✓] 已配置连接真实后端
)

echo.
echo [配置] 后端地址: http://localhost:8000
echo [提示] 如需修改，请编辑 vite.config.js
echo.
echo ========================================
echo.
echo [启动] 正在启动前端开发服务器...
echo.
echo 前端地址: http://localhost:5173
echo.
echo 按 Ctrl+C 停止服务
echo.
echo ========================================
echo.

call npm run dev

pause

