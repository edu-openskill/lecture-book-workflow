-- Pandoc Lua 필터: 텍스트 흐름 블록 사이에 #v(paragraph-gap) 삽입
-- 표, 코드블록, 이미지, heading 등 독립 블록 요소 사이에는 삽입하지 않음
-- (독립 블록은 Typst에서 자체 block(above/below)로 여백 관리)

-- 텍스트 흐름 블록: 문단, 리스트 등 par(spacing)의 영향을 받는 요소
local function is_text_flow(block)
  local t = block.t
  return t == "Para" or t == "Plain"
      or t == "BulletList" or t == "OrderedList"
      or t == "DefinitionList" or t == "LineBlock"
end

function Blocks(blocks)
  local result = {}
  local prev_was_text = false

  for i, block in ipairs(blocks) do
    if prev_was_text and is_text_flow(block) then
      table.insert(result, pandoc.RawBlock("typst", "#v(paragraph-gap)"))
    end

    table.insert(result, block)
    prev_was_text = is_text_flow(block)
  end

  return result
end
