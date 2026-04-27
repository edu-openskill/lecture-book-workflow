#!/usr/bin/env python3
"""v4.3 — 점프투파이썬 스타일 타이포그래피
1. 제목이 앞표지 안에서 크게 (전부 보이게)
2. '특이점이 온 개발자' 사선 기울임 + 두 줄
3. 뒷표지까지 제목 잘린 부분이 이어지는 느낌
4. 전면 화이트, 다이나믹한 타이포그래피 레이아웃"""
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


# ── 폰트 ──
f_series_s = F(6)
f_sub      = F(14, bold=True)
f_author   = F(8, bold=True)
f_pub      = F(7)
f_tagline  = F(8)
f_small_desc = F(6.5)

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
         title_size=75,
         tagline="컨테이너의 모든 것",
         small_desc="중학생도 첫날부터 실습하는  초고속 입문서",
         desc=["컨테이너가 왜 필요한지 모르겠다면,","이 책이 출발점입니다.","",
               "가상 머신과 컨테이너의 차이부터","Docker Compose로 서비스를 엮는 법까지.",
               "이야기로 시작해서 실습으로 마무리합니다."]),
    dict(id="msa", title="MSA", sub="개념편",
         c1=(75,60,180),
         title_size=90,
         tagline="마이크로서비스 아키텍처",
         small_desc="모놀리스의 한계를 넘어서는  아키텍처 입문서",
         desc=["모놀리스에서 마이크로서비스로,","왜 쪼개야 하는지부터 시작합니다.","",
               "서비스 분리, API Gateway, 이벤트 기반 통신.",
               "작은 서비스가 큰 시스템을 이루는 원리를","이야기와 코드로 풀어냅니다."]),
    dict(id="rag", title="RAG", sub="개념편",
         c1=(120,50,160),
         title_size=90,
         tagline="검색 증강 생성",
         small_desc="LLM이 모르는 것에 답하게 만드는  AI 입문서",
         desc=["LLM이 모르는 걸 어떻게 답하게 할까?","검색 증강 생성의 핵심을 짚습니다.","",
               "임베딩, 벡터 검색, 프롬프트 엔지니어링.",
               "AI가 우리 데이터를 이해하게 만드는 법을","처음부터 차근차근 안내합니다."]),
    dict(id="tech-collection", title="기술모음", sub="개념편",
         c1=(180,120,30),
         title_size=60,
         tagline="개발자 필수 기술 총정리",
         small_desc="개발자라면 반드시 알아야 할  필수 기술 가이드",
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


def draw_rotated_text(img, x, y, text, font, fill, angle):
    """회전된 텍스트를 이미지에 그리기"""
    d_tmp = ImageDraw.Draw(img)
    bb = d_tmp.textbbox((0,0), text, font=font)
    tw_ = bb[2] - bb[0]
    th_ = bb[3] - bb[1]

    # 넉넉한 캔버스
    pad = max(tw_, th_)
    canvas = Image.new("RGBA", (tw_ + pad*2, th_ + pad*2), (0,0,0,0))
    cd = ImageDraw.Draw(canvas)
    cd.text((pad, pad), text, fill=fill, font=font)

    rotated = canvas.rotate(angle, resample=Image.BICUBIC, expand=True)

    # 중심점 보정
    rw, rh = rotated.size
    paste_x = x - rw // 2
    paste_y = y - rh // 2

    img.paste(rotated, (paste_x, paste_y), rotated)


def create_spread(b):
    img = Image.new("RGB", (W, H), (255,255,255))
    d = ImageDraw.Draw(img)
    c1 = b["c1"]

    fx = X_FRONT
    f_title = F(b["title_size"], bold=True)

    # ════════════════════════════════════════════════════
    #  앞표지
    # ════════════════════════════════════════════════════

    # --- "특이점이 온 개발자" 사선 기울임 두 줄 (상단) ---
    f_series_line1 = F(18, bold=True)
    f_series_line2 = F(22, bold=True)

    line1 = "특이점이 온"
    line2 = "개발자"

    # 앞표지 상단에 사선으로 배치 (약 -8도 기울임)
    angle = 8
    cx1 = fx + FRONT // 2 - mm(5)
    cy1 = mm(28)
    draw_rotated_text(img, cx1, cy1, line1, f_series_line1, (30,30,30), angle)

    cx2 = fx + FRONT // 2 + mm(12)
    cy2 = mm(50)
    draw_rotated_text(img, cx2, cy2, line2, f_series_line2, (30,30,30), angle)

    d = ImageDraw.Draw(img)  # 재생성

    # --- 작은 설명 텍스트 (점프투파이썬의 "중학생도 첫날부터~" 스타일) ---
    sd_w = tw(d, b["small_desc"], f_small_desc)
    d.text((fx + (FRONT - sd_w)//2, mm(68)),
           b["small_desc"], fill=(100,100,100), font=f_small_desc)

    # --- 메인 제목 (앞표지 안에서 크게, 전부 보이게) ---
    title_text = b["title"]
    title_tw = tw(d, title_text, f_title)
    title_th = th(d, title_text, f_title)

    # 앞표지 중앙에 배치 (좌우 여백 고려)
    title_x = fx + (FRONT - title_tw) // 2
    title_y = int(H * 0.32)

    # 제목이 앞표지보다 넓으면 크기 조절
    if title_tw > FRONT - mm(10):
        # 폰트 줄여서 다시
        adjusted_size = b["title_size"] * (FRONT - mm(15)) // title_tw
        f_title = F(adjusted_size, bold=True)
        title_tw = tw(d, title_text, f_title)
        title_th = th(d, title_text, f_title)
        title_x = fx + (FRONT - title_tw) // 2

    d.text((title_x, title_y), title_text, fill=(25,25,25), font=f_title)

    # --- 뒷표지에 잘린 느낌으로 제목 반복 (왼쪽에 걸쳐서) ---
    bx = X_BACK
    # 뒷표지 오른쪽 끝에서 잘리도록 배치
    f_back_title = F(b["title_size"], bold=True)
    back_tw = tw(d, title_text, f_back_title)
    # 글자의 오른쪽 1/3만 보이도록
    back_x = bx + BACK - int(back_tw * 0.35)
    back_y = int(H * 0.18)
    back_c = (240, 240, 240)  # 매우 연하게
    d.text((back_x, back_y), title_text, fill=back_c, font=f_back_title)

    # --- 부제 "개념편" + 컬러 언더라인 ---
    sub_y = title_y + title_th + mm(5)

    # 언더라인 (포인트 컬러 — 점프투파이썬의 밑줄 느낌)
    line_w = mm(40)
    line_x = fx + (FRONT - line_w) // 2
    line_thick = mm(1.2)
    d.rectangle([(line_x, sub_y), (line_x + line_w, sub_y + line_thick)], fill=c1)

    sub_text_y = sub_y + mm(4)
    sub_w = tw(d, b["sub"], f_sub)
    d.text((fx + (FRONT - sub_w)//2, sub_text_y), b["sub"], fill=c1, font=f_sub)

    # --- 태그라인 ---
    tag_y = sub_text_y + th(d, b["sub"], f_sub) + mm(6)
    tag_w = tw(d, b["tagline"], f_tagline)
    d.text((fx + (FRONT - tag_w)//2, tag_y), b["tagline"],
           fill=(100,100,100), font=f_tagline)

    # --- 하단: 출판사 ---
    bot_y = H - mm(25)
    ptxt = "OPENSKILL BOOKS"
    pw_ = tw(d, ptxt, f_pub)
    d.text((fx + (FRONT - pw_)//2, bot_y), ptxt,
           fill=(160,160,160), font=f_pub)

    # 시리즈 (우하단)
    stxt2 = "특이점이 온 개발자 시리즈"
    sw2 = tw(d, stxt2, f_series_s)
    d.text((fx + FRONT - sw2 - mm(4), H - BLEED - mm(5)),
           stxt2, fill=(190,190,190), font=f_series_s)

    # ════════════════════════════════════════════════════
    #  뒷표지 (화이트)
    # ════════════════════════════════════════════════════
    BLM = bx + mm(10)

    # 시리즈 라벨
    d.text((BLM, mm(12)), "특이점이 온 개발자 시리즈",
           fill=(160,160,160), font=F(7, bold=True))
    d.line([(BLM, mm(21)), (bx + BACK - mm(10), mm(21))],
           fill=(230,230,230), width=1)

    # 설명 텍스트 (하단)
    desc_y = int(H * 0.55)
    for line in b["desc"]:
        if line == "":
            desc_y += mm(5); continue
        d.text((BLM, desc_y), line, fill=(60,60,60), font=f_bk_desc)
        desc_y += th(d, line, f_bk_desc) + mm(3)

    desc_y += mm(6)
    d.line([(BLM, desc_y), (bx + BACK - mm(10), desc_y)],
           fill=(230,230,230), width=1)
    desc_y += mm(5)

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
                outline=(210,210,210), width=2)
    it = "ISBN 000-00-0000-000-0"
    d.text((bc_x+(bc_w-tw(d,it,f_isbn))//2, bc_y+mm(4)),
           it, fill=(170,170,170), font=f_isbn)
    pt = "(ISBN 발급 후 교체)"
    d.text((bc_x+(bc_w-tw(d,pt,f_isbn_sm))//2, bc_y+bc_h-mm(5)),
           pt, fill=(190,190,190), font=f_isbn_sm)
    d.text((bc_x, bc_y-mm(8)), "정가 15,000원", fill=(60,60,60), font=f_price)

    d.text((BLM, H - BLEED - mm(5)), "books.openskill.kr",
           fill=(190,190,190), font=f_bk_url)

    # ════════════════════════════════════════════════════
    #  앞날개 (화이트)
    # ════════════════════════════════════════════════════
    ffx = X_FFLAP
    FLM = ffx + mm(5)
    d.rectangle([(ffx, 0), (ffx+FLAP+BLEED, H)], fill=(252,252,252))
    fy = mm(14)
    d.text((FLM, fy), "저자 소개", fill=(60,60,60), font=f_fl_title)
    fy += th(d, "저자 소개", f_fl_title) + mm(3)
    d.line([(FLM, fy), (ffx+FLAP-mm(5), fy)], fill=(210,210,210), width=2)
    fy += mm(4)
    for line in AUTHOR_BIO:
        if line == "":
            fy += mm(3); continue
        d.text((FLM, fy), line, fill=(70,70,70), font=f_fl_body)
        fy += th(d, line, f_fl_body) + mm(2.5)
    d.text((FLM, H-BLEED-mm(6)), "openskill.kr", fill=(170,170,170), font=f_fl_sm)

    # ════════════════════════════════════════════════════
    #  뒷날개 (화이트)
    # ════════════════════════════════════════════════════
    bfx = X_BFLAP
    BFLM = bfx + mm(5)
    d.rectangle([(0, 0), (bfx+FLAP, H)], fill=(252,252,252))
    by = mm(14)
    d.text((BFLM, by), "시리즈 안내", fill=(60,60,60), font=f_fl_title)
    by += th(d, "시리즈 안내", f_fl_title) + mm(3)
    d.line([(BFLM, by), (bfx+FLAP-mm(5), by)], fill=(210,210,210), width=2)
    by += mm(4)
    d.text((BFLM, by), "특이점이 온 개발자", fill=(40,40,40), font=f_fl_title)
    by += th(d, "특이점이 온 개발자", f_fl_title) + mm(3)
    for t in ["AI 시대, 개발자의 새로운 출발점.",
              "같은 시리즈의 다른 책들도", "만나보세요."]:
        d.text((BFLM, by), t, fill=(110,110,110), font=f_fl_sm)
        by += th(d, t, f_fl_sm) + mm(2)
    by += mm(4)
    for other in SERIES_OTHER[b["id"]]:
        d.text((BFLM, by), f"  {other}", fill=(70,70,70), font=f_fl_body)
        by += th(d, other, f_fl_body) + mm(3)
    d.text((BFLM, H-BLEED-mm(6)), "books.openskill.kr",
           fill=(170,170,170), font=f_fl_sm)

    # ════════════════════════════════════════════════════
    #  책등 (화이트)
    # ════════════════════════════════════════════════════
    st = f"특이점이 온 개발자 — {b['title']} {b['sub']}"
    tmp = Image.new("RGBA", (H, SPINE), (0,0,0,0))
    td = ImageDraw.Draw(tmp)
    stw_ = tw(td, st, f_spine)
    td.text(((H-stw_)//2, (SPINE-th(td,st,f_spine))//2),
            st, fill=(100,100,100), font=f_spine)
    aw = tw(td, "류재성", f_spine_sm)
    td.text((H-aw-mm(2), (SPINE-th(td,"류재성",f_spine_sm))//2),
            "류재성", fill=(150,150,150), font=f_spine_sm)
    img.paste(tmp.rotate(90, expand=True), (X_SPINE, 0),
              tmp.rotate(90, expand=True))

    # ════════════════════════════════════════════════════
    #  재단 가이드
    # ════════════════════════════════════════════════════
    gc = (215,215,215)
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
    p = os.path.join(OUT, f"spread-v4.3-{b['id']}.png")
    img.save(p, dpi=(DPI,DPI))
    print(f"OK {p} ({img.size[0]}x{img.size[1]})")

print(f"\nv4.3 점프투 스타일 타이포그래피 — {len(BOOKS)}권 완료")
