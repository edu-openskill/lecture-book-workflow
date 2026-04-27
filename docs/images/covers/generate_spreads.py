#!/usr/bin/env python3
"""4권 표지 스프레드 v3 — 화이트 배경 + 와이어프레임 기하학 장식
폰트: Pretendard / 배경: 화이트 + 하단 컬러 바"""
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

# ── Pretendard 폰트 ──
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
    # 폴백
    for p in ["/System/Library/Fonts/AppleSDGothicNeo.ttc"]:
        try: return ImageFont.truetype(p, px, index=(5 if bold else 0))
        except: continue
    return ImageFont.load_default()

# 앞표지
f_series   = F(10, bold=True)
f_title    = F(48, bold=True)
f_sub      = F(14, bold=True)
f_tag      = F(7)
f_author   = F(10, bold=True)
f_pub      = F(8)
f_series_s = F(6)
f_feat     = F(6.5, bold=True)

# 뒷표지
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
         feats=["컨테이너의 개념부터 실전까지", "이야기로 시작하는 기술 입문서", "Docker Compose 실습 수록"],
         desc=["컨테이너가 왜 필요한지 모르겠다면,","이 책이 출발점입니다.","",
               "가상 머신과 컨테이너의 차이부터","Docker Compose로 서비스를 엮는 법까지.",
               "이야기로 시작해서 실습으로 마무리합니다."]),
    dict(id="msa", title="MSA", sub="개념편",
         c1=(75,60,180), c2=(30,25,70),
         feats=["모놀리스에서 마이크로서비스로", "서비스 분리와 통신의 원리", "API Gateway 실습 수록"],
         desc=["모놀리스에서 마이크로서비스로,","왜 쪼개야 하는지부터 시작합니다.","",
               "서비스 분리, API Gateway, 이벤트 기반 통신.",
               "작은 서비스가 큰 시스템을 이루는 원리를","이야기와 코드로 풀어냅니다."]),
    dict(id="rag", title="RAG", sub="개념편",
         c1=(120,50,160), c2=(45,20,70),
         feats=["검색 증강 생성의 핵심 원리", "임베딩과 벡터 검색 실습", "프롬프트 엔지니어링 수록"],
         desc=["LLM이 모르는 걸 어떻게 답하게 할까?","검색 증강 생성의 핵심을 짚습니다.","",
               "임베딩, 벡터 검색, 프롬프트 엔지니어링.",
               "AI가 우리 데이터를 이해하게 만드는 법을","처음부터 차근차근 안내합니다."]),
    dict(id="tech-collection", title="기술모음", sub="개념편",
         c1=(180,120,30), c2=(80,50,20),
         feats=["개발자 필수 기술 총정리", "Git, CI/CD, 테스트, 모니터링", "현장 실무 사례 수록"],
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
#  와이어프레임 장식 함수
# ══════════════════════════════════════════════════

def draw_waves(d, x0, y0, width, n_lines, spacing, amplitude, color, lw):
    for i in range(n_lines):
        pts = []
        base_y = y0 + i * spacing
        for px in range(0, width, 3):
            wave = amplitude * math.sin(2.5 * math.pi * px / width + i * 0.4)
            pts.append((x0 + px, int(base_y + wave)))
        if len(pts) > 1:
            d.line(pts, fill=color, width=lw)

def draw_sphere(d, cx, cy, r, color, lw):
    n = 8
    for i in range(n):
        angle = math.pi * i / n
        rx = max(3, int(r * abs(math.sin(angle))))
        d.ellipse([(cx-rx, cy-r), (cx+rx, cy+r)], outline=color, width=lw)
    for i in range(1, n):
        frac = i / n
        y_off = int(r * (2*frac - 1))
        lat_r = int(r * math.cos(math.asin(abs(2*frac - 1))))
        if lat_r > 3:
            ry = max(3, lat_r // 3)
            d.ellipse([(cx-lat_r, cy+y_off-ry), (cx+lat_r, cy+y_off+ry)],
                      outline=color, width=lw)

def draw_blob(d, cx, cy, r, bumps, color, lw):
    pts = []
    for i in range(200):
        a = 2 * math.pi * i / 200
        rr = r * (1 + 0.25 * math.sin(bumps * a) + 0.12 * math.cos(bumps*2*a + 1))
        pts.append((int(cx + rr * math.cos(a)), int(cy + rr * math.sin(a))))
    pts.append(pts[0])
    d.line(pts, fill=color, width=lw)

def draw_cube(d, x, y, w, h, depth, color, lw):
    dx, dy = depth, -depth
    d.line([(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)], fill=color, width=lw)
    d.line([(x+dx,y+dy),(x+w+dx,y+dy),(x+w+dx,y+h+dy),(x+dx,y+h+dy),(x+dx,y+dy)],
           fill=color, width=lw)
    for px, py in [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]:
        d.line([(px,py),(px+dx,py+dy)], fill=color, width=lw)

def draw_grid(d, x, y, w, h, rows, cols, color, lw):
    for r in range(rows+1):
        ry = y + r * h // rows
        d.line([(x, ry), (x+w, ry)], fill=color, width=lw)
    for c in range(cols+1):
        cx_ = x + c * w // cols
        d.line([(cx_, y), (cx_, y+h)], fill=color, width=lw)


def th(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[3] - bb[1]

def tw(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[2] - bb[0]


# ══════════════════════════════════════════════════
#  스프레드 생성
# ══════════════════════════════════════════════════

def create_spread(b):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    c1, c2 = b["c1"], b["c2"]

    # ════════════════════════════════════════════
    #  앞표지 — 화이트 배경 + 와이어프레임 장식
    # ════════════════════════════════════════════
    fx = X_FRONT
    LM = mm(10)

    # 배경: 전체 화이트
    d.rectangle([(fx, 0), (fx+FRONT, H)], fill=(255,255,255))

    # 와이어프레임 색상 (화이트 배경 위 연한 테마색)
    wire_c = tuple(c1[i] + int((255 - c1[i]) * 0.70) for i in range(3))
    wire_b = tuple(c1[i] + int((255 - c1[i]) * 0.55) for i in range(3))
    wire_lw = max(2, mm(0.4))

    # 장식: 좌상단 물결선
    draw_waves(d, fx - mm(5), mm(5), mm(70), 7, mm(4), mm(10), wire_c, wire_lw)

    # 장식: 우상단 물결선
    draw_waves(d, fx + FRONT - mm(55), mm(2), mm(60), 5, mm(5), mm(12), wire_c, wire_lw)

    # 장식: 좌측 블롭
    draw_blob(d, fx + mm(20), int(H*0.45), mm(18), 5, wire_c, wire_lw)
    draw_blob(d, fx + mm(25), int(H*0.37), mm(12), 4, wire_c, wire_lw)

    # 장식: 우측 큐브
    draw_cube(d, fx+FRONT-mm(42), int(H*0.08), mm(20), mm(18), mm(8), wire_c, wire_lw)

    # 장식: 중앙 와이어프레임 구
    sphere_cx = fx + FRONT // 2
    sphere_cy = int(H * 0.53)
    draw_sphere(d, sphere_cx, sphere_cy, mm(28), wire_b, wire_lw)

    # 시리즈명
    stxt = "특이점이 온 개발자"
    sw = tw(d, stxt, f_series)
    d.text((fx + (FRONT-sw)//2, int(H*0.18)), stxt, fill=(100,100,100), font=f_series)

    # 제목 (HUGE, 다크)
    title_w = tw(d, b["title"], f_title)
    title_y = int(H * 0.25)
    d.text((fx + (FRONT-title_w)//2, title_y), b["title"], fill=(30,30,30), font=f_title)

    # 부제 (테마 컬러)
    sub_w = tw(d, b["sub"], f_sub)
    sub_y = title_y + th(d, b["title"], f_title) + mm(5)
    bar_len = mm(12)
    bar_y = sub_y + th(d, b["sub"], f_sub) // 2
    sub_x = fx + (FRONT - (bar_len + mm(3) + sub_w)) // 2
    d.line([(sub_x, bar_y), (sub_x + bar_len, bar_y)], fill=c1, width=mm(0.8))
    d.text((sub_x + bar_len + mm(3), sub_y), b["sub"], fill=c1, font=f_sub)

    # 피처 텍스트 (중앙, 회색)
    feat_y = int(H * 0.72)
    for feat in b.get("feats", []):
        fw_ = tw(d, feat, f_feat)
        d.text((fx + (FRONT-fw_)//2, feat_y), feat, fill=(100,100,100), font=f_feat)
        feat_y += th(d, feat, f_feat) + mm(4)

    # 하단 컬러 바
    bar_top = H - mm(32)
    d.rectangle([(fx, bar_top), (fx+FRONT, H)], fill=c2)

    # 저자 + 출판사 (컬러 바 위)
    atxt = "저자  류재성"
    aw_ = tw(d, atxt, f_author)
    d.text((fx + (FRONT-aw_)//2, bar_top + mm(6)), atxt, fill="white", font=f_author)
    ptxt = "OPENSKILL BOOKS"
    pw_ = tw(d, ptxt, f_pub)
    d.text((fx + (FRONT-pw_)//2, bar_top + mm(6) + th(d, atxt, f_author) + mm(3)),
           ptxt, fill=(200,200,200), font=f_pub)

    # 시리즈 안내 (바 우하단)
    stxt2 = "특이점이 온 개발자 시리즈"
    sw2 = tw(d, stxt2, f_series_s)
    d.text((fx + FRONT - sw2 - mm(4), H - BLEED - mm(4)),
           stxt2, fill=(180,180,180), font=f_series_s)

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
        dx = -1 if cx > W//2 else 1
        dy_ = -1 if cy > H//2 else 1
        d.line([(cx,cy),(cx,cy+dy_*ml)], fill=gc, width=1)
        d.line([(cx,cy),(cx+dx*ml,cy)], fill=gc, width=1)
    d.line([(X_SPINE,0),(X_SPINE,H)], fill=gc, width=1)
    d.line([(X_SPINE+SPINE,0),(X_SPINE+SPINE,H)], fill=gc, width=1)
    for fold_x in [X_BACK, X_FFLAP]:
        for y in range(0, H, mm(5)):
            d.line([(fold_x, y), (fold_x, min(y+mm(2.5), H))], fill=gc, width=1)

    return img


OUT = os.path.join(BASE)
for b in BOOKS:
    img = create_spread(b)
    p = os.path.join(OUT, f"spread-{b['id']}.png")
    img.save(p, dpi=(DPI,DPI))
    print(f"OK {p} ({img.size[0]}x{img.size[1]})")

print(f"\n전체: {W}x{H}px = {W/MM:.0f}x{H/MM:.0f}mm")
