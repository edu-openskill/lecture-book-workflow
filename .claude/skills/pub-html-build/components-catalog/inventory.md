# 컴포넌트 인벤토리

챕터에서 실제 사용된 HTML 컴포넌트와 마크다운 directive 전수. `components-catalog/` 카테고리 문서의 원본 데이터.

## 출처

- CSS: `.claude/skills/pub-html-build/styles/{components.css, print.css}`
- 챕터: `projects/사내AI비서_v2/chapters/0[1-9]-*.md`, `10-*.md` (10개)

## Directive (Markdown 확장)

| Directive | 출현 횟수 | 담당 카테고리 |
|----------|----------|-------------|
| `:::term-box` | 15 | boxes |
| `:::tip` | 13 | boxes |
| `:::remember` | 10 | boxes |
| `:::goal` | 10 | boxes |
| `::::prep` | 9 | boxes |
| `:::note` | 3 | boxes |
| `:::preview` | 1 | boxes (거의 미사용) |

## CSS 클래스 카테고리

### boxes
박스형 블록. `:::`/`::::` directive의 렌더 결과.

- `.goal-box`, `.gl`
- `.prep-section`, `.prep-header`, `.prep-header-title`, `.prep-header-meta`, `.prep-body`, `.prep-item`, `.prep-item-title`, `.prep-note`, `.prep-section-md`
- `.term-box`
- `.remember`
- `.tip`
- `.change-note`, `.preview-notice`
- `.result`, `.result.fail`, `.result.ok`

### fullmap
책 전체 구성도.

- `.arch-fullmap`, `.arch-fullmap-title`
- `.afm-row` (+ `.afm-user`, `.afm-three`, `.afm-ext`)
- `.afm-box` (+ `.afm-faint`, `.afm-on`, `.afm-dashed`, `.afm-round`)
- `.afm-zone`, `.afm-zone-ch`, `.afm-zone-label`
- `.afm-tag`, `.afm-label`, `.afm-sub`, `.afm-note`

### cards
개별 카드 단위.

- `.chunk-with-meta` + `.cwm-title`, `.cwm-card`, `.cwm-body`, `.cwm-meta`, `.cwm-tag`, `.cwm-note` (CH04)
- `.embed-example-row` + `.eer-card`, `.eer-group` (`.similar`/`.different`), `.eer-group-label` (`.good`/`.bad`), `.eer-item`, `.eer-text`, `.eer-vec`, `.eer-image`, `.eer-caption` (CH04)

### comparisons
비교형 시각 요소.

- `.annotated-compare` + `.ac-heading`, `.ac-block` (`.llm`/`.truth`), `.ac-label`, `.ac-name`, `.ac-tech`, `.ac-content`, `.ac-strike`, `.ac-note` (CH01)
- `.overlap-text-demo` + `.otd-row` (`.otd-original`), `.otd-label` (`.c1`/`.c2`/`.c3`), `.otd-arrow`, `.otd-note`, `.otd-text` (CH03)
- `.reindex-compare` + `.rc-arrow`, `.rc-badge-full`, `.rc-badge-inc` (CH03) — **주의**: CH07의 `.rc-timeline`과 같은 `rc-*` 접두어지만 별도 컴포넌트
- `.cache-diff` (CH07)
- `.dual-image` + `figure`/`figcaption` (CH04)

### pipelines
흐름/타임라인/파이프라인.

- `.rag-pipeline-box`, `.rag-pipeline-title`, `.rag-pipeline`, `.rag-step`, `.s-num`, `.s-title`, `.s-desc`, `.s-meta`, `.rag-arrow` (CH01)
- `.rc-timeline` (CH07) — CH03 reindex-compare의 `rc-*`와 네임스페이스 충돌 주의
- `.ec-cabinet` (CH07)
- `.wrapper-arch` (CH07)
- `.journey-forward`, `.jf-group`, `.jf-group-label`, `.jf-items`, `.jf-item`, `.jf-part-desc`, `.jf-ch`, `.jf-title`, `.jf-sub`, `.jf-hint`, `.jf-desc` (CH01 여정 맵)
- `.journey-roadmap`, `.roadmap-line`, `.roadmap-part`, `.roadmap-node`, `.node-dot`, `.node-icon`, `.node-title`, `.node-story` (CH01)

### captions
인라인 라벨/캡션/태그.

- `.caption`
- `.eer-caption`, `.cwm-note`
- `.afm-tag`, `.afm-zone-ch`, `.afm-zone-label`, `.afm-note`
- `.rl-caption` (CH06 ReAct 루프)
- Markdown 이탤릭 캡션 규칙: `*그림 N-N. 설명*` (전자책은 Typst 미경유라 수동 번호 유지)

### 보조 / 글로벌
특정 카테고리에 속하지 않지만 전역 사용.

- `.dialogue`, `.speaker`, `.thought` (대사·내면독백)
- `.term` (용어 강조)
- `.chapter-minimap`, `.minimap-label`, `.minimap-boxes`, `.mm-box`, `.mm-arrow`, `.minimap-note` (챕터 미니맵)
- `.arch-tree`, `.at-root`, `.at-root-icon/name/desc`, `.at-part`, `.at-branch`, `.at-line`, `.at-folder`, `.at-part-tag`, `.at-children`, `.at-leaf`, `.at-file`, `.at-file-desc`, `.at-ch` (아키텍처 트리)
- `.api-tag`, `.rag-tag`, `.agent-tag`, `.tune-tag` (태그 뱃지)
- `.num-badge`

## 챕터별 주요 사용 분포

| 챕터 | 주요 컴포넌트 |
|-----|--------------|
| CH01 | journey-forward, journey-roadmap, annotated-compare, rag-pipeline-box |
| CH02 | arch-fullmap (이하 CH03~CH10 공통) |
| CH03 | overlap-text-demo, reindex-compare |
| CH04 | chunk-with-meta, embed-example-row, dual-image |
| CH05 | (주로 rag chain 코드 + fullmap) |
| CH06 | rl-caption, arch-fullmap (ReAct 시퀀스) |
| CH07 | rc-timeline, ec-cabinet, wrapper-arch, cache-diff |
| CH08~10 | arch-fullmap 주로 |

## 주의사항 (네임스페이스)

- `rc-*` 접두어 **중복 사용**:
  - CH03: `reindex-compare` (재인덱싱 비교) — `rc-arrow`, `rc-badge-full`, `rc-badge-inc`
  - CH07: `rc-timeline` (타임라인) — `rc-*` 서브 클래스
  - 신규 컴포넌트 생성 시 `rc-*` 접두어 재사용 금지. 고유 접두어 확보 필요.
- `s-*` 접두어는 `rag-pipeline` 내부 step 전용.
