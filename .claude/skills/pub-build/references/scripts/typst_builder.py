#!/usr/bin/env python3
"""범용 마크다운 → Typst → PDF 변환 엔진
   프로젝트별 설정(챕터 목록, 경로 등)은 호출 측에서 config로 전달.
   의존성: typst, pandoc, npx @mermaid-js/mermaid-cli, Pillow, PyMuPDF
"""

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

# Mermaid 다이어그램 전역 카운터
_mermaid_counter = 0

# Mermaid 커스텀 설정 파일 경로
_MERMAID_CONFIG = Path(__file__).parent / "mermaid-config.json"


# ══════════════════════════════════════
# 이미지 공백 자동 제거
# ══════════════════════════════════════

def autocrop_image(img_path: Path, padding: int = 6) -> bool:
    """이미지 파일의 위아래/좌우 공백을 자동으로 잘라냄"""
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return False

    try:
        img = Image.open(img_path).convert("RGB")
        bg = Image.new("RGB", img.size, (255, 255, 255))
        diff = ImageChops.difference(img, bg)
        bbox = diff.getbbox()
        if bbox:
            bbox = (
                max(0, bbox[0] - padding),
                max(0, bbox[1] - padding),
                min(img.width, bbox[2] + padding),
                min(img.height, bbox[3] + padding),
            )
            trimmed = (bbox[1]) + (img.height - bbox[3])
            if trimmed > 20:
                cropped = img.crop(bbox)
                cropped.save(img_path)
                return True
    except Exception:
        pass
    return False


def autocrop_all_assets(assets_dir: Path, mermaid_out: Path):
    """assets + mermaid 디렉토리의 모든 PNG 이미지 공백 제거"""
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("   [경고] Pillow 미설치 → 이미지 공백 자르기 건너뜀 (pip install Pillow)")
        return

    count = 0
    for png in assets_dir.rglob("*.png"):
        if autocrop_image(png):
            count += 1
    if mermaid_out.exists():
        for png in mermaid_out.rglob("*.png"):
            if autocrop_image(png):
                count += 1
    if count:
        print(f"   이미지 공백 제거: {count}개 파일")


# ══════════════════════════════════════
# 전처리 함수
# ══════════════════════════════════════

def _postprocess_mermaid_svg(svg_path: Path) -> None:
    """SVG 후처리: 둥근 모서리, 그림자, 모던 B&W 스타일 적용"""
    svg_text = svg_path.read_text(encoding='utf-8')

    # 1. defs에 드롭 쉐도우 필터 추가
    shadow_filter = '''<defs>
    <filter id="drop-shadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="#00000020"/>
    </filter>
  </defs>'''
    if '<defs>' in svg_text:
        svg_text = svg_text.replace('<defs>', shadow_filter.replace('</defs>', ''), 1)
    elif '<svg' in svg_text:
        svg_text = svg_text.replace('</svg>', f'  {shadow_filter}\n</svg>', 1)

    # 2. 노드(rect)에 둥근 모서리 + 그림자 적용
    svg_text = re.sub(
        r'(<rect[^>]*class="[^"]*(?:basic|node)[^"]*"[^>]*)(/?>)',
        lambda m: m.group(1) + ' rx="10" ry="10" filter="url(#drop-shadow)"' + m.group(2)
        if 'rx=' not in m.group(1) else m.group(0),
        svg_text
    )

    # 3. label-container에도 둥근 모서리 적용
    svg_text = re.sub(
        r'(<rect[^>]*class="[^"]*label-container[^"]*"[^>]*)(/?>)',
        lambda m: m.group(1) + ' rx="10" ry="10"' + m.group(2)
        if 'rx=' not in m.group(1) else m.group(0),
        svg_text
    )

    # 4. cluster(subgraph) rect에 둥근 모서리 적용
    svg_text = re.sub(
        r'(<rect[^>]*class="[^"]*cluster[^"]*"[^>]*)(/?>)',
        lambda m: m.group(1) + ' rx="12" ry="12"' + m.group(2)
        if 'rx=' not in m.group(1) else m.group(0),
        svg_text
    )

    svg_path.write_text(svg_text, encoding='utf-8')


def render_mermaid_diagrams(text: str, mermaid_out: Path) -> str:
    """mermaid 코드 블록을 SVG→후처리→PNG로 렌더링하여 교체"""
    global _mermaid_counter
    mermaid_out.mkdir(parents=True, exist_ok=True)

    def replace_mermaid(m):
        global _mermaid_counter
        code = m.group(1).strip()
        _mermaid_counter += 1
        img_name = f"mermaid_{_mermaid_counter:03d}.png"
        img_path = mermaid_out / img_name
        svg_path = mermaid_out / f"mermaid_{_mermaid_counter:03d}.svg"

        if img_path.exists():
            abs_path = img_path.resolve()
            return f'\n![다이어그램]({_typst_root_path(abs_path)})\n'

        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            # Step 1: SVG로 렌더링
            mmdc_cmd = [
                'npx', '-y', '@mermaid-js/mermaid-cli',
                '-i', tmp_path, '-o', str(svg_path),
                '-b', 'white', '-q',
            ]
            if _MERMAID_CONFIG.exists():
                mmdc_cmd.extend(['-c', str(_MERMAID_CONFIG)])
            else:
                mmdc_cmd.extend(['-t', 'neutral'])
            result = subprocess.run(
                mmdc_cmd,
                capture_output=True, text=True, timeout=60
            )

            if result.returncode == 0 and svg_path.exists():
                # Step 2: SVG 후처리 (둥근 모서리, 그림자)
                _postprocess_mermaid_svg(svg_path)

                # Step 3: SVG → PNG 변환 (고해상도)
                png_cmd = [
                    'npx', '-y', '@mermaid-js/mermaid-cli',
                    '-i', tmp_path, '-o', str(img_path),
                    '-b', 'white',
                    '-w', '800', '-s', '2', '-q',
                ]
                if _MERMAID_CONFIG.exists():
                    png_cmd.extend(['-c', str(_MERMAID_CONFIG)])
                else:
                    png_cmd.extend(['-t', 'neutral'])
                png_result = subprocess.run(
                    png_cmd,
                    capture_output=True, text=True, timeout=60
                )

                if png_result.returncode == 0 and img_path.exists():
                    abs_path = img_path.resolve()
                    print(f"   Mermaid 렌더링: {img_name}")
                    return f'\n![다이어그램]({abs_path})\n'

            # 실패 시 텍스트 대체
            labels = re.findall(r'\["([^"]+)"\]', code)
            if labels:
                flow = " → ".join(labels[:6])
                return f'\n*[다이어그램: {flow}]*\n'
            return '\n*[다이어그램]*\n'
        except (subprocess.TimeoutExpired, FileNotFoundError):
            labels = re.findall(r'\["([^"]+)"\]', code)
            if labels:
                flow = " → ".join(labels[:6])
                return f'\n*[다이어그램: {flow}]*\n'
            return '\n*[다이어그램]*\n'
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    return re.sub(r'```mermaid\s*\n(.*?)```', replace_mermaid, text, flags=re.DOTALL)


def _typst_root_path(p: Path) -> str:
    """절대경로를 Typst --root(/) 기준 경로 문자열로 변환.
    forward slash 통일 + 드라이브 문자 제거(Windows). 예: C:\\a\\b → /a/b, /a/b → /a/b."""
    posix = p.as_posix()
    if p.drive:                       # 'C:' 등 → 제거하여 root-상대 경로로
        posix = posix[len(p.drive):]
    return posix


def fix_image_paths(text: str, source_file: Path) -> str:
    """마크다운 이미지 상대경로 → 절대경로로 변환 (file:// 없이)"""
    source_dir = source_file.parent

    # HTML <img src="..."> → 마크다운 ![](src) 정규화.
    # image-gen 스킬이 플레이스홀더를 <img> 태그로 교체하므로, 이를 마크다운
    # 이미지 흐름(→ Pandoc → #auto-image)에 합류시킨다. alt는 비운다
    # (캡션은 뒤따르는 *그림 N-N* 줄이 담당 → 중복 캡션 방지).
    def html_img_to_md(m):
        tag = m.group(0)
        src_m = re.search(r'src\s*=\s*["\']([^"\']+)["\']', tag)
        if not src_m:
            return tag
        return f'![]({src_m.group(1)})'

    text = re.sub(r'<img\b[^>]*>', html_img_to_md, text, flags=re.IGNORECASE)

    def replace_img(m):
        alt = m.group(1)
        rel_path = m.group(2)
        if rel_path.startswith('file://'):
            return f'![{alt}]({rel_path[7:]})'
        abs_path = (source_dir / rel_path).resolve()
        if abs_path.exists():
            # Typst 경로는 --root(/) 기준 가상경로. forward slash + 드라이브 문자 제거로
            # Windows(C:/Users/...)와 macOS(/Users/...) 모두 root-상대(/Users/...)로 통일.
            return f'![{alt}]({_typst_root_path(abs_path)})'
        else:
            return f'*[이미지: {alt}]*'

    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, text)


def clean_comments(text: str) -> str:
    """HTML 주석 제거 (GEMINI PROMPT, CAPTURE NEEDED, 기타)"""
    text = re.sub(r'<!--\s*\[GEMINI PROMPT.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--\s*\[CAPTURE NEEDED.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text


def fix_br_tags(text: str) -> str:
    """코드 블록 밖의 <br> → 마크다운 줄바꿈으로 변환.
    코드 블록(```)과 mermaid 내의 <br>는 보존."""
    parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
    for i, part in enumerate(parts):
        if not part.startswith('```'):
            parts[i] = re.sub(r'<br\s*/?>', '  ', part)
    return ''.join(parts)


# ══════════════════════════════════════
# 통합
# ══════════════════════════════════════

def build_integrated_md(front: list, chapters: list, back: list,
                        mermaid_out: Path) -> str:
    """모든 파일을 하나의 마크다운으로 통합"""
    parts = []
    all_files = [("front", front), ("chapters", chapters), ("back", back)]

    for section_name, files in all_files:
        for f in files:
            if not f.exists():
                print(f"   [경고] 파일 없음: {f}")
                continue

            print(f"   처리 중: {f.name}")
            content = f.read_text(encoding="utf-8")
            content = clean_comments(content)
            content = fix_image_paths(content, f)
            content = render_mermaid_diagrams(content, mermaid_out)
            content = fix_br_tags(content)
            parts.append(content)
            parts.append("\n\n---\n\n")

    return "\n".join(parts)


# ══════════════════════════════════════
# Pandoc 변환
# ══════════════════════════════════════

def md_to_typst(md_path: Path, typ_path: Path) -> bool:
    """Pandoc으로 마크다운 → Typst 변환"""
    cmd = [
        'pandoc',
        str(md_path),
        '-f', 'markdown+pipe_tables+fenced_code_blocks+backtick_code_blocks-citations',
        '-t', 'typst',
        '-o', str(typ_path),
        '--wrap=none',
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"   [오류] Pandoc 변환 실패: {result.stderr}")
        return False

    print(f"   Pandoc 변환 완료: {typ_path.name}")
    return True


# ══════════════════════════════════════
# Typst 후처리
# ══════════════════════════════════════

def _get_image_aspect_ratio(path: str) -> float | None:
    """이미지의 종횡비(width/height)를 반환. 실패 시 None."""
    try:
        from PIL import Image
        img = Image.open(path)
        w, h = img.size
        return w / h if h > 0 else None
    except Exception:
        return None


def _detect_image_max_width(path: str) -> str:
    """이미지 경로 패턴으로 유형별 최대 너비(비율) 결정.
    Mermaid 이미지는 종횡비를 감지하여 자동 조절:
      - 가로형(AR>2.0): 0.75 (넓게)
      - 중간(1.0~2.0):  0.55
      - 세로형(AR<1.0): 0.45 (좁게)
    실제 크기는 Typst auto-image 함수가 페이지 공간에 맞게 자동 조절."""
    if 'chapter-opening' in path:
        return '0.7'     # 최대 70%
    elif 'mermaid_' in path:
        ar = _get_image_aspect_ratio(path)
        if ar is not None:
            if ar > 2.0:
                return '0.75'   # 가로로 넓은 다이어그램
            elif ar > 1.0:
                return '0.55'   # 정사각형~약간 가로
            else:
                return '0.45'   # 세로로 긴 다이어그램
        return '0.55'    # fallback
    elif any(x in path for x in ['step1', 'step2', 'step3', 'step4']):
        return '0.65'    # 최대 65%
    else:
        # 극단적으로 세로가 긴 이미지(AR < 0.55)는 축소
        ar = _get_image_aspect_ratio(path)
        if ar is not None and ar < 0.55:
            return '0.38'    # 세로가 매우 긴 브라우저 캡처 등
        return '0.6'     # 최대 60% (auto-image가 페이지에 맞춰 자동 축소)


def fix_math_typst(text: str) -> str:
    """Pandoc Typst 출력에서 LaTeX 잔여 매크로를 Typst math로 보정."""
    import re
    # \begin{aligned}...\end{aligned} → 줄바꿈 + & 정렬 제거(단순화)
    def _strip_aligned(m):
        body = m.group(1)
        body = body.replace('\\\\', '\\ ').replace('&', '')
        return body
    text = re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', _strip_aligned, text, flags=re.S)
    # \xrightarrow{f} → arrow.r (라벨 손실 허용)
    text = re.sub(r'\\xrightarrow\{[^}]*\}', ' arrow.r ', text)
    return text


def fix_typst_content(text: str) -> str:
    """Pandoc 출력의 Typst 코드를 후처리"""
    text = fix_math_typst(text)

    # 1. 이미지 수정: !#link("path")[alt] → #auto-image (페이지 공간 자동 조절)
    def fix_image(m):
        path = m.group(1)
        alt = m.group(2).strip()
        max_w = _detect_image_max_width(path)
        if alt:
            return f'#auto-image("{path}", alt: [{alt}], max-width: {max_w})'
        else:
            return f'#auto-image("{path}", max-width: {max_w})'

    text = re.sub(r'!#link\("([^"]+)"\)\[([^\]]*)\]', fix_image, text)

    # 2. 이미지 수정: #box(image("path")) → #auto-image
    def fix_box_image(m):
        path = m.group(1)
        max_w = _detect_image_max_width(path)
        return f'#auto-image("{path}", max-width: {max_w})'

    text = re.sub(r'#box\(image\("([^"]+)"\)\)', fix_box_image, text)

    # 3. 이미지 수정: #figure(image("path"), caption: [...]) → #auto-image
    def fix_figure_image(m):
        path = m.group(1)
        alt = ' '.join(m.group(2).split()) if m.group(2) else ""
        max_w = _detect_image_max_width(path)
        if alt:
            return f'#auto-image("{path}", alt: [{alt}], max-width: {max_w})'
        else:
            return f'#auto-image("{path}", max-width: {max_w})'

    text = re.sub(
        r'#figure\(image\("([^"]+)"\)\s*,\s*caption:\s*\[([^\]]*)\]\s*\)',
        fix_figure_image, text
    )

    # 3.5 이미지 바로 뒤의 #emph[그림 N-M: ...] 캡션을 auto-image의 alt 파라미터로 병합
    #     이미지와 캡션이 같은 페이지에 있도록 보장 (캡션만 다음 페이지로 넘어가는 고아 방지)
    def _merge_caption_into_auto_image(m):
        img_call = m.group(1)  # #auto-image("path", max-width: 0.6)
        caption = m.group(2)    # 그림 2-4: 설명 텍스트
        # alt: 파라미터가 이미 있으면 건드리지 않음
        if 'alt:' in img_call:
            return m.group(0)
        # max-width: 앞에 alt: 삽입
        return img_call.replace('max-width:', f'alt: [{caption}], max-width:')

    text = re.sub(
        r'(#auto-image\([^)]*\))\s*\n?#emph\[((?:[^\]\\]|\\.)*)\]',
        _merge_caption_into_auto_image,
        text
    )

    # 4. 한국어 라벨 제거 (Pandoc이 생성하는 <한국어-라벨>)
    text = re.sub(r'<[가-힣a-zA-Z0-9.\-_]+>\n', '\n', text)

    # 5. 수평선 바로 뒤에 heading(= 또는 ==)이 오면 수평선 제거 (pagebreak 중복 방지)
    text = re.sub(r'#horizontalrule\n+(?==)', '', text)

    # 6. 남은 수평선을 Typst 방식으로
    text = text.replace('#horizontalrule', '#v(4pt)\n#block(width: 100%, height: 0.5pt, fill: rgb("#e5e7eb"))\n#v(4pt)')

    # 7. 표 열 균등화: Pandoc이 생성한 퍼센트 기반 열(38.71%, 32.26%, ...)을 1fr로 변환
    #    짧은 열이 과도하게 넓고 긴 텍스트 열이 좁아지는 문제 해결
    def _equalize_table_columns(m):
        pct_list = m.group(1)
        col_count = len(re.findall(r'[\d.]+%', pct_list))
        if col_count > 0:
            return f'columns: ({", ".join(["1fr"] * col_count)})'
        return m.group(0)

    text = re.sub(r'columns:\s*\(([\d.%,\s]+)\)', _equalize_table_columns, text)

    return text


def merge_template_and_content(template_path: Path, content: str) -> str:
    """템플릿 + Pandoc 변환 내용을 하나의 .typ 파일로 합침

    template_path가 가리키는 디렉토리에 book_base.typ이 있으면
    프로젝트 설정(book.typ) + 범용 스타일(book_base.typ) + 본문 순서로 합침.
    없으면 기존처럼 단일 템플릿 + 본문.
    """
    template = template_path.read_text(encoding="utf-8")
    base_path = template_path.parent / "book_base.typ"
    if base_path.exists():
        base = base_path.read_text(encoding="utf-8")
        return template + "\n" + base + "\n" + content
    return template + "\n" + content


# ══════════════════════════════════════
# Typst 컴파일
# ══════════════════════════════════════

def typst_compile(typ_path: Path, pdf_path: Path,
                  font_path: Path | None = None) -> bool:
    """Typst로 PDF 컴파일"""
    cmd = [
        'typst', 'compile',
        str(typ_path),
        str(pdf_path),
        '--root', '/',
    ]
    if font_path:
        cmd.extend(['--font-path', str(font_path)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"   [오류] Typst 컴파일 실패:\n{result.stderr}")
        return False

    print(f"   Typst 컴파일 완료: {pdf_path.name}")
    return True


# ══════════════════════════════════════
# 의존성 확인
# ══════════════════════════════════════

def check_dependencies() -> bool:
    """필수 도구 설치 확인"""
    missing = []
    for tool in ['typst', 'pandoc']:
        if shutil.which(tool) is None:
            missing.append(tool)

    if missing:
        print(f"[오류] 필수 도구 미설치: {', '.join(missing)}")
        print(f"  설치: brew install {' '.join(missing)}")
        return False

    for tool in ['typst', 'pandoc']:
        result = subprocess.run([tool, '--version'], capture_output=True, text=True)
        version = result.stdout.strip().split('\n')[0]
        print(f"   {tool}: {version}")

    return True


# ══════════════════════════════════════
# 메인 빌드 함수
# ══════════════════════════════════════

def build(config: dict):
    """PDF 빌드 실행.

    config 필수 키:
        title:       str       — 책 제목 (출력 메시지용)
        base:        Path      — 프로젝트 루트
        assets_dir:  Path      — 이미지 에셋 디렉토리
        mermaid_out: Path      — Mermaid 렌더링 출력 디렉토리
        template:    Path      — Typst 템플릿 (book.typ)
        font_path:   Path|None — 추가 폰트 디렉토리
        front:       list[Path]— 전문 마크다운 파일 목록
        chapters:    list[Path]— 챕터 마크다운 파일 목록
        back:        list[Path]— 후문 마크다운 파일 목록
        output_md:   Path      — 통합 마크다운 출력 경로
        output_typ:  Path      — 최종 Typst 출력 경로
        output_pdf:  Path      — PDF 출력 경로
    """
    global _mermaid_counter

    title = config.get('title', 'Book')
    print(f"{title} 통합 PDF 생성 (Typst)")
    print("=" * 50)

    # 0. 의존성 확인
    if not check_dependencies():
        return

    # 1. Mermaid 초기화
    _mermaid_counter = 0
    mermaid_out = config['mermaid_out']
    if mermaid_out.exists():
        shutil.rmtree(mermaid_out)

    # 2. 마크다운 통합 + 전처리
    print("\n[1/6] 마크다운 통합 + 전처리...")
    integrated_md = build_integrated_md(
        config['front'], config['chapters'], config['back'], mermaid_out
    )
    output_md = config['output_md']
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(integrated_md, encoding="utf-8")
    print(f"\n   통합 마크다운: {output_md.name}")

    # 3. 이미지 공백 자동 제거
    print("\n[2/6] 이미지 공백 자동 제거...")
    autocrop_all_assets(config['assets_dir'], mermaid_out)

    # 4. Pandoc: MD → Typst (임시)
    print("\n[3/6] Pandoc 변환 (MD → Typst)...")
    output_typ = config['output_typ']
    temp_typ = output_typ.with_suffix('.raw.typ')
    if not md_to_typst(output_md, temp_typ):
        return

    # 5. 후처리 + 템플릿 병합
    print("\n[4/6] 후처리 + 템플릿 병합...")
    raw_content = temp_typ.read_text(encoding="utf-8")
    fixed_content = fix_typst_content(raw_content)
    final_typ = merge_template_and_content(config['template'], fixed_content)
    output_typ.write_text(final_typ, encoding="utf-8")
    temp_typ.unlink(missing_ok=True)
    print(f"   최종 Typst: {output_typ.name}")

    # 6. Typst 컴파일: TYP → PDF
    print("\n[5/6] Typst 컴파일 (TYP → PDF)...")
    output_pdf = config['output_pdf']
    if not typst_compile(output_typ, output_pdf, config.get('font_path')):
        return

    size_mb = output_pdf.stat().st_size / (1024 * 1024)
    print(f"\n   PDF 생성 완료: {output_pdf.name} ({size_mb:.1f} MB)")

    # 7. 레이아웃 분석
    print("\n[6/6] 레이아웃 분석...")
    try:
        # pdf_layout_checker를 동적 import (스킬 스크립트 또는 프로젝트에서 제공)
        import importlib.util
        checker_path = config.get('layout_checker')
        if checker_path and Path(checker_path).exists():
            spec = importlib.util.spec_from_file_location("pdf_layout_checker", checker_path)
            checker = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(checker)
        else:
            import pdf_layout_checker as checker

        checker.print_page_usage(str(output_pdf))
        issues = checker.analyze_layout(str(output_pdf))
        checker.print_report(issues, str(output_pdf))
    except (ImportError, AttributeError):
        print("   [참고] pdf_layout_checker 없음 → 레이아웃 분석 건너뜀")
    except Exception as e:
        print(f"   [경고] 레이아웃 분석 오류: {e}")

    print(f"\n{'=' * 50}")
    print(f"완료: {output_pdf}")
