#!/usr/bin/env python3
"""
build.py —— 把 SMR-book 下的 Markdown 整编为一本 PDF 书
流程：预处理 21 个 MD → Pandoc 合并 → Tectonic 编译
"""

import os
import re
import sys
import shutil
import subprocess
from pathlib import Path

# ----- 路径 -----
ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
CHAPTERS = BUILD / "chapters"
SOURCE_MD = sorted(ROOT.glob("Chapter_*.md"))
README_MD = ROOT / "README.md"

# ----- 工具：转义 LaTeX 特殊字符（在代码块外） -----

FENCE_RE = re.compile(r'^(`{3,}|~{3,}).*$', re.MULTILINE)

# 标题前缀剥离：把 MD 里手写的「第 N 章」「N.M」「N.M.K」去掉，让 LaTeX 自动编号
# H1:  # 第 1 章　SMR 介绍          →  # SMR 介绍
# H2:  ## 1.1　引言                 →  ## 引言
# H3:  ### 1.2.1　推动力            →  ### 推动力
# 分隔符是全角空格 U+3000（　）
H1_NUM_RE = re.compile(r'^(# )第\s*\d+\s*章　?', re.MULTILINE)
H2_NUM_RE = re.compile(r'^(## )\d+\.\d+　?', re.MULTILINE)
H3_NUM_RE = re.compile(r'^(### )\d+\.\d+\.\d+　?', re.MULTILINE)


def strip_manual_numbering(text):
    """剥离 MD 标题里手写的章号/节号，交由 LaTeX 自动编号"""
    text = H1_NUM_RE.sub(r'\1', text)
    text = H2_NUM_RE.sub(r'\1', text)
    text = H3_NUM_RE.sub(r'\1', text)
    return text


def split_code_spans(text):
    """
    把文本切成 (kind, content) 列表。
    kind == 'code'：在 ``` 围栏内（含围栏行本身），不转义
    kind == 'text'：普通 markdown，需要转义
    """
    lines = text.split('\n')
    out = []
    in_code = False
    buf_text = []
    buf_code = []

    def flush(buf, kind):
        if buf:
            out.append((kind, '\n'.join(buf)))
            buf.clear()

    for line in lines:
        if re.match(r'^(`{3,}|~{3,})', line):
            if in_code:
                # closing fence
                buf_code.append(line)
                flush(buf_code, 'code')
                in_code = False
            else:
                # opening fence
                flush(buf_text, 'text')
                buf_code.append(line)
                in_code = True
        else:
            if in_code:
                buf_code.append(line)
            else:
                buf_text.append(line)
    flush(buf_text, 'text')
    if in_code:  # 未闭合，按代码处理
        flush(buf_code, 'code')
    return out


def escape_text(text):
    """
    在普通 markdown 文本中转义 LaTeX 特殊字符。
    注意：转义不能影响 markdown 语法本身（# - * 等 markdown 语法字符要保留）。
    只转义 LaTeX 特有的危险字符： % & $ 以及不在数学/代码里的 ~
    """
    # 用占位符保护行内代码 `...`（反引号包裹）
    code_spans = []

    def stash_code(m):
        code_spans.append(m.group(0))
        return f'\x00CODE{len(code_spans) - 1}\x00'

    text = re.sub(r'`[^`\n]+`', stash_code, text)

    # 保护 markdown 链接 [text](url) 中的 url（可能含 & %）
    links = []

    def stash_link(m):
        whole = m.group(0)
        url = m.group(2)
        text_part = m.group(1)
        # 转义 url 里的危险字符
        url_escaped = url.replace('%', r'\%').replace('&', r'\&').replace('#', r'\#')
        # 转义 text_part 里的危险字符（但保留 markdown 格式）
        text_escaped = (text_part
                        .replace('&', r'\&')
                        .replace('%', r'\%'))
        whole_escaped = f'[{text_escaped}]({url_escaped})'
        links.append(whole_escaped)
        return f'\x00LINK{len(links) - 1}\x00'

    text = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', stash_link, text)

    # 现在对剩下的文本做 LaTeX 转义
    # 顺序：先 & 再 % 再 $（互不影响）
    # 注意 & 也是 markdown 表格的列分隔符 —— 但 markdown 表格里 & 仍要转义为 \&
    text = text.replace('&', r'\&')
    text = text.replace('%', r'\%')
    text = text.replace('$', r'\$')
    # ~（波浪号）在 LaTeX 里是不可断空格，作为普通字符要替换
    # 但 markdown 中 ~~ 可能是删除线 —— 我们书里没有删除线，所以直接替换
    text = text.replace('~', r'\textasciitilde{}')

    # 还原链接和代码
    for i, l in enumerate(links):
        text = text.replace(f'\x00LINK{i}\x00', l)
    for i, c in enumerate(code_spans):
        text = text.replace(f'\x00CODE{i}\x00', c)

    return text


def preprocess_md(src_path: Path, dst_path: Path):
    """读 MD → 剥离手写编号 → 转义 → 写到 dst"""
    text = src_path.read_text(encoding='utf-8')
    # 1. 先剥离手写章号/节号（让 LaTeX 自动编号）
    text = strip_manual_numbering(text)
    # 2. 再做代码块保护的转义
    parts = split_code_spans(text)
    out = []
    for kind, content in parts:
        if kind == 'code':
            out.append(content)
        else:
            out.append(escape_text(content))
    dst_path.write_text('\n'.join(out), encoding='utf-8')


def main():
    # 1. 清理 + 建目录
    if CHAPTERS.exists():
        shutil.rmtree(CHAPTERS)
    CHAPTERS.mkdir(parents=True)

    # 2. 预处理 README（作为前言，不编号）
    readme_dst = CHAPTERS / "00_preface.md"
    readme_text = README_MD.read_text(encoding='utf-8')
    # 把第一行 # 小型模块化反应堆（SMR）技术 替换为 # 前言 {.unnumbered}
    # {.unnumbered} 让 Pandoc 生成 \chapter*（不编号、不进计数器）
    readme_text = re.sub(r'^#\s+小型模块化反应堆.*$',
                         '# 前言 {.unnumbered}',
                         readme_text, count=1, flags=re.MULTILINE)
    # README 里的子标题 ## 作者简介 等也设为 unnumbered（避免前言内出现 0.1 这种编号）
    readme_text = re.sub(r'^(## )([^\n{]+)$', r'\1\2 {.unnumbered}',
                         readme_text, flags=re.MULTILINE)
    readme_text = re.sub(r'^(### )([^\n{]+)$', r'\1\2 {.unnumbered}',
                         readme_text, flags=re.MULTILINE)
    # README 里的章节链接 [第 N 章](./Chapter_xx.md) 改为纯文本
    readme_text = re.sub(r'\[([^\]]+)\]\([^)]+\.md\)', r'\1', readme_text)
    tmp = CHAPTERS / "00_preface_raw.md"
    tmp.write_text(readme_text, encoding='utf-8')
    preprocess_md(tmp, readme_dst)
    tmp.unlink()

    # 3. 预处理 20 章
    for src in SOURCE_MD:
        dst = CHAPTERS / (src.stem + ".md")
        preprocess_md(src, dst)
        print(f"  preprocessed: {src.name} → {dst.name}")

    # 4. 汇总所有 MD 文件路径（按顺序：前言 + 20 章）
    md_files = [readme_dst] + [CHAPTERS / (s.stem + ".md") for s in SOURCE_MD]

    # 5. Pandoc 合并为单一 .tex
    print("\n=== Pandoc 合并 ===")
    pandoc_cmd = [
        "pandoc",
        *[str(f) for f in md_files],
        "build/metadata.yaml",
        "--template=build/template.tex",
        "--lua-filter=build/filter.lua",
        "--top-level-division=chapter",
        "--toc",
        "--toc-depth=2",
        "--number-sections",
        "-o", "build/book.tex",
    ]
    print(" ".join(pandoc_cmd))
    r = subprocess.run(pandoc_cmd, cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        print("PANDOC STDERR:\n", r.stderr)
        sys.exit(1)
    if r.stderr.strip():
        print("Pandoc warnings:\n", r.stderr)

    # 6. Tectonic 编译
    print("\n=== Tectonic 编译 ===")
    tectonic_cmd = [
        "tectonic",
        "-X", "compile",
        "--keep-logs",
        "--keep-intermediates",
        "build/book.tex",
    ]
    print(" ".join(tectonic_cmd))
    r = subprocess.run(tectonic_cmd, cwd=str(ROOT), capture_output=True, text=True)
    print(r.stdout[-3000:] if len(r.stdout) > 3000 else r.stdout)
    if r.returncode != 0:
        print("TECTONIC STDERR:\n", r.stderr[-3000:])
        # 打印完整日志
        log = BUILD / "book.log"
        if log.exists():
            print("\n=== book.log 最后 100 行 ===")
            print("\n".join(log.read_text(encoding='utf-8', errors='replace').splitlines()[-100:]))
        sys.exit(1)

    # 7. 成功
    pdf = BUILD / "book.pdf"
    if pdf.exists():
        size_kb = pdf.stat().st_size / 1024
        # 复制一份带友好名字的成品
        final_pdf = ROOT / "SMR技术.pdf"
        shutil.copy2(pdf, final_pdf)
        print(f"\n✓ 编译成功：{pdf} ({size_kb:.0f} KB)")
        print(f"✓ 成品输出：{final_pdf}")
    else:
        print(f"\n✗ PDF 未生成：{pdf}")
        sys.exit(1)


if __name__ == "__main__":
    main()
