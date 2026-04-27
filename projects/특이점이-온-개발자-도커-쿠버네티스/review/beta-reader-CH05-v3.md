# Beta Reader 리포트: CH05 — Kubernetes 네트워킹 (v6)

## 프로젝트
- 대상 파일: `chapters-v2/05-Kubernetes-네트워킹-v6.md`
- 분량: 324줄 / 3개 절

## 페르소나 10명

| # | 이름 | 이야기 | 기술 | 실습 |
|---|------|:----:|:----:|:----:|
| 1 | 신입 백엔드 | 4 | **5** | 3 |
| 2 | 프론트엔드 | 4 | **5** | 4 |
| 3 | SI 개발자 | 3 | **5** | 4 |
| 4 | 데이터 엔지니어 | 4 | **5** | 3 |
| 5 | PM/기획자 | 3 | 4 | 4 (스킵 가능) |
| 6 | 비전공 전직자 | 4 | 4 | 3 |
| 7 | DevOps 주니어 | 4 | 4 | 3 |
| 8 | CS 학생 | 4 | 4 | 3 |
| 9 | CTO/시니어 | 4 | 4 | — |
| 10 | 게임 개발자 | 3 | 4 | 4 |

**평균**: 이야기 3.7/5 · 기술 4.4/5 · 실습 3.44/5

## 요약
- 통과: 10/10
- 공통 지적 4건 (3명 이상)
- 총평: **기술 평점 최고. 다만 Ingress 실습 부재 + 이야기 후반 얇음**

## 공통 피드백 (3명 이상)

| 영역 | 피드백 | 언급 | 심각도 |
|------|--------|------|--------|
| Ingress 실습 부재 | 5.2.3이 "다음 챕터 종합실습에서"로 끝. Ingress YAML 예제·접속 검증이 이 챕터에 없음. Service는 YAML 봤는데 Ingress는 안 보여줌 — "반쪽짜리" 인상 | 1, 2, 4, 5, 6, 7, 9 (7명) | **높음** |
| L4/L7 표 "JSON 파싱: 안 함/안 함" | 동어반복, 변별력 없음. "TLS 종료" "리라이트" 등 실제 차이점으로 교체 권장 | 4, 7, 8, 9 | 중 |
| 중반 기술 밀도 급등 | 5.1.4~5.1.7 kube-proxy/Endpoint Controller 밀도 올라가며 캐릭터 증발. 독자 숨참 | 1, 5, 6, 7 | 중 |
| 후반 캐릭터 부재 | 5.1.4 이후 오픈이 내면독백 희소, 교과서 톤 | 1, 2, 3, 5, 9 | 중 |

## 강점 (다수 언급)

| 강점 | 언급 |
|------|------|
| **5.1.2 "누구 입장의 포트" 표** — 이 책 최고의 표라는 평 | 1, 2, 3, 4, 5, 6, 7, 9, 10 (9명) |
| **5.3.2 Docker↔K8s 매핑 표** — CH02 원형 서사 회수 | 1, 2, 3, 4, 6, 7, 8, 10 |
| 5.3.1 "요청의 여정" 표 + "확인하는 것" 컬럼 | 1, 2, 5, 8, 10 |
| 대표 전화번호(Service) / 고속도로 분기점(L4) / 안내 데스크(L7) 비유 | 1, 2, 3, 6, 7, 8, 9, 10 |
| `minikube service --url` 터미널 점유 경고 | 1, 2, 4, 6 |
| ClusterIP "가상 주소" 한 줄 설명 | 1, 2, 8 |
| "같은 원리, 다른 규모" 카피 | 4, 7, 10 |

## 심각도별 이슈

### 높음
1. **Ingress 실습 부재** (7명) — `minikube addons enable ingress` + `kubectl get pods -n ingress-nginx`로 Controller 뜨는 것까지는 보여주거나, 간단한 Ingress YAML 스켈레톤(host/path/backend 3줄)이라도 미리보기 필요

### 중간
2. L4/L7 표 "JSON 파싱: 안 함/안 함" 삭제 or 변별 있는 행으로 교체
3. 5.1.6 kube-proxy/Endpoint Controller/iptables DNAT 3종 연속 밀도 → 중간 내면 독백/동료 대사 삽입
4. NodePort 30000~32767 범위 왜 이런지 (P10)
5. Endpoint vs EndpointSlice "하위호환" 한 줄 (P7, P9)
6. kube-proxy iptables vs IPVS/nftables 언제 어떤 모드 (P7)
7. DNAT 약어 첫 노출 시 "Destination NAT" 풀이 (P6)

### CTO/시니어 추가 지적 (P9)
- 이미지 경로 CH04/CH05 혼재 — 5장 본문인데 `ch4-service-*.png`, `selector-labels.png` 등 CH04 폴더 참조 → 자산 리네이밍 필요

### 특정 페르소나
- P1: LoadBalancer가 Minikube에서 `<pending>` 뜨는 이유 각주
- P3: 포트 3종 실제 패킷 흐름 시퀀스(외부:30080 → SVC:80 → Pod:80) 한 줄
- P8: `kubectl get endpoints`, `iptables -t nat -L | grep KUBE-` 직접 확인 실습
- P10: `sessionAffinity: ClientIP` 키워드 한 줄 (UDP 스티키 세션)

## 페르소나별 주요 반응

- **P1 신입 백엔드** (기술 5/5): "포트 3종 책상에 붙여두고 싶을 정도", "CH02 푸드코트가 여기서 다시 이름 갈아 돌아오는 원형 서사"
- **P2 프론트엔드** (이야기 4, 기술 5, 실습 4): "nginx location 블록 경험이 Ingress L7로 바로 연결", "NGINX→Ingress Controller 매핑 결정적"
- **P3 SI 10년** (기술 5, 이야기 3): "L4/L7 스위치 경험 = kube-proxy/Ingress 즉시 매핑"
- **P4 데이터 엔지니어** (기술 5): "Compose의 단순 포트 매핑에서 K8s 3포트로의 점프 완벽 흡수"
- **P7 DevOps**: "책갈피 대상 5.1.2/5.3.2 표" + "디버깅 명령(`describe svc`, `get endpoints`) 부재로 실무 감각 반 발짝 모자람"
- **P9 CTO**: "Docker↔K8s 매핑표가 이 챕터의 척추"

## 수정 제안 (우선순위순)

| # | 위치 | 제안 | 심각도 |
|---|------|------|--------|
| 1 | 5.2.3 Ingress 절 말미 | `minikube addons enable ingress` + `kubectl get pods -n ingress-nginx` 확인까지만이라도 실습 추가. Ingress 리소스 YAML 3줄 스켈레톤 미리보기 | 높음 |
| 2 | 5.2.2 L4/L7 표 | "JSON 파싱: 안 함/안 함" 행 제거 또는 "TLS 종료" / "URL 경로 라우팅" 등 변별력 있는 항목으로 교체 | 중 |
| 3 | 5.1.6 중간 | 오픈이 내면 독백 1~2개 추가 (밀도 완화) | 중 |
| 4 | 5.1.6 DNAT 첫 노출 | "DNAT = Destination NAT, 목적지 주소 변환" 풀이 한 줄 | 중 |
| 5 | 5.1.5 LoadBalancer | Minikube에서 `<pending>` 현상 한 줄 각주 | 중 |
| 6 | 이미지 자산 | `ch4-service-*.png` 등 CH05 본문인데 CH04 폴더 참조하는 이미지 → CH05로 리네이밍 | 중 |
| 7 | 5.1.6 각주 | EndpointSlice가 기본이 된 이유 (Endpoints의 O(N) 리스트 성능) 한 줄 | 낮 |
| 8 | 5.1.6 참고박스 | kube-proxy iptables vs IPVS 선택 기준 한 줄 (대규모 Service 시 IPVS) | 낮 |

## 결론
- **기술 평점 4.4 — 챕터 중 최고**
- Ingress 실습 최소 미리보기만 보강하면 "반쪽" 인상 해소
- 5.1.2 포트 표, 5.3.2 매핑 표는 이 책의 하이라이트 (거의 전원 칭찬)
- P9 CTO 추천 의향 확정
