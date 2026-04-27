#!/usr/bin/env python3
"""OpenSkillBooks SVG Logo Generator v4

실습형 IT 기술서(Cookbook) 출판 브랜드.
핵심 가치: 따라하기, 간결, 코드+비유, 개발자 친화.

4 styles x 3 moods x 4 colors = 48 SVGs
"""
import os

DIR = os.path.dirname(os.path.abspath(__file__))

COLORS = {
    "C1": ("#1A1A1A", "#008080", "#00A89D"),
    "C2": ("#1A237E", "#4FC3F7", "#81D4FA"),
    "C3": ("#006666", "#B4781E", "#D4942A"),
    "C4": ("#2D2D2D", "#888888", "#AAAAAA"),
}

COLOR_NAMES = {
    "C1": "Black + Teal",
    "C2": "Navy + Sky",
    "C3": "Teal + Amber",
    "C4": "Mono",
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 아이콘 A: 코드 페이지 (테크/모던용)
# 접힌 모서리 문서 + 코드 라인 + </> 브래킷
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def icon_code_page(stroke, accent, sw="2.5", scale=1.0, ox=0, oy=0):
    return f'''<g transform="translate({ox},{oy}) scale({scale})">
      <path d="M 15 5 L 62 5 L 75 18 L 75 95 L 15 95 Z"
            fill="white" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>
      <path d="M 62 5 L 62 18 L 75 18"
            fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>
      <line x1="25" y1="32" x2="58" y2="32" stroke="{accent}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
      <line x1="29" y1="44" x2="62" y2="44" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" opacity="0.35"/>
      <line x1="25" y1="56" x2="52" y2="56" stroke="{accent}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
      <line x1="29" y1="68" x2="56" y2="68" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" opacity="0.35"/>
      <polyline points="30,80 22,86 30,92" fill="none" stroke="{stroke}" stroke-width="2.2"
                stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
      <line x1="37" y1="79" x2="47" y2="93" stroke="{stroke}" stroke-width="1.8"
            stroke-linecap="round" opacity="0.45"/>
      <polyline points="54,80 62,86 54,92" fill="none" stroke="{stroke}" stroke-width="2.2"
                stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
    </g>'''


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 아이콘 B: 펼친 책 (따뜻한/친근용)
# V자 오픈북 + 양쪽 코드 라인 + 상단 스파클
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def icon_open_book(stroke, accent, sw="2.5", scale=1.0, ox=0, oy=0):
    return f'''<g transform="translate({ox},{oy}) scale({scale})">
      <path d="M 45 18 Q 38 14, 12 16 L 8 82 Q 38 78, 45 75 Z"
            fill="white" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>
      <path d="M 45 18 Q 52 14, 78 16 L 82 82 Q 52 78, 45 75 Z"
            fill="white" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>
      <line x1="17" y1="34" x2="38" y2="32" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
      <line x1="17" y1="46" x2="36" y2="44" stroke="{accent}" stroke-width="1.5" stroke-linecap="round" opacity="0.35"/>
      <line x1="17" y1="58" x2="34" y2="56" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
      <line x1="52" y1="32" x2="73" y2="34" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
      <line x1="54" y1="44" x2="71" y2="46" stroke="{accent}" stroke-width="1.5" stroke-linecap="round" opacity="0.35"/>
      <line x1="52" y1="56" x2="69" y2="58" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
      <circle cx="45" cy="10" r="3" fill="{accent}" opacity="0.45"/>
    </g>'''


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 아이콘 C: 브래킷 프레임 (전문/신뢰용)
# { } 중괄호 프레임 + 코드 라인
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def icon_bracket_frame(stroke, accent, sw="2.8", scale=1.0, ox=0, oy=0):
    return f'''<g transform="translate({ox},{oy}) scale({scale})">
      <path d="M 32 8 Q 22 8, 18 16 L 18 38 Q 18 44, 10 48 Q 18 52, 18 58 L 18 80 Q 22 88, 32 88"
            fill="none" stroke="{stroke}" stroke-width="{sw}"
            stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M 58 8 Q 68 8, 72 16 L 72 38 Q 72 44, 80 48 Q 72 52, 72 58 L 72 80 Q 68 88, 58 88"
            fill="none" stroke="{stroke}" stroke-width="{sw}"
            stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="30" y1="32" x2="60" y2="32" stroke="{accent}" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
      <line x1="33" y1="48" x2="57" y2="48" stroke="{accent}" stroke-width="2.2" stroke-linecap="round" opacity="0.65"/>
      <line x1="30" y1="64" x2="54" y2="64" stroke="{accent}" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
    </g>'''


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S1: Combination Mark (심볼 + 텍스트)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def s1_m1(m, a, g):
    """테크/모던: 코드 페이지 아이콘 + 모노스페이스 워드마크"""
    icon = icon_code_page(m, a, "2.5", scale=0.95, ox=8, oy=10)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks</title>
  {icon}
  <g id="wordmark">
    <text x="105" y="55" font-family="'SF Mono','Fira Code','Pretendard',monospace"
          font-size="32" font-weight="800" letter-spacing="1.5" fill="{m}">OPENSKILLBOOKS</text>
    <text x="107" y="80" font-family="'Pretendard','SF Pro Display',sans-serif"
          font-size="12" font-weight="400" letter-spacing="5" fill="{a}" opacity="0.7">Hands-on Tech Books</text>
  </g>
</svg>'''


def s1_m2(m, a, g):
    """따뜻한/친근: 펼친 책 아이콘 + 라운드 폰트"""
    icon = icon_open_book(m, a, "2.5", scale=0.95, ox=8, oy=8)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks</title>
  {icon}
  <g id="wordmark">
    <text x="105" y="55" font-family="'Pretendard','Apple SD Gothic Neo',sans-serif"
          font-size="34" font-weight="700" letter-spacing="1" fill="{m}">OpenSkillBooks</text>
    <text x="107" y="82" font-family="'Pretendard',sans-serif"
          font-size="12" font-weight="400" letter-spacing="4" fill="{a}" opacity="0.6">Learn by Doing</text>
  </g>
</svg>'''


def s1_m3(m, a, g):
    """전문/신뢰: 브래킷 프레임 아이콘 + 세리프"""
    icon = icon_bracket_frame(m, a, "2.8", scale=0.95, ox=5, oy=8)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks</title>
  {icon}
  <g id="wordmark">
    <text x="100" y="52" font-family="'Georgia','Palatino','Times New Roman',serif"
          font-size="32" font-weight="700" letter-spacing="2" fill="{m}">OPENSKILLBOOKS</text>
    <text x="102" y="82" font-family="'Georgia','Palatino',serif"
          font-size="12" font-weight="400" letter-spacing="6" fill="{a}" opacity="0.6">Open Skill Books</text>
  </g>
</svg>'''


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S2: 타이포그래피 중심
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def s2_m1(m, a, g):
    """테크/모던: 모노스페이스 + 터미널 커서"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 100"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks</title>
  <text x="20" y="50" font-family="'SF Mono','Fira Code','JetBrains Mono',monospace"
        font-size="36" font-weight="800" letter-spacing="1" fill="{m}">OPENSKILLBOOKS</text>
  <rect x="488" y="24" width="3" height="32" fill="{a}" opacity="0.7">
    <animate attributeName="opacity" values="0.7;0.1;0.7" dur="1.2s" repeatCount="indefinite"/>
  </rect>
  <text x="22" y="78" font-family="'SF Mono','Fira Code',monospace"
        font-size="11" font-weight="400" letter-spacing="3" fill="{a}" opacity="0.55">&gt;_ hands-on dev cookbook</text>
</svg>'''


def s2_m2(m, a, g):
    """따뜻한/친근: 라운드 타이포 + 스텝 도트 연결"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 110"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks</title>
  <text x="260" y="48" text-anchor="middle"
        font-family="'Pretendard','Apple SD Gothic Neo',sans-serif"
        font-size="38" font-weight="700" letter-spacing="1" fill="{m}">OpenSkillBooks</text>
  <line x1="100" y1="68" x2="180" y2="68" stroke="{a}" stroke-width="1" opacity="0.25" stroke-linecap="round"/>
  <circle cx="190" cy="68" r="3.5" fill="{a}" opacity="0.35"/>
  <line x1="200" y1="68" x2="250" y2="68" stroke="{a}" stroke-width="1" opacity="0.3" stroke-linecap="round"/>
  <circle cx="260" cy="68" r="4" fill="{a}" opacity="0.6"/>
  <line x1="270" y1="68" x2="320" y2="68" stroke="{a}" stroke-width="1" opacity="0.3" stroke-linecap="round"/>
  <circle cx="330" cy="68" r="3.5" fill="{a}" opacity="0.35"/>
  <line x1="340" y1="68" x2="420" y2="68" stroke="{a}" stroke-width="1" opacity="0.25" stroke-linecap="round"/>
  <text x="260" y="96" text-anchor="middle"
        font-family="'Pretendard',sans-serif"
        font-size="11" font-weight="400" letter-spacing="8" fill="{a}" opacity="0.45">STEP BY STEP</text>
</svg>'''


def s2_m3(m, a, g):
    """전문/신뢰: OPEN(thin) SKILL(bold) BOOKS(thin) + 라인"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 110"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks</title>
  <text x="260" y="46" text-anchor="middle"
        font-family="'Georgia','Palatino','Times New Roman',serif"
        font-size="36" letter-spacing="5" fill="{m}">
    <tspan font-weight="300">OPEN</tspan><tspan font-weight="900">SKILL</tspan><tspan font-weight="300">BOOKS</tspan>
  </text>
  <line x1="80" y1="58" x2="440" y2="58" stroke="{a}" stroke-width="0.7"/>
  <text x="260" y="84" text-anchor="middle"
        font-family="'Georgia','Palatino',serif"
        font-size="13" font-weight="400" letter-spacing="12" fill="{a}" opacity="0.5">COOKBOOK</text>
</svg>'''


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S3: 아이콘만 (텍스트 없음)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def s3_m1(m, a, g):
    """테크/모던: 코드 페이지 아이콘 크게"""
    icon = icon_code_page(m, a, "3.2", scale=1.25, ox=2, oy=5)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 135"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks Icon</title>
  {icon}
</svg>'''


def s3_m2(m, a, g):
    """따뜻한/친근: 펼친 책 아이콘 크게"""
    icon = icon_open_book(m, a, "3", scale=1.25, ox=2, oy=10)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 130"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks Icon</title>
  {icon}
</svg>'''


def s3_m3(m, a, g):
    """전문/신뢰: 브래킷 프레임 아이콘 크게"""
    icon = icon_bracket_frame(m, a, "3.5", scale=1.25, ox=5, oy=10)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 130"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks Icon</title>
  {icon}
</svg>'''


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S4: 워드마크 + 미니멀 장식
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def s4_m1(m, a, g):
    """테크/모던: 작은 코드페이지 + 워드마크 + 라인"""
    icon = icon_code_page(m, a, "1.8", scale=0.42, ox=5, oy=16)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 100"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks</title>
  {icon}
  <text x="55" y="42" font-family="'SF Mono','Fira Code','Pretendard',monospace"
        font-size="28" font-weight="900" letter-spacing="2.5" fill="{m}">OPENSKILLBOOKS</text>
  <line x1="55" y1="54" x2="490" y2="54" stroke="{a}" stroke-width="0.8" opacity="0.3"/>
  <text x="57" y="72" font-family="'Pretendard',sans-serif"
        font-size="12" font-weight="400" letter-spacing="5" fill="{a}" opacity="0.6">Hands-on Dev Cookbook</text>
</svg>'''


def s4_m2(m, a, g):
    """따뜻한/친근: 중앙 소문자 + 작은 책 아이콘 + 웨이브"""
    icon = icon_open_book(m, a, "1.8", scale=0.3, ox=222, oy=0)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 110"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks</title>
  <defs>
    <linearGradient id="wvG" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{a}" stop-opacity="0.15"/>
      <stop offset="50%" stop-color="{a}"/>
      <stop offset="100%" stop-color="{g}" stop-opacity="0.15"/>
    </linearGradient>
  </defs>
  {icon}
  <text x="260" y="65" text-anchor="middle"
        font-family="'Pretendard','Apple SD Gothic Neo',sans-serif"
        font-size="38" font-weight="700" letter-spacing="1" fill="{m}">openskillbooks</text>
  <path d="M 60 80 C 100 70, 140 90, 180 80 S 260 70, 300 80 S 380 90, 420 80 S 460 70, 470 80"
        fill="none" stroke="url(#wvG)" stroke-width="2" stroke-linecap="round"/>
  <text x="260" y="102" text-anchor="middle"
        font-family="'Pretendard',sans-serif"
        font-size="10" letter-spacing="6" fill="{a}" opacity="0.45">learn by doing</text>
</svg>'''


def s4_m3(m, a, g):
    """전문/신뢰: 대문자 + 다이아몬드 장식 + 작은 브래킷 아이콘"""
    icon = icon_bracket_frame(m, a, "1.5", scale=0.32, ox=2, oy=18)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 105"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks</title>
  {icon}
  <line x1="42" y1="40" x2="105" y2="40" stroke="{a}" stroke-width="0.7"/>
  <polygon points="112,40 117,34 122,40 117,46" fill="{a}"/>
  <line x1="398" y1="40" x2="500" y2="40" stroke="{a}" stroke-width="0.7"/>
  <polygon points="391,40 396,34 401,40 396,46" fill="{a}"/>
  <text x="260" y="50" text-anchor="middle"
        font-family="'Georgia','Palatino','Times New Roman',serif"
        font-size="28" font-weight="700" letter-spacing="7" fill="{m}">OPENSKILLBOOKS</text>
  <line x1="130" y1="62" x2="390" y2="62" stroke="{a}" stroke-width="0.5"/>
  <text x="260" y="85" text-anchor="middle"
        font-family="'Georgia','Palatino',serif"
        font-size="12" letter-spacing="8" fill="{a}" opacity="0.5">COOKBOOK SERIES</text>
</svg>'''


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 생성기
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESIGNS = {
    "S1-M1": s1_m1, "S1-M2": s1_m2, "S1-M3": s1_m3,
    "S2-M1": s2_m1, "S2-M2": s2_m2, "S2-M3": s2_m3,
    "S3-M1": s3_m1, "S3-M2": s3_m2, "S3-M3": s3_m3,
    "S4-M1": s4_m1, "S4-M2": s4_m2, "S4-M3": s4_m3,
}

STYLE_NAMES = {"S1": "심볼+텍스트", "S2": "타이포", "S3": "아이콘", "S4": "워드마크"}
MOOD_NAMES = {"M1": "테크/모던", "M2": "따뜻한/친근", "M3": "전문/신뢰"}


def main():
    count = 0
    for design_key, design_fn in DESIGNS.items():
        for color_key, (mc, ac, gc) in COLORS.items():
            filename = f"logo-{design_key}-{color_key}.svg"
            filepath = os.path.join(DIR, filename)
            svg = design_fn(mc, ac, gc)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(svg)
            count += 1
            s, mood = design_key.split("-")
            print(f"  {filename:30s} {STYLE_NAMES[s]:10s} {MOOD_NAMES[mood]:10s} {COLOR_NAMES[color_key]}")
    print(f"\n총 {count}개 SVG 생성 완료!")


if __name__ == "__main__":
    main()
