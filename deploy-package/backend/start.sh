#!/bin/bash

# 安佑预混料每日行情 - 一键启动脚本

echo "========================================="
echo "安佑预混料每日行情 - 文档自动生成系统"
echo "========================================="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到Python3环境"
    exit 1
fi

echo "✅ Python环境检查通过"

# 检查依赖
echo ""
echo "📦 检查依赖..."
python3 -c "import openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  缺少openpyxl，正在安装..."
    pip install openpyxl
fi

python3 -c "import schedule" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  缺少schedule，正在安装..."
    pip install schedule
fi

echo "✅ 依赖检查通过"

# 停止旧进程
echo ""
echo "🛑 停止旧进程..."
pkill -f download_server.py 2>/dev/null
pkill -f scheduler.py 2>/dev/null
sleep 1
echo "✅ 旧进程已停止"

# 生成文档（首次运行）
echo ""
echo "📄 生成文档..."
python3 generate_weekly_documents.py
if [ $? -eq 0 ]; then
    echo "✅ 文档生成成功"
else
    echo "❌ 文档生成失败"
    exit 1
fi

# 启动下载服务器
echo ""
echo "🚀 启动下载服务器..."
python3 download_server.py > download_server.log 2>&1 &
SERVER_PID=$!
sleep 2

# 检查服务器是否正常启动
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ 下载服务器启动成功 (PID: $SERVER_PID)"
    echo "   服务地址: http://localhost:5001"
else
    echo "❌ 下载服务器启动失败"
    cat download_server.log
    exit 1
fi

# 启动定时任务
echo ""
echo "⏰ 启动定时任务调度器..."
python3 scheduler.py > scheduler.log 2>&1 &
SCHEDULER_PID=$!
sleep 2

# 检查调度器是否正常启动
if ps -p $SCHEDULER_PID > /dev/null; then
    echo "✅ 定时任务调度器启动成功 (PID: $SCHEDULER_PID)"
    echo "   执行时间: 每周日中午12:00"
else
    echo "❌ 定时任务调度器启动失败"
    cat scheduler.log
    exit 1
fi

# 打印服务信息
echo ""
echo "========================================="
echo "✅ 所有服务启动成功！"
echo "========================================="
echo ""
echo "服务信息："
echo "  - 下载服务器: http://localhost:5001 (PID: $SERVER_PID)"
echo "  - 定时任务调度器: 运行中 (PID: $SCHEDULER_PID)"
echo ""
echo "可用API："
echo "  - GET http://localhost:5001/api/documents"
echo "  - GET http://localhost:5001/download/<filename>"
echo ""
echo "日志文件："
echo "  - 下载服务器: download_server.log"
echo "  - 定时任务: scheduler.log"
echo ""
echo "提示："
echo "  - 打开 profile.html 可以下载文档"
echo "  - 按 Ctrl+C 停止所有服务"
echo "========================================="
echo ""

# 等待用户中断
trap "echo ''; echo '🛑 正在停止所有服务...'; kill $SERVER_PID $SCHEDULER_PID 2>/dev/null; echo '✅ 所有服务已停止'; exit 0" INT TERM

while true; do
    sleep 1
done
