# -*- coding: utf-8 -*-
import re, io

md_path = r"C:\study\book-new\book-workflow\projects\특이점이-온-개발자-도커-쿠버네티스\chapters\03-Docker-다루기-v10.md"

with io.open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1) 기존 figure 번호 +1 (그림 3-2 이상만)
def inc(m):
    n = int(m.group(1))
    return "그림 3-%d" % (n + 1) if n >= 2 else m.group(0)

text = re.sub(r"그림 3-(\d+)", inc, text)

# 2) 677행 본문 참조: "그림 3-15와 3-16" -> 시프트 후 "그림 3-16와 3-16" -> 교정
assert "그림 3-16와 3-16을 보면" in text, "line-677 reference not found in expected form"
text = text.replace("그림 3-16와 3-16을 보면", "그림 3-16과 3-17을 보면")

# 3) 한눈에 보기(그림 3-2) 삽입 — '## 3.1 Dockerfile' 앞
overview = u'''<div class="svg-figure">
<svg viewBox="0 0 820 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="챕터 3 한눈에 보기: 브라우저 요청을 NGINX(챕터 3.2)가 받아 백엔드 두 대에 분배하고, 두 백엔드는 데이터 그룹의 공용 Redis(챕터 3.3)와 DB(챕터 3.4)를 함께 사용한다. 전체는 Docker Compose(챕터 3.5)로 묶인다">
  <defs>
    <marker id="ov-req" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#475569"/></marker>
    <marker id="ov-res" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#94a3b8"/></marker>
  </defs>
  <text x="410" y="26" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">챕터 3 한눈에 보기 — 전체 구조</text>
  <rect x="176" y="50" width="628" height="256" rx="12" fill="none" stroke="#475569" stroke-width="1.4" stroke-dasharray="6,4"/>
  <text x="192" y="70" font-size="11" font-weight="600" fill="#0f172a">Docker Compose 챕터 3.5</text>
  <rect x="28" y="162" width="104" height="52" rx="8" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <text x="80" y="193" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">브라우저</text>
  <rect x="196" y="162" width="112" height="52" rx="8" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <text x="252" y="184" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">NGINX</text>
  <text x="252" y="202" text-anchor="middle" font-size="10" font-weight="700" fill="#475569">챕터 3.2</text>
  <rect x="372" y="118" width="124" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <text x="434" y="148" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">백엔드1</text>
  <rect x="372" y="212" width="124" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <text x="434" y="242" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">백엔드2</text>
  <rect x="556" y="112" width="232" height="152" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3,2"/>
  <text x="574" y="130" font-size="10" font-style="italic" fill="#475569">데이터</text>
  <rect x="576" y="140" width="192" height="46" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="672" y="158" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Redis</text>
  <text x="672" y="175" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">챕터 3.3</text>
  <rect x="576" y="196" width="192" height="46" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="672" y="214" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">DB</text>
  <text x="672" y="231" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">챕터 3.4</text>
  <line x1="132" y1="184" x2="194" y2="184" stroke="#475569" stroke-width="1.6" marker-end="url(#ov-req)"/>
  <line x1="194" y1="193" x2="134" y2="193" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#ov-res)"/>
  <line x1="308" y1="176" x2="370" y2="150" stroke="#475569" stroke-width="1.6" marker-end="url(#ov-req)"/>
  <line x1="370" y1="160" x2="308" y2="186" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#ov-res)"/>
  <line x1="308" y1="200" x2="370" y2="230" stroke="#475569" stroke-width="1.6" marker-end="url(#ov-req)"/>
  <line x1="370" y1="222" x2="308" y2="192" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#ov-res)"/>
  <line x1="496" y1="150" x2="554" y2="184" stroke="#475569" stroke-width="1.6" marker-end="url(#ov-req)"/>
  <line x1="554" y1="193" x2="498" y2="160" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#ov-res)"/>
  <line x1="496" y1="232" x2="554" y2="194" stroke="#475569" stroke-width="1.6" marker-end="url(#ov-req)"/>
  <line x1="554" y1="203" x2="498" y2="242" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#ov-res)"/>
</svg>
</div>

*그림 3-2. 챕터 3 한눈에 보기 - 전체 구조*

'''

anchor = u"## 3.1 Dockerfile - 환경을 자동으로 만들기"
assert text.count(anchor) == 1, "anchor count != 1"
text = text.replace(anchor, overview + anchor, 1)

with io.open(md_path, "w", encoding="utf-8") as f:
    f.write(text)

print("done")
