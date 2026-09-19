#!/usr/bin/env python3
"""
build.py —— Markdown 整编为一本 PDF 书（research-to-book skill 配套脚本）
流程：预处理 MD → Pandoc 合并 → Tectonic 编译

用法：
    cd <book_dir>   # 即含 README.md + Chapter_*.md 的目录
    python3 build.py [--book-title 标题] [--book-author 作者]

会读取同目录下 build/ 子目录里的 template.tex / header.tex / cover.tex /
filter.lua / metadata.yaml。如果这些文件不存在，自动从 bundled 模板拷贝
（通过环境变量 RTB_ASSETS 指向 skill 的 assets 目录）。

占位符：metadata.yaml 和 cover.tex 里的 {{BOOK_TITLE}} {{BOOK_AUTHOR}}
{{COVER_*}} 等会被替换为实际值（来自命令行参数或自动推断）。
"""

import os
import re
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

# ----- 路径 -----
ROOT = Path.cwd()
BUILD = ROOT / "build"
CHAPTERS = BUILD / "chapters"
SOURCE_MD = sorted(ROOT.glob("Chapter_*.md"))
README_MD = ROOT / "README.md"
ASSETS = Path(os.environ.get("RTB_ASSETS", Path(__file__).resolve().parent))

# ----- Markdown 标题里的手写章号/节号剥离 -----
# # 第 1 章　SMR 介绍  →  # SMR 介绍
# ## 1.1　引言         →  ## 引言
# ### 1.2.1　推动力    →  ### 推动力
# 分隔符是全角空格 U+3000
H1_NUM_RE = re.compile(r'^(# )第\s*\d+\s*章\s*[　\s]?', re.MULTILINE)
H2_NUM_RE = re.compile(r'^(## )\d+\.\d+\s*[　\s]?', re.MULTILINE)
H3_NUM_RE = re.compile(r'^(### )\d+\.\d+\.\d+\s*[　\s]?', re.MULTILINE)


def strip_manual_numbering(text):
    """剥离 MD 标题里手写的章号/节号，交由 LaTeX 自动编号"""
    text = H1_NUM_RE.sub(r'\1', text)
    text = H2_NUM_RE.sub(r'\1', text)
    text = H3_NUM_RE.sub(r'\1', text)
    return text


def split_code_spans(text):
    """把文本切成 ('code', content) / ('text', content) 两类，代码块内不转义"""
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


# Unicode 上下标 → 普通数字映射（用于聚合连续上下标后交给 LaTeX 命令渲染）
SUP_MAP = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9',
           '⁺':'+','⁻':'-','⁼':'=','⁽':'(','⁾':')','ⁿ':'n'}
SUB_MAP = {'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9',
           '₊':'+','₋':'-','₌':'=','₍':'(','₎':')','ₐ':'a','ₑ':'e','ₒ':'o','ₓ':'x','ₙ':'n',
           'ᵢ':'i','ⱼ':'j','ᵣ':'r','ₛ':'s','ₜ':'t','ₕ':'h','ₖ':'k','ₗ':'l','ₘ':'m','ₚ':'p','ᵤ':'u','ᵥ':'v'}
_SUP_CHARS = ''.join(re.escape(k) for k in SUP_MAP)
_SUB_CHARS = ''.join(re.escape(k) for k in SUB_MAP)


def _convert_superscripts(text):
    """把连续的 Unicode 上标聚合为 \\textsuperscript{}（避免每个数字单独成组）"""
    def repl(m):
        s = ''.join(SUP_MAP[c] for c in m.group(0))
        return r'\textsuperscript{' + s + '}'
    return re.sub(f'[{_SUP_CHARS}]+', repl, text)


def _convert_subscripts(text):
    """把连续的 Unicode 下标聚合为 \\textsubscript{}"""
    def repl(m):
        s = ''.join(SUB_MAP[c] for c in m.group(0))
        return r'\textsubscript{' + s + '}'
    return re.sub(f'[{_SUB_CHARS}]+', repl, text)


def escape_text(text):
    """在普通 markdown 文本（代码块外）转义 LaTeX 危险字符：% & $ ~
    并把 Unicode 上下标、℃、℉ 转换为 LaTeX 命令（西文字体缺失这些字形）"""
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

    text = text.replace('&', r'\&').replace('%', r'\%').replace('$', r'\$')
    text = text.replace('~', r'\textasciitilde{}')

    # Unicode 上下标 / 度数符号 → LaTeX 命令（西文字体无这些字形，否则渲染丢失）
    text = _convert_subscripts(text)
    text = _convert_superscripts(text)
    text = text.replace('℃', r'$^{\circ}$C').replace('℉', r'$^{\circ}$F')
    # emoji / 其他字形缺失字符
    text = text.replace('⚠️', r'\textbf{[注意]}').replace('⚠', r'\textbf{[注意]}')

    for i, l in enumerate(links):
        text = text.replace(f'\x00L{i}\x00', l)
    for i, c in enumerate(code_spans):
        text = text.replace(f'\x00C{i}\x00', c)
    return text


def preprocess_md(src_path: Path, dst_path: Path):
    """读 MD → 剥离手写编号 → 转义 → 写到 dst"""
    text = src_path.read_text(encoding='utf-8')
    text = strip_manual_numbering(text)
    parts = split_code_spans(text)
    out = [c if k == 'code' else escape_text(c) for k, c in parts]
    dst_path.write_text('\n'.join(out), encoding='utf-8')


def check_tools():
    """检测 pandoc 和 tectonic 是否安装，缺失给出清晰提示"""
    missing = []
    for tool in ['pandoc', 'tectonic']:
        if shutil.which(tool) is None:
            missing.append(tool)
    if missing:
        print("✗ 缺少工具：" + ", ".join(missing))
        for t in missing:
            if t == 'pandoc':
                print("  安装 pandoc：brew install pandoc")
            elif t == 'tectonic':
                print("  安装 tectonic：brew install tectonic")
        print("\n已跳过 PDF 编译。Markdown 预处理产物仍在 build/chapters/。")
        return False
    return True


def detect_fonts():
    """
    检测平台和字体，返回 header.tex 应使用的字体配置段。
    macOS：用 Songti SC / PingFang SC / STKaiti（系统自带）
    Linux：尝试 Noto Sans CJK / Noto Serif CJK
    其他：回退到 Latin Modern（用户需自己改）
    """
    import platform
    system = platform.system()

    def has_font(name):
        try:
            r = subprocess.run(['fc-list', ':family'], capture_output=True, text=True, timeout=5)
            return name in r.stdout
        except Exception:
            return False

    if system == 'Darwin':
        # macOS：已知 Songti/PingFang/STKaiti 系统自带，不用检测
        return 'macos'
    elif system == 'Linux':
        if has_font('Noto Serif CJK SC') and has_font('Noto Sans CJK SC'):
            return 'linux-noto'
        if has_font('Source Han Serif SC') and has_font('Source Han Sans SC'):
            return 'linux-sourcehan'
    return 'generic'


def render_template(text: str, vars: dict) -> str:
    """简单占位符替换：{{KEY}} → vars[KEY]"""
    for k, v in vars.items():
        text = text.replace('{{' + k + '}}', str(v))
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--book-title', default=None, help='书名（默认从 README 第一行推断）')
    ap.add_argument('--book-author', default=None, help='作者（默认 "编者"）')
    ap.add_argument('--book-subtitle', default='', help='英文副标题')
    ap.add_argument('--book-date', default=None, help='日期（默认当前年份）')
    ap.add_argument('--pdf-name', default=None, help='成品 PDF 文件名（默认从书名推断）')
    ap.add_argument('--skip-pdf', action='store_true', help='只做 MD 预处理，不编译 PDF')
    args = ap.parse_args()

    # ----- 校验输入 -----
    if not SOURCE_MD:
        print(f"✗ 当前目录 {ROOT} 下没有 Chapter_*.md 文件")
        sys.exit(1)
    if not README_MD.exists():
        print(f"✗ 当前目录 {ROOT} 下没有 README.md")
        sys.exit(1)

    # ----- 推断元信息 -----
    readme_first_line = README_MD.read_text(encoding='utf-8').split('\n', 1)[0]
    default_title = re.sub(r'^#\s+', '', readme_first_line).strip() or "未命名书籍"
    book_title = args.book_title or default_title
    book_author = args.book_author or "编者"
    book_subtitle = args.book_subtitle
    import datetime
    year = datetime.date.today().year
    book_date = args.book_date or f"{year} 年"
    year_cn = ''.join('〇一二三四五六七八九'[int(d)] for d in str(year))
    # 简单的 PDF 文件名：书名去括号 + .pdf
    pdf_name = args.pdf_name or re.sub(r'[（）()【】\[\]\/\\:*?"<>|]', '', book_title).strip() + ".pdf"

    # 推断封面占位符（从书名提取主标题/后缀）
    # 例如 "小型模块化反应堆（SMR）技术" → main="小型模块化反应堆", suffix="（SMR）技术"
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
        cover_symbol = book_title[:4]
        cover_badge = book_title[:6]

    template_vars = {
        'BOOK_TITLE': book_title,
        'BOOK_SUBTITLE': book_subtitle,
        'BOOK_AUTHOR': book_author,
        'BOOK_DATE': book_date,
        'COVER_BADGE': cover_badge,
        'COVER_TOPTAG': f"{cover_symbol} · 专题调研",
        'COVER_SYMBOL': cover_symbol,
        'COVER_TITLE_MAIN': cover_main,
        'COVER_TITLE_SUFFIX': cover_suffix,
        'COVER_SUBTITLE': book_subtitle or 'A Research Compendium',
        'COVER_AUTHOR': book_author,
        'COVER_SOURCE_NOTE': '基于公开资料整理 · 仅供学习参考',
        'COVER_YEAR_CN': f'二〇{year_cn}年',
    }

    # ----- 1. 准备 build/ 目录，拷贝模板 -----
    if CHAPTERS.exists():
        shutil.rmtree(CHAPTERS)
    CHAPTERS.mkdir(parents=True)
    BUILD.mkdir(exist_ok=True)

    # 拷贝模板并替换占位符
    for tpl_name in ['template.tex', 'header.tex', 'cover.tex', 'filter.lua', 'metadata.yaml']:
        src_tpl = ASSETS / tpl_name
        dst_tpl = BUILD / tpl_name
        if not src_tpl.exists():
            print(f"✗ 模板缺失：{src_tpl}")
            sys.exit(1)
        content = src_tpl.read_text(encoding='utf-8')
        content = render_template(content, template_vars)
        dst_tpl.write_text(content, encoding='utf-8')

    # 根据平台调整 header.tex 的字体配置
    font_platform = detect_fonts()
    header_path = BUILD / 'header.tex'
    header = header_path.read_text(encoding='utf-8')
    # 这里只做简单提示：macOS 默认配置可用，其他平台需用户手动改
    if font_platform != 'macos':
        print(f"⚠ 检测到平台 {font_platform}，header.tex 里的 CJK 字体可能需要手动调整。")
        print("  macOS 默认用 Songti SC / PingFang SC / STKaiti；")
        print("  Linux 推荐 Noto Serif CJK SC / Noto Sans CJK SC。")

    # ----- 2. 预处理 README（作为前言，不编号） -----
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

    # ----- 3. 预处理各章 -----
    for src in SOURCE_MD:
        dst = CHAPTERS / (src.stem + ".md")
        preprocess_md(src, dst)
        print(f"  preprocessed: {src.name} → {dst.name}")

    md_files = [readme_dst] + [CHAPTERS / (s.stem + ".md") for s in SOURCE_MD]

    # ----- 4. 是否跳过 PDF -----
    if args.skip_pdf:
        print(f"\n✓ Markdown 预处理完成（跳过 PDF 编译）")
        print(f"  产物在：{CHAPTERS}")
        return

    if not check_tools():
        return

    # ----- 5. Pandoc 合并 -----
    print("\n=== Pandoc 合并 ===")
    pandoc_cmd = [
        "pandoc",
        *[str(f) for f in md_files],
        "build/metadata.yaml",
        "--template=build/template.tex",
        "--lua-filter=build/filter.lua",
        "--top-level-division=chapter",
        "--toc", "--toc-depth=2",
        "--number-sections",
        "-o", "build/book.tex",
    ]
    r = subprocess.run(pandoc_cmd, cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        print("PANDOC STDERR:\n", r.stderr); sys.exit(1)
    if r.stderr.strip():
        print("Pandoc warnings:\n", r.stderr)

    # ----- 6. Tectonic 编译 -----
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
        print("\n排错请参考 skill 的 references/pdf-build-troubleshooting.md")
        sys.exit(1)

    # ----- 7. 成功 -----
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
