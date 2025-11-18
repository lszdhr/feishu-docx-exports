#!/bin/bash

# 飞书文档批量导出工具安装脚本

echo "🚀 飞书文档批量导出工具安装程序"
echo "=================================="

# 检查Python版本
echo "📋 检查Python版本..."
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ $python_version"
else
    echo "❌ 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

# 检查pip
echo "📋 检查pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 已安装"
else
    echo "❌ 未找到pip3，请先安装pip"
    exit 1
fi

# 安装依赖
echo "📦 安装Python依赖包..."
pip3 install -r requirements.txt

if [[ $? -eq 0 ]]; then
    echo "✅ 依赖包安装成功"
else
    echo "❌ 依赖包安装失败"
    exit 1
fi

# 检查Chrome浏览器
echo "📋 检查Chrome浏览器..."
if command -v google-chrome &> /dev/null; then
    echo "✅ Chrome浏览器已安装"
elif command -v chromium-browser &> /dev/null; then
    echo "✅ Chromium浏览器已安装"
elif [[ -d "/Applications/Google Chrome.app" ]]; then
    echo "✅ Chrome浏览器已安装"
else
    echo "⚠️  未找到Chrome浏览器，请手动安装"
    echo "   下载地址: https://www.google.com/chrome/"
fi

# 创建示例链接文件
if [[ ! -f "feishu_links.txt" ]]; then
    echo "📝 创建示例链接文件..."
    python3 link_collector.py
fi

# 设置脚本权限
echo "🔧 设置脚本权限..."
chmod +x *.py

echo ""
echo "🎉 安装完成！"
echo "=================================="
echo "📖 使用说明："
echo "1. 运行 'python3 link_collector.py' 收集文档链接"
echo "2. 安装飞书文档助手Chrome插件"
echo "3. 运行 'python3 feishu_batch_export.py' 开始导出"
echo ""
echo "📚 详细文档请查看 README.md"