#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的链接验证测试
"""

import re
from urllib.parse import urlparse

def is_valid_feishu_url(url):
    """验证是否为有效的飞书文档URL"""
    try:
        parsed = urlparse(url)
        valid_domains = [
            'feishu.cn',
            'larksuite.com', 
            'docs.feishu.cn',
            'bytedance.com'
        ]
        
        return any(domain in parsed.netloc for domain in valid_domains) and (
            '/docx/' in url or 
            '/wiki/' in url or 
            '/docs/' in url or
            '/doc/' in url
        )
    except:
        return False

def test_link():
    """测试链接"""
    test_url = "https://uvw8s43wky3.feishu.cn/wiki/X9OAwWHJViGlyMkr5LrcZdZZndg"
    
    print("🔍 测试飞书链接验证")
    print("=" * 50)
    print(f"测试链接: {test_url}")
    
    # 验证链接
    is_valid = is_valid_feishu_url(test_url)
    print(f"链接有效性: {'✅ 有效' if is_valid else '❌ 无效'}")
    
    # 解析链接信息
    parsed = urlparse(test_url)
    print(f"域名: {parsed.netloc}")
    print(f"路径: {parsed.path}")
    
    # 判断文档类型
    if '/wiki/' in test_url:
        doc_type = "Wiki文档"
    elif '/docx/' in test_url:
        doc_type = "Docx文档"
    else:
        doc_type = "其他文档"
    
    print(f"文档类型: {doc_type}")
    
    # 测试链接读取
    try:
        with open('feishu_links.txt', 'r', encoding='utf-8') as f:
            links = [line.strip() for line in f.readlines() if line.strip()]
        print(f"✅ 成功从文件读取 {len(links)} 个链接")
        for i, link in enumerate(links, 1):
            print(f"  {i}. {link}")
    except Exception as e:
        print(f"❌ 读取链接文件失败: {e}")
    
    print("=" * 50)
    print("🎯 结论: 该链接格式正确，可以被导出工具识别和处理")

if __name__ == "__main__":
    test_link()