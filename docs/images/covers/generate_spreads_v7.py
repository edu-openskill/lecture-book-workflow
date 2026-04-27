#!/usr/bin/env python3
"""v7 — 세로 사이드 밴드
- 앞표지 좌측에 세로 컬러 밴드 (25mm)
- 밴드가 시리즈 아이덴티티 역할
- 나머지는 화이트 + v4.5 타이포그래피
- 밴드 안에 시리즈명 세로 배치"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw

from cover_base import (
    mm, F, tw, th, FRONT, BLEED, H, W,
    X_FRONT, X_FFLAP, BOOKS, save_spreads,
)


def render_front_v7(img, d, b):
    """v7 앞표지 — 세로 사이드 밴드"""
    fx = X_FRONT
    c1 = b["c1"]
    band_w = mm(25)
    LM = fx + band_w + mm(10)  # 밴드 오른쪽에서 시작
    RM = fx + FRONT - mm(12)

    # --- 세로 컬러 밴드 ---
    d.rectangle([(fx, 0), (fx + band_w, H)], fill=c1)

    # --- 밴드 안: 시리즈명 세로 ---
    f_band = F(5, bold=True)
    band_text = "특이점이 온 개발자"
    tmp = Image.new("RGBA", (H, band_w), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    btw = tw(td, band_text, f_band)
    td.text(((H - btw) // 2, (band_w - th(td, band_text, f_band)) // 2),
            band_text, fill=(255, 255, 255), font=f_band)
    rotated = tmp.rotate(90, expand=True)
    img.paste(rotated, (fx, 0), rotated)

    # --- 상단 설명 텍스트 (우측 정렬) ---
    f_top = F(5.5)
    top_y = mm(12)
    for desc_line in b["top_descs"]:
        dw = tw(d, desc_line, f_top)
        d.text((RM - dw, top_y), desc_line, fill=(140, 140, 140), font=f_top)
        top_y += th(d, desc_line, f_top) + mm(2)

    # --- "특이점이 온 개발자" 스택형 타이포 ---
    f_big = F(28, bold=True)
    f_mid = F(16, bold=True)
    f_dev = F(24, bold=True)

    x_cur = LM
    y_line1 = mm(35)
    d.text((x_cur, y_line1), "특", fill=(30, 30, 30), font=f_big)
    x_cur += tw(d, "특", f_big) + mm(0.5)
    baseline_offset = mm(28) - mm(16)
    d.text((x_cur, y_line1 + baseline_offset), "이점이",
           fill=(80, 80, 80), font=f_mid)
    x_cur += tw(d, "이점이", f_mid) + mm(4)
    d.text((x_cur, y_line1), "온", fill=(30, 30, 30), font=f_big)

    y_line2 = y_line1 + mm(30)
    d.text((LM, y_line2), "개발자", fill=(40, 40, 40), font=f_dev)

    # --- 메인 타이틀 ---
    series_bottom = y_line2 + mm(28)
    main_lines = [(t, s, b_, a, x, c)
                  for t, s, b_, a, x, c in b.get("lines", [])
                  if t not in ("특이점이", "온 개발자") and t != "_GAP"]

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

        if color_key == "dark":
            fill = (30, 30, 30)
        elif color_key == "gray":
            fill = (120, 120, 120)
        else:
            fill = (30, 30, 30)

        if align == "L":
            x = LM + mm(x_off)
        elif align == "R":
            x = RM - t_w + mm(x_off)
        else:
            x = fx + band_w + (FRONT - band_w - t_w) // 2 + mm(x_off)

        # 그림자
        d.text((x + mm(2.5), cur_y + mm(2.5)), text,
               fill=(235, 235, 235), font=font)
        d.text((x, cur_y), text, fill=fill, font=font)

        cur_y += mm(cur_size) + mm(2)

    # --- 태그라인 ---
    cur_y += mm(3)
    f_tag = F(7)
    d.text((LM, cur_y), b["tagline"], fill=(130, 130, 130), font=f_tag)

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
           fill=(100, 100, 100), font=f_author)

    # --- 출판사 (좌측 하단) ---
    f_pub = F(7, bold=True)
    f_pub2 = F(6)
    d.text((LM, H - mm(25)), "OPENSKILL BOOKS",
           fill=(160, 160, 160), font=f_pub)
    d.text((LM, H - mm(17)), "오픈스킬북스",
           fill=(180, 180, 180), font=f_pub2)


if __name__ == "__main__":
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
    save_spreads("v7", render_front_v7)
