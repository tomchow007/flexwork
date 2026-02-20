#!/bin/bash
echo "🚀 启动灵活用工平台 Web 版"
echo "================================"

cd "$(dirname "$0")"

# 检查 web_app.py
if [ ! -f "web_app.py" ]; then
    echo "❌ 错误: web_app.py 不存在"
    exit 1
fi

# 设置 PATH
export PATH="$PATH:/Users/zhoutao/Library/Python/3.9/bin"

echo "正在启动 Streamlit 服务..."
echo "浏览器将自动打开..."
echo ""
echo "按 Ctrl+C 停止服务"
echo "================================"
echo ""

# 启动 Streamlit
python3 -m streamlit run web_app.py --server.port 8501
