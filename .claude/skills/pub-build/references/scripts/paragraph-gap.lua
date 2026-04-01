-- Pandoc Lua 필터: 연속된 문단(Para) 사이에만 #v(paragraph-gap) 삽입
-- 표, 코드블록, 이미지, heading 등 다른 블록 요소 사이에는 삽입하지 않음

function Blocks(blocks)
  local result = {}
  local prev_was_para = false

  for i, block in ipairs(blocks) do
    -- 이전 블록이 Para이고 현재 블록도 Para이면 간격 삽입
    if prev_was_para and block.t == "Para" then
      table.insert(result, pandoc.RawBlock("typst", "#v(paragraph-gap)"))
    end

    table.insert(result, block)
    prev_was_para = (block.t == "Para")
  end

  return result
end
