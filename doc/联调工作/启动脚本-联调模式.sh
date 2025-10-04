#!/bin/bash

echo ""
echo "========================================"
echo "  RAG 前端 - 联调模式启动"
echo "========================================"
echo ""
echo "正在检查配置..."
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "[错误] 未检测到 Node.js，请先安装 Node.js"
    echo "下载地址: https://nodejs.org/"
    exit 1
fi

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "[提示] 首次运行，正在安装依赖..."
    echo ""
    npm install
    if [ $? -ne 0 ]; then
        echo ""
        echo "[错误] 依赖安装失败"
        exit 1
    fi
fi

echo "[配置] 检查 Mock 数据配置..."
if ! grep -q "USE_MOCK = false" src/utils/env.js; then
    echo "[警告] 当前使用 Mock 数据模式"
    echo ""
    echo "要连接真实后端，请修改 src/utils/env.js 第19行:"
    echo "  export const USE_MOCK = false"
    echo ""
    read -p "是否继续启动（Mock模式）？(y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
else
    echo "[✓] 已配置连接真实后端"
fi

echo ""
echo "[配置] 后端地址: http://localhost:8000"
echo "[提示] 如需修改，请编辑 vite.config.js"
echo ""
echo "========================================"
echo ""
echo "[启动] 正在启动前端开发服务器..."
echo ""
echo "前端地址: http://localhost:5173"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""
echo "========================================"
echo ""

npm run dev

