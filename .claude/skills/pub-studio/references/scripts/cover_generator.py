#!/usr/bin/env python3
"""표지 자동 생성 + 디자인 위자드

사용법:
    from cover_generator import generate_front_cover, wizard_step1_layout
    cover_path = generate_front_cover(config, output_dir)

    # 위자드 단계별
    paths = wizard_step1_layout(config, output_dir, ebook=True)
    paths = wizard_step2_shadow(config, output_dir, main_words, ebook=True)
    paths = wizard_step3_color(config, output_dir, main_words, shadow_map, ebook=True)
    path  = wizard_step4_confirm(config, output_dir, main_words, shadow_map, color_map, ebook=True)

main_words 튜플: (text, size_mm, bold, align, x_off, color, [same_row])
  - align: "L"/"R"/"C"
  - color: "dark"/"gray" 또는 RGB 튜플 (30,30,30)
  - same_row: True면 이전 행에 나란히 배치
"""
from __future__ import annotations

import base64
import os
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DPI = 300
MM = DPI / 25.4

# B5 기준 치수
FLAP = int(80 * MM)
BACK = int(182 * MM)
SPINE = int(9 * MM)
FRONT = int(182 * MM)
BLEED = int(3 * MM)
W = BLEED + FLAP + BACK + SPINE + FRONT + FLAP + BLEED
H = int(257 * MM) + 2 * BLEED

X_FRONT = BLEED + FLAP + BACK + SPINE

SERIES_MAIN_GAP_MM = 10
BOTTOM_SAFE_MM = 60

_FONT_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", "..", "docs", "images", "covers", "fonts"))


# ── 유틸 ──

def _mm(v): return int(v * MM)

def _font(size_mm, bold=False):
    px = _mm(size_mm)
    names = (["Pretendard-Bold.otf", "Pretendard-SemiBold.otf"] if bold
             else ["Pretendard-Regular.otf", "Pretendard-SemiBold.otf"])
    for name in names:
        p = os.path.join(_FONT_DIR, name)
        if os.path.exists(p):
            try: return ImageFont.truetype(p, px)
            except Exception: continue
    try: return ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", px, index=(5 if bold else 0))
    except Exception: return ImageFont.load_default()

def _tw(d, text, font):
    bb = d.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]

def _th(d, text, font):
    bb = d.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]

def _is_hangul(ch): return "\uac00" <= ch <= "\ud7a3"
def _hangul_ratio(text):
    chars = [c for c in text if not c.isspace()]
    return sum(1 for c in chars if _is_hangul(c)) / len(chars) if chars else 0.0
def _is_acronym(w): return len(w) >= 2 and w.isascii() and w.isupper()
def _is_proper_noun(w): return len(w) >= 2 and w.isascii() and w[0].isupper() and not w.isupper()

def _find_anchor(words):
    for i, w in enumerate(words):
        if _is_acronym(w): return i, w
    for i, w in enumerate(words):
        if _is_proper_noun(w): return i, w
    idx = min(range(len(words)), key=lambda i: len(words[i]))
    return idx, words[idx]

def _resolve_color(color_key):
    """색상키를 RGB 튜플로 변환."""
    if isinstance(color_key, tuple): return color_key
    return (30, 30, 30) if color_key == "dark" else (120, 120, 120)


# ── 그림자/색상 프리셋 ──

def _shadow_none(_words): return {}
def _shadow_soft(words): return {w[0]: ((230, 230, 230), 2) for w in words}
def _shadow_heavy(words): return {w[0]: ((210, 210, 210), 3.5) for w in words}
def _shadow_anchor_only(words):
    return {w[0]: ((220, 220, 220), 2.5) for w in words
            if _resolve_color(w[5]) == (30, 30, 30)}

SHADOW_PRESETS = {
    "none": ("클린 (그림자 없음)", _shadow_none),
    "soft": ("소프트 그림자", _shadow_soft),
    "heavy": ("헤비 그림자 (진하게)", _shadow_heavy),
    "anchor": ("앵커만 그림자", _shadow_anchor_only),
}

def _color_all_dark(words): return {w[0]: (30, 30, 30) for w in words}
def _color_anchor_dark(words):
    anchor_idx, _ = _find_anchor([w[0] for w in words])
    return {w[0]: (30, 30, 30) if i == anchor_idx else (120, 120, 120) for i, w in enumerate(words)}
def _color_aux_light(words):
    anchor_idx, _ = _find_anchor([w[0] for w in words])
    return {w[0]: (20, 20, 20) if i == anchor_idx else (160, 160, 160) for i, w in enumerate(words)}
def _color_gradient(words):
    n = len(words)
    anchor_idx, _ = _find_anchor([w[0] for w in words])
    result = {}
    for i, w in enumerate(words):
        if i == anchor_idx:
            result[w[0]] = (20, 20, 20)
        else:
            gray = 100 + int(60 * i / max(n - 1, 1))
            result[w[0]] = (gray, gray, gray)
    return result

COLOR_PRESETS = {
    "all_dark": ("전체 검정", _color_all_dark),
    "anchor_dark": ("앵커만 검정 + 보조 회색", _color_anchor_dark),
    "aux_light": ("보조 연회색 + 앵커 검정", _color_aux_light),
    "gradient": ("회색 농도 차등", _color_gradient),
}


# ── 자동 레이아웃 ──

def auto_layout_title(title, subtitle=""):  # noqa: ARG001
    words = title.split()
    if not words: return [[("제목 없음", 40, True, "L", -2, "dark")]]
    anchor_idx, anchor_word = _find_anchor(words)
    aux_words = [w for i, w in enumerate(words) if i != anchor_idx]
    aux_text = " ".join(aux_words)
    anchor_size = 55 if _hangul_ratio(anchor_word) < 0.5 else 50
    aux_size = max(15, int(anchor_size * 0.33))
    if _hangul_ratio(aux_text) > 0.5: aux_size = max(15, aux_size - 2)

    v1 = ([(aux_text, aux_size, True, "L", -2, "gray")] if aux_text else []) + \
         [(anchor_word, anchor_size, True, "L", -2, "dark")]
    v2 = [(anchor_word, anchor_size, True, "L", -2, "dark")] + \
         ([(aux_text, aux_size, True, "R", 0, "gray")] if aux_text else [])
    if len(words) <= 2:
        v3 = [(w, anchor_size if i == anchor_idx else int(anchor_size * 0.6),
               True, "L" if i == 0 else "R", -2 if i == 0 else 0,
               "dark" if i == anchor_idx else "gray") for i, w in enumerate(words)]
    else:
        before = " ".join(words[:anchor_idx])
        after = " ".join(words[anchor_idx + 1:])
        v3 = ([(before, aux_size, True, "L", -2, "gray")] if before else []) + \
             [(anchor_word, anchor_size, True, "L", -2, "dark")] + \
             ([(after, aux_size, True, "R", 0, "gray")] if after else [])
    return [v1, v2, v3]


# ── 렌더링 ──

def _build_cover_data(config):
    cd = config.get("cover_data", {})
    title = config.get("title", "")
    subtitle = config.get("subtitle", "")
    if "main_words" not in cd:
        vs = auto_layout_title(title, subtitle)
        mw = vs[0] if vs else [(title, 50, True, "L", -2, "dark")]
    else:
        mw = cd["main_words"]
    return {
        "series": cd.get("series", ""), "series_sub": cd.get("series_sub", ""),
        "authors": cd.get("authors", ""), "badges": cd.get("badges", []),
        "publisher": cd.get("publisher", "오픈스킬북스"),
        "accent_color": cd.get("accent_color", (45, 99, 235)),
        "top_descs": cd.get("top_descs", []), "main_words": mw,
        "tagline": subtitle, "title": title, "subtitle": subtitle,
    }


def _render_front_cover(d, data, shadow_map=None, color_map=None):
    """앞표지 렌더링. shadow_map/color_map으로 그림자/색상 제어."""
    c1 = data["accent_color"]
    fx = X_FRONT
    LM = fx + _mm(12)
    RM = fx + FRONT - _mm(12)

    # 상단 설명
    f_top = _font(5.5)
    top_y = _mm(12)
    for dl in data["top_descs"]:
        d.text((RM - _tw(d, dl, f_top), top_y), dl, fill=(140, 140, 140), font=f_top)
        top_y += _th(d, dl, f_top) + _mm(2)

    # 시리즈
    if data["series"]:
        f_big, f_mid, f_dev = _font(28, True), _font(16, True), _font(24, True)
        x_cur, y1 = LM, _mm(35)
        d.text((x_cur, y1), "특", fill=(30, 30, 30), font=f_big)
        x_cur += _tw(d, "특", f_big) + _mm(0.5)
        d.text((x_cur, y1 + _mm(12)), "이점이", fill=(80, 80, 80), font=f_mid)
        x_cur += _tw(d, "이점이", f_mid) + _mm(4)
        d.text((x_cur, y1), "온", fill=(30, 30, 30), font=f_big)
        d.text((LM, y1 + _mm(30)), "개발자", fill=(40, 40, 40), font=f_dev)
        series_bottom = y1 + _mm(30) + _mm(28)
    else:
        series_bottom = _mm(50)

    cur_y = series_bottom + _mm(SERIES_MAIN_GAP_MM)
    bottom_safe_y = H - _mm(BOTTOM_SAFE_MM)
    max_w = RM - LM - _mm(5)

    # 높이 계산 + 자동 축소
    total_h, prev_rh = 0, 0
    for entry in data["main_words"]:
        same_row = entry[6] if len(entry) > 6 else False
        rh = _mm(entry[1]) + _mm(entry[1] * 0.05)
        if same_row:
            total_h += max(prev_rh, rh) - prev_rh
            prev_rh = max(prev_rh, rh)
        else:
            total_h += rh
            prev_rh = rh
    avail = bottom_safe_y - cur_y
    scale = min(1.0, avail / total_h) if total_h > 0 else 1.0
    if scale < 1.0:
        print(f"   [자동축소] {total_h}px > {avail}px → {scale:.2f}배")

    prev_row_y = cur_y
    cur_y_before = cur_y

    for entry in data["main_words"]:
        text, size, bold_flag, align, x_off, color_key = entry[:6]
        same_row = entry[6] if len(entry) > 6 else False
        cur_size = int(size * scale) if scale < 1.0 else size

        if same_row:
            cur_y = prev_row_y

        font = _font(cur_size, bold=bold_flag)
        t_w = _tw(d, text, font)
        while t_w > max_w and cur_size > 10:
            cur_size -= 2
            font = _font(cur_size, bold=bold_flag)
            t_w = _tw(d, text, font)

        # 색상: color_map 우선 → 원본 color_key
        fill = color_map.get(text) if color_map and text in color_map else _resolve_color(color_key)

        if align == "L": x = LM + _mm(x_off)
        elif align == "R": x = RM - t_w + _mm(x_off)
        else: x = fx + (FRONT - t_w) // 2 + _mm(x_off)

        # 그림자: shadow_map 우선 → None이면 기본 소프트
        if shadow_map is not None:
            sh = shadow_map.get(text)
            if sh:
                d.text((x + _mm(sh[1]), cur_y + _mm(sh[1])), text, fill=sh[0], font=font)
        else:
            d.text((x + _mm(2.5), cur_y + _mm(2.5)), text, fill=(235, 235, 235), font=font)

        d.text((x, cur_y), text, fill=fill, font=font)

        line_gap = _mm(cur_size * 0.05)
        prev_row_y = cur_y
        rb = cur_y + _mm(cur_size) + line_gap
        if same_row: cur_y = max(cur_y_before, rb)
        else: cur_y_before = rb; cur_y = rb

    # 태그라인
    cur_y += _mm(3)
    f_tag = _font(7)
    d.text((LM, cur_y), data["tagline"], fill=(130, 130, 130), font=f_tag)

    # 배지
    if data["badges"]:
        cur_y += _th(d, data["tagline"], f_tag) + _mm(5)
        fb = _font(3.5); bh = _mm(5); bpx = _mm(2.5); bg = _mm(1.5); rg = _mm(2)
        mid = len(data["badges"]) // 2 + len(data["badges"]) % 2
        for row in [data["badges"][:mid], data["badges"][mid:]]:
            bx = LM
            for bt in row:
                bw = _tw(d, bt, fb) + bpx * 2
                d.rounded_rectangle([(bx, cur_y), (bx + bw, cur_y + bh)],
                    radius=_mm(3), fill=(240, 243, 248), outline=(220, 225, 235))
                bb = d.textbbox((0, 0), bt, font=fb)
                d.text((bx + bpx, cur_y + (bh - bb[3] + bb[1]) // 2 - bb[1]), bt, fill=(70, 85, 105), font=fb)
                bx += bw + bg
            cur_y += bh + rg

    # 하단 고정
    if data["series_sub"]:
        fs = _font(16, True); sw = _tw(d, data["series_sub"], fs); sy = H - _mm(40)
        d.rectangle([(RM - _mm(40), sy - _mm(3)), (RM, sy - _mm(2.2))], fill=c1)
        d.text((RM - sw, sy), data["series_sub"], fill=c1, font=fs)
    if data["authors"]:
        fa = _font(4); at = data["authors"] + " 지음"
        d.text((RM - _tw(d, at, fa), H - _mm(18)), at, fill=(130, 130, 130), font=fa)
    d.text((LM, H - _mm(25)), "OPENSKILL BOOKS", fill=(160, 160, 160), font=_font(7, True))
    d.text((LM, H - _mm(17)), data["publisher"], fill=(180, 180, 180), font=_font(6))


def _render_single(config, main_words, shadow_map=None, color_map=None):
    data = _build_cover_data(config)
    data["main_words"] = main_words
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    _render_front_cover(d, data, shadow_map=shadow_map, color_map=color_map)
    return img.crop((X_FRONT, BLEED, X_FRONT + FRONT, H - BLEED))


def _save_variation(front, output_dir, idx, ebook=False):
    output_dir = Path(output_dir)
    if ebook:
        front = front.resize((750, 1110), Image.LANCZOS)
        p = output_dir / f"cover_v{idx}.jpg"
        front.save(str(p), "JPEG", quality=90, dpi=(72, 72))
    else:
        p = output_dir / f"cover_v{idx}.png"
        front.save(str(p), dpi=(DPI, DPI))
    return p


# ── HTML UI ──

def _generate_html_preview(paths, descs, title, output_dir, ebook=False, step_label=""):
    cards = ""
    for i, (p, desc) in enumerate(zip(paths, descs), 1):
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        mime = "image/jpeg" if p.suffix == ".jpg" else "image/png"
        kb = p.stat().st_size / 1024
        cards += f'''
        <div class="card" onclick="select({i})" id="card-{i}">
          <div class="card-img"><img src="data:{mime};base64,{b64}" alt="v{i}"></div>
          <div class="card-info">
            <span class="card-label">v{i}</span>
            <span class="card-desc">{desc}</span>
            <span class="card-size">{kb:.0f}KB</span>
          </div>
        </div>'''

    spec = "750x1110 &middot; 72ppi &middot; JPG" if ebook else "B5 300DPI &middot; PNG"
    step_html = f'<span class="badge">{step_label}</span>' if step_label else ""

    html = f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>표지 선택 — {title}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,'Pretendard',sans-serif;background:#f5f5f7;color:#1d1d1f;padding:40px 20px}}
.header{{text-align:center;margin-bottom:36px}}
.header h1{{font-size:28px;font-weight:700;margin-bottom:8px}}
.header p{{font-size:14px;color:#86868b}}
.badge{{display:inline-block;background:#0071e3;color:#fff;padding:4px 12px;border-radius:12px;font-size:12px;margin-bottom:8px}}
.grid{{display:flex;gap:24px;justify-content:center;flex-wrap:wrap;max-width:1200px;margin:0 auto}}
.card{{background:#fff;border-radius:16px;overflow:hidden;cursor:pointer;transition:all .2s;border:3px solid transparent;box-shadow:0 2px 12px rgba(0,0,0,.08);width:260px}}
.card:hover{{transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,0,0,.12)}}
.card.selected{{border-color:#0071e3;box-shadow:0 0 0 2px #0071e3,0 8px 24px rgba(0,113,227,.2)}}
.card-img{{padding:16px;background:#fafafa;display:flex;justify-content:center}}
.card-img img{{height:360px;width:auto;object-fit:contain;border-radius:4px;box-shadow:0 1px 4px rgba(0,0,0,.1)}}
.card-info{{padding:14px 16px;display:flex;flex-direction:column;gap:4px}}
.card-label{{font-size:18px;font-weight:700}}.card-desc{{font-size:13px;color:#6e6e73}}.card-size{{font-size:11px;color:#aeaeb2}}
.result{{text-align:center;margin-top:32px;font-size:15px;color:#86868b;min-height:40px}}
.cmd{{display:inline-block;margin-top:8px;background:#1d1d1f;color:#f5f5f7;padding:8px 20px;border-radius:8px;font-family:'SF Mono',monospace;font-size:13px;user-select:all}}
</style></head><body>
<div class="header">{step_html}<h1>{title}</h1><p>{spec}</p></div>
<div class="grid">{cards}</div>
<div class="result" id="result">표지를 클릭하여 선택하세요</div>
<script>
function select(n){{document.querySelectorAll('.card').forEach(c=>c.classList.remove('selected'));
document.getElementById('card-'+n).classList.add('selected');
document.getElementById('result').innerHTML='<strong>v'+n+'</strong> 선택됨<br><span class="cmd">선택: v'+n+'</span>'}}
</script></body></html>'''

    hp = Path(output_dir) / "cover_preview.html"
    hp.write_text(html, encoding="utf-8")
    return hp


# ── 위자드 4단계 ──

def wizard_step1_layout(config, output_dir, ebook=False):
    """Step 2-1: 레이아웃 변형 4가지 생성 + HTML UI"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    title = config.get("title", "")
    subtitle = config.get("subtitle", "")

    variations = auto_layout_title(title, subtitle)
    cd = config.get("cover_data", {})
    if "main_words" in cd and cd["main_words"] not in variations:
        variations.insert(0, cd["main_words"])

    paths, descs = [], []
    labels = ["현재 설정", "보조 + 앵커", "앵커 + 보조", "의미 단위 분할"]
    for i, var in enumerate(variations[:4], 1):
        front = _render_single(config, var)
        p = _save_variation(front, output_dir, i, ebook)
        paths.append(p)
        descs.append(labels[i - 1] if i <= len(labels) else f"변형 {i}")
        print(f"   [v{i}] {descs[-1]}")

    _generate_html_preview(paths, descs, title, output_dir, ebook, step_label="Step 1/4: 레이아웃")
    return paths


def wizard_step2_shadow(config, output_dir, main_words, ebook=False):
    """Step 2-2: 그림자 변형 4가지 생성 + HTML UI"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    title = config.get("title", "")

    paths, descs = [], []
    for i, (key, (desc, fn)) in enumerate(SHADOW_PRESETS.items(), 1):
        sm = fn(main_words)
        front = _render_single(config, main_words, shadow_map=sm)
        p = _save_variation(front, output_dir, i, ebook)
        paths.append(p)
        descs.append(desc)
        print(f"   [v{i}] {desc}")

    _generate_html_preview(paths, descs, title, output_dir, ebook, step_label="Step 2/4: 그림자")
    return paths


def wizard_step3_color(config, output_dir, main_words, shadow_map=None, ebook=False):
    """Step 2-3: 폰트 색상 변형 4가지 생성 + HTML UI"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    title = config.get("title", "")

    paths, descs = [], []
    for i, (key, (desc, fn)) in enumerate(COLOR_PRESETS.items(), 1):
        cm = fn(main_words)
        front = _render_single(config, main_words, shadow_map=shadow_map, color_map=cm)
        p = _save_variation(front, output_dir, i, ebook)
        paths.append(p)
        descs.append(desc)
        print(f"   [v{i}] {desc}")

    _generate_html_preview(paths, descs, title, output_dir, ebook, step_label="Step 3/4: 폰트 색상")
    return paths


def wizard_step4_confirm(config, output_dir, main_words,
                         shadow_map=None, color_map=None, ebook=False):
    """Step 2-4: 최종 이미지 생성 + cover 파일 저장"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    front = _render_single(config, main_words, shadow_map=shadow_map, color_map=color_map)
    if ebook:
        front = front.resize((750, 1110), Image.LANCZOS)
        p = output_dir / "cover.jpg"
        front.save(str(p), "JPEG", quality=90, dpi=(72, 72))
    else:
        p = output_dir / "cover.png"
        front.save(str(p), dpi=(DPI, DPI))

    kb = p.stat().st_size / 1024
    print(f"   표지 확정: {p.name} ({kb:.0f}KB)")
    return p


# ── 하위호환 공개 API ──

def generate_front_cover(config, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = _build_cover_data(config)
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    _render_front_cover(d, data)
    front = img.crop((X_FRONT, BLEED, X_FRONT + FRONT, H - BLEED))
    p = output_dir / "cover.png"
    front.save(str(p), dpi=(DPI, DPI))
    print(f"   표지 생성: {p.name} ({front.size[0]}x{front.size[1]})")
    return p

def generate_cover_previews(config, output_dir, ebook=False):
    return wizard_step1_layout(config, output_dir, ebook=ebook)

def select_cover_variation(output_dir, variation_num):
    output_dir = Path(output_dir)
    for ext in ("jpg", "png"):
        src = output_dir / f"cover_v{variation_num}.{ext}"
        if src.exists():
            dst = output_dir / f"cover.{ext}"
            shutil.copy2(src, dst)
            print(f"   표지 선택: v{variation_num} → cover.{ext}")
            return dst
    print(f"   [오류] cover_v{variation_num} 없음")
    return None

def generate_spread(config, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    p = output_dir / "spread.png"
    data = _build_cover_data(config)
    img = Image.new("RGB", (W, H), (255, 255, 255))
    _render_front_cover(ImageDraw.Draw(img), data)
    img.save(str(p), dpi=(DPI, DPI))
    return p
