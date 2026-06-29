#!/usr/bin/env python3
"""
build_book_pdf.py — HTML 다이어그램이 많은 책(MSA·도커쿠버네티스 등)의
머릿말+프롤로그+챕터 최신본+에필로그+맺음말을 PDF로 변환하고, 각 번호 챕터 앞에
구분 표지 페이지를 끼워 표지·판권지·목차·페이지번호·계층 북마크까지 한 권으로 병합한다.

책별 하드코딩 없음. 프로젝트 경로만 받고, 챕터 순서는 책별 설정 파일에서 읽는다.

  PYTHONUTF8=1 python .claude/skills/pub-html-to-pdf/build_book_pdf.py \
      --project-root projects/<책폴더>

전제(반드시 먼저): chapters/front/back 마크다운을 build_html.py로 HTML 빌드해 둘 것.
  이 스크립트(render_pdf)는 기존 .build/*.html을 PDF로 굽기만 하고 마크다운을 재생성하지 않는다.

설정 파일: projects/<책>/book/pdf-build.json
  {
    "chapters": ["preface","prologue","01-...-v5", ..., "epilogue","afterword"],
    "output": "(선택) 출력 PDF 파일명. 기본값 = 책 폴더명 + .pdf",
    "top_labels": { "(선택) 파일명": "목차 라벨" }
  }
  - chapters는 글롭이 아니라 명시 리스트(버전 핀 유지).
  - 물리 순서 관례: 맨 앞 2개 = 머릿말·프롤로그, 그다음 목차, 이후 챕터들, 끝에 에필로그·맺음말.

데이터 파일(있으면 사용): book/dividers.json(챕터표지), book/colophon.json(판권지), assets/cover.jpg(표지)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_pdf import render_pdf  # noqa: E402

# front/back 파일명 → 목차 라벨. 책마다 파일명이 달라(preface vs 머릿말) 둘 다 흡수.
DEFAULT_TOP_LABELS = {
    "preface": "머릿말",
    "머릿말": "머릿말",
    "prologue": "프롤로그",
    "epilogue": "에필로그",
    "afterword": "맺음말",
    "마치며": "맺음말",
}


def _divider_html(data: dict) -> str:
    sub_html = f'<div class="sub">{data["sub"]}</div>' if data.get("sub") else ""
    goal_items = "".join(f"<li>{g}</li>" for g in data.get("goal", []))
    goal_html = ""
    if goal_items:
        goal_html = (
            '<div class="goal"><div class="gh">이번 챕터가 끝나면</div>'
            f"<ul>{goal_items}</ul></div>"
        )
    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<link rel="stylesheet" href="./styles/fonts.css">
<link rel="stylesheet" href="./styles/tokens.css">
<link rel="stylesheet" href="./tokens.css">
<style>
* {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
html,body {{ margin:0; font-family:var(--font-body,"Pretendard",sans-serif); }}
.s1 {{ min-height:235mm; display:flex; flex-direction:column;
  align-items:center; justify-content:center; text-align:center;
  padding:0 16mm; box-sizing:border-box; }}
.s1 .label {{ letter-spacing:.34em; font-size:15px; font-weight:700;
  color:var(--color-accent,#4f46e5); margin-bottom:6px; }}
.s1 .num {{ font-size:140px; font-weight:800; line-height:1;
  color:var(--color-accent,#4f46e5); }}
.s1 .rule {{ width:68px; height:3px; border-radius:2px;
  background:var(--color-accent-warm,#ff7849); margin:28px 0 32px; }}
.s1 .title {{ font-size:36px; font-weight:800;
  color:var(--color-text-heading,#0f172a); }}
.s1 .sub {{ font-size:19px; font-weight:500;
  color:var(--color-text-muted,#64748b); margin-top:14px; }}
.goal {{ margin-top:54px; width:min(30em,86%); text-align:left; box-sizing:border-box;
  border:1px solid var(--color-accent-border,#c7d2fe); border-radius:14px; padding:22px 26px; }}
.goal .gh {{ font-size:14px; font-weight:700; letter-spacing:.04em;
  color:var(--color-accent-text,#3730a3); margin-bottom:12px; text-align:center; }}
.goal ul {{ margin:0; padding:0; list-style:none; }}
.goal li {{ position:relative; padding-left:20px; margin:9px 0;
  font-size:15px; line-height:1.7; color:#374151; }}
.goal li::before {{ content:""; position:absolute; left:2px; top:11px;
  width:7px; height:7px; border-radius:50%; background:var(--color-accent,#4f46e5); }}
.goal b {{ color:var(--color-text-heading,#0f172a); font-weight:700; }}
</style></head><body>
<div class="s1">
  <div class="label">CHAPTER</div>
  <div class="num">{data["n"]}</div>
  <div class="rule"></div>
  <div class="title">{data["title"]}</div>
  {sub_html}
  {goal_html}
</div>
</body></html>
"""


def _load_dividers(dividers_json: Path) -> dict:
    if not dividers_json.exists():
        return {}
    raw = json.loads(dividers_json.read_text(encoding="utf-8"))
    return {c["n"]: c for c in raw["chapters"]}


def _cover_pdf(project: Path, pdf_dir: Path) -> "Path | None":
    """assets/cover.jpg를 A4 한 페이지 PDF로 만들어 맨 앞에 붙인다.
    cover.jpg가 없으면 표지 없이 진행."""
    cover = project / "assets" / "cover.jpg"
    if not cover.exists():
        print("[!] 표지 없음(assets/cover.jpg) → 표지 페이지 생략")
        return None
    import fitz
    out = pdf_dir / "_cover.pdf"
    doc = fitz.open()
    page = doc.new_page(width=595.276, height=841.890)  # A4
    page.insert_image(page.rect, filename=str(cover), keep_proportion=True)
    doc.save(str(out))
    doc.close()
    print(f"[>] 표지 페이지 생성: {cover.name}")
    return out


def _colophon_pdf(project: Path, build_dir: Path, pdf_dir: Path) -> "Path | None":
    """book/colophon.json으로 판권지(출판정보) 한 페이지 PDF를 만든다.
    표지 다음·머릿말 앞에 들어간다. 파일 없으면 생략."""
    cj = project / "book" / "colophon.json"
    if not cj.exists():
        return None
    d = json.loads(cj.read_text(encoding="utf-8"))
    rows = "".join(
        f'<tr><td class="k">{k}</td><td class="v">{v}</td></tr>'
        for k, v in [
            (d.get("edition", "초판 1쇄 발행"), d.get("pubdate", "")),
            ("지은이", d.get("authors", "")),
            ("펴낸이", d.get("founder", "")),
            ("펴낸곳", d.get("publisher", "")),
            ("등록", d.get("registration", "")),
            ("주소", d.get("address", "")),
            ("전화", d.get("phone", "")),
            ("이메일", d.get("email", "")),
            ("ISBN", d.get("isbn", "")),
            ("정가", d.get("price", "")),
        ]
        if v)
    notices = "".join(f"<p>{n}</p>" for n in d.get("notices", []))
    css = (
        "* { -webkit-print-color-adjust: exact !important;"
        " print-color-adjust: exact !important; }"
        "html,body { margin:0; font-family:var(--font-body,'Pretendard',sans-serif);"
        " color:#1a202c; }"
        ".wrap { min-height:235mm; display:flex; flex-direction:column;"
        " justify-content:flex-end; padding:24mm 24mm 28mm; box-sizing:border-box; }"
        ".ctitle { font-size:20px; font-weight:800; margin-bottom:12px; }"
        ".rule { height:2px; width:58px; background:var(--color-accent,#4f46e5);"
        " margin-bottom:20px; }"
        ".meta { border-collapse:collapse; font-size:13.5px; margin-bottom:18px; }"
        ".meta td { padding:4px 0; vertical-align:top; }"
        ".meta .k { color:#64748b; width:120px; font-weight:600; }"
        ".meta .v { color:#1a202c; }"
        ".copy { font-size:13px; color:#334155; font-weight:600; margin-bottom:22px; }"
        ".notice { font-size:11px; color:#94a3b8; line-height:1.7;"
        " border-top:1px solid #e2e8f0; padding-top:14px; }"
        ".notice p { margin:3px 0; }")
    html = (
        '<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">'
        '<link rel="stylesheet" href="./styles/fonts.css">'
        '<link rel="stylesheet" href="./styles/tokens.css">'
        '<link rel="stylesheet" href="./tokens.css">'
        f"<style>{css}</style></head><body><div class=\"wrap\">"
        f'<div class="ctitle">{d.get("title", "")}</div>'
        '<div class="rule"></div>'
        f'<table class="meta">{rows}</table>'
        f'<div class="copy">© {d.get("year", "")} {d.get("authors", "")}</div>'
        f'<div class="notice">{notices}</div>'
        "</div></body></html>")
    cp_html = build_dir / "_colophon.html"
    cp_html.write_text(html, encoding="utf-8")
    cp_pdf = pdf_dir / "_colophon.pdf"
    print("[>] 판권지 → PDF")
    render_pdf(cp_html, cp_pdf, pagedjs=False)
    return cp_pdf


def _chapter_headings(html_path) -> list:
    """챕터 HTML에서 번호 매겨진 절(h2: N.M)·소절(h3: N.M.K)을 문서 순서로 추출."""
    txt = Path(html_path).read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"<(h2|h3)\b[^>]*>(.*?)</\1>", txt, re.S):
        lvl = 2 if m.group(1) == "h2" else 3
        inner = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if re.match(r"^\d+\.\d+", inner):  # N.M / N.M.K 형태만 (prep의 "1. " 제외)
            out.append((lvl, inner))
    return out


def _find_heading_offsets(chapter_pdf, headings) -> list:
    """각 heading이 챕터 PDF의 몇 번째 페이지(0-based)에 있는지 본문 텍스트로 찾는다."""
    import fitz
    doc = fitz.open(str(chapter_pdf))
    pages = [doc[i].get_text().replace(" ", "").replace("\n", "")
             for i in range(doc.page_count)]
    doc.close()
    res, start = [], 0
    for lvl, text in headings:
        key = text.replace(" ", "")[:18]
        off = 0
        for p in range(start, len(pages)):
            if key and key in pages[p]:
                off, start = p, p
                break
        res.append((lvl, text, off))
    return res


def _toc_html(entries) -> str:
    """entries: (level, label, page). 계층 목차 HTML."""
    rows = "".join(
        f'<div class="trow l{lvl}"><span class="tl">{lbl}</span>'
        f'<span class="td"></span><span class="tp">{pg}</span></div>'
        for lvl, lbl, pg in entries)
    css = (
        "* { -webkit-print-color-adjust: exact !important;"
        " print-color-adjust: exact !important; }"
        "html,body { margin:0; font-family:var(--font-body,'Pretendard',sans-serif);"
        " color:#1a202c; }"
        ".wrap { padding: 2mm 22mm 24mm; }"
        ".tt { font-size:30px; font-weight:800; margin:0 0 26px; letter-spacing:-0.5px; }"
        ".trow { display:flex; align-items:baseline; }"
        ".tl { white-space:nowrap; }"
        ".td { flex:1; border-bottom:1px dotted #c8ccd4; margin:0 8px; }"
        ".tp { white-space:nowrap; }"
        ".l1 { margin:16px 0 6px; font-size:15px; }"
        ".l1 .tl { font-weight:700; } .l1 .tp { color:var(--color-accent,#4f46e5);"
        " font-weight:700; }"
        ".l2 { margin:5px 0 5px 18px; font-size:13px; }"
        ".l2 .tl { font-weight:600; color:#2d3748; } .l2 .tp { color:#4a5568; }"
        ".l3 { margin:3px 0 3px 38px; font-size:12px; }"
        ".l3 .tl { color:#5a6678; } .l3 .tp { color:#8a93a3; }")
    return (
        '<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">'
        '<link rel="stylesheet" href="./styles/fonts.css">'
        '<link rel="stylesheet" href="./styles/tokens.css">'
        '<link rel="stylesheet" href="./tokens.css">'
        f"<style>{css}</style></head><body><div class=\"wrap\">"
        '<div class="tt">목차</div>'
        f"{rows}</div></body></html>")


def _finalize(src, dst, phys, toc_entries):
    """기존 챕터별 푸터 숫자를 가리고 전체 기준 번호(머릿말=1)를 찍는다.
    표지·목차 페이지는 번호 없음. 계층 PDF 북마크도 추가."""
    import fitz
    doc = fitz.open(str(src))

    flags, toc_phys, pos = [], None, 0
    for pdf, numbered in phys:
        c = fitz.open(str(pdf)).page_count
        if toc_phys is None and "_toc" in str(pdf):
            toc_phys = pos + 1
        flags += [numbered] * c
        pos += c

    body_to_phys, body = {}, 0
    for i, page in enumerate(doc):
        ph, pw = page.rect.height, page.rect.width
        for b in page.get_text("blocks"):
            x0, y0, x1, y1, txt = b[0], b[1], b[2], b[3], b[4]
            if y0 > ph - 58 and txt.strip().isdigit():
                page.draw_rect(fitz.Rect(x0 - 6, y0 - 3, x1 + 6, y1 + 3),
                               color=(1, 1, 1), fill=(1, 1, 1))
        if i < len(flags) and flags[i]:
            body += 1
            body_to_phys[body] = i + 1
            page.insert_textbox(fitz.Rect(pw / 2 - 40, ph - 42, pw / 2 + 40, ph - 22),
                                str(body), fontsize=9, align=1, color=(0.35, 0.35, 0.35))

    # 문서 등장 순서(seq)를 보존해 정렬한다. (page, level)로 정렬하면 소절과
    # 다음 절이 같은 페이지에 걸릴 때 절(h2)이 앞 소절(h3)보다 먼저 와 번호가 뒤집힌다.
    raw, seq = [], 0
    if toc_phys:
        raw.append((1, "목차", toc_phys, seq)); seq += 1
    for lvl, label, bp in toc_entries:
        if bp in body_to_phys:
            raw.append((lvl, label, body_to_phys[bp], seq)); seq += 1
    raw.sort(key=lambda e: (e[2], e[3]))  # (page, 문서 등장 순서)
    outline, prev = [], 0
    for lvl, label, pno, _ in raw:
        lvl = min(lvl, prev + 1)  # 레벨 점프 방지(set_toc 요구)
        outline.append([lvl, label, pno])
        prev = lvl
    doc.set_toc(outline)
    doc.save(str(dst))
    doc.close()


def main() -> int:
    ap = argparse.ArgumentParser(description="HTML 다이어그램 책의 PDF 한 권 병합 빌드")
    ap.add_argument("--project-root", required=True,
                    help="projects/<책폴더> 경로")
    args = ap.parse_args()

    project = Path(args.project_root).resolve()
    if not project.exists():
        print(f"[!] 프로젝트 경로 없음: {project}")
        return 1
    build_dir = project / ".build"
    pdf_dir = build_dir / "pdf"
    dividers_json = project / "book" / "dividers.json"
    cfg_path = project / "book" / "pdf-build.json"
    if not cfg_path.exists():
        print(f"[!] 설정 파일 없음: {cfg_path}")
        print("    book/pdf-build.json 에 {\"chapters\": [...]} 를 만들어 주세요.")
        return 1
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    chapters = cfg.get("chapters", [])
    if not chapters:
        print("[!] pdf-build.json 의 chapters 가 비어 있음")
        return 1
    top_labels = {**DEFAULT_TOP_LABELS, **cfg.get("top_labels", {})}
    out_name = cfg.get("output", f"{project.name}.pdf")

    pdf_dir.mkdir(parents=True, exist_ok=True)
    dividers = _load_dividers(dividers_json)
    import fitz

    cover = _cover_pdf(project, pdf_dir)

    # 1) 모든 파트 렌더 (numbering 순서: 머릿말, 프롤로그, [표지+챕터]*, 에필로그, 맺음말)
    rendered = []
    for name in chapters:
        html = build_dir / f"{name}.html"
        if not html.exists():
            print(f"[!] HTML 없음: {html}")
            continue
        if name[:2].isdigit():
            n = str(int(name[:2]))
            data = dividers.get(n)
            if data:
                d_html = build_dir / f"_divider-ch{n}.html"
                d_pdf = pdf_dir / f"_divider-ch{n}.pdf"
                d_html.write_text(_divider_html(data), encoding="utf-8")
                print(f"[>] 챕터 {n} 표지 → PDF")
                render_pdf(d_html, d_pdf, pagedjs=False)
                rendered.append({"pdf": d_pdf, "lvl": 1,
                                 "label": f"챕터 {n}. {data['title']}", "sub": None})
            pdf = pdf_dir / f"{name}.pdf"
            print(f"[>] {name} → PDF")
            render_pdf(html, pdf, pagedjs=False)
            rendered.append({"pdf": pdf, "lvl": None, "label": None,
                             "sub": _find_heading_offsets(pdf, _chapter_headings(html))})
        else:
            pdf = pdf_dir / f"{name}.pdf"
            print(f"[>] {name} → PDF")
            render_pdf(html, pdf, pagedjs=False)
            rendered.append({"pdf": pdf, "lvl": 1,
                             "label": top_labels.get(name), "sub": None})

    if len(rendered) < 2:
        print("[!] 변환된 PDF 부족")
        return 1

    # 2) 본문 페이지(머릿말=1) 누적 + 목차 엔트리(절·소절 포함)
    toc_entries, body = [], 1
    for r in rendered:
        cnt = fitz.open(str(r["pdf"])).page_count
        if r["label"]:
            toc_entries.append((r["lvl"], r["label"], body))
        if r["sub"]:
            for lvl, text, off in r["sub"]:
                toc_entries.append((lvl, text, body + off))
        body += cnt

    # 3) 목차 렌더
    toc_html_p = build_dir / "_toc.html"
    toc_html_p.write_text(_toc_html(toc_entries), encoding="utf-8")
    toc_pdf = pdf_dir / "_toc.pdf"
    print("[>] 목차 → PDF")
    render_pdf(toc_html_p, toc_pdf, pagedjs=False)

    # 4) 물리 조립: 표지 + 판권지 + 머릿말 + 프롤로그 + 목차 + (챕터 파트들) + 에필로그 + 맺음말
    colophon = _colophon_pdf(project, build_dir, pdf_dir)
    phys = []
    if cover:
        phys.append((cover, False))
    if colophon:
        phys.append((colophon, False))        # 판권지(번호 없음)
    phys.append((rendered[0]["pdf"], True))   # 머릿말
    phys.append((rendered[1]["pdf"], True))   # 프롤로그
    phys.append((toc_pdf, False))             # 목차
    for r in rendered[2:]:
        phys.append((r["pdf"], True))

    from pypdf import PdfWriter
    writer = PdfWriter()
    for pdf, _ in phys:
        writer.append(str(pdf))
    tmp = pdf_dir / "_merged_tmp.pdf"
    with open(tmp, "wb") as f:
        writer.write(f)
    writer.close()

    # 5) 페이지 번호 재부여 + 북마크
    merged = pdf_dir / out_name
    _finalize(tmp, merged, phys, toc_entries)
    tmp.unlink(missing_ok=True)
    print(f"[OK] 병합 완료(표지·판권지·머릿말·프롤로그·목차 + 계층 목차/번호): {merged}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
