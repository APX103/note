#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《官僚体制的政治》(The Politics of Bureaucracy, Gordon Tullock) OCR 整理本
→ 分章 HTML + 独立目录页。

清理规则：
  - 删除独立成行的 OCR 页码，及粘连在正文中的页码（人工核对的清单）
  - 合并被页边界切断的段落
  - 半角标点（, ; : ?）出现在汉字之间时转全角
  - LaTeX 残留（$..$、\\mathbf、_{n}、\\% 等）转为普通文本
  - 脚注标记 ①②③ / 星号 → 上标；脚注正文收集到章末"注释"
  - 原 OCR 远程图片已失效（CDN 403）：按原书文字描述重绘 SVG，装饰图丢弃
"""
import os
import re
import html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'source', '官僚体制的政治.md')
OUT = os.path.join(ROOT, 'chapters')

BOOK_TITLE = '官僚体制的政治'
BOOK_EN = 'The Politics of Bureaucracy'
BOOK_AUTHOR = '[美] 戈登·塔洛克 著'
PREFACE_AUTHOR = '詹姆斯·M. 布坎南'

PARTS = {
    'p1': ('第一篇', '导论'),
    'p2': ('第二篇', '政治人的世界'),
    'p3': ('第三篇', '向下看'),
    'p4': ('第四篇', '结束语'),
}

CH_TITLES = {
    1: '本书是讲什么的', 2: '预备知识', 3: '一般氛围', 4: '观望者与同盟者',
    5: '政治人的世界——领导', 6: '单个领导的情形', 7: '集体领导', 8: '多位领导',
    9: '同僚、侍臣和男爵', 10: '追随者', 11: '下属与下级', 12: '了解他们自己',
    13: '帕金森法则', 14: '交头接耳传信息', 15: '一个思想实验', 16: '实验的继续',
    17: '组织任务的限度', 18: '放松要求', 19: '控制的问题', 20: '执行',
    21: '用结果判断', 22: '节省劳力的工具——成本核算', 23: '多种多样节省劳力的工具',
    24: '外部检查', 25: '该做些什么？究竟该做些什么？',
}
CH_PART = {}
for _n in (1, 2):
    CH_PART[_n] = 'p1'
for _n in range(3, 11):
    CH_PART[_n] = 'p2'
for _n in range(11, 25):
    CH_PART[_n] = 'p3'
CH_PART[25] = 'p4'

CN_NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8,
          '九': 9, '十': 10, '十一': 11, '十二': 12, '十三': 13, '十四': 14,
          '十五': 15, '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
          '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25}

# 人工核对过的正文粘连页码/OCR 错字清理清单（唯一串替换）
INLINE_FIXES = [
    ('，5可以为接受了分析模型', '，可以为接受了分析模型'),
    ('隐含9意思', '隐含意思'),
    ('参照10政治人', '参照政治人'),
    ('时16期中', '时期中'),
    ('的23能力', '的能力'),
    ('在24等级制顶层', '在等级制顶层'),
    ('。29同钱', '。同钱'),
    ('，50连这么', '，连这么'),
    ('，66几乎', '，几乎'),
    ('，77除非', '，除非'),
    ('要比79用于', '要比用于'),
    ('可以85挑选', '可以挑选'),
    ('看出87来', '看出来'),
    ('这个91集体', '这个集体'),
    ('中的94大多数', '中的大多数'),
    ('纯粹100形式', '纯粹形式'),
    ('，105以保证', '，以保证'),
    ('这个108工具', '这个工具'),
    ('其一，111他可以', '其一，他可以'),
    ('基本112考虑', '基本考虑'),
    ('，150也由于', '，也由于'),
    ('大中208型', '大中型'),
    ('成本228会计', '成本会计'),
    ('，238这个管理机构', '，这个管理机构'),
    ('喜爱 99 时', '喜爱时'),
    ('上 122 级的垂青', '上级的垂青'),
    ('分析 156 可以毫无困难', '分析可以毫无困难'),
    # 同位素 OCR 错字：天然铀浓缩分离的是 U-235 与 U-238
    ('铀237', '铀238'),
    ('铀 237', '铀 238'),
    ('轴 235', '铀 235'),
    ('守愿选择B', '宁愿选择B'),
    # 重复用词修剪
    ('也会有也会有', '也会有'),
]

# ---------------------------------------------------------------------------
# 文本清理
# ---------------------------------------------------------------------------

def demath(s):
    """把 LaTeX 残留转普通文本。"""
    def conv(m):
        t = m.group(1)
        t = t.replace('\\%', '%').replace('\\sim', '–')
        t = re.sub(r'\\(?:mathbf|mathrm|mathit)\{([^}]*)\}', r'\1', t)
        t = t.replace('^{\prime\prime}', '″').replace("^{\\prime\\prime}", '″')
        t = t.replace('^{\prime}', '′').replace("^{\\prime}", '′')
        t = re.sub(r'_\{(\d+)\}',
                   lambda mm: ''.join(chr(0x2080 + int(d)) for d in mm.group(1)), t)
        t = t.replace('{', '').replace('}', '')
        return t
    s = re.sub(r'\$([^$]+)\$', conv, s)
    # 独立的 \star 标记保留原样，由脚注逻辑处理
    return s


CJK = r'\u4e00-\u9fff\u201c\u201d\u2018\u2019\u3001\u3002\uff0c\uff1b\uff1a\uff08\uff09\u2014\u2026'


def fix_punct(s):
    s = re.sub('([' + CJK + r'])[ \t]*,[ \t]*([' + CJK + r'])', r'\1，\2', s)
    s = re.sub('([' + CJK + r'])[ \t]*;[ \t]*([' + CJK + r'])', r'\1；\2', s)
    s = re.sub('([' + CJK + r'])[ \t]*:[ \t]*([' + CJK + r'])', r'\1：\2', s)
    s = re.sub('([' + CJK + r'])[ \t]*\?[ \t]*([' + CJK + r'])', r'\1？\2', s)
    # 全角标点前误留的空格（多来自 LaTeX 残留两侧）
    s = re.sub(r' +([。，；：？！）】》」』])', r'\1', s)
    # 内容为纯中文/数字的半角括号转全角
    s = re.sub(r'\(([^()]{1,60})\)',
               lambda m: '（' + m.group(1) + '）'
               if re.search(r'[\u4e00-\u9fff]', m.group(1))
               and not re.search(r'[A-Za-z]', m.group(1)) else m.group(0), s)
    return s


def clean_text(s):
    for a, b in INLINE_FIXES:
        s = s.replace(a, b)
    s = demath(s)
    s = fix_punct(s)
    # 段尾粘连的页码（"……这也 8"）
    s = re.sub(r'(?<=[\u4e00-\u9fff，、；]) \d{1,3}$', '', s)
    # 行内多余空白（汉字之间的零散空格）
    s = re.sub('([' + CJK + r']) +([' + CJK + r'])', r'\1\2', s)
    s = re.sub(' {2,}', ' ', s)
    return s.strip()


def to_html(s):
    """转义并注入行内标记（脚注上标等）。"""
    s = H.escape(s, quote=False)
    s = re.sub(r'([①②③④⑤])', r'<sup class="fn">\1</sup>', s)
    s = re.sub(r'(\*+)', lambda m: '<sup class="fn">' + m.group(1) + '</sup>', s)
    return s


TERMINAL = set('。！？：；…”』」）】》?!')
MERGE_END = re.compile('[' + CJK + r']$|，$|、$|；$')


def mergeable_end(t):
    if t[-1] not in TERMINAL and (MERGE_END.search(t) or re.search(r'\d$', t)):
        return True
    return False


# ---------------------------------------------------------------------------
# 解析
# ---------------------------------------------------------------------------

IMG_MAP = {  # url hash 前缀 → (svg key) 或 None(丢弃装饰图)
    '6ab8dcc6': None,               # 篇章装饰页
    '1962e732': None,               # 篇章装饰页
    '639d6cbb': 'three_categories',  # ch3 三分类
    'b9ae7a0f': 'cross_lines',      # ch3 交叉线
    '1071d23d': 'observers',        # ch4 观望者
    '190c338b': 'allies',           # ch4 同盟者
    'a085c396': 'leader_above',     # ch5 领导
    '7908147f': 'single_org',       # ch6 组织图叠加
    '56842d0d': 'voter_line',       # ch7 选民分布
    '6ddb90b5': 'three_candidates', # ch7 三候选人
    '3c69c0ea': 'b_prime',          # ch7 B′/B″
    'b61eb0b5': 'multiple_leaders', # ch8 多位领导
    '3a9e9211': 'colleagues',       # ch9 同僚
    'ada2f951': 'colleagues_dots',  # ch9 小黑点
    'eb729c19': 'matrix',           # ch24 十字形体制
}

FIG_CAPTIONS = {
    'three_categories': '等级制中的三大类：上级、平级、下级（参照政治人 P 居中）',
    'cross_lines': '交叉线示意图：与 P 横向距离越远，级别界限越宽',
    'observers': '圆圈之外的人即观望者',
    'allies': '同盟者：分处两条平行等级制、利益圈不相交',
    'leader_above': '领导居于参照政治人正上方',
    'single_org': '“政治人的世界”叠加到常见组织图上（无参与边界，正是问题所在）',
    'voter_line': '均匀分布的选民与位置 A′、B′、B、C',
    'three_candidates': '第一位候选人选 A、第二位选 B 后，B 右侧对第三位候选人更有利',
    'b_prime': 'B′（中点附近）与 B″（最右端）位置',
    'multiple_leaders': '多位领导：P 期望晋升到 y',
    'colleagues': '同僚：与 P 组织位置接近、足以加入其权力斗争的平级者',
    'colleagues_dots': '小黑点为其他政治人所处的位置',
    'matrix': '十字形体制（参谋制）：纵向指挥链与横向职能部门交叉',
}


def parse():
    lines = open(SRC, encoding='utf-8').read().split('\n')
    # 跳过文件头与原目录：从 "# 前言" 开始
    start = next(i for i, l in enumerate(lines) if l.strip() == '# 前言')
    chapters = {}   # key -> list of blocks
    order = []      # 章节顺序 key
    cur = None
    part_subtitle_pending = False

    for raw in lines[start:]:
        l = raw.strip()
        if not l:
            continue
        if re.fullmatch(r'\d{1,3}', l):          # 独立页码行
            continue
        if l.startswith('# '):
            title = l[2:].strip()
            title = re.sub(r'^\d{1,3}\s*', '', title)   # 如 "217 第二十三章"
            if title == '前言':
                cur = 'preface'
                chapters[cur] = []
                order.append(cur)
                continue
            if re.fullmatch(r'第[一二三四]篇', title):
                part_subtitle_pending = True     # 下一个短标题是篇名，跳过
                continue
            if part_subtitle_pending:
                part_subtitle_pending = False
                continue
            m = re.match(r'^第([一二三四五六七八九十]{1,3})章\s+(.*)$', title)
            if m and CN_NUM.get(m.group(1)):
                cur = 'ch%02d' % CN_NUM[m.group(1)]
                chapters[cur] = []
                order.append(cur)
                continue
            # 章内小节
            chapters[cur].append(('h2', clean_text(title)))
            continue
        m = re.match(r'^!\[[^\]]*\]\(([^)]+)\)', l)
        if m:
            url = m.group(1)
            h = url.rsplit('/', 1)[-1][:8]
            key = IMG_MAP.get(h, 'MISS')
            if key is None:
                continue
            chapters[cur].append(('fig', key))
            continue
        if re.match(r'^[①②③④⑤]', l):            # 脚注正文
            chapters[cur].append(('note', clean_text(l)))
            continue
        if l.startswith('$\\star$') or l.startswith('⋆'):   # 星号脚注正文
            body = clean_text(re.sub(r'^(\$\\star\$|⋆)\s*', '', l))
            chapters[cur].append(('note', '⋆ ' + body))
            continue
        chapters[cur].append(('p', l))
    return order, chapters


NUM_ITEM = re.compile(r'^[（(]\d+[）)]')


def merge_paragraphs(blocks):
    """合并被页码/脚注切断的段落（脚注块透明跳过）。"""
    out = []
    i = 0
    while i < len(blocks):
        kind, payload = blocks[i]
        if kind != 'p':
            out.append((kind, payload))
            i += 1
            continue
        text = payload
        num_head = bool(NUM_ITEM.match(payload))
        j = i + 1
        skipped = []
        while j < len(blocks):
            k2, p2 = blocks[j]
            if k2 == 'note':
                skipped.append((k2, p2))
                j += 1
                continue
            if (k2 == 'p' and not num_head and not NUM_ITEM.match(p2)
                    and mergeable_end(text) and re.match('^[\u4e00-\u9fff]', p2)):
                text += p2
                j += 1
                continue
            break
        out.append(('p', clean_text(text)))
        out.extend(skipped)      # 被跨越的脚注块按原顺序保留
        i = j
    return out


# ---------------------------------------------------------------------------
# SVG 示意图（按原书文字描述重绘）
# ---------------------------------------------------------------------------

SVG_STYLE = '''
  text { font-family: -apple-system, "PingFang SC", "Hiragino Sans GB", sans-serif;
         font-size: 13px; fill: #475569; }
  .lab { fill: #94a3b8; font-size: 12px; }
  .person { fill: #94a3b8; }
  .p-ref { fill: #6366f1; }
  .p-ring { fill: none; stroke: #6366f1; stroke-width: 1.5; }
  .ln { stroke: #cbd5e1; stroke-width: 1.2; fill: none; }
  .ln-d { stroke: #94a3b8; stroke-width: 1.2; stroke-dasharray: 5 4; fill: none; }
  .box { fill: #ffffff; stroke: #94a3b8; stroke-width: 1.2; rx: 6; }
  .box-t { fill: #334155; }
'''


def _dot(x, y, cls='person', r=6):
    return '<circle class="%s" cx="%d" cy="%d" r="%d"/>' % (cls, x, y, r)


def _ref(x, y):
    return ('<circle class="p-ring" cx="%d" cy="%d" r="11"/>' % (x, y)
            + _dot(x, y, 'p-ref', 7)
            + '<text x="%d" y="%d" text-anchor="middle" style="font-weight:600;fill:#6366f1">P</text>'
            % (x, y + 4))


def _txt(x, y, s, cls=''):
    return '<text class="%s" x="%d" y="%d" text-anchor="middle">%s</text>' % (cls, x, y, s)


def wrap_svg(elements, w=560, h=300):
    return ('<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img">'
            '<style>%s</style>%s</svg>') % (w, h, SVG_STYLE, ''.join(elements))


def svg_three_categories():
    e = []
    e += [_txt(280, 45, '上级（级别比他高的人）')]
    e.append('<line class="ln" x1="130" y1="70" x2="430" y2="70"/>')
    e += [_dot(180, 70), _dot(230, 70), _dot(330, 70), _dot(380, 70)]
    e.append('<line class="ln" x1="60" y1="160" x2="500" y2="160"/>')
    e += [_dot(130, 160), _dot(185, 160), _ref(280, 160), _dot(375, 160), _dot(430, 160)]
    e.append('<line class="ln" x1="130" y1="250" x2="430" y2="250"/>')
    e += [_dot(170, 250), _dot(225, 250), _dot(280, 250), _dot(335, 250), _dot(390, 250)]
    e += [_txt(280, 290, '下级（级别比他低的人）'),
          _txt(64, 164, '平级', 'lab'),
          _txt(64, 254, '下级', 'lab'),
          _txt(510, 74, '上级', 'lab')]
    return wrap_svg(e)


def svg_cross_lines():
    e = ['<line class="ln" x1="40" y1="160" x2="520" y2="160"/>',
         '<line class="ln-d" x1="120" y1="70" x2="440" y2="250"/>',
         '<line class="ln-d" x1="120" y1="250" x2="440" y2="70"/>']
    e += [_ref(280, 160)]
    e += [_txt(280, 40, '平级'), _txt(280, 285, '平级')]
    e += [_txt(90, 160, '远', 'lab'), _txt(470, 160, '远', 'lab')]
    e += [_txt(280, 115, '级别界限窄', 'lab'), _txt(280, 210, '级别界限窄', 'lab')]
    e += [_txt(115, 55, '界限宽', 'lab'), _txt(445, 55, '界限宽', 'lab'),
          _txt(115, 275, '界限宽', 'lab'), _txt(445, 275, '界限宽', 'lab')]
    return wrap_svg(e)


def svg_observers():
    e = ['<circle class="ln-d" cx="280" cy="160" r="95"/>']
    e += [_ref(280, 160), _dot(230, 120), _dot(330, 130), _dot(240, 205), _dot(330, 200)]
    e += [_dot(90, 70), _dot(470, 65), _dot(70, 250), _dot(480, 255), _dot(280, 35)]
    e += [_txt(140, 90, '观望者', 'lab'), _txt(420, 100, '观望者', 'lab'),
          _txt(120, 270, '观望者', 'lab'), _txt(430, 275, '观望者', 'lab'),
          _txt(280, 285, '圈内：直接参与者', 'lab')]
    return wrap_svg(e)


def svg_allies():
    e = ['<line class="ln" x1="40" y1="100" x2="520" y2="100"/>',
         '<line class="ln" x1="40" y1="220" x2="520" y2="220"/>']
    e += ['<circle class="p-ring" cx="190" cy="100" r="52" stroke-dasharray="0"/>',
          _ref(190, 100)]
    e += ['<circle cx="390" cy="220" r="52" fill="none" stroke="#10b981" stroke-width="1.5"/>',
          '<circle class="person" cx="390" cy="220" r="7"/>',
          _txt(390, 224, 'A', '')]
    e += [_txt(190, 30, '政治人所在的等级制', 'lab'),
          _txt(390, 285, '同盟者所在的等级制', 'lab'),
          _txt(292, 160, '两个利益圈不相交', 'lab')]
    return wrap_svg(e, h=310)


def svg_leader_above():
    e = ['<rect class="box" x="240" y="50" width="80" height="34" rx="6"/>',
         _txt(280, 72, '领导', 'box-t'),
         '<line class="ln" x1="280" y1="84" x2="280" y2="140"/>',
         _ref(280, 160)]
    e += [_dot(150, 160), _dot(205, 160), _dot(355, 160), _dot(410, 160)]
    e.append('<line class="ln" x1="120" y1="250" x2="440" y2="250"/>')
    e += [_dot(180, 250), _dot(240, 250), _dot(280, 250), _dot(330, 250), _dot(390, 250)]
    e += [_txt(64, 164, '平级', 'lab'), _txt(64, 254, '下级', 'lab'),
          _txt(280, 290, '领导居于参照政治人正上方', 'lab')]
    return wrap_svg(e)


def svg_single_org():
    e = ['<rect class="box" x="245" y="35" width="70" height="32" rx="6"/>',
         _txt(280, 56, 'A', 'box-t')]
    xs = [120, 205, 355, 440]
    for i, x in enumerate(xs, 1):
        e.append('<rect class="box" x="%d" y="115" width="64" height="32" rx="6"/>' % (x - 32))
        e.append(_txt(x, 136, 'B%d' % i, 'box-t'))
        e.append('<line class="ln" x1="280" y1="67" x2="%d" y2="115"/>' % x)
    e.append('<line class="ln" x1="355" y1="147" x2="355" y2="185"/>')
    e += [_ref(355, 205)]
    e.append('<line class="ln" x1="290" y1="235" x2="420" y2="235"/>')
    e += [_dot(310, 235), _dot(355, 235), _dot(400, 235)]
    e += [_txt(355, 270, 'B3 在 P 的上四分之一象限 → 单个领导；', 'lab'),
          _txt(355, 290, '若参与范围大到把 A 也圈进来 → 多位领导', 'lab')]
    return wrap_svg(e)


def svg_voter_line():
    e = ['<line class="ln" x1="50" y1="170" x2="510" y2="170"/>']
    for x in range(70, 500, 22):
        e.append('<line class="ln" x1="%d" y1="163" x2="%d" y2="177"/>' % (x, x))
    pts = [('A′', 130), ('B′', 230), ('B', 310), ('C', 440)]
    for name, x in pts:
        e.append('<circle cx="%d" cy="170" r="6" fill="#6366f1"/>' % x)
        e.append(_txt(x, 145, name, ''))
    e += [_txt(280, 60, '选民沿直线均匀分布（每道短竖线为一位选民）', 'lab'),
          _txt(310, 210, 'B：分布的中点', 'lab')]
    return wrap_svg(e)


def svg_three_candidates():
    e = ['<line class="ln" x1="50" y1="170" x2="510" y2="170"/>']
    for name, x in [('A', 170), ('B', 300), ('C', 400)]:
        e.append('<circle cx="%d" cy="170" r="6" fill="#6366f1"/>' % x)
        e.append(_txt(x, 145, name, ''))
    e.append('<path class="ln-d" d="M 315 170 L 500 170" transform="translate(0,-18)"/>')
    e += [_txt(170, 210, '第一位候选人', 'lab'), _txt(300, 210, '第二位候选人', 'lab'),
          _txt(400, 210, '第三位候选人', 'lab'),
          _txt(405, 120, 'B 右侧的位置更有利', 'lab')]
    return wrap_svg(e)


def svg_b_prime():
    e = ['<line class="ln" x1="50" y1="170" x2="510" y2="170"/>']
    for name, x in [('B′', 300), ('B″', 470)]:
        e.append('<circle cx="%d" cy="170" r="6" fill="#6366f1"/>' % x)
        e.append(_txt(x, 145, name, ''))
    e += [_txt(300, 210, '中点附近', 'lab'),
          _txt(470, 210, '最右端：不会被从右侧进场者击败', 'lab')]
    return wrap_svg(e)


def svg_multiple_leaders():
    e = []
    for x, y, t in [(160, 55, '领导1'), (300, 40, '领导2'), (440, 60, '领导3')]:
        e.append('<rect class="box" x="%d" y="%d" width="72" height="32" rx="6"/>' % (x - 36, y))
        e.append(_txt(x, y + 21, t, 'box-t'))
    e += [_ref(280, 200)]
    e.append('<path class="ln-d" d="M 300 185 C 360 150, 410 130, 440 96"/>')
    e.append('<path d="M 440 96 l -10 -2 l 4 10 z" fill="#94a3b8"/>')
    e.append('<circle cx="440" cy="110" r="4" fill="none" stroke="#10b981" stroke-width="1.5"/>')
    e += [_txt(465, 112, 'y', ''), _txt(280, 260, 'P 期望移动到 y：把一些领导变为同僚', 'lab')]
    return wrap_svg(e)


def svg_colleagues():
    e = ['<rect class="box" x="244" y="45" width="72" height="32" rx="6"/>',
         _txt(280, 66, '领导', 'box-t'),
         '<line class="ln" x1="280" y1="77" x2="280" y2="130"/>']
    e += [_dot(170, 160, 'p-ref', 6), _dot(390, 160, 'p-ref', 6)]
    e += [_txt(170, 140, '同僚', 'lab'), _txt(390, 140, '同僚', 'lab')]
    e += [_ref(280, 160)]
    e.append('<line class="ln" x1="230" y1="255" x2="330" y2="255"/>')
    e += [_dot(250, 255), _dot(280, 255), _dot(310, 255)]
    e += [_txt(280, 290, '同僚：位置接近到足以加入 P 的权力斗争', 'lab')]
    return wrap_svg(e)


def svg_colleagues_dots():
    e = []
    for x, y in [(140, 70), (420, 60)]:
        e.append('<rect class="box" x="%d" y="%d" width="64" height="30" rx="6"/>' % (x, y))
    e += [_txt(172, 90, '领导', 'lab'), _txt(452, 80, '领导', 'lab')]
    for x, y in [(110, 160), (200, 150), (250, 175), (360, 155), (450, 170),
                 (150, 240), (330, 245), (480, 235)]:
        e.append('<circle cx="%d" cy="%d" r="5"/>' % (x, y))
    e += [_ref(280, 205)]
    e += [_txt(530, 165, '小黑点＝', 'lab'), _txt(530, 182, '其他政治人', 'lab')]
    return wrap_svg(e)


def svg_matrix():
    e = []
    for y, t in [(50, '部门领导'), (135, '地域处室 1'), (220, '地域处室 2')]:
        e.append('<rect class="box" x="238" y="%d" width="84" height="34" rx="6"/>' % y)
        e.append(_txt(280, y + 22, t, 'box-t'))
        e.append('<line class="ln" x1="280" y1="%d" x2="280" y2="%d"/>' % (y + 34, y + 66))
    e.append('<line class="ln" x1="60" y1="300" x2="500" y2="300"/>')
    for x, t in [(110, '职能参谋 1'), (280, '职能参谋 2'), (450, '职能参谋 3')]:
        e.append('<rect class="box" x="%d" y="283" width="100" height="34" rx="6" fill="#f5f6f8"/>'
                 % (x - 50))
        e.append(_txt(x, 305, t, ''))
    e.append('<line class="ln-d" x1="280" y1="254" x2="280" y2="283"/>')
    e += [_txt(60, 40, '纵向指挥链', 'lab'), _txt(470, 340, '横向职能参谋线', 'lab')]
    return wrap_svg(e, h=350)


SVGS = {k: f for k, f in [
    ('three_categories', svg_three_categories), ('cross_lines', svg_cross_lines),
    ('observers', svg_observers), ('allies', svg_allies),
    ('leader_above', svg_leader_above), ('single_org', svg_single_org),
    ('voter_line', svg_voter_line), ('three_candidates', svg_three_candidates),
    ('b_prime', svg_b_prime), ('multiple_leaders', svg_multiple_leaders),
    ('colleagues', svg_colleagues), ('colleagues_dots', svg_colleagues_dots),
    ('matrix', svg_matrix),
]}

# ---------------------------------------------------------------------------
# HTML 模板
# ---------------------------------------------------------------------------

CSS = '''
:root {
  --bg:#fafbfc; --surface:#ffffff; --text:#1a1a2e; --text-2:#5a5a7a;
  --accent:#6366f1; --accent-2:#8b5cf6; --border:#e8eaef;
  --code-bg:#f1f3f5; --tag-bg:#eef0ff; --shadow:0 1px 3px rgba(0,0,0,.04);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  background:var(--bg); color:var(--text); line-height:1.8; -webkit-font-smoothing:antialiased;
}
.topbar {
  position:sticky; top:0; z-index:10; background:rgba(250,251,252,.85);
  backdrop-filter:blur(8px); border-bottom:1px solid var(--border);
}
.topbar-inner { max-width:760px; margin:0 auto; padding:10px 24px;
  display:flex; justify-content:space-between; align-items:center; }
.topbar .book { font-size:.85em; color:var(--text-2); }
.topbar .book a { color:var(--text); text-decoration:none; font-weight:600; }
.topbar nav a { color:var(--accent); text-decoration:none; font-size:.85em; margin-left:18px; }
.container { max-width:760px; margin:0 auto; padding:0 24px; }
.hero { padding:52px 0 34px; border-bottom:1px solid var(--border); margin-bottom:44px; }
.part-badge {
  display:inline-block; font-size:.78em; font-weight:600; letter-spacing:.05em;
  color:var(--accent); background:var(--tag-bg); border-radius:6px; padding:3px 10px; margin-bottom:14px;
}
.hero h1 {
  font-family:"Songti SC","Noto Serif SC","STSong",serif;
  font-size:1.7em; font-weight:700; letter-spacing:.01em; margin-bottom:10px;
}
.hero .meta { color:var(--text-2); font-size:.86em; display:flex; gap:14px; flex-wrap:wrap; }
.prose { padding-bottom:30px; }
.prose p {
  font-family:"Songti SC","Noto Serif SC","STSong",serif;
  font-size:1.02em; color:#2c2c44; text-align:justify; margin-bottom:1.15em;
}
.prose h2 {
  font-size:1.12em; font-weight:700; color:var(--text);
  margin:2.1em 0 1em; padding-left:12px; border-left:3px solid var(--accent);
}
.prose .num-item {
  font-family:"Songti SC","Noto Serif SC","STSong",serif;
  color:#2c2c44; margin-bottom:.45em; padding-left:1.2em; text-indent:-1.2em;
}
sup.fn { color:var(--accent); font-size:.72em; }
figure { margin:1.8em 0; text-align:center; }
figure svg { max-width:100%; height:auto; border:1px solid var(--border);
  border-radius:10px; background:var(--surface); box-shadow:var(--shadow); }
figcaption { font-size:.8em; color:var(--text-2); margin-top:8px; }
.notes {
  background:var(--surface); border:1px solid var(--border); border-radius:12px;
  padding:20px 26px; margin:36px 0 10px; box-shadow:var(--shadow);
}
.notes h3 { font-size:.92em; color:var(--text-2); letter-spacing:.08em; margin-bottom:10px; }
.notes p { font-size:.86em; color:var(--text-2); margin-bottom:.8em; text-align:justify; }
.navfoot { display:grid; grid-template-columns:1fr auto 1fr; gap:12px;
  margin:40px 0 20px; padding-top:28px; border-top:1px solid var(--border); }
.navfoot a {
  text-decoration:none; color:var(--text); background:var(--surface);
  border:1px solid var(--border); border-radius:10px; padding:14px 18px;
  font-size:.88em; transition:all .2s ease; box-shadow:var(--shadow);
}
.navfoot a:hover { border-color:var(--accent); transform:translateY(-1px); }
.navfoot .dir { display:block; font-size:.75em; color:var(--text-2); margin-bottom:2px; }
.navfoot .next { text-align:right; }
.navfoot .toc { display:flex; align-items:center; color:var(--accent); font-weight:600; }
.footer { padding:26px 0 40px; text-align:center; color:var(--text-2); font-size:.8em; }
.footer a { color:var(--accent); text-decoration:none; }
@media (max-width:600px){
  .hero h1{font-size:1.35em} .navfoot{grid-template-columns:1fr 1fr} .navfoot .toc{display:none}
}
'''

TOPBAR = '''
<div class="topbar"><div class="topbar-inner">
  <div class="book"><a href="../index.html">《官僚体制的政治》<span style="font-weight:400;color:var(--text-2)"> · 塔洛克</span></a></div>
  <nav><a href="../index.html">← 返回目录</a></nav>
</div></div>'''


def chapter_html(cid, blocks, fig_counter):
    notes = [p for k, p in blocks if k == 'note']
    body = []
    fig_no = 0
    for kind, payload in blocks:
        if kind == 'h2':
            body.append('<h2>%s</h2>' % to_html(payload))
        elif kind == 'fig':
            fig_no += 1
            svg = SVGS[payload]()
            body.append('<figure>%s<figcaption>图 %d　%s（依原书文字描述重绘）</figcaption></figure>'
                        % (svg, fig_no, FIG_CAPTIONS[payload]))
        elif kind == 'p':
            if NUM_ITEM.match(payload):
                body.append('<p class="num-item">%s</p>' % to_html(payload))
            else:
                body.append('<p>%s</p>' % to_html(payload))
    notes_html = ''
    if notes:
        items = ''.join('<p>%s</p>' % to_html(n) for n in notes)
        notes_html = '<div class="notes"><h3>注 释</h3>%s</div>' % items

    # 导航
    keys = ORDER
    idx = keys.index(cid)
    prev_id, next_id = (keys[idx - 1] if idx > 0 else None,
                        keys[idx + 1] if idx + 1 < len(keys) else None)

    def navcard(tid, cls, direction):
        if not tid:
            return '<span></span>'
        return ('<a class="%s" href="%s.html"><span class="dir">%s</span>%s</a>'
                % (cls, tid, direction, H.escape(CH_LABEL[tid], quote=False)))

    nav = ('<div class="navfoot">%s<a class="toc" href="../index.html">目录</a>%s</div>'
           % (navcard(prev_id, 'prev', '← 上一页'), navcard(next_id, 'next', '下一页 →')))

    if cid == 'preface':
        badge = '原书前言'
        h1 = '前言'
        meta = '<span>%s</span><span>%s</span>' % (BOOK_AUTHOR, PREFACE_AUTHOR + ' 撰')
    else:
        n = int(cid[2:])
        pid = CH_PART[n]
        badge = '%s · %s' % PARTS[pid]
        h1 = '第%s章　%s' % (CN_NUM_INV[n], CH_TITLES[n])
        meta = '<span>%s</span><span>%s</span>' % (BOOK_AUTHOR, BOOK_EN)

    return CHAPTER_TMPL % {
        'title': H.escape((h1 + ' · ' if cid != 'preface' else '') + BOOK_TITLE, quote=False),
        'css': CSS,
        'topbar': TOPBAR.replace('{id}', cid),
        'badge': badge,
        'h1': h1,
        'meta': meta,
        'body': '\n'.join(body),
        'notes': notes_html,
        'nav': nav,
    }


CHAPTER_TMPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s</title>
<style>%(css)s</style>
</head>
<body>
%(topbar)s
<div class="container">
  <div class="hero">
    <div class="part-badge">%(badge)s</div>
    <h1>%(h1)s</h1>
    <div class="meta">%(meta)s</div>
  </div>
  <div class="prose">
%(body)s
  </div>
  %(notes)s
  %(nav)s
  <div class="footer">《官僚体制的政治》笔记 · 由 OCR 整理本转换，已清理页码与排版残留 · <a href="../../index.html">返回笔记首页</a></div>
</div>
</body>
</html>
'''

CN_NUM_INV = {v: k for k, v in CN_NUM.items()}

TOC_TMPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s — 目录</title>
<style>%(css)s</style>
</head>
<body>
<div class="container">
  <div class="hero">
    <div class="part-badge">书籍精读 · %(en)s</div>
    <h1>%(title)s</h1>
    <div class="meta">
      <span>%(author)s</span><span>前言：詹姆斯·M. 布坎南</span><span>4 篇 · 25 章</span>
    </div>
    <p class="intro">%(intro)s</p>
  </div>
  %(parts)s
  <div class="footer">由 OCR 整理本转换为分章 HTML · 已清理页码与排版残留，插图按原书文字描述重绘 · <a href="../index.html">返回笔记首页</a></div>
</div>
</body>
</html>
'''

TOC_CSS = CSS + '''
.hero { padding:64px 0 40px; }
.intro { color:var(--text-2); font-size:.92em; margin-top:16px; max-width:640px; text-align:justify; }
.part { margin-bottom:34px; }
.part h2 {
  font-size:1.02em; font-weight:600; color:var(--text-2); letter-spacing:.04em;
  margin-bottom:12px; padding-bottom:10px; border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:10px;
}
.part h2 .dot { width:8px; height:8px; border-radius:50%; background:var(--accent); }
.ch-list { display:flex; flex-direction:column; }
.ch-row {
  display:flex; align-items:baseline; gap:14px; text-decoration:none; color:var(--text);
  padding:11px 16px; border-radius:10px; transition:background .15s ease;
}
.ch-row:hover { background:var(--surface); box-shadow:var(--shadow); }
.ch-row .no {
  font-size:.78em; color:var(--accent); font-weight:600; min-width:3.4em;
  font-variant-numeric:tabular-nums;
}
.ch-row .t { font-size:.98em; font-family:"Songti SC","Noto Serif SC",serif; }
.ch-row .arr { margin-left:auto; color:var(--accent); opacity:0; font-size:.85em; transition:opacity .15s ease; }
.ch-row:hover .arr { opacity:1; }
.preface-row .no { color:#10b981; }
'''


def toc_html():
    parts_html = []
    # 前言单独一组
    rows = ['<a class="ch-row preface-row" href="chapters/preface.html" id="ch-preface">'
            '<span class="no">前言</span><span class="t">布坎南序：政治人、经济人与官僚体制的效率</span>'
            '<span class="arr">&rarr;</span></a>']
    parts_html.append('<div class="part"><h2><span class="dot"></span>原书前言</h2>'
                      '<div class="ch-list">%s</div></div>' % ''.join(rows))
    for pid, (pn, pt) in PARTS.items():
        rows = []
        for n in range(1, 26):
            if CH_PART[n] != pid:
                continue
            cid = 'ch%02d' % n
            rows.append('<a class="ch-row" href="chapters/%s.html" id="ch-%s">'
                        '<span class="no">第%s章</span><span class="t">%s</span>'
                        '<span class="arr">&rarr;</span></a>'
                        % (cid, cid, CN_NUM_INV[n], H.escape(CH_TITLES[n], quote=False)))
        parts_html.append('<div class="part"><h2><span class="dot"></span>%s　%s</h2>'
                          '<div class="ch-list">%s</div></div>' % (pn, pt, ''.join(rows)))
    intro = ('公共选择学派奠基人之一戈登·塔洛克的代表作：不从"官僚是执行机器"的规范假设出发，'
             '而是以一个理性、有抱负、以晋升为目标的政治人为原子，重建等级制组织的运行逻辑——'
             '从领导的多种形态、同僚与追随者，到信息传递、控制手段与组织任务的天然限度，'
             '最后落到"该做些什么"。本笔记由中文译本 OCR 整理本转换为分章 HTML。')
    return TOC_TMPL % {
        'title': BOOK_TITLE, 'en': BOOK_EN, 'author': BOOK_AUTHOR,
        'css': TOC_CSS, 'intro': intro, 'parts': '\n  '.join(parts_html),
    }


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

ORDER = []
CH_LABEL = {}


def main():
    global ORDER, CH_LABEL
    order, chapters = parse()
    ORDER = order
    CH_LABEL = {'preface': '前言（布坎南）'}
    for n in range(1, 26):
        CH_LABEL['ch%02d' % n] = '第%s章 %s' % (CN_NUM_INV[n], CH_TITLES[n])

    os.makedirs(OUT, exist_ok=True)
    fig_total = 0
    for cid in order:
        blocks = merge_paragraphs(chapters[cid])
        fig_total += sum(1 for k, _ in blocks if k == 'fig')
        path = os.path.join(OUT, cid + '.html')
        open(path, 'w', encoding='utf-8').write(chapter_html(cid, blocks, None))
        n_p = sum(1 for k, _ in blocks if k == 'p')
        print('%-10s %3d 段  %d 图  %d 注  %6d B' % (
            cid, n_p,
            sum(1 for k, _ in blocks if k == 'fig'),
            sum(1 for k, _ in blocks if k == 'note'),
            os.path.getsize(path)))
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(toc_html())
    print('TOC →', os.path.join(ROOT, 'index.html'))
    print('figures total:', fig_total)


if __name__ == '__main__':
    main()
