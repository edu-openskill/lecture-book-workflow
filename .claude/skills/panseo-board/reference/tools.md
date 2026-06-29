# 판서보드 엔진 내부 구조 (참고용 — 수정하지 말 것)

엔진은 `template/board_template.html`의 `<script>` 한 곳에 들어 있다. 강의별로는 `STEPS`와 강조색만 바꾼다.

## 데이터 모델 — 벡터 획(stroke)
판서는 픽셀이 아니라 **획 객체 배열**로 저장된다.

```
stroke = { color, size, erase:false, pts:[{x, y, p}, ...] }   // p = 필압
```

- 손을 내릴 때(pointerdown)부터 뗄 때(pointerup)까지 = **한 획 = 객체 하나**.
- 화면은 `render()`가 이 배열을 다시 그려서 표시한다(`drawStroke`).
- 슬라이드마다(`slideStrokes[i]`)·판서모드(`boardStrokes`) 별로 배열이 따로 있어 왕복해도 유지된다.
- 창 크기 변경 시 벡터라 다시 선명하게 렌더된다(`fit(true)` → `render()`).

## 선택 / 이동
- `pickStroke(p)`: 클릭 지점에서 **가장 가까운 한 획**(거리 ≤ 12+굵기)을 위에서부터 찾는다. → 겹친 다른 획은 안 잡힘.
- `liftStrokes(idxs)`: 고른 획(들)을 배열에서 빼서 떠 있는 상태로. 끌어 옮긴 뒤 `commitFloat()`이 좌표를 더해 다시 배열에 넣는다.
- ✂선택은 사각형에 닿는 획들을, ✋이동은 누른 한 획을 들어올린다.
- 이동 모드에선 커서가 `grab`/`grabbing`으로 바뀐다.

## 지우개 (파괴적)
- 라이브로는 `destination-out`으로 지워 보여주고, 손을 떼면 `applyErase(path)`가 **경로 근처(반경 ≈ 굵기×1.7)의 점을 실제로 잘라내** 획을 여러 조각으로 분할한다.
- 즉 지운 부분은 데이터에서 사라지므로, 그 획을 이동해도 복원되지 않는다.

## 되돌리기
- `snapshot()` = 현재 획 배열의 얕은 복사를 스택에 저장(획 추가·이동·지우기·전체지움 직전).
- `doUndo()` = 스택에서 꺼내 레이어 교체 후 `render()`. 한 동작 = 한 번 되돌리기.

## 단축키
`b` 판서모드 · `g` 모눈 · `e` 지우개 · `c` 전체지움 · `s` 도형스냅 on/off · `f` 전체화면 · `Esc` 이동조각 고정 · `Ctrl/Cmd+Z` 되돌리기 · `←→`/`PageUp/Down` 슬라이드.

## 도형 스냅 (draw-and-hold, v2)
`pointerdown/move/up`에 정지 타이머(`holdArm/holdTrack/holdCancel`)를 달아, 그리다 ~0.6초 멈추면 `trySnap`이 발동한다. 먼저 한 획을 `recognizeShape`(직선·사각형·원/타원·삼각형)로 보고, 실패하면 `clusterFrom`으로 가까이 이어진 획들을 모아 `cloudRect`/`cloudEllipse`(점구름 인식)로 합친다. 직선은 수평/수직 ±`SNAP_DEG`(10°)면 축으로 교정. 결과는 점 배열로 생성되어 선택·이동·지우개와 그대로 호환. 파라미터: `HOLD_MS=600`, `HOLD_MOVE=5`, `SNAP_DEG=10`, `GAP=28`.

## 태블릿
좌상단 `⛶` 버튼이 `requestFullscreen()`(webkit 포함)을 토글한다. 갤럭시탭 등은 키보드를 꽂아도 F11이 안 되고, 사용자가 화면을 탭했을 때만 전체화면이 허용되기 때문. 펜 판서 중 오작동을 막으려 화면 전체가 아니라 **작은 코너 버튼에만** 건다.
