#!/usr/bin/env python3
"""v4 표지 스프레드 — 컨셉 A '코드의 진화' (The Evolution of Code)
미니멀 그래픽 + 네온 코드 조각 + 기하학 패턴 + 빛나는 코드 <{...}>
색상: 1권 블루, 2권 그린, 3권 레드, 4권 골드"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os

DPI = 300
MM = DPI / 25.4

FLAP = int(80 * MM)
BACK = int(182 * MM)
SPINE = int(9 * MM)
FRONT = int(182 * MM)
BLEED = int(3 * MM)
W = BLEED + FLAP + BACK + SPINE + FRONT + FLAP + BLEED
H = int(257 * MM) + 2 * BLEED

X_BFLAP = BLEED
X_BACK  = BLEED + FLAP
X_SPINE = BLEED + FLAP + BACK
X_FRONT = BLEED + FLAP + BACK + SPINE
X_FFLAP = BLEED + FLAP + BACK + SPINE + FRONT

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "v4-assets")

def mm(v):
    return int(v * MM)

def F(size_mm, bold=False):
    px = mm(size_mm)
    paths = ["/System/Library/Fonts/AppleSDGothicNeo.ttc",
             "/Library/Fonts/AppleSDGothicNeo.ttc"]
    for p in paths:
        try: return ImageFont.truetype(p, px, index=(5 if bold else 0))
        except:
            try: return ImageFont.truetype(p, px)
            except: continue
    return ImageFont.load_default()

def FM(size_mm):
    """모노스페이스 폰트 (코드용)"""
    px = mm(size_mm)
    paths = ["/System/Library/Fonts/Menlo.ttc",
             "/System/Library/Fonts/SFMono-Regular.otf",
             "/Library/Fonts/SF-Mono-Regular.otf"]
    for p in paths:
        try: return ImageFont.truetype(p, px)
        except: continue
    return F(size_mm)

# 폰트
f_series   = F(9, bold=True)
f_title    = F(50, bold=True)
f_sub      = F(14, bold=True)
f_tag      = F(6.5)
f_author   = F(9, bold=True)
f_pub      = F(7)
f_series_s = F(5)
f_code     = FM(4)            # 떠다니는 코드 텍스트
f_code_lg  = FM(8)            # 큰 코드 심볼

f_bk_label = F(8, bold=True)
f_bk_desc  = F(7)
f_bk_pub   = F(10, bold=True)
f_bk_eng   = F(7)
f_bk_url   = F(6)
f_price    = F(7, bold=True)
f_isbn     = F(5)
f_isbn_sm  = F(4)
f_bk_bot   = F(7)

f_spine    = F(1.8, bold=True)
f_spine_sm = F(1.3)
f_fl_title = F(6.5, bold=True)
f_fl_body  = F(5)
f_fl_sm    = F(4)

# ── 데이터 (색상: 블루/그린/레드/골드) ──
BOOKS = [
    dict(id="docker", title="Docker", sub="개념편",
         c1=(40,120,220), c2=(12,30,65), glow=(80,160,255),
         img_file="book1-blue.jpg",
         code_snippets=["docker build -t app .", "FROM node:18-alpine",
                        "EXPOSE 3000", "docker compose up -d"],
         desc=["컨테이너가 왜 필요한지 모르겠다면,","이 책이 출발점입니다.","",
               "가상 머신과 컨테이너의 차이부터","Docker Compose로 서비스를 엮는 법까지.",
               "이야기로 시작해서 실습으로 마무리합니다."]),
    dict(id="msa", title="MSA", sub="개념편",
         c1=(40,190,90), c2=(12,55,28), glow=(80,230,130),
         img_file="book2-green.jpg",
         code_snippets=["@RestController", "gateway.routes()",
                        "event.publish()", "service.register()"],
         desc=["모놀리스에서 마이크로서비스로,","왜 쪼개야 하는지부터 시작합니다.","",
               "서비스 분리, API Gateway, 이벤트 기반 통신.",
               "작은 서비스가 큰 시스템을 이루는 원리를","이야기와 코드로 풀어냅니다."]),
    dict(id="rag", title="RAG", sub="개념편",
         c1=(210,50,50), c2=(65,15,15), glow=(255,90,90),
         img_file="book3-red.jpg",
         code_snippets=["embedding = model.encode()", "vector_store.search()",
                        "prompt_template.format()", "llm.generate(context)"],
         desc=["LLM이 모르는 걸 어떻게 답하게 할까?","검색 증강 생성의 핵심을 짚습니다.","",
               "임베딩, 벡터 검색, 프롬프트 엔지니어링.",
               "AI가 우리 데이터를 이해하게 만드는 법을","처음부터 차근차근 안내합니다."]),
    dict(id="tech-collection", title="기술모음", sub="개념편",
         c1=(220,170,40), c2=(70,55,12), glow=(255,210,80),
         img_file="book4-gold.jpg",
         code_snippets=["git commit -m 'feat'", "pipeline.trigger()",
                        "assert result == True", "monitor.alert()"],
         desc=["개발자라면 알아야 할 기술들을","한 권에 모았습니다.","",
               "Git, CI/CD, 테스트, 모니터링까지.",
               "현장에서 바로 쓸 수 있는 기술들을","이야기와 실습으로 정리합니다."]),
]
SERIES_OTHER = {
    "docker": ["MSA 개념편","RAG 개념편","기술모음 개념편"],
    "msa": ["Docker 개념편","RAG 개념편","기술모음 개념편"],
    "rag": ["Docker 개념편","MSA 개념편","기술모음 개념편"],
    "tech-collection": ["Docker 개념편","MSA 개념편","RAG 개념편"],
}
AUTHOR_BIO = ["류재성","","메타코딩 유튜브 채널 운영자이자",
              "오픈스킬북스의 저자.","",
              "복잡한 기술을 이야기로 풀어내는","것을 좋아하며, AI 시대의 개발자가",
              "갖춰야 할 기술을 탐구합니다."]

def th(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[3] - bb[1]

def tw(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[2] - bb[0]


def load_cover_image(filename, target_w, target_h):
    """에셋 이미지 로드 + 크롭/리사이즈"""
    path = os.path.join(ASSETS, filename)
    if not os.path.exists(path):
        return None
    try:
        img = Image.open(path).convert("RGB")
        # 비율 유지하며 target 크기에 맞게 크롭
        iw, ih = img.size
        ratio_w = target_w / iw
        ratio_h = target_h / ih
        ratio = max(ratio_w, ratio_h)
        new_w = int(iw * ratio)
        new_h = int(ih * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        # 중앙 크롭
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        img = img.crop((left, top, left + target_w, top + target_h))
        return img
    except Exception as e:
        print(f"  이미지 로드 실패: {e}")
        return None


def make_gradient(w, h, c_top, c_bot):
    """세로 그라디언트 이미지"""
    img = Image.new("RGB", (w, h))
    for y in range(h):
        f = y / max(h-1, 1)
        r = int(c_top[0] + (c_bot[0] - c_top[0]) * f)
        g = int(c_top[1] + (c_bot[1] - c_top[1]) * f)
        b = int(c_top[2] + (c_bot[2] - c_top[2]) * f)
        ImageDraw.Draw(img).line([(0, y), (w, y)], fill=(r, g, b))
    return img


def draw_floating_code(d, fx, front_w, h, snippets, color, font):
    """떠다니는 코드 텍스트 장식 (앞표지 배경)"""
    positions = [
        (0.05, 0.15), (0.65, 0.10), (0.10, 0.55),
        (0.60, 0.60), (0.30, 0.72), (0.75, 0.35),
        (0.15, 0.38), (0.55, 0.45),
    ]
    # 코드 스니펫 + 고정 심볼
    texts = snippets + ["<{...}>", "{ }", "=>", "//", "( )", "[ ]"]
    for i, (rx, ry) in enumerate(positions):
        if i >= len(texts):
            break
        txt = texts[i]
        alpha = 0.15 + 0.1 * math.sin(i * 1.7)
        c = tuple(int(v * alpha) + int(255 * (1-alpha) * 0.05) for v in color)
        x = fx + int(front_w * rx)
        y = int(h * ry)
        d.text((x, y), txt, fill=c, font=font)


def draw_neon_symbol(img, cx, cy, text, font, color, blur_r=8):
    """네온 글로우 텍스트 (코드 심볼)"""
    d = ImageDraw.Draw(img)
    bb = d.textbbox((0,0), text, font=font)
    tw_ = bb[2] - bb[0]
    th_ = bb[3] - bb[1]

    # 글로우 레이어
    glow = Image.new("RGB", img.size, (0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.text((cx - tw_//2, cy - th_//2), text, fill=color, font=font)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=blur_r))

    # 합성 (Screen blend 근사)
    from PIL import ImageChops
    img_out = ImageChops.add(img, glow)

    # 선명한 텍스트 위에 다시
    d2 = ImageDraw.Draw(img_out)
    bright = tuple(min(255, v + 80) for v in color)
    d2.text((cx - tw_//2, cy - th_//2), text, fill=bright, font=font)
    return img_out


def create_spread(b):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    c1, c2, glow_c = b["c1"], b["c2"], b["glow"]

    # ════════════════════════════════════════════
    #  앞표지 — 코드의 진화
    # ════════════════════════════════════════════
    fx = X_FRONT

    # 배경: 에셋 이미지 or 그라디언트
    cover_img = load_cover_image(b["img_file"], FRONT, H)
    if cover_img:
        # 이미지 + 색상 오버레이 (블렌드)
        overlay = Image.new("RGB", (FRONT, H), c2)
        cover_img = Image.blend(cover_img, overlay, 0.55)
        # 밝기 조정
        cover_img = ImageEnhance.Brightness(cover_img).enhance(0.6)
        img.paste(cover_img, (fx, 0))
    else:
        # 그라디언트 폴백
        grad = make_gradient(FRONT, H, c2, (5, 5, 15))
        img.paste(grad, (fx, 0))

    d = ImageDraw.Draw(img)  # 재생성 (paste 후)

    # 떠다니는 코드 텍스트 (배경 장식)
    draw_floating_code(d, fx, FRONT, H, b["code_snippets"], glow_c, f_code)

    # 중앙 네온 코드 심볼 <{...}>
    img = draw_neon_symbol(img, fx + FRONT//2, int(H*0.50),
                           "<{...}>", f_code_lg, glow_c, blur_r=mm(3))
    d = ImageDraw.Draw(img)

    # 상단 가로선 (네온)
    line_y = int(H * 0.12)
    for offset in range(mm(1)):
        alpha = max(0, 255 - offset * 80)
        lc = tuple(min(255, v) for v in glow_c)
        d.line([(fx + mm(8), line_y + offset), (fx + FRONT - mm(8), line_y + offset)],
               fill=lc, width=1)

    # 시리즈명
    stxt = "특이점이 온 개발자"
    sw = tw(d, stxt, f_series)
    d.text((fx + (FRONT-sw)//2, int(H*0.16)), stxt, fill=(200,200,200), font=f_series)

    # 제목 (HUGE 중앙)
    title_w = tw(d, b["title"], f_title)
    title_y = int(H * 0.24)
    # 제목 그림자
    d.text((fx + (FRONT-title_w)//2 + mm(1), title_y + mm(1)),
           b["title"], fill=(0,0,0), font=f_title)
    d.text((fx + (FRONT-title_w)//2, title_y), b["title"], fill="white", font=f_title)

    # 부제
    sub_w = tw(d, b["sub"], f_sub)
    sub_y = title_y + th(d, b["title"], f_title) + mm(5)
    d.text((fx + (FRONT-sub_w)//2, sub_y), b["sub"], fill=glow_c, font=f_sub)

    # 하단 영역
    bot_y = int(H * 0.85)
    # 반투명 다크 바 (근사)
    for y in range(bot_y, H):
        alpha = min(200, int((y - bot_y) / (H - bot_y) * 200))
        d.line([(fx, y), (fx+FRONT, y)],
               fill=(c2[0]//2, c2[1]//2, c2[2]//2), width=1)

    # 저자
    atxt = "저자  류재성"
    aw_ = tw(d, atxt, f_author)
    d.text((fx + (FRONT-aw_)//2, int(H*0.88)), atxt, fill="white", font=f_author)

    # 출판사
    ptxt = "OPENSKILL BOOKS"
    pw_ = tw(d, ptxt, f_pub)
    d.text((fx + (FRONT-pw_)//2, int(H*0.93)), ptxt, fill=(180,180,180), font=f_pub)

    # 시리즈 (하단)
    stxt2 = "특이점이 온 개발자 시리즈"
    sw2 = tw(d, stxt2, f_series_s)
    d.text((fx + FRONT - sw2 - mm(4), H - BLEED - mm(4)),
           stxt2, fill=(120,120,120), font=f_series_s)

    # 하단 네온 라인
    d.line([(fx + mm(8), bot_y), (fx + FRONT - mm(8), bot_y)],
           fill=glow_c, width=2)

    # ════════════════════════════════════════════
    #  뒷표지
    # ════════════════════════════════════════════
    bx = X_BACK
    BLM = bx + mm(8)

    d.rectangle([(bx, 0), (bx+BACK, int(H*0.10))], fill=c1)
    d.text((BLM, BLEED+mm(2.5)), "특이점이 온 개발자 시리즈", fill="white", font=f_bk_label)

    dy = int(H * 0.15)
    for line in b["desc"]:
        if line == "":
            dy += mm(6)
            continue
        d.text((BLM, dy), line, fill=(50,50,50), font=f_bk_desc)
        dy += th(d, line, f_bk_desc) + mm(3.5)

    dy += mm(5)
    d.line([(BLM, dy), (bx+BACK-mm(8), dy)], fill=(200,200,200), width=3)
    dy += mm(5)

    d.text((BLM, dy), "오픈스킬북스", fill=(60,60,60), font=f_bk_pub)
    dy += th(d, "오픈스킬북스", f_bk_pub) + mm(3)
    d.text((BLM, dy), "OPENSKILL BOOKS", fill=(120,120,120), font=f_bk_eng)
    dy += th(d, "OPENSKILL BOOKS", f_bk_eng) + mm(2)
    d.text((BLM, dy), "books.openskill.kr", fill=(120,120,120), font=f_bk_url)

    bc_w, bc_h = mm(55), mm(30)
    bc_x = bx + BACK - mm(8) - bc_w
    bc_y = H - BLEED - mm(22) - bc_h
    d.rectangle([(bc_x, bc_y), (bc_x+bc_w, bc_y+bc_h)], outline=(180,180,180), width=3)
    it = "ISBN 000-00-0000-000-0"
    d.text((bc_x+(bc_w-tw(d,it,f_isbn))//2, bc_y+mm(4)), it, fill=(150,150,150), font=f_isbn)
    pt = "(ISBN 발급 후 교체)"
    d.text((bc_x+(bc_w-tw(d,pt,f_isbn_sm))//2, bc_y+bc_h-mm(6)), pt, fill=(180,180,180), font=f_isbn_sm)
    d.text((bc_x, bc_y-mm(10)), "정가 15,000원", fill=(60,60,60), font=f_price)

    d.rectangle([(bx, H-mm(10)), (bx+BACK, H)], fill=c1)
    d.text((BLM, H-mm(8)), "books.openskill.kr", fill="white", font=f_bk_bot)

    # ════════════════════════════════════════════
    #  앞날개
    # ════════════════════════════════════════════
    ffx = X_FFLAP
    FLM = ffx + mm(4)
    d.rectangle([(ffx, 0), (ffx+FLAP+BLEED, H)], fill=(248,248,248))
    d.rectangle([(ffx, 0), (ffx+FLAP+BLEED, mm(10))], fill=c1)
    fy = mm(14)
    d.text((FLM, fy), "저자 소개", fill=c2, font=f_fl_title)
    fy += th(d, "저자 소개", f_fl_title) + mm(3)
    d.line([(FLM, fy), (ffx+FLAP-mm(4), fy)], fill=c1, width=3)
    fy += mm(4)
    for line in AUTHOR_BIO:
        if line == "":
            fy += mm(3)
            continue
        d.text((FLM, fy), line, fill=(60,60,60), font=f_fl_body)
        fy += th(d, line, f_fl_body) + mm(2.5)
    d.text((FLM, H-BLEED-mm(6)), "openskill.kr", fill=(150,150,150), font=f_fl_sm)

    # ════════════════════════════════════════════
    #  뒷날개
    # ════════════════════════════════════════════
    bfx = X_BFLAP
    BFLM = bfx + mm(4)
    d.rectangle([(0, 0), (bfx+FLAP, H)], fill=(248,248,248))
    d.rectangle([(0, 0), (bfx+FLAP, mm(10))], fill=c1)
    by = mm(14)
    d.text((BFLM, by), "시리즈 안내", fill=c2, font=f_fl_title)
    by += th(d, "시리즈 안내", f_fl_title) + mm(3)
    d.line([(BFLM, by), (bfx+FLAP-mm(4), by)], fill=c1, width=3)
    by += mm(4)
    d.text((BFLM, by), "특이점이 온 개발자", fill=(40,40,40), font=f_fl_title)
    by += th(d, "특이점이 온 개발자", f_fl_title) + mm(3)
    for t in ["AI 시대, 개발자의 새로운 출발점.", "같은 시리즈의 다른 책들도", "만나보세요."]:
        d.text((BFLM, by), t, fill=(100,100,100), font=f_fl_sm)
        by += th(d, t, f_fl_sm) + mm(2)
    by += mm(4)
    for other in SERIES_OTHER[b["id"]]:
        d.text((BFLM, by), f"  {other}", fill=(60,60,60), font=f_fl_body)
        by += th(d, other, f_fl_body) + mm(3)
    d.text((BFLM, H-BLEED-mm(6)), "books.openskill.kr", fill=(150,150,150), font=f_fl_sm)

    # ════════════════════════════════════════════
    #  책등
    # ════════════════════════════════════════════
    d.rectangle([(X_SPINE, 0), (X_SPINE+SPINE, H)], fill=c2)
    st = f"특이점이 온 개발자 — {b['title']} {b['sub']}"
    tmp = Image.new("RGBA", (H, SPINE), (0,0,0,0))
    td = ImageDraw.Draw(tmp)
    stw_ = tw(td, st, f_spine)
    td.text(((H-stw_)//2, (SPINE-th(td,st,f_spine))//2), st, fill="white", font=f_spine)
    aw = tw(td, "류재성", f_spine_sm)
    td.text((H-aw-mm(2), (SPINE-th(td,"류재성",f_spine_sm))//2),
            "류재성", fill=(200,200,200), font=f_spine_sm)
    img.paste(tmp.rotate(90, expand=True), (X_SPINE, 0), tmp.rotate(90, expand=True))

    # ════════════════════════════════════════════
    #  재단 가이드
    # ════════════════════════════════════════════
    gc = (200,200,200)
    ml = mm(5)
    for cx, cy in [(BLEED,BLEED),(W-BLEED,BLEED),(BLEED,H-BLEED),(W-BLEED,H-BLEED)]:
        dx_ = -1 if cx > W//2 else 1
        dy_ = -1 if cy > H//2 else 1
        d.line([(cx,cy),(cx,cy+dy_*ml)], fill=gc, width=1)
        d.line([(cx,cy),(cx+dx_*ml,cy)], fill=gc, width=1)
    d.line([(X_SPINE,0),(X_SPINE,H)], fill=gc, width=1)
    d.line([(X_SPINE+SPINE,0),(X_SPINE+SPINE,H)], fill=gc, width=1)
    for fold_x in [X_BACK, X_FFLAP]:
        for y in range(0, H, mm(5)):
            d.line([(fold_x, y), (fold_x, min(y+mm(2.5), H))], fill=gc, width=1)

    return img


OUT = os.path.join(BASE)
for b in BOOKS:
    img = create_spread(b)
    p = os.path.join(OUT, f"spread-v4-{b['id']}.png")
    img.save(p, dpi=(DPI,DPI))
    print(f"OK {p} ({img.size[0]}x{img.size[1]})")

print(f"\n컨셉 A '코드의 진화' — {len(BOOKS)}권 완료")
