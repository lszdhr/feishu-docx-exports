#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 PDF 文件中提取飞书链接，并写入/合并到 feishu_links.txt

用法：
    python3 pdf_link_extractor.py /路径/到/含链接的PDF.pdf
若不传参数，会提示输入路径，默认尝试 ../选调面试.pdf。
"""

import os
import sys

from PyPDF2 import PdfReader

from link_collector import FeishuLinkCollector


def extract_feishu_links_from_pdf(pdf_path, output_file="feishu_links.txt"):
    if not os.path.exists(pdf_path):
        print(f"❌ PDF文件不存在: {pdf_path}")
        return

    print(f"📄 正在解析 PDF: {pdf_path}")

    collector = FeishuLinkCollector(output_file=output_file)
    collector.load_existing_links()

    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"❌ 无法读取 PDF 文件: {e}")
        return

    added_from_annots = 0
    added_from_text = 0

    for page_index, page in enumerate(reader.pages):
        # 1）注释中的链接（常见的可点击链接）
        annots = page.get("/Annots")
        if annots:
            for annot in annots:
                try:
                    obj = annot.get_object()
                    action = obj.get("/A")
                    if not action:
                        continue
                    uri = action.get("/URI")
                    if not uri:
                        continue
                    if collector.add_link(uri):
                        added_from_annots += 1
                except Exception:
                    continue

        # 2）文本中的裸 URL（作为补充）
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""

        if text.strip():
            added_from_text += collector.add_links_from_text(text)

    collector.remove_duplicates()
    collector.save_links()

    print(f"✅ 从 PDF 注释中新增链接: {added_from_annots}")
    print(f"✅ 从 PDF 文本中新增链接: {added_from_text}")


def main():
    print("🚀 PDF 飞书链接提取工具")
    print("=" * 40)

    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        default_path = "../选调面试.pdf"
        pdf_path = input(f"请输入包含飞书链接的 PDF 文件路径（默认: {default_path}）: ").strip() or default_path

    extract_feishu_links_from_pdf(pdf_path, output_file="feishu_links.txt")


if __name__ == "__main__":
    main()
