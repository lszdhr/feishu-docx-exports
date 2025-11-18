#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书文档链接收集工具
帮助用户快速收集需要导出的飞书文档链接

使用方法：
1. 手动将飞书文档链接粘贴到links.txt文件中
2. 或使用此工具的交互式收集功能
"""

import os
import re
from urllib.parse import urlparse

class FeishuLinkCollector:
    def __init__(self, output_file="feishu_links.txt"):
        """
        初始化链接收集器
        
        Args:
            output_file (str): 输出文件名
        """
        self.output_file = output_file
        self.links = []
        
    def is_valid_feishu_url(self, url):
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
    
    def load_existing_links(self):
        """加载已存在的链接"""
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    self.links = [line.strip() for line in f.readlines() if line.strip()]
                print(f"✅ 已加载 {len(self.links)} 个现有链接")
                return True
            except Exception as e:
                print(f"❌ 加载现有链接失败: {e}")
                return False
        return False
    
    def add_link(self, url):
        """添加单个链接"""
        if not url.strip():
            return False
            
        if not self.is_valid_feishu_url(url):
            print(f"⚠️  无效的飞书文档URL: {url}")
            return False
            
        if url in self.links:
            print(f"⚠️  链接已存在: {url}")
            return False
            
        self.links.append(url)
        print(f"✅ 已添加链接: {url}")
        return True
    
    def add_links_from_text(self, text):
        """从文本中批量添加链接"""
        # 使用正则表达式提取URL
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        found_urls = re.findall(url_pattern, text)
        
        added_count = 0
        for url in found_urls:
            if self.add_link(url):
                added_count += 1
        
        print(f"📊 从文本中添加了 {added_count} 个有效链接")
        return added_count
    
    def remove_duplicates(self):
        """去除重复链接"""
        original_count = len(self.links)
        self.links = list(dict.fromkeys(self.links))  # 保持顺序的去重
        removed_count = original_count - len(self.links)
        
        if removed_count > 0:
            print(f"🗑️  移除了 {removed_count} 个重复链接")
        
        return removed_count
    
    def save_links(self):
        """保存链接到文件"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                for link in self.links:
                    f.write(link + '\n')
            
            print(f"💾 已保存 {len(self.links)} 个链接到 {self.output_file}")
            return True
        except Exception as e:
            print(f"❌ 保存链接失败: {e}")
            return False
    
    def show_links(self):
        """显示所有链接"""
        if not self.links:
            print("📝 暂无链接")
            return
        
        print(f"\n📋 当前共有 {len(self.links)} 个链接:")
        print("=" * 60)
        
        for i, link in enumerate(self.links, 1):
            print(f"{i:2d}. {link}")
        
        print("=" * 60)
    
    def interactive_collect(self):
        """交互式收集链接"""
        print("🚀 飞书文档链接收集工具")
        print("=" * 40)
        
        # 加载现有链接
        self.load_existing_links()
        
        while True:
            print("\n📋 请选择操作:")
            print("1. 添加单个链接")
            print("2. 从剪贴板批量添加")
            print("3. 从文本文件批量导入")
            print("4. 查看所有链接")
            print("5. 去除重复链接")
            print("6. 删除指定链接")
            print("7. 保存并退出")
            print("0. 退出（不保存）")
            
            choice = input("\n请输入选项 (0-7): ").strip()
            
            if choice == '1':
                url = input("请输入飞书文档链接: ").strip()
                self.add_link(url)
                
            elif choice == '2':
                try:
                    import pyperclip
                    text = pyperclip.paste()
                    added = self.add_links_from_text(text)
                    if added == 0:
                        print("⚠️  剪贴板中没有找到有效的飞书链接")
                except ImportError:
                    print("❌ 需要安装pyperclip库: pip install pyperclip")
                except:
                    print("❌ 无法访问剪贴板")
                    
            elif choice == '3':
                file_path = input("请输入文本文件路径: ").strip()
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text = f.read()
                        self.add_links_from_text(text)
                    except Exception as e:
                        print(f"❌ 读取文件失败: {e}")
                else:
                    print("❌ 文件不存在")
                    
            elif choice == '4':
                self.show_links()
                
            elif choice == '5':
                self.remove_duplicates()
                
            elif choice == '6':
                self.show_links()
                try:
                    index = int(input("\n请输入要删除的链接序号: ")) - 1
                    if 0 <= index < len(self.links):
                        removed = self.links.pop(index)
                        print(f"🗑️  已删除: {removed}")
                    else:
                        print("❌ 序号无效")
                except ValueError:
                    print("❌ 请输入有效的数字")
                    
            elif choice == '7':
                self.save_links()
                break
                
            elif choice == '0':
                print("👋 退出（不保存更改）")
                break
                
            else:
                print("❌ 无效选项，请重新选择")

def create_sample_links_file():
    """创建示例链接文件"""
    sample_content = """# 飞书文档链接示例
# 每行一个链接，以#开头的行为注释

# 主文档
https://docs.feishu.cn/docx/xxxxxxxx

# 子文档
https://docs.feishu.cn/docx/yyyyyyyy
https://docs.feishu.cn/docx/zzzzzzzz

# 知识库文档
https://your-domain.feishu.cn/wiki/xxxxxxxx
"""
    
    with open("feishu_links.txt", 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print("📝 已创建示例链接文件: feishu_links.txt")
    print("请编辑此文件，添加您的飞书文档链接")

def main():
    """主函数"""
    print("🚀 飞书文档链接收集工具")
    print("=" * 40)
    
    # 检查是否已存在链接文件
    if not os.path.exists("feishu_links.txt"):
        print("📝 未找到链接文件，创建示例文件...")
        create_sample_links_file()
        print("\n💡 提示：")
        print("1. 编辑 feishu_links.txt 文件")
        print("2. 或使用交互式收集工具")
        print("3. 每行一个飞书文档链接")
        
        choice = input("\n是否使用交互式收集工具？(y/n): ").strip().lower()
        if choice != 'y':
            return
    
    # 启动交互式收集
    collector = FeishuLinkCollector()
    collector.interactive_collect()

if __name__ == "__main__":
    main()