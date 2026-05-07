# Ch.5 Kubernetes 네트워킹

다음 날 아침이었습니다. 자리에 앉아 가방을 내려놓고 어제 띄워둔 Pod 네 대를 다시 떠올렸습니다. 자동 복구와 무중단 교체가 두 눈앞에서 돌아갔던 장면이 아직 또렷했습니다.

그때 옆자리 동료가 의자를 밀고 와 모니터를 들여다봤습니다.

**동료**: "오픈이 님, 어제 띄운 거 어떻게 들어가요? 주소 좀 알려 주세요."

오픈이는 입을 떼려다 말았습니다. 정작 그 한마디가 막혔습니다.

*'어, 어디로 들어가지...'*

`kubectl get pods`를 다시 두드렸습니다. Pod 네 대가 각자 다른 IP를 들고 줄지어 떠 있었습니다. 어제는 잘 돌아간다는 사실에만 들떠 있었는데, 막상 누군가에게 들어가는 문을 보여 주려니 손에 잡히는 주소가 한 개도 없었습니다.

게다가 Pod IP는 재시작 때마다 바뀝니다. 동료에게 IP 한 줄을 적어 주는 순간, Pod가 한 번이라도 죽었다 살아나면 그 주소는 사라진 번호가 됩니다.

*'도커 때 Nginx 한 대를 앞에 세웠던 것처럼, 그 앞에 변하지 않는 문 하나가 있어야 하는데.'*

오픈이는 다시 공식 문서를 펼쳤습니다.

## 5.1 Service - Pod의 고정 주소

### 5.1.1 Service가 필요한 이유

문서를 훑던 오픈이의 눈에 **Service**라는 항목이 들어왔습니다. Pod의 상태나 위치와 상관없이 변하지 않는 고정 진입점을 제공하는 자리, 그 일을 맡는 리소스가 Service였습니다.

가맹점이 많은 프랜차이즈를 떠올려 보면 이해가 쉽습니다. 매장 직원이 누구로 바뀌든 점장이 자리를 옮기든, 손님은 **브랜드 대표 번호** 하나로 언제든 주문을 넣을 수 있습니다. 직원의 휴대폰 번호가 아니라 매장에 붙박이로 걸려 있는 번호라, 사람이 바뀌어도 그대로 남습니다.

Service가 클러스터 안에서 같은 자리를 맡습니다. Pod가 죽고 새로 뜨면서 IP가 바뀌어도, 그 앞에 걸린 대표 번호는 흔들리지 않습니다.

<div class="svg-figure">
<svg viewBox="0 0 760 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="외부 요청이 Service라는 고정 진입점을 거쳐 여러 Pod로 분배되는 구조">
  <defs>
    <marker id="sv-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">Service — 고정 진입점</text>
  <rect x="20" y="100" width="130" height="80" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="85" y="135" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">외부 요청</text>
  <text x="85" y="158" text-anchor="middle" font-size="10" fill="#6b7280">브라우저·클라이언트</text>
  <line x1="150" y1="140" x2="198" y2="140" stroke="#475569" stroke-width="1.8" marker-end="url(#sv-p)"/>
  <text x="174" y="132" text-anchor="middle" font-size="10" fill="#6b7280" font-style="italic">요청</text>
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
  <line x1="380" y1="170" x2="505" y2="290" stroke="#475569" stroke-width="1.8" marker-end="url(#sv-p)"/>
  <rect x="510" y="265" width="180" height="55" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="600" y="287" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Pod 4</text>
  <text x="600" y="305" text-anchor="middle" font-size="11" font-family="monospace" fill="#6b7280">10.0.0.15</text>
</svg>
</div>

*그림 5-1. Service는 Pod IP가 바뀌어도 변하지 않는 고정 주소를 제공*

### 5.1.2 Service 생성

:::tip
전체 실습 코드는 깃헙을 참고합니다.

**실습 코드 (GitHub)**: https://github.com/metacoding-10-linux-docker/docker/tree/master/ex11
:::

오픈이는 직접 띄워 보기로 했습니다. 먼저 Pod를 세우고 그 앞에 대표 번호를 답니다.

오픈이는 `ex11` 폴더를 열었습니다. 어제 사용했던 `deploy-ex02.yml`이 그대로 남아 있습니다. 이 파일은 Pod 네 개를 띄우는 Deployment 설정입니다.

```bash
kubectl apply -f ex11/deploy-ex02.yml   # Pod 4개 생성
```

오픈이는 다음으로 Service YAML을 살펴봤습니다.

**ex11/service-ex01.yml**
```yaml
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
      nodePort: 30080   # 외부에서 노드로 진입할 때 사용하는 포트 (30000~32767)
```

핵심은 `selector` 한 줄입니다. Service는 Pod의 IP를 외워두지 않습니다. 대신 라벨로 식구를 가립니다. `app: nginx` 라벨이 붙은 Pod라면 IP가 무엇이든 뒤로 묶습니다. Pod가 죽고 새로 뜨면서 IP가 10.0.0.5에서 10.0.0.13으로 바뀌어도, 라벨만 같으면 Service는 그 Pod를 한 식구로 인식합니다.

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
  <text x="525" y="71" font-size="11" font-family="monospace" fill="#7b341e">labels: </text>
  <text x="585" y="71" font-size="11" font-family="monospace" font-weight="700" fill="#7b341e">app: nginx</text>
  <text x="722" y="48" text-anchor="end" font-size="11" font-weight="700" fill="#ff7849">선택</text>
  <rect x="510" y="105" width="220" height="60" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="525" y="128" font-size="12" font-weight="700" fill="#7b341e">Pod 2</text>
  <text x="525" y="151" font-size="11" font-family="monospace" fill="#7b341e">labels: </text>
  <text x="585" y="151" font-size="11" font-family="monospace" font-weight="700" fill="#7b341e">app: nginx</text>
  <text x="722" y="128" text-anchor="end" font-size="11" font-weight="700" fill="#ff7849">선택</text>
  <rect x="510" y="185" width="220" height="60" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.4" stroke-dasharray="4,3"/>
  <text x="525" y="208" font-size="12" font-weight="700" fill="#94a3b8">Pod 3</text>
  <text x="525" y="231" font-size="11" font-family="monospace" fill="#94a3b8">labels: </text>
  <text x="585" y="231" font-size="11" font-family="monospace" font-weight="700" fill="#94a3b8">app: db</text>
  <text x="722" y="208" text-anchor="end" font-size="11" font-weight="700" fill="#94a3b8">제외</text>
</svg>
</div>

*그림 5-2. selector가 지정한 라벨(app: nginx)을 가진 Pod만 매칭하고 다른 라벨은 제외*

라벨이 일치하는 Pod 두 대만 Service 뒤로 묶이고, 다른 라벨이 붙은 Pod는 명단에서 빠집니다. 어제 Deployment를 만들 때 `app: nginx` 라벨을 매겼던 이유가 여기서 회수됩니다. 그 라벨이 오늘은 Service의 식구 명부 역할을 합니다.

### 5.1.3 Service 타입과 접근 범위

YAML을 다 작성하기 전에 오픈이는 `type: NodePort` 한 줄에서 멈췄습니다.

*'NodePort 말고 다른 type도 있다는 거네. 어떤 차이가 있을까.'*

문서를 더 들여다보니, Service는 누구에게 문을 여느냐에 따라 세 종류로 나뉘어 있었습니다. 집에 비유하자면 셋 다 문이긴 한데, 누구에게 열려 있는지가 다릅니다. 가족끼리만 쓰는 방문이 **ClusterIP**, 초대장을 받은 손님에게만 알려주는 옆문 비밀번호가 **NodePort**, 누구나 들어올 수 있는 정문이 **LoadBalancer** 입니다.

#### ① ClusterIP

서비스 타입의 기본값입니다. 외부에서는 아예 접근이 불가능하며, 클러스터 내부의 Pod끼리 서로를 호출할 때만 사용합니다.

DB Pod 같은 경우가 여기에 해당합니다. 백엔드만 DB에 붙으면 되지, 외부 손님이 DB에 직접 들어올 일은 없습니다. 외부 노출이 필요 없는 구성에 ClusterIP를 씌우면, 안에서만 통하는 내선 번호가 생깁니다.

<div class="svg-figure">
<svg viewBox="0 0 760 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ClusterIP — 외부 접근은 차단되고 클러스터 내부 Pod끼리만 통신하는 구조">
  <defs>
    <marker id="cip-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
    <marker id="cip-x" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#dc2626"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">ClusterIP — 클러스터 안에서만 통신</text>
  <rect x="20" y="100" width="130" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="85" y="125" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">외부 Host</text>
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

*그림 5-3. ClusterIP는 외부 요청은 닿지 못하고 내부 Pod끼리만 통신*

#### ② NodePort

이번 실습에서 사용한 방식입니다. 노드(서버) 자체에 특정 포트를 열어 외부에서 들어올 수 있게 합니다.

YAML에 `nodePort: 30080`이라고 적으면 노드의 30080번 포트가 열립니다. 그 포트로 들어온 요청이 클러스터 내부의 Service로 흘러갑니다. 옆문 비밀번호 30080을 아는 손님만 들어올 수 있는 구조입니다. 다만 서비스가 늘어날수록 비밀번호가 30080, 30081, 30082처럼 줄줄이 늘어나서, 누가 어느 문을 쓰는지 외우는 일이 만만치 않아집니다.

<div class="svg-figure">
<svg viewBox="0 0 760 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="NodePort — 노드 IP의 특정 포트(30080)를 통해 외부에서 Service로 접근하는 구조">
  <defs>
    <marker id="np-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">NodePort — 노드 IP의 특정 포트로 외부 접근 허용</text>
  <rect x="20" y="100" width="130" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="85" y="125" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">외부 Host</text>
  <text x="85" y="145" text-anchor="middle" font-size="10" font-family="monospace" fill="#6b7280">노드IP:30080</text>
  <line x1="150" y1="130" x2="195" y2="130" stroke="#475569" stroke-width="1.8" marker-end="url(#np-p)"/>
  <rect x="195" y="50" width="555" height="160" rx="10" fill="#fff" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="6,4"/>
  <text x="210" y="71" font-size="11" font-weight="700" fill="#7b341e">Kubernetes 클러스터</text>
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

*그림 5-4. NodePort는 노드의 특정 포트로 외부 접근을 허용*

#### ③ LoadBalancer

실제 운영 환경에서 가장 흔히 쓰는 방식입니다. AWS나 GCP 같은 클라우드 위에서 돌리는 클러스터라면, 쿠버네티스가 클라우드 사업자에게 공인 IP 하나를 발급받아 Service에 붙여 줍니다. 사용자는 30080 같은 포트 번호를 따로 외울 필요가 없고, 발급된 IP나 도메인 하나로 곧장 들어옵니다.

다만 사용자 눈에 보이지 않는 안쪽에서는 NodePort와 ClusterIP가 함께 만들어집니다. LoadBalancer 타입은 그 위에 공인 IP를 한 겹 더 얹은 형태로, 외부 트래픽은 공인 IP → 노드의 NodePort → kube-proxy → Pod 순으로 흘러갑니다.

<div class="svg-figure">
<svg viewBox="0 0 760 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LoadBalancer — 공인 IP가 각 노드의 kube-proxy를 거쳐 Pod로 분산되며, Service는 클러스터 레벨 논리 리소스로 모든 노드에 걸쳐 존재">
  <defs>
    <marker id="lb-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">LoadBalancer — 공인 IP 하나로 여러 노드에 분산</text>
  <rect x="20" y="60" width="100" height="34" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="70" y="82" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">User 1</text>
  <rect x="20" y="118" width="100" height="34" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="70" y="140" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">User 2</text>
  <rect x="20" y="176" width="100" height="34" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="70" y="198" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">User 3</text>
  <text x="70" y="225" text-anchor="middle" font-size="10" font-family="monospace" fill="#6b7280">myapp.com</text>
  <line x1="120" y1="77" x2="148" y2="120" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <line x1="120" y1="135" x2="148" y2="140" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <line x1="120" y1="193" x2="148" y2="165" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <rect x="150" y="100" width="140" height="90" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8" stroke-dasharray="6,4"/>
  <text x="220" y="125" text-anchor="middle" font-size="11" font-weight="600" fill="#7b341e">Cloud Provider</text>
  <text x="220" y="148" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">LoadBalancer</text>
  <text x="220" y="172" text-anchor="middle" font-size="10" font-family="monospace" fill="#7b341e">공인 IP</text>
  <rect x="320" y="40" width="420" height="250" rx="10" fill="#fff" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="5,3"/>
  <text x="333" y="58" font-size="11" font-weight="700" fill="#7b341e">Kubernetes 클러스터</text>
  <rect x="325" y="70" width="55" height="210" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="352" y="175" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e" transform="rotate(-90 352 175)">Service</text>
  <line x1="290" y1="145" x2="323" y2="145" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <line x1="380" y1="107" x2="410" y2="107" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <line x1="380" y1="180" x2="410" y2="180" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <line x1="380" y1="253" x2="410" y2="253" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <rect x="410" y="75" width="320" height="65" rx="6" fill="#fff" stroke="#475569" stroke-width="1.2"/>
  <text x="425" y="93" font-size="10" font-weight="700" fill="#0f172a">Node 1</text>
  <rect x="425" y="100" width="155" height="32" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="502" y="120" text-anchor="middle" font-size="10" fill="#475569">kube-proxy (NodePort)</text>
  <line x1="582" y1="116" x2="600" y2="116" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <rect x="600" y="100" width="80" height="32" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="640" y="120" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Pod</text>
  <rect x="410" y="148" width="320" height="65" rx="6" fill="#fff" stroke="#475569" stroke-width="1.2"/>
  <text x="425" y="166" font-size="10" font-weight="700" fill="#0f172a">Node 2</text>
  <rect x="425" y="173" width="155" height="32" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="502" y="193" text-anchor="middle" font-size="10" fill="#475569">kube-proxy (NodePort)</text>
  <line x1="582" y1="189" x2="600" y2="189" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <rect x="600" y="173" width="80" height="32" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="640" y="193" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Pod</text>
  <rect x="410" y="221" width="320" height="65" rx="6" fill="#fff" stroke="#475569" stroke-width="1.2"/>
  <text x="425" y="239" font-size="10" font-weight="700" fill="#0f172a">Node 3</text>
  <rect x="425" y="246" width="155" height="32" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="502" y="266" text-anchor="middle" font-size="10" fill="#475569">kube-proxy (NodePort)</text>
  <line x1="582" y1="262" x2="600" y2="262" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <rect x="600" y="246" width="80" height="32" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="640" y="266" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Pod</text>
</svg>
</div>

*그림 5-5. LoadBalancer는 클라우드가 공인 IP를 발급해 여러 노드에 분산*

세 타입의 차이를 한 표로 정리하면 다음과 같습니다.

| 타입 | 접근 범위 | 사용 사례 |
|:----:|:---------|:---------|
| `ClusterIP` | 클러스터 내부만 | 백엔드·DB 등 외부 노출이 불필요한 서비스 |
| `NodePort` | 노드IP:포트로 외부 접근 가능 | 테스트 및 개발 환경 |
| `LoadBalancer` | 공인 IP로 외부 접근 가능 | 실제 클라우드 운영 환경 |

타입은 정리됐지만 YAML에 적힌 `port`, `targetPort`, `nodePort`라는 세 포트가 한 자리에 모여 있는 게 여전히 어색했습니다.

#### 포트 흐름

*'세 개가 다 80, 30080, 80인데 셋이 무슨 차이지.'*

다시 들여다보니 셋은 서로 주인이 다른 포트였습니다.

* `nodePort`는 노드(서버)의 포트입니다.
* `port`는 Service 자체의 포트입니다.
* `targetPort`는 실제 Pod의 포트입니다.

외부에서 Pod까지 닿는 라우팅 경로를 한 YAML에서 한꺼번에 선언하니, 자연히 세 단계가 줄지어 적히게 됩니다.

<div class="svg-figure">
<svg viewBox="0 0 760 420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="노드 큰 박스 안에 NodePort, Service, Pod가 자리하고 외부 사용자가 NodePort로 진입해 Service를 거쳐 Pod 안 컨테이너에 도달하는 구조">
  <defs>
    <marker id="nps-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
    <marker id="nps-o" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2937">노드 한 채 안에 자리한 NodePort, Service, Pod</text>
  <rect x="20" y="180" width="130" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="85" y="208" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">외부 사용자</text>
  <text x="85" y="228" text-anchor="middle" font-size="10" fill="#6b7280">브라우저</text>
  <rect x="220" y="60" width="520" height="340" rx="12" fill="#fff" stroke="#475569" stroke-width="2.4"/>
  <text x="240" y="84" font-size="13" font-weight="700" fill="#475569">Node (워커 서버)</text>
  <rect x="240" y="158" width="120" height="104" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <rect x="252" y="178" width="96" height="64" rx="6" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="300" y="205" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">NodePort</text>
  <text x="300" y="228" text-anchor="middle" font-size="13" font-family="monospace" font-weight="700" fill="#7b341e">:30080</text>
  <text x="300" y="254" text-anchor="middle" font-size="9" fill="#7b341e">노드 외벽 진입 자리</text>
  <path d="M 360 195 Q 385 170, 410 152" fill="none" stroke="#475569" stroke-width="1.8" marker-end="url(#nps-d)"/>
  <rect x="400" y="115" width="240" height="90" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="520" y="146" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">Service</text>
  <line x1="415" y1="160" x2="625" y2="160" stroke="#fde4d3" stroke-width="0.8"/>
  <text x="520" y="187" text-anchor="middle" font-size="15" font-family="monospace" font-weight="700" fill="#7b341e">:80 (port)</text>
  <line x1="520" y1="205" x2="520" y2="252" stroke="#475569" stroke-width="2" marker-end="url(#nps-d)"/>
  <text x="680" y="230" text-anchor="middle" font-size="10" font-style="italic" fill="#475569">selector 매칭</text>
  <rect x="400" y="258" width="240" height="125" rx="8" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  <text x="415" y="278" font-size="11" font-weight="700" fill="#475569">Pod</text>
  <rect x="425" y="295" width="190" height="78" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.4"/>
  <text x="520" y="320" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">컨테이너 (nginx)</text>
  <text x="520" y="350" text-anchor="middle" font-size="14" font-family="monospace" font-weight="700" fill="#0f6f3f">:80 (targetPort)</text>
  <line x1="150" y1="210" x2="237" y2="210" stroke="#ff7849" stroke-width="2.6" marker-end="url(#nps-o)"/>
  <text x="190" y="200" text-anchor="middle" font-size="12" font-family="monospace" font-weight="700" fill="#7b341e">노드IP:30080</text>
</svg>
</div>

*그림 5-6. 노드 안에 NodePort, Service, Pod가 자리하고 외부 사용자가 NodePort로 진입해 Service를 거쳐 Pod 안 컨테이너에 닿는 구조*

| 포트 종류 | 소유 주체 | 역할 | 생략 시 |
|:--------:|:---------|:-----|:-------|
| `nodePort` | 노드(서버) | 외부에서 노드 IP로 접근할 때 열리는 포트 | 30000~32767 중 자동 할당 |
| `port` | Service | 클러스터 내부에서 Service를 부를 때 쓰는 포트 | 생략 불가 (필수) |
| `targetPort` | Pod(컨테이너) | 컨테이너 앱이 사용하는 포트와 일치해야 함 | `port` 값과 동일하게 설정 |

### 5.1.4 외부에서 Service 접속해 보기

Service가 정말 고정 진입점 역할을 하는지 직접 확인해야 어제 막혔던 자리가 풀립니다. 외부에서 들어가 보고, Pod가 죽고 IP가 바뀌어도 같은 주소로 닿는지 차례로 시험해 보겠습니다.

이제 작성한 YAML을 클러스터에 적용해 보겠습니다.

```bash
kubectl apply -f ex11/service-ex01.yml   # Service YAML 적용
```

<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">실행결과</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-key">$</span> <span class="tl-str">kubectl apply -f ex11/service-ex01.yml</span></div>
    <div>service/nginx-service created</div>
  </div>
</div>

*그림 5-7. Service 생성 결과*

`nginx-service created`라는 한 줄이 떴습니다. 이제 동료에게 보여줄 주소가 생긴 것 같았습니다. 오픈이는 곧장 브라우저를 열고 `localhost:30080`을 입력했습니다.

화면이 멈춰 있었습니다. 빈 페이지가 한참 동안 그대로였습니다.

*'분명 30080 포트를 열었는데 왜 안 들어가지.'*

번뜩, 어제 미니큐브를 처음 띄울 때 봤던 메시지가 떠올랐습니다. 미니큐브는 컴퓨터 안에서 가상 환경을 한 겹 두르고 돌아갑니다. 노트북이 사는 동네와 미니큐브가 사는 동네가 서로 다른 네트워크라, 30080을 미니큐브 쪽에 열어 두었어도 노트북 쪽에서는 그 포트가 보이지 않습니다.

:::note
**미니큐브는 왜 localhost로 바로 접속되지 않을까요**

미니큐브는 컴퓨터 내부의 가상 환경(VM 또는 컨테이너)에서 돌아갑니다. 즉, 미니큐브라는 가상 세계와 우리 PC라는 현실 세계가 별도의 네트워크로 분리되어 있습니다. 그래서 도커가 포트포워딩으로 호스트와 컨테이너를 연결했던 것처럼, 미니큐브 환경과 PC 사이에도 별도의 통로가 필요합니다.
:::

다행히 미니큐브는 두 동네를 잇는 통로를 만드는 명령어를 따로 마련해 두고 있습니다.

| 방법 | 명령어 | 설명 |
|:------:|:-----|:-----|
| URL 생성 | `minikube service <서비스이름> --url` | NodePort 또는 LoadBalancer 타입의 Service에 접근할 수 있는 URL 생성 |
| 터널 개방 | `minikube tunnel` | LoadBalancer 타입 서비스에 외부 IP 부여 |
| 포트 포워딩 | `kubectl port-forward service/<서비스이름> 8080:80` | 호스트 포트와 서비스 포트를 직접 연결 |

NodePort 타입에는 `minikube service --url`이 가장 간단합니다. 한 번 실행하면 노트북에서 들어갈 수 있는 URL을 발급해 줍니다.

```bash
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

*그림 5-8. minikube service URL 생성 결과*

URL이 한 줄 떴고 커서는 그대로 멈춰 있습니다. 이 명령어는 통로를 살려두기 위해 터미널을 점유한 채로 머물러 있습니다. 발급된 주소를 그대로 브라우저에 붙여 넣자, 익숙한 NGINX 환영 페이지가 모니터에 가득 찼습니다.

![](../assets/CH04/chap03-44.png)

*그림 5-9. 브라우저에서 nginx 접속 확인*

이번엔 Pod 변동을 시험해 볼 차례였습니다. Pod가 죽고 IP가 바뀌어도 Service 뒤로 새 Pod가 자동 연결되는지 직접 보기로 했습니다. 오픈이는 통로를 닫고 Pod를 전부 지웠습니다. Deployment가 살아 있으니 곧 새 Pod가 자동으로 올라왔습니다.

```bash
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
    <div>pod "nginx-replica-756b46b54c-7qztnx" deleted from default namespace</div>
    <div>pod "nginx-replica-756b46b54c-cb592" deleted from default namespace</div>
    <div>pod "nginx-replica-756b46b54c-ff5dt" deleted from default namespace</div>
    <div>pod "nginx-replica-756b46b54c-hpnzm" deleted from default namespace</div>
    <div><span class="tl-key">$</span> <span class="tl-str">minikube service nginx-service --url</span></div>
    <div>http://127.0.0.1:3082</div>
    <div>! windows 에서 Docker 드라이버를 사용하고 있기 때문에, 터미널을 열어야 실행할 수 있습니다.</div>
  </div>
</div>

*그림 5-10. Pod 삭제 후 Service 접속 확인*

새 URL로 접속하니 NGINX 페이지가 그대로 떴습니다. Pod IP가 전부 바뀌었어도 Service는 새 Pod에 이미 연결되어 있었습니다.

*'와, 진짜네. Pod가 새로 만들어지면 IP가 바뀌었을 텐데. Service가 뒤에서 주소를 알아서 연결해주는구나.'*

## 5.2 Ingress - 도메인 라우팅

### 5.2.1 Service의 한계

그때 옆자리 의자가 다시 굴러왔습니다. 동료가 화면을 살피며 "이 주소로 사람들이 쉽게 들어올 수 있겠어요?"라고 물었습니다.

오픈이는 발급된 `127.0.0.1:10345`를 다시 봤습니다. 터미널을 닫는 순간 사라지는 주소였습니다. 다시 띄울 때마다 포트도 바뀌었습니다.

*'안에서는 Service로 묶었는데, 밖에서 들어올 입구는 아직 임시구나.'*

Service를 하나 더 띄우면 입구도 또 하나 늘어납니다. 손님 입장에서 입구가 두 개, 세 개로 늘어난다는 뜻입니다. 그렇다고 임시 포트를 사람마다 알려 줄 수도 없습니다.

*'도커 때 NGINX가 그 자리에 있었지.'*

도커에서는 NGINX가 손님 앞에 서서 같은 도메인 아래 경로별로 뒤쪽 서버를 갈라 보내 줬습니다. 쿠버네티스에서도 그 자리가 필요합니다.

Service YAML을 처음부터 끝까지 다시 훑어봐도 경로별 라우팅 항목은 보이지 않았습니다. Service는 라벨로 Pod를 묶을 줄만 알지, URL 경로를 보고 갈래를 나누는 일은 하지 않습니다.

*'Service 안에는 그런 기능이 없으니, 그 일을 맡는 다른 리소스가 따로 있는 건가.'*

쿠버네티스 문서를 검색하다 곧 답이 나왔습니다. 그 자리를 맡는 전용 리소스의 이름이 **Ingress**였습니다.

### 5.2.2 Ingress의 역할

Service는 Pod 그룹마다 고정 진입점을 만들어 줍니다. 그러면 외부에서 들어올 때 Service의 수만큼 진입점을 알아야 합니다. 외부 도메인 하나로 들어와도 안에서 알아서 갈라져 가는 구조가 필요합니다.

**Ingress**가 이 분기를 자동으로 처리합니다. 외부 도메인 하나로 들어온 요청의 URL 경로를 보고 어느 Service로 보낼지 결정합니다. 우체국 물류 센터의 작업자가 우편의 바코드를 찍고 어느 우체국으로 보낼지 정해 주는 것과 같습니다.

<div class="svg-figure">
<svg viewBox="0 0 760 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ingress가 도메인과 경로를 읽어 적절한 Service로 요청을 분기하는 구조">
  <defs>
    <marker id="ir-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">Ingress — 경로를 읽어 요청을 Service로 분기</text>
  <g transform="translate(60, 110)">
    <circle cx="0" cy="0" r="14" fill="#fff" stroke="#475569" stroke-width="1.6"/>
    <path d="M -22 35 Q -22 12 0 12 Q 22 12 22 35 L 22 55 L -22 55 Z" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  </g>
  <text x="60" y="195" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">고객</text>
  <line x1="90" y1="120" x2="200" y2="120" stroke="#475569" stroke-width="1.6" marker-end="url(#ir-p)"/>
  <text x="145" y="112" text-anchor="middle" font-size="10" font-style="italic" fill="#6b7280">/order, /stores</text>
  <rect x="200" y="90" width="170" height="60" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="285" y="115" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">Ingress</text>
  <text x="285" y="135" text-anchor="middle" font-size="10" fill="#7b341e">경로 읽음</text>
  <line x1="370" y1="105" x2="555" y2="65" stroke="#475569" stroke-width="1.6" marker-end="url(#ir-p)"/>
  <text x="465" y="78" text-anchor="middle" font-size="11" font-family="monospace" font-weight="700" fill="#0f172a">/order</text>
  <line x1="370" y1="135" x2="555" y2="175" stroke="#475569" stroke-width="1.6" marker-end="url(#ir-p)"/>
  <text x="465" y="162" text-anchor="middle" font-size="11" font-family="monospace" font-weight="700" fill="#0f172a">/stores</text>
  <rect x="560" y="40" width="170" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="645" y="70" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">order-service</text>
  <rect x="560" y="160" width="170" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="645" y="190" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">stores-service</text>
</svg>
</div>

*그림 5-11. Ingress가 도메인과 경로를 읽어 요청을 적절한 Service로 연결하는 구조*

:::term-box
**Ingress**: 클러스터 외부의 HTTP/HTTPS 요청을 도메인과 URL 경로 기준으로 내부 Service에 연결하는 라우팅 규칙입니다. Service가 개별 Pod 그룹의 고정 주소를 제공한다면, Ingress는 여러 Service를 하나의 진입점으로 묶어 줍니다.
:::

Service는 Pod 묶음 하나에 대표 번호를 달고, Ingress는 그 대표 번호 여러 개를 묶어 손님 쪽 진입을 한 곳으로 통일합니다. 한 단계 위에 또 한 명의 문지기를 두는 구조라, 외부 도메인 하나에 여러 Service를 매달 수 있습니다.

*'외부 진입점 하나로 다 묶을 수 있다는 거네. 직접 띄워 봐야 감이 오겠다.'*

### 5.2.3 Ingress 적용하기

:::tip
전체 실습 코드는 깃헙을 참고합니다.

**실습 코드 (GitHub)**: https://github.com/metacoding-10-linux-docker/docker/tree/master/ex12
:::

문서의 첫 줄을 읽던 오픈이의 눈이 한 곳에서 멈췄습니다.

> "인그레스 컨트롤러가 있어야 인그레스를 충족할 수 있다. 인그레스 리소스만 생성한다면 효과가 없다."

*'인그레스 리소스 말고 컨트롤러라는 게 또 따로 있어야 한다고?'*

Ingress는 두 가지로 분리됩니다. 라우팅 규칙을 적은 **리소스(YAML)** 가 물류 센터의 주소 사전 역할을 하고, 그 사전을 읽고 외부 트래픽을 실제로 처리하는 **컨트롤러(Pod)** 가 물류 센터 본체 역할을 합니다.

주소 사전만 펼쳐 두고 물류 센터가 꺼져 있으면 우편이 그대로 쌓일 뿐입니다. 규칙(리소스)과 실행(컨트롤러)이 함께 떠 있어야 라우팅이 작동합니다.

<div class="svg-figure">
<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ingress 리소스(YAML 선언)와 Ingress Controller(Pod 집행) — 선언과 집행의 분리">
  <defs>
    <marker id="rc-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">Ingress 리소스(YAML, 선언) ↔ Controller(Pod, 집행)</text>
  <rect x="40" y="60" width="300" height="140" rx="8" fill="#fff" stroke="#dc2626" stroke-width="1.8"/>
  <path d="M 48 60 H 332 Q 340 60 340 68 V 82 H 40 V 68 Q 40 60 48 60 Z" fill="#dc2626"/>
  <text x="190" y="76" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">집행 · 실제 요청 처리</text>
  <text x="190" y="110" text-anchor="middle" font-size="14" font-weight="700" fill="#b91c1c">Ingress Controller</text>
  <text x="190" y="128" text-anchor="middle" font-size="10" fill="#7b341e">클러스터 안에서 도는 Pod</text>
  <circle cx="170" cy="148" r="6" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <circle cx="190" cy="148" r="6" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <circle cx="210" cy="148" r="6" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="190" y="180" text-anchor="middle" font-size="10" fill="#475569">외부 요청을 규칙대로 Service에 전달</text>
  <rect x="420" y="60" width="300" height="140" rx="8" fill="#fff" stroke="#1565c0" stroke-width="1.8"/>
  <path d="M 428 60 H 712 Q 720 60 720 68 V 82 H 420 V 68 Q 420 60 428 60 Z" fill="#1565c0"/>
  <text x="570" y="76" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">선언 · 라우팅 규칙</text>
  <text x="570" y="110" text-anchor="middle" font-size="14" font-weight="700" fill="#1565c0">Ingress 리소스</text>
  <text x="570" y="128" text-anchor="middle" font-size="10" fill="#1e40af">YAML 문서</text>
  <text x="570" y="155" text-anchor="middle" font-size="11" font-family="monospace" fill="#0f172a">path: /order → order-service</text>
  <text x="570" y="175" text-anchor="middle" font-size="11" font-family="monospace" fill="#0f172a">path: /stores → stores-service</text>
  <line x1="416" y1="130" x2="345" y2="130" stroke="#475569" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#rc-p)"/>
  <text x="380" y="120" text-anchor="middle" font-size="11" font-style="italic" font-weight="600" fill="#475569">규칙을 읽음</text>
</svg>
</div>

*그림 5-12. Ingress 리소스(선언)와 Ingress Controller(집행)의 분리*

| 구성 요소 | 역할 | 비유 | 쿠버네티스 철학 |
|:---------:|:-----|:-----|:---------------|
| `Ingress 리소스` | 라우팅 규칙을 정의한 문서 (YAML) | 주소 사전 | `선언` |
| `Ingress Controller` | 외부 요청을 처리하는 소프트웨어 | 우편물 집중국 본체 | `집행` |

*'아, 규칙만 적어 둔다고 알아서 굴러가는 게 아니구나. 그 규칙을 읽고 실제로 실행해 주는 역할이 따로 필요한 거네.'*

실습을 위해 미니큐브에 인그레스를 활성화해 보겠습니다. 미니큐브는 Ingress Controller를 애드온 형태로 한 번에 띄울 수 있는 명령어를 제공합니다.

```bash
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

*그림 5-13. minikube에서 ingress 애드온 활성화 과정*

마지막 줄에 `'ingress' addon is enabled`가 떴습니다. 컨트롤러 Pod가 실제로 떠 있는지 한 번 더 확인합니다.

```bash
kubectl get pods -n ingress-nginx        # 컨트롤러 Pod 확인
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
    <div>ingress-nginx-admission-create-zg9hh        0/1     Completed   0          52m</div>
    <div>ingress-nginx-admission-patch-bvxlw         0/1     Completed   1          52m</div>
    <div>ingress-nginx-controller-9cc49f96f-qrpm7    1/1     Running     0          52m</div>
  </div>
</div>

*그림 5-14. Ingress Controller Pod가 Running 상태임을 확인*

`ingress-nginx-controller`가 `1/1 Running` 상태입니다. 물류 센터가 가동되어 우편을 받을 준비를 마쳤다는 뜻입니다.

:::note
**실제 운영 환경에서의 Ingress Controller**

미니큐브 애드온은 학습용 명령어입니다. 실제로는 `ingress-nginx` 같은 컨트롤러를 직접 설치하거나 클라우드 서비스가 제공하는 전용 컨트롤러를 사용합니다. 방식의 차이일 뿐, 클러스터 내부에서 컨트롤러 Pod가 요청을 분산하는 구조는 동일합니다.
:::

#### ① 두 서비스 준비

이제 들어온 요청을 받아 처리할 Service를 띄울 차례입니다. 주문 쪽과 매장 쪽을 각각 ClusterIP Service로 만들겠습니다. 두 Service는 같은 이미지(`hashicorp/http-echo`)를 쓰는데, `-text` 옵션으로 응답 문구만 달리 줍니다. 주문 쪽은 `"주문 접수 완료"`, 매장 쪽은 `"매장 선택"`이 돌아옵니다.

`ex12/` 안에는 주문과 매장 각각 **Pod를 띄우는 Deployment** 와 그 Pod를 묶는 **ClusterIP Service** 가 한 쌍씩 들어 있습니다.

| 파일 | 종류 | 역할 |
|:----:|:-----|:-----|
| `order-deploy.yml` | Deployment | 주문 응답 Pod ("주문 접수 완료") |
| `order-service.yml` | Service (ClusterIP) | 주문 Pod를 묶는 내부 창구 (port 5678) |
| `stores-deploy.yml` | Deployment | 매장 응답 Pod ("매장 선택") |
| `stores-service.yml` | Service (ClusterIP) | 매장 Pod를 묶는 내부 창구 (port 5678) |

두 Service 모두 ClusterIP 타입이라 클러스터 바깥에서는 직접 접근할 수 없습니다. 부서 내선 같은 자리라, 손님이 직접 그 번호를 누르지는 못합니다. 손님 쪽 요청을 받아서 이 둘로 갈라 보낼 Ingress 규칙이 필요합니다.

#### ② 규칙 문서 작성

이제 컨트롤러에게 어떤 경로를 어디로 보낼지 정의한 지침서를 전달할 차례입니다.

**ex12/ingress-ex01.yml**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ex12-ingress
spec:
  ingressClassName: nginx           # 어느 Controller가 이 규칙을 집행할지 지정
  rules:
    - http:
        paths:
          - path: /order            # 주문 경로 → order-service
            pathType: Prefix
            backend:
              service:
                name: order-service
                port:
                  number: 5678
          - path: /stores           # 매장 경로 → stores-service
            pathType: Prefix
            backend:
              service:
                name: stores-service
                port:
                  number: 5678
```

`rules` 아래 두 개의 `path`가 있고, 각 경로가 서로 다른 Service를 가리킵니다. 우체국 비유로 옮기면, 이 YAML이 물류 센터의 주소 사전입니다. `/order`로 들어오면 주문 Service로, `/stores`로 들어오면 매장 Service로 돌리라는 두 줄짜리 지침이 적혀 있습니다. 이미 가동된 물류 센터(컨트롤러 Pod)가 이 지침을 읽고 실제 트래픽을 분류해 보냅니다.

오픈이는 `ex12/` 폴더의 모든 파일을 적용해 두 Service와 Ingress 규칙을 한 번에 등록했습니다.

```bash
kubectl apply -f ex12/
kubectl get ingress                     # 등록된 인그레스 확인
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
    <div><span class="tl-key">$</span> <span class="tl-str">kubectl get ingress</span></div>
    <div>NAME           CLASS   HOSTS   ADDRESS   PORTS   AGE</div>
    <div>ex12-ingress   nginx   *                 80      37s</div>
  </div>
</div>

*그림 5-15. Ingress 리소스 등록 확인*

#### ③ 브라우저로 접속

가상 세계와 원활히 통신하기 위해 별도 터미널에서 `minikube tunnel`을 실행합니다.

```bash
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

*그림 5-16. minikube tunnel 실행 화면*

이제 브라우저에서 경로별로 직접 접속해 보겠습니다.

* `http://localhost/order` → "주문 접수 완료"
* `http://localhost/stores` → "매장 선택"

<!-- [CAPTURE NEEDED: 브라우저에서 http://localhost/order 접속 시 "주문 접수 완료" 응답 확인 화면. 자산 경로: assets/CH05/mock-order-page.png] -->
![](../assets/CH05/mock-order-page.png)

*그림 5-17. /order 접속 결과 - "주문 접수 완료"*

<!-- [CAPTURE NEEDED: 브라우저에서 http://localhost/stores 접속 시 "매장 선택" 응답 확인 화면. 자산 경로: assets/CH05/mock-stores-page.png] -->
![](../assets/CH05/mock-stores-page.png)

*그림 5-18. /stores 접속 결과 - "매장 선택"*

같은 도메인인데 뒤에 붙는 경로 한 글자에 따라 응답이 갈라집니다. `localhost` 한 곳으로만 들어오는데도 누른 경로에 따라 주문 Service와 매장 Service로 정확히 갈라집니다. Ingress가 URL 경로를 읽고 알맞은 Service로 트래픽을 분기해 준 결과입니다.

동료가 등 뒤로 와서 화면을 들여다봤습니다.

**동료**: "이번엔 주소 하나만 알려 주면 되는 거예요?"

오픈이는 `localhost/order`와 `localhost/stores`를 차례로 적어 줬습니다. 이번에는 포트 번호도 없고, 따로 외울 IP도 없었습니다.

## 5.3 브라우저에서 Pod까지의 경로

오후 늦게 옥상에 잠깐 올라갔습니다. 바람을 맞으며 머릿속 그림을 다시 한 번 정리하고 싶었기 때문입니다. NodePort, kube-proxy, Ingress Controller, ClusterIP. 이름은 다 들어봤는데 한 줄로 늘어놓고 보면 누가 어디에 서서 무얼 하는지가 흐릿합니다.

자리로 돌아와 흰 종이를 한 장 꺼냈습니다. 통합 사이트의 *브라우저에서 Pod까지* 한 번 죽 그어 봤습니다. 한 자리에 너무 많은 컴포넌트가 모이지 않게, 일을 세 단계로 잘랐습니다.

<div class="svg-figure">
<svg viewBox="0 0 1080 600" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="요청이 Pod까지 닿는 전체 흐름 — 세 단계가 클러스터 안에서 일어나는 위치">
  <defs>
    <marker id="ov-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#94a3b8"/></marker>
    <marker id="ov-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="ov-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="540" y="26" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2937">전체 흐름 한눈에 — 세 단계가 일어나는 위치</text>
  <text x="20" y="120" font-size="10" font-weight="600" fill="#475569">로컬호스트</text>
  <rect x="20" y="130" width="130" height="100" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="85" y="186" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">Host</text>
  <line x1="150" y1="170" x2="232" y2="170" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <circle cx="190" cy="153" r="11" fill="#ff7849"/>
  <text x="190" y="157" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">1</text>
  <rect x="200" y="80" width="860" height="500" rx="10" fill="none" stroke="#475569" stroke-width="1.4" stroke-dasharray="6,4"/>
  <text x="630" y="100" text-anchor="middle" font-size="11" font-style="italic" fill="#475569">쿠버네티스 가상세계 (클러스터)</text>
  <rect x="235" y="110" width="135" height="135" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="302" y="128" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">클러스터 입구</text>
  <rect x="252" y="142" width="100" height="70" rx="6" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="302" y="170" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">NodePort</text>
  <text x="302" y="190" text-anchor="middle" font-size="12" font-family="monospace" fill="#7b341e">:30080</text>
  <text x="302" y="234" text-anchor="middle" font-size="9" fill="#7b341e">NodePort Service</text>
  <line x1="370" y1="170" x2="490" y2="170" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <rect x="490" y="150" width="100" height="40" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="540" y="174" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Kube Proxy</text>
  <line x1="590" y1="170" x2="640" y2="170" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <rect x="640" y="150" width="180" height="40" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="730" y="174" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Ingress Controller</text>
  <rect x="900" y="135" width="140" height="80" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="970" y="160" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">API Server</text>
  <text x="970" y="180" text-anchor="middle" font-size="10" fill="#7b341e">Ingress·Service·Pod 정보</text>
  <line x1="822" y1="160" x2="898" y2="155" stroke="#475569" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#ov-s)"/>
  <line x1="898" y1="195" x2="822" y2="190" stroke="#ff7849" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#ov-a)"/>
  <rect x="420" y="245" width="600" height="65" rx="32" fill="#f5faff" stroke="#bfdbfe" stroke-width="1"/>
  <text x="1005" y="260" text-anchor="end" font-size="10" font-weight="700" fill="#94a3b8">L7</text>
  <line x1="730" y1="190" x2="600" y2="245" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <line x1="730" y1="190" x2="850" y2="245" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <circle cx="660" cy="218" r="11" fill="#ff7849"/>
  <text x="660" y="222" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">2</text>
  <text x="600" y="259" text-anchor="middle" font-size="9" font-weight="600" fill="#7b341e">ClusterIP</text>
  <rect x="540" y="262" width="120" height="32" rx="16" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="600" y="283" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">order-service</text>
  <text x="850" y="259" text-anchor="middle" font-size="9" font-weight="600" fill="#7b341e">ClusterIP</text>
  <rect x="790" y="262" width="120" height="32" rx="16" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="850" y="283" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">stores-service</text>
  <line x1="600" y1="310" x2="600" y2="335" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <line x1="850" y1="310" x2="850" y2="335" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <rect x="420" y="335" width="600" height="100" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="1005" y="350" text-anchor="end" font-size="10" font-weight="700" fill="#94a3b8">L4</text>
  <rect x="490" y="365" width="220" height="55" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="505" y="382" font-size="10" font-weight="700" fill="#7b341e">Node 1</text>
  <text x="695" y="382" text-anchor="end" font-size="9" font-family="monospace" fill="#7b341e">port :30080</text>
  <rect x="555" y="390" width="100" height="22" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="605" y="405" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">Kube Proxy</text>
  <rect x="740" y="365" width="220" height="55" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="755" y="382" font-size="10" font-weight="700" fill="#7b341e">Node 2</text>
  <text x="945" y="382" text-anchor="end" font-size="9" font-family="monospace" fill="#7b341e">port :30080</text>
  <rect x="805" y="390" width="100" height="22" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="855" y="405" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">Kube Proxy</text>
  <rect x="225" y="375" width="120" height="55" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="285" y="397" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Endpoint</text>
  <text x="285" y="412" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Controller</text>
  <line x1="345" y1="397" x2="555" y2="402" stroke="#475569" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ov-s)"/>
  <line x1="345" y1="420" x2="555" y2="473" stroke="#475569" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ov-s)"/>
  <line x1="605" y1="412" x2="585" y2="450" stroke="#ff7849" stroke-width="2.2" stroke-dasharray="3,2" marker-end="url(#ov-a)"/>
  <line x1="605" y1="412" x2="635" y2="450" stroke="#ff7849" stroke-width="2.2" stroke-dasharray="3,2" marker-end="url(#ov-a)"/>
  <line x1="855" y1="412" x2="835" y2="450" stroke="#ff7849" stroke-width="2.2" stroke-dasharray="3,2" marker-end="url(#ov-a)"/>
  <line x1="855" y1="412" x2="885" y2="450" stroke="#ff7849" stroke-width="2.2" stroke-dasharray="3,2" marker-end="url(#ov-a)"/>
  <circle cx="730" cy="430" r="11" fill="#ff7849"/>
  <text x="730" y="434" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">3</text>
  <rect x="510" y="453" width="200" height="40" rx="6" fill="none" stroke="#ff7849" stroke-width="1.4" stroke-dasharray="4,3"/>
  <rect x="525" y="461" width="65" height="24" rx="12" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="557" y="477" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">Pod A</text>
  <rect x="615" y="461" width="65" height="24" rx="12" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="647" y="477" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">Pod A</text>
  <rect x="760" y="453" width="200" height="40" rx="6" fill="none" stroke="#ff7849" stroke-width="1.4" stroke-dasharray="4,3"/>
  <rect x="775" y="461" width="65" height="24" rx="12" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="807" y="477" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">Pod B</text>
  <rect x="865" y="461" width="65" height="24" rx="12" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="897" y="477" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">Pod B</text>
  <line x1="610" y1="493" x2="710" y2="525" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,2"/>
  <line x1="850" y1="493" x2="780" y2="525" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,2"/>
  <rect x="610" y="525" width="270" height="35" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <text x="745" y="547" text-anchor="middle" font-size="11" font-weight="600" fill="#94a3b8">Deployment</text>
</svg>
</div>

*그림 5-19. 요청이 Pod까지 닿는 전체 흐름 - 세 단계가 일어나는 위치*

세 단계는 우편이 발신자의 손을 떠나 받는 사람의 우편함에 닿기까지의 길과 닮아 있었습니다. 발신자가 우체국 입구로 들어가 창구 직원에게 우편을 맡기면 직원이 송장을 붙입니다(1단계). 송장이 붙은 우편이 물류 센터에 도착해 바코드를 찍어 어느 우체국으로 보낼지 정합니다(2단계). 결정된 우체국에서 그 동네 집배원이 받는 주소를 보고 우편함에 우편을 넣습니다(3단계). 통합 사이트도 똑같습니다. 브라우저가 도메인을 누르면 클러스터 입구를 통과하고, Ingress Controller가 경로를 보고 어느 Service인지 정하고, 노드의 kube-proxy가 살아있는 Pod 한 대로 패킷을 건넵니다.

### 5.3.1 1단계 진입 - 우체국 입구에서 송장을 붙인다

발신자가 우편을 들고 동네 우체국 **입구**로 들어갑니다. 안쪽 **창구 직원**에게 우편을 맡기면, 직원이 우편에 **송장**을 붙입니다. 송장에는 우편이 어느 물류 센터로 갈지가 새겨집니다. 발신자는 우편이 그 다음 어떻게 옮겨지는지 알 필요가 없습니다.

<div class="svg-figure">
<svg viewBox="0 0 800 270" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="1단계 비유 — 발신자가 우체국 입구로 들어가 창구 직원에게 우편을 맡기고 직원이 송장을 붙임">
  <defs>
    <marker id="m1n-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="400" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">창구 직원이 우편에 송장을 붙이는 순간</text>
  <!-- 좌측: 우체국 입구 (축소) -->
  <g transform="translate(20, 130)">
    <rect x="0" y="0" width="70" height="75" rx="4" fill="#fff" stroke="#7b341e" stroke-width="1.4"/>
    <path d="M -2 0 L 72 0 L 72 -8 L -2 -8 Z" fill="#7b341e"/>
    <rect x="28" y="30" width="14" height="20" rx="2" fill="#7b341e"/>
    <text x="35" y="70" text-anchor="middle" font-size="9" font-weight="600" fill="#7b341e">입구</text>
  </g>
  <!-- 발신자 -->
  <g transform="translate(5, 165)">
    <circle cx="10" cy="0" r="8" fill="#fff" stroke="#475569" stroke-width="1.2"/>
    <path d="M 0 10 Q 0 22 10 22 Q 20 22 20 10 L 20 40 L 0 40 Z" fill="#fff4ed" stroke="#475569" stroke-width="1.2"/>
  </g>
  <text x="15" y="220" text-anchor="middle" font-size="8" fill="#94a3b8">발신자</text>
  <!-- 화살표: 입구로 -->
  <path d="M 20 185 L 95 185" stroke="#ff7849" stroke-width="1.6" marker-end="url(#m1n-a)"/>
  <!-- 가운데: 창구 카운터 (큼지막하게) -->
  <g transform="translate(200, 85)">
    <!-- 카운터 테이블 -->
    <rect x="0" y="0" width="160" height="100" rx="4" fill="#fff" stroke="#7b341e" stroke-width="2"/>
    <line x1="0" y1="28" x2="160" y2="28" stroke="#7b341e" stroke-width="1.2"/>
    <text x="80" y="20" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">창구 카운터</text>
    <!-- 송장 부착 라벨 -->
    <text x="80" y="-4" text-anchor="middle" font-size="10" font-style="italic" font-weight="700" fill="#dc2626">송장 부착!</text>
    <!-- 우편 (카운터 가운데에 크게) -->
    <g transform="translate(18, 45)">
      <rect x="0" y="0" width="78" height="48" rx="2" fill="#fef3c7" stroke="#d97706" stroke-width="1.6"/>
      <line x1="0" y1="0" x2="39" y2="24" stroke="#d97706" stroke-width="1.2"/>
      <line x1="78" y1="0" x2="39" y2="24" stroke="#d97706" stroke-width="1.2"/>
    </g>
    <!-- 송장 (흰 종이 + 빨간 테두리 + 검은 바코드, 우편 우상단에 비스듬히 붙음) -->
    <g transform="translate(60, 36) rotate(-6)">
      <!-- 효과선 (방금 막 붙은 표시) -->
      <line x1="-3" y1="-4" x2="-7" y2="-10" stroke="#dc2626" stroke-width="1.6"/>
      <line x1="24" y1="-6" x2="24" y2="-13" stroke="#dc2626" stroke-width="1.6"/>
      <line x1="50" y1="-4" x2="55" y2="-10" stroke="#dc2626" stroke-width="1.6"/>
      <!-- 송장 라벨 (흰 종이 + 빨간 테두리) -->
      <rect x="0" y="0" width="48" height="34" rx="2" fill="#fff" stroke="#dc2626" stroke-width="2.2"/>
      <text x="24" y="10" text-anchor="middle" font-size="7" font-weight="700" fill="#dc2626">송장</text>
      <line x1="3" y1="13" x2="45" y2="13" stroke="#dc2626" stroke-width="0.4"/>
      <!-- 바코드 (검은 줄무늬) -->
      <line x1="5" y1="17" x2="5" y2="30" stroke="#0f172a" stroke-width="0.8"/>
      <line x1="8" y1="17" x2="8" y2="30" stroke="#0f172a" stroke-width="1.4"/>
      <line x1="11" y1="17" x2="11" y2="30" stroke="#0f172a" stroke-width="0.6"/>
      <line x1="14" y1="17" x2="14" y2="30" stroke="#0f172a" stroke-width="1.2"/>
      <line x1="17" y1="17" x2="17" y2="30" stroke="#0f172a" stroke-width="0.8"/>
      <line x1="20" y1="17" x2="20" y2="30" stroke="#0f172a" stroke-width="1.4"/>
      <line x1="23" y1="17" x2="23" y2="30" stroke="#0f172a" stroke-width="0.6"/>
      <line x1="26" y1="17" x2="26" y2="30" stroke="#0f172a" stroke-width="1.2"/>
      <line x1="29" y1="17" x2="29" y2="30" stroke="#0f172a" stroke-width="0.8"/>
      <line x1="32" y1="17" x2="32" y2="30" stroke="#0f172a" stroke-width="1.4"/>
      <line x1="35" y1="17" x2="35" y2="30" stroke="#0f172a" stroke-width="0.6"/>
      <line x1="38" y1="17" x2="38" y2="30" stroke="#0f172a" stroke-width="1.2"/>
      <line x1="41" y1="17" x2="41" y2="30" stroke="#0f172a" stroke-width="0.8"/>
    </g>
    <!-- 창구 직원 (오른쪽, 왼팔 뻗어 송장 위에 손) -->
    <g transform="translate(128, 38)">
      <!-- 머리 -->
      <circle cx="0" cy="0" r="11" fill="#fff" stroke="#475569" stroke-width="1.4"/>
      <!-- 몸 -->
      <path d="M -14 12 Q -14 32 0 32 Q 14 32 14 12 L 14 52 L -14 52 Z" fill="#fff4ed" stroke="#475569" stroke-width="1.4"/>
      <!-- 왼팔 (어깨에서 송장 쪽으로 뻗음) -->
      <line x1="-12" y1="14" x2="-32" y2="20" stroke="#475569" stroke-width="2.6" stroke-linecap="round"/>
      <!-- 손 (송장 위에 닿음) -->
      <circle cx="-34" cy="20" r="4.5" fill="#fff4ed" stroke="#475569" stroke-width="1.4"/>
    </g>
  </g>
  <!-- 오른쪽: 다음 단계 -->
  <g transform="translate(600, 120)">
    <rect x="0" y="0" width="150" height="105" rx="6" fill="#fff" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,2"/>
    <text x="75" y="32" text-anchor="middle" font-size="11" font-weight="700" fill="#0f172a">다음 단계</text>
    <text x="75" y="58" text-anchor="middle" font-size="9" fill="#7b341e">물류 센터에서</text>
    <text x="75" y="75" text-anchor="middle" font-size="9" fill="#7b341e">바코드를</text>
    <text x="75" y="90" text-anchor="middle" font-size="9" fill="#7b341e">스캔합니다</text>
  </g>
  <!-- 흐름 화살표 -->
  <line x1="385" y1="135" x2="520" y2="135" stroke="#ff7849" stroke-width="2.2" marker-end="url(#m1n-a)"/>
  <text x="450" y="128" text-anchor="middle" font-size="8" font-style="italic" fill="#7b341e">물류 센터로</text>
</svg>
</div>

*그림 5-20. 발신자가 우체국 입구에서 창구 직원에게 우편을 맡기면 송장이 붙습니다*

| 비유 | IT 용어 | 한 줄 설명 |
|:---:|:---|:---|
| 발신자 | **외부 호스트** | 브라우저로 요청을 보내는 사용자 |
| 우체국 입구 | **NodePort** | 노드 외벽의 공개 포트 |
| 창구 직원 | **kube-proxy (1차)** | iptables 규칙으로 패킷을 받아 다음 단계로 전달 |
| 송장 | **NAT 변환** | 패킷의 목적지를 Ingress Controller Pod로 변환 |

브라우저가 `http://localhost/order`를 누르면 요청은 노드의 NodePort(`:30080`)로 들어옵니다. 같은 노드의 kube-proxy가 iptables 규칙으로 그 패킷을 가로채 NodePort Service 뒤에 묶인 Ingress Controller Pod로 변환해 보냅니다. 송장이 붙는 단계입니다 — 어디로 갈지를 패킷에 새겨 다음 단계로 넘기는 자리입니다.

<div class="svg-figure">
<svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="1단계 IT — 외부 요청이 NodePort + kube-proxy(1차)를 거쳐 Ingress Controller에 도달">
  <defs>
    <marker id="fl1n-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="400" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">외부 요청 → NodePort → kube-proxy(1차) → Ingress Controller</text>
  <rect x="20" y="120" width="120" height="80" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="80" y="155" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">외부 호스트</text>
  <text x="80" y="180" text-anchor="middle" font-size="10" fill="#6b7280">브라우저</text>
  <line x1="140" y1="160" x2="195" y2="160" stroke="#ff7849" stroke-width="2.4" marker-end="url(#fl1n-a)"/>
  <rect x="195" y="60" width="585" height="200" rx="10" fill="#fff" stroke="#475569" stroke-width="1.4" stroke-dasharray="6,4"/>
  <text x="487" y="78" text-anchor="middle" font-size="11" font-style="italic" fill="#475569">Kubernetes 클러스터 (워커 노드)</text>
  <rect x="220" y="120" width="120" height="80" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="280" y="148" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">NodePort</text>
  <text x="280" y="170" text-anchor="middle" font-size="11" font-family="monospace" fill="#7b341e">:30080</text>
  <text x="280" y="190" text-anchor="middle" font-size="9" fill="#7b341e">노드 외벽 진입</text>
  <line x1="340" y1="160" x2="400" y2="160" stroke="#ff7849" stroke-width="2.4" marker-end="url(#fl1n-a)"/>
  <text x="370" y="150" text-anchor="middle" font-size="9" font-style="italic" fill="#7b341e">DNAT</text>
  <rect x="400" y="120" width="160" height="80" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="480" y="148" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">kube-proxy (1차)</text>
  <text x="480" y="170" text-anchor="middle" font-size="9" fill="#7b341e">iptables 규칙 따라</text>
  <text x="480" y="185" text-anchor="middle" font-size="9" fill="#7b341e">Pod IP로 변환</text>
  <line x1="560" y1="160" x2="615" y2="160" stroke="#ff7849" stroke-width="2.4" marker-end="url(#fl1n-a)"/>
  <rect x="615" y="120" width="150" height="80" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="690" y="155" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">Ingress Controller</text>
  <text x="690" y="180" text-anchor="middle" font-size="9" fill="#7b341e">(L7 처리 시작)</text>
  <text x="167" y="145" text-anchor="middle" font-size="10" font-family="monospace" font-weight="700" fill="#7b341e">localhost/order</text>
</svg>
</div>

*그림 5-21. NodePort와 kube-proxy(1차)가 외부 요청을 Ingress Controller로 전달*

### 5.3.2 2단계 분류 - 물류 센터가 바코드를 보고 어디로 보낼지 정한다

송장이 붙은 우편이 **물류 센터**에 도착합니다. 작업자가 송장의 **바코드**를 스캐너로 찍으면 서울 우체국·부산 우체국 가운데 어디로 갈지 자동으로 뜹니다. 어떤 바코드가 어느 우체국으로 가는지는 옆에 비치된 **주소 사전**에 적혀 있습니다. 주소 사전은 우체국 정보가 바뀔 때마다 즉시 고쳐 둡니다.

<div class="svg-figure">
<svg viewBox="0 0 800 290" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="2단계 비유 — 물류 센터에서 작업자가 송장의 바코드를 스캔하고 주소 사전과 대조해 어느 우체국으로 보낼지 결정">
  <defs>
    <marker id="m2n-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="m2n-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="400" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">스캐너가 송장의 바코드를 찍으면 서울 우체국이 결정됩니다</text>
  <!-- 좌측: 주소 사전 (책) -->
  <g transform="translate(25, 85)">
    <rect x="0" y="0" width="105" height="95" rx="2" fill="#fff" stroke="#7b341e" stroke-width="1.4"/>
    <rect x="0" y="0" width="12" height="95" fill="#7b341e"/>
    <text x="6" y="50" text-anchor="middle" font-size="6" font-weight="700" fill="#fff" transform="rotate(-90 6 50)">RULES</text>
    <text x="58" y="18" text-anchor="middle" font-size="9" font-weight="700" fill="#7b341e">주소 사전</text>
    <line x1="18" y1="24" x2="100" y2="24" stroke="#94a3b8" stroke-width="0.4"/>
    <text x="20" y="38" font-size="7" fill="#7b341e" font-weight="700">▶ 서울</text>
    <text x="20" y="52" font-size="7" fill="#94a3b8">  부산</text>
    <text x="20" y="66" font-size="7" fill="#94a3b8">  대구</text>
    <text x="20" y="80" font-size="7" fill="#94a3b8">  광주</text>
  </g>
  <!-- 가운데: 컨베이어 + 우편 + 스캐너 (핵심 동작) -->
  <g transform="translate(200, 65)">
    <!-- 컨베이어 벨트 -->
    <rect x="0" y="80" width="200" height="20" fill="#e5e7eb" stroke="#7b341e" stroke-width="1.2"/>
    <line x1="5" y1="82" x2="195" y2="82" stroke="#7b341e" stroke-width="0.6" stroke-dasharray="4,2"/>
    <!-- 우편 (컨베이어 위) -->
    <g transform="translate(40, 55)">
      <rect x="0" y="0" width="50" height="32" rx="1" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/>
      <line x1="2" y1="2" x2="25" y2="16" stroke="#d97706" stroke-width="0.8"/>
      <line x1="50" y1="2" x2="25" y2="16" stroke="#d97706" stroke-width="0.8"/>
      <!-- 큰 빨간 송장 -->
      <rect x="28" y="-16" width="45" height="28" rx="2" fill="#dc2626" stroke="#7b341e" stroke-width="1.4"/>
      <line x1="33" y1="-8" x2="33" y2="6" stroke="#fff" stroke-width="1"/>
      <line x1="38" y1="-8" x2="38" y2="6" stroke="#0f172a" stroke-width="1.2"/>
      <line x1="43" y1="-8" x2="43" y2="6" stroke="#fff" stroke-width="0.8"/>
      <line x1="48" y1="-8" x2="48" y2="6" stroke="#0f172a" stroke-width="1.2"/>
      <line x1="53" y1="-8" x2="53" y2="6" stroke="#fff" stroke-width="1"/>
      <line x1="58" y1="-8" x2="58" y2="6" stroke="#0f172a" stroke-width="1"/>
      <line x1="63" y1="-8" x2="63" y2="6" stroke="#fff" stroke-width="0.8"/>
      <text x="50.5" y="10" text-anchor="middle" font-size="6" fill="#fff" font-weight="700">송장</text>
    </g>
    <!-- 스캐너 (위에서 크게) -->
    <g transform="translate(110, 15)">
      <rect x="0" y="0" width="55" height="45" rx="4" fill="#1f2937" stroke="#0f172a" stroke-width="1.4"/>
      <rect x="8" y="8" width="39" height="18" rx="2" fill="#fef3c7" stroke="#0f172a" stroke-width="1"/>
      <line x1="13" y1="12" x2="13" y2="22" stroke="#0f172a" stroke-width="0.8"/>
      <line x1="17" y1="12" x2="17" y2="22" stroke="#0f172a" stroke-width="1.2"/>
      <line x1="21" y1="12" x2="21" y2="22" stroke="#0f172a" stroke-width="0.6"/>
      <line x1="25" y1="12" x2="25" y2="22" stroke="#0f172a" stroke-width="1"/>
      <line x1="29" y1="12" x2="29" y2="22" stroke="#0f172a" stroke-width="0.8"/>
      <line x1="33" y1="12" x2="33" y2="22" stroke="#0f172a" stroke-width="1.2"/>
      <line x1="37" y1="12" x2="37" y2="22" stroke="#0f172a" stroke-width="0.6"/>
      <line x1="41" y1="12" x2="41" y2="22" stroke="#0f172a" stroke-width="1"/>
      <text x="27.5" y="39" text-anchor="middle" font-size="8" fill="#fff" font-weight="700">SCAN</text>
    </g>
    <!-- 스캐너 광선 (굵고 눈에 띄게) -->
    <line x1="137.5" y1="60" x2="65" y2="87" stroke="#ff7849" stroke-width="2.4" stroke-dasharray="3,2"/>
    <text x="95" y="65" text-anchor="middle" font-size="9" font-weight="700" fill="#ff7849">바코드</text>
    <text x="95" y="77" text-anchor="middle" font-size="9" font-weight="700" fill="#ff7849">스캔</text>
    <!-- 작업자 (스캐너 옆에서 스캔) -->
    <g transform="translate(155, 88)">
      <circle cx="0" cy="0" r="9" fill="#fff" stroke="#475569" stroke-width="1.2"/>
      <path d="M -12 9 Q -12 24 0 24 Q 12 24 12 9 L 12 35 L -12 35 Z" fill="#fff4ed" stroke="#475569" stroke-width="1.2"/>
      <!-- 손이 스캐너를 쥔 형태 -->
      <g transform="translate(-5, -5)">
        <circle cx="0" cy="0" r="2.5" fill="#7b341e"/>
      </g>
    </g>
  </g>
  <text x="235" y="180" text-anchor="middle" font-size="8" fill="#7b341e">작업자</text>
  <!-- 오른쪽: 우체국 목록 (지도 핀 형태) -->
  <g transform="translate(600, 85)">
    <!-- 서울 (강조) -->
    <g transform="translate(0, 0)">
      <circle cx="35" cy="15" r="18" fill="#fff4ed" stroke="#ff7849" stroke-width="2.2"/>
      <text x="35" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">서울</text>
    </g>
    <!-- 부산 -->
    <g transform="translate(0, 50)">
      <circle cx="35" cy="15" r="15" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
      <text x="35" y="18" text-anchor="middle" font-size="9" fill="#94a3b8">부산</text>
    </g>
    <!-- 대구 -->
    <g transform="translate(0, 95)">
      <circle cx="35" cy="15" r="15" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
      <text x="35" y="18" text-anchor="middle" font-size="9" fill="#94a3b8">대구</text>
    </g>
    <!-- 광주 -->
    <g transform="translate(0, 140)">
      <circle cx="35" cy="15" r="15" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
      <text x="35" y="18" text-anchor="middle" font-size="9" fill="#94a3b8">광주</text>
    </g>
  </g>
  <!-- 결정 화살표 -->
  <line x1="425" y1="110" x2="555" y2="110" stroke="#ff7849" stroke-width="2.2" marker-end="url(#m2n-a)"/>
  <text x="490" y="102" text-anchor="middle" font-size="9" font-style="italic" font-weight="700" fill="#7b341e">결정!</text>
</svg>
</div>

*그림 5-22. 물류 센터가 송장의 바코드를 찍고 어느 우체국으로 보낼지 정합니다*

| 비유 | IT 용어 | 한 줄 설명 |
|:---:|:---|:---|
| 물류 센터 | **Ingress Controller** | URL·Host로 보낼 Service를 결정하는 Pod |
| 바코드 | **URL·Host 헤더** | 패킷의 L7 식별 정보 |
| 주소 사전 | **내부 명단** | API Server를 watch해 받아 둔 Ingress·Service 정보 |
| 서울 우체국·부산 우체국 | **Service (ClusterIP)** | 셀렉터로 묶인 Pod 그룹의 가상 진입 주소 |

Ingress Controller는 요청의 URL 경로와 Host 헤더를 읽어 등록된 Ingress 규칙과 대조합니다. *"이 요청은 `order-service`다."* 판단이 끝나면 미리 받아 둔 내부 명단에서 `order-service`의 ClusterIP를 곧바로 꺼냅니다.

<div class="svg-figure">
<svg viewBox="0 0 800 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="2단계 IT — Ingress Controller가 API Server에서 받아 둔 명단으로 결정된 Service의 ClusterIP로 전송">
  <defs>
    <marker id="fl2n-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="fl2n-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="400" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">Ingress Controller → 내부 명단 조회 → 결정된 Service ClusterIP로 전송</text>
  <rect x="20" y="55" width="220" height="120" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="130" y="95" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">API Server</text>
  <text x="130" y="115" text-anchor="middle" font-size="10" fill="#7b341e">Ingress·Service·Pod 정보</text>
  <text x="130" y="143" text-anchor="middle" font-size="10" fill="#7b341e">(미리 받아 둠)</text>
  <rect x="285" y="55" width="200" height="120" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.6"/>
  <text x="385" y="95" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Ingress Controller</text>
  <text x="385" y="115" text-anchor="middle" font-size="11" fill="#6b7280">Pod</text>
  <text x="385" y="143" text-anchor="middle" font-size="10" fill="#7b341e">URL·Host 읽음</text>
  <line x1="285" y1="100" x2="245" y2="100" stroke="#475569" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#fl2n-s)"/>
  <text x="265" y="90" text-anchor="middle" font-size="9" font-style="italic" font-family="monospace" fill="#475569">"order-service?"</text>
  <line x1="245" y1="135" x2="285" y2="135" stroke="#ff7849" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#fl2n-a)"/>
  <text x="265" y="150" text-anchor="middle" font-size="9" font-style="italic" font-family="monospace" fill="#7b341e">"10.96.0.20"</text>
  <line x1="490" y1="99" x2="575" y2="99" stroke="#ff7849" stroke-width="2.4" marker-end="url(#fl2n-a)"/>
  <rect x="575" y="78" width="205" height="42" rx="21" fill="#fff4ed" stroke="#ff7849" stroke-width="2.4"/>
  <text x="677" y="104" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">order-service (10.96.0.20)</text>
  <rect x="585" y="130" width="185" height="28" rx="14" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="677" y="148" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">stores-service (10.96.0.21)</text>
  <rect x="585" y="165" width="185" height="28" rx="14" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="677" y="183" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">payment-service (10.96.0.22)</text>
  <rect x="585" y="200" width="185" height="28" rx="14" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="677" y="218" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">cs-service (10.96.0.23)</text>
  <text x="400" y="245" text-anchor="middle" font-size="10" font-style="italic" fill="#94a3b8">다음 단계 (3단계): kube-proxy(2차)가 Pod IP로 변환</text>
</svg>
</div>

*그림 5-23. Ingress Controller가 URL을 읽어 Service를 선택, 미리 받아 둔 명단에서 ClusterIP를 꺼냄*

### 5.3.3 3단계 배달 - 집배원이 우편함에 넣는다

**서울 우체국**으로 도착한 우편을 그 동네 **집배원**이 받습니다. 집배원은 우편의 **받는 주소**를 보고 동네 안의 어느 집인지 정해 그 집의 **우편함**에 우편을 넣습니다. 우편함이 우편의 종착지입니다.

<div class="svg-figure">
<svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="3단계 비유 — 서울 우체국에서 집배원이 우편을 받아 받는 주소를 보고 각 집의 우편함에 우편을 넣음">
  <defs>
    <marker id="m3n-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="400" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">집배원이 받는 주소를 보고 집 B의 우편함에 우편을 넣습니다</text>
  <!-- 좌: 서울 우체국 (축소) -->
  <g transform="translate(15, 140)">
    <rect x="0" y="0" width="65" height="75" rx="0" fill="#fff" stroke="#7b341e" stroke-width="1.4"/>
    <path d="M -2 0 L 67 0 L 67 -8 L -2 -8 Z" fill="#7b341e"/>
    <circle cx="32.5" cy="20" r="8" fill="#fff" stroke="#7b341e" stroke-width="1"/>
    <text x="32.5" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">▣</text>
    <rect x="26" y="48" width="13" height="22" fill="#7b341e"/>
  </g>
  <!-- 집배원 출발 -->
  <g transform="translate(105, 155)">
    <circle cx="0" cy="0" r="9" fill="#fff" stroke="#475569" stroke-width="1.2"/>
    <path d="M -11 10 Q -11 24 0 24 Q 11 24 11 10 L 11 35 L -11 35 Z" fill="#fff4ed" stroke="#475569" stroke-width="1.2"/>
    <!-- 가방 -->
    <rect x="10" y="15" width="15" height="15" rx="1" fill="#fef3c7" stroke="#d97706" stroke-width="1"/>
  </g>
  <text x="105" y="210" text-anchor="middle" font-size="8" fill="#94a3b8">집배원</text>
  <!-- 동선 (점선 화살표) -->
  <path d="M 130 175 Q 280 210 390 180" stroke="#ff7849" stroke-width="2" stroke-dasharray="4,3" fill="none" marker-end="url(#m3n-a)"/>
  <!-- 받는 주소 확인 (경로 위) -->
  <g transform="translate(250, 150)">
    <rect x="0" y="0" width="50" height="30" rx="2" fill="#fff" stroke="#7b341e" stroke-width="1.2"/>
    <text x="25" y="12" text-anchor="middle" font-size="7" fill="#7b341e">받는 주소</text>
    <text x="25" y="22" text-anchor="middle" font-size="7" fill="#7b341e">마포 번지 B</text>
  </g>
  <!-- 우측: 가구 3채 (집 B에 우편이 들어가는 모습을 중심) -->
  <!-- 집 A (흐린) -->
  <g transform="translate(420, 115)">
    <path d="M 0 32 L 28 2 L 56 32 L 56 88 L 0 88 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
    <rect x="22" y="58" width="10" height="25" fill="#cbd5e1"/>
    <!-- 우편함 -->
    <rect x="-12" y="65" width="12" height="12" rx="0.5" fill="#f5f5f5" stroke="#cbd5e1" stroke-width="1"/>
    <circle cx="-6" cy="71" r="1.5" fill="#cbd5e1"/>
  </g>
  <text x="448" y="220" text-anchor="middle" font-size="9" fill="#cbd5e1">집 A</text>
  <!-- 집 B (강조 - 우편이 들어가는 모습) -->
  <g transform="translate(545, 100)">
    <!-- 집 외관 -->
    <path d="M 0 35 L 32 0 L 64 35 L 64 100 L 0 100 Z" fill="#fef3c7" stroke="#ff7849" stroke-width="2.8"/>
    <rect x="26" y="65" width="12" height="32" fill="#ff7849"/>
    <!-- 창 -->
    <rect x="8" y="48" width="8" height="8" fill="#4da6ff" stroke="#ff7849" stroke-width="0.6"/>
    <rect x="48" y="48" width="8" height="8" fill="#4da6ff" stroke="#ff7849" stroke-width="0.6"/>
    <!-- 우편함 (크고 강조) -->
    <rect x="-18" y="72" width="18" height="18" rx="2" fill="#fef3c7" stroke="#dc2626" stroke-width="2.2"/>
    <line x1="-18" y1="78" x2="0" y2="78" stroke="#dc2626" stroke-width="1"/>
    <circle cx="-9" cy="78" r="2" fill="#dc2626"/>
    <!-- 깃발 (열린 우편함) -->
    <rect x="-18" y="68" width="4" height="6" fill="#dc2626" stroke="#7b341e" stroke-width="0.6"/>
    <!-- 우편이 우편함 안으로 들어가는 모습 -->
    <g transform="translate(-10, 70)">
      <rect x="0" y="0" width="16" height="10" rx="1" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/>
      <line x1="2" y1="1" x2="8" y2="5" stroke="#d97706" stroke-width="0.6"/>
      <line x1="16" y1="1" x2="8" y2="5" stroke="#d97706" stroke-width="0.6"/>
    </g>
  </g>
  <text x="577" y="220" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">집 B</text>
  <text x="577" y="237" font-size="9" font-style="italic" font-weight="700" fill="#dc2626">우편함에 넣음</text>
  <!-- 집 C (흐린) -->
  <g transform="translate(710, 115)">
    <path d="M 0 32 L 28 2 L 56 32 L 56 88 L 0 88 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
    <rect x="22" y="58" width="10" height="25" fill="#cbd5e1"/>
    <!-- 우편함 -->
    <rect x="-12" y="65" width="12" height="12" rx="0.5" fill="#f5f5f5" stroke="#cbd5e1" stroke-width="1"/>
    <circle cx="-6" cy="71" r="1.5" fill="#cbd5e1"/>
  </g>
  <text x="738" y="220" text-anchor="middle" font-size="9" fill="#cbd5e1">집 C</text>
</svg>
</div>

*그림 5-24. 서울 우체국에서 집배원이 받는 주소를 보고 우편함에 우편을 넣습니다*

| 비유 | IT 용어 | 한 줄 설명 |
|:---:|:---|:---|
| 서울 우체국 | **Service (ClusterIP)** | 도착한 ClusterIP를 받는 자리 |
| 집배원 | **kube-proxy (2차)** | iptables DNAT으로 ClusterIP를 살아있는 Pod IP로 변환 |
| 받는 주소 | **Endpoints** | Service 셀렉터에 매칭된 살아있는 Pod IP 목록 |
| 우편함 | **Pod** | 실제 비즈니스 로직을 처리하는 앱 |

ClusterIP를 향한 요청은 노드의 kube-proxy(2차)가 가로챕니다. Endpoints에 올라 있는 살아있는 Pod 한 대를 골라 그 IP로 바꿔 보냅니다. 요청이 Pod에 닿으면 애플리케이션 로직이 응답을 돌려줍니다. 이 흐름이 어긋나지 않는 이유는 Endpoint Controller가 뒤에서 Endpoints를 계속 손보기 때문입니다. Service의 selector에 매칭되는 Pod가 새로 뜨거나 죽으면 곧바로 감지해 Pod IP 목록에서 빼고 더합니다.

<div class="svg-figure">
<svg viewBox="0 0 800 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="3단계 IT — kube-proxy(2차)가 ClusterIP를 Pod IP로 변환, Endpoint Controller가 Pod IP 목록 갱신">
  <defs>
    <marker id="fl3n-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="fl3n-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
    <marker id="fl3n-bi" markerWidth="10" markerHeight="10" refX="5" refY="3" orient="auto-start-reverse"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="400" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">ClusterIP → kube-proxy(2차) DNAT → Pod IP → Pod 응답</text>
  <rect x="20" y="80" width="160" height="40" rx="20" fill="#fff" stroke="#cbd5e1" stroke-width="1.6"/>
  <text x="100" y="105" text-anchor="middle" font-size="12" font-weight="600" fill="#94a3b8">Service ClusterIP</text>
  <line x1="180" y1="100" x2="240" y2="100" stroke="#ff7849" stroke-width="2.4" marker-end="url(#fl3n-a)"/>
  <rect x="240" y="60" width="540" height="180" rx="10" fill="#fff" stroke="#475569" stroke-width="1.4" stroke-dasharray="6,4"/>
  <text x="510" y="78" text-anchor="middle" font-size="11" font-style="italic" fill="#475569">워커 노드</text>
  <rect x="260" y="90" width="180" height="80" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2.4"/>
  <text x="350" y="118" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">kube-proxy (2차)</text>
  <text x="350" y="138" text-anchor="middle" font-size="9" fill="#7b341e">iptables DNAT</text>
  <text x="350" y="153" text-anchor="middle" font-size="9" fill="#7b341e">ClusterIP → Pod IP</text>
  <rect x="495" y="85" width="270" height="105" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="630" y="103" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">백엔드 Pod 그룹</text>
  <line x1="440" y1="129" x2="532" y2="129" stroke="#ff7849" stroke-width="2" marker-end="url(#fl3n-a)"/>
  <rect x="522" y="113" width="90" height="32" rx="16" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="567" y="134" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Pod A</text>
  <rect x="647" y="113" width="90" height="32" rx="16" fill="#fff" stroke="#ff7849" stroke-width="1.6"/>
  <text x="692" y="134" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Pod B</text>
  <text x="630" y="167" text-anchor="middle" font-size="9" fill="#7b341e">애플리케이션 로직 실행 → 응답</text>
  <rect x="20" y="250" width="260" height="80" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2" stroke-dasharray="5,3"/>
  <text x="150" y="278" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Endpoint Controller</text>
  <text x="150" y="298" text-anchor="middle" font-size="10" fill="#7b341e">Pod 변동 감시</text>
  <text x="150" y="313" text-anchor="middle" font-size="10" fill="#7b341e">→ Pod IP 목록 갱신</text>
  <line x1="285" y1="250" x2="345" y2="172" stroke="#475569" stroke-width="1.4" stroke-dasharray="5,3" marker-start="url(#fl3n-bi)" marker-end="url(#fl3n-bi)"/>
  <text x="270" y="215" font-size="9" font-style="italic" fill="#475569">watch (구독·알림)</text>
</svg>
</div>

*그림 5-25. ClusterIP가 kube-proxy(2차)를 통해 Pod IP로 변환되어 Pod에 응답. Endpoint Controller가 Pod IP 목록을 갱신*

:::note
**비유에서 단순화한 두 지점 - API Server의 매개**

비유 그림은 흐름을 또렷이 보여주려고 화살표를 직접 이어 두었습니다. 2단계에서 Ingress Controller가 ClusterIP를 곧장 *조회*하는 것처럼 그렸지만, 실제로는 API Server를 watch(구독)해서 받아 둔 명단을 들고 있다가 즉시 꺼냅니다. 3단계에서도 kube-proxy가 Pod IP 명단을 직접 들고 있는 것처럼 보이지만, Endpoint Controller가 갱신한 결과가 API Server에 저장되고 각 노드의 kube-proxy가 API Server를 watch해서 변경 알림을 받는 구조입니다. 두 경우 모두 사이에 API Server라는 매개가 끼어 있는데, 비유 그림에서는 이 매개를 생략한 것입니다.
:::

:::note
**더 깊이 - 1·3단계와 2단계는 보는 정보가 다릅니다 (L4 vs L7)**

같은 *전달*처럼 보여도 단계마다 들여다보는 깊이가 다릅니다. 1단계와 3단계는 봉투 겉면(IP·Port)만 보고 빠르게 옮기는 L4입니다. 2단계는 봉투를 열어 안의 글(URL·Host)까지 읽는 L7입니다. 우체국으로 옮겨 보면 차이가 또렷합니다. 1·3단계는 *송장*만 보고 옮기고, 2단계의 물류 센터만 *바코드 안의 받는 주소 정보*까지 읽고 어느 우체국인지 정합니다. L4는 빠르게 옮기고, L7은 한 단계 더 들여다본 다음 결정을 내립니다.
:::

종이 위에 길게 늘어놓은 컴포넌트들이 한 줄로 묶이자, 따로따로 떠 있던 이름들이 머릿속에서 자기 자리를 찾았습니다.

*'우편이 입구에 들어와 송장이 붙고, 물류 센터에서 바코드를 보고 우체국이 정해지고, 그 동네 집배원이 우편함에 넣는다. 각자 한 가지 일만 하는데 이게 합쳐지니 전체가 굴러가네.'*

자리에서 일어나기 전 종이 한 구석에 짧게 한 줄을 더 적었습니다. *네트워크는 끝났는데, 이걸로 진짜 운영이 되나?* 통합 사이트에는 DB 비밀번호도 있고, 매장 데이터도 있습니다. Pod가 한 번 죽고 다시 뜰 때마다 비밀번호가 노출되거나 데이터가 같이 사라진다면, 오늘 만든 문은 무용지물입니다.

문 자체는 다 달았습니다. 그 다음 매듭이 따로 있다는 사실만 메모로 남겼습니다.

## 이것만은 기억하자

- **Service는 Pod의 변하지 않는 직통 전화번호입니다.** Pod는 소모품이라 IP가 수시로 바뀌지만, Service는 변하지 않는 주소를 제공하며 트래픽을 골고루 분산합니다.
- **Service 뒤에는 세 조력자가 있습니다.** 실시간 Pod 명단을 관리하는 **Endpoint Controller**, 명단을 노드에 전파하는 **API Server**, 그리고 실제 길을 닦는 **kube-proxy**가 협력하여 패킷을 배달합니다.
- **Ingress는 물류 센터입니다.** 숫자(IP·Port)만 보는 Service와 달리, Ingress는 도메인과 URL 경로를 읽고 적절한 Service로 연결하는 라우팅을 담당합니다. 라우팅 규칙을 정의하는 **리소스(YAML)** 와 실제 요청을 처리하는 **컨트롤러(Pod)** 가 한 팀으로 움직입니다.

네트워크라는 뼈대는 이제 완벽히 갖춰졌습니다. 하지만 실제 서비스를 운영하려면 DB 비밀번호 같은 보안 정보와, 파드가 사라져도 데이터가 보존되는 영속성 처리가 필수적입니다.

다음 챕터에서는 설정값(**ConfigMap**), 보안 비밀(**Secret**), 그리고 데이터의 영속성(**Volume**)에 대해 알아보겠습니다.
