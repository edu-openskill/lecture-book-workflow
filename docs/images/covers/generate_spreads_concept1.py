#!/usr/bin/env python3
"""컨셉 1 — '기초 입문자형' 핵심 요약형
하이라이트 키워드 박스 + 친근한 아이콘 그래픽 + 포인트 컬러 불릿"""
from PIL import Image, ImageDraw, ImageFont
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
FONT_DIR = os.path.join(BASE, "fonts")

def mm(v):
    return int(v * MM)

def F(size_mm, bold=False):
    px = mm(size_mm)
    if bold:
        names = ["Pretendard-Bold.otf", "Pretendard-SemiBold.otf"]
    else:
        names = ["Pretendard-Regular.otf", "Pretendard-SemiBold.otf"]
    for name in names:
        p = os.path.join(FONT_DIR, name)
        if os.path.exists(p):
            try: return ImageFont.truetype(p, px)
            except: continue
    for p in ["/System/Library/Fonts/AppleSDGothicNeo.ttc"]:
        try: return ImageFont.truetype(p, px, index=(5 if bold else 0))
        except: continue
    return ImageFont.load_default()

def th(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[3] - bb[1]

def tw(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[2] - bb[0]

# ── 폰트 ──
f_series   = F(10, bold=True)
f_title    = F(42, bold=True)
f_sub      = F(14, bold=True)
f_author   = F(10, bold=True)
f_pub      = F(8)
f_series_s = F(6)
f_highlight = F(9, bold=True)
f_bullet   = F(7)
f_keyword  = F(11, bold=True)

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

# ── 데이터 ──
BOOKS = [
    dict(id="docker", title="Docker", sub="개념편",
         c1=(0,128,128), c2=(25,60,80),
         keywords=["컨테이너", "이미지", "Compose"],
         bullets=["가상 머신과 컨테이너, 뭐가 다를까?",
                  "Dockerfile 하나로 환경을 통일하는 법",
                  "Compose로 서비스를 한 번에 띄우기"],
         icon_type="container",
         desc=["컨테이너가 왜 필요한지 모르겠다면,","이 책이 출발점입니다.","",
               "가상 머신과 컨테이너의 차이부터","Docker Compose로 서비스를 엮는 법까지.",
               "이야기로 시작해서 실습으로 마무리합니다."]),
    dict(id="msa", title="MSA", sub="개념편",
         c1=(75,60,180), c2=(30,25,70),
         keywords=["서비스 분리", "API Gateway", "이벤트"],
         bullets=["모놀리스는 왜 한계에 부딪히는가?",
                  "서비스를 쪼개는 기준과 원칙",
                  "이벤트 기반 통신의 핵심 패턴"],
         icon_type="network",
         desc=["모놀리스에서 마이크로서비스로,","왜 쪼개야 하는지부터 시작합니다.","",
               "서비스 분리, API Gateway, 이벤트 기반 통신.",
               "작은 서비스가 큰 시스템을 이루는 원리를","이야기와 코드로 풀어냅니다."]),
    dict(id="rag", title="RAG", sub="개념편",
         c1=(120,50,160), c2=(45,20,70),
         keywords=["임베딩", "벡터 검색", "프롬프트"],
         bullets=["LLM이 모르는 것에 답하게 만드는 원리",
                  "텍스트를 벡터로 바꾸는 임베딩의 비밀",
                  "프롬프트 하나로 결과가 달라지는 이유"],
         icon_type="brain",
         desc=["LLM이 모르는 걸 어떻게 답하게 할까?","검색 증강 생성의 핵심을 짚습니다.","",
               "임베딩, 벡터 검색, 프롬프트 엔지니어링.",
               "AI가 우리 데이터를 이해하게 만드는 법을","처음부터 차근차근 안내합니다."]),
    dict(id="tech-collection", title="기술모음", sub="개념편",
         c1=(180,120,30), c2=(80,50,20),
         keywords=["Git", "CI/CD", "테스트"],
         bullets=["개발자 필수 기술을 한 권에 정리",
                  "코드 관리부터 배포 자동화까지",
                  "현장에서 바로 쓸 수 있는 실무 지식"],
         icon_type="tools",
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


# ══════════════════════════════════════════════════
#  아이콘 그리기 함수
# ══════════════════════════════════════════════════

def draw_icon_container(d, cx, cy, size, color):
    """컨테이너 아이콘 (상자 + 파도)"""
    s = size
    # 상자
    lw = max(2, mm(0.5))
    d.rounded_rectangle([(cx-s, cy-s), (cx+s, cy+s)],
                         radius=mm(3), outline=color, width=lw)
    # 내부 수평선
    for i in range(3):
        y = cy - s//2 + (i+1) * s // 2
        d.line([(cx-s+mm(3), y), (cx+s-mm(3), y)], fill=color, width=lw)

def draw_icon_network(d, cx, cy, size, color):
    """네트워크 아이콘 (노드 + 연결선)"""
    lw = max(2, mm(0.4))
    r = mm(3)
    positions = [(cx, cy-size), (cx-size, cy), (cx+size, cy),
                 (cx-size//2, cy+size), (cx+size//2, cy+size)]
    for i, (x1, y1) in enumerate(positions):
        for x2, y2 in positions[i+1:]:
            d.line([(x1,y1),(x2,y2)], fill=color, width=lw)
    for x, y in positions:
        d.ellipse([(x-r, y-r), (x+r, y+r)], fill="white", outline=color, width=lw)

def draw_icon_brain(d, cx, cy, size, color):
    """뇌 아이콘 (원 + 연결)"""
    lw = max(2, mm(0.4))
    r = size // 3
    offsets = [(-r, -r), (r, -r), (0, 0), (-r, r), (r, r)]
    for ox, oy in offsets:
        d.ellipse([(cx+ox-r, cy+oy-r), (cx+ox+r, cy+oy+r)],
                  outline=color, width=lw)

def draw_icon_tools(d, cx, cy, size, color):
    """도구 아이콘 (기어)"""
    lw = max(2, mm(0.5))
    teeth = 8
    r_out = size
    r_in = int(size * 0.65)
    pts = []
    for i in range(teeth * 2):
        a = math.pi * i / teeth
        r = r_out if i % 2 == 0 else r_in
        pts.append((int(cx + r * math.cos(a)), int(cy + r * math.sin(a))))
    pts.append(pts[0])
    d.line(pts, fill=color, width=lw)
    d.ellipse([(cx-r_in//2, cy-r_in//2), (cx+r_in//2, cy+r_in//2)],
              outline=color, width=lw)

ICON_FN = {
    "container": draw_icon_container,
    "network": draw_icon_network,
    "brain": draw_icon_brain,
    "tools": draw_icon_tools,
}


def draw_highlight_box(d, x, y, text, font, bg_color, text_color):
    """하이라이트 키워드 박스"""
    tw_ = tw(d, text, font)
    th_ = th(d, text, font)
    pad_x, pad_y = mm(3), mm(1.5)
    d.rounded_rectangle(
        [(x - pad_x, y - pad_y), (x + tw_ + pad_x, y + th_ + pad_y)],
        radius=mm(2), fill=bg_color
    )
    d.text((x, y), text, fill=text_color, font=font)
    return tw_ + pad_x * 2


# ══════════════════════════════════════════════════
#  스프레드 생성
# ══════════════════════════════════════════════════

def create_spread(b):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    c1, c2 = b["c1"], b["c2"]

    # 연한 테마색
    c1_light = tuple(c1[i] + int((255 - c1[i]) * 0.85) for i in range(3))
    c1_mid = tuple(c1[i] + int((255 - c1[i]) * 0.4) for i in range(3))

    fx = X_FRONT

    # ════════════════════════════════════════════
    #  앞표지 — 기초 입문자형
    # ════════════════════════════════════════════
    d.rectangle([(fx, 0), (fx+FRONT, H)], fill=(255,255,255))

    # 상단 얇은 컬러 스트라이프
    d.rectangle([(fx, 0), (fx+FRONT, mm(5))], fill=c1)

    # 시리즈명
    stxt = "특이점이 온 개발자"
    sw = tw(d, stxt, f_series)
    d.text((fx + (FRONT-sw)//2, mm(14)), stxt, fill=(120,120,120), font=f_series)

    # 제목
    title_y = int(H * 0.14)
    title_w = tw(d, b["title"], f_title)
    d.text((fx + (FRONT-title_w)//2, title_y), b["title"], fill=(30,30,30), font=f_title)

    # 부제 (컬러 바 + 텍스트)
    sub_y = title_y + th(d, b["title"], f_title) + mm(6)
    sub_w = tw(d, b["sub"], f_sub)
    bar_w = mm(10)
    sub_total = bar_w + mm(3) + sub_w
    sub_x = fx + (FRONT - sub_total) // 2
    bar_y = sub_y + th(d, b["sub"], f_sub) // 2
    d.line([(sub_x, bar_y), (sub_x + bar_w, bar_y)], fill=c1, width=mm(0.8))
    d.text((sub_x + bar_w + mm(3), sub_y), b["sub"], fill=c1, font=f_sub)

    # 아이콘 (중앙)
    icon_cy = int(H * 0.42)
    icon_fn = ICON_FN.get(b["icon_type"], draw_icon_container)
    icon_fn(d, fx + FRONT//2, icon_cy, mm(22), c1_mid)

    # 하이라이트 키워드 박스 (아이콘 아래)
    kw_y = int(H * 0.56)
    total_kw_w = 0
    for kw in b["keywords"]:
        total_kw_w += tw(d, kw, f_keyword) + mm(6) + mm(4)
    total_kw_w -= mm(4)
    kw_x = fx + (FRONT - total_kw_w) // 2
    for kw in b["keywords"]:
        w_ = draw_highlight_box(d, kw_x, kw_y, kw, f_keyword, c1_light, c2)
        kw_x += w_ + mm(4)

    # 불릿 포인트 (하단)
    bullet_y = int(H * 0.66)
    bullet_x = fx + mm(20)
    dot_r = mm(1.5)
    for bullet in b["bullets"]:
        d.ellipse([(bullet_x, bullet_y + mm(1)),
                   (bullet_x + dot_r*2, bullet_y + mm(1) + dot_r*2)],
                  fill=c1)
        d.text((bullet_x + dot_r*2 + mm(3), bullet_y), bullet,
               fill=(60,60,60), font=f_bullet)
        bullet_y += th(d, bullet, f_bullet) + mm(5)

    # 하단 컬러 바
    bar_top = H - mm(32)
    d.rectangle([(fx, bar_top), (fx+FRONT, H)], fill=c2)
    atxt = "저자  류재성"
    aw_ = tw(d, atxt, f_author)
    d.text((fx + (FRONT-aw_)//2, bar_top + mm(6)), atxt, fill="white", font=f_author)
    ptxt = "OPENSKILL BOOKS"
    pw_ = tw(d, ptxt, f_pub)
    d.text((fx + (FRONT-pw_)//2, bar_top + mm(6) + th(d, atxt, f_author) + mm(3)),
           ptxt, fill=(200,200,200), font=f_pub)
    stxt2 = "특이점이 온 개발자 시리즈"
    sw2 = tw(d, stxt2, f_series_s)
    d.text((fx + FRONT - sw2 - mm(4), H - BLEED - mm(4)),
           stxt2, fill=(180,180,180), font=f_series_s)

    # ════════════════════════════════════════════
    #  뒷표지 (화이트 배경)
    # ════════════════════════════════════════════
    bx = X_BACK
    BLM = bx + mm(8)
    d.rectangle([(bx, 0), (bx+BACK, H)], fill=(255,255,255))
    d.rectangle([(bx, 0), (bx+BACK, int(H*0.10))], fill=c1)
    d.text((BLM, BLEED+mm(2.5)), "특이점이 온 개발자 시리즈", fill="white", font=f_bk_label)
    dy = int(H * 0.15)
    for line in b["desc"]:
        if line == "":
            dy += mm(6); continue
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
            fy += mm(3); continue
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
    #  책등 (화이트 배경)
    # ════════════════════════════════════════════
    d.rectangle([(X_SPINE, 0), (X_SPINE+SPINE, H)], fill=(255,255,255))
    st = f"특이점이 온 개발자 — {b['title']} {b['sub']}"
    tmp = Image.new("RGBA", (H, SPINE), (0,0,0,0))
    td = ImageDraw.Draw(tmp)
    stw_ = tw(td, st, f_spine)
    td.text(((H-stw_)//2, (SPINE-th(td,st,f_spine))//2), st, fill=(40,40,40), font=f_spine)
    aw = tw(td, "류재성", f_spine_sm)
    td.text((H-aw-mm(2), (SPINE-th(td,"류재성",f_spine_sm))//2),
            "류재성", fill=(100,100,100), font=f_spine_sm)
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


OUT = BASE
for b in BOOKS:
    img = create_spread(b)
    p = os.path.join(OUT, f"spread-concept1-{b['id']}.png")
    img.save(p, dpi=(DPI,DPI))
    print(f"OK {p} ({img.size[0]}x{img.size[1]})")

print(f"\n컨셉 1 '기초 입문자형' — {len(BOOKS)}권 완료")
