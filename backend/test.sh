#!/bin/bash

# 测试脚本 - 验证所有功能

echo "========================================="
echo "安佑预混料每日行情 - 功能测试"
echo "========================================="
echo ""

# 测试计数器
PASS=0
FAIL=0

# 测试函数
test_case() {
    local name=$1
    local command=$2

    echo "🧪 测试: $name"
    if eval "$command" > /dev/null 2>&1; then
        echo "✅ 通过"
        ((PASS++))
    else
        echo "❌ 失败"
        ((FAIL++))
    fi
    echo ""
}

# 1. 检查Python环境
test_case "Python环境检查" "python3 --version"

# 2. 检查openpyxl依赖
test_case "openpyxl依赖检查" "python3 -c 'import openpyxl'"

# 3. 检查schedule依赖
test_case "schedule依赖检查" "python3 -c 'import schedule'"

# 4. 检查生成脚本
test_case "文档生成脚本检查" "test -f generate_weekly_documents.py"

# 5. 检查下载服务器
test_case "下载服务器脚本检查" "test -f download_server.py"

# 6. 检查调度器
test_case "定时任务调度器检查" "test -f scheduler.py"

# 7. 检查前端页面
test_case "前端页面检查" "test -f profile.html"

# 8. 检查下载服务器是否运行
test_case "下载服务器运行检查" "curl -s -o /dev/null http://localhost:5001/api/documents"

# 9. 测试API接口
echo "🧪 测试: API接口响应"
API_RESPONSE=$(curl -s http://localhost:5001/api/documents)
if echo "$API_RESPONSE" | grep -q '"success"' && echo "$API_RESPONSE" | grep -q '"documents"'; then
    echo "✅ 通过"
    ((PASS++))
else
    echo "❌ 失败"
    ((FAIL++))
fi
echo ""

# 10. 检查生成的Excel文件
echo "🧪 测试: Excel文件检查"
EXCEL_FILE=$(ls -1 本周行情数据_*.xlsx 2>/dev/null | head -1)
if [ -n "$EXCEL_FILE" ] && [ -f "$EXCEL_FILE" ]; then
    echo "✅ 通过"
    ((PASS++))
else
    echo "❌ 失败"
    ((FAIL++))
fi
echo ""

# 11. 检查生成的TXT文件
test_case "TXT文件检查" "test -f 每周周报_*.txt"

# 12. 测试Excel下载
echo "🧪 测试: Excel文档下载"
if curl -s -o /tmp/test_excel.xlsx "http://localhost:5001/download/本周行情数据_2026-01-12至2026-01-18.xlsx" && [ -s /tmp/test_excel.xlsx ]; then
    echo "✅ 通过"
    ((PASS++))
else
    echo "❌ 失败"
    ((FAIL++))
fi
echo ""

# 13. 测试TXT下载
echo "🧪 测试: TXT文档下载"
if curl -s -o /tmp/test_report.txt "http://localhost:5001/download/每周周报_2026-01-12至2026-01-18.txt" && grep -q "安佑预混料市场周报" /tmp/test_report.txt; then
    echo "✅ 通过"
    ((PASS++))
else
    echo "❌ 失败"
    ((FAIL++))
fi
echo ""

# 打印测试结果
echo "========================================="
echo "测试结果汇总"
echo "========================================="
echo ""
echo "总计: $((PASS + FAIL)) 项"
echo "✅ 通过: $PASS 项"
echo "❌ 失败: $FAIL 项"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "🎉 所有测试通过！系统运行正常。"
    exit 0
else
    echo "⚠️  有 $FAIL 项测试失败，请检查系统配置。"
    exit 1
fi
