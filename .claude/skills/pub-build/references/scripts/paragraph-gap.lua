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

-- 블록이 이미지만 포함하는지 확인 (![](path) → Para[Image] 또는 Plain[Image])
local function is_image_block(block)
  if (block.t == "Para" or block.t == "Plain") and #block.content == 1 and block.content[1].t == "Image" then
    return true
  end
  return false
end

-- Para 블록이 이탤릭 캡션인지 확인 (*캡션 텍스트* → Para[Emph])
local function is_caption_para(block)
  if block.t == "Para" and #block.content >= 1 and block.content[1].t == "Emph" then
    return true
  end
  return false
end

function Blocks(blocks)
  local result = {}
  local prev_was_text = false
  local prev_was_image = false
  local prev_was_caption = false

  for i, block in ipairs(blocks) do
    -- 이미지 바로 뒤 이탤릭 캡션이면 gap 삽입하지 않음
    if prev_was_image and is_caption_para(block) then
      -- gap 없이 바로 이어붙임 (후처리에서 auto-image alt로 병합됨)
      table.insert(result, block)
      prev_was_text = false
      prev_was_image = false
      prev_was_caption = true
    -- 캡션 바로 뒤 문단이면 gap 삽입하지 않음 (figure 자체 여백 사용)
    elseif prev_was_caption and is_text_flow(block) then
      table.insert(result, block)
      prev_was_text = is_text_flow(block)
      prev_was_image = false
      prev_was_caption = false
    -- 이미지(캡션 없음) 바로 뒤 문단이면 gap 삽입하지 않음
    elseif prev_was_image and is_text_flow(block) then
      table.insert(result, block)
      prev_was_text = is_text_flow(block)
      prev_was_image = false
      prev_was_caption = false
    else
      if prev_was_text and is_text_flow(block) then
        table.insert(result, pandoc.RawBlock("typst", "#v(paragraph-gap)"))
      end
      table.insert(result, block)
      prev_was_text = is_text_flow(block)
      prev_was_image = is_image_block(block)
      prev_was_caption = false
    end
  end

  return result
end
