#!/usr/bin/env python3
"""md2tex.py —— 把 Markdown 章节转成干净 LaTeX 片段（不含 preamble/document）"""
import re
import sys
import os

SRC_DIR = "/Volumes/ssd/main_link/work/note/Memory-Consistency-Coherence-book"
DST_DIR = "/Volumes/ssd/main_link/work/note/MCC-LaTeX/chapters"


def escape_inline(text: str) -> str:
    """转义 LaTeX 特殊字符（代码块/表格内不调用）"""
    # 顺序很重要：先处理反斜杠与花括号
    text = text.replace("\\", r"\textbackslash{}")
    text = text.replace("{", r"\{").replace("}", r"\}")
    # % & # $ _ ~ ^
    text = text.replace("%", r"\%")
    text = text.replace("&", r"\&")
    text = text.replace("#", r"\#")
    text = text.replace("$", r"\$")
    text = text.replace("_", r"\_")
    text = text.replace("~", r"\textasciitilde{}")
    text = text.replace("^", r"\textasciicircum{}")
    # 上下标 Unicode（化学/数学常用）—— 用 LaTeX 命令
    sup = {"⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9","⁻":"-","⁺":"+"}
    sub = {"₀":"0","₁":"1","₂":"2","₃":"3","₄":"4","₅":"5","₆":"6","₇":"7","₈":"8","₉":"9"}
    def conv_sup(m):
        return r"\textsuperscript{" + "".join(sup[c] for c in m.group(0)) + "}"
    def conv_sub(m):
        return r"\textsubscript{" + "".join(sub[c] for c in m.group(0)) + "}"
    text = re.sub(f"[{''.join(re.escape(k) for k in sup)}]+", conv_sup, text)
    text = re.sub(f"[{''.join(re.escape(k) for k in sub)}]+", conv_sub, text)
    text = text.replace("℃", r"$^{\circ}$C").replace("℉", r"$^{\circ}$F")
    text = text.replace("→", r"$\rightarrow$").replace("∝", r"$\propto$")
    text = text.replace("≥", r"$\geq$").replace("≤", r"$\leq$")
    text = text.replace("≈", r"$\approx$").replace("×", r"$\times$")
    return text


def md_inline(text: str) -> str:
    """处理行内 Markdown 标记：**bold**, *emph*, `code`, [text](url)"""
    # 先 stash 行内代码（转义内部字符）
    codes = []
    def stash_code(m):
        codes.append(m.group(1))
        return f"\x00CODE{len(codes)-1}\x00"
    text = re.sub(r"`([^`\n]+)`", stash_code, text)

    # 链接 [text](url)
    def repl_link(m):
        return r"\href{" + m.group(2) + "}{" + escape_inline(m.group(1)) + "}"
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_link, text)

    # 转义剩余字符
    text = escape_inline(text)

    # **bold**
    text = re.sub(r"\*\*([^*\n]+)\*\*", r"\\textbf{\1}", text)
    # *emph*
    text = re.sub(r"\*([^*\n]+)\*", r"\\emph{\1}", text)

    # 还原代码（用 \texttt，内部需转义）
    for i, c in enumerate(codes):
        # 代码内部转义：$ % & # _ { } ~ ^ \
        c = c.replace("\\", r"\textbackslash{}")
        c = c.replace("{", r"\{").replace("}", r"\}")
        c = c.replace("%", r"\%").replace("&", r"\&").replace("#", r"\#")
        c = c.replace("$", r"\$").replace("_", r"\_")
        c = c.replace("~", r"\textasciitilde{}").replace("^", r"\textasciicircum{}")
        text = text.replace(f"\x00CODE{i}\x00", r"\texttt{" + c + "}")
    return text


def convert_table(lines: list) -> list:
    """把 Markdown 表格转成 booktabs tabular"""
    rows = []
    for ln in lines:
        ln = ln.strip()
        if not ln.startswith("|"):
            continue
        # 跳过分隔行 |---|---|
        if re.match(r"^\|[\s:\-\|]+\|$", ln):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        rows.append(cells)
    if not rows:
        return []
    ncols = len(rows[0])
    spec = "l" + "l" * (ncols - 1)  # 简单：全左对齐
    out = []
    # 判断是否在 itemize 等环境内（外层会处理缩进）；这里给一个居中表格
    out.append(r"\begin{center}")
    out.append(r"\begin{tabular}{" + spec + "}")
    out.append(r"\toprule")
    # 表头
    out.append(" & ".join(md_inline(c) for c in rows[0]) + r" \\")
    out.append(r"\midrule")
    # 数据
    for r in rows[1:]:
        out.append(" & ".join(md_inline(c) for c in r) + r" \\")
    out.append(r"\bottomrule")
    out.append(r"\end{tabular}")
    out.append(r"\end{center}")
    out.append("")
    return out


def convert(md_path: str) -> str:
    text = open(md_path, encoding="utf-8").read()
    lines = text.split("\n")
    out = []
    i = 0
    in_code = False
    code_buf = []
    code_lang = ""

    while i < len(lines):
        ln = lines[i]
        raw = ln  # 原始行（未处理）

        # 代码块 ```
        if re.match(r"^```", raw):
            if not in_code:
                in_code = True
                code_lang = raw.strip("`").strip()
                code_buf = []
            else:
                # 结束代码块
                out.append(r"\begin{verbatim}")
                out.extend(code_buf)
                out.append(r"\end{verbatim}")
                out.append("")
                in_code = False
            i += 1
            continue
        if in_code:
            code_buf.append(raw)
            i += 1
            continue

        # 章标题 # 第 N 章　标题
        m = re.match(r"^#\s+第\s*\d+\s*章\s*(.+)$", raw)
        if m:
            out.append(r"\chapter{" + md_inline(m.group(1).strip()) + "}")
            i += 1
            continue

        # 节标题 ## N.M　标题  （剥离子写编号）
        m = re.match(r"^##\s+(?:\d+\.\d+\s*[　 ]?)?(.+)$", raw)
        if m:
            title = m.group(1).strip()
            if title == "参考文献":
                out.append(r"\section*{参考文献}")
                out.append(r"\begin{itemize}")
                i += 1
                # 收集后续列表项（数字编号）
                while i < len(lines):
                    ln2 = lines[i]
                    if re.match(r"^\s*\d+\.\s", ln2):
                        item = re.sub(r"^\s*\d+\.\s*", "", ln2.strip())
                        out.append(r"\item " + md_inline(item))
                        i += 1
                    elif ln2.strip() == "":
                        i += 1
                    else:
                        break
                out.append(r"\end{itemize}")
                continue
            out.append(r"\section{" + md_inline(title) + "}")
            i += 1
            continue

        # 小节标题 ###
        m = re.match(r"^###\s+(?:\d+\.\d+\.\d+\s*[　 ]?)?(.+)$", raw)
        if m:
            out.append(r"\subsection{" + md_inline(m.group(1).strip()) + "}")
            i += 1
            continue

        # 水平线 ---
        if re.match(r"^---+\s*$", raw):
            i += 1
            continue

        # 引用块 >（章首核心命题）
        if raw.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].startswith(">"):
                content = re.sub(r"^>\s?", "", lines[i])
                quote_lines.append(md_inline(content))
                i += 1
            out.append(r"\begin{epigraph}")
            out.extend(quote_lines)
            out.append(r"\end{epigraph}")
            out.append("")
            continue

        # 表格
        if raw.strip().startswith("|"):
            tbl_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl_lines.append(lines[i])
                i += 1
            out.extend(convert_table(tbl_lines))
            continue

        # 无序列表 - / *
        if re.match(r"^\s*[-*]\s+", raw):
            out.append(r"\begin{itemize}")
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i])
                out.append(r"\item " + md_inline(item))
                i += 1
            out.append(r"\end{itemize}")
            out.append("")
            continue

        # 有序列表 1. 2.
        if re.match(r"^\s*\d+\.\s+", raw) and not (out and out[-1].startswith(r"\section*{参考文献}")):
            out.append(r"\begin{enumerate}")
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[i])
                out.append(r"\item " + md_inline(item))
                i += 1
            out.append(r"\end{enumerate}")
            out.append("")
            continue

        # 空行
        if raw.strip() == "":
            out.append("")
            i += 1
            continue

        # 普通段落
        out.append(md_inline(raw))
        i += 1

    return "\n".join(out) + "\n"


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    for num in range(1, 12):
        # 找到对应的 md 文件
        candidates = [f for f in os.listdir(SRC_DIR) if f.startswith(f"Chapter_{num:02d}_")]
        if not candidates:
            print(f"!! 找不到第 {num} 章", file=sys.stderr)
            continue
        src = os.path.join(SRC_DIR, candidates[0])
        dst = os.path.join(DST_DIR, f"ch{num:02d}.tex")
        tex = convert(src)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(tex)
        print(f"✓ {candidates[0]} → ch{num:02d}.tex ({len(tex)} bytes)")


if __name__ == "__main__":
    main()
