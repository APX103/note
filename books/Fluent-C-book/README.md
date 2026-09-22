# Fluent C

《Fluent C》— Christopher Preschern, O'Reilly Media, 2022.

本目录是从 EPUB（`~/Documents/Fluent_C.epub`）转换出的全书 Markdown 版本，供 AI / 全文检索使用。原书为英文。

## 全书结构（C 语言设计模式）

**Part I. C Patterns**（`Part_01_C_Patterns.md`）

| 章节 | 文件 | 主题 |
|---|---|---|
| 1 | [Chapter_01_Error_Handling.md](Chapter_01_Error_Handling.md) | 错误处理：Function Split、Guard Clause、Samurai Principle、Goto Error Handling、Cleanup Record、Object-Based Error Handling |
| 2 | [Chapter_02_Returning_Error_Information.md](Chapter_02_Returning_Error_Information.md) | 返回错误信息：Return Status Codes、Return Relevant Errors、Special Return Values、Log Errors |
| 3 | [Chapter_03_Memory_Management.md](Chapter_03_Memory_Management.md) | 内存管理：Stack First、Eternal Memory、Lazy Cleanup、Dedicated Ownership、Allocation Wrapper、Pointer Check、Memory Pool |
| 4 | [Chapter_04_Returning_Data_from_C_Functions.md](Chapter_04_Returning_Data_from_C_Functions.md) | 从 C 函数返回数据 |
| 5 | [Chapter_05_Data_Lifetime_and_Ownership.md](Chapter_05_Data_Lifetime_and_Ownership.md) | 数据生命周期与所有权 |
| 6 | [Chapter_06_Flexible_APIs.md](Chapter_06_Flexible_APIs.md) | 灵活的 API 设计 |
| 7 | [Chapter_07_Flexible_Iterator_Interfaces.md](Chapter_07_Flexible_Iterator_Interfaces.md) | 灵活的迭代器接口 |
| 8 | [Chapter_08_Organizing_Files_in_Modular_Programs.md](Chapter_08_Organizing_Files_in_Modular_Programs.md) | 模块化程序的文件组织 |
| 9 | [Chapter_09_Escaping_ifdef_Hell.md](Chapter_09_Escaping_ifdef_Hell.md) | 逃离 #ifdef 地狱（跨平台抽象层） |

**Part II. Pattern Stories**（`Part_02_Pattern_Stories.md`）

| 章节 | 文件 | 主题 |
|---|---|---|
| 10 | [Chapter_10_Implementing_Logging_Functionality.md](Chapter_10_Implementing_Logging_Functionality.md) | 实战：逐步实现日志系统 |
| 11 | [Chapter_11_Building_a_User_Management_System.md](Chapter_11_Building_a_User_Management_System.md) | 实战：构建用户管理系统 |
| 12 | [Chapter_12_Conclusion.md](Chapter_12_Conclusion.md) | 总结 |

其他：[Preface.md](Preface.md)（前言，含全书模式总览）、[Index.md](Index.md)（术语索引，链接指向各章）。

## 转换说明

- 工具：`pandoc -f html -t gfm-raw_html --wrap=none`，逐章转换自 EPUB 内的 HTML。
- 图片在 `images/`（含封面 `cover.png` 与各章插图 `fluc_XXXX.png`），文内引用已改为相对路径。
- 已去除每页末尾的 OceanofPDF 水印；跨章链接已改写为指向本章 Markdown 文件（原文内锚点不保留）。
- 代码块、表格均为 GFM 格式，可直接被 AI 阅读。
