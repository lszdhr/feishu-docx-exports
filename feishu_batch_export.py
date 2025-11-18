#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书文档批量导出工具
支持个人免费用户批量导出飞书云文档为PDF格式

需要安装：
pip install selenium pyautogui webdriver-manager

使用前请确保：
1. 安装Chrome浏览器
2. 安装飞书文档助手Chrome插件
3. 准备好文档链接列表文件
"""

import time
import os
import sys
import json
import pyautogui
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# 导入进度监控器
from progress_monitor import ProgressMonitor

class FeishuBatchExporter:
    def __init__(self, links_file, download_dir, delay=3):
        """
        初始化批量导出工具
        
        Args:
            links_file (str): 包含文档链接的文本文件路径
            download_dir (str): 下载目录路径
            delay (int): 每个操作之间的延迟时间（秒）
        """
        self.links_file = links_file
        self.download_dir = download_dir
        self.delay = delay
        self.driver = None
        self.processed_links = []
        self.failed_links = []
        
        # 初始化进度监控器
        self.monitor = ProgressMonitor()
        
        # 确保下载目录存在
        os.makedirs(download_dir, exist_ok=True)
        
    def setup_chrome_driver(self):
        """设置Chrome驱动"""
        chrome_options = Options()
        
        # 设置下载目录
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # 设置窗口大小
        chrome_options.add_argument("--window-size=1920,1080")
        
        # 禁用一些可能干扰的功能
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # 允许扩展（为了使用飞书插件）
        chrome_options.add_argument("--enable-extensions")
        
        try:
            # 自动下载并安装ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Chrome驱动启动成功")
            return True
        except WebDriverException as e:
            print(f"❌ Chrome驱动启动失败: {e}")
            print("💡 请确保已安装Chrome浏览器")
            return False
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return False
    
    def load_document_links(self):
        """从文件加载文档链接"""
        try:
            with open(self.links_file, 'r', encoding='utf-8') as f:
                links = [line.strip() for line in f.readlines() if line.strip()]
            
            print(f"✅ 成功加载 {len(links)} 个文档链接")
            return links
        except Exception as e:
            print(f"❌ 加载链接文件失败: {e}")
            return []
    
    def export_single_document(self, url, doc_index, total_docs):
        """
        导出单个文档
        
        Args:
            url (str): 文档URL
            doc_index (int): 当前文档索引
            total_docs (int): 总文档数量
        """
        try:
            # 更新进度显示
            self.monitor.update_progress(url, False, "正在处理...")
            
            # 访问文档页面
            self.driver.get(url)
            
            # 等待页面加载完成
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 等待页面完全加载
            time.sleep(self.delay)
            
            # 尝试找到并点击导出按钮
            export_success = self.click_export_button()
            
            if export_success:
                # 处理可能的弹窗
                self.handle_download_dialog()
                
                # 更新进度为成功
                self.monitor.update_progress(url, True)
                self.processed_links.append(url)
            else:
                # 更新进度为失败
                self.monitor.update_progress(url, False, "无法找到导出按钮")
                self.failed_links.append(url)
                
        except TimeoutException as e:
            self.monitor.update_progress(url, False, f"页面加载超时: {str(e)}")
            self.failed_links.append(url)
        except Exception as e:
            self.monitor.update_progress(url, False, f"处理出错: {str(e)}")
            self.failed_links.append(url)
    
    def click_export_button(self):
        """点击导出按钮"""
        try:
            # 方法1: 尝试通过快捷键触发导出
            # Ctrl+P 打印，然后选择保存为PDF
            modifier_key = 'command' if sys.platform == 'darwin' else 'ctrl'
            pyautogui.hotkey(modifier_key, 'p')
            time.sleep(2)
            
            # 在打印对话框中按回车保存
            pyautogui.press('enter')
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"快捷键导出失败，尝试其他方法: {e}")
            
            try:
                # 方法2: 尝试查找并点击页面上的导出按钮
                # 这里需要根据实际的飞书页面结构来调整
                export_selectors = [
                    "//button[contains(text(), '导出')]",
                    "//button[contains(@title, '导出')]",
                    "//div[contains(@class, 'export')]",
                    "//span[contains(text(), '导出')]",
                    "//button[contains(@aria-label, '导出')]"
                ]
                
                for selector in export_selectors:
                    try:
                        export_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        export_button.click()
                        time.sleep(2)
                        return True
                    except:
                        continue
                        
            except Exception as e2:
                print(f"按钮点击方法也失败: {e2}")
                
            return False
    
    def handle_download_dialog(self):
        """处理下载对话框"""
        try:
            # 等待可能的下载对话框出现
            time.sleep(2)
            
            # 尝试按回车键确认下载
            pyautogui.press('enter')
            time.sleep(1)
            
            # 如果还有对话框，再试一次
            pyautogui.press('enter')
            
        except Exception as e:
            print(f"处理下载对话框时出错: {e}")
    
    def export_all_documents(self):
        """批量导出所有文档"""
        links = self.load_document_links()
        if not links:
            print("❌ 没有找到可导出的文档链接")
            return
        
        print(f"🚀 准备批量导出 {len(links)} 个文档")
        print(f"📁 下载目录: {self.download_dir}")
        
        # 初始化进度监控
        self.monitor.start_export(len(links))
        
        # 初始化Chrome驱动
        if not self.setup_chrome_driver():
            print("❌ 无法启动Chrome驱动，导出终止")
            return
        
        try:
            # 逐个处理文档
            for i, link in enumerate(links, 1):
                self.export_single_document(link, i, len(links))
                
                # 每处理10个文档后稍作休息
                if i % 10 == 0:
                    print(f"🔄 已处理 {i} 个文档，休息30秒...")
                    time.sleep(30)
                else:
                    # 正常间隔
                    time.sleep(self.delay)
            
            # 完成导出
            self.monitor.finish_export()
            
            # 输出结果统计
            self.print_export_summary()
            
        except KeyboardInterrupt:
            print("\n⚠️  用户中断了导出过程")
            self.monitor.finish_export()
        except Exception as e:
            print(f"\n❌ 导出过程中发生严重错误: {e}")
            self.monitor.finish_export()
        finally:
            # 关闭浏览器
            if self.driver:
                self.driver.quit()
                print("🔒 Chrome浏览器已关闭")
    
    def print_export_summary(self):
        """打印导出结果统计"""
        print("\n" + "="*50)
        print("📊 导出结果统计")
        print("="*50)
        print(f"✅ 成功导出: {len(self.processed_links)} 个文档")
        print(f"❌ 导出失败: {len(self.failed_links)} 个文档")
        
        # 显示错误摘要
        self.monitor.print_error_summary()
        
        if self.failed_links:
            print("\n❌ 失败的文档链接:")
            for i, link in enumerate(self.failed_links, 1):
                print(f"  {i}. {link}")
            
            # 保存失败链接到文件
            failed_file = os.path.join(self.download_dir, "failed_links.txt")
            with open(failed_file, 'w', encoding='utf-8') as f:
                for link in self.failed_links:
                    f.write(link + '\n')
            print(f"\n💾 失败链接已保存到: {failed_file}")
        
        # 创建导出报告
        self.create_export_report()
        
        print(f"\n📁 所有导出的文件都在: {self.download_dir}")
        print("="*50)
    
    def create_export_report(self):
        """创建导出报告"""
        report = {
            'export_time': datetime.now().isoformat(),
            'total_docs': len(self.processed_links) + len(self.failed_links),
            'successful': len(self.processed_links),
            'failed': len(self.failed_links),
            'download_directory': self.download_dir,
            'processed_links': self.processed_links,
            'failed_links': self.failed_links
        }
        
        report_file = os.path.join(self.download_dir, "export_report.json")
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"📋 导出报告已保存到: {report_file}")
        except Exception as e:
            print(f"❌ 保存导出报告失败: {e}")

def main():
    """主函数"""
    print("🚀 飞书文档批量导出工具")
    print("="*30)
    
    # 配置参数
    links_file = "feishu_links.txt"  # 包含文档链接的文件
    download_dir = "./feishu_exports"  # 下载目录
    delay = 3  # 操作间隔时间（秒）
    
    # 检查链接文件是否存在
    if not os.path.exists(links_file):
        print(f"❌ 链接文件 '{links_file}' 不存在")
        print("请先创建该文件，并在其中填入飞书文档链接（每行一个）")
        return
    
    # 创建导出器实例
    exporter = FeishuBatchExporter(links_file, download_dir, delay)
    
    # 开始批量导出
    exporter.export_all_documents()
    
    print("\n🎉 批量导出完成！")

if __name__ == "__main__":
    main()