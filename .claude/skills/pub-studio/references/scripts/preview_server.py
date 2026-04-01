"""프리뷰 서버 — HTTP 라우팅 + 비즈니스 로직 위임

preview.py의 make_handler/PreviewHandler를 OOP로 리팩토링.
모든 비즈니스 로직은 BuildPipeline, BuildCache, VerificationLoop 등에 위임.
HTTP 핸들러는 URL 디스패치만 담당하는 얇은 레이어.
"""

from __future__ import annotations

import http.server
import importlib.util
import json
import mimetypes
import os
import re
import shutil
import socket
import sys
import threading
import time
import urllib.parse
import webbrowser
from datetime import datetime
from pathlib import Path

from models import BuildResult, DesignState, VerificationResult
from build_cache import BuildCache
from build_pipeline import BuildPipeline
from image_registry import ImageRegistry
from layout_checker import LayoutChecker
from verification_loop import VerificationLoop

# ══════════════════════════════════════
# 프로젝트 감지 (모듈 레벨 함수 — 클래스 불필요)
# ══════════════════════════════════════

ROOT = Path(__file__).resolve().parents[5]  # 프로젝트 루트 (.claude/skills/pub-studio/references/scripts → 5단계 상위)
PROJECTS_DIR = ROOT / "projects"
HTML_FILE = Path(__file__).resolve().parent.parent / "preview_editor.html"  # references/preview_editor.html
DESIGNS_FILE = Path(__file__).resolve().parent.parent / "designs.json"  # references/designs.json (글로벌)
VARIANTS_FILE = Path(__file__).resolve().parent.parent / "variants.json"  # references/variants.json (커스텀 변형)
PRESETS_FILE = ROOT / ".claude" / "skills" / "pub-typst-design" / "references" / "templates" / "components" / "presets.json"
DEFAULT_PORT = 3333
BUILD_DIR_NAME = ".pdf-build"  # 스테이징 디렉토리명


def find_projects() -> list[dict]:
    if not PROJECTS_DIR.exists():
        return []
    dirs = [d for d in PROJECTS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return [{"name": d.name, "path": str(d)} for d in dirs]


def select_project(name: str | None = None) -> Path:
    projects = find_projects()
    if not projects:
        print("projects/ 폴더에 프로젝트가 없습니다.")
        sys.exit(1)
    if name:
        for p in projects:
            if p["name"] == name:
                return Path(p["path"])
        print(f"프로젝트 '{name}'을 찾을 수 없습니다.")
        print(f"사용 가능: {', '.join(p['name'] for p in projects)}")
        sys.exit(1)
    if len(projects) == 1:
        print(f"프로젝트: {projects[0]['name']}")
        return Path(projects[0]["path"])
    print("\n프로젝트를 선택하세요:\n")
    for i, p in enumerate(projects, 1):
        print(f"  {i}. {p['name']}")
    print()
    while True:
        try:
            choice = int(input("번호: ").strip())
            if 1 <= choice <= len(projects):
                return Path(projects[choice - 1]["path"])
        except (ValueError, EOFError):
            pass
        print(f"1~{len(projects)} 사이 번호를 입력하세요.")


# ══════════════════════════════════════
# 스테이징 (.pdf-build/)
# ══════════════════════════════════════

def stage_files(project_path: Path) -> dict:
    """소스 MD 파일을 .pdf-build/md/로 복사. 스테이징 정보 반환."""
    build_dir = project_path / BUILD_DIR_NAME
    md_dir = build_dir / "md"

    # 디렉토리 생성
    for sub in ("front", "chapters", "back"):
        (md_dir / sub).mkdir(parents=True, exist_ok=True)
    (build_dir / "_mermaid_images").mkdir(parents=True, exist_ok=True)
    (build_dir / "preview_svg").mkdir(parents=True, exist_ok=True)

    staged = {"front": 0, "chapters": 0, "back": 0}

    # 소스 → 스테이징 복사 매핑
    copies = [
        ("chapters", project_path / "chapters"),
        ("front", project_path / "book" / "front"),
        ("back", project_path / "book" / "back"),
    ]
    for group, src_dir in copies:
        if not src_dir.exists():
            continue
        for f in src_dir.glob("*.md"):
            shutil.copy2(f, md_dir / group / f.name)
            staged[group] += 1

    # assets 심링크 생성 (이미지 상대경로 해결: ../assets/CH01/ → 실제 assets/)
    assets_src = project_path / "assets"
    assets_link = md_dir / "assets"
    if assets_src.exists() and not assets_link.exists():
        assets_link.symlink_to(assets_src.resolve())
        print(f"  심링크: .pdf-build/md/assets → {assets_src}")

    total = sum(staged.values())
    print(f"  스테이징: {total}개 파일 → .pdf-build/md/")
    return staged


def _apply_default_checked(files: list[dict]):
    """버전 파일 기본 선택 로직.

    같은 이름의 -vN 파일이 있으면 버전 없는 파일(최신)만 체크.
    버전 없는 파일이 없으면 가장 높은 버전만 체크.
    """
    # base name → 버전 번호 목록
    bases: dict[str, list[int]] = {}
    has_latest: dict[str, bool] = {}

    for f in files:
        stem = f["name"].rsplit(".", 1)[0]
        m = re.match(r'^(.+)-v(\d+)$', stem)
        if m:
            base = m.group(1)
            ver = int(m.group(2))
            bases.setdefault(base, []).append(ver)
        else:
            has_latest[stem] = True

    for f in files:
        stem = f["name"].rsplit(".", 1)[0]
        m = re.match(r'^(.+)-v(\d+)$', stem)
        if m:
            base, ver = m.group(1), int(m.group(2))
            if base in has_latest:
                f["default_checked"] = False
            else:
                f["default_checked"] = (ver == max(bases[base]))
        else:
            f["default_checked"] = True


def _staging_to_source(staging_rel: str) -> str | None:
    """스테이징 경로 → 소스 경로 변환.

    .pdf-build/md/front/X → book/front/X
    .pdf-build/md/chapters/X → chapters/X
    .pdf-build/md/back/X → book/back/X
    """
    prefix = f"{BUILD_DIR_NAME}/md/"
    if not staging_rel.startswith(prefix):
        return None
    inner = staging_rel[len(prefix):]
    if inner.startswith("chapters/"):
        return inner
    if inner.startswith("front/") or inner.startswith("back/"):
        return "book/" + inner
    return None


# ══════════════════════════════════════
# 프로젝트 스캔 (모듈 레벨 함수)
# ══════════════════════════════════════

def scan_project(project_path: Path) -> dict:
    result = {
        "name": project_path.name,
        "path": str(project_path),
        "chapters": [],
        "front": [],
        "back": [],
        "assets": {},
    }
    md_dir = project_path / BUILD_DIR_NAME / "md"

    # front 파일 우선순위 (번호 접두사가 없으므로 이름 기반 정렬)
    _FRONT_ORDER = {"preface": 0, "github": 1, "prologue": 2, "roadmap": 3}

    def _front_sort_key(path):
        stem = path.stem.lower()
        for prefix, order in _FRONT_ORDER.items():
            if stem.startswith(prefix):
                return (order, stem)
        return (99, stem)

    # .pdf-build/md/ 에서 스캔 (스테이징된 파일)
    for group, sub in [("chapters", "chapters"), ("front", "front"), ("back", "back")]:
        group_dir = md_dir / sub
        if not group_dir.exists():
            continue
        sort_fn = _front_sort_key if group == "front" else None
        for f in sorted(group_dir.glob("*.md"), key=sort_fn):
            if f.name == "목차.md":
                continue
            entry = {
                "name": f.name,
                "path": f"{BUILD_DIR_NAME}/md/{sub}/{f.name}",
                "size": f.stat().st_size,
            }
            result[group].append(entry)

    # 버전 파일 기본 선택 로직 적용
    for group_key in ("front", "chapters", "back"):
        _apply_default_checked(result[group_key])
    assets_dir = project_path / "assets"
    if assets_dir.exists():
        for ch_dir in sorted(assets_dir.iterdir()):
            if not ch_dir.is_dir() or ch_dir.name.startswith("."):
                continue
            ch_assets = {}
            for sub in sorted(ch_dir.iterdir()):
                if sub.is_dir():
                    images = [
                        f.name for f in sorted(sub.iterdir())
                        if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")
                    ]
                    if images:
                        ch_assets[sub.name] = images
                elif sub.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"):
                    ch_assets.setdefault("_root", []).append(sub.name)
            if ch_assets:
                result["assets"][ch_dir.name] = ch_assets
    progress_file = project_path / "progress.json"
    if progress_file.exists():
        try:
            result["progress"] = json.loads(progress_file.read_text(encoding="utf-8"))
        except Exception:
            result["progress"] = {}
    return result


# ══════════════════════════════════════
# MD 블록 파서 (순수 함수)
# ══════════════════════════════════════

def parse_md_to_blocks(text: str) -> list[dict]:
    lines = text.split("\n")
    blocks = []
    i = 0
    counter = 0

    def make_block(btype, content, meta, start, end):
        nonlocal counter
        counter += 1
        return {
            "id": f"blk_{counter:03d}", "type": btype,
            "content": content, "meta": meta,
            "start_line": start + 1, "end_line": end + 1,
        }

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("<!--"):
            start = i
            comment_lines = [line]
            if "-->" not in stripped[4:]:
                i += 1
                while i < len(lines) and "-->" not in lines[i]:
                    comment_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    comment_lines.append(lines[i])
            content = "\n".join(comment_lines)
            meta = {}
            if "GEMINI PROMPT" in content:
                meta["prompt_type"] = "GEMINI PROMPT"
            elif "CAPTURE NEEDED" in content:
                meta["prompt_type"] = "CAPTURE NEEDED"
            blocks.append(make_block("comment", content, meta, start, i))
            i += 1
            continue
        if stripped.startswith("```"):
            start = i
            lang = stripped[3:].strip()
            code_lines = [line]
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                code_lines.append(lines[i])
            blocks.append(make_block("code", "\n".join(code_lines), {"lang": lang}, start, i))
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.+)", line)
        if m:
            blocks.append(make_block("heading", line, {"level": len(m.group(1))}, i, i))
            i += 1
            continue
        if re.match(r"^---+\s*$", stripped):
            blocks.append(make_block("hr", line, {}, i, i))
            i += 1
            continue
        img_m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if img_m:
            blocks.append(make_block("image", line, {
                "alt": img_m.group(1), "src": img_m.group(2),
            }, i, i))
            i += 1
            continue
        if stripped.startswith(">"):
            start = i
            quote_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i])
                i += 1
            blocks.append(make_block("quote", "\n".join(quote_lines), {}, start, i - 1))
            continue
        if stripped.startswith("|"):
            start = i
            table_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            blocks.append(make_block("table", "\n".join(table_lines), {}, start, i - 1))
            continue
        start = i
        para_lines = [line]
        i += 1
        while i < len(lines):
            nl = lines[i]
            ns = nl.strip()
            if (not ns or ns.startswith("#") or ns.startswith("```") or
                ns.startswith("---") or ns.startswith(">") or ns.startswith("|") or
                ns.startswith("<!--") or re.match(r"^!\[", ns)):
                break
            para_lines.append(nl)
            i += 1
        blocks.append(make_block("paragraph", "\n".join(para_lines), {}, start, i - 1))
    return blocks


def blocks_to_md(blocks: list[dict]) -> str:
    parts = []
    for i, block in enumerate(blocks):
        if i > 0:
            prev = blocks[i - 1]
            if prev["type"] == "comment" and block["type"] == "image":
                parts.append("\n")
            else:
                parts.append("\n\n")
        parts.append(block["content"])
    return "".join(parts) + "\n"


def add_preview_src(blocks: list[dict], chapter_rel_path: str) -> list[dict]:
    chapter_dir = Path(chapter_rel_path).parent
    for block in blocks:
        if block["type"] == "image" and "src" in block["meta"]:
            src = block["meta"]["src"]
            if not (src.startswith("http") or src.startswith("/")):
                resolved = (chapter_dir / src).as_posix()
                parts = []
                for p in resolved.split("/"):
                    if p == ".." and parts:
                        parts.pop()
                    elif p != ".":
                        parts.append(p)
                block["meta"]["preview_src"] = "/" + "/".join(parts)
    return blocks


def backup_file(file_path: Path) -> str | None:
    today = datetime.now().strftime("%Y-%m-%d")
    backup_path = file_path.with_suffix(f".md.{today}.bak")
    if not backup_path.exists():
        shutil.copy2(file_path, backup_path)
        return str(backup_path)
    return None


# ══════════════════════════════════════
# PreviewServer
# ══════════════════════════════════════

def _load_build_config(
    project_path: Path,
    design_state: dict | None = None,
    build_dir: Path | None = None,
) -> dict:
    """프로젝트 build_pdf_typst.py에서 CONFIG 로드.

    build_dir이 주어지면 중간 산출물 경로를 .pdf-build/로 오버라이드.
    """
    build_script = project_path / "book" / "build_pdf_typst.py"
    if not build_script.exists():
        raise FileNotFoundError("build_pdf_typst.py not found")
    spec = importlib.util.spec_from_file_location("build_pdf_typst", build_script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    config = dict(mod.CONFIG)
    if design_state:
        config["design_state"] = design_state
        components = design_state.get("components", {})
        if components:
            config["design"] = ",".join(f"{k}={v}" for k, v in components.items())
    # 스테이징 디렉토리로 중간 산출물 경로 오버라이드
    if build_dir:
        config["output_md"] = build_dir / "integrated.md"
        config["mermaid_out"] = build_dir / "_mermaid_images"
    return config


class PreviewServer:
    """PDF 디자인 프리뷰 서버.

    HTTP 라우팅은 얇은 디스패처(_RequestHandler).
    비즈니스 로직은 BuildPipeline, BuildCache, VerificationLoop에 위임.
    """

    def __init__(
        self,
        project_path: Path,
        port: int = DEFAULT_PORT,
        initial_file: str | None = None,
    ):
        self._project_path = project_path
        self._port = port
        self._build_dir = project_path / BUILD_DIR_NAME

        # 스테이징: 소스 MD → .pdf-build/md/
        stage_files(project_path)
        self._project_info = scan_project(project_path)

        # 서비스 객체
        config = _load_build_config(project_path, build_dir=self._build_dir)
        self._cache = BuildCache()
        self._pipeline = BuildPipeline(config)
        self._checker = LayoutChecker()
        self._verifier = VerificationLoop(self._pipeline, self._checker)

        # 검증 루프 비동기 상태
        self._verification_result: VerificationResult | None = None
        self._verification_running = False
        self._layout_issues: list[dict] = []

        # 파일 모드 초기화
        if initial_file:
            self._init_file_mode(initial_file)

    def _init_file_mode(self, file_path_str: str):
        from build_pipeline import _get_typst_builder
        tb = _get_typst_builder()
        fp = Path(file_path_str)
        if not fp.is_absolute():
            fp = self._project_path / fp
        if fp.exists() and fp.suffix == ".typ":
            ok, designable = self._cache.load_typ_file(fp, tb.extract_content_from_typ)
            print(f"  파일 모드: {fp.name} ({'디자인 가능' if designable else '뷰어 전용'})")
        else:
            print(f"  경고: {fp} 파일을 찾을 수 없거나 .typ가 아닙니다.")

    # ── GET 핸들러 ──

    def handle_get_project(self) -> dict:
        return self._project_info

    def handle_get_files(self) -> dict:
        return {
            "chapters": self._project_info["chapters"],
            "front": self._project_info["front"],
            "back": self._project_info["back"],
        }

    def handle_get_blocks(self, rel_path: str) -> dict | None:
        file_path = self._project_path / rel_path
        if not file_path.exists() or file_path.suffix != ".md":
            return None
        text = file_path.read_text(encoding="utf-8")
        blocks = parse_md_to_blocks(text)
        blocks = add_preview_src(blocks, rel_path)
        mtime = file_path.stat().st_mtime
        return {"path": rel_path, "blocks": blocks, "last_modified": mtime}

    def handle_get_file_content(self, rel_path: str) -> dict | None:
        file_path = self._project_path / rel_path
        if not file_path.exists() or file_path.suffix != ".md":
            return None
        text = file_path.read_text(encoding="utf-8")
        mtime = file_path.stat().st_mtime
        return {"path": rel_path, "content": text, "last_modified": mtime}

    def handle_get_images(self) -> dict:
        return self._pipeline.image_registry.to_dict()

    def handle_get_mode(self) -> dict:
        return self._cache.get_mode_info()

    def handle_get_svg_meta(self) -> dict:
        return self._cache.get_svg_meta()

    def handle_get_svg_page(self, page_num: str) -> Path | None:
        svg_dir = self._cache.svg_dir
        if svg_dir:
            svg_file = svg_dir / f"page_{page_num}.svg"
            if svg_file.exists():
                return svg_file
        return None

    def handle_get_layout_issues(self) -> dict:
        return {
            "issues": self._layout_issues,
            "verification": self._verification_result.to_dict() if self._verification_result else None,
        }

    def handle_get_verification_status(self) -> dict:
        return {
            "running": self._verification_running,
            "result": self._verification_result.to_dict() if self._verification_result else None,
        }

    def handle_get_designs(self, include_full: bool = False) -> dict:
        if not DESIGNS_FILE.exists():
            return {"designs": {}}
        store = json.loads(DESIGNS_FILE.read_text(encoding="utf-8"))
        if include_full:
            return store
        summary = {}
        for name, entry in store.get("designs", {}).items():
            summary[name] = {
                "created_at": entry.get("created_at"),
                "updated_at": entry.get("updated_at"),
            }
        return {"designs": summary}

    # ── POST 핸들러 ──

    def _sync_to_source(self, staging_rel: str, content: str) -> str | None:
        """스테이징 파일 저장 후 소스에도 동기화. 소스 백업 경로 반환."""
        source_rel = _staging_to_source(staging_rel)
        if not source_rel:
            return None
        source_path = self._project_path / source_rel
        if source_path.exists():
            bak = backup_file(source_path)
            source_path.write_text(content, encoding="utf-8")
            return bak
        return None

    def handle_post_save(self, data: dict) -> dict:
        rel_path = data.get("path", "")
        blocks = data.get("blocks", [])
        client_mtime = data.get("last_modified", 0)
        file_path = self._project_path / rel_path
        if not file_path.exists():
            return {"error": "File not found"}
        current_mtime = file_path.stat().st_mtime
        if client_mtime and abs(current_mtime - client_mtime) > 1:
            return {"error": "File modified externally", "server_mtime": current_mtime}
        md_text = blocks_to_md(blocks)
        file_path.write_text(md_text, encoding="utf-8")
        # 소스 파일에도 동기화
        bak = self._sync_to_source(rel_path, md_text)
        return {"ok": True, "backup": bak, "last_modified": file_path.stat().st_mtime}

    def handle_post_save_raw(self, data: dict) -> dict:
        rel_path = data.get("path", "")
        content = data.get("content", "")
        file_path = self._project_path / rel_path
        if not file_path.exists():
            return {"error": "File not found"}
        file_path.write_text(content, encoding="utf-8")
        # 소스 파일에도 동기화
        bak = self._sync_to_source(rel_path, content)
        return {"ok": True, "backup": bak, "last_modified": file_path.stat().st_mtime}

    def handle_post_build_svg(self, data: dict) -> dict:
        design_state_dict = data.get("design_state")
        design_state = DesignState.from_dict(design_state_dict) if design_state_dict else DesignState()
        is_file_mode = self._cache.mode == "file" or data.get("mode") == "file"

        start = time.time()
        stage_run = 0

        try:
            config = _load_build_config(self._project_path, design_state_dict, build_dir=self._build_dir)
            self._pipeline.update_config(config)

            if is_file_mode and self._cache.file_content is not None:
                stage_run = self._build_svg_file_mode(data, design_state, config)
            else:
                stage_run = self._build_svg_project_mode(data, design_state, config)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"ok": False, "error": str(e)[-2000:]}

        duration = round(time.time() - start, 2)

        # 표 메타데이터 추출
        table_info = []
        try:
            typ_file = self._build_dir / "final.typ"
            if typ_file.exists():
                pc = self._cache.page_count
                if pc == 0:
                    svg_dir = self._build_dir / "preview_svg"
                    if svg_dir.exists():
                        pc = len(list(svg_dir.glob("*.svg")))
                table_info = BuildPipeline.extract_table_info(typ_file.read_text(encoding="utf-8"), pc)
        except Exception:
            pass

        return {
            "ok": True,
            "page_count": self._cache.page_count,
            "svg_base": "/api/svg/",
            "duration": duration,
            "stage": stage_run if stage_run else "cached",
            "mode": self._cache.mode,
            "tables": table_info,
        }

    def _build_svg_file_mode(self, data: dict, design_state: DesignState, config: dict) -> int:
        """파일 모드 빌드. Stage 2만 실행."""
        stage_run = 0
        inc_cover = data.get("include_cover", True)
        inc_toc = data.get("include_toc", True)
        design_hash = self._cache.compute_design_hash(design_state.to_dict(), inc_cover, inc_toc)

        if self._cache.file_designable:
            if not self._cache.is_stage2_valid(design_hash):
                final_typ = self._pipeline.assemble_final_typ(
                    self._cache.file_content,
                    design_state,
                    skip_cover=not data.get("include_cover", True),
                    skip_toc=not data.get("include_toc", True),
                )
                stage_run = 2
            else:
                return 0  # cached
        else:
            if self._cache._design_hash is None:
                final_typ = self._cache.file_content
                stage_run = 2
            else:
                return 0  # cached

        if stage_run > 0:
            svg_dir = self._build_dir / "preview_svg"
            typ_path = self._build_dir / "final.typ"
            typ_path.write_text(final_typ, encoding="utf-8")
            page_count = self._pipeline.compile_svg(typ_path, svg_dir)
            self._cache.update_stage2(svg_dir, page_count, typ_path, design_hash)

        return stage_run

    def _build_svg_project_mode(self, data: dict, design_state: DesignState, config: dict) -> int:
        """프로젝트 모드 빌드. Stage 1 + Stage 2."""
        files_dict = data.get("files", {})
        force_stage1 = data.get("force_stage1", False)
        stage_run = 0

        if not any(files_dict.get(s) for s in ("front", "chapters", "back")):
            raise ValueError("No files selected")

        # Stage 1
        file_hash = self._cache.compute_file_hash(self._project_path, files_dict)
        if not self._cache.is_stage1_valid(file_hash) or force_stage1:
            front, chapters, back = BuildPipeline.resolve_file_lists(
                self._project_path, files_dict
            )
            raw_typ = self._pipeline.build_raw_typ(front, chapters, back)
            images = self._pipeline.image_registry.get_all()
            self._cache.update_stage1(raw_typ, file_hash, images)
            stage_run = 1

        # Stage 2
        inc_cover = data.get("include_cover", True)
        inc_toc = data.get("include_toc", True)
        design_hash = self._cache.compute_design_hash(design_state.to_dict(), inc_cover, inc_toc)
        if not self._cache.is_stage2_valid(design_hash) or stage_run == 1:
            final_typ = self._pipeline.assemble_final_typ(
                self._cache.raw_typ,
                design_state,
                skip_cover=not data.get("include_cover", True),
                skip_toc=not data.get("include_toc", True),
            )
            svg_dir = self._build_dir / "preview_svg"
            typ_path = self._build_dir / "final.typ"
            typ_path.write_text(final_typ, encoding="utf-8")
            page_count = self._pipeline.compile_svg(typ_path, svg_dir)
            self._cache.update_stage2(svg_dir, page_count, typ_path, design_hash)
            stage_run = max(stage_run, 2)

        return stage_run

    def handle_post_build_verified(self, data: dict) -> dict:
        """검증 빌드 — 백그라운드 스레드에서 실행."""
        if self._verification_running:
            return {"error": "검증이 이미 진행 중입니다"}

        design_state_dict = data.get("design_state")
        design_state = DesignState.from_dict(design_state_dict) if design_state_dict else DesignState()

        # 먼저 일반 빌드 실행
        build_result = self.handle_post_build_svg(data)
        if not build_result.get("ok"):
            return build_result

        # 검증 루프 실행
        self._verification_running = True

        def _run_verification():
            try:
                config = _load_build_config(self._project_path, design_state_dict, build_dir=self._build_dir)
                typ_path = self._cache.typ_path
                pdf_path = self._build_dir / "preview.pdf"
                svg_dir = self._cache.svg_dir

                result = self._verifier.run(
                    typ_path=typ_path,
                    pdf_path=pdf_path,
                    raw_typ=self._cache.raw_typ,
                    design_state=design_state,
                    svg_dir=svg_dir,
                )
                self._verification_result = result
                self._layout_issues = [i.to_dict() for i in result.issues]

                # SVG 캐시 업데이트
                if result.build_result and result.build_result.page_count > 0:
                    self._cache.update_stage2(
                        svg_dir, result.build_result.page_count,
                        typ_path, self._cache.compute_design_hash(
                        design_state.to_dict(),
                        data.get("include_cover", True),
                        data.get("include_toc", True),
                    ),
                    )
            except Exception as e:
                import traceback
                traceback.print_exc()
                self._verification_result = VerificationResult(
                    round_number=0,
                    build_result=BuildResult(success=False, error=str(e)),
                )
            finally:
                self._verification_running = False

        thread = threading.Thread(target=_run_verification, daemon=True)
        thread.start()

        return {
            "ok": True,
            "message": "검증 시작됨. /api/verification-status로 진행 상태 확인",
        }

    def handle_post_export_pdf(self, data: dict) -> dict:
        design_state = data.get("design_state")
        start = time.time()
        typ_path = self._cache.typ_path
        if not typ_path or not typ_path.exists():
            return {"ok": False, "error": "프리뷰를 먼저 빌드하세요"}
        config = _load_build_config(self._project_path, design_state, build_dir=self._build_dir)
        pdf_path = Path(config["output_pdf"])
        if not self._pipeline.compile_pdf(typ_path, pdf_path):
            return {"ok": False, "error": "Typst PDF 컴파일 실패"}
        duration = round(time.time() - start, 1)
        rel_pdf = str(pdf_path.relative_to(self._project_path))
        return {"ok": True, "pdf": "/" + rel_pdf, "duration": duration}

    def handle_post_image_override(self, data: dict) -> dict:
        path = data.get("path", "")
        width = data.get("width")
        style = data.get("style")
        if not path:
            return {"error": "path 필수"}
        self._pipeline.image_registry.set_override(
            path,
            width=width / 100 if width and width > 1 else width,
            style=style,
        )
        self._cache.invalidate_stage2()
        return {"ok": True}

    def handle_post_load_file(self, data: dict) -> dict:
        file_path_str = data.get("path", "")
        if not file_path_str:
            return {"error": "path 필수"}
        fp = Path(file_path_str)
        if not fp.is_absolute():
            fp = self._project_path / fp
        if not fp.exists() or fp.suffix != ".typ":
            return {"error": f"파일 없음 또는 .typ 아님: {fp}"}
        from build_pipeline import _get_typst_builder
        tb = _get_typst_builder()
        ok, designable = self._cache.load_typ_file(fp, tb.extract_content_from_typ)
        return {"ok": ok, "designable": designable, "path": str(fp)}

    def handle_post_switch_mode(self, data: dict) -> dict:
        mode = data.get("mode", "project")
        if mode == "project":
            self._cache.reset_to_project_mode()
            return {"ok": True, "mode": "project"}
        return {"error": f"알 수 없는 모드: {mode}"}

    def handle_post_restage(self, _data: dict) -> dict:
        """소스 MD 재스테이징. 소스에서 변경된 파일을 .pdf-build/md/로 다시 복사."""
        staged = stage_files(self._project_path)
        self._project_info = scan_project(self._project_path)
        self._cache.reset_to_project_mode()
        return {"ok": True, "staged": staged, "files": self.handle_get_files()}

    def handle_post_combine_md(self, data: dict) -> dict:
        files_dict = data.get("files", {})
        if not any(files_dict.get(s) for s in ("front", "chapters", "back")):
            return {"error": "No files selected"}
        from build_pipeline import _get_typst_builder
        tb = _get_typst_builder()
        config = _load_build_config(self._project_path, build_dir=self._build_dir)
        front, chapters, back = BuildPipeline.resolve_file_lists(
            self._project_path, files_dict
        )
        integrated = tb.build_integrated_md(front, chapters, back, config["mermaid_out"])
        # 통합 MD는 .pdf-build/에 저장 + book/에도 복사
        output_md = self._build_dir / "integrated.md"
        output_md.parent.mkdir(parents=True, exist_ok=True)
        output_md.write_text(integrated, encoding="utf-8")
        return {"ok": True, "path": str(output_md.relative_to(self._project_path)), "size": len(integrated)}

    def handle_post_design_save(self, data: dict) -> dict:
        name = data.get("name", "").strip()
        if not name:
            return {"error": "디자인 이름을 입력하세요"}
        if len(name) > 50:
            return {"error": "이름은 50자 이하여야 합니다"}
        design_state = data.get("state")
        if not design_state:
            return {"error": "디자인 상태가 비어있습니다"}
        overwrite = data.get("overwrite", False)

        if DESIGNS_FILE.exists():
            store = json.loads(DESIGNS_FILE.read_text(encoding="utf-8"))
        else:
            store = {"_version": 1, "designs": {}}

        if name in store["designs"] and not overwrite:
            return {"error": "duplicate", "message": f"'{name}' 이미 존재합니다. 덮어쓰시겠습니까?"}

        # imageOverrides는 프로젝트 종속이므로 제거
        saved_state = {k: v for k, v in design_state.items() if k != "imageOverrides"}
        saved_state["imageOverrides"] = {}

        now = datetime.now().isoformat(timespec="seconds")
        entry = store["designs"].get(name, {})
        store["designs"][name] = {
            "created_at": entry.get("created_at", now),
            "updated_at": now,
            "state": saved_state,
        }
        DESIGNS_FILE.write_text(
            json.dumps(store, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return {"ok": True, "name": name}

    def handle_post_design_delete(self, data: dict) -> dict:
        name = data.get("name", "").strip()
        if not DESIGNS_FILE.exists():
            return {"error": "저장된 디자인이 없습니다"}
        store = json.loads(DESIGNS_FILE.read_text(encoding="utf-8"))
        if name not in store.get("designs", {}):
            return {"error": f"'{name}' 디자인을 찾을 수 없습니다"}
        del store["designs"][name]
        DESIGNS_FILE.write_text(
            json.dumps(store, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return {"ok": True}

    # ── 프리셋 CRUD (presets.json) ──

    def _load_presets(self) -> dict:
        if not PRESETS_FILE.exists():
            return {}
        return json.loads(PRESETS_FILE.read_text(encoding="utf-8"))

    def _save_presets(self, presets: dict):
        PRESETS_FILE.write_text(
            json.dumps(presets, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def handle_get_presets(self) -> dict:
        return {"presets": self._load_presets()}

    def handle_post_preset_save(self, data: dict) -> dict:
        preset_id = data.get("id", "").strip()
        name = data.get("name", "").strip()
        description = data.get("description", "").strip()
        components = data.get("components")
        if not name:
            return {"error": "프리셋 이름을 입력하세요"}
        if not components:
            return {"error": "컴포넌트 설정이 비어있습니다"}

        presets = self._load_presets()

        # 새 프리셋이면 다음 번호 자동 부여
        if not preset_id:
            existing_ids = [int(k) for k in presets.keys() if k.isdigit()]
            preset_id = str(max(existing_ids) + 1 if existing_ids else 1)

        presets[preset_id] = {
            "name": name,
            "description": description,
            "components": components,
        }
        self._save_presets(presets)
        return {"ok": True, "id": preset_id}

    def handle_post_preset_update(self, data: dict) -> dict:
        preset_id = data.get("id", "").strip()
        if not preset_id:
            return {"error": "프리셋 ID가 필요합니다"}
        presets = self._load_presets()
        if preset_id not in presets:
            return {"error": f"프리셋 '{preset_id}'을 찾을 수 없습니다"}

        if "name" in data:
            presets[preset_id]["name"] = data["name"].strip()
        if "description" in data:
            presets[preset_id]["description"] = data["description"].strip()
        if "components" in data:
            presets[preset_id]["components"] = data["components"]
        if "overrides" in data:
            presets[preset_id]["overrides"] = data["overrides"]

        self._save_presets(presets)
        return {"ok": True, "id": preset_id}

    def handle_post_preset_delete(self, data: dict) -> dict:
        preset_id = data.get("id", "").strip()
        if not preset_id:
            return {"error": "프리셋 ID가 필요합니다"}
        presets = self._load_presets()
        if preset_id not in presets:
            return {"error": f"프리셋 '{preset_id}'을 찾을 수 없습니다"}
        del presets[preset_id]
        self._save_presets(presets)
        return {"ok": True}

    # ── 커스텀 변형 API ──

    def _load_variants_store(self) -> dict:
        if VARIANTS_FILE.exists():
            return json.loads(VARIANTS_FILE.read_text(encoding="utf-8"))
        return {"_version": 1, "variants": {}}

    def _save_variants_store(self, store: dict):
        VARIANTS_FILE.write_text(
            json.dumps(store, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def handle_get_variants(self) -> dict:
        """컴포넌트별 커스텀 변형 목록 반환."""
        store = self._load_variants_store()
        return {"ok": True, "variants": store.get("variants", {})}

    def handle_post_variant_save(self, data: dict) -> dict:
        """변형 생성/수정. builtIn(d1/d2)은 수정 불가."""
        component = data.get("component", "").strip()
        variant_id = data.get("variantId", "").strip()
        name = data.get("name", "").strip()
        properties = data.get("properties", {})

        if not component or not variant_id:
            return {"error": "component, variantId 필수"}
        if variant_id in ("d1", "d2"):
            return {"error": "내장 변형(d1/d2)은 수정할 수 없습니다"}
        if not name:
            name = variant_id

        store = self._load_variants_store()
        variants = store.setdefault("variants", {})
        comp_variants = variants.setdefault(component, {})
        comp_variants[variant_id] = {
            "name": name,
            "builtIn": False,
            "properties": properties,
        }
        self._save_variants_store(store)
        return {"ok": True, "variantId": variant_id}

    def handle_post_variant_delete(self, data: dict) -> dict:
        """커스텀 변형 삭제. builtIn(d1/d2)은 삭제 불가."""
        component = data.get("component", "").strip()
        variant_id = data.get("variantId", "").strip()

        if not component or not variant_id:
            return {"error": "component, variantId 필수"}
        if variant_id in ("d1", "d2"):
            return {"error": "내장 변형(d1/d2)은 삭제할 수 없습니다"}

        store = self._load_variants_store()
        comp_variants = store.get("variants", {}).get(component, {})
        if variant_id not in comp_variants:
            return {"error": f"'{variant_id}' 변형을 찾을 수 없습니다"}
        del comp_variants[variant_id]
        if not comp_variants:
            del store["variants"][component]
        self._save_variants_store(store)
        return {"ok": True}

    # ── 서버 시작 ──

    def start(self):
        """HTTP 서버 시작 + 브라우저 열기."""
        handler_class = self._make_handler()
        port = _find_free_port(self._port)
        with http.server.HTTPServer(("", port), handler_class) as server:
            url = f"http://localhost:{port}"
            print(f"\n  프로젝트:   {self._project_path.name}")
            print(f"  빌드 폴더: .pdf-build/")
            print(f"  서버:       {url}")
            print(f"  종료:       Ctrl+C\n")
            webbrowser.open(url)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("\n서버 종료.")

    def _make_handler(self):
        """얇은 HTTP 핸들러 팩토리."""
        server = self

        class _RequestHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass

            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                path = urllib.parse.unquote(parsed.path)
                query = dict(urllib.parse.parse_qsl(parsed.query))

                if path == "/":
                    self._serve_file(HTML_FILE, "text/html; charset=utf-8")
                elif path == "/api/project":
                    self._serve_json(server.handle_get_project())
                elif path == "/api/files":
                    self._serve_json(server.handle_get_files())
                elif path == "/api/blocks":
                    result = server.handle_get_blocks(query.get("path", ""))
                    if result is None:
                        self._serve_json({"error": "File not found"}, 404)
                    else:
                        self._serve_json(result)
                elif path == "/api/file-content":
                    result = server.handle_get_file_content(query.get("path", ""))
                    if result is None:
                        self._serve_json({"error": "File not found"}, 404)
                    else:
                        self._serve_json(result)
                elif path == "/api/images":
                    self._serve_json(server.handle_get_images())
                elif path.startswith("/api/svg/"):
                    page_num = path.split("/")[-1].split("?")[0]
                    svg_file = server.handle_get_svg_page(page_num)
                    if svg_file:
                        self._serve_file(svg_file, "image/svg+xml")
                    else:
                        self.send_error(404, "SVG page not found")
                elif path == "/api/mode":
                    self._serve_json(server.handle_get_mode())
                elif path == "/api/svg-meta":
                    self._serve_json(server.handle_get_svg_meta())
                elif path == "/api/layout-issues":
                    self._serve_json(server.handle_get_layout_issues())
                elif path == "/api/verification-status":
                    self._serve_json(server.handle_get_verification_status())
                elif path == "/api/designs":
                    include_full = query.get("full") == "true"
                    self._serve_json(server.handle_get_designs(include_full))
                elif path == "/api/variants":
                    self._serve_json(server.handle_get_variants())
                elif path == "/api/presets":
                    self._serve_json(server.handle_get_presets())
                elif path.startswith("/static/"):
                    rel = path[len("/static/"):]
                    static_dir = Path(__file__).resolve().parent.parent / "static"
                    file_path = (static_dir / rel).resolve()
                    if file_path.is_relative_to(static_dir) and file_path.is_file():
                        ctype, _ = mimetypes.guess_type(str(file_path))
                        self._serve_file(file_path, ctype or "application/octet-stream")
                    else:
                        self.send_error(404)
                elif path.startswith(("/assets/", "/chapters/", "/book/", "/.pdf-build/")):
                    file_path = server._project_path / path.lstrip("/")
                    if file_path.exists() and file_path.is_file():
                        ctype, _ = mimetypes.guess_type(str(file_path))
                        self._serve_file(file_path, ctype or "application/octet-stream")
                    else:
                        self.send_error(404)
                else:
                    self.send_error(404)

            def do_POST(self):
                parsed = urllib.parse.urlparse(self.path)
                path = urllib.parse.unquote(parsed.path)
                body = self._read_body()
                if body is None:
                    return
                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    self._serve_json({"error": "Invalid JSON"}, 400)
                    return

                routes = {
                    "/api/save": server.handle_post_save,
                    "/api/save-raw": server.handle_post_save_raw,
                    "/api/build-svg": server.handle_post_build_svg,
                    "/api/build-verified": server.handle_post_build_verified,
                    "/api/export-pdf": server.handle_post_export_pdf,
                    "/api/image-override": server.handle_post_image_override,
                    "/api/load-file": server.handle_post_load_file,
                    "/api/switch-mode": server.handle_post_switch_mode,
                    "/api/designs/save": server.handle_post_design_save,
                    "/api/designs/delete": server.handle_post_design_delete,
                    "/api/variants/save": server.handle_post_variant_save,
                    "/api/variants/delete": server.handle_post_variant_delete,
                    "/api/presets/save": server.handle_post_preset_save,
                    "/api/presets/update": server.handle_post_preset_update,
                    "/api/presets/delete": server.handle_post_preset_delete,
                    "/api/combine-md": server.handle_post_combine_md,
                    "/api/restage": server.handle_post_restage,
                }

                handler = routes.get(path)
                if handler:
                    try:
                        result = handler(data)
                        status = 200
                        if "error" in result and "ok" not in result:
                            status = 400
                        self._serve_json(result, status)
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        self._serve_json({"ok": False, "error": str(e)[-2000:]}, 500)
                else:
                    self.send_error(404)

            def _serve_file(self, file_path, content_type):
                try:
                    data = Path(file_path).read_bytes()
                    self.send_response(200)
                    self.send_header("Content-Type", content_type)
                    self.send_header("Content-Length", len(data))
                    self.send_header("Cache-Control", "no-cache")
                    self.end_headers()
                    self.wfile.write(data)
                except Exception:
                    self.send_error(500)

            def _serve_json(self, data, status=200):
                body = json.dumps(data, ensure_ascii=False).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", len(body))
                self.end_headers()
                self.wfile.write(body)

            def _read_body(self):
                length = int(self.headers.get("Content-Length", 0))
                if length == 0:
                    self._serve_json({"error": "Empty body"}, 400)
                    return None
                return self.rfile.read(length)

        return _RequestHandler


def _find_free_port(start: int = DEFAULT_PORT, tries: int = 10) -> int:
    for port in range(start, start + tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"포트 {start}~{start + tries - 1} 모두 사용 중")
