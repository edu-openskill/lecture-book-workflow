#!/usr/bin/env python3
"""v4.4 — 타이포그래피 레이아웃 개선
- 특이점이 온 / 개발자: 크기 차등 + 오프셋 배치 + 사선
- 메인 제목: 좌측 정렬로 역동적 배치
- 설명 텍스트 위치 최적화
- 뒷표지 고스트 제목 위치 조정"""
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
    bb = draw.textbbox((0,0), text, font=font)
    return bb[3] - bb[1]

def tw(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[2] - bb[0]

def draw_rotated_text(img, x, y, text, font, fill, angle):
    """회전된 텍스트 (x,y = 중심점)"""
    d_tmp = ImageDraw.Draw(img)
    bb = d_tmp.textbbox((0,0), text, font=font)
    tw_ = bb[2] - bb[0]
    th_ = bb[3] - bb[1]
    pad = max(tw_, th_)
    canvas = Image.new("RGBA", (tw_ + pad*2, th_ + pad*2), (0,0,0,0))
    cd = ImageDraw.Draw(canvas)
    cd.text((pad, pad), text, fill=fill, font=font)
    rotated = canvas.rotate(angle, resample=Image.BICUBIC, expand=True)
    rw, rh = rotated.size
    img.paste(rotated, (x - rw//2, y - rh//2), rotated)


# ── 폰트 ──
f_series_s = F(6)
f_sub      = F(16, bold=True)
f_pub      = F(7)
f_tagline  = F(8)
f_small_desc = F(6)

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
         title_size=70,
         tagline="컨테이너의 모든 것",
         small_desc=["이야기로 시작해서","실습으로 마무리하는 입문서"],
         desc=["컨테이너가 왜 필요한지 모르겠다면,","이 책이 출발점입니다.","",
               "가상 머신과 컨테이너의 차이부터","Docker Compose로 서비스를 엮는 법까지.",
               "이야기로 시작해서 실습으로 마무리합니다."]),
    dict(id="msa", title="MSA", sub="개념편",
         c1=(75,60,180),
         title_size=85,
         tagline="마이크로서비스 아키텍처",
         small_desc=["모놀리스의 한계를 넘어서는","아키텍처 입문서"],
         desc=["모놀리스에서 마이크로서비스로,","왜 쪼개야 하는지부터 시작합니다.","",
               "서비스 분리, API Gateway, 이벤트 기반 통신.",
               "작은 서비스가 큰 시스템을 이루는 원리를","이야기와 코드로 풀어냅니다."]),
    dict(id="rag", title="RAG", sub="개념편",
         c1=(120,50,160),
         title_size=85,
         tagline="검색 증강 생성",
         small_desc=["LLM이 모르는 것에 답하게 만드는","AI 입문서"],
         desc=["LLM이 모르는 걸 어떻게 답하게 할까?","검색 증강 생성의 핵심을 짚습니다.","",
               "임베딩, 벡터 검색, 프롬프트 엔지니어링.",
               "AI가 우리 데이터를 이해하게 만드는 법을","처음부터 차근차근 안내합니다."]),
    dict(id="tech-collection", title="기술모음", sub="개념편",
         c1=(180,120,30),
         title_size=55,
         tagline="개발자 필수 기술 총정리",
         small_desc=["개발자라면 반드시 알아야 할","필수 기술 가이드"],
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

    fx = X_FRONT
    LM = fx + mm(12)   # 앞표지 좌측 마진
    RM = fx + FRONT - mm(12)

    # ════════════════════════════════════════════════════
    #  앞표지
    # ════════════════════════════════════════════════════

    # --- "특이점이 온 / 개발자" 사선 + 크기 차등 ---
    f_s1 = F(13, bold=True)   # "특이점이 온" (작게)
    f_s2 = F(28, bold=True)   # "개발자" (크게)

    # "특이점이 온" — 우측 정렬, 살짝 위
    s1 = "특이점이 온"
    s1w = tw(d, s1, f_s1)
    s1_x = RM - s1w
    s1_y = mm(18)
    draw_rotated_text(img, s1_x + s1w//2, s1_y, s1, f_s1, (50,50,50), 5)

    # "개발자" — 우측 정렬, 아래로, 더 크게
    s2 = "개발자"
    s2w = tw(d, s2, f_s2)
    s2_x = RM - s2w + mm(5)
    s2_y = mm(38)
    draw_rotated_text(img, s2_x + s2w//2, s2_y, s2, f_s2, (25,25,25), 5)

    d = ImageDraw.Draw(img)

    # --- 작은 설명 (두 줄, 좌측) ---
    sd_y = mm(62)
    for line in b["small_desc"]:
        d.text((LM, sd_y), line, fill=(130,130,130), font=f_small_desc)
        sd_y += th(d, line, f_small_desc) + mm(1.5)

    # --- 얇은 구분선 ---
    d.line([(LM, sd_y + mm(3)), (RM, sd_y + mm(3))],
           fill=(220,220,220), width=1)

    # --- 메인 제목 (좌측 정렬, 역동적) ---
    f_title = F(b["title_size"], bold=True)
    title_text = b["title"]
    title_tw = tw(d, title_text, f_title)
    title_th = th(d, title_text, f_title)

    # 앞표지 폭에 맞게 조절
    if title_tw > FRONT - mm(20):
        ratio = (FRONT - mm(24)) / title_tw
        f_title = F(int(b["title_size"] * ratio), bold=True)
        title_tw = tw(d, title_text, f_title)
        title_th = th(d, title_text, f_title)

    title_x = LM - mm(2)  # 좌측 정렬 (약간 밖으로)
    title_y = sd_y + mm(8)
    d.text((title_x, title_y), title_text, fill=(20,20,20), font=f_title)

    # --- "개념편" + 컬러 언더라인 (제목 아래 좌측) ---
    sub_y = title_y + title_th + mm(3)
    line_x = LM
    line_w = mm(35)
    d.rectangle([(line_x, sub_y), (line_x + line_w, sub_y + mm(1.2))], fill=c1)
    d.text((line_x, sub_y + mm(4)), b["sub"], fill=c1, font=f_sub)

    # --- 태그라인 (부제 아래) ---
    tag_y = sub_y + mm(4) + th(d, b["sub"], f_sub) + mm(5)
    d.text((LM, tag_y), b["tagline"], fill=(110,110,110), font=f_tagline)

    # --- 하단 출판사 ---
    ptxt = "OPENSKILL BOOKS"
    pw_ = tw(d, ptxt, f_pub)
    d.text((fx + (FRONT - pw_)//2, H - mm(22)),
           ptxt, fill=(170,170,170), font=f_pub)

    stxt2 = "특이점이 온 개발자 시리즈"
    sw2 = tw(d, stxt2, f_series_s)
    d.text((fx + FRONT - sw2 - mm(4), H - BLEED - mm(5)),
           stxt2, fill=(195,195,195), font=f_series_s)

    # ════════════════════════════════════════════════════
    #  뒷표지 — 고스트 제목 (상단, 잘림 느낌)
    # ════════════════════════════════════════════════════
    bx = X_BACK
    BLM = bx + mm(10)

    # 고스트 제목: 뒷표지 상단에 크게, 오른쪽이 잘리는 느낌
    f_ghost = F(b["title_size"] + 10, bold=True)
    ghost_text = title_text
    ghost_x = bx + mm(5)
    ghost_y = mm(15)
    d.text((ghost_x, ghost_y), ghost_text, fill=(242,242,242), font=f_ghost)

    # 시리즈 라벨 (상단)
    d.text((BLM, mm(10)), "특이점이 온 개발자 시리즈",
           fill=(170,170,170), font=F(6.5, bold=True))

    # 설명 텍스트 (중앙~하단)
    desc_y = int(H * 0.48)
    for line in b["desc"]:
        if line == "":
            desc_y += mm(4); continue
        d.text((BLM, desc_y), line, fill=(60,60,60), font=f_bk_desc)
        desc_y += th(d, line, f_bk_desc) + mm(3)

    desc_y += mm(5)
    d.line([(BLM, desc_y), (bx + BACK - mm(10), desc_y)],
           fill=(230,230,230), width=1)
    desc_y += mm(4)

    d.text((BLM, desc_y), "오픈스킬북스", fill=(60,60,60), font=f_bk_pub)
    desc_y += th(d, "오픈스킬북스", f_bk_pub) + mm(2)
    d.text((BLM, desc_y), "OPENSKILL BOOKS", fill=(150,150,150), font=f_bk_eng)
    desc_y += th(d, "OPENSKILL BOOKS", f_bk_eng) + mm(1.5)
    d.text((BLM, desc_y), "books.openskill.kr", fill=(150,150,150), font=f_bk_url)

    # ISBN + 가격
    bc_w, bc_h = mm(50), mm(28)
    bc_x = bx + BACK - mm(10) - bc_w
    bc_y = H - BLEED - mm(18) - bc_h
    d.rectangle([(bc_x, bc_y), (bc_x+bc_w, bc_y+bc_h)],
                outline=(215,215,215), width=2)
    it = "ISBN 000-00-0000-000-0"
    d.text((bc_x+(bc_w-tw(d,it,f_isbn))//2, bc_y+mm(4)),
           it, fill=(175,175,175), font=f_isbn)
    pt = "(ISBN 발급 후 교체)"
    d.text((bc_x+(bc_w-tw(d,pt,f_isbn_sm))//2, bc_y+bc_h-mm(5)),
           pt, fill=(195,195,195), font=f_isbn_sm)
    d.text((bc_x, bc_y-mm(8)), "정가 15,000원", fill=(60,60,60), font=f_price)

    d.text((BLM, H - BLEED - mm(5)), "books.openskill.kr",
           fill=(195,195,195), font=f_bk_url)

    # ════════════════════════════════════════════════════
    #  앞날개
    # ════════════════════════════════════════════════════
    ffx = X_FFLAP
    FLM = ffx + mm(5)
    d.rectangle([(ffx, 0), (ffx+FLAP+BLEED, H)], fill=(252,252,252))
    fy = mm(14)
    d.text((FLM, fy), "저자 소개", fill=(60,60,60), font=f_fl_title)
    fy += th(d, "저자 소개", f_fl_title) + mm(3)
    d.line([(FLM, fy), (ffx+FLAP-mm(5), fy)], fill=(215,215,215), width=2)
    fy += mm(4)
    for line in AUTHOR_BIO:
        if line == "":
            fy += mm(3); continue
        d.text((FLM, fy), line, fill=(70,70,70), font=f_fl_body)
        fy += th(d, line, f_fl_body) + mm(2.5)
    d.text((FLM, H-BLEED-mm(6)), "openskill.kr", fill=(175,175,175), font=f_fl_sm)

    # ════════════════════════════════════════════════════
    #  뒷날개
    # ════════════════════════════════════════════════════
    bfx = X_BFLAP
    BFLM = bfx + mm(5)
    d.rectangle([(0, 0), (bfx+FLAP, H)], fill=(252,252,252))
    by = mm(14)
    d.text((BFLM, by), "시리즈 안내", fill=(60,60,60), font=f_fl_title)
    by += th(d, "시리즈 안내", f_fl_title) + mm(3)
    d.line([(BFLM, by), (bfx+FLAP-mm(5), by)], fill=(215,215,215), width=2)
    by += mm(4)
    d.text((BFLM, by), "특이점이 온 개발자", fill=(40,40,40), font=f_fl_title)
    by += th(d, "특이점이 온 개발자", f_fl_title) + mm(3)
    for t in ["AI 시대, 개발자의 새로운 출발점.",
              "같은 시리즈의 다른 책들도", "만나보세요."]:
        d.text((BFLM, by), t, fill=(115,115,115), font=f_fl_sm)
        by += th(d, t, f_fl_sm) + mm(2)
    by += mm(4)
    for other in SERIES_OTHER[b["id"]]:
        d.text((BFLM, by), f"  {other}", fill=(70,70,70), font=f_fl_body)
        by += th(d, other, f_fl_body) + mm(3)
    d.text((BFLM, H-BLEED-mm(6)), "books.openskill.kr",
           fill=(175,175,175), font=f_fl_sm)

    # ════════════════════════════════════════════════════
    #  책등
    # ════════════════════════════════════════════════════
    st = f"특이점이 온 개발자 — {b['title']} {b['sub']}"
    tmp = Image.new("RGBA", (H, SPINE), (0,0,0,0))
    td = ImageDraw.Draw(tmp)
    stw_ = tw(td, st, f_spine)
    td.text(((H-stw_)//2, (SPINE-th(td,st,f_spine))//2),
            st, fill=(110,110,110), font=f_spine)
    aw = tw(td, "류재성", f_spine_sm)
    td.text((H-aw-mm(2), (SPINE-th(td,"류재성",f_spine_sm))//2),
            "류재성", fill=(160,160,160), font=f_spine_sm)
    img.paste(tmp.rotate(90, expand=True), (X_SPINE, 0),
              tmp.rotate(90, expand=True))

    # ════════════════════════════════════════════════════
    #  재단 가이드
    # ════════════════════════════════════════════════════
    gc = (218,218,218)
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
    p = os.path.join(OUT, f"spread-v4.4-{b['id']}.png")
    img.save(p, dpi=(DPI,DPI))
    print(f"OK {p} ({img.size[0]}x{img.size[1]})")

print(f"\nv4.4 타이포그래피 레이아웃 개선 — {len(BOOKS)}권 완료")
