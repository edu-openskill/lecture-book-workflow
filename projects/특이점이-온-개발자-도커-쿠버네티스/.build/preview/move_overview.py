# -*- coding: utf-8 -*-
import io

md_path = r"C:\study\book-new\book-workflow\projects\특이점이-온-개발자-도커-쿠버네티스\chapters\03-Docker-다루기-v10.md"

with io.open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

start = text.index(u'<div class="svg-figure">\n<svg viewBox="0 0 820 320"')
end_marker = u"*그림 3-2. 챕터 3 한눈에 보기 - 전체 구조*"
end = text.index(end_marker) + len(end_marker)
block = text[start:end]

# 현재 위치(프렙 뒤)에서 블록 + 뒤 빈 줄 제거
assert text[end:end+2] == u"\n\n", repr(text[end:end+2])
text = text[:start] + text[end+2:]

# 목표 박스 위로 삽입
goal = u"\n\n:::goal\n"
idx = text.index(goal)
text = text[:idx] + u"\n\n" + block + text[idx:]

with io.open(md_path, "w", encoding="utf-8") as f:
    f.write(text)

print("done")
