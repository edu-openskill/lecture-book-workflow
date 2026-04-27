"""2단계 빌드 캐시

preview.py의 전역 _cache dict를 클래스로 추출.
Stage 1 (MD→Typst) + Stage 2 (디자인 조립) 각각 해시 기반 캐시 무효화.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Callable

from models import ImageInfo


class BuildCache:
    """2단계 빌드 캐시 + 파일 모드 상태."""

    def __init__(self):
        # Stage 1 캐시
        self._file_hash: str | None = None
        self._raw_typ: str | None = None
        # Stage 2 캐시
        self._design_hash: str | None = None
        self._svg_dir: Path | None = None
        self._page_count: int = 0
        self._typ_path: Path | None = None
        # 이미지 목록
        self._images: list[ImageInfo] = []
        # 파일 모드
        self._mode: str = "project"
        self._file_path: str | None = None
        self._file_designable: bool = True
        self._file_content: str | None = None

    # ── 프로퍼티 ──

    @property
    def raw_typ(self) -> str | None:
        return self._raw_typ

    @property
    def page_count(self) -> int:
        return self._page_count

    @property
    def typ_path(self) -> Path | None:
        return self._typ_path

    @property
    def svg_dir(self) -> Path | None:
        return self._svg_dir

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def file_path(self) -> str | None:
        return self._file_path

    @property
    def file_designable(self) -> bool:
        return self._file_designable

    @property
    def file_content(self) -> str | None:
        return self._file_content

    @property
    def images(self) -> list[ImageInfo]:
        return list(self._images)

    # ── 해시 계산 ──

    @staticmethod
    def compute_file_hash(project_path: Path, files_dict: dict) -> str:
        """선택된 파일 경로 + mtime → 해시."""
        parts = []
        for section in ("front", "chapters", "back"):
            for rel in sorted(files_dict.get(section, [])):
                fp = project_path / rel
                if fp.exists():
                    parts.append(f"{rel}:{fp.stat().st_mtime}")
        return hashlib.md5("|".join(parts).encode()).hexdigest()

    @staticmethod
    def compute_design_hash(design_state: dict | None,
                            include_cover: bool = True,
                            include_toc: bool = True) -> str:
        """design_state + cover/toc 옵션 → 해시."""
        obj = {
            "state": design_state or {},
            "cover": include_cover,
            "toc": include_toc,
        }
        raw = json.dumps(obj, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(raw.encode()).hexdigest()

    # ── 캐시 유효성 ──

    def is_stage1_valid(self, file_hash: str) -> bool:
        return self._file_hash == file_hash and self._raw_typ is not None

    def is_stage2_valid(self, design_hash: str) -> bool:
        return self._design_hash == design_hash

    # ── 캐시 업데이트 ──

    def update_stage1(self, raw_typ: str, file_hash: str,
                      images: list[ImageInfo] | None = None):
        self._raw_typ = raw_typ
        self._file_hash = file_hash
        self._design_hash = None  # Stage 2 강제 재실행
        if images is not None:
            self._images = images

    def update_stage2(self, svg_dir: Path, page_count: int,
                      typ_path: Path, design_hash: str):
        self._svg_dir = svg_dir
        self._page_count = page_count
        self._typ_path = typ_path
        self._design_hash = design_hash

    def invalidate_stage2(self):
        """Stage 2 캐시만 무효화 (이미지 오버라이드 변경 시)."""
        self._design_hash = None

    # ── 파일 모드 ──

    def load_typ_file(self, file_path: Path,
                      extract_fn: Callable[[str], str | None]) -> tuple[bool, bool]:
        """파일 모드: .typ 파일 로드. (ok, designable) 반환."""
        text = file_path.read_text(encoding="utf-8")
        content = extract_fn(text)

        if content is not None:
            self._file_content = content
            self._file_designable = True
        else:
            self._file_content = text
            self._file_designable = False

        self._mode = "file"
        self._file_path = str(file_path)
        self._raw_typ = None
        self._design_hash = None
        self._file_hash = None
        return True, self._file_designable

    def reset_to_project_mode(self):
        """파일 모드 → 프로젝트 모드 전환."""
        self._mode = "project"
        self._file_path = None
        self._file_designable = True
        self._file_content = None
        self._raw_typ = None
        self._design_hash = None
        self._file_hash = None

    # ── 직렬화 ──

    def get_mode_info(self) -> dict:
        """현재 모드 정보 (API 응답용)."""
        return {
            "mode": self._mode,
            "file_path": self._file_path,
            "designable": self._file_designable,
        }

    def get_svg_meta(self) -> dict:
        """SVG 메타 정보 (API 응답용)."""
        return {
            "page_count": self._page_count,
            "has_cache": self._svg_dir is not None,
        }
