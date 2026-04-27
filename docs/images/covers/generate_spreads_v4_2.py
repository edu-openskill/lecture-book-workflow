#!/usr/bin/env python3
"""v4.2 — 타이포그래피 스프레드형
1. 전면 화이트 (불필요한 색상 제거)
2. 제목이 뒷표지→책등→앞표지 전체를 관통
3. '특이점이 온 개발자' 점프투자바 스타일 대형 볼드"""
from PIL import Image, ImageDraw, ImageFont
import os

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

# 뒷표지~앞표지 전체 영역
SPAN_X = X_BACK
SPAN_W = BACK + SPINE + FRONT
SPAN_CX = SPAN_X + SPAN_W // 2

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
f_series   = F(22, bold=True)      # 점프투자바 스타일 대형
f_series_s = F(6)
f_sub      = F(16, bold=True)
f_author   = F(9, bold=True)
f_pub      = F(7)
f_tagline  = F(8)

f_bk_desc  = F(7)
f_bk_pub   = F(9, bold=True)
f_bk_eng   = F(6.5)
f_bk_url   = F(5.5)
f_price    = F(7, bold=True)
f_isbn     = F(5)
f_isbn_sm  = F(4)

f_spine    = F(1.8, bold=True)
f_spine_sm = F(1.3)
f_fl_title = F(6.5, bold=True)
f_fl_body  = F(5)
f_fl_sm    = F(4)


# ── 데이터 ──
BOOKS = [
    dict(id="docker", title="Docker", sub="개념편",
         c1=(0,128,128),
         # 뒷표지~앞표지 관통 글자 크기 (mm)
         span_size=155,
         tagline="컨테이너의 모든 것",
         desc=["컨테이너가 왜 필요한지 모르겠다면,","이 책이 출발점입니다.","",
               "가상 머신과 컨테이너의 차이부터","Docker Compose로 서비스를 엮는 법까지.",
               "이야기로 시작해서 실습으로 마무리합니다."]),
    dict(id="msa", title="MSA", sub="개념편",
         c1=(75,60,180),
         span_size=200,
         tagline="마이크로서비스 아키텍처",
         desc=["모놀리스에서 마이크로서비스로,","왜 쪼개야 하는지부터 시작합니다.","",
               "서비스 분리, API Gateway, 이벤트 기반 통신.",
               "작은 서비스가 큰 시스템을 이루는 원리를","이야기와 코드로 풀어냅니다."]),
    dict(id="rag", title="RAG", sub="개념편",
         c1=(120,50,160),
         span_size=200,
         tagline="검색 증강 생성",
         desc=["LLM이 모르는 걸 어떻게 답하게 할까?","검색 증강 생성의 핵심을 짚습니다.","",
               "임베딩, 벡터 검색, 프롬프트 엔지니어링.",
               "AI가 우리 데이터를 이해하게 만드는 법을","처음부터 차근차근 안내합니다."]),
    dict(id="tech-collection", title="기술모음", sub="개념편",
         c1=(180,120,30),
         span_size=105,
         tagline="개발자 필수 기술 총정리",
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


def create_spread(b):
    img = Image.new("RGB", (W, H), (255,255,255))
    d = ImageDraw.Draw(img)
    c1 = b["c1"]

    # ════════════════════════════════════════════════════
    #  1단계: 전체 화이트 기반
    # ════════════════════════════════════════════════════

    # ════════════════════════════════════════════════════
    #  2단계: 뒷표지→책등→앞표지 관통 초대형 제목
    # ════════════════════════════════════════════════════
    f_span = F(b["span_size"], bold=True)

    title_text = b["title"]
    span_tw = tw(d, title_text, f_span)
    span_th = th(d, title_text, f_span)

    # 관통 제목 위치: 뒷표지~앞표지 중앙, 세로 중앙보다 약간 위
    span_tx = SPAN_CX - span_tw // 2
    span_ty = int(H * 0.30) - span_th // 2

    # 고스트 (더 큰, 더 연한)
    f_ghost = F(b["span_size"] + 15, bold=True)
    ghost_tw = tw(d, title_text, f_ghost)
    ghost_x = SPAN_CX - ghost_tw // 2
    ghost_y = span_ty - mm(8)
    ghost_c = (235, 235, 235)
    d.text((ghost_x, ghost_y), title_text, fill=ghost_c, font=f_ghost)

    # 메인 제목 (검정)
    d.text((span_tx, span_ty), title_text, fill=(25, 25, 25), font=f_span)

    # ════════════════════════════════════════════════════
    #  3단계: 앞표지 텍스트 요소
    # ════════════════════════════════════════════════════
    fx = X_FRONT

    # "특이점이 온 개발자" — 점프투자바 스타일 (대형 볼드, 상단)
    stxt = "특이점이 온 개발자"
    sw = tw(d, stxt, f_series)
    d.text((fx + (FRONT - sw) // 2, mm(15)), stxt,
           fill=(30, 30, 30), font=f_series)

    # 부제 "개념편" + 컬러 언더라인
    sub_y = span_ty + span_th + mm(5)
    sub_w = tw(d, b["sub"], f_sub)
    sub_x = fx + (FRONT - sub_w) // 2
    # 언더라인 (포인트 컬러)
    line_w = mm(30)
    line_x = fx + (FRONT - line_w) // 2
    d.rectangle([(line_x, sub_y - mm(1)),
                 (line_x + line_w, sub_y + mm(1))], fill=c1)
    d.text((sub_x, sub_y + mm(3)), b["sub"], fill=c1, font=f_sub)

    # 태그라인
    tag_y = sub_y + th(d, b["sub"], f_sub) + mm(10)
    tag_w = tw(d, b["tagline"], f_tagline)
    d.text((fx + (FRONT - tag_w) // 2, tag_y), b["tagline"],
           fill=(120, 120, 120), font=f_tagline)

    # 출판사 (하단, 화이트 배경)
    bot_y = H - mm(30)
    ptxt = "OPENSKILL BOOKS"
    pw_ = tw(d, ptxt, f_pub)
    d.text((fx + (FRONT - pw_) // 2, bot_y),
           ptxt, fill=(150, 150, 150), font=f_pub)

    # 시리즈 표시 (우하단)
    stxt2 = "특이점이 온 개발자 시리즈"
    sw2 = tw(d, stxt2, f_series_s)
    d.text((fx + FRONT - sw2 - mm(4), H - BLEED - mm(5)),
           stxt2, fill=(180, 180, 180), font=f_series_s)

    # ════════════════════════════════════════════════════
    #  4단계: 뒷표지 텍스트 요소 (화이트 배경)
    # ════════════════════════════════════════════════════
    bx = X_BACK
    BLM = bx + mm(10)

    # 상단 시리즈 라벨 (컬러 없이, 텍스트만)
    d.text((BLM, mm(12)), "특이점이 온 개발자 시리즈",
           fill=(150, 150, 150), font=F(7, bold=True))

    # 얇은 구분선
    d.line([(BLM, mm(22)), (bx + BACK - mm(10), mm(22))],
           fill=(220, 220, 220), width=1)

    # 설명 텍스트 (관통 제목 아래)
    desc_y = max(int(H * 0.55), span_ty + span_th + mm(15))
    for line in b["desc"]:
        if line == "":
            desc_y += mm(5)
            continue
        d.text((BLM, desc_y), line, fill=(60, 60, 60), font=f_bk_desc)
        desc_y += th(d, line, f_bk_desc) + mm(3)

    desc_y += mm(6)
    d.line([(BLM, desc_y), (bx + BACK - mm(10), desc_y)],
           fill=(220, 220, 220), width=1)
    desc_y += mm(5)

    # 출판사 정보
    d.text((BLM, desc_y), "오픈스킬북스", fill=(60, 60, 60), font=f_bk_pub)
    desc_y += th(d, "오픈스킬북스", f_bk_pub) + mm(2)
    d.text((BLM, desc_y), "OPENSKILL BOOKS", fill=(140, 140, 140), font=f_bk_eng)
    desc_y += th(d, "OPENSKILL BOOKS", f_bk_eng) + mm(1.5)
    d.text((BLM, desc_y), "books.openskill.kr", fill=(140, 140, 140), font=f_bk_url)

    # ISBN + 가격 (우하단)
    bc_w, bc_h = mm(50), mm(28)
    bc_x = bx + BACK - mm(10) - bc_w
    bc_y = H - BLEED - mm(18) - bc_h
    d.rectangle([(bc_x, bc_y), (bc_x + bc_w, bc_y + bc_h)],
                outline=(200, 200, 200), width=2)
    it = "ISBN 000-00-0000-000-0"
    d.text((bc_x + (bc_w - tw(d, it, f_isbn)) // 2, bc_y + mm(4)),
           it, fill=(160, 160, 160), font=f_isbn)
    pt = "(ISBN 발급 후 교체)"
    d.text((bc_x + (bc_w - tw(d, pt, f_isbn_sm)) // 2, bc_y + bc_h - mm(5)),
           pt, fill=(180, 180, 180), font=f_isbn_sm)
    d.text((bc_x, bc_y - mm(8)), "정가 15,000원",
           fill=(60, 60, 60), font=f_price)

    # 하단 URL
    url_t = "books.openskill.kr"
    d.text((BLM, H - BLEED - mm(5)), url_t,
           fill=(180, 180, 180), font=f_bk_url)

    # ════════════════════════════════════════════════════
    #  5단계: 앞날개 (화이트)
    # ════════════════════════════════════════════════════
    ffx = X_FFLAP
    FLM = ffx + mm(5)
    d.rectangle([(ffx, 0), (ffx + FLAP + BLEED, H)], fill=(252, 252, 252))

    fy = mm(14)
    d.text((FLM, fy), "저자 소개", fill=(60, 60, 60), font=f_fl_title)
    fy += th(d, "저자 소개", f_fl_title) + mm(3)
    d.line([(FLM, fy), (ffx + FLAP - mm(5), fy)], fill=(200, 200, 200), width=2)
    fy += mm(4)
    for line in AUTHOR_BIO:
        if line == "":
            fy += mm(3)
            continue
        d.text((FLM, fy), line, fill=(70, 70, 70), font=f_fl_body)
        fy += th(d, line, f_fl_body) + mm(2.5)
    d.text((FLM, H - BLEED - mm(6)), "openskill.kr",
           fill=(160, 160, 160), font=f_fl_sm)

    # ════════════════════════════════════════════════════
    #  6단계: 뒷날개 (화이트)
    # ════════════════════════════════════════════════════
    bfx = X_BFLAP
    BFLM = bfx + mm(5)
    d.rectangle([(0, 0), (bfx + FLAP, H)], fill=(252, 252, 252))

    by = mm(14)
    d.text((BFLM, by), "시리즈 안내", fill=(60, 60, 60), font=f_fl_title)
    by += th(d, "시리즈 안내", f_fl_title) + mm(3)
    d.line([(BFLM, by), (bfx + FLAP - mm(5), by)],
           fill=(200, 200, 200), width=2)
    by += mm(4)
    d.text((BFLM, by), "특이점이 온 개발자",
           fill=(40, 40, 40), font=f_fl_title)
    by += th(d, "특이점이 온 개발자", f_fl_title) + mm(3)
    for t in ["AI 시대, 개발자의 새로운 출발점.",
              "같은 시리즈의 다른 책들도", "만나보세요."]:
        d.text((BFLM, by), t, fill=(110, 110, 110), font=f_fl_sm)
        by += th(d, t, f_fl_sm) + mm(2)
    by += mm(4)
    for other in SERIES_OTHER[b["id"]]:
        d.text((BFLM, by), f"  {other}", fill=(70, 70, 70), font=f_fl_body)
        by += th(d, other, f_fl_body) + mm(3)
    d.text((BFLM, H - BLEED - mm(6)), "books.openskill.kr",
           fill=(160, 160, 160), font=f_fl_sm)

    # ════════════════════════════════════════════════════
    #  7단계: 책등 (화이트, 제목은 관통 텍스트가 이미 지나감)
    # ════════════════════════════════════════════════════
    # 책등 영역은 이미 관통 제목이 그려져 있음
    # 추가로 세로 텍스트 (연한 회색)
    st = f"특이점이 온 개발자 — {b['title']} {b['sub']}"
    tmp = Image.new("RGBA", (H, SPINE), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    stw_ = tw(td, st, f_spine)
    td.text(((H - stw_) // 2, (SPINE - th(td, st, f_spine)) // 2),
            st, fill=(160, 160, 160), font=f_spine)
    aw = tw(td, "류재성", f_spine_sm)
    td.text((H - aw - mm(2), (SPINE - th(td, "류재성", f_spine_sm)) // 2),
            "류재성", fill=(180, 180, 180), font=f_spine_sm)
    img.paste(tmp.rotate(90, expand=True), (X_SPINE, 0),
              tmp.rotate(90, expand=True))

    # ════════════════════════════════════════════════════
    #  8단계: 재단 가이드
    # ════════════════════════════════════════════════════
    gc = (210, 210, 210)
    ml = mm(5)
    for cx, cy in [(BLEED, BLEED), (W - BLEED, BLEED),
                   (BLEED, H - BLEED), (W - BLEED, H - BLEED)]:
        dx_ = -1 if cx > W // 2 else 1
        dy_ = -1 if cy > H // 2 else 1
        d.line([(cx, cy), (cx, cy + dy_ * ml)], fill=gc, width=1)
        d.line([(cx, cy), (cx + dx_ * ml, cy)], fill=gc, width=1)
    d.line([(X_SPINE, 0), (X_SPINE, H)], fill=gc, width=1)
    d.line([(X_SPINE + SPINE, 0), (X_SPINE + SPINE, H)], fill=gc, width=1)
    for fold_x in [X_BACK, X_FFLAP]:
        for y in range(0, H, mm(5)):
            d.line([(fold_x, y), (fold_x, min(y + mm(2.5), H))],
                   fill=gc, width=1)

    return img


OUT = BASE
for b in BOOKS:
    img = create_spread(b)
    p = os.path.join(OUT, f"spread-v4.2-{b['id']}.png")
    img.save(p, dpi=(DPI, DPI))
    print(f"OK {p} ({img.size[0]}x{img.size[1]})")

print(f"\nv4.2 타이포그래피 스프레드형 — {len(BOOKS)}권 완료")
