# Project Overview

This directory contains a comprehensive Feishu (Lark) document batch export tool specifically designed for individual free users. The solution enables batch exporting of 90+ Feishu cloud documents to PDF format without requiring enterprise-level permissions.

## Project Type

This is a Python-based automation project that combines web scraping, browser automation, and progress monitoring to solve the document export limitation for personal Feishu users.

## Key Technologies

- **Python 3.7+**: Core programming language
- **Selenium WebDriver**: Browser automation for document access
- **Chrome Extensions**: Feishu document helper for PDF conversion
- **PyAutoGUI**: GUI automation for handling download dialogs
- **JSON Logging**: Comprehensive progress tracking and error reporting

## Directory Structure

```
/Users/lszhyj/Code/test_kimi/
├── feishu_batch_export.py     # Main batch export script
├── link_collector.py          # Document link collection utility
├── progress_monitor.py        # Real-time progress monitoring
├── setup.sh                   # One-click installation script
├── requirements.txt           # Python dependencies
├── README.md                  # Comprehensive documentation
├── 快速上手.md                 # Quick start guide
├── chrome_extension_guide.md  # Chrome extension installation guide
└── IFLOW.md                   # This file
```

## Building and Running

### Installation
```bash
# Run the installation script
./setup.sh

# Or manually install dependencies
pip install -r requirements.txt
```

### Core Workflow
1. **Link Collection**: Gather Feishu document URLs
```bash
python3 link_collector.py
```

2. **Batch Export**: Process all documents automatically
```bash
python3 feishu_batch_export.py
```

### Configuration
Edit `feishu_batch_export.py` to customize:
- `links_file`: Path to document links file
- `download_dir`: Output directory for PDFs
- `delay`: Operation interval time (seconds)

## Development Conventions

### Code Style
- **Encoding**: UTF-8 with Chinese comments
- **Docstrings**: Comprehensive function documentation
- **Error Handling**: Graceful failure recovery with logging
- **Progress Monitoring**: Real-time status updates and ETA calculation

### Architecture Patterns
- **Modular Design**: Separate modules for distinct functionalities
- **Class-based Structure**: Object-oriented approach for maintainability
- **JSON Logging**: Structured error tracking and reporting
- **Automated Recovery**: Failed document retry mechanisms

### Testing Approach
- **Manual Testing**: User-guided testing with real Feishu documents
- **Error Simulation**: Comprehensive exception handling
- **Progress Validation**: Real-time monitoring verification

## Key Features

### Core Capabilities
- **Batch Processing**: Handle 90+ documents in single session
- **PDF Export**: High-quality PDF with searchable text
- **Progress Monitoring**: Real-time进度显示、成功率、预计时间
- **Error Recovery**: Automatic failed document logging and retry
- **Free User Support**: No enterprise account required

### Technical Highlights
- **Chrome Extension Integration**: Leverages browser extensions for PDF conversion
- **Intelligent URL Validation**: Feishu link verification and deduplication
- **Resource Management**: Automatic browser cleanup and memory management
- **Cross-platform Compatibility**: Works on Windows, macOS, and Linux

## Usage Context

This tool is specifically designed for:
- Personal Feishu free users with large document collections
- Users needing offline PDF copies of cloud documents
- Document migration and backup scenarios
- Automated document archiving workflows

## Important Considerations

### Prerequisites
- Chrome browser with Feishu document helper extension
- Stable internet connection
- Valid access permissions for target documents
- Python 3.7+ environment

### Limitations
- Export speed depends on network conditions (2-3 hours for 90 documents)
- Requires manual Chrome extension installation
- Success rate typically 85%+ depending on document accessibility

### Compliance
- Intended for personal use only
- Users must respect Feishu terms of service
- Only export documents you have permission to access

## Development Notes

The project addresses a specific pain point for Feishu free users who lack API access for bulk operations. By combining browser automation with Chrome extensions, it provides a viable alternative to enterprise-level solutions while maintaining ease of use and comprehensive error handling.