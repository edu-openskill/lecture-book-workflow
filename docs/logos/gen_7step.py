#!/usr/bin/env python3
"""OpenSkillBooks Logo — 7단계 프로세스

블로그 '로고 제작 7가지 단계'를 그대로 적용.
각 단계의 결과물을 SVG로 생성하고, HTML 프리뷰로 진행 과정을 보여준다.

STEP 1. 브랜드 아이덴티티 → 슬로건/이념 확정 (텍스트)
STEP 2. 디자인 디깅 → 경쟁사 분석 (텍스트)
STEP 3. 스타일 & 색감 → 색상 팔레트 확정 (SVG 팔레트)
STEP 4. 서체 활용 → 4가지 서체 스타일 비교 (SVG)
STEP 5. 형태 활용 → 4가지 아이콘 형태 비교 (SVG)
STEP 6. 스케치 → 제작 → 서체+형태 조합 최종 후보 (SVG)
STEP 7. 브랜딩 활용 → 컬러 베리에이션 + 활용 예시 (SVG)
"""
import os

DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DIR, "7step")
os.makedirs(OUT, exist_ok=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 3: 색상 팔레트
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PALETTES = {
    "A": {"name": "Black + Teal", "main": "#1A1A1A", "accent": "#008080", "light": "#B2DFDB"},
    "B": {"name": "Navy + Sky",   "main": "#1A237E", "accent": "#4FC3F7", "light": "#B3E5FC"},
    "C": {"name": "Teal + Amber", "main": "#006666", "accent": "#B4781E", "light": "#FFE0B2"},
    "D": {"name": "Mono",         "main": "#2D2D2D", "accent": "#888888", "light": "#E0E0E0"},
}

def step3_palette():
    """STEP 3: 색상 팔레트 비교 SVG"""
    rows = ""
    y = 10
    for key, p in PALETTES.items():
        rows += f'''
    <text x="10" y="{y+18}" font-family="'Pretendard',sans-serif" font-size="13" font-weight="600" fill="#333">Palette {key}: {p['name']}</text>
    <rect x="200" y="{y}" width="60" height="28" rx="4" fill="{p['main']}"/>
    <rect x="268" y="{y}" width="60" height="28" rx="4" fill="{p['accent']}"/>
    <rect x="336" y="{y}" width="60" height="28" rx="4" fill="{p['light']}"/>
    <text x="215" y="{y+18}" font-family="monospace" font-size="9" fill="white">{p['main']}</text>
    <text x="278" y="{y+18}" font-family="monospace" font-size="9" fill="white">{p['accent']}</text>
    <text x="346" y="{y+18}" font-family="monospace" font-size="9" fill="#333">{p['light']}</text>'''
        y += 40
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 175">
  <rect width="420" height="175" fill="white" rx="8"/>
  {rows}
</svg>'''
    with open(os.path.join(OUT, "step3-palette.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 4: 서체 활용 — 4가지 서체 비교
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def step4_fonts():
    """STEP 4: 서체 스타일 비교"""
    fonts = [
        ("4a", "Serif", "'Georgia','Palatino','Times New Roman',serif", "700", "3",
         "OPENSKILLBOOKS", "전문적, 전통적 느낌. O'Reilly/Manning 스타일"),
        ("4b", "Sans-serif", "'Pretendard','SF Pro Display','Helvetica',sans-serif", "800", "2",
         "OPENSKILLBOOKS", "깔끔, 현대적. Packt/한빛미디어 스타일"),
        ("4c", "Monospace", "'SF Mono','Fira Code','JetBrains Mono',monospace", "700", "1",
         "OPENSKILLBOOKS", "코드/개발자 느낌. 기술서 차별화"),
        ("4d", "Mixed Weight", "'Pretendard','SF Pro Display',sans-serif", "300", "2",
         "OPEN|SKILL|BOOKS", "무게감 대비로 시선 유도"),
    ]

    for fid, label, family, weight, spacing, text, desc in fonts:
        if "|" in text:
            parts = text.split("|")
            text_el = f'''<tspan font-weight="300">{parts[0]}</tspan><tspan font-weight="900">{parts[1]}</tspan><tspan font-weight="300">{parts[2]}</tspan>'''
        else:
            text_el = text

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 100">
  <rect width="480" height="100" fill="white" rx="8"/>
  <text x="12" y="18" font-family="'Pretendard',sans-serif" font-size="11" fill="#888">{label}</text>
  <text x="240" y="58" text-anchor="middle" font-family={family}
        font-size="34" font-weight="{weight}" letter-spacing="{spacing}" fill="#1A1A1A">{text_el}</text>
  <text x="240" y="88" text-anchor="middle" font-family="'Pretendard',sans-serif"
        font-size="11" fill="#999">{desc}</text>
</svg>'''
        with open(os.path.join(OUT, f"step4-font-{fid}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 5: 형태 활용 — 4가지 아이콘 형태
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def step5_shapes():
    """STEP 5: 아이콘 형태 비교"""
    m, a = "#1A1A1A", "#008080"

    # 5a: 도형화 — 코드 페이지
    svg_5a = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <rect width="200" height="200" fill="white" rx="8"/>
  <text x="100" y="20" text-anchor="middle" font-family="'Pretendard',sans-serif" font-size="11" fill="#888">5-1. 도형화 (코드 페이지)</text>
  <g transform="translate(55,30) scale(1.1)">
    <path d="M 15 5 L 62 5 L 75 18 L 75 95 L 15 95 Z"
          fill="white" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <path d="M 62 5 L 62 18 L 75 18"
          fill="none" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <line x1="25" y1="32" x2="58" y2="32" stroke="{a}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
    <line x1="29" y1="44" x2="62" y2="44" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.35"/>
    <line x1="25" y1="56" x2="52" y2="56" stroke="{a}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
    <line x1="29" y1="68" x2="56" y2="68" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.35"/>
    <polyline points="30,80 22,86 30,92" fill="none" stroke="{m}" stroke-width="2.2"
              stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
    <line x1="37" y1="79" x2="47" y2="93" stroke="{m}" stroke-width="1.8" stroke-linecap="round" opacity="0.45"/>
    <polyline points="54,80 62,86 54,92" fill="none" stroke="{m}" stroke-width="2.2"
              stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
  </g>
  <text x="100" y="160" text-anchor="middle" font-family="'Pretendard',sans-serif" font-size="10" fill="#666">문서 + 코드라인 + 꺾쇠 브래킷</text>
  <text x="100" y="178" text-anchor="middle" font-family="'Pretendard',sans-serif" font-size="10" fill="#999">기술서 출판사 정체성 직관적 표현</text>
</svg>'''

    # 5b: 엠블럼 — 원형 배지 안에 책+코드
    svg_5b = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <rect width="200" height="200" fill="white" rx="8"/>
  <text x="100" y="20" text-anchor="middle" font-family="'Pretendard',sans-serif" font-size="11" fill="#888">5-2. 엠블럼 (원형 배지)</text>
  <g transform="translate(100,100)">
    <circle cx="0" cy="0" r="62" fill="none" stroke="{m}" stroke-width="2.5"/>
    <circle cx="0" cy="0" r="55" fill="none" stroke="{m}" stroke-width="1"/>
    <path d="M -18 -20 Q -22 -24, -28 -18 L -28 18 Q -22 22, -18 16 Z"
          fill="none" stroke="{a}" stroke-width="2" stroke-linejoin="round"/>
    <path d="M -18 -20 Q -14 -24, -8 -18 L -8 18 Q -14 22, -18 16 Z"
          fill="white" stroke="{a}" stroke-width="2" stroke-linejoin="round"/>
    <polyline points="6,-8 2,-2 6,4" fill="none" stroke="{m}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <polyline points="18,-8 22,-2 18,4" fill="none" stroke="{m}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <line x1="10" y1="-10" x2="16" y2="6" stroke="{m}" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
    <text x="0" y="-38" text-anchor="middle" font-family="'Georgia',serif"
          font-size="9" letter-spacing="3" fill="{m}">OPENSKILL</text>
    <text x="0" y="48" text-anchor="middle" font-family="'Georgia',serif"
          font-size="9" letter-spacing="3" fill="{m}">BOOKS</text>
  </g>
  <text x="100" y="178" text-anchor="middle" font-family="'Pretendard',sans-serif" font-size="10" fill="#999">전통 + 권위 느낌, 레트로 스타일</text>
</svg>'''

    # 5c: 모노그램 — OSB 이니셜
    svg_5c = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <rect width="200" height="200" fill="white" rx="8"/>
  <text x="100" y="20" text-anchor="middle" font-family="'Pretendard',sans-serif" font-size="11" fill="#888">5-3. 모노그램 (이니셜)</text>
  <g transform="translate(100,95)">
    <text x="0" y="0" text-anchor="middle" font-family="'SF Mono','Fira Code',monospace"
          font-size="64" font-weight="900" fill="{m}" letter-spacing="-2">OSB</text>
    <line x1="-52" y1="14" x2="52" y2="14" stroke="{a}" stroke-width="1.5"/>
    <text x="0" y="32" text-anchor="middle" font-family="'Pretendard',sans-serif"
          font-size="9" letter-spacing="4" fill="{a}">OPENSKILLBOOKS</text>
  </g>
  <text x="100" y="178" text-anchor="middle" font-family="'Pretendard',sans-serif" font-size="10" fill="#999">간결, 파비콘/앱아이콘에 적합</text>
</svg>'''

    # 5d: 펼친 책 — 오픈북
    svg_5d = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <rect width="200" height="200" fill="white" rx="8"/>
  <text x="100" y="20" text-anchor="middle" font-family="'Pretendard',sans-serif" font-size="11" fill="#888">5-4. 펼친 책 (오픈북)</text>
  <g transform="translate(55,28) scale(1.1)">
    <path d="M 45 18 Q 38 14, 12 16 L 8 82 Q 38 78, 45 75 Z"
          fill="white" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <path d="M 45 18 Q 52 14, 78 16 L 82 82 Q 52 78, 45 75 Z"
          fill="white" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <line x1="17" y1="34" x2="38" y2="32" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
    <line x1="17" y1="46" x2="36" y2="44" stroke="{a}" stroke-width="1.5" stroke-linecap="round" opacity="0.35"/>
    <line x1="17" y1="58" x2="34" y2="56" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
    <line x1="52" y1="32" x2="73" y2="34" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
    <line x1="54" y1="44" x2="71" y2="46" stroke="{a}" stroke-width="1.5" stroke-linecap="round" opacity="0.35"/>
    <line x1="52" y1="56" x2="69" y2="58" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
    <circle cx="45" cy="10" r="3" fill="{a}" opacity="0.45"/>
  </g>
  <text x="100" y="160" text-anchor="middle" font-family="'Pretendard',sans-serif" font-size="10" fill="#666">펼친 책 + 코드 라인 + 스파클</text>
  <text x="100" y="178" text-anchor="middle" font-family="'Pretendard',sans-serif" font-size="10" fill="#999">따뜻하고 친근한 학습 이미지</text>
</svg>'''

    for name, svg in [("5a", svg_5a), ("5b", svg_5b), ("5c", svg_5c), ("5d", svg_5d)]:
        with open(os.path.join(OUT, f"step5-shape-{name}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 6: 스케치 -> 제작 — 서체 + 형태 조합
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def step6_combine():
    """STEP 6: 서체 x 형태 최종 후보 6종"""
    m, a = "#1A1A1A", "#008080"

    combos = []

    # 6-1: 코드페이지 + 모노스페이스 (테크 풀)
    combos.append(("6-1", "Code Page + Monospace", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 110">
  <rect width="480" height="110" fill="white" rx="8"/>
  <text x="12" y="16" font-family="'Pretendard',sans-serif" font-size="10" fill="#aaa">6-1. 도형화 + Monospace</text>
  <g transform="translate(8,14) scale(0.42)">
    <path d="M 15 5 L 62 5 L 75 18 L 75 95 L 15 95 Z" fill="white" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <path d="M 62 5 L 62 18 L 75 18" fill="none" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <line x1="25" y1="32" x2="58" y2="32" stroke="{a}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
    <line x1="29" y1="44" x2="62" y2="44" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.35"/>
    <line x1="25" y1="56" x2="52" y2="56" stroke="{a}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
    <line x1="29" y1="68" x2="56" y2="68" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.35"/>
    <polyline points="30,80 22,86 30,92" fill="none" stroke="{m}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
    <line x1="37" y1="79" x2="47" y2="93" stroke="{m}" stroke-width="1.8" stroke-linecap="round" opacity="0.45"/>
    <polyline points="54,80 62,86 54,92" fill="none" stroke="{m}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
  </g>
  <text x="55" y="50" font-family="'SF Mono','Fira Code',monospace" font-size="30" font-weight="800" letter-spacing="1.5" fill="{m}">OPENSKILLBOOKS</text>
  <line x1="55" y1="60" x2="460" y2="60" stroke="{a}" stroke-width="0.8" opacity="0.25"/>
  <text x="57" y="80" font-family="'Pretendard',sans-serif" font-size="12" letter-spacing="4" fill="{a}" opacity="0.6">Hands-on Dev Cookbook</text>
</svg>'''))

    # 6-2: 코드페이지 + 산세리프
    combos.append(("6-2", "Code Page + Sans-serif", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 110">
  <rect width="480" height="110" fill="white" rx="8"/>
  <text x="12" y="16" font-family="'Pretendard',sans-serif" font-size="10" fill="#aaa">6-2. 도형화 + Sans-serif</text>
  <g transform="translate(8,14) scale(0.42)">
    <path d="M 15 5 L 62 5 L 75 18 L 75 95 L 15 95 Z" fill="white" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <path d="M 62 5 L 62 18 L 75 18" fill="none" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <line x1="25" y1="32" x2="58" y2="32" stroke="{a}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
    <line x1="29" y1="44" x2="62" y2="44" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.35"/>
    <line x1="25" y1="56" x2="52" y2="56" stroke="{a}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
    <line x1="29" y1="68" x2="56" y2="68" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.35"/>
    <polyline points="30,80 22,86 30,92" fill="none" stroke="{m}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
    <line x1="37" y1="79" x2="47" y2="93" stroke="{m}" stroke-width="1.8" stroke-linecap="round" opacity="0.45"/>
    <polyline points="54,80 62,86 54,92" fill="none" stroke="{m}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
  </g>
  <text x="55" y="50" font-family="'Pretendard','SF Pro Display',sans-serif" font-size="32" font-weight="900" letter-spacing="2" fill="{m}">OPENSKILLBOOKS</text>
  <line x1="55" y1="60" x2="460" y2="60" stroke="{a}" stroke-width="0.8" opacity="0.25"/>
  <text x="57" y="80" font-family="'Pretendard',sans-serif" font-size="12" letter-spacing="5" fill="{a}" opacity="0.6">Open Skill Books</text>
</svg>'''))

    # 6-3: 엠블럼 + 세리프
    combos.append(("6-3", "Emblem + Serif", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 110">
  <rect width="480" height="110" fill="white" rx="8"/>
  <text x="12" y="16" font-family="'Pretendard',sans-serif" font-size="10" fill="#aaa">6-3. 엠블럼 + Serif</text>
  <g transform="translate(55,55)">
    <circle cx="0" cy="0" r="38" fill="none" stroke="{m}" stroke-width="2"/>
    <circle cx="0" cy="0" r="33" fill="none" stroke="{m}" stroke-width="0.8"/>
    <path d="M -10,-14 Q -13,-17 -17,-12 L -17,12 Q -13,16 -10,10 Z" fill="none" stroke="{a}" stroke-width="1.5" stroke-linejoin="round"/>
    <path d="M -10,-14 Q -7,-17 -3,-12 L -3,12 Q -7,16 -10,10 Z" fill="white" stroke="{a}" stroke-width="1.5" stroke-linejoin="round"/>
    <polyline points="5,-5 2,0 5,5" fill="none" stroke="{m}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    <polyline points="13,-5 16,0 13,5" fill="none" stroke="{m}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="0" y="-22" text-anchor="middle" font-family="'Georgia',serif" font-size="7" letter-spacing="2" fill="{m}">OPENSKILL</text>
    <text x="0" y="30" text-anchor="middle" font-family="'Georgia',serif" font-size="7" letter-spacing="2" fill="{m}">BOOKS</text>
  </g>
  <text x="130" y="48" font-family="'Georgia','Palatino',serif" font-size="30" font-weight="700" letter-spacing="3" fill="{m}">OPENSKILLBOOKS</text>
  <line x1="130" y1="58" x2="460" y2="58" stroke="{a}" stroke-width="0.6" opacity="0.3"/>
  <text x="132" y="78" font-family="'Georgia',serif" font-size="11" letter-spacing="6" fill="{a}" opacity="0.5">Cookbook Series</text>
</svg>'''))

    # 6-4: OSB 모노그램 + 모노스페이스
    combos.append(("6-4", "Monogram + Monospace", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 110">
  <rect width="480" height="110" fill="white" rx="8"/>
  <text x="12" y="16" font-family="'Pretendard',sans-serif" font-size="10" fill="#aaa">6-4. 모노그램 + Monospace</text>
  <g transform="translate(50,58)">
    <rect x="-38" y="-30" width="76" height="60" rx="8" fill="none" stroke="{m}" stroke-width="2"/>
    <text x="0" y="8" text-anchor="middle" font-family="'SF Mono','Fira Code',monospace"
          font-size="32" font-weight="900" fill="{m}">OSB</text>
  </g>
  <text x="110" y="48" font-family="'SF Mono','Fira Code',monospace" font-size="28" font-weight="700" letter-spacing="2" fill="{m}">OPENSKILLBOOKS</text>
  <line x1="110" y1="58" x2="460" y2="58" stroke="{a}" stroke-width="0.8" opacity="0.25"/>
  <text x="112" y="78" font-family="'SF Mono',monospace" font-size="11" letter-spacing="3" fill="{a}" opacity="0.55">&gt;_ hands-on dev cookbook</text>
</svg>'''))

    # 6-5: 오픈북 + 산세리프
    combos.append(("6-5", "Open Book + Sans-serif", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 110">
  <rect width="480" height="110" fill="white" rx="8"/>
  <text x="12" y="16" font-family="'Pretendard',sans-serif" font-size="10" fill="#aaa">6-5. 펼친 책 + Sans-serif</text>
  <g transform="translate(8,10) scale(0.42)">
    <path d="M 45 18 Q 38 14, 12 16 L 8 82 Q 38 78, 45 75 Z" fill="white" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <path d="M 45 18 Q 52 14, 78 16 L 82 82 Q 52 78, 45 75 Z" fill="white" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <line x1="17" y1="34" x2="38" y2="32" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
    <line x1="17" y1="46" x2="36" y2="44" stroke="{a}" stroke-width="1.5" stroke-linecap="round" opacity="0.35"/>
    <line x1="17" y1="58" x2="34" y2="56" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
    <line x1="52" y1="32" x2="73" y2="34" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
    <line x1="54" y1="44" x2="71" y2="46" stroke="{a}" stroke-width="1.5" stroke-linecap="round" opacity="0.35"/>
    <line x1="52" y1="56" x2="69" y2="58" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
    <circle cx="45" cy="10" r="3" fill="{a}" opacity="0.45"/>
  </g>
  <text x="55" y="50" font-family="'Pretendard','Apple SD Gothic Neo',sans-serif" font-size="32" font-weight="700" letter-spacing="1" fill="{m}">OpenSkillBooks</text>
  <text x="57" y="78" font-family="'Pretendard',sans-serif" font-size="12" letter-spacing="4" fill="{a}" opacity="0.55">Learn by Doing</text>
</svg>'''))

    # 6-6: Mixed weight 타이포 only
    combos.append(("6-6", "Mixed Weight Typography", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 110">
  <rect width="480" height="110" fill="white" rx="8"/>
  <text x="12" y="16" font-family="'Pretendard',sans-serif" font-size="10" fill="#aaa">6-6. 무게감 대비 타이포</text>
  <text x="240" y="52" text-anchor="middle" font-family="'Georgia','Palatino',serif" font-size="36" letter-spacing="4" fill="{m}">
    <tspan font-weight="300">OPEN</tspan><tspan font-weight="900">SKILL</tspan><tspan font-weight="300">BOOKS</tspan>
  </text>
  <line x1="60" y1="62" x2="420" y2="62" stroke="{a}" stroke-width="0.7"/>
  <text x="240" y="86" text-anchor="middle" font-family="'Georgia',serif" font-size="12" letter-spacing="10" fill="{a}" opacity="0.5">COOKBOOK</text>
</svg>'''))

    for cid, label, svg in combos:
        with open(os.path.join(OUT, f"step6-combo-{cid}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 7: 브랜딩 활용 — 컬러 베리에이션
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def step7_variations():
    """STEP 7: 최종 후보 1개(6-1)의 4컬러 베리에이션 + 다크 버전"""
    colors = [
        ("A", "#1A1A1A", "#008080"),
        ("B", "#1A237E", "#4FC3F7"),
        ("C", "#006666", "#B4781E"),
        ("D", "#2D2D2D", "#888888"),
    ]

    def make_logo(m, a, bg="white", text_sub_color=None):
        tc = text_sub_color or a
        return f'''<g transform="translate(8,10) scale(0.42)">
    <path d="M 15 5 L 62 5 L 75 18 L 75 95 L 15 95 Z" fill="{bg}" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <path d="M 62 5 L 62 18 L 75 18" fill="none" stroke="{m}" stroke-width="2.5" stroke-linejoin="round"/>
    <line x1="25" y1="32" x2="58" y2="32" stroke="{a}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
    <line x1="29" y1="44" x2="62" y2="44" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.35"/>
    <line x1="25" y1="56" x2="52" y2="56" stroke="{a}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
    <line x1="29" y1="68" x2="56" y2="68" stroke="{a}" stroke-width="1.8" stroke-linecap="round" opacity="0.35"/>
    <polyline points="30,80 22,86 30,92" fill="none" stroke="{m}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
    <line x1="37" y1="79" x2="47" y2="93" stroke="{m}" stroke-width="1.8" stroke-linecap="round" opacity="0.45"/>
    <polyline points="54,80 62,86 54,92" fill="none" stroke="{m}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
  </g>
  <text x="55" y="48" font-family="'SF Mono','Fira Code',monospace" font-size="28" font-weight="800" letter-spacing="1.5" fill="{m}">OPENSKILLBOOKS</text>
  <line x1="55" y1="58" x2="460" y2="58" stroke="{a}" stroke-width="0.8" opacity="0.25"/>
  <text x="57" y="76" font-family="'Pretendard',sans-serif" font-size="12" letter-spacing="4" fill="{tc}" opacity="0.6">Hands-on Dev Cookbook</text>'''

    # Light background versions
    for key, mc, ac in colors:
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 95">
  <rect width="500" height="95" fill="white" rx="6"/>
  {make_logo(mc, ac)}
</svg>'''
        with open(os.path.join(OUT, f"step7-light-{key}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)

    # Dark background versions
    for key, mc, ac in colors:
        light_m = "#FFFFFF" if key != "D" else "#E0E0E0"
        light_a = ac
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 95">
  <rect width="500" height="95" fill="#1a1a1a" rx="6"/>
  {make_logo(light_m, light_a, bg="#1a1a1a", text_sub_color=light_a)}
</svg>'''
        with open(os.path.join(OUT, f"step7-dark-{key}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HTML 프리뷰
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_html():
    html = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>OpenSkillBooks Logo - 7 Step Process</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Pretendard','Apple SD Gothic Neo',sans-serif; background:#f8f8f8; color:#333; max-width:900px; margin:0 auto; padding:30px 20px; }
  h1 { font-size:26px; text-align:center; margin-bottom:6px; }
  .sub { text-align:center; color:#888; font-size:13px; margin-bottom:40px; }
  .step { margin-bottom:50px; }
  .step-num { display:inline-block; background:#008080; color:white; font-size:12px; font-weight:700; padding:3px 10px; border-radius:12px; margin-bottom:8px; }
  .step h2 { font-size:20px; margin-bottom:12px; }
  .step p { font-size:14px; color:#555; line-height:1.7; margin-bottom:8px; }
  .step ul { font-size:14px; color:#555; line-height:1.8; margin:8px 0 16px 20px; }
  .step li { margin-bottom:4px; }
  .grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:16px 0; }
  .grid-4 { display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:12px; margin:16px 0; }
  .card { background:white; border-radius:10px; padding:12px; box-shadow:0 2px 8px rgba(0,0,0,0.06); }
  .card img { width:100%; height:auto; }
  .card-label { text-align:center; font-size:11px; color:#aaa; margin-top:6px; }
  .highlight { background:#e0f2f1; padding:12px 16px; border-radius:8px; margin:12px 0; font-size:14px; }
  .highlight strong { color:#00695c; }
  .divider { border:none; border-top:2px solid #e0e0e0; margin:40px 0; }
  .tag { display:inline-block; background:#e8f5e9; color:#2e7d32; font-size:11px; padding:2px 8px; border-radius:4px; }
</style>
</head>
<body>

<h1>OpenSkillBooks Logo Design</h1>
<p class="sub">7 Step Process</p>

<!-- STEP 1 -->
<div class="step">
  <span class="step-num">STEP 1</span>
  <h2>Brand Identity</h2>
  <div class="highlight">
    <strong>Slogan:</strong> "Follow along, and you'll build it"<br>
    <strong>Identity:</strong> Concise code + everyday analogies = hands-on tech books anyone can follow
  </div>
  <ul>
    <li><strong>Target:</strong> Developers who know the basics but need specific technology guides</li>
    <li><strong>Values:</strong> Concise, Code-first, Step-by-step, Practical</li>
    <li><strong>Naming:</strong> OpenSkillBooks = Open + Skill + Books</li>
    <li><strong>Personality:</strong> Developer-friendly, Modern, Trustworthy</li>
  </ul>
</div>

<!-- STEP 2 -->
<div class="step">
  <span class="step-num">STEP 2</span>
  <h2>Design Digging</h2>
  <p>IT tech book publishers research:</p>
  <ul>
    <li><strong>O'Reilly:</strong> Animal illustrations + Serif font (traditional, authoritative)</li>
    <li><strong>Manning:</strong> Historical figures + Serif (formal, academic)</li>
    <li><strong>Packt:</strong> Sans-serif + Geometric shapes (modern, tech)</li>
    <li><strong>Hanbit Media:</strong> Sans-serif + Clean layout (practical, Korean)</li>
    <li><strong>WikiBooks:</strong> Serif + Minimal (professional)</li>
  </ul>
  <div class="highlight">
    <strong>Differentiation:</strong> Code + Book fusion icon. No other publisher uses a "code document" as their icon. This directly communicates "technical hands-on book".
  </div>
</div>

<hr class="divider">

<!-- STEP 3 -->
<div class="step">
  <span class="step-num">STEP 3</span>
  <h2>Style & Color Palette</h2>
  <p>4 color palettes for different contexts (print, web, dark mode):</p>
  <div class="card" style="max-width:450px;margin:16px auto;">
    <img src="step3-palette.svg">
  </div>
</div>

<hr class="divider">

<!-- STEP 4 -->
<div class="step">
  <span class="step-num">STEP 4</span>
  <h2>Font Styles</h2>
  <p>4 font approaches compared:</p>
  <div class="grid-2">
    <div class="card"><img src="step4-font-4a.svg"><div class="card-label">Serif (traditional)</div></div>
    <div class="card"><img src="step4-font-4b.svg"><div class="card-label">Sans-serif (modern)</div></div>
    <div class="card"><img src="step4-font-4c.svg"><div class="card-label">Monospace (developer)</div></div>
    <div class="card"><img src="step4-font-4d.svg"><div class="card-label">Mixed weight (contrast)</div></div>
  </div>
</div>

<hr class="divider">

<!-- STEP 5 -->
<div class="step">
  <span class="step-num">STEP 5</span>
  <h2>Shape / Icon Concepts</h2>
  <p>4 icon shapes from the blog's categories:</p>
  <div class="grid-4">
    <div class="card"><img src="step5-shape-5a.svg"><div class="card-label">Geometric</div></div>
    <div class="card"><img src="step5-shape-5b.svg"><div class="card-label">Emblem</div></div>
    <div class="card"><img src="step5-shape-5c.svg"><div class="card-label">Monogram</div></div>
    <div class="card"><img src="step5-shape-5d.svg"><div class="card-label">Open Book</div></div>
  </div>
</div>

<hr class="divider">

<!-- STEP 6 -->
<div class="step">
  <span class="step-num">STEP 6</span>
  <h2>Sketch &rarr; Final Candidates</h2>
  <p>Font + Shape combinations (6 candidates):</p>
  <div class="grid-2">
    <div class="card"><img src="step6-combo-6-1.svg"><div class="card-label"><span class="tag">PICK</span> Code Page + Mono</div></div>
    <div class="card"><img src="step6-combo-6-2.svg"><div class="card-label">Code Page + Sans</div></div>
    <div class="card"><img src="step6-combo-6-3.svg"><div class="card-label">Emblem + Serif</div></div>
    <div class="card"><img src="step6-combo-6-4.svg"><div class="card-label">Monogram + Mono</div></div>
    <div class="card"><img src="step6-combo-6-5.svg"><div class="card-label">Open Book + Sans</div></div>
    <div class="card"><img src="step6-combo-6-6.svg"><div class="card-label">Mixed Weight Typo</div></div>
  </div>
</div>

<hr class="divider">

<!-- STEP 7 -->
<div class="step">
  <span class="step-num">STEP 7</span>
  <h2>Branding Application</h2>
  <p>Color variations for different contexts:</p>

  <h3 style="font-size:14px;color:#666;margin:16px 0 8px;">Light Background</h3>
  <div class="grid-2">
    <div class="card"><img src="step7-light-A.svg"><div class="card-label">A. Black + Teal</div></div>
    <div class="card"><img src="step7-light-B.svg"><div class="card-label">B. Navy + Sky</div></div>
    <div class="card"><img src="step7-light-C.svg"><div class="card-label">C. Teal + Amber</div></div>
    <div class="card"><img src="step7-light-D.svg"><div class="card-label">D. Mono</div></div>
  </div>

  <h3 style="font-size:14px;color:#666;margin:16px 0 8px;">Dark Background</h3>
  <div class="grid-2">
    <div class="card" style="background:#1a1a1a"><img src="step7-dark-A.svg"><div class="card-label" style="color:#666">A. White + Teal</div></div>
    <div class="card" style="background:#1a1a1a"><img src="step7-dark-B.svg"><div class="card-label" style="color:#666">B. White + Sky</div></div>
    <div class="card" style="background:#1a1a1a"><img src="step7-dark-C.svg"><div class="card-label" style="color:#666">C. White + Amber</div></div>
    <div class="card" style="background:#1a1a1a"><img src="step7-dark-D.svg"><div class="card-label" style="color:#666">D. Light Gray</div></div>
  </div>
</div>

</body>
</html>'''
    with open(os.path.join(OUT, "preview-7step.html"), "w", encoding="utf-8") as f:
        f.write(html)


def main():
    print("STEP 3: 색상 팔레트...")
    step3_palette()
    print("STEP 4: 서체 비교...")
    step4_fonts()
    print("STEP 5: 형태 비교...")
    step5_shapes()
    print("STEP 6: 조합 후보...")
    step6_combine()
    print("STEP 7: 컬러 베리에이션...")
    step7_variations()
    print("HTML 프리뷰 생성...")
    generate_html()
    print(f"\n7step/ 폴더에 생성 완료! preview-7step.html을 브라우저에서 열어보세요.")


if __name__ == "__main__":
    main()
