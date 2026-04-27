#!/usr/bin/env python3
"""처음 만나는 도커 & 쿠버네티스 — PDF 빌드 스크립트"""

import sys
import shutil
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
BOOK = PROJECT / "book"
CHAPTERS_DIR = PROJECT / "chapters"
SKILL_SCRIPTS = Path(__file__).resolve().parent.parent.parent.parent / ".claude" / "skills" / "pub-build" / "references" / "scripts"

sys.path.insert(0, str(SKILL_SCRIPTS))
import typst_builder


def find_chapter(*candidates):
    """첫 번째로 존재하는 파일 반환"""
    for name in candidates:
        p = CHAPTERS_DIR / name
        if p.exists():
            return p
    print(f"   [경고] 챕터 파일 없음: {candidates}")
    return CHAPTERS_DIR / candidates[0]


CONFIG = {
    "title": "처음 만나는 도커 & 쿠버네티스",
    "base": PROJECT,
    "assets_dir": PROJECT / "images",
    "mermaid_out": BOOK / "_mermaid",
    "template": BOOK / "book.typ",
    "font_path": None,

    "front": [
        BOOK / "front" / "prologue.md",
    ],

    "chapters": [
        find_chapter("ch1-why-container.md"),
        find_chapter("ch2-docker-understanding.md"),
        find_chapter("ch3-docker-working.md"),
        find_chapter("ch4-k8s-v2.md"),
        find_chapter("ch5-k8s-v2.md"),
    ],

    "back": [
        BOOK / "back" / "afterword.md",
        BOOK / "back" / "appendix.md",
    ],

    "output_md":  BOOK / "integrated.md",
    "output_typ": BOOK / "book_final.typ",
    "output_pdf": BOOK / "처음-만나는-도커-쿠버네티스.pdf",

    "layout_checker": str(SKILL_SCRIPTS / "pdf_layout_checker.py"),

    # 이미지 테두리 설정
    "image_border": {
        "enabled": True,
        "color": "#5ba8d9",
        "thickness": 1.2,
        "style": "dashed",
        "padding": 8,
        "exclude_terminal": True,
    },
}


def typst_compile_python(typ_path: Path, pdf_path: Path) -> bool:
    try:
        import typst as typst_mod
        pdf_bytes = typst_mod.compile(str(typ_path), root=str(Path("/")),
                                       font_paths=[r"C:\Windows\Fonts"])
        pdf_path.write_bytes(pdf_bytes)
        print(f"   Typst 컴파일 완료: {pdf_path.name}")
        return True
    except Exception as e:
        print(f"   [오류] Typst 컴파일 실패: {e}")
        return False


def main():
    # --design 인자 파싱 (기본: 6)
    design_arg = "6"
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--design" and i < len(sys.argv):
            design_arg = sys.argv[i + 1]
            break
        if arg.startswith("--design="):
            design_arg = arg.split("=", 1)[1]
            break

    title = CONFIG["title"]
    print(f"{title} 통합 PDF 생성 (Typst) — 디자인 프리셋 {design_arg}")
    print("=" * 50)

    import os
    pandoc_path = shutil.which("pandoc") or shutil.which("pandoc.exe") or r"C:\Users\82105\AppData\Local\Pandoc\pandoc.exe"
    if not Path(pandoc_path).exists():
        print("[오류] pandoc 미설치")
        return
    pandoc_dir = str(Path(pandoc_path).parent)
    if pandoc_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = pandoc_dir + os.pathsep + os.environ.get("PATH", "")

    typst_builder._mermaid_counter = 0
    mermaid_out = CONFIG["mermaid_out"]
    if mermaid_out.exists():
        shutil.rmtree(mermaid_out)

    print("\n[1/6] 마크다운 통합 + 전처리...")
    integrated_md = typst_builder.build_integrated_md(
        CONFIG["front"], CONFIG["chapters"], CONFIG["back"], mermaid_out
    )
    output_md = CONFIG["output_md"]
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(integrated_md, encoding="utf-8")
    print(f"\n   통합 마크다운: {output_md.name}")

    print("\n[2/6] 이미지 공백 자동 제거...")
    typst_builder.autocrop_all_assets(CONFIG["assets_dir"], mermaid_out)

    print("\n[3/6] Pandoc 변환 (MD → Typst)...")
    output_typ = CONFIG["output_typ"]
    temp_typ = output_typ.with_suffix(".raw.typ")
    if not typst_builder.md_to_typst(output_md, temp_typ):
        return

    print("\n[4/6] 후처리 + 템플릿 병합...")
    raw_content = temp_typ.read_text(encoding="utf-8")
    image_border_preset = CONFIG.get("image_border_preset", "plain")
    fixed_content = typst_builder.fix_typst_content(
        raw_content, image_border_preset=image_border_preset
    )

    final_typ = typst_builder.merge_template_and_content(
        CONFIG["template"], fixed_content, design=design_arg
    )
    output_typ.write_text(final_typ, encoding="utf-8")
    temp_typ.unlink(missing_ok=True)
    print(f"   최종 Typst: {output_typ.name}")

    print("\n[5/6] Typst 컴파일 (TYP → PDF)...")
    output_pdf = CONFIG["output_pdf"]
    if not typst_compile_python(output_typ, output_pdf):
        return

    size_mb = output_pdf.stat().st_size / (1024 * 1024)
    print(f"\n   PDF 생성 완료: {output_pdf.name} ({size_mb:.1f} MB)")

    print("\n[6/6] 레이아웃 분석...")
    try:
        import importlib.util
        checker_path = CONFIG.get("layout_checker")
        if checker_path and Path(checker_path).exists():
            spec = importlib.util.spec_from_file_location("pdf_layout_checker", checker_path)
            checker = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(checker)
            checker.print_page_usage(str(output_pdf))
            issues = checker.analyze_layout(str(output_pdf))
            checker.print_report(issues, str(output_pdf))
        else:
            print("   [참고] pdf_layout_checker 없음 → 건너뜀")
    except Exception as e:
        print(f"   [경고] 레이아웃 분석 오류: {e}")

    print(f"\n{'=' * 50}")
    print(f"완료: {output_pdf}")


if __name__ == "__main__":
    main()
