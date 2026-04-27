#!/usr/bin/env python3
"""표지 공통 모듈 — 상수, 헬퍼, 공유 렌더링 함수"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── 상수 ──
DPI = 300
MM = DPI / 25.4

FLAP  = int(80 * MM)
BACK  = int(182 * MM)
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


# ── 헬퍼 ──
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
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]

def tw(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]


# ── 공통 폰트 ──
f_pub      = F(7)
f_series_s = F(6)
f_bk_desc  = F(7)
f_bk_pub   = F(9, bold=True)
f_bk_eng   = F(6.5)
f_bk_url   = F(5.5)
f_price    = F(7, bold=True)
f_isbn     = F(5)
f_isbn_sm  = F(4)
f_spine_f  = F(1.8, bold=True)
f_spine_sm = F(1.3)
f_fl_title = F(6.5, bold=True)
f_fl_body  = F(5)
f_fl_sm    = F(4)


# ── 데이터 (4권) ──
BOOKS = [
    dict(
        id="docker", c1=(0, 128, 128),
        title="Docker", sub="개념편",
        tagline="컨테이너의 모든 것",
        top_descs=["컨테이너가 왜 필요한지 모를 때",
                   "Docker Compose로 서비스를 엮고 싶을 때",
                   "이야기로 시작하는 입문서가 필요할 때"],
        desc=["컨테이너가 왜 필요한지 모르겠다면,",
              "이 책이 출발점입니다.", "",
              "가상 머신과 컨테이너의 차이부터",
              "Docker Compose로 서비스를 엮는 법까지.",
              "이야기로 시작해서 실습으로 마무리합니다."],
    ),
    dict(
        id="msa", c1=(75, 60, 180),
        title="MSA", sub="개념편",
        tagline="마이크로서비스 아키텍처",
        top_descs=["모놀리스의 한계를 느꼈을 때",
                   "서비스를 쪼개야 하는 이유를 알고 싶을 때",
                   "이벤트 기반 통신을 이해하고 싶을 때"],
        desc=["모놀리스에서 마이크로서비스로,",
              "왜 쪼개야 하는지부터 시작합니다.", "",
              "서비스 분리, API Gateway, 이벤트 기반 통신.",
              "작은 서비스가 큰 시스템을 이루는 원리를",
              "이야기와 코드로 풀어냅니다."],
    ),
    dict(
        id="rag", c1=(120, 50, 160),
        title="RAG", sub="개념편",
        tagline="검색 증강 생성",
        top_descs=["LLM이 모르는 것에 답하게 만들고 싶을 때",
                   "임베딩과 벡터 검색을 이해하고 싶을 때",
                   "AI가 우리 데이터를 활용하게 만들고 싶을 때"],
        desc=["LLM이 모르는 걸 어떻게 답하게 할까?",
              "검색 증강 생성의 핵심을 짚습니다.", "",
              "임베딩, 벡터 검색, 프롬프트 엔지니어링.",
              "AI가 우리 데이터를 이해하게 만드는 법을",
              "처음부터 차근차근 안내합니다."],
    ),
    dict(
        id="spring", c1=(180, 120, 30),
        title="Spring", sub="개념편",
        tagline="9가지 기술",
        top_descs=["OAuth와 OIDC를 제대로 이해하고 싶을 때",
                   "Spring Security 설정이 막막할 때",
                   "인증/인가의 흐름을 한눈에 보고 싶을 때"],
        desc=["Spring 생태계의 9가지 핵심 기술을",
              "한 권에 담았습니다.", "",
              "OAuth, OIDC, Spring Security부터",
              "실전 인증/인가 흐름까지.",
              "이야기와 실습으로 정리합니다."],
    ),
]

SERIES_OTHER = {
    "docker": ["MSA 개념편", "RAG 개념편", "Spring 개념편"],
    "msa":    ["Docker 개념편", "RAG 개념편", "Spring 개념편"],
    "rag":    ["Docker 개념편", "MSA 개념편", "Spring 개념편"],
    "spring": ["Docker 개념편", "MSA 개념편", "RAG 개념편"],
}

AUTHOR_BIO = [
    "류재성", "",
    "메타코딩 유튜브 채널 운영자이자",
    "오픈스킬북스의 저자.", "",
    "복잡한 기술을 이야기로 풀어내는",
    "것을 좋아하며, AI 시대의 개발자가",
    "갖춰야 할 기술을 탐구합니다.",
]


# ══════════════════════════════════════════════════
#  공유 렌더링 함수
# ══════════════════════════════════════════════════

def new_spread():
    """빈 스프레드 이미지 + Draw 반환"""
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    return img, d


def render_back_cover(img, d, b):
    """뒷표지 렌더링"""
    bx = X_BACK
    BLM = bx + mm(10)

    # 시리즈 라벨
    d.text((BLM, mm(12)), "특이점이 온 개발자 시리즈",
           fill=(160, 160, 160), font=F(7, bold=True))
    d.line([(BLM, mm(21)), (bx + BACK - mm(10), mm(21))],
           fill=(230, 230, 230), width=1)

    # 설명 텍스트
    desc_y = int(H * 0.55)
    for line in b["desc"]:
        if line == "":
            desc_y += mm(5)
            continue
        d.text((BLM, desc_y), line, fill=(60, 60, 60), font=f_bk_desc)
        desc_y += th(d, line, f_bk_desc) + mm(3)

    desc_y += mm(6)
    d.line([(BLM, desc_y), (bx + BACK - mm(10), desc_y)],
           fill=(230, 230, 230), width=1)
    desc_y += mm(5)

    d.text((BLM, desc_y), "오픈스킬북스", fill=(60, 60, 60), font=f_bk_pub)
    desc_y += th(d, "오픈스킬북스", f_bk_pub) + mm(2)
    d.text((BLM, desc_y), "OPENSKILL BOOKS", fill=(150, 150, 150), font=f_bk_eng)
    desc_y += th(d, "OPENSKILL BOOKS", f_bk_eng) + mm(1.5)
    d.text((BLM, desc_y), "books.openskill.kr", fill=(150, 150, 150), font=f_bk_url)

    # ISBN + 가격
    bc_w, bc_h = mm(50), mm(28)
    bc_x = bx + BACK - mm(10) - bc_w
    bc_y = H - BLEED - mm(18) - bc_h
    d.rectangle([(bc_x, bc_y), (bc_x + bc_w, bc_y + bc_h)],
                outline=(210, 210, 210), width=2)
    it = "ISBN 000-00-0000-000-0"
    d.text((bc_x + (bc_w - tw(d, it, f_isbn)) // 2, bc_y + mm(4)),
           it, fill=(170, 170, 170), font=f_isbn)
    pt = "(ISBN 발급 후 교체)"
    d.text((bc_x + (bc_w - tw(d, pt, f_isbn_sm)) // 2, bc_y + bc_h - mm(5)),
           pt, fill=(190, 190, 190), font=f_isbn_sm)
    d.text((bc_x, bc_y - mm(8)), "정가 15,000원", fill=(60, 60, 60), font=f_price)

    d.text((BLM, H - BLEED - mm(5)), "books.openskill.kr",
           fill=(190, 190, 190), font=f_bk_url)


def render_front_flap(img, d):
    """앞날개 (저자 소개)"""
    ffx = X_FFLAP
    FLM = ffx + mm(5)
    d.rectangle([(ffx, 0), (ffx + FLAP + BLEED, H)], fill=(252, 252, 252))
    fy = mm(14)
    d.text((FLM, fy), "저자 소개", fill=(60, 60, 60), font=f_fl_title)
    fy += th(d, "저자 소개", f_fl_title) + mm(3)
    d.line([(FLM, fy), (ffx + FLAP - mm(5), fy)], fill=(210, 210, 210), width=2)
    fy += mm(4)
    for line in AUTHOR_BIO:
        if line == "":
            fy += mm(3)
            continue
        d.text((FLM, fy), line, fill=(70, 70, 70), font=f_fl_body)
        fy += th(d, line, f_fl_body) + mm(2.5)
    d.text((FLM, H - BLEED - mm(6)), "openskill.kr",
           fill=(170, 170, 170), font=f_fl_sm)


def render_back_flap(img, d, b):
    """뒷날개 (시리즈 안내)"""
    bfx = X_BFLAP
    BFLM = bfx + mm(5)
    d.rectangle([(0, 0), (bfx + FLAP, H)], fill=(252, 252, 252))
    by = mm(14)
    d.text((BFLM, by), "시리즈 안내", fill=(60, 60, 60), font=f_fl_title)
    by += th(d, "시리즈 안내", f_fl_title) + mm(3)
    d.line([(BFLM, by), (bfx + FLAP - mm(5), by)], fill=(210, 210, 210), width=2)
    by += mm(4)
    d.text((BFLM, by), "특이점이 온 개발자", fill=(40, 40, 40), font=f_fl_title)
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
           fill=(170, 170, 170), font=f_fl_sm)


def render_spine(img, d, b):
    """책등"""
    st = f"특이점이 온 개발자 — {b['title']} {b['sub']}"
    tmp = Image.new("RGBA", (H, SPINE), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    stw_ = tw(td, st, f_spine_f)
    td.text(((H - stw_) // 2, (SPINE - th(td, st, f_spine_f)) // 2),
            st, fill=(100, 100, 100), font=f_spine_f)
    aw = tw(td, "류재성", f_spine_sm)
    td.text((H - aw - mm(2), (SPINE - th(td, "류재성", f_spine_sm)) // 2),
            "류재성", fill=(150, 150, 150), font=f_spine_sm)
    img.paste(tmp.rotate(90, expand=True), (X_SPINE, 0),
              tmp.rotate(90, expand=True))


def render_crop_guides(img, d):
    """재단 가이드"""
    gc = (215, 215, 215)
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


def build_spread(b, render_front_fn):
    """공통 스프레드 조립: 뒷표지+날개+책등+재단가이드 + 커스텀 앞표지"""
    img, d = new_spread()
    render_back_cover(img, d, b)
    render_front_flap(img, d)
    render_back_flap(img, d, b)
    render_spine(img, d, b)
    render_front_fn(img, d, b)
    render_crop_guides(img, d)
    return img


def save_spreads(version, render_front_fn):
    """4권 모두 생성하고 저장"""
    for b in BOOKS:
        img = build_spread(b, render_front_fn)
        p = os.path.join(BASE, f"spread-{version}-{b['id']}.png")
        img.save(p, dpi=(DPI, DPI))
        print(f"OK {p} ({img.size[0]}x{img.size[1]})")
    print(f"\n{version} — {len(BOOKS)}권 완료")
