#!/usr/bin/env python3
"""v5 — 다크 모드
- 짙은 배경 (거의 블랙) + 화이트 타이포
- v4.5 스택형 타이포그래피 유지
- 그림자 대신 액센트 컬러 글로우
- 고급스러운 다크 테마"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cover_base import (
    mm, F, tw, th, FRONT, BLEED, H, W,
    X_FRONT, X_FFLAP, BOOKS, save_spreads,
)


def render_front_v5(img, d, b):
    """v5 앞표지 — 다크 모드"""
    fx = X_FRONT
    c1 = b["c1"]
    LM = fx + mm(12)
    RM = fx + FRONT - mm(12)

    # --- 다크 배경 ---
    bg = (25, 25, 30)
    d.rectangle([(fx, 0), (fx + FRONT, H)], fill=bg)

    # --- 상단 설명 텍스트 (우측 정렬) ---
    f_top = F(5.5)
    top_y = mm(12)
    for desc_line in b["top_descs"]:
        dw = tw(d, desc_line, f_top)
        d.text((RM - dw, top_y), desc_line, fill=(100, 100, 110), font=f_top)
        top_y += th(d, desc_line, f_top) + mm(2)

    # --- "특이점이 온 개발자" 스택형 타이포 ---
    f_big = F(28, bold=True)
    f_mid = F(16, bold=True)
    f_dev = F(24, bold=True)

    x_cur = LM
    y_line1 = mm(35)
    d.text((x_cur, y_line1), "특", fill=(240, 240, 245), font=f_big)
    x_cur += tw(d, "특", f_big) + mm(0.5)
    baseline_offset = mm(28) - mm(16)
    d.text((x_cur, y_line1 + baseline_offset), "이점이",
           fill=(160, 160, 170), font=f_mid)
    x_cur += tw(d, "이점이", f_mid) + mm(4)
    d.text((x_cur, y_line1), "온", fill=(240, 240, 245), font=f_big)

    y_line2 = y_line1 + mm(30)
    d.text((LM, y_line2), "개발자", fill=(200, 200, 210), font=f_dev)

    # --- 메인 타이틀 (글로우 + 화이트) ---
    series_bottom = y_line2 + mm(28)
    main_lines = [(t, s, b_, a, x, c)
                  for t, s, b_, a, x, c in b.get("lines", [])
                  if t not in ("특이점이", "온 개발자") and t != "_GAP"]

    # lines가 없으면 title로 대체
    if not main_lines:
        main_lines = [(b["title"], 55, True, "L", -2, "dark")]

    max_w = RM - LM - mm(5)
    cur_y = series_bottom

    for text, size, bold_flag, align, x_off, color_key in main_lines:
        cur_size = size
        font = F(cur_size, bold=bold_flag)
        t_w = tw(d, text, font)
        while t_w > max_w and cur_size > 10:
            cur_size -= 2
            font = F(cur_size, bold=bold_flag)
            t_w = tw(d, text, font)

        if align == "L":
            x = LM + mm(x_off)
        elif align == "R":
            x = RM - t_w + mm(x_off)
        else:
            x = fx + (FRONT - t_w) // 2 + mm(x_off)

        # 글로우 (액센트 컬러)
        glow_color = tuple(min(255, c + 40) for c in c1)
        for dx, dy in [(mm(2), mm(2)), (mm(-1), mm(1)), (mm(1), mm(-1))]:
            d.text((x + dx, cur_y + dy), text,
                   fill=(*glow_color, ), font=font)

        # 본체 (화이트)
        d.text((x, cur_y), text, fill=(255, 255, 255), font=font)

        cur_y += mm(cur_size) + mm(2)

    # --- 태그라인 ---
    cur_y += mm(3)
    f_tag = F(7)
    d.text((LM, cur_y), b["tagline"], fill=(120, 120, 130), font=f_tag)

    # --- 개념편 (우측 하단) ---
    f_sub = F(16, bold=True)
    sub_w = tw(d, b["sub"], f_sub)
    sub_y = H - mm(55)
    line_w = mm(40)
    d.rectangle([(RM - line_w, sub_y - mm(3)),
                 (RM, sub_y - mm(3) + mm(0.8))], fill=c1)
    d.text((RM - sub_w, sub_y), b["sub"], fill=c1, font=f_sub)

    # --- 저자 ---
    f_author = F(7)
    aw = tw(d, "류재성 지음", f_author)
    d.text((RM - aw, H - mm(35)), "류재성 지음",
           fill=(140, 140, 150), font=f_author)

    # --- 출판사 (좌측 하단) ---
    f_pub = F(7, bold=True)
    f_pub2 = F(6)
    d.text((LM, H - mm(25)), "OPENSKILL BOOKS",
           fill=(80, 80, 90), font=f_pub)
    d.text((LM, H - mm(17)), "오픈스킬북스",
           fill=(70, 70, 80), font=f_pub2)


if __name__ == "__main__":
    # v4.5 호환: lines 데이터 추가
    for b in BOOKS:
        if "lines" not in b:
            title = b["title"]
            if title == "Spring":
                b["lines"] = [
                    ("특이점이", 20, True, "L", 0, "dark"),
                    ("온 개발자", 25, True, "R", 0, "gray"),
                    ("_GAP", 12, False, "L", 0, "dark"),
                    ("Spring", 50, True, "L", -2, "dark"),
                ]
            elif len(title) <= 4:
                b["lines"] = [
                    ("특이점이", 20, True, "L", 0, "dark"),
                    ("온 개발자", 25, True, "R", 0, "gray"),
                    ("_GAP", 12, False, "L", 0, "dark"),
                    (title, 55 if len(title) <= 3 else 48, True, "L", -2, "dark"),
                ]
            else:
                b["lines"] = [
                    ("특이점이", 20, True, "L", 0, "dark"),
                    ("온 개발자", 25, True, "R", 0, "gray"),
                    ("_GAP", 12, False, "L", 0, "dark"),
                    (title, 40, True, "L", -2, "dark"),
                ]
    save_spreads("v5", render_front_v5)
