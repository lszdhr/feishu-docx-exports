#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书文档导出进度监控工具
提供实时进度显示、错误统计和日志记录功能
"""

import time
import json
import os
from datetime import datetime

class ProgressMonitor:
    def __init__(self, log_file="export_log.json"):
        """
        初始化进度监控器
        
        Args:
            log_file (str): 日志文件路径
        """
        self.log_file = log_file
        self.start_time = None
        self.total_docs = 0
        self.processed_docs = 0
        self.failed_docs = 0
        self.current_doc = ""
        self.errors = []
        
        # 加载之前的日志（如果存在）
        self.load_log()
    
    def load_log(self):
        """加载之前的日志"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    self.errors = log_data.get('errors', [])
                print(f"📋 已加载之前的日志，包含 {len(self.errors)} 条错误记录")
            except:
                self.errors = []
    
    def start_export(self, total_docs):
        """开始导出"""
        self.start_time = time.time()
        self.total_docs = total_docs
        self.processed_docs = 0
        self.failed_docs = 0
        self.current_doc = ""
        
        print(f"\n🚀 开始批量导出 {total_docs} 个文档")
        print("=" * 60)
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
    
    def update_progress(self, doc_url, success=True, error_msg=""):
        """更新进度"""
        self.current_doc = doc_url
        
        if success:
            self.processed_docs += 1
            status = "✅ 成功"
        else:
            self.failed_docs += 1
            status = "❌ 失败"
            
            # 记录错误信息
            error_info = {
                'timestamp': datetime.now().isoformat(),
                'url': doc_url,
                'error': error_msg
            }
            self.errors.append(error_info)
        
        # 计算进度
        total_processed = self.processed_docs + self.failed_docs
        progress_percent = (total_processed / self.total_docs) * 100
        
        # 计算预估剩余时间
        if self.start_time and total_processed > 0:
            elapsed_time = time.time() - self.start_time
            avg_time_per_doc = elapsed_time / total_processed
            remaining_docs = self.total_docs - total_processed
            eta_seconds = remaining_docs * avg_time_per_doc
            eta = f"{int(eta_seconds // 60)}分{int(eta_seconds % 60)}秒"
        else:
            eta = "计算中..."
        
        # 显示进度条
        bar_length = 40
        filled_length = int(bar_length * progress_percent // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        # 清屏并显示进度
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"🚀 飞书文档批量导出进度")
        print("=" * 60)
        print(f"📊 进度: [{bar}] {progress_percent:.1f}%")
        print(f"📄 已处理: {total_processed}/{self.total_docs}")
        print(f"✅ 成功: {self.processed_docs}  ❌ 失败: {self.failed_docs}")
        print(f"⏱️  预计剩余时间: {eta}")
        print(f"📝 当前文档: {doc_url[:50]}...")
        
        if not success and error_msg:
            print(f"⚠️  错误信息: {error_msg}")
        
        print("=" * 60)
    
    def finish_export(self):
        """完成导出"""
        if self.start_time:
            total_time = time.time() - self.start_time
            hours = int(total_time // 3600)
            minutes = int((total_time % 3600) // 60)
            seconds = int(total_time % 60)
            
            print(f"\n🎉 导出完成！")
            print("=" * 60)
            print(f"⏰ 总用时: {hours}小时{minutes}分{seconds}秒")
            print(f"📊 总计: {self.total_docs} 个文档")
            print(f"✅ 成功: {self.processed_docs} 个")
            print(f"❌ 失败: {self.failed_docs} 个")
            
            if self.total_docs > 0:
                success_rate = (self.processed_docs / self.total_docs) * 100
                print(f"📈 成功率: {success_rate:.1f}%")
            
            print("=" * 60)
            
            # 保存日志
            self.save_log()
    
    def save_log(self):
        """保存日志"""
        log_data = {
            'export_time': datetime.now().isoformat(),
            'total_docs': self.total_docs,
            'processed_docs': self.processed_docs,
            'failed_docs': self.failed_docs,
            'errors': self.errors
        }
        
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
            print(f"📋 日志已保存到: {self.log_file}")
        except Exception as e:
            print(f"❌ 保存日志失败: {e}")
    
    def print_error_summary(self):
        """打印错误摘要"""
        if not self.errors:
            print("✅ 没有错误记录")
            return
        
        print(f"\n❌ 错误摘要 (共 {len(self.errors)} 个):")
        print("=" * 60)
        
        for i, error in enumerate(self.errors[-10:], 1):  # 只显示最后10个错误
            timestamp = error['timestamp'][:19].replace('T', ' ')
            print(f"{i}. [{timestamp}] {error['error']}")
            print(f"   URL: {error['url'][:60]}...")
            print()
        
        if len(self.errors) > 10:
            print(f"... 还有 {len(self.errors) - 10} 个错误，详见日志文件")
        
        print("=" * 60)

# 使用示例
if __name__ == "__main__":
    # 模拟导出过程
    monitor = ProgressMonitor()
    monitor.start_export(5)
    
    # 模拟处理文档
    docs = [
        "https://docs.feishu.cn/docx/doc1",
        "https://docs.feishu.cn/docx/doc2", 
        "https://docs.feishu.cn/docx/doc3",
        "https://docs.feishu.cn/docx/doc4",
        "https://docs.feishu.cn/docx/doc5"
    ]
    
    for i, doc in enumerate(docs):
        time.sleep(2)  # 模拟处理时间
        
        if i == 2:  # 模拟一个错误
            monitor.update_progress(doc, False, "网络超时")
        else:
            monitor.update_progress(doc, True)
    
    monitor.finish_export()
    monitor.print_error_summary()