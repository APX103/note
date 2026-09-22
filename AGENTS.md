# AGENTS.md — note 仓库维护指南

本仓库是个人技术笔记库：主体是**单文件自包含 HTML 文章**，另有书籍精读（Markdown 章节 + LaTeX 工程）和少量项目代码。2026-09-22 完成过一次全库分类重构（见文末「历史与备份」）。

## 目录结构（一级分类，勿在根目录散放文件）

| 目录 | 内容 | 判定规则（新文章放哪） |
|---|---|---|
| `agent/` | AI Agent：架构、多智能体、框架源码分析（Claude Code / Kimi / ADK）、A2A、沙箱、MCP | 凡以 Agent / LLM 应用工程 / 协议平台为主题的研究、调研、设计 |
| `llm/` | 模型侧技术：注意力、MoE、推理优化 | 讲模型结构 / 推理系统本身，而非 Agent 应用的 |
| `embedded/` | 嵌入式与硬件：ESP32 / M5StickS3 / STM32 / HiSpark 开发实录、教程、调研、仿真 | 开发板、固件、烧录、外设驱动、嵌入式仿真/游戏引擎 |
| `products/` | 产品全栈方案（多文档项目） | 一个产品从 PRD 到 GTM 的成套方案（如 kids-voice-toy、vibecoding-wand） |
| `books/` | 书籍精读（每本书一个目录：md 章节 + build.py + PDF） | 整本书的精读 / 翻译 / 排版工程 |
| `career/` | 职业发展、学习路线图 | 不属于技术的成长 / 路线图类 |
| `other/` | 杂项（XML 导出、示意图、Obsidian 插件配置） | 无主文件的兜底，能用前面分类就别放这 |

子目录专题：大类内可建子目录放系列（先例：`agent/a2a/`、`agent/agentpanel/`、`embedded/stm32h743-openmv-camera/`）。

## 新增文章标准流程

1. **命名**：英文 kebab-case 或 snake_case（如 `esp32-wakenet-diy-tutorial.html`），与库内风格一致；不要用空格。
2. **放入分类目录**（按上表判定），单文件自包含：CSS 内联、图片用相对路径或内嵌，不依赖站外资源。
3. **更新该分类的 `index.html`**：在合适的 section 里加一张卡片，格式固定（`data-date` 填文章最后修改日期，排序用）：
   ```html
   <a class="card" data-date="2026-09-22" href="文件名.html">
       <div class="card-title"><span class="arrow">&rarr;</span> 标题</div>
       <div class="card-desc"><span class="tag">标签</span> 一句话描述</div>
   </a>
   ```
4. 检查文中若有指向库内其他文章的相对链接，路径要带对目录层级。

## Index 页面的动态机制（2026-09-22 起）

- **分类页**：页尾内嵌脚本自动按各 section 网格内的实际卡片数重算 `(N)` 计数 — 加卡片后**无需手改计数**。
- **根页**：内嵌脚本 fetch 各分类 `index.html`，自动重算「分类导览」的篇数徽章，并按卡片 `data-date` 全局排序重建「最新记录」前 8 篇 — 加文章后**无需手改根页**。
- **file:// 降级**：直接双击打开时浏览器禁止 fetch，根页显示生成时的静态快照（分类页计数仍自动）。因此**新分类/大批量变动时建议顺手刷新根页静态快照**，日常加一篇则可跳过。
- 「最新记录」按**最后修改时间**排序；纯路径维护类改动（如修链接）不应顶到最前，必要时可用 `touch -t YYYYMMDDHHMM` 修正文件 mtime 后同步 `data-date`。

页面风格沿用现有 index 的深色卡片样式（CSS 直接从任一 `分类/index.html` 复制）。

## 勿动清单

- `wandlink/` — 私人项目，已 gitignore，**永不入库、永不移动**。
- `embedded/magic-wand/wakenet/.venv/` 与 `.../data/` — gitignored（训练数据可再生，README 有复现命令）。
- `.obsidian/`、`.claude/`、`.zcode/` — 编辑器/工具状态。
- `books/*/build/` — LaTeX 构建产物，由各书目录的 `build.py` 重新生成。

## 已知历史问题（不必修）

- `agent/agentpanel/` 两篇 HTML 引用的 `image/*.png` 在入库时就不存在（原文档截取自未入库的外部项目），保持原样。

## 历史与备份（2026-09-22 重构）

- 重构前所有文章平铺在根目录；本次按主题归入 7 个分类目录（`git mv`，历史保留），并重建了两层 index 导览。
- 备份：本地分支 `backup/pre-restructure-2026-09-22` + 仓库外完整 bundle `../note-backup-2026-09-22.bundle`（`git clone ../note-backup-2026-09-22.bundle` 即可恢复）。
