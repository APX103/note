-- filter.lua —— SMR-book Markdown→LaTeX 结构映射
-- 配合 Pandoc + 自定义 template.tex 使用

-- BlockQuote → epigraph 环境（朱砂左竖线 + 楷体）
function BlockQuote(el)
  -- el.content 是 list of Blocks，直接展开
  local blocks = { pandoc.RawBlock('latex', '\\begin{epigraph}') }
  for _, b in ipairs(el.content) do
    blocks[#blocks + 1] = b
  end
  blocks[#blocks + 1] = pandoc.RawBlock('latex', '\\end{epigraph}')
  return blocks
end

-- HorizontalRule → 丢弃（章首 --- 不需要）
function HorizontalRule()
  return {}
end

-- CodeBlock：默认用 verbatim 即可，pandoc 已经会处理。
-- 这里我们只对无标注的 code block 标注一下，确保走 verbatim 而不是 listings。
function CodeBlock(el)
  if el.attr.classes[1] == nil then
    -- 无语言标注：明确走 verbatim
    return pandoc.RawBlock('latex',
      '\\begin{verbatim}' .. el.text .. '\\end{verbatim}')
  end
  -- 有语言标注的（理论上全书没有），保留原样
  return nil
end

-- 让章首（level=1 header）触发换页
function Header(el)
  if el.level == 1 then
    return {
      pandoc.RawBlock('latex', '\\cleardoublepage'),
      el,
    }
  end
  return nil
end
