#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并指定目录下的所有 PDF 文件，生成一个新的 PDF：
- 以文件名为/以“选调面试”开头的 PDF 作为第一个文件
- 其余 PDF 排序规则随意（这里按文件名排序）

默认目录：/Users/lszhyj/Documents/选调面试/飞书笔记
默认输出文件名：选调面试_合并.pdf

用法：
    python3 merge_pdfs.py
或：
    python3 merge_pdfs.py /path/to/folder
"""

import os
import sys

from PyPDF2 import PdfMerger


DEFAULT_FOLDER = "/Users/lszhyj/Documents/选调面试/飞书笔记"
OUTPUT_NAME = "选调面试_合并.pdf"


def merge_pdfs(folder: str) -> None:
    if not os.path.isdir(folder):
        print(f"❌ 目录不存在: {folder}")
        return

    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"❌ 目录下没有找到 PDF 文件: {folder}")
        return

    first_pdf = None
    for f in pdf_files:
        name, _ = os.path.splitext(f)
        if name == "选调面试" or name.startswith("选调面试"):
            first_pdf = f
            break

    others = sorted(f for f in pdf_files if f != first_pdf)
    ordered = ([first_pdf] if first_pdf else []) + others

    print("📋 即将按以下顺序合并：")
    for idx, f in enumerate(ordered, 1):
        print(f"  {idx:2d}. {f}")

    output_path = os.path.join(folder, OUTPUT_NAME)

    merger = PdfMerger()
    try:
        for f in ordered:
            path = os.path.join(folder, f)
            print(f"➕ 合并: {path}")
            merger.append(path)

        merger.write(output_path)
        print(f"✅ 已生成合并文件: {output_path}")
    finally:
        merger.close()


def main() -> None:
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = input(f"请输入要合并 PDF 的目录（默认: {DEFAULT_FOLDER}）: ").strip() or DEFAULT_FOLDER

    merge_pdfs(folder)


if __name__ == "__main__":
    main()
