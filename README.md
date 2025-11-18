# 飞书文档批量导出工具

（仓库名：`feishu-docx-exports`）专为个人免费用户设计的飞书云文档批量导出解决方案，支持将90+文档一次性导出为PDF格式。

## ✨ 功能特点

- 🚀 **批量导出**：一次性处理90个文档，无需手动操作
- 📄 **PDF格式**：导出的PDF保持完整格式，文字可搜索、可复制
- 📊 **实时监控**：显示导出进度、成功率、预计剩余时间
- 🔄 **错误恢复**：自动记录失败文档，支持重新导出
- 📁 **目录保持**：自动整理导出文件，便于管理
- 🆓 **完全免费**：无需企业版账号，个人用户即可使用

## 📋 系统要求

- Python 3.7+
- Chrome浏览器
- 稳定的网络连接

## 🚀 快速开始

### 第一步：安装依赖

```bash
pip install -r requirements.txt
```

### 第二步：安装Chrome插件

1. 打开Chrome浏览器
2. 访问Chrome应用商店，搜索"飞书文档助手"
3. 点击"添加到Chrome"
4. 配置插件默认导出格式为PDF

详细安装说明请参考：[Chrome插件安装指南](chrome_extension_guide.md)

### 第三步：准备文档链接

1. 运行链接收集工具：
```bash
python link_collector.py
```

2. 按照提示添加您的飞书文档链接
3. 保存后会生成`feishu_links.txt`文件

### 第四步：开始批量导出

```bash
python feishu_batch_export.py
```

## 📁 文件说明

| 文件名 | 说明 |
|--------|------|
| `feishu_batch_export.py` | 主要的批量导出脚本 |
| `link_collector.py` | 文档链接收集工具 |
| `progress_monitor.py` | 进度监控和日志记录 |
| `chrome_extension_guide.md` | Chrome插件安装指南 |
| `requirements.txt` | Python依赖包列表 |
| `feishu_links.txt` | 文档链接列表（需要手动创建） |

## 🔧 配置选项

### 自定义导出参数

编辑`feishu_batch_export.py`文件中的`main()`函数：

```python
# 配置参数
links_file = "feishu_links.txt"  # 链接文件路径
download_dir = "./feishu_exports"  # 下载目录
delay = 3  # 操作间隔时间（秒）
```

### 调整导出策略

- **delay参数**：网络较慢时可适当增加延迟时间
- **批量大小**：脚本每处理10个文档会自动休息30秒
- **重试机制**：失败的文档会记录在`failed_links.txt`中

## 📊 导出结果

导出完成后，会在下载目录中生成：

- 所有PDF文档文件
- `export_report.json`：详细的导出报告
- `failed_links.txt`：失败文档列表（如有）
- `export_log.json`：完整的操作日志

## ⚠️ 注意事项

1. **权限要求**：确保您对所有文档有查看权限
2. **网络稳定**：导出过程中请保持网络连接稳定
3. **不要操作**：导出时请勿操作浏览器窗口
4. **时间预估**：90个文档预计需要2-3小时

## 🛠️ 故障排除

### 常见问题

**Q: Chrome驱动启动失败**
A: 请确保已安装Chrome浏览器，或手动下载ChromeDriver

**Q: 插件无法导出**
A: 检查插件是否正确安装，尝试重新安装插件

**Q: 部分文档导出失败**
A: 失败的文档会记录在`failed_links.txt`中，可手动处理

**Q: 导出速度很慢**
A: 检查网络连接，或在网络空闲时段运行

### 日志分析

查看`export_log.json`文件了解详细的错误信息：

```bash
# 查看最近的错误
python -c "
import json
with open('feishu_exports/export_log.json', 'r', encoding='utf-8') as f:
    log = json.load(f)
    for error in log['errors'][-5:]:
        print(f\"{error['timestamp']}: {error['error']}\")
"
```

## 🔄 重新导出失败的文档

如果部分文档导出失败，可以：

1. 编辑`failed_links.txt`，只保留需要重新导出的链接
2. 重命名为`feishu_links.txt`
3. 重新运行导出脚本

## 📈 性能优化建议

1. **网络优化**：使用有线网络连接
2. **系统资源**：关闭不必要的程序
3. **批量策略**：大量文档可分批导出
4. **时段选择**：在网络负载较低时运行

## 🤝 技术支持

如遇到问题：

1. 检查本文档的故障排除部分
2. 查看日志文件了解具体错误
3. 确认所有依赖都已正确安装

## 📝 更新日志

### v1.0.0 (2024-01-01)
- ✅ 初始版本发布
- ✅ 支持批量PDF导出
- ✅ 实时进度监控
- ✅ 错误处理和恢复

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

---

**免责声明**：本工具仅供个人学习使用，请遵守飞书服务条款，仅导出您有权限的文档。
