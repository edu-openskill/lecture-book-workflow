# 챕터 5. Kubernetes 네트워킹

오픈이는 지금까지 학습한 내용을 바탕으로 테스트 서버를 Pod로 재구성했습니다. Pod가 종료되더라도 Deployment가 즉시 새 Pod를 실행해 주니 마음이 든든했습니다.

다음 날 아침, 동료가 찾아왔습니다.

**동료**: "오픈 씨, 어제 테스트 서버에 올렸다는 서비스, 접속이 안 되는데 어떻게 들어가요?"

오픈이는 당황했습니다. 로그상으로는 정상 실행 중이었지만, 정작 브라우저로 접속해 본 적은 없었기 때문입니다. 서둘러 Pod 목록에서 IP를 확인해 브라우저에 입력해 보았지만, 페이지는 열리지 않았습니다.

![Pod는 떠 있는데 접근할 주소가 없던 아침](../assets/CH05/gemini/01_prologue-no-fixed-address.png)

*그림 5-1. Pod는 떠 있는데 접근할 주소가 없던 아침*

게다가 Pod가 재생성될 때마다 IP가 바뀌니, IP로는 접근할 수도 없었습니다.

*'쿠버네티스 환경에서는 외부에서 Pod로 어떻게 접속해야 하지?'*

막막해진 오픈이가 선배에게 묻자, 선배가 화면을 보며 설명했습니다.

**선배**: "외부 요청이 실제 Pod까지 도달하려면 두 가지가 필요해요. 들어온 요청을 도메인이나 경로에 따라 알맞은 곳으로 보내 주는 **Ingress**, 그리고 수시로 바뀌는 Pod를 묶어 고정된 진입점을 제공하는 **Service**죠. 이 두 가지를 한번 알아봐요."

<div class="svg-figure svg-figure--wide">
<svg viewBox="0 0 1200 540" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="요청이 Pod까지 도달하는 전체 흐름 — 1·2단계와 컨트롤 플레인이 위쪽 가로로, 3단계가 아래쪽에 두 컬럼(order/stores)으로 평행">
  <defs>
    <marker id="ov-a" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#1f2937"/></marker>
    <marker id="ov-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#94a3b8"/></marker>
  </defs>
  <text x="600" y="24" text-anchor="middle" font-size="17" font-weight="700" fill="#1f2937">전체 흐름 한눈에 — 세 단계가 일어나는 위치</text>
  <rect x="20" y="180" width="130" height="80" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="85" y="226" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">클라이언트</text>
  <rect x="200" y="70" width="980" height="460" rx="10" fill="none" stroke="#475569" stroke-width="1.4" stroke-dasharray="6,4"/>
  <text x="690" y="92" text-anchor="middle" font-size="14" font-style="italic" fill="#1f2937">Kubernetes 클러스터</text>
  <rect x="220" y="110" width="320" height="230" rx="8" fill="#fffaf0" stroke="#fed7aa" stroke-width="1"/>
  <text x="380" y="128" text-anchor="middle" font-size="16" font-weight="700" fill="#7b341e">1단계 외부 진입 <tspan font-size="12" fill="#94a3b8" font-weight="600">[L4]</tspan> <tspan font-size="13" fill="#7b341e" font-weight="700">· Service(NodePort)</tspan></text>
  <rect x="240" y="180" width="140" height="80" rx="8" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="310" y="207" text-anchor="middle" font-size="17" font-weight="700" fill="#7b341e">NodePort</text>
  <text x="310" y="227" text-anchor="middle" font-size="15" font-family="monospace" fill="#7b341e">:30080</text>
  <text x="310" y="247" text-anchor="middle" font-size="14" fill="#7b341e">각 노드의 외부 포트</text>
  <line x1="150" y1="220" x2="238" y2="220" stroke="#1f2937" stroke-width="1.4" marker-end="url(#ov-a)"/>
  <line x1="380" y1="220" x2="398" y2="220" stroke="#1f2937" stroke-width="1.4" marker-end="url(#ov-a)"/>
  <rect x="400" y="195" width="120" height="50" rx="6" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="460" y="216" text-anchor="middle" font-size="15" font-weight="700" fill="#7b341e">kube-proxy</text>
  <text x="460" y="233" text-anchor="middle" font-size="14" fill="#7b341e">iptables DNAT</text>
  <line x1="520" y1="220" x2="558" y2="220" stroke="#1f2937" stroke-width="1.4" marker-end="url(#ov-a)"/>
  <rect x="560" y="110" width="340" height="230" rx="8" fill="#fffaf0" stroke="#fed7aa" stroke-width="1"/>
  <text x="730" y="128" text-anchor="middle" font-size="16" font-weight="700" fill="#7b341e">2단계 정밀 분류 <tspan font-size="12" fill="#94a3b8" font-weight="600">[L7]</tspan> <tspan font-size="13" fill="#7b341e" font-weight="700">· Ingress</tspan></text>
  <rect x="600" y="155" width="260" height="60" rx="6" fill="#fff" stroke="#ff7849" stroke-width="2.4"/>
  <text x="730" y="178" text-anchor="middle" font-size="15" font-weight="700" fill="#7b341e">Ingress Controller</text>
  <text x="730" y="196" text-anchor="middle" font-size="14" fill="#7b341e">URL·도메인으로 Service 결정</text>
  <line x1="690" y1="215" x2="630" y2="266" stroke="#1f2937" stroke-width="1.4" marker-end="url(#ov-a)"/>
  <line x1="770" y1="215" x2="830" y2="266" stroke="#1f2937" stroke-width="1.4" marker-end="url(#ov-a)"/>
  <text x="565" y="265" text-anchor="middle" font-size="14" font-weight="600" fill="#7b341e">ClusterIP</text>
  <rect x="565" y="270" width="130" height="38" rx="19" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="630" y="294" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">order-service</text>
  <text x="895" y="265" text-anchor="middle" font-size="14" font-weight="600" fill="#7b341e">ClusterIP</text>
  <rect x="765" y="270" width="130" height="38" rx="19" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="830" y="294" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">stores-service</text>
  <rect x="920" y="125" width="240" height="190" rx="6" fill="#f8fafc" fill-opacity="0.5" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="5,3"/>
  <text x="1040" y="142" text-anchor="middle" font-size="13" font-style="italic" fill="#1f2937">컨트롤 플레인 (백그라운드)</text>
  <rect x="940" y="155" width="200" height="50" rx="4" fill="#fff" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="1040" y="174" text-anchor="middle" font-size="14" font-weight="600" fill="#475569">EndpointSlice Controller</text>
  <text x="1040" y="193" text-anchor="middle" font-size="11" fill="#1f2937">Pod 변동 감시 → Pod 목록 갱신</text>
  <rect x="940" y="232" width="200" height="50" rx="4" fill="#fff" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="1040" y="251" text-anchor="middle" font-size="14" font-weight="600" fill="#475569">API Server</text>
  <text x="1040" y="270" text-anchor="middle" font-size="11" fill="#1f2937">Ingress·Service·EndpointSlice 정보</text>
  <line x1="1025" y1="205" x2="1025" y2="230" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3,2" marker-end="url(#ov-s)"/>
  <text x="1010" y="223" font-size="14" font-style="italic" fill="#1f2937" text-anchor="end">갱신</text>
  <line x1="1055" y1="230" x2="1055" y2="205" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3,2" marker-end="url(#ov-s)"/>
  <line x1="938" y1="252" x2="860" y2="218" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3,2" marker-end="url(#ov-s)"/>
  <rect x="220" y="360" width="940" height="160" rx="8" fill="#fffaf0" stroke="#fed7aa" stroke-width="1"/>
  <text x="240" y="378" font-size="16" font-weight="700" fill="#7b341e">3단계 내부 분배 <tspan font-size="12" fill="#94a3b8" font-weight="600">[L4]</tspan> <tspan font-size="13" fill="#7b341e" font-weight="700">· Service(ClusterIP)</tspan></text>
  <line x1="630" y1="308" x2="630" y2="394" stroke="#1f2937" stroke-width="1.4" marker-end="url(#ov-a)"/>
  <line x1="830" y1="308" x2="830" y2="394" stroke="#1f2937" stroke-width="1.4" marker-end="url(#ov-a)"/>
  <rect x="565" y="398" width="130" height="44" rx="6" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="630" y="418" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">kube-proxy</text>
  <text x="630" y="434" text-anchor="middle" font-size="14" fill="#7b341e">iptables DNAT</text>
  <rect x="765" y="398" width="130" height="44" rx="6" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="830" y="418" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">kube-proxy</text>
  <text x="830" y="434" text-anchor="middle" font-size="14" fill="#7b341e">iptables DNAT</text>
  <line x1="630" y1="442" x2="630" y2="460" stroke="#1f2937" stroke-width="1.4" marker-end="url(#ov-a)"/>
  <line x1="830" y1="442" x2="830" y2="460" stroke="#1f2937" stroke-width="1.4" marker-end="url(#ov-a)"/>
  <rect x="565" y="476" width="130" height="34" rx="6" fill="none" stroke="#ff7849" stroke-width="1.4" stroke-dasharray="4,3"/>
  <rect x="572" y="482" width="56" height="22" rx="11" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="600" y="497" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">Pod A1</text>
  <rect x="632" y="482" width="56" height="22" rx="11" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="660" y="497" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">Pod A2</text>
  <rect x="765" y="476" width="130" height="34" rx="6" fill="none" stroke="#ff7849" stroke-width="1.4" stroke-dasharray="4,3"/>
  <rect x="772" y="482" width="56" height="22" rx="11" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="800" y="497" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">Pod B1</text>
  <rect x="832" y="482" width="56" height="22" rx="11" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="860" y="497" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">Pod B2</text>
  <line x1="937" y1="285" x2="893" y2="398" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3,2" marker-end="url(#ov-s)"/>
</svg>
</div>

*그림 5-2. 챕터 5 한눈에 보기 - 요청이 Pod까지 도달하는 전체 흐름*

::::prep
**실습 준비**. 예제 코드

이 책의 실습 코드는 GitHub 레포 하나에 챕터별 폴더로 담겨 있습니다. 아래 명령으로 레포를 한 번 git clone 합니다. 이후 챕터마다 해당 폴더로 이동해 실습합니다.

```bash [터미널] 예제 코드 클론
git clone https://github.com/metacoding-10-linux-docker/start
```

이번 챕터는 `ex11`~`ex12` 폴더를 사용합니다.

완성된 코드는 아래 주소에서 확인하세요.

```bash [터미널] 완성 코드
https://github.com/metacoding-10-linux-docker/final
```
::::

## 5.1 Service - Pod의 고정 주소

### 5.1.1 Service가 필요한 이유

Pod의 IP는 고정된 값이 아닙니다. Pod는 종료되거나 새 버전으로 교체될 때마다 새로 만들어지고, 그때마다 IP가 바뀝니다. 게다가 같은 역할을 하는 Pod를 여러 개 띄워 두면, 요청을 그중 어디로 보낼지도 정해야 합니다.

**Service**는 이 문제를 해결합니다. Pod IP가 바뀌어도 변하지 않는 **고정 진입점**을 만들고, 들어온 요청을 **연결된 여러 Pod**에 **분배**하는 리소스입니다.

<div class="svg-figure">
<svg viewBox="0 0 760 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="외부 요청이 Service를 거쳐 클러스터 안 여러 Pod로 분배되는 구조">
  <defs>
    <marker id="sv-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <rect x="20" y="100" width="130" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="85" y="135" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">외부 요청</text>
  <text x="85" y="158" text-anchor="middle" font-size="10" fill="#6b7280">브라우저·클라이언트</text>
  <line x1="150" y1="140" x2="198" y2="140" stroke="#475569" stroke-width="1.8" marker-end="url(#sv-p)"/>
  <text x="174" y="132" text-anchor="middle" font-size="10" fill="#6b7280" font-style="italic">요청</text>
  <rect x="190" y="30" width="510" height="225" rx="10" fill="none" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="6,4"/>
  <text x="205" y="20" font-size="11" font-weight="700" fill="#7b341e">Kubernetes 클러스터</text>
  <rect x="200" y="100" width="180" height="80" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="290" y="135" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">Service</text>
  <text x="290" y="158" text-anchor="middle" font-size="11" fill="#7b341e">고정 진입점</text>
  <line x1="380" y1="125" x2="505" y2="68" stroke="#475569" stroke-width="1.8" marker-end="url(#sv-p)"/>
  <line x1="380" y1="140" x2="505" y2="140" stroke="#475569" stroke-width="1.8" marker-end="url(#sv-p)"/>
  <line x1="380" y1="155" x2="505" y2="212" stroke="#475569" stroke-width="1.8" marker-end="url(#sv-p)"/>
  <text x="445" y="134" text-anchor="middle" font-size="10" fill="#6b7280" font-style="italic">분배</text>
  <rect x="510" y="40" width="180" height="55" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="600" y="62" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Pod 1</text>
  <text x="600" y="80" text-anchor="middle" font-size="11" font-family="monospace" fill="#6b7280">10.0.0.5</text>
  <rect x="510" y="115" width="180" height="55" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="600" y="137" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Pod 2</text>
  <text x="600" y="155" text-anchor="middle" font-size="11" font-family="monospace" fill="#6b7280">10.0.0.9</text>
  <rect x="510" y="190" width="180" height="55" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="600" y="212" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Pod 3</text>
  <text x="600" y="230" text-anchor="middle" font-size="11" font-family="monospace" fill="#6b7280">10.0.0.12</text>
</svg>
</div>

*그림 5-3. Service는 Pod IP가 바뀌어도 변하지 않는 고정 주소를 제공*

### 5.1.2 Service 생성

이제 Pod에 연결할 Service를 직접 만들어 보겠습니다.

실습 코드는 `ex11` 폴더에 있습니다. 이전 챕터에서 사용한 `deploy-ex02.yml`을 사용합니다.

```text
ex11/
├── deploy-ex02.yml    # nginx Pod 4개를 유지하는 Deployment 정의
├── service-ex01.yml   # Pod 앞에 붙이는 NodePort Service 정의
└── README.md          # 실습 안내
```

다음은 Service를 정의한 YAML입니다.

```yaml [실습 1] ex11/service-ex01.yml. NodePort Service 정의
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort        # 노드 IP와 포트로 외부 접근이 가능한 타입
  selector:
    app: nginx          # 이 라벨을 가진 Pod들을 뒤에 연결
  ports:
    - port: 80          # 클러스터 내부에서 Service로 진입하는 포트
      targetPort: 80    # Service가 Pod로 요청을 전달하는 포트
      nodePort: 30080   # 외부에서 노드로 진입할 때 사용하는 포트 (기본 허용 범위 30000~32767)
```

Service는 **Deployment**와 마찬가지로 **selector**에 지정한 라벨과 일치하는 Pod를 골라 연결합니다.

<div class="svg-figure">
<svg viewBox="0 0 760 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Service의 selector(app: nginx)와 같은 라벨을 가진 Pod만 골라 매칭하고, 라벨이 다른 Pod는 제외하는 구조">
  <defs>
    <marker id="sl-svc" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">selector — 같은 라벨을 가진 Pod만 매칭</text>
  <rect x="40" y="80" width="220" height="100" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <path d="M 48 80 L 252 80 Q 260 80 260 88 L 260 106 L 40 106 L 40 88 Q 40 80 48 80 Z" fill="#ff7849"/>
  <text x="150" y="99" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">Service</text>
  <text x="150" y="135" text-anchor="middle" font-size="11" font-weight="600" fill="#7b341e">selector</text>
  <text x="150" y="163" text-anchor="middle" font-size="14" font-family="monospace" font-weight="700" fill="#7b341e">app: nginx</text>
  <path d="M 260 115 Q 380 70, 510 55" fill="none" stroke="#ff7849" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#sl-svc)"/>
  <path d="M 260 135 Q 380 135, 510 135" fill="none" stroke="#ff7849" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#sl-svc)"/>
  <rect x="510" y="25" width="220" height="60" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="525" y="48" font-size="12" font-weight="700" fill="#7b341e">Pod 1</text>
  <text x="525" y="71" font-size="13" font-family="monospace" fill="#7b341e">labels: </text>
  <text x="585" y="71" font-size="13" font-family="monospace" font-weight="700" fill="#7b341e">app: nginx</text>
  <text x="722" y="48" text-anchor="end" font-size="11" font-weight="700" fill="#ff7849">선택</text>
  <rect x="510" y="105" width="220" height="60" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="525" y="128" font-size="12" font-weight="700" fill="#7b341e">Pod 2</text>
  <text x="525" y="151" font-size="13" font-family="monospace" fill="#7b341e">labels: </text>
  <text x="585" y="151" font-size="13" font-family="monospace" font-weight="700" fill="#7b341e">app: nginx</text>
  <text x="722" y="128" text-anchor="end" font-size="11" font-weight="700" fill="#ff7849">선택</text>
  <rect x="510" y="185" width="220" height="60" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.4" stroke-dasharray="4,3"/>
  <text x="525" y="208" font-size="12" font-weight="700" fill="#94a3b8">Pod 3</text>
  <text x="525" y="231" font-size="13" font-family="monospace" fill="#94a3b8">labels: </text>
  <text x="585" y="231" font-size="13" font-family="monospace" font-weight="700" fill="#94a3b8">app: db</text>
  <text x="722" y="208" text-anchor="end" font-size="11" font-weight="700" fill="#94a3b8">제외</text>
</svg>
</div>

*그림 5-4. selector가 지정한 라벨(app: nginx)을 가진 Pod만 매칭하고 다른 라벨은 제외*

### 5.1.3 Service 타입과 접근 범위

앞서 작성한 Service YAML에는 `type: NodePort` 설정이 있습니다. Service는 접근 범위에 따라 타입이 **ClusterIP**, **NodePort**, **LoadBalancer**로 나뉩니다.

#### ClusterIP

**ClusterIP**는 사내에서만 연결되는 **내선 번호**입니다. **클러스터 안의 Pod끼리는 서로 연결되지만, 외부에서는 접근할 수 없습니다.** DB처럼 외부에 노출할 필요가 없는 구성에 적합하며, 서비스 타입의 기본값입니다.

<div class="svg-figure">
<svg viewBox="0 0 760 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ClusterIP — 외부 접근은 차단되고 클러스터 내부 Pod끼리만 통신하는 구조">
  <defs>
    <marker id="cip-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
    <marker id="cip-x" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#dc2626"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">ClusterIP — 클러스터 안에서만 통신</text>
  <rect x="20" y="100" width="130" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="85" y="125" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">클라이언트</text>
  <text x="85" y="145" text-anchor="middle" font-size="10" fill="#6b7280">브라우저·외부 PC</text>
  <line x1="150" y1="130" x2="270" y2="130" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#cip-x)"/>
  <g transform="translate(210,130)">
    <circle r="14" fill="#fff" stroke="#dc2626" stroke-width="2"/>
    <line x1="-7" y1="-7" x2="7" y2="7" stroke="#dc2626" stroke-width="2.4"/>
    <line x1="-7" y1="7" x2="7" y2="-7" stroke="#dc2626" stroke-width="2.4"/>
  </g>
  <text x="210" y="172" text-anchor="middle" font-size="10" font-style="italic" fill="#b91c1c">접근 차단</text>
  <rect x="290" y="50" width="450" height="190" rx="10" fill="#fff" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="6,4"/>
  <text x="305" y="71" font-size="11" font-weight="700" fill="#7b341e">Kubernetes 클러스터</text>
  <rect x="305" y="100" width="120" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="365" y="125" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">내부 Pod</text>
  <text x="365" y="145" text-anchor="middle" font-size="10" fill="#6b7280">호출자</text>
  <line x1="425" y1="130" x2="475" y2="130" stroke="#475569" stroke-width="1.8" marker-end="url(#cip-p)"/>
  <rect x="475" y="100" width="130" height="60" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="540" y="123" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Service</text>
  <text x="540" y="143" text-anchor="middle" font-size="10" font-family="monospace" fill="#7b341e">ClusterIP</text>
  <line x1="605" y1="120" x2="650" y2="100" stroke="#475569" stroke-width="1.6" marker-end="url(#cip-p)"/>
  <line x1="605" y1="140" x2="650" y2="180" stroke="#475569" stroke-width="1.6" marker-end="url(#cip-p)"/>
  <rect x="650" y="80" width="80" height="50" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="690" y="110" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">Pod A</text>
  <rect x="650" y="170" width="80" height="50" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="690" y="200" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">Pod B</text>
</svg>
</div>

*그림 5-5. ClusterIP는 외부 요청은 닿지 못하고 내부 Pod끼리만 통신*

#### NodePort

**NodePort**는 외부에서도 연결할 수 있는 **직통 번호**입니다. Service를 NodePort로 지정하면, **노드(서버)에 외부와 통하는 포트가 열립니다.** 외부에서 그 노드의 IP와 포트로 접속하면, 요청이 클러스터 안의 Service를 거쳐 Pod로 전달됩니다.

<div class="svg-figure">
<svg viewBox="0 0 760 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="NodePort — 노드 IP의 특정 포트(30080)를 통해 외부에서 Service로 접근하는 구조">
  <defs>
    <marker id="np-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">NodePort — 노드 IP의 특정 포트로 외부 접근 허용</text>
  <rect x="20" y="100" width="130" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="85" y="125" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">클라이언트</text>
  <text x="85" y="145" text-anchor="middle" font-size="10" font-family="monospace" fill="#6b7280">노드IP:30080</text>
  <rect x="195" y="50" width="555" height="160" rx="10" fill="#fff" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="6,4"/>
  <text x="210" y="71" font-size="11" font-weight="700" fill="#7b341e">Kubernetes 클러스터</text>
  <line x1="150" y1="130" x2="220" y2="130" stroke="#475569" stroke-width="1.8" marker-end="url(#np-p)"/>
  <rect x="220" y="100" width="130" height="60" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2.4"/>
  <text x="285" y="124" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">NodePort</text>
  <text x="285" y="144" text-anchor="middle" font-size="11" font-family="monospace" fill="#7b341e">:30080</text>
  <line x1="350" y1="130" x2="400" y2="130" stroke="#475569" stroke-width="1.8" marker-end="url(#np-p)"/>
  <rect x="400" y="100" width="130" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="465" y="123" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Service</text>
  <text x="465" y="143" text-anchor="middle" font-size="10" font-family="monospace" fill="#6b7280">ClusterIP</text>
  <line x1="530" y1="120" x2="585" y2="95" stroke="#475569" stroke-width="1.6" marker-end="url(#np-p)"/>
  <line x1="530" y1="140" x2="585" y2="165" stroke="#475569" stroke-width="1.6" marker-end="url(#np-p)"/>
  <rect x="585" y="70" width="120" height="50" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="645" y="100" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">Pod A</text>
  <rect x="585" y="150" width="120" height="50" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="645" y="180" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">Pod B</text>
</svg>
</div>

*그림 5-6. NodePort는 노드의 특정 포트로 외부 접근을 허용*

#### LoadBalancer

**LoadBalancer**는 외부 요청을 한곳에서 받아 연결하는 **대표 번호**입니다. Service를 LoadBalancer로 지정하면, AWS·GCP 같은 클라우드 플랫폼이 **공인 IP**를 발급합니다. **그 IP로 들어온 모든 요청을 받아, 뒤에 있는 여러 노드에 분산합니다.** 실제 운영에서 가장 흔히 사용합니다.

<div class="svg-figure">
<svg viewBox="0 0 760 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LoadBalancer — 공인 IP가 각 노드의 NodePort로 직접 트래픽을 분산하고, Service는 Pod 집합을 라벨로 묶는 논리 리소스">
  <defs>
    <marker id="lb-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">LoadBalancer — 공인 IP 하나로 여러 노드에 분산</text>
  <rect x="150" y="60" width="100" height="34" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="200" y="82" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">User 1</text>
  <rect x="150" y="118" width="100" height="34" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="200" y="140" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">User 2</text>
  <rect x="150" y="176" width="100" height="34" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="200" y="198" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">User 3</text>
  <line x1="250" y1="77" x2="303" y2="120" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <line x1="250" y1="135" x2="303" y2="140" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <line x1="250" y1="193" x2="303" y2="165" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <rect x="305" y="100" width="140" height="90" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8" stroke-dasharray="6,4"/>
  <text x="375" y="125" text-anchor="middle" font-size="11" font-weight="600" fill="#7b341e">클라우드 (AWS, GCP 등)</text>
  <text x="375" y="148" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">LoadBalancer</text>
  <text x="375" y="172" text-anchor="middle" font-size="10" font-family="monospace" fill="#7b341e">공인 IP</text>
  <rect x="500" y="40" width="170" height="250" rx="10" fill="#fff" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="5,3"/>
  <text x="513" y="58" font-size="11" font-weight="700" fill="#7b341e">Kubernetes 클러스터</text>
  <line x1="445" y1="120" x2="508" y2="107" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <line x1="445" y1="145" x2="508" y2="180" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <line x1="445" y1="170" x2="508" y2="253" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <rect x="510" y="75" width="150" height="65" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="525" y="93" font-size="10" font-weight="700" fill="#0f172a">Node 1</text>
  <rect x="560" y="95" width="80" height="32" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="600" y="115" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Pod</text>
  <rect x="510" y="148" width="150" height="65" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="525" y="166" font-size="10" font-weight="700" fill="#0f172a">Node 2</text>
  <rect x="560" y="168" width="80" height="32" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="600" y="188" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Pod</text>
  <rect x="510" y="221" width="150" height="65" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="525" y="239" font-size="10" font-weight="700" fill="#0f172a">Node 3</text>
  <rect x="560" y="241" width="80" height="32" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="600" y="261" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Pod</text>
</svg>
</div>

*그림 5-7. LoadBalancer는 클라우드가 공인 IP를 발급해 여러 노드에 분산*

LoadBalancer 타입은 ClusterIP와 NodePort를 함께 포함합니다. 그래서 Service 하나로 내부 통신과 외부 접근이 모두 처리됩니다.

### 5.1.4 포트 흐름

Service YAML의 포트 설정에는 `port`, `targetPort`, `nodePort` 세 종류가 있습니다. 각 포트는 외부에서 들어온 요청을 Pod까지 단계별로 전달합니다.

외부 사용자가 노드의 `nodePort`로 접속하면, 요청은 `port`로 열려 있는 Service에 도달하고, Service는 이를 Pod의 `targetPort`로 전달합니다.

<div class="svg-figure">
<svg viewBox="0 0 760 420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="노드 큰 박스 안에 NodePort, Service, Pod가 있고 외부 사용자가 NodePort로 진입해 Service를 거쳐 Pod 안 컨테이너에 도달하는 구조">
  <defs>
    <marker id="nps-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
    <marker id="nps-o" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2937">노드 안의 NodePort, Service, Pod</text>
  <rect x="0" y="180" width="130" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="65" y="208" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">외부 사용자</text>
  <text x="65" y="228" text-anchor="middle" font-size="10" fill="#6b7280">브라우저</text>
  <rect x="220" y="60" width="520" height="340" rx="12" fill="#fff" stroke="#475569" stroke-width="2.4" stroke-dasharray="6,4"/>
  <text x="240" y="84" font-size="13" font-weight="700" fill="#475569">Node (워커 노드)</text>
  <rect x="240" y="158" width="120" height="104" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <rect x="252" y="178" width="96" height="64" rx="6" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="300" y="205" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">NodePort</text>
  <text x="300" y="228" text-anchor="middle" font-size="13" font-family="monospace" font-weight="700" fill="#7b341e">:30080</text>
  <text x="300" y="254" text-anchor="middle" font-size="9" fill="#7b341e">각 노드의 외부 포트</text>
  <rect x="420" y="115" width="200" height="90" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <path d="M 360 195 Q 385 170, 430 152" fill="none" stroke="#475569" stroke-width="1.8" marker-end="url(#nps-d)"/>
  <text x="520" y="146" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">Service</text>
  <line x1="435" y1="160" x2="605" y2="160" stroke="#fde4d3" stroke-width="0.8"/>
  <text x="520" y="187" text-anchor="middle" font-size="15" font-family="monospace" font-weight="700" fill="#7b341e">:80 (port)</text>
  <line x1="520" y1="205" x2="520" y2="252" stroke="#475569" stroke-width="2" marker-end="url(#nps-d)"/>
  <rect x="420" y="258" width="200" height="125" rx="8" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <text x="435" y="278" font-size="11" font-weight="700" fill="#475569">Pod</text>
  <rect x="445" y="295" width="160" height="78" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.4"/>
  <text x="520" y="320" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">컨테이너</text>
  <text x="520" y="350" text-anchor="middle" font-size="14" font-family="monospace" font-weight="700" fill="#0f6f3f">:80 (targetPort)</text>
  <line x1="130" y1="210" x2="237" y2="210" stroke="#ff7849" stroke-width="2.6" marker-end="url(#nps-o)"/>
  <text x="190" y="200" text-anchor="middle" font-size="12" font-family="monospace" font-weight="700" fill="#7b341e">노드IP:30080</text>
</svg>
</div>

*그림 5-8. NodePort에서 Service를 거쳐 Pod 컨테이너까지 이어지는 포트 흐름*

| 포트 종류 | 위치 | 역할 | 생략 시 |
|:--------:|:-----|:-----|:-------|
| `nodePort` | 워커 노드 | 외부 사용자가 노드 IP로 클러스터 내부에 접근할 때 열리는 포트 | 30000~32767 범위에서 자동 할당. 같은 범위로 직접 지정도 가능 |
| `port` | Service | 클러스터 내부의 다른 Pod가 이 Service를 호출할 때 쓰는 포트 | 생략 불가 (필수) |
| `targetPort` | Pod(컨테이너) | Service가 받은 트래픽을 전달할 컨테이너의 수신 포트 (컨테이너 포트와 일치) | 생략 시 `port`와 같은 값 |

### 5.1.5 외부에서 Service 접속해 보기

이제 실습을 해 보겠습니다. 아래 명령어를 실행해 클러스터에 적용한 뒤, 외부에서 실제로 접속되는지 확인합니다.

```bash [터미널] Pod와 Service 생성
kubectl apply -f ex11/deploy-ex02.yml    # Pod 4개 생성
kubectl apply -f ex11/service-ex01.yml   # Service YAML 적용
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-key">$</span> <span class="tl-str">kubectl apply -f ex11/deploy-ex02.yml</span></div>
    <div>deployment.apps/nginx-replica created</div>
    <div><span class="tl-key">$</span> <span class="tl-str">kubectl apply -f ex11/service-ex01.yml</span></div>
    <div>service/nginx-service created</div>
  </div>
</div>

*그림 5-9. Pod와 Service 생성 결과*

브라우저를 열고 NodePort로 설정한 30080 포트(`localhost:30080`)로 접속합니다. 그런데 연결할 수 없다는 화면이 뜹니다.

*'분명 30080 포트를 열었는데 왜 안 들어가지.'*

:::note
**NodePort로 접속이 안 되는 이유**

미니큐브는 내 컴퓨터 안에 작은 가상 환경을 만들고, 그 안에서 클러스터를 실행합니다. 이 가상 환경은 별개의 PC처럼 동작해서, 내 컴퓨터와 다른 네트워크를 가집니다. 그래서 NodePort를 열어도 `localhost` 주소로는 접근할 수 없습니다.
:::

이 문제를 해결하기 위해, 미니큐브에는 내 컴퓨터와 클러스터를 연결하는 별도의 명령어가 있습니다.

<table>
  <thead>
    <tr>
      <th style="width:15%">방법</th>
      <th style="width:50%">명령어</th>
      <th style="width:35%">설명</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:center">URL 생성</td>
      <td style="white-space:nowrap"><code>minikube service &lt;서비스이름&gt; --url</code></td>
      <td><strong>Service 한 개에 접근할 임시 URL 생성</strong>. NodePort 접근에 사용</td>
    </tr>
    <tr>
      <td style="text-align:center">터널 개방</td>
      <td style="white-space:nowrap"><code>minikube tunnel</code></td>
      <td><strong>LoadBalancer·Ingress에 외부 IP 부여</strong>. LoadBalancer·Ingress 접근에 사용</td>
    </tr>
  </tbody>
</table>

NodePort에 접근할 때는 임시 URL을 만드는 `minikube service`를 사용합니다. 명령을 실행하면 내 컴퓨터에서 접속할 수 있는 URL이 출력됩니다.

```bash [터미널] Service 접근 URL 생성
minikube service nginx-service --url   # Service 접근 URL 생성
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-key">$</span> <span class="tl-str">minikube service nginx-service --url</span></div>
    <div>http://127.0.0.1:10345</div>
    <div>! windows 에서 Docker 드라이버를 사용하고 있기 때문에, 터미널을 열어야 실행할 수 있습니다.</div>
  </div>
</div>

*그림 5-10. minikube service URL 생성 결과*

URL이 출력되고 커서는 그대로 멈춰 있습니다. 이 명령은 연결을 유지하는 동안 터미널에서 계속 실행됩니다. 출력된 주소를 브라우저에 붙여 넣으면 NGINX 환영 페이지가 나타납니다.

![](../assets/CH05/terminal/01_nginx-welcome.png)

*그림 5-11. 브라우저에서 nginx 접속 확인*

다음으로 Pod가 사라지고 IP가 바뀌어도 Service가 새 Pod로 자동 연결되는지 직접 확인합니다. Ctrl+C로 터미널을 빠져나온 후 Pod를 전부 지웁니다.

```bash [터미널] Pod 재생성 후 같은 주소로 재접속
kubectl delete pod --all                # 모든 Pod 삭제 (Deployment가 자동 재생성)
minikube service nginx-service --url    # 다시 접속 URL 확인
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-key">$</span> <span class="tl-str">kubectl delete pod --all</span></div>
    <div>pod "nginx-replica-756b46b54c-7qztnx" deleted</div>
    <div>pod "nginx-replica-756b46b54c-cb592" deleted</div>
    <div>pod "nginx-replica-756b46b54c-ff5dt" deleted</div>
    <div>pod "nginx-replica-756b46b54c-hpnzm" deleted</div>
    <div><span class="tl-key">$</span> <span class="tl-str">minikube service nginx-service --url</span></div>
    <div>http://127.0.0.1:3082</div>
    <div>! windows 에서 Docker 드라이버를 사용하고 있기 때문에, 터미널을 열어야 실행할 수 있습니다.</div>
  </div>
</div>

*그림 5-12. Pod 삭제 후 Service 접속 확인*

새 URL로 접속해도 NGINX 페이지가 그대로 나옵니다.

*'Pod 앞에 Service를 두니까, Service로 요청만 보내면 Pod까지 전달되는구나.'*

## 5.2 Ingress - 도메인 라우팅

Service는 Pod 그룹마다 고정 주소를 제공합니다. 하지만 Service는 IP와 포트만으로 요청을 전달할 뿐, 같은 도메인 안에서 **URL 경로에 따라 요청을 나눠 보내지는 못합니다**. 이 한계를 해결하는 리소스가 Ingress입니다.

### 5.2.1 Ingress의 역할

**Ingress**는 외부 도메인 하나로 들어온 요청을 **URL 경로에 따라 알맞은 Service로 보냅니다**. 예를 들어 `/order` 경로와 `/stores` 경로를 각각의 Service로 보내도록 규칙을 적어 두면, Ingress가 요청 경로를 읽어 알맞은 Service로 전달합니다.

<div class="svg-figure">
<svg viewBox="0 0 920 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ingress가 도메인과 경로를 읽어 적절한 Service로 요청을 분기하고, 각 Service가 점선으로 묶인 Pod 그룹을 가리키는 구조">
  <defs>
    <marker id="ir-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="460" y="22" text-anchor="middle" font-size="15" font-weight="700" fill="#1f2937">Ingress — 경로를 읽어 요청을 Service로 분기</text>
  <rect x="165" y="40" width="695" height="215" rx="10" fill="#fff" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="6,4"/>
  <text x="180" y="61" font-size="13" font-weight="700" fill="#7b341e">Kubernetes 클러스터</text>
  <g transform="translate(0,12)">
  <g transform="translate(60, 125)">
    <circle cx="0" cy="0" r="14" fill="#fff" stroke="#475569" stroke-width="1.6"/>
    <path d="M -22 35 Q -22 12 0 12 Q 22 12 22 35 L 22 55 L -22 55 Z" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  </g>
  <text x="60" y="210" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">고객</text>
  <line x1="90" y1="135" x2="178" y2="135" stroke="#475569" stroke-width="1.6" marker-end="url(#ir-p)"/>
  <text x="135" y="127" text-anchor="middle" font-size="12" font-style="italic" fill="#6b7280">/order, /stores</text>
  <rect x="180" y="105" width="160" height="60" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="260" y="130" text-anchor="middle" font-size="16" font-weight="700" fill="#7b341e">Ingress</text>
  <text x="260" y="150" text-anchor="middle" font-size="12" fill="#7b341e">경로 읽음</text>
  <line x1="340" y1="120" x2="398" y2="80" stroke="#475569" stroke-width="1.6" marker-end="url(#ir-p)"/>
  <text x="368" y="82" text-anchor="middle" font-size="13" font-family="monospace" font-weight="700" fill="#0f172a">/order</text>
  <line x1="340" y1="150" x2="398" y2="190" stroke="#475569" stroke-width="1.6" marker-end="url(#ir-p)"/>
  <text x="368" y="195" text-anchor="middle" font-size="13" font-family="monospace" font-weight="700" fill="#0f172a">/stores</text>
  <rect x="400" y="60" width="120" height="40" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="460" y="85" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">order-service</text>
  <rect x="400" y="170" width="120" height="40" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="460" y="195" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">stores-service</text>
  <line x1="520" y1="80" x2="578" y2="80" stroke="#475569" stroke-width="1.6" marker-end="url(#ir-p)"/>
  <rect x="580" y="50" width="270" height="60" rx="8" fill="#fff" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,3"/>
  <rect x="600" y="62" width="110" height="36" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="655" y="85" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Pod</text>
  <rect x="720" y="62" width="110" height="36" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="775" y="85" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Pod</text>
  <line x1="520" y1="190" x2="578" y2="190" stroke="#475569" stroke-width="1.6" marker-end="url(#ir-p)"/>
  <rect x="580" y="160" width="270" height="60" rx="8" fill="#fff" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,3"/>
  <rect x="600" y="172" width="110" height="36" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="655" y="195" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Pod</text>
  <rect x="720" y="172" width="110" height="36" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="775" y="195" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Pod</text>
  </g>
</svg>
</div>

*그림 5-13. Ingress가 도메인과 경로를 읽어 요청을 적절한 Service로 연결하는 구조*

### 5.2.2 Ingress 컨트롤러

Ingress는 **Ingress 리소스(YAML)** 와 **Ingress 컨트롤러** 두 가지로 구성됩니다.

Ingress 리소스에는 어떤 경로를 어느 Service로 보낼지 **라우팅 규칙을 적어 둡니다**. 그리고 외부 요청이 들어오면 Ingress 컨트롤러가 **이 규칙대로 알맞은 Service로 전달합니다**.

<div class="svg-figure">
<svg viewBox="0 0 760 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ingress Controller가 Ingress 리소스(YAML)에서 규칙을 받아 외부 요청을 두 Service로 분기하는 구조">
  <defs>
    <marker id="ic13-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
    <marker id="ic13-ref" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">Ingress Controller가 리소스의 규칙을 받아 요청을 Service로 분기</text>

  <rect x="135" y="40" width="605" height="310" rx="10" fill="#fff" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="6,4"/>
  <text x="150" y="61" font-size="11" font-weight="700" fill="#7b341e">Kubernetes 클러스터</text>

  <rect x="180" y="75" width="200" height="80" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <path d="M 188 75 H 372 Q 380 75 380 83 V 95 H 180 V 83 Q 180 75 188 75 Z" fill="#475569"/>
  <text x="280" y="90" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Ingress 리소스 (YAML)</text>
  <text x="200" y="120" font-size="12" font-family="monospace" fill="#0f172a">/order   → order-service</text>
  <text x="200" y="140" font-size="12" font-family="monospace" fill="#0f172a">/stores → stores-service</text>

  <line x1="280" y1="158" x2="280" y2="200" stroke="#475569" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#ic13-ref)"/>
  <text x="318" y="182" text-anchor="middle" font-size="10" font-style="italic" fill="#475569">규칙 전달</text>

  <g transform="translate(60, 240)">
    <circle cx="0" cy="0" r="14" fill="#fff" stroke="#475569" stroke-width="1.6"/>
    <path d="M -22 35 Q -22 12 0 12 Q 22 12 22 35 L 22 55 L -22 55 Z" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  </g>
  <text x="60" y="325" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">고객</text>

  <line x1="90" y1="250" x2="198" y2="250" stroke="#475569" stroke-width="1.6" marker-end="url(#ic13-p)"/>
  <text x="145" y="242" text-anchor="middle" font-size="10" font-style="italic" fill="#6b7280">/order, /stores</text>

  <rect x="200" y="200" width="160" height="100" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <path d="M 208 200 H 352 Q 360 200 360 208 V 220 H 200 V 208 Q 200 200 208 200 Z" fill="#ff7849"/>
  <text x="280" y="215" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Ingress Controller</text>
  <text x="280" y="248" text-anchor="middle" font-size="10" fill="#7b341e">외부 트래픽 처리</text>
  <circle cx="248" cy="275" r="8" fill="#fff" stroke="#ff7849" stroke-width="1.4"/>
  <circle cx="280" cy="275" r="8" fill="#fff" stroke="#ff7849" stroke-width="1.4"/>
  <circle cx="312" cy="275" r="8" fill="#fff" stroke="#ff7849" stroke-width="1.4"/>

  <line x1="360" y1="225" x2="438" y2="200" stroke="#475569" stroke-width="1.6" marker-end="url(#ic13-p)"/>
  <text x="400" y="198" text-anchor="middle" font-size="11" font-family="monospace" font-weight="700" fill="#0f172a">/order</text>

  <line x1="360" y1="275" x2="438" y2="295" stroke="#475569" stroke-width="1.6" marker-end="url(#ic13-p)"/>
  <text x="400" y="312" text-anchor="middle" font-size="11" font-family="monospace" font-weight="700" fill="#0f172a">/stores</text>

  <rect x="440" y="180" width="160" height="40" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="520" y="205" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">order-service</text>

  <rect x="440" y="275" width="160" height="40" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="520" y="300" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">stores-service</text>
</svg>
</div>

*그림 5-14. Ingress 리소스(YAML)와 Ingress 컨트롤러*

### 5.2.3 Ingress 적용하기

실습을 위해 미니큐브에 인그레스를 활성화해 보겠습니다. 미니큐브는 Ingress 컨트롤러를 애드온 형태로 한 번에 배포할 수 있는 명령어를 제공합니다.

```bash [터미널] 인그레스 애드온 활성화
minikube addons enable ingress           # 인그레스 애드온 활성화
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-key">$</span> <span class="tl-str">minikube addons enable ingress</span></div>
    <div>* ingress is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.</div>
    <div>You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS</div>
    <div>* After the addon is enabled, please run "minikube tunnel" and your ingress resources would be available at "127.0.0.1"</div>
    <div>&nbsp;&nbsp;&nbsp;- Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.6.2</div>
    <div>&nbsp;&nbsp;&nbsp;- Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.6.2</div>
    <div>&nbsp;&nbsp;&nbsp;- Using image registry.k8s.io/ingress-nginx/controller:v1.13.2</div>
    <div>* Verifying ingress addon...</div>
    <div>* The 'ingress' addon is enabled</div>
  </div>
</div>

*그림 5-15. minikube에서 ingress 애드온 활성화 과정*

Ingress 컨트롤러가 실제로 떠 있는지 확인합니다.

```bash [터미널] Ingress 컨트롤러 확인
kubectl get pods -n ingress-nginx        # Ingress 컨트롤러 확인
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-key">$</span> <span class="tl-str">kubectl get pods -n ingress-nginx</span></div>
    <div>NAME                                        READY   STATUS      RESTARTS   AGE</div>
    <div>ingress-nginx-admission-create-zg9hh        0/1     Completed   0          40s</div>
    <div>ingress-nginx-admission-patch-bvxlw         0/1     Completed   1          40s</div>
    <div>ingress-nginx-controller-9cc49f96f-qrpm7    1/1     Running     0          35s</div>
  </div>
</div>

*그림 5-16. Ingress 컨트롤러가 Running 상태임을 확인*

:::tip
**실제 환경에서는 어떻게 띄울까**

실제 서비스 환경에서는 Ingress 컨트롤러를 클러스터에 직접 설치해야 합니다. 그런 다음 외부 사용자가 접속할 수 있도록 클라우드의 공인 IP와 연결하는 작업이 필요합니다. 앞서 사용한 미니큐브 애드온은 이 두 단계를 명령어 하나로 처리해 줍니다.
:::

`ex12` 폴더에는 Ingress 규칙과 두 Service, 그리고 각 Service가 가리키는 Deployment가 함께 들어 있습니다.

```text
ex12/
├── ingress-ex01.yml   # /order·/stores 경로별 라우팅 규칙
├── order-deploy.yml    # 주문 응답 Pod Deployment
├── order-service.yml   # 주문 Pod 앞 ClusterIP Service
├── stores-deploy.yml   # 매장 응답 Pod Deployment
├── stores-service.yml  # 매장 Pod 앞 ClusterIP Service
└── README.md           # 실습 안내
```

이제 외부 요청을 주문 Service와 매장 Service로 나눠 보낼 **Ingress 규칙**을 만들 차례입니다. 두 Service는 **ClusterIP** 타입이라 클러스터 바깥에서는 직접 접근할 수 없습니다.

다음은 `/order`와 `/stores` 두 경로를 각각의 Service로 분기하는 Ingress YAML입니다.

```yaml [실습 2] ex12/ingress-ex01.yml. 경로별 라우팅 규칙
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ex12-ingress
spec:
  ingressClassName: nginx           # 어느 Ingress 컨트롤러가 이 규칙을 집행할지 지정
  rules:
    - http:
        paths:
          - path: /order            # 주문 경로 → order-service
            pathType: Prefix        # /order로 시작하는 하위 경로까지 매칭
            backend:
              service:
                name: order-service
                port:
                  number: 5678
          - path: /stores           # 매장 경로 → stores-service
            pathType: Prefix        # /stores로 시작하는 하위 경로까지 매칭
            backend:
              service:
                name: stores-service
                port:
                  number: 5678
```

이제 `ex12` 폴더의 모든 파일을 한 번에 적용합니다.

```bash [터미널] Ingress 규칙과 두 Service 일괄 적용
kubectl apply -f ex12/                  # ex12 폴더 내 모든 yaml 일괄 적용
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-key">$</span> <span class="tl-str">kubectl apply -f ex12/</span></div>
    <div>ingress.networking.k8s.io/ex12-ingress created</div>
    <div>deployment.apps/order-deploy created</div>
    <div>service/order-service created</div>
    <div>deployment.apps/stores-deploy created</div>
    <div>service/stores-service created</div>
  </div>
</div>

*그림 5-17. Ingress 리소스 등록 확인*

### 5.2.4 외부에서 Ingress 접속해 보기

클러스터를 호스트와 연결하기 위해, 외부 IP를 부여하는 `minikube tunnel`을 별도 터미널에서 실행합니다.

```bash [터미널] 외부 터널 개방
minikube tunnel                          # 별도 터미널에서 실행
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-key">$</span> <span class="tl-str">minikube tunnel</span></div>
    <div>* Tunnel successfully started</div>
    <div>* NOTE: Please do not close this terminal as this process must stay alive for the tunnel to be accessible ...</div>
    <div>* Starting tunnel for service ex12-ingress.</div>
  </div>
</div>

*그림 5-18. minikube tunnel 실행 화면*

이제 브라우저에서 두 경로를 차례로 접속해 보겠습니다.

먼저 `http://localhost/order`를 열면 "주문 접수 완료"가 나옵니다.

<!-- [CAPTURE NEEDED: 브라우저에서 http://localhost/order 접속 시 "주문 접수 완료" 응답 확인 화면. 자산 경로: assets/CH05/mock-order-page.png] -->
![](../assets/CH05/terminal/02_order-result.png)

*그림 5-19. /order 접속 결과*

이어서 `http://localhost/stores`를 열면 "매장 선택"이 나옵니다.

<!-- [CAPTURE NEEDED: 브라우저에서 http://localhost/stores 접속 시 "매장 선택" 응답 확인 화면. 자산 경로: assets/CH05/mock-stores-page.png] -->
![](../assets/CH05/terminal/03_stores-result.png)

*그림 5-20. /stores 접속 결과*

도메인은 하나인데 경로마다 다른 응답이 돌아왔습니다. Ingress가 경로를 보고 알맞은 **Service**로 요청을 넘기고, Service가 다시 그 뒤의 **Pod**로 요청을 전달해 응답이 만들어진 결과입니다.

*그럼 한 요청 안에서 Ingress와 Service는 각각 어떤 정보를 보고 처리하는 걸까?*

### 5.2.5 두 리소스의 계층 분담

두 리소스가 같은 요청에서 보는 정보가 다른 모습은 우편 봉투의 송장과 닮았습니다.

**우편 송장**에는 두 가지 정보가 함께 적혀 있습니다. 물류 센터가 어느 지역으로 보낼지 정할 때 찍는 **송장 바코드**, 그리고 그 지역 우체국에서 **집배원**이 직접 눈으로 확인하는 **받는 곳 주소**입니다.

<div class="svg-figure">
<svg viewBox="0 0 800 305" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="우편 위 송장에 바코드(스캐너로 읽음)와 받는 곳 주소(눈으로 읽음)가 함께 있고, 물류 센터는 바코드까지, 집배원은 받는 곳 주소만 읽음">
  <defs>
    <marker id="lbl-orange" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="lbl-slate" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="400" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2937">우편 송장에 두 가지 정보가 함께 있습니다</text>
  <g transform="translate(180, 56)">
    <rect x="0" y="0" width="440" height="240" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
    <line x1="0" y1="0" x2="220" y2="80" stroke="#d97706" stroke-width="1.3"/>
    <line x1="440" y1="0" x2="220" y2="80" stroke="#d97706" stroke-width="1.3"/>
    <text x="220" y="-12" text-anchor="middle" font-size="15" font-weight="700" fill="#7b341e">우편</text>
    <g transform="translate(20, 90)">
      <rect x="0" y="0" width="400" height="135" rx="3" fill="#fff" stroke="#dc2626" stroke-width="1.6"/>
      <text x="200" y="-4" text-anchor="middle" font-size="10" font-weight="700" fill="#dc2626">송장</text>
      <rect x="8" y="8" width="384" height="58" rx="2" fill="#fffaf0" stroke="#cbd5e1" stroke-width="0.8"/>
      <text x="16" y="24" font-size="12" font-weight="700" fill="#dc2626">송장 바코드</text>
      <text x="386" y="24" text-anchor="end" font-size="9" font-style="italic" fill="#1f2937">스캐너로 읽음</text>
      <g transform="translate(16, 30)">
        <line x1="0" y1="0" x2="0" y2="24" stroke="#0f172a" stroke-width="1"/>
        <line x1="3" y1="0" x2="3" y2="24" stroke="#0f172a" stroke-width="1.4"/>
        <line x1="6" y1="0" x2="6" y2="24" stroke="#0f172a" stroke-width="0.6"/>
        <line x1="9" y1="0" x2="9" y2="24" stroke="#0f172a" stroke-width="1"/>
        <line x1="12" y1="0" x2="12" y2="24" stroke="#0f172a" stroke-width="0.8"/>
        <line x1="15" y1="0" x2="15" y2="24" stroke="#0f172a" stroke-width="1.2"/>
        <line x1="18" y1="0" x2="18" y2="24" stroke="#0f172a" stroke-width="0.5"/>
        <line x1="21" y1="0" x2="21" y2="24" stroke="#0f172a" stroke-width="1"/>
        <line x1="24" y1="0" x2="24" y2="24" stroke="#0f172a" stroke-width="0.7"/>
        <line x1="27" y1="0" x2="27" y2="24" stroke="#0f172a" stroke-width="1.3"/>
        <line x1="30" y1="0" x2="30" y2="24" stroke="#0f172a" stroke-width="0.6"/>
        <line x1="33" y1="0" x2="33" y2="24" stroke="#0f172a" stroke-width="1"/>
        <line x1="36" y1="0" x2="36" y2="24" stroke="#0f172a" stroke-width="0.8"/>
        <line x1="39" y1="0" x2="39" y2="24" stroke="#0f172a" stroke-width="1.2"/>
        <line x1="42" y1="0" x2="42" y2="24" stroke="#0f172a" stroke-width="0.5"/>
        <line x1="45" y1="0" x2="45" y2="24" stroke="#0f172a" stroke-width="1.1"/>
        <line x1="48" y1="0" x2="48" y2="24" stroke="#0f172a" stroke-width="0.7"/>
        <line x1="51" y1="0" x2="51" y2="24" stroke="#0f172a" stroke-width="1.3"/>
        <line x1="54" y1="0" x2="54" y2="24" stroke="#0f172a" stroke-width="0.6"/>
        <line x1="57" y1="0" x2="57" y2="24" stroke="#0f172a" stroke-width="1"/>
        <line x1="60" y1="0" x2="60" y2="24" stroke="#0f172a" stroke-width="0.8"/>
        <line x1="63" y1="0" x2="63" y2="24" stroke="#0f172a" stroke-width="1.2"/>
        <line x1="66" y1="0" x2="66" y2="24" stroke="#0f172a" stroke-width="0.5"/>
        <line x1="69" y1="0" x2="69" y2="24" stroke="#0f172a" stroke-width="1.1"/>
        <line x1="72" y1="0" x2="72" y2="24" stroke="#0f172a" stroke-width="0.7"/>
        <line x1="75" y1="0" x2="75" y2="24" stroke="#0f172a" stroke-width="1.3"/>
        <line x1="78" y1="0" x2="78" y2="24" stroke="#0f172a" stroke-width="0.6"/>
        <line x1="81" y1="0" x2="81" y2="24" stroke="#0f172a" stroke-width="1"/>
        <line x1="84" y1="0" x2="84" y2="24" stroke="#0f172a" stroke-width="0.8"/>
        <line x1="87" y1="0" x2="87" y2="24" stroke="#0f172a" stroke-width="1.2"/>
        <line x1="90" y1="0" x2="90" y2="24" stroke="#0f172a" stroke-width="0.5"/>
        <line x1="93" y1="0" x2="93" y2="24" stroke="#0f172a" stroke-width="1.1"/>
        <line x1="96" y1="0" x2="96" y2="24" stroke="#0f172a" stroke-width="0.7"/>
        <line x1="99" y1="0" x2="99" y2="24" stroke="#0f172a" stroke-width="1.3"/>
        <line x1="102" y1="0" x2="102" y2="24" stroke="#0f172a" stroke-width="0.6"/>
        <line x1="105" y1="0" x2="105" y2="24" stroke="#0f172a" stroke-width="1"/>
        <line x1="108" y1="0" x2="108" y2="24" stroke="#0f172a" stroke-width="0.8"/>
        <line x1="111" y1="0" x2="111" y2="24" stroke="#0f172a" stroke-width="1.2"/>
        <line x1="114" y1="0" x2="114" y2="24" stroke="#0f172a" stroke-width="0.5"/>
        <line x1="117" y1="0" x2="117" y2="24" stroke="#0f172a" stroke-width="1.1"/>
        <line x1="120" y1="0" x2="120" y2="24" stroke="#0f172a" stroke-width="0.7"/>
        <line x1="123" y1="0" x2="123" y2="24" stroke="#0f172a" stroke-width="1.3"/>
        <line x1="126" y1="0" x2="126" y2="24" stroke="#0f172a" stroke-width="0.6"/>
        <line x1="129" y1="0" x2="129" y2="24" stroke="#0f172a" stroke-width="1"/>
        <line x1="132" y1="0" x2="132" y2="24" stroke="#0f172a" stroke-width="0.8"/>
      </g>
      <text x="200" y="62" text-anchor="middle" font-size="10" font-family="monospace" fill="#dc2626">1234-5678-90</text>
      <rect x="8" y="72" width="384" height="56" rx="2" fill="#fffaf0" stroke="#cbd5e1" stroke-width="0.8"/>
      <text x="16" y="88" font-size="12" font-weight="700" fill="#475569">받는 곳 주소</text>
      <text x="386" y="88" text-anchor="end" font-size="9" font-style="italic" fill="#1f2937">사람이 눈으로 읽음</text>
      <text x="16" y="106" font-size="12" font-family="monospace" font-weight="700" fill="#0f172a">서울시 강남구 테헤란로 123</text>
      <text x="16" y="122" font-size="12" font-family="monospace" font-weight="700" fill="#0f172a">○○빌딩 5층  김영진</text>
    </g>
  </g>
  <g transform="translate(20, 110)">
    <rect x="0" y="0" width="150" height="60" rx="6" fill="#fff" stroke="#ff7849" stroke-width="2"/>
    <text x="75" y="22" text-anchor="middle" font-size="15" font-weight="700" fill="#7b341e">물류 센터</text>
    <text x="75" y="40" text-anchor="middle" font-size="10" fill="#7b341e">송장 바코드까지</text>
    <text x="75" y="54" text-anchor="middle" font-size="9" fill="#7b341e">스캐너로 정밀 분기</text>
  </g>
  <line x1="170" y1="140" x2="216" y2="158" stroke="#ff7849" stroke-width="2.4" marker-end="url(#lbl-orange)"/>
  <g transform="translate(630, 158)">
    <rect x="0" y="0" width="150" height="60" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
    <text x="75" y="22" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">집배원</text>
    <text x="75" y="40" text-anchor="middle" font-size="10" fill="#475569">받는 곳 주소만</text>
    <text x="75" y="54" text-anchor="middle" font-size="9" fill="#1f2937">눈으로 읽고 분류</text>
  </g>
  <line x1="630" y1="200" x2="582" y2="230" stroke="#475569" stroke-width="2.2" marker-end="url(#lbl-slate)"/>
</svg>
</div>

*그림 5-21. 우편 위 송장에 바코드와 받는 곳 주소가 함께 있고, 물류 센터는 바코드까지, 집배원은 받는 곳 주소만 읽습니다*

이 우편 송장의 구조를 네트워크 **패킷**에 그대로 옮겨 보겠습니다. 패킷은 **클라이언트와 서버가 네트워크로 데이터를 주고받는 기본 단위**입니다.

<div class="svg-figure">
<svg viewBox="0 0 800 270" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="실제 패킷의 두 정보 — HTTP 페이로드(Host·URL)와 TCP/IP 헤더(IP·포트). Ingress는 HTTP 페이로드까지, Service는 TCP/IP 헤더만 읽음">
  <defs>
    <marker id="it-orange" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="it-slate" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="400" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2937">실제 패킷에 두 종류의 정보가 함께 들어 있습니다</text>
  <g transform="translate(220, 50)">
    <rect x="0" y="0" width="360" height="200" rx="4" fill="#f8fafc" stroke="#475569" stroke-width="1.6" stroke-dasharray="4,3"/>
    <text x="180" y="-8" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">패킷</text>
    <g transform="translate(14, 16)">
      <rect x="0" y="0" width="332" height="86" rx="3" fill="#fff" stroke="#dc2626" stroke-width="1.4"/>
      <text x="14" y="18" font-size="12" font-weight="700" fill="#dc2626">HTTP 페이로드</text>
      <text x="318" y="18" text-anchor="end" font-size="9" font-style="italic" fill="#1f2937">L7 · HTTP 서버가 파싱</text>
      <line x1="14" y1="24" x2="318" y2="24" stroke="#fed7aa" stroke-width="0.5"/>
      <text x="14" y="42" font-size="12" font-family="monospace" font-weight="700" fill="#0f172a">GET /order HTTP/1.1</text>
      <text x="14" y="58" font-size="12" font-family="monospace" fill="#0f172a">Host: localhost</text>
      <text x="14" y="74" font-size="12" font-family="monospace" fill="#0f172a">User-Agent: ...</text>
    </g>
    <g transform="translate(14, 112)">
      <rect x="0" y="0" width="332" height="74" rx="3" fill="#fff" stroke="#475569" stroke-width="1.4"/>
      <text x="14" y="18" font-size="12" font-weight="700" fill="#475569">TCP/IP 헤더</text>
      <text x="318" y="18" text-anchor="end" font-size="9" font-style="italic" fill="#1f2937">L4 · iptables가 즉시 읽음</text>
      <line x1="14" y1="24" x2="318" y2="24" stroke="#cbd5e1" stroke-width="0.5"/>
      <text x="14" y="42" font-size="12" font-family="monospace" fill="#475569">받는 IP</text>
      <text x="318" y="42" text-anchor="end" font-size="12" font-family="monospace" font-weight="700" fill="#0f172a">10.96.0.20</text>
      <text x="14" y="58" font-size="12" font-family="monospace" fill="#475569">받는 포트</text>
      <text x="318" y="58" text-anchor="end" font-size="12" font-family="monospace" font-weight="700" fill="#0f172a">80</text>
      <text x="14" y="71" font-size="10" font-family="monospace" fill="#1f2937">...프로토콜·TTL 등</text>
    </g>
  </g>
  <g transform="translate(20, 88)">
    <rect x="0" y="0" width="150" height="60" rx="6" fill="#fff" stroke="#ff7849" stroke-width="2"/>
    <text x="75" y="22" text-anchor="middle" font-size="15" font-weight="700" fill="#7b341e">Ingress</text>
    <text x="75" y="40" text-anchor="middle" font-size="10" fill="#7b341e">HTTP 페이로드까지</text>
    <text x="75" y="54" text-anchor="middle" font-size="9" fill="#7b341e">Pod 안 HTTP 파싱</text>
  </g>
  <line x1="170" y1="108" x2="232" y2="100" stroke="#ff7849" stroke-width="2.4" marker-end="url(#it-orange)"/>
  <g transform="translate(630, 168)">
    <rect x="0" y="0" width="150" height="60" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
    <text x="75" y="22" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Service</text>
    <text x="75" y="40" text-anchor="middle" font-size="10" fill="#475569">받는 IP·포트만</text>
    <text x="75" y="54" text-anchor="middle" font-size="9" fill="#1f2937">iptables 규칙 매칭</text>
  </g>
  <line x1="630" y1="198" x2="568" y2="194" stroke="#475569" stroke-width="2.2" marker-end="url(#it-slate)"/>
</svg>
</div>

*그림 5-22. 실제 패킷에 HTTP 페이로드와 TCP/IP 헤더가 함께 들어 있고, Ingress는 페이로드까지, Service는 헤더만 읽습니다*

패킷 안에는 우편 송장처럼 역할이 다른 여러 종류의 데이터가 섞여 있습니다. 이 정보들은 각자의 역할에 따라 **전송 계층**(Layer 4)과 **응용 계층**(Layer 7)에서 각각 처리됩니다.

| 구분 | 전송 계층 (L4) | 응용 계층 (L7) |
|:---:|:---|:---|
| **역할** | 데이터를 어느 컴퓨터의 어느 프로세스로 보낼지 안내 | 패킷 내부의 메시지·콘텐츠를 해석 |
| **보는 정보** | 패킷 겉면(헤더)의 받는 IP·포트 | 패킷 내부의 URL·도메인 |
| **담당 리소스** | **Service** | **Ingress** |
| **동작** | 지정된 IP·포트로 들어온 요청을 백엔드 Pod로 분산·전달 | 세부 경로(`/order`, `/stores`)에 따라 알맞은 Service로 전달 |

## 5.3 브라우저에서 Pod까지의 경로

이전 챕터에서는 개발자의 명령으로 Pod를 띄우고 관리하는 흐름을 다뤘습니다. 이번에는 사용자가 브라우저에서 요청했을 때 Pod에 도달하는 흐름을, 우체국에 우편을 보내는 예시를 통해 단계별로 알아보겠습니다.

### 5.3.1 NodePort로 클러스터에 들어오기

먼저 발신자가 **중앙 우체국** 창구에 우편을 맡깁니다. 우편을 받은 **창구 직원**은 다음 거점인 **물류 센터**로 보냅니다.

브라우저가 보낸 요청도 비슷하게 흘러갑니다. 요청이 노드에 열린 **NodePort**로 클러스터에 들어오면, 같은 노드의 **kube-proxy**가 패킷의 목적지를 다음 거점인 **Ingress 컨트롤러**의 IP로 바꿉니다. 그러면 패킷은 Ingress 컨트롤러로 전달됩니다.

<div class="svg-figure">
<svg viewBox="0 0 780 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="1단계 손그림 — 우편이 우체국(NodePort·kube-proxy)을 거쳐 물류 센터(Ingress 컨트롤러)로">
  <defs>
    <marker id="il1-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#1f2937"/></marker>
  </defs>
  <text x="390" y="26" text-anchor="middle" font-size="15" font-weight="700" fill="#1f2937">우체국이 우편을 받아 물류 센터로 보냅니다</text>
  <rect x="100" y="125" width="80" height="50" rx="3" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <path d="M100 125 L140 150 L180 125" fill="none" stroke="#475569" stroke-width="1.4"/>
  <text x="140" y="192" text-anchor="middle" font-size="12" font-weight="700" fill="#475569">요청 (우편)</text>
  <text x="140" y="208" text-anchor="middle" font-size="10" font-family="monospace" fill="#94a3b8">metacoding.com/order</text>
  <line x1="180" y1="150" x2="289" y2="150" stroke="#1f2937" stroke-width="1.6" marker-end="url(#il1-a)"/>
  <path d="M299 92 L481 92 L390 66 Z" fill="#fde4d3" stroke="#7b341e" stroke-width="1.6"/>
  <rect x="305" y="92" width="170" height="116" fill="#fff" stroke="#7b341e" stroke-width="1.8"/>
  <rect x="333" y="98" width="114" height="20" fill="#7b341e"/>
  <text x="390" y="111" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">우체국</text>
  <rect x="293" y="126" width="24" height="50" rx="2" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <circle cx="305" cy="151" r="2.4" fill="#ff7849"/>
  <text x="305" y="194" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">NodePort</text>
  <rect x="338" y="130" width="108" height="44" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="392" y="150" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">kube-proxy</text>
  <text x="392" y="165" text-anchor="middle" font-size="9" fill="#7b341e">규칙대로 IP 변환</text>
  <line x1="475" y1="150" x2="549" y2="150" stroke="#1f2937" stroke-width="1.6" marker-end="url(#il1-a)"/>
  <path d="M549 92 L731 92 L640 66 Z" fill="#fde4d3" stroke="#7b341e" stroke-width="1.6"/>
  <rect x="555" y="92" width="170" height="116" fill="#fff" stroke="#7b341e" stroke-width="1.8"/>
  <rect x="583" y="98" width="114" height="20" fill="#7b341e"/>
  <text x="640" y="111" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">물류 센터</text>
  <rect x="586" y="126" width="108" height="62" rx="2" fill="#fff4ed" stroke="#7b341e" stroke-width="1.4"/>
  <line x1="586" y1="140" x2="694" y2="140" stroke="#7b341e" stroke-width="0.8"/>
  <line x1="586" y1="154" x2="694" y2="154" stroke="#7b341e" stroke-width="0.8"/>
  <line x1="586" y1="168" x2="694" y2="168" stroke="#7b341e" stroke-width="0.8"/>
  <text x="640" y="230" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">Ingress 컨트롤러</text>
  <text x="640" y="243" text-anchor="middle" font-size="10" fill="#7b341e">URL·도메인으로 분기</text>
</svg>
</div>

*그림 5-23. 요청이 NodePort로 들어와 Ingress 컨트롤러로 향합니다*

| 컴포넌트 | 이 단계에서 하는 일 |
|---|---|
| **NodePort** | 노드에 포트를 열어 외부 요청을 클러스터 안으로 받는 입구 |
| **kube-proxy** | 패킷의 목적지를 노드 IP에서 Ingress 컨트롤러의 IP로 바꿈 |

### 5.3.2 Ingress가 URL·도메인으로 Service 분기하기

우편이 **물류 센터**에 도착합니다. 물류 센터에서는 바코드를 스캐너로 찍어 등록된 **분류 규칙**에 따라 어느 지역 우체국으로 갈지 정합니다.

Ingress 컨트롤러도 **Ingress 리소스**에 적힌 규칙으로 요청을 보낼 곳을 정합니다. 요청의 **URL 경로와 도메인**을 그 규칙과 비교해 맞는 **Service**를 고릅니다.

<div class="svg-figure">
<svg viewBox="0 0 760 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="2단계 손그림 — 물류 센터(Ingress 컨트롤러)가 송장을 보고 /order는 order-service, /stores는 stores-service 우체국으로 분기">
  <defs>
    <marker id="il2-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#1f2937"/></marker>
  </defs>
  <text x="380" y="26" text-anchor="middle" font-size="15" font-weight="700" fill="#1f2937">물류 센터가 송장을 보고 알맞은 우체국으로 보냅니다</text>
  <rect x="100" y="150" width="80" height="50" rx="3" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <path d="M100 150 L140 175 L180 150" fill="none" stroke="#475569" stroke-width="1.4"/>
  <text x="140" y="216" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">요청</text>
  <text x="140" y="231" text-anchor="middle" font-size="11" font-family="monospace" fill="#7b341e">/order</text>
  <line x1="180" y1="175" x2="246" y2="175" stroke="#1f2937" stroke-width="1.6" marker-end="url(#il2-a)"/>
  <path d="M242 110 L470 110 L356 82 Z" fill="#fde4d3" stroke="#7b341e" stroke-width="1.6"/>
  <rect x="248" y="110" width="222" height="130" fill="#fff" stroke="#7b341e" stroke-width="1.8"/>
  <rect x="285" y="116" width="148" height="20" fill="#7b341e"/>
  <text x="359" y="131" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">물류 센터</text>
  <rect x="258" y="144" width="204" height="64" rx="3" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="360" y="161" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Ingress 규칙</text>
  <text x="266" y="183" font-size="11" font-family="monospace" fill="#0f172a">/order  → order-service</text>
  <text x="266" y="201" font-size="11" font-family="monospace" fill="#0f172a">/stores → stores-service</text>
  <text x="359" y="228" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">Ingress 컨트롤러</text>
  <path d="M470 150 Q505 120 538 104" fill="none" stroke="#1f2937" stroke-width="1.6" marker-end="url(#il2-a)"/>
  <text x="500" y="110" text-anchor="middle" font-size="11" font-family="monospace" font-weight="700" fill="#7b341e">/order</text>
  <path d="M470 200 Q505 230 538 246" fill="none" stroke="#1f2937" stroke-width="1.6" marker-end="url(#il2-a)"/>
  <text x="500" y="256" text-anchor="middle" font-size="11" font-family="monospace" font-weight="700" fill="#7b341e">/stores</text>
  <path d="M534 72 L706 72 L620 50 Z" fill="#fde4d3" stroke="#7b341e" stroke-width="1.6"/>
  <rect x="540" y="72" width="160" height="60" fill="#fff" stroke="#7b341e" stroke-width="1.8"/>
  <rect x="556" y="78" width="128" height="18" fill="#7b341e"/>
  <text x="620" y="90" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">order-service</text>
  <text x="620" y="118" text-anchor="middle" font-size="10" fill="#7b341e">Service (우체국)</text>
  <path d="M534 228 L706 228 L620 206 Z" fill="#fde4d3" stroke="#7b341e" stroke-width="1.6"/>
  <rect x="540" y="228" width="160" height="60" fill="#fff" stroke="#7b341e" stroke-width="1.8"/>
  <rect x="556" y="234" width="128" height="18" fill="#7b341e"/>
  <text x="620" y="250" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">stores-service</text>
  <text x="620" y="278" text-anchor="middle" font-size="10" fill="#7b341e">Service (우체국)</text>
</svg>
</div>

*그림 5-24. Ingress 컨트롤러가 경로에 따라 알맞은 Service로 보냅니다*

| 컴포넌트 | 이 단계에서 하는 일 |
|---|---|
| **Ingress 컨트롤러** | 요청을 받아 URL 경로·도메인에 맞는 Service로 전달 |
| **Ingress 규칙** | 어떤 경로·도메인을 어느 Service로 보낼지 적어 둔 설정 |

### 5.3.3 ClusterIP가 Pod로 전달하기

물류 센터에서 우체국으로 도착한 우편은 이제 배송이 시작됩니다. **집배원**은 **배송 목록**에 적힌 **우편함**에 우편을 넣습니다.

마지막 단계는 **kube-proxy**가 담당합니다. kube-proxy는 도착한 패킷의 IP를 **EndpointSlice**에서 살아있는 **Pod** 중 하나의 IP로 바꿉니다. 그러면 패킷은 그 Pod로 전달됩니다.

<div class="svg-figure">
<svg viewBox="0 0 760 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="3단계 손그림 — order-service 우체국에 도착한 우편의 목적지를 kube-proxy가 배송 목록(EndpointSlice)을 보고 살아있는 우편함(Pod B)으로 바꿈">
  <defs>
    <marker id="il3-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#1f2937"/></marker>
    <marker id="il3-g" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#94a3b8"/></marker>
  </defs>
  <text x="380" y="26" text-anchor="middle" font-size="15" font-weight="700" fill="#1f2937">집배원이 배송 목록을 보고 우편함에 우편을 넣습니다</text>
  <path d="M40 138 L248 138 L144 112 Z" fill="#fde4d3" stroke="#7b341e" stroke-width="1.6"/>
  <rect x="52" y="138" width="184" height="96" fill="#fff" stroke="#7b341e" stroke-width="1.8"/>
  <rect x="76" y="144" width="136" height="20" fill="#7b341e"/>
  <text x="144" y="159" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">order-service</text>
  <text x="144" y="202" text-anchor="middle" font-size="11" fill="#7b341e">Service (우체국)</text>
  <line x1="236" y1="184" x2="282" y2="184" stroke="#1f2937" stroke-width="1.6" marker-end="url(#il3-a)"/>
  <rect x="298" y="50" width="124" height="78" rx="3" fill="#fff" stroke="#7b341e" stroke-width="1.6"/>
  <rect x="344" y="44" width="32" height="12" rx="2" fill="#7b341e"/>
  <text x="360" y="72" text-anchor="middle" font-size="9" font-weight="700" fill="#7b341e">EndpointSlice(배송 목록)</text>
  <text x="310" y="90" font-size="9" fill="#94a3b8">Pod A</text>
  <rect x="306" y="96" width="108" height="14" fill="#fff4ed"/>
  <text x="310" y="107" font-size="9" font-weight="700" fill="#7b341e">Pod B  (살아있음)</text>
  <text x="310" y="124" font-size="9" fill="#94a3b8">Pod C</text>
  <rect x="300" y="160" width="120" height="48" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="360" y="180" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">kube-proxy</text>
  <text x="360" y="196" text-anchor="middle" font-size="9" fill="#7b341e">명단 보고 IP 변환</text>
  <line x1="360" y1="131" x2="360" y2="158" stroke="#7b341e" stroke-width="1.4" stroke-dasharray="3 2" marker-end="url(#il3-a)"/>
  <text x="368" y="148" font-size="9" font-style="italic" fill="#7b341e">명단</text>
  <line x1="420" y1="184" x2="492" y2="184" stroke="#1f2937" stroke-width="1.6" marker-end="url(#il3-a)"/>
  <rect x="500" y="120" width="150" height="40" rx="3" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <line x1="520" y1="132" x2="630" y2="132" stroke="#cbd5e1" stroke-width="2"/>
  <text x="575" y="146" text-anchor="middle" font-size="11" font-weight="700" fill="#94a3b8">Pod A</text>
  <rect x="500" y="164" width="150" height="44" rx="3" fill="#fff4ed" stroke="#ff7849" stroke-width="2.4"/>
  <line x1="520" y1="177" x2="630" y2="177" stroke="#ff7849" stroke-width="2"/>
  <text x="575" y="195" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Pod B (살아있음)</text>
  <rect x="500" y="212" width="150" height="40" rx="3" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/>
  <line x1="520" y1="224" x2="630" y2="224" stroke="#cbd5e1" stroke-width="2"/>
  <text x="575" y="238" text-anchor="middle" font-size="11" font-weight="700" fill="#94a3b8">Pod C</text>
</svg>
</div>

*그림 5-25. kube-proxy가 살아있는 Pod로 목적지를 바꿉니다*

| 컴포넌트 | 이 단계에서 하는 일 |
|---|---|
| **Service (ClusterIP)** | 여러 Pod를 대표하는 고정 IP로, 요청이 이 주소로 들어옴 |
| **EndpointSlice** | Service에 연결된, 지금 살아있는 Pod들의 IP 목록 |
| **kube-proxy** | 요청의 목적지를 ClusterIP에서 살아있는 Pod의 IP로 바꿈 |

:::tip
**Ingress 컨트롤러와 kube-proxy가 설정을 받는 방법**

클러스터에 등록된 모든 설정은 **API Server**를 거쳐 상태 저장소인 **etcd**에 보관됩니다. 각 컴포넌트는 API Server로부터 자신에게 필요한 설정을 전달받아 적용합니다. 이때 Ingress 컨트롤러는 YAML로 작성된 **Ingress 리소스**를 받아 라우팅 규칙으로 사용하고, kube-proxy는 살아있는 Pod 목록인 **EndpointSlice**를 받아 IP 변환에 반영합니다.
:::

이번 챕터에서는 외부에서 들어온 요청이 클러스터 안의 Pod까지 도달하는 흐름을 살펴봤습니다. 하나의 요청이 들어오면 Ingress는 도메인과 URL 경로를, Service는 IP와 포트를 확인해 목적지를 결정합니다.

*'이제 요청이 클러스터 안에서 Pod까지 닿는 구조를 알았으니, 내 프로젝트에도 직접 적용해 볼 수 있겠다.'*

다음 챕터에서는 실제 운영 환경에 필요한 환경 변수와 데이터 저장소를 다뤄 보겠습니다.

:::remember
**이것만은 기억하자**

- **Service는 Pod의 고정 진입점입니다.** Pod는 소모품이라 IP가 수시로 바뀌지만, Service는 변하지 않는 주소를 제공하며 트래픽을 분산합니다.
- **Service는 접근 범위에 따라 세 종류로 나뉩니다.** **ClusterIP**는 클러스터 안에서만 통신합니다. **NodePort**는 노드의 IP와 포트로 외부에 열립니다. **LoadBalancer**는 클라우드가 발급한 공인 IP로 외부에 열립니다.
- **Ingress는 외부 요청을 URL 경로로 분기합니다.** 숫자(IP·포트)만 보는 Service와 달리, 도메인과 URL 경로를 읽어 알맞은 Service로 연결합니다. 라우팅 규칙을 정의하는 **리소스(YAML)** 와 실제 요청을 처리하는 **Ingress 컨트롤러(Pod)** 가 함께 동작합니다.
:::
