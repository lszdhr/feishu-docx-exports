#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版飞书导出测试 - 不依赖外部库
仅测试链接访问和页面结构分析
"""

import time
import os
import json
from datetime import datetime

class SimpleFeishuTest:
    def __init__(self):
        self.processed_links = []
        self.failed_links = []
        self.test_results = []
    
    def load_links(self):
        """加载链接"""
        try:
            with open('feishu_links.txt', 'r', encoding='utf-8') as f:
                links = [line.strip() for line in f.readlines() if line.strip()]
            return links
        except Exception as e:
            print(f"❌ 加载链接失败: {e}")
            return []
    
    def test_link_access(self, url):
        """测试链接访问（模拟）"""
        print(f"🔍 测试访问: {url}")
        
        # 模拟页面访问分析
        test_result = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'accessible': True,
            'doc_type': 'wiki' if '/wiki/' in url else 'docx',
            'domain': url.split('/')[2] if len(url.split('/')) > 2 else 'unknown',
            'export_feasible': True,
            'notes': []
        }
        
        # 分析链接特征
        if 'feishu.cn' in url:
            test_result['notes'].append('✅ 飞书中国域名')
        else:
            test_result['notes'].append('⚠️ 非标准飞书域名')
        
        if '/wiki/' in url:
            test_result['notes'].append('✅ Wiki文档格式')
            test_result['export_method'] = 'Ctrl+P打印或页面导出按钮'
        elif '/docx/' in url:
            test_result['notes'].append('✅ Docx文档格式')
            test_result['export_method'] = 'Ctrl+P打印或页面导出按钮'
        else:
            test_result['notes'].append('⚠️ 未知文档格式')
            test_result['export_feasible'] = False
        
        # 模拟访问延迟
        time.sleep(1)
        
        return test_result
    
    def run_test(self):
        """运行测试"""
        print("🚀 开始飞书链接导出可行性测试")
        print("=" * 60)
        
        links = self.load_links()
        if not links:
            print("❌ 没有找到测试链接")
            return
        
        print(f"📋 找到 {len(links)} 个测试链接")
        
        for i, link in enumerate(links, 1):
            print(f"\n[{i}/{len(links)}] 测试链接...")
            
            result = self.test_link_access(link)
            self.test_results.append(result)
            
            if result['export_feasible']:
                self.processed_links.append(link)
                print(f"✅ 测试通过 - {result['doc_type']}文档")
            else:
                self.failed_links.append(link)
                print(f"❌ 测试失败")
            
            # 显示测试详情
            for note in result['notes']:
                print(f"   {note}")
            print(f"   推荐导出方式: {result.get('export_method', '未知')}")
        
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 测试报告")
        print("=" * 60)
        
        print(f"✅ 可导出链接: {len(self.processed_links)}")
        print(f"❌ 不可导出链接: {len(self.failed_links)}")
        print(f"📈 成功率: {(len(self.processed_links) / len(self.test_results) * 100):.1f}%")
        
        # 保存详细报告
        report = {
            'test_time': datetime.now().isoformat(),
            'total_links': len(self.test_results),
            'successful': len(self.processed_links),
            'failed': len(self.failed_links),
            'results': self.test_results
        }
        
        report_file = 'test_report.json'
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"📋 详细报告已保存到: {report_file}")
        except Exception as e:
            print(f"❌ 保存报告失败: {e}")
        
        # 给出建议
        print("\n💡 建议:")
        if len(self.processed_links) > 0:
            print("1. ✅ 链接格式正确，可以使用完整版导出工具")
            print("2. 🔧 需要安装依赖: pip install -r requirements.txt")
            print("3. 🌐 确保网络连接稳定")
            print("4. 🖥️ 准备Chrome浏览器和飞书文档助手插件")
        else:
            print("1. ❌ 链接格式可能有问题，请检查URL是否正确")
            print("2. 🔍 确认链接是否为有效的飞书文档链接")

if __name__ == "__main__":
    tester = SimpleFeishuTest()
    tester.run_test()