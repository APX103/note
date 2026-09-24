#!/usr/bin/env python3
"""
build.py —— 本书本地构建脚本（基于 research-to-book skill 的 build.py 定制）

定制点（相对原版）：
1. 模板默认取本书 assets/ 目录（RTB_ASSETS 环境变量仍可覆盖）；
2. escape_text 增加 LaTeX 数学直通：$$...$$ 显示公式与 $...$ 行内公式在转义前
   先被摘出，转义后原样放回，配合 Pandoc 的 tex_math_dollars 扩展输出真公式
   （本书第 5、6 章为公式密集章节）；
3. 作者默认值改为本书编者。

用法：
    cd STM32G4-Motor-Control-book
    python3 build.py [--book-title 标题] [--book-author 作者]
"""

import os
import re
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

ROOT = Path.cwd()
BUILD = ROOT / "build"
CHAPTERS = BUILD / "chapters"
SOURCE_MD = sorted(ROOT.glob("Chapter_*.md"))
README_MD = ROOT / "README.md"
ASSETS = Path(os.environ.get("RTB_ASSETS", Path(__file__).resolve().parent / "assets"))

H1_NUM_RE = re.compile(r'^(# )第\s*\d+\s*章\s*[　\s]?', re.MULTILINE)
H2_NUM_RE = re.compile(r'^(## )\d+\.\d+\s*[　\s]?', re.MULTILINE)
H3_NUM_RE = re.compile(r'^(### )\d+\.\d+\.\d+\s*[　\s]?', re.MULTILINE)


def strip_manual_numbering(text):
    text = H1_NUM_RE.sub(r'\1', text)
    text = H2_NUM_RE.sub(r'\1', text)
    text = H3_NUM_RE.sub(r'\1', text)
    return text


def split_code_spans(text):
    lines = text.split('\n')
    out, in_code, buf_text, buf_code = [], False, [], []

    def flush(buf, kind):
        if buf:
            out.append((kind, '\n'.join(buf)))
            buf.clear()

    for line in lines:
        if re.match(r'^(`{3,}|~{3,})', line):
            if in_code:
                buf_code.append(line); flush(buf_code, 'code'); in_code = False
            else:
                flush(buf_text, 'text'); buf_code.append(line); in_code = True
        else:
            (buf_code if in_code else buf_text).append(line)
    flush(buf_text, 'text')
    if in_code:
        flush(buf_code, 'code')
    return out


SUP_MAP = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9',
           '⁺':'+','⁻':'-','⁼':'=','⁽':'(','⁾':')','ⁿ':'n'}
SUB_MAP = {'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9',
           '₊':'+','₋':'-','₌':'=','₍':'(','₎':')','ₐ':'a','ₑ':'e','ₒ':'o','ₓ':'x','ₙ':'n',
           'ᵢ':'i','ⱼ':'j','ᵣ':'r','ₛ':'s','ₜ':'t','ₕ':'h','ₖ':'k','ₗ':'l','ₘ':'m','ₚ':'p','ᵤ':'u','ᵥ':'v'}
_SUP_CHARS = ''.join(re.escape(k) for k in SUP_MAP)
_SUB_CHARS = ''.join(re.escape(k) for k in SUB_MAP)


def _convert_superscripts(text):
    def repl(m):
        s = ''.join(SUP_MAP[c] for c in m.group(0))
        return r'\textsuperscript{' + s + '}'
    return re.sub(f'[{_SUP_CHARS}]+', repl, text)


def _convert_subscripts(text):
    def repl(m):
        s = ''.join(SUB_MAP[c] for c in m.group(0))
        return r'\textsubscript{' + s + '}'
    return re.sub(f'[{_SUB_CHARS}]+', repl, text)


DISPLAY_MATH_RE = re.compile(r'\$\$(.+?)\$\$', re.DOTALL)
INLINE_MATH_RE = re.compile(r'(?<!\$)\$([^$\n]+)\$(?!\$)')


def escape_text(text):
    """代码块外的文本：先摘出行内代码/链接/数学公式，再转义 % & $ ~，
    最后按 代码→链接→数学 的逆序放回。"""
    code_spans = []
    text = re.sub(r'`[^`\n]+`',
                  lambda m: (code_spans.append(m.group(0)), f'\x00C{len(code_spans)-1}\x00')[1],
                  text)
    links = []
    def stash_link(m):
        url = m.group(2).replace('%', r'\%').replace('&', r'\&').replace('#', r'\#')
        tp = m.group(1).replace('&', r'\&').replace('%', r'\%')
        links.append(f'[{tp}]({url})')
        return f'\x00L{len(links)-1}\x00'
    text = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', stash_link, text)

    # —— 数学公式直通（本书定制）——
    maths = []
    def stash_math(m):
        maths.append(m.group(0))
        return f'\x00M{len(maths)-1}\x00'
    text = DISPLAY_MATH_RE.sub(stash_math, text)
    text = INLINE_MATH_RE.sub(stash_math, text)

    text = text.replace('&', r'\&').replace('%', r'\%').replace('$', r'\$')
    text = text.replace('~', r'\textasciitilde{}')

    text = _convert_subscripts(text)
    text = _convert_superscripts(text)
    text = text.replace('℃', r'$^{\circ}$C').replace('℉', r'$^{\circ}$F')
    text = text.replace('ℏ', r'$\hbar$').replace('∝', r'$\propto$').replace('→', r'$\rightarrow$')
    text = text.replace('⚠️', r'\textbf{[注意]}').replace('⚠', r'\textbf{[注意]}')

    for i, m in enumerate(maths):
        text = text.replace(f'\x00M{i}\x00', m)
    for i, l in enumerate(links):
        text = text.replace(f'\x00L{i}\x00', l)
    for i, c in enumerate(code_spans):
        text = text.replace(f'\x00C{i}\x00', c)
    return text


def preprocess_md(src_path: Path, dst_path: Path):
    text = src_path.read_text(encoding='utf-8')
    text = strip_manual_numbering(text)
    parts = split_code_spans(text)
    out = [c if k == 'code' else escape_text(c) for k, c in parts]
    dst_path.write_text('\n'.join(out), encoding='utf-8')


def check_tools():
    missing = []
    for tool in ['pandoc', 'tectonic']:
        if shutil.which(tool) is None:
            missing.append(tool)
    if missing:
        print("✗ 缺少工具：" + ", ".join(missing))
        return False
    return True


def render_template(text: str, vars: dict) -> str:
    for k, v in vars.items():
        text = text.replace('{{' + k + '}}', str(v))
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--book-title', default=None)
    ap.add_argument('--book-author', default="李佳伦")
    ap.add_argument('--book-subtitle', default='')
    ap.add_argument('--book-date', default=None)
    ap.add_argument('--pdf-name', default=None)
    ap.add_argument('--skip-pdf', action='store_true')
    args = ap.parse_args()

    if not SOURCE_MD:
        print(f"✗ 当前目录 {ROOT} 下没有 Chapter_*.md 文件")
        sys.exit(1)
    if not README_MD.exists():
        print(f"✗ 当前目录 {ROOT} 下没有 README.md")
        sys.exit(1)

    readme_first_line = README_MD.read_text(encoding='utf-8').split('\n', 1)[0]
    default_title = re.sub(r'^#\s+', '', readme_first_line).strip() or "未命名书籍"
    book_title = args.book_title or default_title
    book_author = args.book_author
    book_subtitle = args.book_subtitle
    import datetime
    year = datetime.date.today().year
    book_date = args.book_date or f"{year} 年"
    year_cn = ''.join('〇一二三四五六七八九'[int(d)] for d in str(year))
    pdf_name = args.pdf_name or re.sub(r'[（）()【】\[\]\/\\:*?"<>|]', '', book_title).strip() + ".pdf"

    m = re.match(r'^(.*?)[（(]([^）)]+)[）)](.*)$', book_title)
    if m:
        cover_main = m.group(1).strip()
        abbr = m.group(2).strip()
        cover_suffix = f"（{abbr}）{m.group(3).strip()}"
        cover_symbol = abbr
        cover_badge = abbr
    else:
        cover_main = book_title
        cover_suffix = ''
        cover_symbol = book_title[:4] if len(book_title) >= 4 else book_title
        cover_badge = book_title[:2] if len(book_title) >= 2 else book_title

    template_vars = {
        'BOOK_TITLE': book_title,
        'BOOK_SUBTITLE': book_subtitle,
        'BOOK_AUTHOR': book_author,
        'BOOK_DATE': book_date,
        'COVER_BADGE': cover_badge,
        'COVER_TOPTAG': f"{cover_symbol} · 技术实战",
        'COVER_SYMBOL': cover_symbol,
        'COVER_TITLE_MAIN': cover_main,
        'COVER_TITLE_SUFFIX': cover_suffix,
        'COVER_SUBTITLE': book_subtitle or '电机控制 · 从套件到算法',
        'COVER_AUTHOR': book_author,
        'COVER_SOURCE_NOTE': '基于公开资料整理 · 仅供学习参考',
        'COVER_YEAR_CN': f'{year_cn}年',
    }

    if CHAPTERS.exists():
        shutil.rmtree(CHAPTERS)
    CHAPTERS.mkdir(parents=True)
    BUILD.mkdir(exist_ok=True)

    for tpl_name in ['template.tex', 'header.tex', 'cover.tex', 'filter.lua', 'metadata.yaml']:
        src_tpl = ASSETS / tpl_name
        dst_tpl = BUILD / tpl_name
        if not src_tpl.exists():
            print(f"✗ 模板缺失：{src_tpl}")
            sys.exit(1)
        content = src_tpl.read_text(encoding='utf-8')
        content = render_template(content, template_vars)
        dst_tpl.write_text(content, encoding='utf-8')

    readme_dst = CHAPTERS / "00_preface.md"
    readme_text = README_MD.read_text(encoding='utf-8')
    readme_text = re.sub(r'^#\s+.*$', '# 前言 {.unnumbered}',
                         readme_text, count=1, flags=re.MULTILINE)
    readme_text = re.sub(r'^(## )([^\n{]+)$', r'\1\2 {.unnumbered}',
                         readme_text, flags=re.MULTILINE)
    readme_text = re.sub(r'^(### )([^\n{]+)$', r'\1\2 {.unnumbered}',
                         readme_text, flags=re.MULTILINE)
    readme_text = re.sub(r'\[([^\]]+)\]\([^)]+\.md\)', r'\1', readme_text)
    tmp = CHAPTERS / "00_preface_raw.md"
    tmp.write_text(readme_text, encoding='utf-8')
    preprocess_md(tmp, readme_dst)
    tmp.unlink()

    for src in SOURCE_MD:
        dst = CHAPTERS / (src.stem + ".md")
        preprocess_md(src, dst)
        print(f"  preprocessed: {src.name} → {dst.name}")

    md_files = [readme_dst] + [CHAPTERS / (s.stem + ".md") for s in SOURCE_MD]

    if args.skip_pdf:
        print(f"\n✓ Markdown 预处理完成（跳过 PDF 编译）")
        print(f"  产物在：{CHAPTERS}")
        return

    if not check_tools():
        return

    # Tectonic 以 book.tex 所在目录（build/）为根解析相对路径——把图片拷进去
    img_src = ROOT / "images"
    if img_src.is_dir():
        img_dst = BUILD / "images"
        if img_dst.exists():
            shutil.rmtree(img_dst)
        shutil.copytree(img_src, img_dst)

    print("\n=== Pandoc 合并 ===")
    pandoc_cmd = [
        "pandoc",
        *[str(f) for f in md_files],
        "build/metadata.yaml",
        "--template=build/template.tex",
        "--lua-filter=build/filter.lua",
        "--top-level-division=chapter",
        "--no-highlight",
        "--toc", "--toc-depth=2",
        "--number-sections",
        "-o", "build/book.tex",
    ]
    r = subprocess.run(pandoc_cmd, cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        print("PANDOC STDERR:\n", r.stderr); sys.exit(1)
    if r.stderr.strip():
        print("Pandoc warnings:\n", r.stderr)

    print("\n=== Tectonic 编译 ===")
    tectonic_cmd = ["tectonic", "-X", "compile", "--keep-logs",
                    "--keep-intermediates", "build/book.tex"]
    r = subprocess.run(tectonic_cmd, cwd=str(ROOT), capture_output=True, text=True)
    print(r.stdout[-2000:] if len(r.stdout) > 2000 else r.stdout)
    if r.returncode != 0:
        print("TECTONIC STDERR:\n", r.stderr[-2000:])
        log = BUILD / "book.log"
        if log.exists():
            print("\n=== book.log 最后 80 行 ===")
            print("\n".join(log.read_text(encoding='utf-8', errors='replace').splitlines()[-80:]))
        sys.exit(1)

    pdf = BUILD / "book.pdf"
    if pdf.exists():
        size_kb = pdf.stat().st_size / 1024
        final_pdf = ROOT / pdf_name
        shutil.copy2(pdf, final_pdf)
        print(f"\n✓ 编译成功：{pdf} ({size_kb:.0f} KB)")
        print(f"✓ 成品输出：{final_pdf}")
    else:
        print(f"\n✗ PDF 未生成：{pdf}"); sys.exit(1)


if __name__ == "__main__":
    main()
