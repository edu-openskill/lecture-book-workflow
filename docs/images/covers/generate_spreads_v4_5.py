#!/usr/bin/env python3
"""v4.5 — 혼공 스타일 스택형 타이포그래피
참고: '혼자 공부하는 컴퓨터구조+운영체제' (한빛미디어)
- 글자 자체가 디자인 (각 단어 크기 극적 차이)
- 엇갈린 배치 (왼/오/중앙 혼합)
- 화이트 배경 + 단일 액센트 컬러
- 회전 없음, 스태거링으로 역동성"""
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
f_spine    = F(1.8, bold=True)
f_spine_sm = F(1.3)
f_fl_title = F(6.5, bold=True)
f_fl_body  = F(5)
f_fl_sm    = F(4)


# ── 데이터 ──
# 각 책의 앞표지 레이아웃을 개별 정의
# lines: [(text, size_mm, bold, align, x_offset_mm, color_key)]
#   align: "L"=좌측정렬, "R"=우측정렬, "C"=중앙
#   x_offset_mm: 기본 정렬에서 추가 오프셋
#   color_key: "dark"=검정, "gray"=회색, "accent"=포인트컬러

BOOKS = [
    dict(
        id="docker", c1=(0, 128, 128),
        sub="개념편",
        tagline="컨테이너의 모든 것",
        top_descs=["컨테이너가 왜 필요한지 모를 때",
                   "Docker Compose로 서비스를 엮고 싶을 때",
                   "이야기로 시작하는 입문서가 필요할 때"],
        lines=[
            ("특이점이", 20, True, "L", 0, "dark"),
            ("온 개발자", 25, True, "R", 0, "gray"),
            ("_GAP", 12, False, "L", 0, "dark"),
            ("Docker", 55, True, "L", -2, "dark"),
        ],
        desc=["컨테이너가 왜 필요한지 모르겠다면,", "이 책이 출발점입니다.", "",
              "가상 머신과 컨테이너의 차이부터", "Docker Compose로 서비스를 엮는 법까지.",
              "이야기로 시작해서 실습으로 마무리합니다."],
    ),
    dict(
        id="msa", c1=(75, 60, 180),
        sub="개념편",
        tagline="마이크로서비스 아키텍처",
        top_descs=["모놀리스의 한계를 느꼈을 때",
                   "서비스를 쪼개야 하는 이유를 알고 싶을 때",
                   "이벤트 기반 통신을 이해하고 싶을 때"],
        lines=[
            ("특이점이", 20, True, "L", 0, "dark"),
            ("온 개발자", 25, True, "R", 0, "gray"),
            ("_GAP", 12, False, "L", 0, "dark"),
            ("MSA", 65, True, "L", -2, "dark"),
        ],
        desc=["모놀리스에서 마이크로서비스로,", "왜 쪼개야 하는지부터 시작합니다.", "",
              "서비스 분리, API Gateway, 이벤트 기반 통신.",
              "작은 서비스가 큰 시스템을 이루는 원리를", "이야기와 코드로 풀어냅니다."],
    ),
    dict(
        id="rag", c1=(120, 50, 160),
        sub="개념편",
        tagline="검색 증강 생성",
        top_descs=["LLM이 모르는 것에 답하게 만들고 싶을 때",
                   "임베딩과 벡터 검색을 이해하고 싶을 때",
                   "AI가 우리 데이터를 활용하게 만들고 싶을 때"],
        lines=[
            ("특이점이", 20, True, "L", 0, "dark"),
            ("온 개발자", 25, True, "R", 0, "gray"),
            ("_GAP", 12, False, "L", 0, "dark"),
            ("RAG", 65, True, "L", -2, "dark"),
        ],
        desc=["LLM이 모르는 걸 어떻게 답하게 할까?", "검색 증강 생성의 핵심을 짚습니다.", "",
              "임베딩, 벡터 검색, 프롬프트 엔지니어링.",
              "AI가 우리 데이터를 이해하게 만드는 법을", "처음부터 차근차근 안내합니다."],
    ),
    dict(
        id="tech-collection", c1=(180, 120, 30),
        sub="개념편",
        tagline="Docker부터 RabbitMQ까지 9가지 실습",
        authors="최주호, 류재성, 김주혁",
        top_descs=["Docker부터 RabbitMQ까지 한 권으로 정리하고 싶을 때",
                   "Spring 주변 기술이 처음일 때",
                   "이야기로 시작하는 실습서가 필요할 때"],
        badges=["Docker", "OAuth2", "Redis", "S3", "SSE",
                "WebSocket", "HLS", "Elasticsearch", "RabbitMQ"],
        lines=[
            ("특이점이", 20, True, "L", 0, "dark"),
            ("온 개발자", 25, True, "R", 0, "gray"),
            ("_GAP", 12, False, "L", 0, "dark"),
            ("Spring", 55, True, "L", -2, "dark"),
            ("Infra", 55, True, "R", 0, "gray"),
        ],
        desc=["Spring Boot 주변 기술 아홉 가지를", "한 권에 모았습니다.", "",
              "Docker, OAuth2, Redis, S3, SSE,",
              "WebSocket, HLS, Elasticsearch, RabbitMQ.",
              "이야기로 시작해서 실습으로 마무리합니다."],
    ),
]

SERIES_OTHER = {
    "docker": ["MSA 개념편", "RAG 개념편", "기술모음 개념편"],
    "msa": ["Docker 개념편", "RAG 개념편", "기술모음 개념편"],
    "rag": ["Docker 개념편", "MSA 개념편", "기술모음 개념편"],
    "tech-collection": ["Docker 개념편", "MSA 개념편", "RAG 개념편"],
}
AUTHOR_BIO = ["류재성", "", "메타코딩 유튜브 채널 운영자이자",
              "오픈스킬북스의 저자.", "",
              "복잡한 기술을 이야기로 풀어내는", "것을 좋아하며, AI 시대의 개발자가",
              "갖춰야 할 기술을 탐구합니다."]


def create_spread(b):
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    c1 = b["c1"]

    fx = X_FRONT
    LM = fx + mm(12)        # 앞표지 좌측 마진
    RM = fx + FRONT - mm(12) # 앞표지 우측 마진

    # ════════════════════════════════════════════════════
    #  앞표지 — 스택형 타이포그래피
    # ════════════════════════════════════════════════════

    # --- 상단 설명 텍스트 (혼공의 "코드 속에 숨어 있는..." 스타일) ---
    f_top = F(5.5)
    top_y = mm(12)
    for desc_line in b["top_descs"]:
        dw = tw(d, desc_line, f_top)
        d.text((RM - dw, top_y), desc_line, fill=(140, 140, 140), font=f_top)
        top_y += th(d, desc_line, f_top) + mm(2)

    # --- "특이점이 온 개발자" 왼쪽 정렬 (크게 + 타이포그래픽) ---
    # "특" 을 크게, "이점이" 를 이어서, "온" 을 크게
    f_big = F(28, bold=True)     # 특, 온 — 큰 글자
    f_mid = F(16, bold=True)     # 이점이 — 중간 글자
    f_dev = F(24, bold=True)     # 개발자

    # 1줄: 특 + 이점이  온
    x_cur = LM
    y_line1 = mm(35)
    # "특"
    d.text((x_cur, y_line1), "특", fill=(30, 30, 30), font=f_big)
    x_cur += tw(d, "특", f_big) + mm(0.5)
    # "이점이" (세로 정렬: 큰 글자 baseline에 맞춤)
    baseline_offset = mm(28) - mm(16)  # 큰 폰트와 중간 폰트 차이
    d.text((x_cur, y_line1 + baseline_offset), "이점이", fill=(80, 80, 80), font=f_mid)
    x_cur += tw(d, "이점이", f_mid) + mm(4)
    # "온"
    d.text((x_cur, y_line1), "온", fill=(30, 30, 30), font=f_big)

    # 2줄: 개발자
    y_line2 = y_line1 + mm(30)
    d.text((LM, y_line2), "개발자", fill=(40, 40, 40), font=f_dev)

    # --- 메인 타이틀 (큰 글씨) ---
    series_bottom = y_line2 + mm(28)

    # 메인 타이틀 크기 자동 조절
    main_lines = [(t, s, b_, a, x, c)
                  for t, s, b_, a, x, c in b["lines"]
                  if t not in ("특이점이", "온 개발자") and t != "_GAP"]

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

        # 색상
        if color_key == "dark":
            fill = (30, 30, 30)
        elif color_key == "gray":
            fill = (120, 120, 120)
        else:
            fill = (30, 30, 30)

        # X 위치
        if align == "L":
            x = LM + mm(x_off)
        elif align == "R":
            x = RM - t_w + mm(x_off)
        else:
            x = fx + (FRONT - t_w) // 2 + mm(x_off)

        # 그림자 (태양이 왼쪽에서 비추는 느낌 → 오른쪽 아래로 그림자)
        shadow_dx = mm(2.5)
        shadow_dy = mm(2.5)
        d.text((x + shadow_dx, cur_y + shadow_dy), text,
               fill=(235, 235, 235), font=font)

        # 본체
        d.text((x, cur_y), text, fill=fill, font=font)

        # 줄 높이: mm(cur_size)로 계산 (textbbox 대신 폰트 크기 기반)
        cur_y += mm(cur_size) + mm(2)

    # --- 태그라인 (메인 타이틀 아래) ---
    cur_y += mm(3)
    f_tag = F(7)
    d.text((LM, cur_y), b["tagline"], fill=(130, 130, 130), font=f_tag)

    # --- 배지 (키워드) 2열 중앙 정렬 ---
    badges = b.get("badges", [])
    if badges:
        cur_y += th(d, b["tagline"], f_tag) + mm(5)
        f_badge = F(3.5)
        badge_h = mm(5)
        badge_pad_x = mm(2.5)
        badge_gap = mm(1.5)
        row_gap = mm(2)
        mid = len(badges) // 2 + len(badges) % 2  # 5 / 4 split for 9
        rows = [badges[:mid], badges[mid:]]
        for row in rows:
            bx = LM  # 왼쪽 정렬
            for badge_text in row:
                bw = tw(d, badge_text, f_badge) + badge_pad_x * 2
                d.rounded_rectangle(
                    [(bx, cur_y), (bx + bw, cur_y + badge_h)],
                    radius=mm(3),
                    fill=(240, 243, 248),
                    outline=(220, 225, 235),
                )
                # 텍스트 수직 중앙: textbbox 기반 정확한 계산
                bb = d.textbbox((0, 0), badge_text, font=f_badge)
                text_h = bb[3] - bb[1]
                ty = cur_y + (badge_h - text_h) // 2 - bb[1]
                d.text((bx + badge_pad_x, ty), badge_text,
                       fill=(70, 85, 105), font=f_badge)
                bx += bw + badge_gap
            cur_y += badge_h + row_gap

    # --- 우측 하단: 개념편 + 저자 (수직 정렬) ---
    f_sub_title = F(16, bold=True)
    sub_text = b["sub"]
    sub_w = tw(d, sub_text, f_sub_title)
    # 구분선
    line_w = mm(40)
    sub_y = H - mm(40)
    d.rectangle([(RM - line_w, sub_y - mm(3)),
                 (RM, sub_y - mm(3) + mm(0.8))], fill=c1)
    # 개념편
    d.text((RM - sub_w, sub_y), sub_text, fill=c1, font=f_sub_title)
    # 저자 (개념편 바로 아래, 우측 정렬)
    f_author = F(4)
    author_text = b.get("authors", "류재성") + " 지음"
    aw_val = tw(d, author_text, f_author)
    d.text((RM - aw_val, H - mm(18)), author_text, fill=(130, 130, 130), font=f_author)

    # --- 출판사 (좌측 하단) ---
    f_pub_name = F(7, bold=True)
    f_pub_icon = F(6)
    pub_y = H - mm(25)
    d.text((LM, pub_y), "OPENSKILL BOOKS", fill=(160, 160, 160), font=f_pub_name)
    d.text((LM, pub_y + mm(8)), "오픈스킬북스", fill=(180, 180, 180), font=f_pub_icon)

    # ════════════════════════════════════════════════════
    #  뒷표지 — 고스트 타이틀 + 설명
    # ════════════════════════════════════════════════════
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

    # ════════════════════════════════════════════════════
    #  앞날개
    # ════════════════════════════════════════════════════
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

    # ════════════════════════════════════════════════════
    #  뒷날개
    # ════════════════════════════════════════════════════
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

    # ════════════════════════════════════════════════════
    #  책등
    # ════════════════════════════════════════════════════
    main_title = b["lines"][3][0]
    if b["id"] == "tech-collection":
        main_title = "기술모음"
    st = f"특이점이 온 개발자 — {main_title} {b['sub']}"
    tmp = Image.new("RGBA", (H, SPINE), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    stw_ = tw(td, st, f_spine)
    td.text(((H - stw_) // 2, (SPINE - th(td, st, f_spine)) // 2),
            st, fill=(100, 100, 100), font=f_spine)
    spine_author = b.get("authors", "류재성").split(",")[0].strip()
    aw = tw(td, spine_author, f_spine_sm)
    td.text((H - aw - mm(2), (SPINE - th(td, spine_author, f_spine_sm)) // 2),
            spine_author, fill=(150, 150, 150), font=f_spine_sm)
    img.paste(tmp.rotate(90, expand=True), (X_SPINE, 0),
              tmp.rotate(90, expand=True))

    return img


def extract_front_cover(spread_img):
    """가이드 라인 그리기 전 스프레드에서 앞표지만 추출 — 전자책용"""
    return spread_img.crop((X_FRONT, BLEED, X_FRONT + FRONT, H - BLEED))


def draw_guides(img):
    """재단 가이드 + 접힘선 그리기 — POD 전용"""
    d = ImageDraw.Draw(img)
    gc = (215, 215, 215)
    ml = int(5 * MM)
    for cx, cy in [(BLEED, BLEED), (W - BLEED, BLEED),
                   (BLEED, H - BLEED), (W - BLEED, H - BLEED)]:
        dx_ = -1 if cx > W // 2 else 1
        dy_ = -1 if cy > H // 2 else 1
        d.line([(cx, cy), (cx, cy + dy_ * ml)], fill=gc, width=1)
        d.line([(cx, cy), (cx + dx_ * ml, cy)], fill=gc, width=1)
    d.line([(X_SPINE, 0), (X_SPINE, H)], fill=gc, width=1)
    d.line([(X_SPINE + SPINE, 0), (X_SPINE + SPINE, H)], fill=gc, width=1)
    for fold_x in [X_BACK, X_FFLAP]:
        for y in range(0, H, int(5 * MM)):
            d.line([(fold_x, y), (fold_x, min(y + int(2.5 * MM), H))],
                   fill=gc, width=1)


OUT = BASE
for b in BOOKS:
    img = create_spread(b)
    # 전자책용 앞표지 (가이드 없이 깨끗하게)
    front = extract_front_cover(img)
    fp = os.path.join(OUT, f"cover-v4.5-{b['id']}.png")
    front.save(fp, dpi=(DPI, DPI))
    print(f"OK {fp} ({front.size[0]}x{front.size[1]})")
    # POD용 전체 스프레드 (가이드 추가)
    draw_guides(img)
    p = os.path.join(OUT, f"spread-v4.5-{b['id']}.png")
    img.save(p, dpi=(DPI, DPI))
    print(f"OK {p} ({img.size[0]}x{img.size[1]})")

print(f"\nv4.5 혼공 스타일 스택형 타이포그래피 — {len(BOOKS)}권 완료")
