#!/usr/bin/env python3
"""S5: S4-M1 기반, 서브텍스트를 더 크고 강하게

S4-M1과 동일 레이아웃, 서브텍스트 크기/굵기만 변경
"""
import os

DIR = os.path.dirname(os.path.abspath(__file__))

COLORS = {
    "C1": ("#1A1A1A", "#008080"),
    "C2": ("#1A237E", "#4FC3F7"),
    "C3": ("#006666", "#B4781E"),
    "C4": ("#2D2D2D", "#888888"),
}


def icon_code_page(stroke, accent, sw="1.8", scale=0.42, ox=5, oy=16):
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


def make_s5(m, a):
    icon = icon_code_page(m, a)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 100"
     role="img" aria-labelledby="t1">
  <title id="t1">OpenSkillBooks</title>
  {icon}
  <text x="55" y="42" font-family="'SF Mono','Fira Code','Pretendard',monospace"
        font-size="28" font-weight="900" letter-spacing="2.5" fill="{m}">OPENSKILLBOOKS</text>
  <line x1="55" y1="54" x2="490" y2="54" stroke="{a}" stroke-width="0.8" opacity="0.3"/>
  <text x="57" y="76" font-family="'Pretendard','SF Pro Display',sans-serif"
        font-size="20" font-weight="700" letter-spacing="3" fill="{a}">Hands-on Dev Cookbook</text>
</svg>'''


def main():
    for ck, (mc, ac) in COLORS.items():
        fname = f"logo-S5-M1-{ck}.svg"
        with open(os.path.join(DIR, fname), "w", encoding="utf-8") as f:
            f.write(make_s5(mc, ac))
        print(f"  {fname}")
    print("\n4개 S5 로고 생성 완료!")


if __name__ == "__main__":
    main()
