"""검증 루프 — build→check→auto-fix→rebuild 사이클

최대 3라운드 실행. 자동 수정 가능한 이슈만 처리하고,
수동 이슈는 UI에 보고한다.
"""

from __future__ import annotations

import time
from pathlib import Path

from models import BuildResult, DesignState, LayoutIssue, VerificationResult
from build_pipeline import BuildPipeline
from layout_checker import LayoutChecker


class VerificationLoop:
    """build → layout check → auto-fix → rebuild 사이클.

    최대 MAX_ROUNDS 라운드. 매 라운드:
    1. PDF 컴파일
    2. 레이아웃 분석
    3. 자동수정 가능 이슈 → ImageRegistry 오버라이드
    4. Stage 2 재조립 → .typ 저장
    5. 반복

    수동 이슈는 수집하여 최종 결과에 포함.
    """

    MAX_ROUNDS = 3

    def __init__(self, pipeline: BuildPipeline, checker: LayoutChecker):
        self._pipeline = pipeline
        self._checker = checker

    def run(
        self,
        typ_path: Path,
        pdf_path: Path,
        raw_typ: str,
        design_state: DesignState,
        svg_dir: Path | None = None,
    ) -> VerificationResult:
        """검증 루프 실행.

        Args:
            typ_path: .typ 파일 경로 (매 라운드 덮어씀)
            pdf_path: PDF 출력 경로
            raw_typ: Stage 1 결과 (불변)
            design_state: 현재 디자인 설정
            svg_dir: SVG 출력 디렉토리 (있으면 마지막 라운드에서 SVG도 생성)

        Returns:
            VerificationResult
        """
        start = time.time()
        all_auto_fixed: list[LayoutIssue] = []
        round_number = 0
        final_issues: list[LayoutIssue] = []
        page_count = 0

        for round_num in range(1, self.MAX_ROUNDS + 1):
            round_number = round_num

            # 1. PDF 컴파일
            ok = self._pipeline.compile_pdf(typ_path, pdf_path)
            if not ok:
                return VerificationResult(
                    round_number=round_num,
                    build_result=BuildResult(
                        success=False,
                        error="PDF 컴파일 실패",
                        duration=time.time() - start,
                    ),
                )

            # 2. 레이아웃 분석
            issues = self._checker.analyze(pdf_path)
            if not issues:
                final_issues = []
                break

            # 3. 분류
            auto_fixable, manual = self._checker.classify_issues(issues)
            final_issues = issues

            if not auto_fixable:
                break  # 자동 수정 가능한 것 없음

            # 4. 수정 제안 생성
            images = self._pipeline.image_registry.get_all()
            auto_fixable = self._checker.suggest_fixes(auto_fixable, images)

            # 5. 수정 적용
            applied = self._apply_fixes(auto_fixable)
            all_auto_fixed.extend(applied)

            # 6. Stage 2 재조립
            final_typ = self._pipeline.assemble_final_typ(
                raw_typ, design_state
            )
            typ_path.write_text(final_typ, encoding="utf-8")

        # 최종 SVG 생성 (있으면)
        if svg_dir:
            page_count = self._pipeline.compile_svg(typ_path, svg_dir)

        # 최종 분류
        _, manual_remaining = self._checker.classify_issues(final_issues)

        duration = time.time() - start
        return VerificationResult(
            round_number=round_number,
            issues=final_issues,
            auto_fixed=all_auto_fixed,
            manual_remaining=manual_remaining,
            build_result=BuildResult(
                success=True,
                typ_path=typ_path,
                pdf_path=pdf_path,
                svg_dir=svg_dir,
                page_count=page_count,
                duration=duration,
                stage_run=2,
                images_detected=self._pipeline.image_registry.get_all(),
            ),
        )

    def _apply_fixes(self, issues: list[LayoutIssue]) -> list[LayoutIssue]:
        """자동 수정 액션을 ImageRegistry에 적용. 적용된 이슈 목록 반환."""
        registry = self._pipeline.image_registry
        applied = []

        for issue in issues:
            if issue.fix_action == "reduce_image_width" and issue.image_path:
                step = 0.1 if issue.issue_type == "large_image" else 0.05
                new_width = registry.reduce_image_width(
                    issue.image_path, step=step
                )
                issue.target_width = new_width
                applied.append(issue)

            elif issue.fix_action == "reduce_nearby_image" and issue.image_path:
                new_width = registry.reduce_image_width(
                    issue.image_path, step=0.05
                )
                issue.target_width = new_width
                applied.append(issue)

            elif issue.fix_action == "remove_pagebreak":
                # pagebreak 제거는 .typ 텍스트 수준 수정이 필요
                # 현재는 이미지 크기 조정만 자동화
                pass

        return applied
