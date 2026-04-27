#!/usr/bin/env python3
"""Mermaid flowchart → D2 변환기.

프로젝트 챕터의 Mermaid 코드블록을 D2 문법으로 변환한다.
지원 범위: flowchart LR/TD, graph TB/LR (단순 flowchart만)

사용법:
    # 단일 .mmd 파일 변환
    python3 mermaid_to_d2.py input.mmd output.d2

    # 마크다운에서 Mermaid 블록 추출 + 일괄 변환
    python3 mermaid_to_d2.py --extract chapters/01-시작.md --outdir assets/CH01/diagram/

    # stdin → stdout
    echo '...' | python3 mermaid_to_d2.py -
"""
from __future__ import annotations

import argparse
import re
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

# ── D2 classes 템플릿 (프로젝트 기본 디자인) ────────────────────────────
D2_CLASSES = textwrap.dedent("""\
    classes: {
      start-end: {
        shape: oval
        style: {
          fill: "#ffffff"
          stroke: "#c5cee0"
          stroke-width: 2
          shadow: true
          font-size: 18
          font-color: "#374151"
        }
        width: 150
        height: 70
      }
      process: {
        shape: rectangle
        style: {
          fill: "#eef2ff"
          font-color: "#1e40af"
          stroke: "#2563eb"
          stroke-width: 2
          border-radius: 8
          shadow: true
          font-size: 18
          bold: true
        }
        width: 150
        height: 60
      }
      danger: {
        shape: oval
        style: {
          fill: "#ffffff"
          stroke: "#c5cee0"
          stroke-width: 2
          shadow: true
          font-size: 18
          font-color: "#374151"
          bold: true
        }
        width: 150
        height: 70
      }
      success: {
        shape: oval
        style: {
          fill: "#ffffff"
          stroke: "#c5cee0"
          stroke-width: 2
          shadow: true
          font-size: 18
          font-color: "#374151"
          bold: true
        }
        width: 150
        height: 70
      }
      storage: {
        shape: cylinder
        style: {
          fill: "#f8fafc"
          stroke: "#c5cee0"
          stroke-width: 2
          shadow: true
          font-size: 18
          font-color: "#374151"
          bold: true
        }
        width: 140
        height: 80
      }
      decision: {
        shape: diamond
        style: {
          fill: "#ffffff"
          stroke: "#2563eb"
          stroke-width: 2
          shadow: true
          font-size: 16
          font-color: "#374151"
          bold: true
        }
        width: 120
        height: 80
      }
      step: {
        shape: rectangle
        style: {
          fill: "#ffffff"
          stroke: "#2563eb"
          stroke-width: 2
          border-radius: 8
          shadow: true
          font-size: 20
          font-color: "#374151"
          bold: true
        }
        width: 220
        height: 70
      }
      group-box: {
        style: {
          stroke: "#2563eb"
          stroke-width: 2
          stroke-dash: 5
          fill: "#ffffff"
          font-size: 22
          bold: true
          font-color: "#1e3a5f"
        }
      }
    }""")

ARROW_STYLE = '  style: { stroke: "#2563eb"; stroke-width: 2 }'


# ── 데이터 모델 ────────────────────────────────────────────────────────

@dataclass
class Node:
    id: str
    label: str
    shape: str = "rectangle"  # rectangle, diamond, cylinder
    d2_class: str = "process"


@dataclass
class Edge:
    src: str
    dst: str
    label: str = ""


@dataclass
class Subgraph:
    id: str
    title: str
    node_ids: list[str] = field(default_factory=list)


@dataclass
class MermaidGraph:
    direction: str = "right"
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    subgraphs: list[Subgraph] = field(default_factory=list)
    class_assignments: dict[str, str] = field(default_factory=dict)
    # Mermaid classDef name → D2 class name
    class_defs: dict[str, str] = field(default_factory=dict)


# ── 파서 ───────────────────────────────────────────────────────────────

def _clean_label(text: str) -> str:
    """Mermaid 라벨의 HTML 태그를 D2 호환으로 변환."""
    text = re.sub(r'<br\s*/?>', r'\\n', text)
    text = text.replace('"', '')
    return text.strip()


def _detect_d2_class(node_id: str, label: str, shape: str,
                     class_assignments: dict[str, str],
                     class_defs: dict[str, str]) -> str:
    """노드의 D2 class를 추론."""
    # 1) 명시적 class 지정 확인
    if node_id in class_assignments:
        mermaid_class = class_assignments[node_id]
        if mermaid_class in class_defs:
            return class_defs[mermaid_class]
        # 이름이 D2 class와 직접 매칭
        if mermaid_class in ("danger", "success", "process", "storage",
                             "decision", "step", "start-end", "group-box"):
            return mermaid_class

    # 2) 다이아몬드 형태
    if shape == "diamond":
        return "decision"

    # 3) 라벨 기반 추론
    lower = label.lower()
    if any(kw in lower for kw in ("db", "벡터", "데이터베이스", "저장")):
        return "storage"
    if any(kw in lower for kw in ("질문", "답변", "출처")):
        return "start-end"

    return "process"


# 노드 정의 패턴들
# A["label"], A[label], A{"label"}, A{label}, A(("label"))
_RE_NODE_BRACKET = re.compile(
    r'([A-Za-z_][\w]*)\s*'
    r'(?:'
    r'\["([^"]*?)"\]'       # ["label"]
    r'|\[([^\]]*?)\]'       # [label]
    r'|\{"([^"]*?)"\}'      # {"label"} diamond
    r'|\{([^}]*?)\}'        # {label} diamond
    r'|\(\("([^"]*?)"\)\)'  # (("label")) circle
    r'|\(\(([^)]*?)\)\)'    # ((label)) circle
    r')'
)

# 노드 ID + 선택적 괄호 정의를 건너뛰는 패턴
_NODE_WITH_OPT_BRACKET = (
    r'([A-Za-z_][\w]*)'
    r'(?:\s*(?:\["[^"]*"\]|\[[^\]]*\]|\{"[^"]*"\}|\{[^}]*\}|\(\("[^"]*"\)\)|\(\([^)]*\)\)))?'
)

# 엣지 패턴: A["x"] --> B["y"], A -->|label| B, A -- "label" --> B
_RE_EDGE = re.compile(
    _NODE_WITH_OPT_BRACKET + r'\s+'
    r'(?:'
    r'-->\s*\|([^|]*)\|\s*'       # -->|label|
    r'|--\s*"([^"]*)"\s*-->\s*'   # -- "label" -->
    r'|-->\s*'                     # -->
    r'|-+\s*"([^"]*)"\s*-+>\s*'   # -- "label" -->  (variant)
    r')\s*'
    + _NODE_WITH_OPT_BRACKET
)

# 체인 엣지 계속 패턴: --> NODE (앞에 src 없이, 문자열 시작부터 매칭)
_RE_CHAIN_CONT = re.compile(
    r'\s*(?:'
    r'-->\s*\|([^|]*)\|\s*'       # -->|label|
    r'|--\s*"([^"]*)"\s*-->\s*'   # -- "label" -->
    r'|-->\s*'                     # -->
    r'|-+\s*"([^"]*)"\s*-+>\s*'   # -- "label" --> (variant)
    r')\s*'
    + _NODE_WITH_OPT_BRACKET
)

# subgraph 패턴
_RE_SUBGRAPH = re.compile(
    r'subgraph\s+(\w+)\s*\["?([^"\]]*)"?\]', re.IGNORECASE
)
_RE_SUBGRAPH_SIMPLE = re.compile(
    r'subgraph\s+(\w+)', re.IGNORECASE
)

# classDef 패턴
_RE_CLASSDEF = re.compile(
    r'classDef\s+(\w+)\s+(.+)', re.IGNORECASE
)

# class 지정 패턴: class A1 danger 또는 class A1,A2 danger
_RE_CLASS_ASSIGN = re.compile(
    r'class\s+([\w,\s]+?)\s+(\w+)', re.IGNORECASE
)

# 방향 감지
_RE_DIRECTION = re.compile(
    r'(?:flowchart|graph)\s+(LR|RL|TD|TB|BT)', re.IGNORECASE
)


def _map_classdef_to_d2(name: str, style_str: str) -> str:
    """Mermaid classDef의 fill 색상을 기반으로 D2 class 이름 추론."""
    lower = style_str.lower()
    if "ffb6c1" in lower or "ff6b6b" in lower or "dc143c" in lower:
        return "danger"
    if "90ee90" in lower or "98fb98" in lower or "2ecc71" in lower:
        return "success"
    if name.lower() == "danger":
        return "danger"
    if name.lower() == "success":
        return "success"
    if name.lower() == "default":
        return "process"
    return "process"


def _register_node_from_line(line: str, node_id: str,
                              graph: MermaidGraph,
                              current_subgraph: Subgraph | None) -> None:
    """엣지에 포함된 노드를 graph.nodes에 등록."""
    if node_id in graph.nodes:
        if current_subgraph and node_id not in current_subgraph.node_ids:
            current_subgraph.node_ids.append(node_id)
        return
    for nm in _RE_NODE_BRACKET.finditer(line):
        if nm.group(1) == node_id:
            raw_label = (nm.group(2) or nm.group(3) or nm.group(4)
                         or nm.group(5) or nm.group(6) or nm.group(7) or "")
            shape = "diamond" if (nm.group(4) is not None or nm.group(5) is not None) else "rectangle"
            graph.nodes[node_id] = Node(
                id=node_id,
                label=_clean_label(raw_label) if raw_label else node_id,
                shape=shape,
            )
            if current_subgraph and node_id not in current_subgraph.node_ids:
                current_subgraph.node_ids.append(node_id)
            return
    graph.nodes[node_id] = Node(id=node_id, label=node_id)
    if current_subgraph and node_id not in current_subgraph.node_ids:
        current_subgraph.node_ids.append(node_id)


def parse_mermaid(code: str) -> MermaidGraph:
    """Mermaid flowchart 코드를 파싱."""
    graph = MermaidGraph()
    lines = code.strip().splitlines()

    current_subgraph: Subgraph | None = None

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("%%"):
            continue

        # 방향 감지
        m = _RE_DIRECTION.match(line)
        if m:
            d = m.group(1).upper()
            graph.direction = "right" if d in ("LR",) else "down" if d in ("TD", "TB") else "left" if d == "RL" else "up"
            continue

        # subgraph
        m = _RE_SUBGRAPH.match(line)
        if m:
            sg = Subgraph(id=m.group(1), title=m.group(2).strip())
            graph.subgraphs.append(sg)
            current_subgraph = sg
            continue
        m = _RE_SUBGRAPH_SIMPLE.match(line)
        if m and "end" not in line.lower().split():
            sg = Subgraph(id=m.group(1), title=m.group(1))
            graph.subgraphs.append(sg)
            current_subgraph = sg
            continue

        if line.lower() == "end":
            current_subgraph = None
            continue

        # classDef
        m = _RE_CLASSDEF.match(line)
        if m:
            name, style_str = m.group(1), m.group(2)
            graph.class_defs[name] = _map_classdef_to_d2(name, style_str)
            continue

        # class assignment
        m = _RE_CLASS_ASSIGN.match(line)
        if m:
            node_ids_str, class_name = m.group(1), m.group(2)
            for nid in re.split(r'[,\s]+', node_ids_str.strip()):
                nid = nid.strip()
                if nid:
                    graph.class_assignments[nid] = class_name
            continue

        # ~~~ (invisible link) — skip
        if "~~~" in line:
            continue

        # 엣지 파싱 — 체인 엣지 지원 (A --> B --> C → 2개 엣지)
        m = _RE_EDGE.search(line)
        if m:
            src_id = m.group(1)
            label = m.group(2) or m.group(3) or m.group(4) or ""
            dst_id = m.group(5)
            graph.edges.append(Edge(src=src_id, dst=dst_id, label=_clean_label(label)))
            _register_node_from_line(line, src_id, graph, current_subgraph)
            _register_node_from_line(line, dst_id, graph, current_subgraph)

            # 체인 계속: B --> C --> D ...
            remaining = line[m.end():]
            prev_dst = dst_id
            while remaining.strip():
                cm = _RE_CHAIN_CONT.match(remaining)
                if not cm:
                    break
                chain_label = cm.group(1) or cm.group(2) or cm.group(3) or ""
                chain_dst = cm.group(4)
                graph.edges.append(Edge(src=prev_dst, dst=chain_dst, label=_clean_label(chain_label)))
                _register_node_from_line(line, chain_dst, graph, current_subgraph)
                prev_dst = chain_dst
                remaining = remaining[cm.end():]
            continue

        # 독립 노드 정의 (엣지 없이)
        for nm in _RE_NODE_BRACKET.finditer(line):
            node_id = nm.group(1)
            if node_id.lower() in ("subgraph", "end", "classDef", "class",
                                     "flowchart", "graph", "style", "linkStyle"):
                continue
            raw_label = nm.group(2) or nm.group(3) or nm.group(4) or nm.group(5) or nm.group(6) or nm.group(7) or ""
            shape = "diamond" if (nm.group(4) is not None or nm.group(5) is not None) else "rectangle"
            if node_id not in graph.nodes:
                graph.nodes[node_id] = Node(
                    id=node_id,
                    label=_clean_label(raw_label) if raw_label else node_id,
                    shape=shape,
                )
            if current_subgraph and node_id not in current_subgraph.node_ids:
                current_subgraph.node_ids.append(node_id)

    # D2 class 할당
    for nid, node in graph.nodes.items():
        node.d2_class = _detect_d2_class(
            nid, node.label, node.shape,
            graph.class_assignments, graph.class_defs,
        )

    return graph


# ── D2 코드 생성 ──────────────────────────────────────────────────────

# D2 라벨에 따옴표가 필요한 특수 문자
_D2_SPECIAL = re.compile(r'[|@#/{};:\'"]')


def _d2_quote_label(label: str) -> str:
    """D2 라벨에 특수문자가 있으면 따옴표로 감싸기."""
    if "\\n" in label or _D2_SPECIAL.search(label):
        return f'"{label}"'
    return label


def _d2_node_line(node: Node, indent: str = "") -> str:
    """D2 노드 정의 한 줄 생성."""
    label_str = _d2_quote_label(node.label)
    return f'{indent}{node.id}: {label_str} {{\n{indent}  class: {node.d2_class}\n{indent}}}'


def _d2_edge_line(edge: Edge, indent: str = "") -> str:
    """D2 엣지 정의 생성."""
    if edge.label:
        quoted = _d2_quote_label(edge.label)
        label_part = f": {quoted} "
    else:
        label_part = ": "
    return (
        f'{indent}{edge.src} -> {edge.dst}{label_part}{{\n'
        f'{indent}{ARROW_STYLE}\n'
        f'{indent}}}'
    )


def generate_d2(graph: MermaidGraph) -> str:
    """파싱된 MermaidGraph를 D2 코드 문자열로 변환."""
    parts: list[str] = []

    # 방향
    parts.append(f"direction: {graph.direction}")
    parts.append("")

    # classes
    parts.append(D2_CLASSES)
    parts.append("")

    # subgraph에 속하는 노드 ID 수집
    subgraph_node_ids: set[str] = set()
    for sg in graph.subgraphs:
        subgraph_node_ids.update(sg.node_ids)

    # 루트 레벨 노드 (subgraph에 속하지 않는)
    for nid, node in graph.nodes.items():
        if nid not in subgraph_node_ids:
            parts.append(_d2_node_line(node))
            parts.append("")

    # subgraph → D2 블록
    for sg in graph.subgraphs:
        quoted_title = _d2_quote_label(sg.title)
        parts.append(f"{sg.id}: {quoted_title} {{")
        parts.append(f"  class: group-box")
        parts.append(f"  direction: {graph.direction}")
        parts.append("")
        for nid in sg.node_ids:
            if nid in graph.nodes:
                parts.append(_d2_node_line(graph.nodes[nid], indent="  "))
                parts.append("")
        # subgraph 내부 엣지
        sg_set = set(sg.node_ids)
        for edge in graph.edges:
            if edge.src in sg_set and edge.dst in sg_set:
                parts.append(_d2_edge_line(edge, indent="  "))
        parts.append("}")
        parts.append("")

    # 루트 레벨 엣지 (subgraph 내부가 아닌)
    for sg in graph.subgraphs:
        sg_set = set(sg.node_ids)
        for edge in graph.edges:
            if edge.src in sg_set and edge.dst in sg_set:
                pass  # 이미 출력됨

    # subgraph에 속하지 않는 엣지 또는 subgraph 간 엣지
    subgraph_internal: set[tuple[str, str, str]] = set()
    for sg in graph.subgraphs:
        sg_set = set(sg.node_ids)
        for edge in graph.edges:
            if edge.src in sg_set and edge.dst in sg_set:
                subgraph_internal.add((edge.src, edge.dst, edge.label))

    # 노드 → 서브그래프 소속 매핑 (크로스 서브그래프 엣지용)
    node_to_sg: dict[str, str] = {}
    for sg in graph.subgraphs:
        for nid in sg.node_ids:
            node_to_sg[nid] = sg.id

    for edge in graph.edges:
        if (edge.src, edge.dst, edge.label) not in subgraph_internal:
            # 크로스 서브그래프 엣지: fully-qualified 경로 사용
            q_src = f"{node_to_sg[edge.src]}.{edge.src}" if edge.src in node_to_sg else edge.src
            q_dst = f"{node_to_sg[edge.dst]}.{edge.dst}" if edge.dst in node_to_sg else edge.dst
            parts.append(_d2_edge_line(Edge(src=q_src, dst=q_dst, label=edge.label)))

    # 끝
    parts.append("")
    return "\n".join(parts)


# ── 마크다운에서 Mermaid 블록 추출 ────────────────────────────────────

def extract_mermaid_blocks(md_path: Path) -> list[tuple[int, str]]:
    """마크다운 파일에서 ```mermaid 코드블록을 추출.

    Returns: [(블록_인덱스, mermaid_코드), ...]
    """
    content = md_path.read_text(encoding="utf-8")
    blocks: list[tuple[int, str]] = []
    pattern = re.compile(r'```mermaid\s*\n(.*?)```', re.DOTALL)
    for i, m in enumerate(pattern.finditer(content)):
        blocks.append((i + 1, m.group(1)))
    return blocks


# ── CLI ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mermaid flowchart → D2 변환기",
    )
    parser.add_argument("input", nargs="?", default="-",
                        help=".mmd 파일 경로 또는 - (stdin)")
    parser.add_argument("output", nargs="?", default=None,
                        help=".d2 출력 경로 (생략 시 stdout)")
    parser.add_argument("--extract", metavar="MD_FILE",
                        help="마크다운에서 Mermaid 블록 추출")
    parser.add_argument("--outdir", metavar="DIR",
                        help="--extract 시 출력 디렉토리")
    parser.add_argument("--prefix", default="diagram",
                        help="--extract 시 파일 접두사 (default: diagram)")
    args = parser.parse_args()

    if args.extract:
        md_path = Path(args.extract)
        if not md_path.exists():
            print(f"Error: {md_path} not found", file=sys.stderr)
            sys.exit(1)
        blocks = extract_mermaid_blocks(md_path)
        if not blocks:
            print(f"No mermaid blocks found in {md_path}", file=sys.stderr)
            sys.exit(0)
        outdir = Path(args.outdir) if args.outdir else md_path.parent
        outdir.mkdir(parents=True, exist_ok=True)
        for idx, code in blocks:
            graph = parse_mermaid(code)
            d2_code = generate_d2(graph)
            out_file = outdir / f"{args.prefix}_{idx:02d}.d2"
            out_file.write_text(d2_code, encoding="utf-8")
            print(f"  [{idx}] → {out_file}")
        print(f"\n{len(blocks)} block(s) converted.")
    else:
        if args.input == "-":
            code = sys.stdin.read()
        else:
            code = Path(args.input).read_text(encoding="utf-8")
        graph = parse_mermaid(code)
        d2_code = generate_d2(graph)
        if args.output:
            Path(args.output).write_text(d2_code, encoding="utf-8")
            print(f"Converted → {args.output}")
        else:
            print(d2_code)


if __name__ == "__main__":
    main()
