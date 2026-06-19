#!/usr/bin/env python3
"""범용 마크다운 → Typst → PDF 변환 엔진
   프로젝트별 설정(챕터 목록, 경로 등)은 호출 측에서 config로 전달.
   의존성: typst, pandoc, npx @mermaid-js/mermaid-cli, Pillow, PyMuPDF
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Mermaid 다이어그램 전역 카운터
_mermaid_counter = 0

# 콘텐츠 마커 — template+base와 content 경계 표시
CONTENT_MARKER = "// ══ CONTENT ══"

# PRE_TOC 마커 — cover와 toc 사이에 삽입되는 콘텐츠 (머릿말 등)
PRE_TOC_MARKER = "// ── PRE_TOC_CONTENT ──"

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
            return f'\n![다이어그램]({_typst_img_path(abs_path)})\n'

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
                    return f'\n![다이어그램]({_typst_img_path(abs_path)})\n'

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


def _typst_img_path(p: Path) -> str:
    """Typst는 드라이브 문자(C:)와 백슬래시를 경로로 받지 않는다.
    컴파일 root(드라이브 루트)를 기준으로 한 루트 절대 POSIX 경로로 변환한다.
    예) C:\\work\\a\\b.png → /work/a/b.png (root=C:\\ 기준 해석)"""
    p = p.resolve()
    rel = p.as_posix()                       # 'C:/work/a/b.png' 또는 '/home/a/b.png'
    anchor = p.anchor.replace('\\', '/')     # 'C:/' (win) 또는 '/' (posix)
    if anchor and rel.startswith(anchor):
        rel = rel[len(anchor):]
    return '/' + rel


def fix_image_paths(text: str, source_file: Path) -> str:
    """마크다운 이미지 상대경로 → 절대경로로 변환 (file:// 없이)"""
    source_dir = source_file.parent
    # 프로젝트 루트 추정 (chapters/ 또는 book/ 상위)
    project_root = source_dir
    for parent in source_file.parents:
        if (parent / "assets").exists():
            project_root = parent
            break

    def replace_img(m):
        alt = m.group(1)
        rel_path = m.group(2)
        if rel_path.startswith('file://'):
            return f'![{alt}]({rel_path[7:]})'
        # 1차: 소스 파일 기준 상대경로
        abs_path = (source_dir / rel_path).resolve()
        if abs_path.exists():
            return f'![{alt}]({_typst_img_path(abs_path)})'
        # 2차: 프로젝트 루트 기준
        abs_path2 = (project_root / rel_path).resolve()
        if abs_path2.exists():
            return f'![{alt}]({_typst_img_path(abs_path2)})'
        # 3차: assets/ 하위에서 파일명으로 검색
        filename = Path(rel_path).name
        for found in project_root.rglob(filename):
            if found.is_file():
                return f'![{alt}]({_typst_img_path(found)})'
        # 못 찾으면 플레이스홀더 텍스트 (Typst 컴파일 에러 방지)
        print(f"   [경고] 이미지 없음: {rel_path}")
        return f'*\\[이미지 누락: {alt}\\]*'

    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, text)


def clean_comments(text: str) -> str:
    """HTML 주석 제거 (GEMINI PROMPT, CAPTURE NEEDED, 기타)"""
    text = re.sub(r'<!--\s*\[GEMINI PROMPT.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--\s*\[CAPTURE NEEDED.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text


def convert_img_tags(text: str) -> str:
    """<img src="..." alt="..."> HTML 태그를 ![alt](src) 마크다운으로 변환.
    코드 블록 내부의 <img>는 보존."""
    parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
    for i, part in enumerate(parts):
        if not part.startswith('```'):
            def _replace_img_tag(m):
                tag = m.group(0)
                src_m = re.search(r'src\s*=\s*["\']([^"\']+)["\']', tag)
                alt_m = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', tag)
                if not src_m:
                    return tag
                src = src_m.group(1)
                alt = alt_m.group(1) if alt_m else ''
                return f'![{alt}]({src})'
            parts[i] = re.sub(r'<img\s[^>]*>', _replace_img_tag, part)
    return ''.join(parts)


def fix_br_tags(text: str) -> str:
    """코드 블록 밖의 <br> → 마크다운 줄바꿈으로 변환.
    코드 블록(```)과 mermaid 내의 <br>는 보존."""
    parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
    for i, part in enumerate(parts):
        if not part.startswith('```'):
            parts[i] = re.sub(r'<br\s*/?>', '  ', part)
    return ''.join(parts)


_CODE_TITLE_RE = re.compile(
    r'^```([A-Za-z][\w+#.\-]*)[ \t]+(\S[^\n]*?)[ \t]*\n(.*?)^```[ \t]*$',
    re.MULTILINE | re.DOTALL)


def split_code_block_titles(text: str) -> str:
    """```언어 [라벨] 제목 형태의 펜스 헤더를 분리한다.

    pandoc은 코드펜스 info string에 공백이 있으면(예: ```bash [터미널] 제목)
    그 블록을 코드 블록으로 인식하지 못해 줄바꿈이 전부 사라진다.
    제목을 코드블록 위 굵은 줄로 빼고 펜스를 ```언어 단일 토큰으로 정규화한다.
    제목 없는 일반 펜스(```bash)는 건드리지 않는다."""
    def repl(m):
        lang, title, body = m.group(1), m.group(2).strip(), m.group(3)
        return f"**{title}**\n```{lang}\n{body}```"
    return _CODE_TITLE_RE.sub(repl, text)


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
            content = convert_img_tags(content)
            content = fix_image_paths(content, f)
            content = render_mermaid_diagrams(content, mermaid_out)
            content = split_code_block_titles(content)
            content = fix_br_tags(content)
            content = re.sub(r'\n{3,}', '\n\n', content)
            parts.append(content)
            parts.append("\n\n---\n\n")

    return "\n".join(parts)


# ══════════════════════════════════════
# Pandoc 변환
# ══════════════════════════════════════

def md_to_typst(md_path: Path, typ_path: Path) -> bool:
    """Pandoc으로 마크다운 → Typst 변환 (paragraph-gap Lua 필터 포함)"""
    lua_filter = Path(__file__).parent / 'paragraph-gap.lua'
    cmd = [
        'pandoc',
        str(md_path),
        '-f', 'markdown+pipe_tables+fenced_code_blocks+backtick_code_blocks-citations',
        '-t', 'typst',
        '-o', str(typ_path),
        '--wrap=none',
        '--lua-filter', str(lua_filter),
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


def _detect_image_style(path: str, preset: str = "plain") -> str:
    """이미지 경로와 프리셋명으로 style 값을 결정.
    프리셋은 (개념도용, 나머지용) 튜플로 매핑.
    개념도 = gemini/ 경로의 이미지."""
    is_gemini = 'gemini/' in path

    presets = {
        'clean-border': ('bordered', 'minimal'),
        'shadow': ('shadow', 'shadow'),
        'primary-shadow': ('bordered-shadow', 'shadow'),
        'minimal': ('minimal', 'minimal'),
    }

    pair = presets.get(preset)
    if pair is None:
        return 'plain'
    concept_style, other_style = pair
    return concept_style if is_gemini else other_style


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


def _detect_image_category(path: str) -> str:
    """이미지 경로로 카테고리 분류 (변수 기반 모드용)"""
    if '/gemini/' in path or 'chapter-opening' in path:
        return 'gemini'
    elif '/terminal/' in path:
        return 'terminal'
    elif '/diagram/' in path or 'mermaid_' in path:
        return 'diagram'
    return 'default'


def fix_typst_content(text: str, image_border_preset: str = "plain", use_image_variables: bool = False, **kwargs) -> str:
    """Pandoc 출력의 Typst 코드를 후처리.
    image_border_preset: 이미지 테두리 프리셋명 (plain, clean-border, shadow, primary-shadow, minimal)"""

    # 1. 이미지 수정: !#link("path")[alt] → #auto-image (페이지 공간 자동 조절)
    def fix_image(m):
        path = m.group(1)
        alt = m.group(2).strip()
        if use_image_variables:
            cat = _detect_image_category(path)
            width_var = f'img-{cat}-width'
            style_var = f'img-{cat}-style'
            if alt:
                return f'#auto-image("{path}", alt: [{alt}], max-width: {width_var}, style: {style_var})'
            else:
                return f'#auto-image("{path}", max-width: {width_var}, style: {style_var})'
        max_w = _detect_image_max_width(path)
        style = _detect_image_style(path, image_border_preset)
        style_param = f', style: "{style}"' if style != "plain" else ""
        if alt:
            return f'#auto-image("{path}", alt: [{alt}], max-width: {max_w}{style_param})'
        else:
            return f'#auto-image("{path}", max-width: {max_w}{style_param})'

    text = re.sub(r'!#link\("([^"]+)"\)\[([^\]]*)\]', fix_image, text)

    # 2. 이미지 수정: #box(image("path")) → #auto-image
    def fix_box_image(m):
        path = m.group(1)
        if use_image_variables:
            cat = _detect_image_category(path)
            width_var = f'img-{cat}-width'
            style_var = f'img-{cat}-style'
            return f'#auto-image("{path}", max-width: {width_var}, style: {style_var})'
        max_w = _detect_image_max_width(path)
        style = _detect_image_style(path, image_border_preset)
        style_param = f', style: "{style}"' if style != "plain" else ""
        return f'#auto-image("{path}", max-width: {max_w}{style_param})'

    text = re.sub(r'#box\(image\("([^"]+)"\)\)', fix_box_image, text)

    # 3. 이미지 수정: #figure(image("path"), caption: [...]) → #auto-image
    def fix_figure_image(m):
        path = m.group(1)
        alt = ' '.join(m.group(2).split()) if m.group(2) else ""
        if use_image_variables:
            cat = _detect_image_category(path)
            width_var = f'img-{cat}-width'
            style_var = f'img-{cat}-style'
            if alt:
                return f'#auto-image("{path}", alt: [{alt}], max-width: {width_var}, style: {style_var})'
            else:
                return f'#auto-image("{path}", max-width: {width_var}, style: {style_var})'
        max_w = _detect_image_max_width(path)
        style = _detect_image_style(path, image_border_preset)
        style_param = f', style: "{style}"' if style != "plain" else ""
        if alt:
            return f'#auto-image("{path}", alt: [{alt}], max-width: {max_w}{style_param})'
        else:
            return f'#auto-image("{path}", max-width: {max_w}{style_param})'

    text = re.sub(
        r'#figure\(image\("([^"]+)"\)\s*,\s*caption:\s*\[([^\]]*)\]\s*\)',
        fix_figure_image, text
    )

    # 3.5 이미지 바로 뒤의 #emph[그림 N-M: ...] 캡션을 auto-image의 alt 파라미터로 병합
    #     이미지와 캡션이 같은 페이지에 있도록 보장 (캡션만 다음 페이지로 넘어가는 고아 방지)
    def _merge_caption_into_auto_image(m):
        img_call = m.group(1)  # #auto-image("path", alt: [...], max-width: 0.6)
        caption = m.group(2)    # 그림 2-4: 설명 텍스트
        # 자동 번호 부여를 위해 수동 "그림 N-N:" / "실행 결과 N-N:" 접두어 제거
        caption = re.sub(r'^(?:그림|실행\s*결과)\s*[\d서]+-\d+\s*[:：]\s*', '', caption)
        if 'alt:' in img_call:
            # alt가 이미 있으면 이탤릭 캡션으로 교체
            return re.sub(r'alt:\s*\[[^\]]*\]', f'alt: [{caption}]', img_call)
        # max-width: 앞에 alt: 삽입
        return img_call.replace('max-width:', f'alt: [{caption}], max-width:')

    text = re.sub(
        r'(#auto-image\([^)]*\))\s*\n?#emph\[((?:[^\]\\]|\\.)*)\]',
        _merge_caption_into_auto_image,
        text
    )

    # 3.55 auto-image 뒤에 빈 줄 보장 (Typst가 figure와 다음 문단을 분리하도록)
    text = re.sub(r'(#auto-image\([^)]*\))\n([^\n])', r'\1\n\n\2', text)

    # 3.6 pre_toc 콘텐츠 heading 목차 제외: = 제목 → #heading(outlined: false)[제목]
    #     pre_toc 파일은 목차 앞에 배치되므로 목차에 포함되면 안 됨
    if kwargs.get('exclude_from_toc'):
        text = re.sub(r'^(=+)\s+(.+)$',
                       lambda m: f'#heading(outlined: false, level: {len(m.group(1))})[{m.group(2).strip()}]',
                       text, flags=re.MULTILINE)

    # 3.7 callout-box 변환: > **라벨**: 내용 or > **라벨: 제목** 내용
    #     라벨을 프라이머리 색상 볼드로 강조
    #     본문에 #strong[...] 등 중첩 브라켓이 있을 수 있으므로 정규식 대신 파싱
    def _convert_callout_boxes(text):
        result = []
        i = 0
        marker = '#quote(block: true)['
        while i < len(text):
            pos = text.find(marker, i)
            if pos == -1:
                result.append(text[i:])
                break
            result.append(text[i:pos])
            # 브라켓 매칭으로 quote 블록 전체 추출
            start = pos + len(marker)
            depth = 1
            j = start
            while j < len(text) and depth > 0:
                if text[j] == '[':
                    depth += 1
                elif text[j] == ']':
                    depth -= 1
                j += 1
            inner = text[start:j-1].strip()
            # 패턴 A: #strong[라벨]: 본문
            m = re.match(r'#strong\[([^\]]+)\]:\s*(.*)', inner, re.DOTALL)
            if not m:
                # 패턴 B: #strong[라벨: 제목] (—|--)? 본문
                m = re.match(r'#strong\[([^:\]]+:\s*[^\]]+)\]\s*(?:---|—|--)?\s*(.*)', inner, re.DOTALL)
            if m:
                label = m.group(1).strip()
                body = m.group(2).strip()
                result.append(f'#callout-box([{label}], [{body}])')
            else:
                # callout 패턴이 아니면 원본 유지
                result.append(f'{marker}{inner}]')
            i = j
        return ''.join(result)

    text = _convert_callout_boxes(text)

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

    # 8. 문단 간격: Pandoc Lua 필터(paragraph-gap.lua)에서 처리
    #    Para→Para 사이에만 #v(paragraph-gap) 삽입 (표/코드/이미지에 영향 없음)

    return text


def merge_template_and_content(template_path: Path, content: str,
                               design: str | None = None,
                               design_state: dict | None = None,
                               skip_cover: bool = False,
                               skip_toc: bool = False,
                               pre_toc_content: str = "") -> str:
    """템플릿 + Pandoc 변환 내용을 하나의 .typ 파일로 합침

    design이 지정되면 컴포넌트 어셈블러로 book_base를 조립.
    없으면 기존 book_base.typ 파일을 사용 (하위호환).
    pre_toc_content가 있으면 cover와 toc 사이에 삽입 (머릿말 등).
    """
    template = template_path.read_text(encoding="utf-8")

    if design is not None:
        from design_assembler import parse_design_arg, load_preset_overrides, assemble_book_base
        selection = parse_design_arg(design)
        # 프리셋에 overrides가 있으면 design_state에 병합 (프리셋이 기본, 사용자가 우선)
        preset_overrides = load_preset_overrides(design) if design.strip() in "123456789" else {}
        if preset_overrides:
            merged = dict(preset_overrides)
            if design_state:
                for k, v in design_state.items():
                    if isinstance(v, dict) and k in merged and isinstance(merged[k], dict):
                        merged[k] = {**merged[k], **v}
                    else:
                        merged[k] = v
            design_state = merged
        base = assemble_book_base(selection, design_state=design_state,
                                  skip_cover=skip_cover, skip_toc=skip_toc)
    else:
        base_path = template_path.parent / "book_base.typ"
        if base_path.exists():
            base = base_path.read_text(encoding="utf-8")
        else:
            base = ""

    # PRE_TOC 마커에 머릿말 등 삽입
    if base and pre_toc_content:
        if PRE_TOC_MARKER in base:
            base = base.replace(PRE_TOC_MARKER, pre_toc_content)
        elif "// 목차" in base or "#outline(" in base:
            # 마커 없을 때 fallback: 목차 섹션 직전에 삽입
            for marker in ["// ══════════════════════════════════════\n// 목차", "// 목차 (자동 생성)", "// 목차"]:
                if marker in base:
                    base = base.replace(marker, pre_toc_content + "\n" + marker, 1)
                    break
    elif base and PRE_TOC_MARKER in base:
        base = base.replace(PRE_TOC_MARKER, "")

    if base:
        return template + "\n" + base + "\n" + CONTENT_MARKER + "\n" + content
    return template + "\n" + CONTENT_MARKER + "\n" + content


def extract_content_from_typ(typ_text: str) -> str | None:
    """CONTENT_MARKER 이후 콘텐츠 추출. 마커 없으면 None 반환."""
    if CONTENT_MARKER in typ_text:
        _, content = typ_text.split(CONTENT_MARKER, 1)
        return content.lstrip("\n")
    return None


# ══════════════════════════════════════
# Typst 컴파일
# ══════════════════════════════════════

def typst_compile_svg(typ_path: Path, svg_dir: Path,
                      font_path: Path | None = None) -> int:
    """Typst → 페이지별 SVG 컴파일. 생성된 페이지 수 반환."""
    svg_dir.mkdir(parents=True, exist_ok=True)
    for old in svg_dir.glob("page_*.svg"):
        old.unlink()

    svg_pattern = str(svg_dir / "page_{p}.svg")
    cmd = [
        'typst', 'compile',
        str(typ_path), svg_pattern,
        '--format', 'svg',
        '--root', '/',
    ]
    if font_path:
        cmd.extend(['--font-path', str(font_path)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"   [오류] Typst SVG 컴파일 실패:\n{result.stderr}")
        raise RuntimeError(result.stderr)

    page_count = len(list(svg_dir.glob("page_*.svg")))
    print(f"   SVG 컴파일 완료: {page_count}페이지")
    return page_count


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
# Stage 1: raw .typ 생성 (캐시용)
# ══════════════════════════════════════

def build_raw_typ(front: list, chapters: list, back: list,
                  mermaid_out: Path, assets_dir: Path,
                  md_output: Path,
                  image_border_preset: str = "plain",
                  use_image_variables: bool = False,
                  exclude_from_toc: bool = False) -> str:
    """Stage 1: MD 파일들 → 통합 MD → Pandoc → 후처리된 raw .typ 콘텐츠.

    템플릿/디자인 병합 전 단계까지만 실행하고 결과 문자열을 반환.
    디자인 변경 시 이 결과를 캐시하여 Stage 2만 재실행하면 ~200ms로 처리 가능.
    """
    global _mermaid_counter
    _mermaid_counter = 0

    # 이미지 공백 제거
    autocrop_all_assets(assets_dir, mermaid_out)

    # 통합 MD
    integrated = build_integrated_md(front, chapters, back, mermaid_out)
    if md_output is None:
        import tempfile
        tmp = tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8")
        tmp.write(integrated)
        tmp.close()
        md_output = Path(tmp.name)
        _tmp_md = True
    else:
        md_output.parent.mkdir(parents=True, exist_ok=True)
        md_output.write_text(integrated, encoding="utf-8")
        _tmp_md = False

    # Pandoc 변환
    raw_typ_path = md_output.with_suffix('.raw.typ')
    if not md_to_typst(md_output, raw_typ_path):
        raise RuntimeError("Pandoc 변환 실패")

    # 후처리
    raw = raw_typ_path.read_text(encoding="utf-8")
    fixed = fix_typst_content(raw, image_border_preset=image_border_preset, use_image_variables=use_image_variables, exclude_from_toc=exclude_from_toc)
    raw_typ_path.unlink(missing_ok=True)
    if _tmp_md:
        md_output.unlink(missing_ok=True)

    print(f"   Stage 1 완료: raw .typ ({len(fixed)} chars)")
    return fixed


# ══════════════════════════════════════
# 부분 빌드 함수
# ══════════════════════════════════════

def build_partial(md_content: str, config: dict,
                  design_state: dict | None = None,
                  include_cover: bool = False) -> Path | None:
    """선택된 블록만 PDF로 빌드 (경량 빌드)

    Parameters:
        md_content: 선택된 블록들의 마크다운 텍스트
        config: 빌드 설정 (build()와 동일한 키)
        design_state: 에디터 디자인 상태 딕셔너리
        include_cover: 표지 페이지 포함 여부
    Returns:
        생성된 PDF 경로, 실패 시 None
    """
    import tempfile

    title = config.get('title', 'Book')
    print(f"{title} 부분 PDF 생성 (Typst)")
    print("-" * 40)

    # 0. 의존성 확인
    if not check_dependencies():
        return None

    # 1. 임시 MD 파일 생성
    book_dir = config['output_md'].parent
    tmp_md = book_dir / "_preview_partial.md"
    tmp_md.write_text(md_content, encoding="utf-8")
    print(f"   임시 MD: {tmp_md.name} ({len(md_content)} chars)")

    # 2. 전처리 (이미지 경로, br 태그 등)
    mermaid_out = config.get('mermaid_out', book_dir / '_mermaid_images')
    processed = build_integrated_md([], [tmp_md], [], mermaid_out)
    tmp_md.write_text(processed, encoding="utf-8")

    # 3. Pandoc 변환
    print("   Pandoc 변환...")
    tmp_raw_typ = book_dir / "_preview_partial.raw.typ"
    if not md_to_typst(tmp_md, tmp_raw_typ):
        print("   [오류] Pandoc 변환 실패")
        return None

    # 4. 후처리
    raw_content = tmp_raw_typ.read_text(encoding="utf-8")
    image_border_preset = config.get('image_border_preset', 'plain')
    fixed_content = fix_typst_content(raw_content, image_border_preset=image_border_preset)

    # 5. 템플릿 병합 (디자인 상태 반영)
    design = config.get('design')
    # design이 없으면 design_state의 components로 생성
    if not design and design_state:
        components = design_state.get('components', {})
        if components:
            design = ",".join(f"{k}={v}" for k, v in components.items())

    final_typ = merge_template_and_content(
        config['template'], fixed_content,
        design=design, design_state=design_state,
        skip_cover=not include_cover, skip_toc=not include_cover
    )

    out_typ = book_dir / "_preview_partial.typ"
    out_pdf = book_dir / "_preview_partial.pdf"
    out_typ.write_text(final_typ, encoding="utf-8")

    # 6. Typst 컴파일
    print("   Typst 컴파일...")
    if not typst_compile(out_typ, out_pdf, config.get('font_path')):
        print("   [오류] Typst 컴파일 실패")
        return None

    # 7. 임시 파일 정리
    for f in [tmp_md, tmp_raw_typ, out_typ]:
        f.unlink(missing_ok=True)

    size_kb = out_pdf.stat().st_size / 1024
    print(f"   완료: {out_pdf.name} ({size_kb:.0f} KB)")
    return out_pdf


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

    config 선택 키:
        image_border_preset: str — 이미지 테두리 프리셋
            "plain" (기본), "clean-border", "shadow", "primary-shadow", "minimal"
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

    # 1b. 표지 자동 생성 (cover_data가 있으면)
    if config.get('cover_data'):
        try:
            _cover_scripts = Path(__file__).resolve().parents[3] / "pub-studio" / "references" / "scripts"
            if str(_cover_scripts) not in sys.path:
                sys.path.insert(0, str(_cover_scripts))
            from cover_generator import generate_front_cover
            cover_dir = config['base'] / "assets"
            cover_path = generate_front_cover(config, cover_dir)
            # book.typ의 book-cover-image 변수를 이 경로로 설정
            template_path = config.get('template')
            if template_path and template_path.exists():
                typ_text = template_path.read_text(encoding="utf-8")
                if 'book-cover-image' in typ_text:
                    import re as _re
                    typ_text = _re.sub(
                        r'#let book-cover-image = ".*?"',
                        f'#let book-cover-image = "{cover_path}"',
                        typ_text,
                    )
                    template_path.write_text(typ_text, encoding="utf-8")
        except Exception as e:
            print(f"   [경고] 표지 자동 생성 실패: {e}")

    # 2. 마크다운 통합 + 전처리
    print("\n[1/6] 마크다운 통합 + 전처리...")
    pre_toc_files = config.get('pre_toc', [])
    integrated_md = build_integrated_md(
        config['front'], config['chapters'], config['back'], mermaid_out
    )
    output_md = config['output_md']
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(integrated_md, encoding="utf-8")
    print(f"\n   통합 마크다운: {output_md.name}")

    # 2b. pre_toc 파일 별도 처리 (머릿말 등 — 목차 앞에 배치)
    pre_toc_typ_content = ""
    if pre_toc_files:
        pre_toc_md = build_integrated_md(pre_toc_files, [], [], mermaid_out)
        pre_toc_md_path = output_md.parent / "_pre_toc.md"
        pre_toc_md_path.write_text(pre_toc_md, encoding="utf-8")
        pre_toc_raw = pre_toc_md_path.parent / "_pre_toc.raw.typ"
        if md_to_typst(pre_toc_md_path, pre_toc_raw):
            raw = pre_toc_raw.read_text(encoding="utf-8")
            image_border_preset = config.get('image_border_preset', 'plain')
            pre_toc_typ_content = fix_typst_content(raw, image_border_preset=image_border_preset, exclude_from_toc=True)
            pre_toc_raw.unlink(missing_ok=True)
        pre_toc_md_path.unlink(missing_ok=True)

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
    image_border_preset = config.get('image_border_preset', 'plain')
    fixed_content = fix_typst_content(raw_content, image_border_preset=image_border_preset)
    design = config.get('design')
    design_state = config.get('design_state')
    final_typ = merge_template_and_content(config['template'], fixed_content,
                                           design=design, design_state=design_state,
                                           pre_toc_content=pre_toc_typ_content)
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
