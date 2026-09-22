# ZCODE.md

本仓库的完整维护规范在 **[AGENTS.md](AGENTS.md)**，添加新内容前先读它。速记版：

- 根目录只有 `index.html` + 7 个分类目录：`agent/` `llm/` `embedded/` `products/` `books/` `career/` `other/`，**新文章按主题放入分类目录，勿散放根目录**。
- 新文章 = 英文 kebab-case 文件名的单文件自包含 HTML；加入后必须在**该分类的 `index.html`** 加卡片（card 结构见 AGENTS.md），重要更新再补根 index「最新记录」。
- 勿动：`wandlink/`（私人，gitignore）、`embedded/magic-wand/wakenet/{.venv,data}`、`.obsidian/` 等工具目录。
- 2026-09-22 分类重构的备份：分支 `backup/pre-restructure-2026-09-22` + `../note-backup-2026-09-22.bundle`。
