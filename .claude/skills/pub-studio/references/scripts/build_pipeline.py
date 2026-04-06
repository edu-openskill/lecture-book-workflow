"""빌드 파이프라인 — typst_builder.py 래핑

MD→Typst→PDF/SVG 전체 파이프라인을 OOP 인터페이스로 제공.
캐시는 소유하지 않음 — 호출자(PreviewServer)가 BuildCache로 관리.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from models import BuildResult, DesignState, ImageInfo
from design_engine import DesignEngine
from image_registry import ImageRegistry

# typst_builder.py 위치
_SCRIPTS_DIR = (
    Path(__file__).resolve().parents[3]
    / "pub-build"
    / "references"
    / "scripts"
)


def _get_typst_builder():
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))
    import typst_builder
    return typst_builder


class BuildPipeline:
    """MD→Typst→PDF/SVG 빌드 엔진.

    typst_builder.py 함수에 위임하되, ImageRegistry를 통합하여
    개별 이미지 오버라이드를 Stage 2에서 적용한다.
    """

    def __init__(self, config: dict):
        self._config = config
        self._image_registry = ImageRegistry()
        self._design_engine = DesignEngine()

    @property
    def image_registry(self) -> ImageRegistry:
        return self._image_registry

    @property
    def config(self) -> dict:
        return self._config

    def update_config(self, config: dict):
        self._config = config

    # ── Stage 1: MD → raw .typ ──

    def build_raw_typ(
        self,
        front: list[Path],
        chapters: list[Path],
        back: list[Path],
    ) -> str:
        """Stage 1: MD 파일 통합 → Pandoc 변환 → 후처리 → raw .typ 문자열.

        완료 후 image_registry.scan_raw_typ() 자동 호출.
        pre_toc 파일이 있으면 별도로 변환하여 _pre_toc_typ에 저장.
        """
        tb = _get_typst_builder()

        # 표지 자동 생성 (cover_data가 있으면)
        if self._config.get("cover_data"):
            try:
                from cover_generator import generate_front_cover
                build_dir = Path(self._config.get("base", ".")) / ".pdf-build"
                cover_path = generate_front_cover(self._config, build_dir)
                # book.typ의 book-cover-image 경로 업데이트
                template_path = Path(self._config.get("template", ""))
                if template_path.exists():
                    typ_text = template_path.read_text(encoding="utf-8")
                    if "book-cover-image" in typ_text:
                        import re as _re
                        typ_text = _re.sub(
                            r'#let book-cover-image = ".*?"',
                            f'#let book-cover-image = "{cover_path}"',
                            typ_text,
                        )
                        template_path.write_text(typ_text, encoding="utf-8")
            except Exception as e:
                print(f"   [경고] 표지 자동 생성 실패: {e}")

        # pre_toc 파일 별도 처리
        pre_toc_files = self._config.get("pre_toc", [])
        self._pre_toc_typ = ""
        if pre_toc_files:
            pre_toc_typ = tb.build_raw_typ(
                front=pre_toc_files, chapters=[], back=[],
                mermaid_out=self._config.get("mermaid_out"),
                assets_dir=self._config.get("assets_dir"),
                md_output=None,
                image_border_preset=self._config.get("image_border_preset", "plain"),
                use_image_variables=self._config.get("use_image_variables", True),
                exclude_from_toc=True,
            )
            self._pre_toc_typ = pre_toc_typ

        raw_typ = tb.build_raw_typ(
            front=front,
            chapters=chapters,
            back=back,
            mermaid_out=self._config.get("mermaid_out"),
            assets_dir=self._config.get("assets_dir"),
            md_output=self._config.get("output_md"),
            image_border_preset=self._config.get("image_border_preset", "plain"),
            use_image_variables=self._config.get("use_image_variables", True),
        )
        # Stage 1 완료 → 이미지 스캔
        self._image_registry.scan_raw_typ(raw_typ)
        return raw_typ

    # ── Stage 2: raw .typ + design → final .typ ──

    def assemble_final_typ(
        self,
        raw_typ: str,
        design_state: DesignState,
        skip_cover: bool = False,
        skip_toc: bool = False,
    ) -> str:
        """Stage 2: 이미지 오버라이드 적용 → 디자인 조립 → template merge.

        1. image_registry.apply_overrides()로 개별 이미지 width/style 교체
        2. design_engine으로 컴포넌트 조립
        3. typst_builder.merge_template_and_content()로 최종 .typ 생성
        """
        tb = _get_typst_builder()

        # 1. 이미지 오버라이드 적용
        content = self._image_registry.apply_overrides(raw_typ)

        # 2. design_arg 구성
        design_arg = self._design_engine.build_design_arg(design_state)

        # 3. merge
        final_typ = tb.merge_template_and_content(
            template_path=Path(self._config["template"]),
            content=content,
            design=design_arg,
            design_state=design_state.to_server_dict(),
            skip_cover=skip_cover,
            skip_toc=skip_toc,
            pre_toc_content=getattr(self, "_pre_toc_typ", ""),
        )

        # 4. 표 열 너비 자동 맞춤 + 수동 오버라이드
        ds = design_state.to_server_dict()
        table_overrides = ds.get("tableOverrides", {})
        final_typ = self._auto_table_columns(final_typ, table_overrides)

        return final_typ

    @staticmethod
    def _auto_table_columns(text: str, overrides: dict | None = None) -> str:
        """각 표의 셀 내용을 분석하여 열 너비를 자동 비례 배분.

        overrides: { "0": [30, 40, 30], "2": [20, 50, 30] } — 표 인덱스별 수동 비율(%)
        """
        import re
        overrides = overrides or {}

        # #table( 위치를 찾아 각 테이블 범위를 파싱
        table_starts = [m.start() for m in re.finditer(r'#table\s*\(', text)]
        if not table_starts:
            return text

        result = []
        prev_end = 0

        for idx, start in enumerate(table_starts):
            # 테이블 범위 찾기 (괄호 매칭)
            depth = 0
            i = start
            while i < len(text):
                if text[i] == '(':
                    depth += 1
                elif text[i] == ')':
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            table_end = i + 1
            table_text = text[start:table_end]

            # columns: 패턴 찾기
            col_match = re.search(r'columns:\s*(?:\(([^)]*)\)|(\d+))', table_text)
            if not col_match:
                result.append(text[prev_end:table_end])
                prev_end = table_end
                continue

            # 열 수 파악
            if col_match.group(2):
                ncols = int(col_match.group(2))
            else:
                ncols = max(len(re.findall(r'fr\b', col_match.group(1))),
                            len(re.findall(r'auto', col_match.group(1))))
            if ncols < 2:
                result.append(text[prev_end:table_end])
                prev_end = table_end
                continue

            # 수동 오버라이드 확인
            if str(idx) in overrides:
                widths = overrides[str(idx)]
                frs = [f'{w}fr' for w in widths]
                new_cols = f'columns: ({", ".join(frs)})'
                new_table = table_text[:col_match.start()] + new_cols + table_text[col_match.end():]
                result.append(text[prev_end:start] + new_table)
                prev_end = table_end
                continue

            # 자동 맞춤: 셀 내용 분석 (한글 2배 폭, 인라인코드 1.3배 가중치)
            import unicodedata
            def _vlen(s):
                return sum(2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1 for c in s)

            def _cell_width(cell_text):
                """셀의 실질 렌더링 폭 추정. 인라인코드는 줄바꿈 안 되므로 가중치 부여."""
                # 인라인코드 추출 (raw 텍스트) — 줄바꿈 불가이므로 최소 폭으로 반영
                code_spans = re.findall(r'`([^`]+)`', cell_text)
                code_width = max((_vlen(c) * 1.3 for c in code_spans), default=0)
                # 일반 텍스트
                clean = re.sub(r'#\w+\[([^\]]*)\]', r'\1', cell_text)
                clean = re.sub(r'#\w+', '', clean)
                clean = re.sub(r'`[^`]*`', '', clean)
                clean = clean.replace('\\', '').strip()
                text_width = _vlen(clean)
                return max(code_width, text_width)

            cells = re.findall(r'\[([^\]]*)\]', table_text)
            max_len = [1] * ncols
            for ci, cell in enumerate(cells):
                col = ci % ncols
                max_len[col] = max(max_len[col], _cell_width(cell))

            # fr 비율 계산 (전체 합 기준 비례, 최소 0.5fr)
            total = max(sum(max_len), 1)
            frs = [f'{max(0.5, round(l / total * ncols, 1))}fr' for l in max_len]
            new_cols = f'columns: ({", ".join(frs)})'
            new_table = table_text[:col_match.start()] + new_cols + table_text[col_match.end():]
            result.append(text[prev_end:start] + new_table)
            prev_end = table_end

        result.append(text[prev_end:])
        return ''.join(result)

    @staticmethod
    def extract_table_info(text: str, page_count: int = 0) -> list[dict]:
        """최종 .typ에서 표 메타데이터를 추출. 표 목록 UI용."""
        import re
        tables = []
        chapter_table_counters: dict[int, int] = {}
        text_len = max(len(text), 1)

        for m in re.finditer(r'#table\s*\(', text):
            start = m.start()
            depth = 0
            i = start
            while i < len(text):
                if text[i] == '(':
                    depth += 1
                elif text[i] == ')':
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            table_text = text[start:i + 1]

            col_m = re.search(r'columns:\s*(?:\(([^)]*)\)|(\d+))', table_text)
            if not col_m:
                continue
            ncols = int(col_m.group(2)) if col_m.group(2) else len(re.findall(r'fr\b|auto', col_m.group(1)))

            # 헤더 셀 추출
            cells = re.findall(r'\[([^\]]*)\]', table_text)
            headers = []
            for ci in range(min(ncols, len(cells))):
                clean = re.sub(r'#\w+\[([^\]]*)\]', r'\1', cells[ci])
                clean = re.sub(r'#\w+', '', clean).strip()
                headers.append(clean)

            # 현재 columns 값 추출
            col_vals = re.findall(r'([\d.]+)fr', col_m.group(0))
            widths = [float(v) for v in col_vals] if col_vals else [1.0] * ncols

            # 챕터 번호: 가장 가까운 H1 역탐색
            preceding = text[:start]
            h1_matches = list(re.finditer(r'^= (.+)$', preceding, re.MULTILINE))
            chapter_num = 0
            nearest_heading = ""
            if h1_matches:
                last_h1 = h1_matches[-1].group(1).strip()
                nearest_heading = last_h1[:40]
                ch_num_m = re.search(r'(\d+)', last_h1)
                if ch_num_m:
                    chapter_num = int(ch_num_m.group(1))

            chapter_table_counters[chapter_num] = chapter_table_counters.get(chapter_num, 0) + 1
            if chapter_num > 0:
                label = f"표 {chapter_num}-{chapter_table_counters[chapter_num]}"
            else:
                label = f"표 서-{chapter_table_counters[0]}"

            # 추정 페이지
            est_page = max(1, round(start / text_len * page_count)) if page_count > 0 else 0

            tables.append({
                "idx": len(tables),
                "cols": ncols,
                "headers": headers,
                "widths": widths,
                "label": label,
                "heading": nearest_heading,
                "est_page": est_page,
            })
        return tables

    # ── 컴파일 ──

    def compile_svg(self, typ_path: Path, svg_dir: Path) -> int:
        """컴파일 .typ → 페이지별 SVG. 페이지 수 반환."""
        tb = _get_typst_builder()
        font_path = self._config.get("font_path")
        fp = Path(font_path) if font_path else None
        return tb.typst_compile_svg(typ_path, svg_dir, font_path=fp)

    def compile_pdf(self, typ_path: Path, pdf_path: Path) -> bool:
        """컴파일 .typ → PDF. 성공 여부 반환."""
        tb = _get_typst_builder()
        font_path = self._config.get("font_path")
        fp = Path(font_path) if font_path else None
        return tb.typst_compile(typ_path, pdf_path, font_path=fp)

    # ── 유틸 ──

    @staticmethod
    def resolve_file_lists(
        project_path: Path, files_dict: dict
    ) -> tuple[list[Path], list[Path], list[Path]]:
        """파일 상대경로 dict → Path 리스트 (front, chapters, back)."""
        front = [
            project_path / f
            for f in files_dict.get("front", [])
            if (project_path / f).exists()
        ]
        chapters = [
            project_path / f
            for f in files_dict.get("chapters", [])
            if (project_path / f).exists()
        ]
        back = [
            project_path / f
            for f in files_dict.get("back", [])
            if (project_path / f).exists()
        ]
        return front, chapters, back

    @staticmethod
    def check_dependencies() -> bool:
        """typst, pandoc 설치 확인."""
        tb = _get_typst_builder()
        return tb.check_dependencies()
