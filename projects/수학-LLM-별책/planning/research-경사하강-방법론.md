# 조사 — 경사하강 최적화 방법론 (8강 설계용)

> 작성: 2026-06-28 · 트리거: 저자 질문 "골짜기 여러 개·보폭 조절·함정 회피 방법 조사"
> **결정**: 이 내용은 **8강(경사하강법)** 에 쓴다. 5강(미분)은 무관($f'(x)=0$ 분석적 바닥찾기까지만).
> 의도 필터(seed-v2): "필요한 만큼만, 대신 직접 풀어서 확실히." → 손풀이 불가능한 엔지니어링은 비유·이름만.

---

## 1. 지형(문제) 정리

| 지형 | 정체 | 비유 |
|------|------|------|
| 볼록(convex) | 골짜기·바닥 하나 | 1강의 매끈한 그릇 |
| 비볼록(non-convex) | 골짜기 여러 개 | 울퉁불퉁한 산맥 = 실제 신경망 손실 |
| 지역 최솟값(local minima) | 주변보단 낮지만 전체 바닥 아님 | 산속 옹달샘 |
| 안장점(saddle point) | 기울기 0이나 한 방향 내리막/다른 방향 오르막 | 말안장 한가운데 |
| 평지(plateau) | 기울기≈0이라 잘 안 움직임 | 끝없는 고원 |

**고차원의 반전**: 변수 수백만 개면 모든 방향이 동시에 오르막인 진짜 지역 최솟값은 천문학적으로 드묾 → 대부분 정체점은 **안장점**(한 방향만 내리막이면 탈출 가능). 그래서 실전에서 "골짜기 함정"은 통념보다 덜 치명적이고, 대부분 바닥이 비슷하게 좋다 = 딥러닝이 작동하는 이유 중 하나.

## 2. 방법들 (문제별)

- **A. 보폭 = 학습률(η)**: 크면 튕김/발산, 작으면 느림. 스케줄링(warmup→cosine decay; 통상 앞 5% warmup + 95% cosine).
- **B. 관성 = 모멘텀**: 무거운 공이 관성으로 얕은 웅덩이 넘고 진동 감쇠.
- **C. 무작위성 = SGD/mini-batch**: 표본으로 기울기 추정 → 노이즈가 안장점·얕은 함정에서 "툭" 쳐 빠져나오게 함.
- **D. 적응적 보폭 = RMSprop/Adam/AdamW**: 좌표마다 보폭 자동조절. **Adam ≈ 모멘텀 + RMSprop + 보정**, **AdamW = Adam + 가중치 감쇠 분리**. LLM 표준 = AdamW.
- **E. 재시작/점프 = warm restarts·simulated annealing**: 가끔 보폭 확 키워 갇힌 곳 탈출.

## 3. 저자 직관 점검

| 직관 | 판정 | 메모 |
|------|------|------|
| "골짜기 여러 개" | ✅ | 비볼록=local minima. 고차원엔 안장점이 더 흔함 |
| "보폭 조절" | ✅ 핵심 | learning rate + scheduling |
| "전체를 한번에 큰 보폭으로 함정 회피" | ⚠️ 반 교정 | **큰 보폭(η)** 으로 얕은 함정 건너뛰기는 맞음. 그러나 "**전체를 한번에**(full-batch)"는 노이즈 없어 더 잘 갇힘 → 함정 회피는 반대로 **표본 조금씩(SGD)+노이즈**가 핵심 |

## 4. 책 스코프 매핑 (확정)

| 주제 | 위치 | 깊이 | 근거 |
|------|------|------|------|
| 보폭 η, 반복 갱신 $\theta \leftarrow \theta - \eta\nabla L$ | **8강 본문** | 정식 + 손풀이 | 경사하강 심장, 직접 풀이 가능 |
| local minima·안장점 "함정" | **8강 직관 한 컷** | 비유·그림만 | 동기엔 필요, 손풀이는 과함 |
| 모멘텀 | **8강 "더 알아보기" / 칼럼** | 비유·이름만 | 무거운 공 직관은 좋으나 수식은 곁가지 |
| Adam·RMSprop·스케줄링 | **8강 "더 알아보기" 한 줄** | 이름만 | 엔지니어링, 손풀이 불가 → 정체성 충돌 |
| 안장점 탈출 이론·SGDR·고차원 분석 | **범위 밖(이연)** | — | PCA처럼 향후 ML/DL 수학 책 |

## 5. 8강 집필 지침 (요약)

1. 본문 줄기: 1강(바닥)+4강(기울기)+5강(미분) 합류 → $\theta \leftarrow \theta - \eta \nabla L$ 반복. worked example로 1변수 직접 굴려보기.
2. 보폭 η 한 컷: 너무 크면 튕김 / 너무 작으면 굼벵이 (그림 1).
3. "함정" 한 컷: 골짜기 여러 개 + 안장점 비유, "고차원에선 대부분 빠져나갈 수 있다"는 위안 (그림 1, 손풀이 없음).
4. "더 알아보기": 모멘텀(무거운 공)·SGD(표본 노이즈로 함정 탈출)·Adam(LLM 표준)을 **이름+비유 3~4줄**. 수식 전개 금지.
5. 끝의 "AI 어디 쓰이나": 이게 L8 역전파에서 가중치 갱신 규칙으로 그대로 재등장.

## 출처
- saddle vs local minima — https://www.tensortonic.com/ml-math/calculus/local-vs-saddle
- escaping saddle points (arXiv) — https://arxiv.org/html/2409.12604v1
- non-convex optimization review (arXiv) — https://arxiv.org/pdf/2410.02017
- cosine LR schedule — https://mbrenndoerfer.com/writing/cosine-learning-rate-schedule-decay-restarts-warmup
- LR scheduling (d2l) — https://d2l.ai/chapter_optimization/lr-scheduler.html
- optimizers from scratch — https://amaarora.github.io/posts/2021-03-13-optimizers.html
- Adam vs SGD vs RMSprop — https://metricgate.com/blogs/adam-vs-sgd-vs-rmsprop-optimizer/
