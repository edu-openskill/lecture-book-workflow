# Ch.5 Kubernetes 네트워킹

다음 날 아침, 사무실 자리에 앉은 오픈이는 어제 생성하고 테스트했던 네 개의 Pod를 떠올렸습니다. 자동 복구도, 새 버전으로의 교체도 성공적으로 확인했습니다.

*'그런데... 이걸 실제로 어떻게 사용해야 하지?'*

Pod 네 대를 띄워두긴 했지만, 정작 어느 주소로 요청을 보내야 할지 막막했습니다. 도커 실습 때 Nginx로 만들었던 단일 진입점이 생각났습니다. Pod IP는 재시작될 때마다 바뀔 텐데, 그 앞단에서 변하지 않고 자리를 지켜줄 진입점이 필요했습니다.

*'쿠버네티스에서는 이 기능을 어떻게 구현할까?'*

궁금해진 오픈이는 다시 공식 문서를 펼쳤습니다.

## 5.1 Service — Pod의 고정 주소

### 5.1.1 Service가 필요한 이유

문서를 훑던 오픈이의 눈에 **Service**라는 항목이 들어왔습니다. Pod의 변화에 상관없이 고정 진입점 역할을 하는 것 바로 이 **Service**였습니다. 

가맹점 내의 점장, 직원과 상관없이 고객은 전화번호 주문을 할 수 있듯이, Service는 쿠버네티스 환경에서 Pod들의 진입점 역할을 합니다.

<div class="svg-figure">
<svg viewBox="0 0 760 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="외부 요청이 Service라는 고정 진입점을 거쳐 여러 Pod로 분배되는 구조">
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
</svg>
</div>

*그림 5-1. Service는 고정 주소를 제공. Pod IP가 바뀌어도 Service 주소는 그대로*

### 5.1.2 Service 생성

:::tip
전체 실습 코드는 깃헙을 참고합니다.

**실습 코드 (GitHub)**: https://github.com/metacoding-10-linux-docker/docker/tree/master/ex11
:::

Service를 실습하려면 대상이 되는 Pod들이 먼저 준비되어야 합니다. 오픈이는 ex11 폴더를 열어, 어제 ex10에서 썼던 것과 같은 deploy-ex02.yml을 다시 실행해 Pod 네 개를 복구했습니다.

```bash
kubectl apply -f ex11/deploy-ex02.yml   #  Pod 4개 생성
```

이제 그 앞에 세울 Service YAML로 넘어갑니다.

**ex11/service-ex01.yml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort        # 노드 IP+포트로 외부 접근 가능한 타입
  selector:
    app: nginx          # 이 라벨을 가진 Pod를 뒤에 붙임
  ports:
  - port: 80            # 다른 Pod → Service 진입 포트
    targetPort: 80      # Service → Pod 전달 포트
    nodePort: 30080     # 외부 → 노드 진입 포트 (30000~32767)
```

Service가 Pod를 찾는 방법은 Deployment와 동일하게 라벨(Label) 매칭 방식을 사용합니다. IP 주소가 아니라 라벨로 연결하기 때문에, Pod가 새로 생성되어 IP가 바뀌더라도 라벨만 일치하면 Service는 요청을 정확히 전달할 수 있습니다.

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

*그림 5-2. selector가 지정한 라벨(app: nginx)을 가진 Pod만 골라 매칭. 다른 라벨(app: db)은 제외*

### 5.1.3 Service 타입과 접근 범위

오픈이는 YAML을 작성하며 포트 설정 부분에서 잠시 멈췄습니다. 

*'type: NodePort 이건 뭐지 ? 그리고 포트를 80번을 썼는데, targetPort도 있고 nodePort도 있네. 각각 어떤 역할을 하는거지'*

찾아보니 Service에는 '누구에게 공개할 것인가'에 따라 세 가지 타입을 선택할 수 있었습니다.

가족끼리 집 안에서만 대화할 때는 **ClusterIP** , 초대받은 고객에게 현관 비밀번호를 알려줄 때는 **NodePort** , 그리고 누구나 자유롭게 드나들도록 정문을 활짝 열어줄 때는 **LoadBalancer** 를 선택하면 됩니다.

#### ClusterIP

서비스 타입의 기본값으로 설정되는 타입입니다. 외부에서는 접근이 불가능하고 클러스터 내부의 Pod끼리만 서로를 부를 때 사용합니다.

*'백엔드 서버만 DB에 접속하면 되지, 굳이 외부 고객에게 DB 주소를 알려줄 필요는 없잖아? 그런 용도로 사용하는 타입이네.'*

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

*그림 5-3. ClusterIP — 외부 요청은 닿지 못하고 내부 Pod끼리만 통신*

#### NodePort 

오픈이가 실습에서 썼던 방식으로, 노드(서버)의 실제 IP에 특정 포트를 열어 외부 접근을 허용합니다.

*'YAML에 30080처럼 nodePort를 넣으면 이 포트로 외부에서 들어올 수 있는 거구나. 그런데 서비스마다 이런 노드포트를 하나씩 열어 주면 금방 관리가 번거로워지겠는데...'*

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

*그림 5-4. NodePort — 노드의 특정 포트로 외부 접근 허용*

#### LoadBalancer 

실제 운영 환경에서 주로 쓰는 방식입니다. 클라우드 서비스(AWS, GCP 등)를 쓰고 있다면, 쿠버네티스가 알아서 외부용 공인 IP를 발급받아 서비스에 딱 붙여줍니다.

사용자는 복잡한 노드 IP나 5자리의 포트 번호를 외울 필요가 없습니다. 그저 발급된 대표 IP 하나로 접속하면, LoadBalancer가 여러 노드에 트래픽을 골고루 나눠줍니다.

<div class="svg-figure">
<svg viewBox="0 0 760 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LoadBalancer — 클라우드가 공인 IP를 발급해 여러 노드의 Service에 트래픽을 분산하는 구조">
  <defs>
    <marker id="lb-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">LoadBalancer — 공인 IP 하나로 여러 노드에 분산</text>
  <rect x="20" y="60" width="120" height="38" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="80" y="84" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">User 1</text>
  <rect x="20" y="115" width="120" height="38" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="80" y="139" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">User 2</text>
  <rect x="20" y="170" width="120" height="38" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="80" y="194" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">User 3</text>
  <text x="80" y="232" text-anchor="middle" font-size="10" font-family="monospace" fill="#6b7280">myapp.com</text>
  <line x1="140" y1="79" x2="240" y2="135" stroke="#475569" stroke-width="1.6" marker-end="url(#lb-p)"/>
  <line x1="140" y1="134" x2="240" y2="148" stroke="#475569" stroke-width="1.6" marker-end="url(#lb-p)"/>
  <line x1="140" y1="189" x2="240" y2="160" stroke="#475569" stroke-width="1.6" marker-end="url(#lb-p)"/>
  <rect x="240" y="100" width="170" height="100" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8" stroke-dasharray="6,4"/>
  <text x="325" y="123" text-anchor="middle" font-size="11" font-weight="600" fill="#7b341e">클라우드 (AWS·GCP)</text>
  <text x="325" y="155" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">LoadBalancer</text>
  <text x="325" y="180" text-anchor="middle" font-size="10" font-family="monospace" fill="#7b341e">공인 IP</text>
  <line x1="410" y1="125" x2="475" y2="100" stroke="#475569" stroke-width="1.6" marker-end="url(#lb-p)"/>
  <line x1="410" y1="150" x2="475" y2="170" stroke="#475569" stroke-width="1.6" marker-end="url(#lb-p)"/>
  <line x1="410" y1="175" x2="475" y2="240" stroke="#475569" stroke-width="1.6" marker-end="url(#lb-p)"/>
  <text x="442" y="115" text-anchor="middle" font-size="9" font-style="italic" fill="#6b7280">분산</text>
  <rect x="465" y="50" width="285" height="240" rx="10" fill="#fff" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="5,3"/>
  <text x="478" y="70" font-size="11" font-weight="700" fill="#7b341e">Kubernetes 클러스터</text>
  <rect x="475" y="80" width="265" height="55" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="495" y="102" font-size="11" font-weight="700" fill="#0f172a">Node 1</text>
  <rect x="555" y="92" width="80" height="32" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.2"/>
  <text x="595" y="113" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Service</text>
  <line x1="635" y1="108" x2="660" y2="108" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <rect x="660" y="92" width="60" height="32" rx="4" fill="#fff" stroke="#475569" stroke-width="1.2"/>
  <text x="690" y="113" text-anchor="middle" font-size="11" font-weight="700" fill="#0f172a">Pod</text>
  <rect x="475" y="150" width="265" height="55" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="495" y="172" font-size="11" font-weight="700" fill="#0f172a">Node 2</text>
  <rect x="555" y="162" width="80" height="32" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.2"/>
  <text x="595" y="183" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Service</text>
  <line x1="635" y1="178" x2="660" y2="178" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <rect x="660" y="162" width="60" height="32" rx="4" fill="#fff" stroke="#475569" stroke-width="1.2"/>
  <text x="690" y="183" text-anchor="middle" font-size="11" font-weight="700" fill="#0f172a">Pod</text>
  <rect x="475" y="220" width="265" height="55" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="495" y="242" font-size="11" font-weight="700" fill="#0f172a">Node 3</text>
  <rect x="555" y="232" width="80" height="32" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.2"/>
  <text x="595" y="253" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Service</text>
  <line x1="635" y1="248" x2="660" y2="248" stroke="#475569" stroke-width="1.4" marker-end="url(#lb-p)"/>
  <rect x="660" y="232" width="60" height="32" rx="4" fill="#fff" stroke="#475569" stroke-width="1.2"/>
  <text x="690" y="253" text-anchor="middle" font-size="11" font-weight="700" fill="#0f172a">Pod</text>
</svg>
</div>

*그림 5-5. LoadBalancer — 클라우드가 공인 IP를 발급하고 여러 노드에 분산*

오픈이는 서비스 타입과 포트를 다음과 같이 정리했습니다.

| 타입 | 접근 범위 | 사용 사례 |
|:----:|:---------|:---------|
| `ClusterIP` | 클러스터 내부만 | 백엔드·DB 등 외부 노출 불필요한 서비스 |
| `NodePort` | 노드IP:포트로 외부 접근 가능 | 테스트, 개발 환경 |
| `LoadBalancer` | 공인 IP로 외부 접근 가능 | 클라우드 운영 환경 |

#### 포트 흐름

타입은 정리됐지만 처음 YAML에서 오픈이를 멈춰 세웠던 또 다른 자리가 그대로 남아 있었습니다. 한 줄에 같이 적힌 `port`, `targetPort`, `nodePort`. 셋은 결국 **각자 다른 주인의 포트**입니다. `nodePort`는 노드의 포트, `port`는 Service의 포트, `targetPort`는 Pod의 포트입니다. Service YAML이 셋을 한 자리에 모아 적는 건, 외부에서 Pod까지의 라우팅 전체를 Service가 한 곳에서 선언하기 때문입니다.

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

| 포트 종류 | 누구의 포트인가 | 역할 | 생략 시 |
|:--------:|:---------------|:-----|:-------|
| `nodePort` | 노드(서버)의 포트 | 외부에서 노드 IP로 접근할 때 열리는 30000~32767 포트 | 30000~32767 중 자동 할당 |
| `port` | Service의 포트 | 클러스터 내부에서 Service를 부를 때 쓰는 포트 | 생략 불가 (필수) |
| `targetPort` | Pod(컨테이너)의 포트 | 컨테이너 앱이 사용하는 포트와 일치해야 함 | `port` 값과 동일하게 설정 |

### 5.1.4 외부에서 Service 접속해 보기

오픈이는 작성한 YAML을 적용했습니다.

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

*그림 5-7. Service 생성*

*'생성됐다. 그럼 바로 브라우저에서 들어가 봐야지.'*

하지만 여기서 오픈이는 예상치 못한 문제에 부딪힙니다.

*'분명 노드포트를 30080로 열었는데 localhost:30080으로 치니 먹통이네. minikube가 내 노트북이랑 한 꺼풀 떨어져 있어서 그런 건가...'*

 Minikube라는 가상 세계와 우리 PC가 별도의 네트워크로 분리되어 있기 때문입니다. 이를 해결하기 위해 Minikube는 임시 통로를 뚫어주는 전용 명령어를 제공합니다.

| 방법 | 명령어 |   설명   |
|:------:|:-----|:-----|
| URL 생성 | `minikube service <서비스이름> --url` | NodePort 혹은 LoadBalancer 타입의 Service에 접근할 수 있는 URL을 생성|
| 터널 개방 | `minikube tunnel` | LoadBalancer 타입의 Service에 외부 IP를 부여 |
| 포트 포워딩 | `kubectl port-forward service/<서비스이름> 8080:80` | 호스트의 8080 포트를 Service의 80 포트로 포워딩 |


:::note
**Minikube는 왜 localhost로 안 닿는가**

Minikube는 내 컴퓨터 내부에서 독립적으로 실행되는 가상 환경(VM 또는 컨테이너)입니다. 즉, Minikube라는 가상 세계와 우리 PC라는 현실 세계가 별도의 네트워크로 분리되어 있습니다. 그래서 도커에서 포트포워딩으로 호스트 PC와 컨테이너를 연결했던 것처럼, Minikube와 통신할 수 있는 다른 방법이 있어야 합니다.
:::

오픈이는 이 중 **minikube service --url** 을 사용했습니다. NodePort로 열어둔 서비스이니, 접근할 수 있는 주소만 하나 받아오면 브라우저에서 바로 확인할 수 있습니다.

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

*그림 5-8. minikube service URL 생성*

명령을 치자 터미널에 URL 한 줄이 나타나더니 커서가 그대로 멈춰 섰습니다.

*'어? 왜 프롬프트가 안 나오지? 고장 났나?'*

잠깐 당황했지만, 이 명령은 터미널을 계속 붙잡고 있어야 통로가 유지되는 방식이라는 걸 깨달았습니다. 생성된 URL을 복사해 브라우저에 입력하자, 드디어 기다리던 NGINX 화면이 나타났습니다.

![](../assets/CH04/chap03-44.png)

*그림 5-9. 브라우저에서 nginx 접속 확인*

확인이 끝났으니 이제 CTRL + C를 눌러 열려 있던 통로를 닫았습니다. 이제 테스트해 볼 것은 **Pod가 죽어도 Service가 고정 진입점 역할을 제대로 해주는가** 입니다.

오픈이는 Service가 새 Pod로 연결을 잘 넘겨주는지 확인하기 위해, 현재 실행 중인 모든 Pod를 삭제했습니다.

```bash
kubectl delete pod --all                  # 모든 Pod 삭제 (Deployment가 새 Pod를 자동 재생성)
minikube service nginx-service --url      # Service 접속 URL 출력
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

*그림 5-10. Pod 삭제 후 Service 접속*

잠시 후 다시 생성된 주소로 브라우저에 접속했습니다. 결과는 예상대로였습니다. Pod가 새로 바뀌었음에도 Nginx 페이지가 표시되었습니다. Service가 고정된 진입점 역할을 충실히 수행하고 있음을 확인했습니다.

*'와, 진짜네. Pod가 새로 만들어지면 IP가 바뀌었을 텐데. Service가 뒤에서 주소를 알아서 연결해주는구나.'*

## 5.2 Ingress — 도메인 라우팅

### 5.2.1 Service의 한계

NodePort로 한 서비스를 띄우는 데 성공했습니다. 그런데 실제 서비스는 백엔드 하나로 끝나지 않습니다. 한 도메인 아래에서 주문·매장·결제 같은 여러 서비스가 함께 돌아야 합니다.

도커 때 같은 문제를 NGINX로 풀었던 게 떠올랐습니다. 앞단에 NGINX 한 대를 두고 `/app1`은 1번 서버로, `/app2`는 2번 서버로 보냈습니다.

쿠버네티스에서도 같은 구조가 필요합니다. 오픈이는 Service로 풀어 보려 했지만 Service 설정에는 보이지 않았습니다.

*'그냥 Service에서 경로 라우팅을 하고 싶은데, 설정할 방법이 없는 것 같은데.'*

그 일을 담당하는 리소스가 따로 있습니다. **Ingress** 입니다.

### 5.2.2 Ingress의 역할

가맹점이 늘어나면 고객이 직통 번호를 일일이 외우기 어렵습니다. 본사가 **공식 앱**을 하나 만들어 두면, 고객은 앱에서 원하는 메뉴를 고르기만 해도 알맞은 지점으로 자동 연결됩니다.

Ingress가 이 공식 앱 역할을 합니다. 고객이 `http://도메인/order`로 접속하면 주문 Service로, `http://도메인/stores`로 접속하면 매장 Service로 나눠 보냅니다.

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

*'외부 진입점 하나로 다 묶을 수 있다는 거네. 직접 띄워 봐야 감이 오겠다.'*

비유만으로는 실감이 오지 않았습니다. 오픈이는 바로 Minikube에 인그레스를 실행 해보기로 했습니다. 

### 5.2.3 Ingress 적용하기

:::tip
전체 실습 코드는 깃헙을 참고합니다.

**실습 코드 (GitHub)**: https://github.com/metacoding-10-linux-docker/docker/tree/master/ex12
:::

공식 문서의 인그레스 페이지를 펼쳐 읽어 내려가려던 중, 문서 첫 줄이 오픈이의 눈에 걸렸습니다.

> "인그레스 컨트롤러가 있어야 인그레스를 충족할 수 있다. 인그레스 리소스만 생성한다면 효과가 없다."

*'이게 무슨 말이지? 인그레스를 만들려는 건데, 인그레스 컨트롤러라는 게 또 따로 있어야 한다고?'*

Ingress는 사실은 YAML 파일에 라우팅 규칙을 작성하는 **Ingress 리소스** 와 외부 요청을 받아서 처리하는 **Ingress 컨트롤러** 두 가지 구성 요소로 이루어져 있습니다. 

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

*그림 5-12. Ingress 리소스(YAML, 선언)와 Ingress Controller(Pod, 집행) — 선언과 집행의 분리*

| 구성 요소 | 역할 | 비유 | 쿠버네티스 철학 |
|:---------:|:-----|:-----|:---------------|
| `Ingress 리소스` | 어떤 도메인과 URL 경로의 요청을 어떤 Service로 보낼지 정의한 규칙 (YAML) | 공식 앱의 라우팅 규칙 | `선언` |
| `Ingress Controller` | 실제로 외부 요청을 받아 처리하는 소프트웨어 | 규칙을 실행하는 공식 앱 | `집행` |

*'아, 규칙만 적어 둔다고 알아서 굴러가는 게 아니구나. 그 규칙을 읽고 실제로 실행해 주는 역할이 따로 필요한 거네.'*

이제 오픈이가 실습으로 풀어 갈 순서가 머릿속에 그려졌습니다. 아직 없는 **공식 앱(Ingress Controller)** 부터 실행하고, 그 앱이 연결해 줄 백엔드 두 개를 띄운 다음, 라우팅 규칙을 YAML로 적어 길을 안내하고, 마지막으로 브라우저로 두 경로가 각자 다른 가맹점에 닿는지 확인하는 흐름이었습니다.

오픈이는 Minikube에서 Ingress 컨트롤러를 활성화했습니다.

```bash
minikube addons enable ingress          # Ingress Controller 애드온 활성화
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

*그림 5-14. minikube에서 ingress 애드온 활성화*

활성화가 끝나자 `ingress-nginx` 네임스페이스에 컨트롤러 Pod가 떠 있었습니다.

```bash
kubectl get pods -n ingress-nginx       # 컨트롤러 Pod 확인
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

*그림 5-15. Ingress Controller Pod가 Running 상태*

:::note
**운영 환경에서의 Ingress Controller 실행**

미니큐브 addon은 학습용 명령어입니다. 실제 운영에서는 `ingress-nginx` 같은 컨트롤러를 직접 하거나, 클라우드 환경에서는 클라우드가 제공하는 컨트롤러를 그대로 쓰면 됩니다. 어느 쪽이든 클러스터 안에 컨트롤러 Pod가 떠서 외부 요청을 갈라 주는 모습은 똑같습니다.
:::

#### 두 서비스 준비

`/order`와 `/stores`로 갈라 받을 백엔드 두 개를 띄웁니다. 둘은 같은 이미지를 쓰고 응답 문구만 다릅니다.

`ex12/` 안에는 주문과 매장 각각 **Pod를 띄우는 Deployment** 와 그 Pod를 묶는 **ClusterIP Service** 가 한 쌍씩 들어 있습니다. 잠시 뒤에 작성할 Ingress 규칙도 같은 폴더에 두고, 마지막에 한 번에 적용할 예정입니다.

| 파일 | 종류 | 역할 |
|:----:|:-----|:-----|
| `order-deploy.yml` | Deployment | 주문 응답 Pod — `-text=주문 접수 완료` |
| `order-service.yml` | Service (ClusterIP) | `order` Pod를 묶는 내부 전용 창구 (port 5678) |
| `stores-deploy.yml` | Deployment | 매장 응답 Pod — `-text=매장 선택` |
| `stores-service.yml` | Service (ClusterIP) | `stores` Pod를 묶는 내부 전용 창구 (port 5678) |

두 Service는 모두 **ClusterIP** 타입이라 클러스터 바깥에서는 직접 접근할 수 없습니다. 바깥 요청을 이 둘로 나눠 보낼 Ingress 규칙이 필요합니다.

#### 규칙 문서 작성

이제 남은 건 앞서 실행해 둔 컨트롤러에게 "**어떤 도메인 어떤 경로를 어디로 보내라**" 고 적어 둘 규칙 문서입니다.

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

오픈이가 적어 내려간 이 YAML이 아까 문서가 말하던 **규칙 문서** 쪽이었습니다. **rules** 아래 두 개의 **path** 가 있고, 각 경로가 서로 다른 Service를 가리킵니다. 규칙을 문서로 선언해 두면, 앞서 실행한 컨트롤러 Pod가 그 규칙을 읽고 실제 요청을 갈라 줍니다.

이제 `ex12/` 안의 모든 파일을 한 번에 올려 두 서비스와 Ingress 규칙을 함께 등록했습니다.

```bash
kubectl apply -f ex12/
kubectl get ingress                               # 등록된 Ingress 확인
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

*그림 5-16. Ingress 리소스 등록 확인 — ex12-ingress*

#### 브라우저로 접속

Docker 드라이버로 Minikube를 띄운 환경에서는 클러스터가 컨테이너 안에 있어 호스트에서 직접 닿지 않습니다. 이 통로를 뚫어 주는 `minikube tunnel` 을 별도 터미널에서 띄워 두면, 호스트의 `localhost` 로 들어온 요청이 Ingress Controller까지 이어집니다.

```bash
minikube tunnel                         # 별도 터미널에서 실행
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
    <div>* Starting tunnel for service frontend-ingress.</div>
  </div>
</div>

*그림 5-17. minikube tunnel 실행으로 외부 접근 경로 확보*

준비가 끝났으니 브라우저를 열어 두 경로를 차례로 들어가 봤습니다. 먼저 `http://localhost/order` 를 주소창에 입력하자 주문 페이지 응답이 돌아왔습니다.

<!-- MOCK: 실제 환경에서 재캡처 후 교체 필요 -->
![](../assets/CH05/mock-order-page.png)

*그림 5-18. `/order` 접속 결과 — "**주문 접수 완료**"*

이어서 `http://localhost/stores` 로 이동하자 이번에는 매장 선택 응답이 떴습니다.

<!-- MOCK: 실제 환경에서 재캡처 후 교체 필요 -->
![](../assets/CH05/mock-stores-page.png)

*그림 5-19. `/stores` 접속 결과 — "**매장 선택**"*

같은 도메인인데 뒤의 경로에 따라 응답이 완전히 달라졌습니다. Ingress 규칙대로 컨트롤러가 경로를 읽어 적절한 Service로 요청을 보냈기 때문입니다.

겉으로 보이는 결과는 매끄러웠지만, 그 사이에서 누가 무엇을 하고 있는지는 아직 손에 잡히지 않았습니다.

## 5.3 브라우저에서 Pod까지의 경로

오픈이는 브라우저의 요청이 Pod까지 닿는 것을 확인했습니다. 이제 쿠버네티스를 더 이해하기 위해 그 사이에서 일어나는 네트워크 흐름을 들여다보겠습니다.

### 5.3.1 핵심 의문 두 가지

오픈이는 두 의문을 하나씩 짚어 가며 Service 뒤에서 어떤 프로그램이 무슨 일을 하고 있는지 들여다봤습니다.

#### 첫 번째 — Pod가 바뀌어도 같은 주소로 닿는 이유

먼저 첫 번째 의문부터 살펴봤습니다. Pod를 다 지웠는데도 같은 Service 주소로 새 Pod에 닿던 일이었습니다. Service 주소는 그대로인데 그 뒤의 Pod IP는 분명 바뀌었습니다. "**지금 살아 있는 Pod는 이것들**"이라고 항상 최신으로 유지해 주는 프로그램이 따로 있어야 합니다.

그 프로그램이 **엔드포인트 컨트롤러(Endpoint Controller)** 입니다. Service의 selector(라벨)에 매칭되는 Pod들을 지켜보다가, Pod가 새로 뜨거나 사라지면 곧바로 해당 Service의 **Pod IP 목록**을 갱신합니다.

<div class="svg-figure">
<svg viewBox="0 0 760 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Endpoint Controller가 Pod의 변동을 감시해 Service의 Pod IP 목록을 최신으로 유지하는 구조">
  <defs>
    <marker id="ec-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">Endpoint Controller — Pod 변동 감시 후 IP 목록 갱신</text>
  <text x="120" y="50" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">실제 Pod 상태</text>
  <rect x="40" y="60" width="160" height="32" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="60" y="80" font-size="12" font-weight="700" fill="#0f172a">Pod A</text>
  <text x="180" y="80" text-anchor="end" font-size="13" font-weight="700" fill="#475569">✓</text>
  <rect x="40" y="105" width="160" height="32" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,3"/>
  <text x="60" y="125" font-size="12" font-weight="700" fill="#94a3b8" text-decoration="line-through">Pod B</text>
  <text x="180" y="125" text-anchor="end" font-size="13" font-weight="700" fill="#94a3b8">✗</text>
  <rect x="40" y="150" width="160" height="32" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="60" y="170" font-size="12" font-weight="700" fill="#7b341e">Pod C</text>
  <text x="180" y="170" text-anchor="end" font-size="13" font-weight="700" fill="#ff7849">+</text>
  <line x1="205" y1="121" x2="265" y2="121" stroke="#475569" stroke-width="1.6" marker-end="url(#ec-p)"/>
  <text x="235" y="113" text-anchor="middle" font-size="10" font-style="italic" fill="#475569">감시</text>
  <rect x="270" y="90" width="130" height="70" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="335" y="115" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">Endpoint</text>
  <text x="335" y="132" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">Controller</text>
  <text x="335" y="150" text-anchor="middle" font-size="9" fill="#7b341e">감시 → 갱신</text>
  <line x1="405" y1="121" x2="435" y2="121" stroke="#475569" stroke-width="1.6" marker-end="url(#ec-p)"/>
  <text x="420" y="113" text-anchor="middle" font-size="10" font-style="italic" fill="#475569">갱신</text>
  <text x="580" y="50" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">Pod IP 목록</text>
  <rect x="440" y="60" width="280" height="130" rx="8" fill="#fff" stroke="#1565c0" stroke-width="1.6"/>
  <text x="460" y="90" font-size="13" font-weight="700" fill="#475569">✓</text>
  <text x="478" y="90" font-size="12" font-weight="600" fill="#0f172a">Pod A · 유지</text>
  <text x="460" y="120" font-size="13" font-weight="700" fill="#94a3b8">✗</text>
  <text x="478" y="120" font-size="12" font-weight="600" fill="#94a3b8" text-decoration="line-through">Pod B · 제거됨</text>
  <text x="460" y="150" font-size="13" font-weight="700" fill="#ff7849">+</text>
  <text x="478" y="150" font-size="12" font-weight="600" fill="#7b341e">Pod C · 추가됨</text>
  <text x="580" y="178" text-anchor="middle" font-size="9" font-style="italic" fill="#6b7280">살아있는 Pod IP만 — kube-proxy로 전달</text>
</svg>
</div>

*그림 5-20. Endpoint Controller가 Pod 변동을 감시해 Pod IP 목록을 갱신합니다*

목록만 갱신된다고 요청이 새 Pod로 흘러가지는 않습니다. 가상 주소(ClusterIP)로 들어온 요청을 실제 Pod IP로 보내는 규칙도 같이 갱신되어야 합니다.

이 일을 맡은 프로그램이 **kube-proxy** 입니다. 클러스터의 모든 노드(서버) 입구에는 들어오고 나가는 짐들을 검사하는 게이트가 있고, kube-proxy는 그 게이트 앞에 "**이 ClusterIP가 적힌 짐은 저 Pod IP로 다시 붙여서 보내라**" 같은 안내문을 붙여 두는 사람입니다. 안내문 묶음이 바로 리눅스 커널이 들고 있는 규칙 목록, **iptables** 입니다. 살아있는 Pod 목록이 바뀌면 안내문에 적힌 Pod IP도 따라서 갱신됩니다.

<div class="svg-figure">
<svg viewBox="0 0 760 270" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="패킷은 리눅스 커널이 직접 처리하고, kube-proxy는 옆에서 iptables 규칙만 등록·갱신하는 구조">
  <defs>
    <marker id="kp-p" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
    <marker id="kp-r" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">패킷은 커널이 처리, kube-proxy는 옆에서 규칙만 관리</text>
  <rect x="40" y="80" width="140" height="60" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="110" y="105" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">Service 주소</text>
  <text x="110" y="125" text-anchor="middle" font-size="10" font-family="monospace" fill="#6b7280">ClusterIP (가상)</text>
  <line x1="180" y1="110" x2="225" y2="110" stroke="#475569" stroke-width="1.6" marker-end="url(#kp-p)"/>
  <rect x="225" y="80" width="240" height="60" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="345" y="105" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Linux 커널 (netfilter)</text>
  <text x="345" y="125" text-anchor="middle" font-size="10" font-family="monospace" fill="#7b341e">iptables 항목 대조 → DNAT</text>
  <line x1="465" y1="100" x2="510" y2="80" stroke="#475569" stroke-width="1.6" marker-end="url(#kp-p)"/>
  <line x1="465" y1="120" x2="510" y2="140" stroke="#475569" stroke-width="1.6" marker-end="url(#kp-p)"/>
  <rect x="515" y="60" width="130" height="40" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="580" y="78" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">Pod A</text>
  <text x="580" y="92" text-anchor="middle" font-size="10" font-family="monospace" fill="#6b7280">Pod IP</text>
  <rect x="515" y="120" width="130" height="40" rx="6" fill="#fff" stroke="#475569" stroke-width="1.4"/>
  <text x="580" y="138" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">Pod B</text>
  <text x="580" y="152" text-anchor="middle" font-size="10" font-family="monospace" fill="#6b7280">Pod IP</text>
  <line x1="345" y1="200" x2="345" y2="142" stroke="#475569" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#kp-r)"/>
  <text x="365" y="175" font-size="10" font-style="italic" font-weight="600" fill="#475569">규칙 등록·갱신</text>
  <rect x="225" y="200" width="240" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="345" y="222" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">kube-proxy</text>
  <text x="345" y="240" text-anchor="middle" font-size="10" fill="#475569">패킷에 손대지 않음 · 규칙 관리만</text>
</svg>
</div>

*그림 5-30. 패킷은 커널이 직접 처리하고, kube-proxy는 옆에서 iptables 항목만 등록·갱신합니다*

:::note
**kube-proxy와 iptables**

kube-proxy는 모든 워커 노드에서 동작하며, 리눅스 커널의 네트워크 규칙(iptables)을 관리합니다. 외부에서 들어오는 NodePort 요청이나 내부의 ClusterIP 요청을 가로채서 실제 Pod IP로 연결해 주는 역할을 맡습니다.
:::

첫 번째 의문은 여기서 풀립니다. Pod를 전부 지웠는데도 같은 Service 주소로 새 Pod에 연결된 이유는, Endpoint Controller가 새 Pod를 즉시 Pod IP 목록에 반영했고, kube-proxy가 그 목록을 보고 iptables 항목의 Pod IP를 새 Pod로 교체했기 때문입니다.

#### 두 번째 — 이름만 적었는데 진짜 Pod까지 닿는 이유

이제 두 번째 의문으로 넘어갑니다. 인그레스 YAML에 `order-service` 라는 이름만 적었는데 진짜 Pod까지 닿던 일이었습니다.

인그레스 컨트롤러가 받은 건 `order-service` 라는 이름이지 IP가 아닙니다. 그런데 kube-proxy가 등록해 둔 iptables 규칙은 ClusterIP로 향한 요청만 가로챕니다. 이름과 ClusterIP 사이를 이어 주는 프로그램이 따로 있어야 합니다.

그 프로그램이 **DNS** 입니다. 클러스터 안에는 전용 DNS 서버가 떠 있습니다. Service가 만들어지면 그 이름이 DNS에 자동으로 등록되고, 그 이름으로 부르면 DNS가 ClusterIP를 알려 줍니다.

DNS에 박히는 이름은 사실 `order-service` 한 단어가 아니라 `order-service.default.svc.cluster.local` 처럼 네임스페이스와 클러스터 도메인이 붙은 긴 형식입니다. 같은 네임스페이스 안에서는 `order-service` 한 단어만 적어도 풀어 줍니다. 또한 Pod가 만들어질 때 클러스터 DNS를 가리키는 설정이 안에 자동으로 박혀 있어서, 어떤 Pod든 코드에 이름만 적어도 자연스럽게 클러스터 DNS로 질의가 흘러갑니다.

<div class="svg-figure">
<svg viewBox="0 0 760 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="클러스터 DNS(CoreDNS)가 Service 이름을 ClusterIP로 변환하는 구조">
  <defs>
    <marker id="dn-r" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
    <marker id="dn-g" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">클러스터 DNS — Service 이름 → ClusterIP 변환</text>
  <rect x="100" y="50" width="560" height="125" rx="8" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="380" y="75" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">클러스터 DNS (CoreDNS)</text>
  <line x1="120" y1="85" x2="640" y2="85" stroke="#fcd4bf" stroke-width="0.8"/>
  <text x="130" y="105" font-family="monospace" font-size="11" fill="#0f172a">order-service.default.svc.cluster.local</text>
  <text x="630" y="105" text-anchor="end" font-family="monospace" font-size="11" font-weight="700" fill="#1565c0">10.96.0.20</text>
  <text x="130" y="125" font-family="monospace" font-size="11" fill="#0f172a">payments.default.svc.cluster.local</text>
  <text x="630" y="125" text-anchor="end" font-family="monospace" font-size="11" font-weight="700" fill="#1565c0">10.96.0.31</text>
  <text x="130" y="145" font-family="monospace" font-size="11" fill="#0f172a">stores.default.svc.cluster.local</text>
  <text x="630" y="145" text-anchor="end" font-family="monospace" font-size="11" font-weight="700" fill="#1565c0">10.96.0.42</text>
  <text x="380" y="166" text-anchor="middle" font-size="9" font-style="italic" fill="#7b341e">Service 생성 시 자동 등록, 삭제 시 자동 제거</text>
  <line x1="300" y1="220" x2="300" y2="180" stroke="#475569" stroke-width="1.6" marker-end="url(#dn-r)"/>
  <text x="285" y="200" text-anchor="end" font-size="10" font-weight="700" fill="#0f172a">① 이름 질의</text>
  <text x="285" y="215" text-anchor="end" font-size="10" font-style="italic" font-family="monospace" fill="#475569">"order-service?"</text>
  <line x1="460" y1="180" x2="460" y2="220" stroke="#ff7849" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#dn-g)"/>
  <text x="475" y="200" font-size="10" font-weight="700" fill="#7b341e">② ClusterIP 응답</text>
  <text x="475" y="215" font-size="10" font-style="italic" font-family="monospace" fill="#7b341e">"10.96.0.20"</text>
  <rect x="100" y="220" width="560" height="50" rx="8" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="380" y="243" text-anchor="middle" font-size="12" font-weight="700" fill="#0f172a">호출자 (Pod / Ingress Controller)</text>
  <text x="380" y="260" text-anchor="middle" font-size="10" fill="#6b7280">Pod 생성 시 /etc/resolv.conf → 클러스터 DNS 자동 설정</text>
</svg>
</div>

*그림 5-31. DNS가 Service 이름을 ClusterIP로 변환합니다*

:::note
**클러스터 DNS**

쿠버네티스는 클러스터 안에 DNS 서버를 함께 띄워 둡니다. Pod가 다른 Service를 이름으로 부르면 이 DNS가 자동으로 ClusterIP를 알려 줍니다. 별도 설정 없이 기본으로 동작합니다. Docker에서 본 Docker DNS(127.0.0.11)와 같은 역할이고, 쿠버네티스에서는 이 DNS를 **CoreDNS**라 부릅니다.
:::

두 번째 의문도 여기서 풀립니다. 컨트롤러가 `order-service` 라는 이름으로 백엔드를 부를 때, 먼저 DNS가 이름을 ClusterIP로 바꾸고, 그다음 kube-proxy가 ClusterIP를 살아있는 Pod IP로 바꿉니다. 이름이 Pod까지 닿기까지 두 단계 변환이 일어납니다.

*'Service 뒤에서 셋이 함께 움직이고 있었구나. Endpoint Controller가 Pod IP 목록을 챙기고, kube-proxy가 길을 깔고, DNS가 이름을 풀고.'*

### 5.3.2 요청의 흐름

의문이 풀리고 나니 처음 막혔던 한 줄을 이제 그어 볼 만했습니다. 외부에서 들어온 한 요청이 백엔드 Pod까지 닿는 전체 흐름을 한 단계씩 따라가 봤습니다. 먼저 다섯 단계가 클러스터 안 어디에서 일어나는지 한 그림으로 그려 두면 다음과 같습니다.

<div class="svg-figure">
<svg viewBox="0 0 1080 600" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="요청이 Pod까지 닿는 전체 흐름 — 다섯 단계가 클러스터 안에서 일어나는 위치">
  <defs>
    <marker id="ov-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#94a3b8"/></marker>
    <marker id="ov-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="ov-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="540" y="26" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2937">전체 흐름 한눈에 — 다섯 단계가 일어나는 위치</text>
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
  <text x="302" y="190" text-anchor="middle" font-size="12" font-family="monospace" fill="#7b341e">:9000</text>
  <text x="302" y="234" text-anchor="middle" font-size="9" fill="#7b341e">NodePort Service</text>
  <line x1="370" y1="170" x2="490" y2="170" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <circle cx="430" cy="153" r="11" fill="#ff7849"/>
  <text x="430" y="157" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">2</text>
  <rect x="490" y="150" width="100" height="40" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="540" y="174" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Kube Proxy</text>
  <line x1="590" y1="170" x2="640" y2="170" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <rect x="640" y="150" width="180" height="40" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="730" y="174" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Ingress Controller Pod</text>
  <rect x="900" y="135" width="140" height="80" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="970" y="160" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">클러스터 DNS</text>
  <text x="970" y="180" text-anchor="middle" font-size="10" fill="#7b341e">이름 → ClusterIP</text>
  <line x1="822" y1="160" x2="898" y2="155" stroke="#475569" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#ov-s)"/>
  <line x1="898" y1="195" x2="822" y2="190" stroke="#ff7849" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#ov-a)"/>
  <rect x="420" y="245" width="600" height="65" rx="32" fill="#f5faff" stroke="#bfdbfe" stroke-width="1"/>
  <text x="1005" y="260" text-anchor="end" font-size="10" font-weight="700" fill="#94a3b8">L7</text>
  <line x1="730" y1="190" x2="600" y2="245" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <line x1="730" y1="190" x2="850" y2="245" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <circle cx="660" cy="218" r="11" fill="#ff7849"/>
  <text x="660" y="222" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">3</text>
  <rect x="540" y="262" width="120" height="32" rx="16" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="600" y="283" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Service A</text>
  <rect x="790" y="262" width="120" height="32" rx="16" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="850" y="283" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Service B</text>
  <line x1="600" y1="310" x2="600" y2="335" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <line x1="850" y1="310" x2="850" y2="335" stroke="#ff7849" stroke-width="2.2" marker-end="url(#ov-a)"/>
  <circle cx="730" cy="320" r="11" fill="#ff7849"/>
  <text x="730" y="324" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">4</text>
  <rect x="420" y="335" width="600" height="100" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="1005" y="350" text-anchor="end" font-size="10" font-weight="700" fill="#94a3b8">L4</text>
  <rect x="490" y="365" width="220" height="55" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="505" y="382" font-size="10" font-weight="700" fill="#7b341e">Node 1</text>
  <text x="695" y="382" text-anchor="end" font-size="9" font-family="monospace" fill="#7b341e">port :9000</text>
  <rect x="555" y="390" width="100" height="22" rx="4" fill="#fff4ed" stroke="#ff7849" stroke-width="1.4"/>
  <text x="605" y="405" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">Kube Proxy</text>
  <rect x="740" y="365" width="220" height="55" rx="6" fill="#fff" stroke="#ff7849" stroke-width="1.8"/>
  <text x="755" y="382" font-size="10" font-weight="700" fill="#7b341e">Node 2</text>
  <text x="945" y="382" text-anchor="end" font-size="9" font-family="monospace" fill="#7b341e">port :9000</text>
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
  <text x="730" y="434" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">5</text>
  <rect x="510" y="453" width="200" height="40" rx="6" fill="none" stroke="#ff7849" stroke-width="1.4" stroke-dasharray="4,3"/>
  <rect x="525" y="461" width="65" height="24" rx="12" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="557" y="477" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">Pod A</text>
  <rect x="615" y="461" width="65" height="24" rx="12" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="647" y="477" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">Pod A</text>
  <rect x="760" y="453" width="200" height="40" rx="6" fill="none" stroke="#ff7849" stroke-width="1.4" stroke-dasharray="4,3"/>
  <rect x="775" y="461" width="65" height="24" rx="12" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="807" y="477" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">Pod A</text>
  <rect x="865" y="461" width="65" height="24" rx="12" fill="#fff4ed" stroke="#ff7849" stroke-width="1.6"/>
  <text x="897" y="477" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">Pod B</text>
  <line x1="610" y1="493" x2="710" y2="525" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,2"/>
  <line x1="850" y1="493" x2="780" y2="525" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,2"/>
  <rect x="610" y="525" width="270" height="35" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4,3"/>
  <text x="745" y="547" text-anchor="middle" font-size="11" font-weight="600" fill="#94a3b8">Deployment</text>
</svg>
</div>

다섯 단계는 위 그림에서 ①~⑤ 위치를 차례로 짚어 가는 흐름입니다. 5.2의 비유를 빌리면, 고객이 본사 **공식 앱**(Ingress)으로 주문을 넣을 때 앱 내부에서 일어나는 일을 줌인해서 봅니다. 한 단계씩 비유로 먼저 풀고, 곧이어 같은 단계의 IT 구조를 봅니다.

**1단계 — 외부 입구 통과: 고객이 공식 앱을 연다**

휴대폰을 켠 고객이 본사 공식 앱 아이콘을 누릅니다. 앱은 본사가 외부에 공개해 둔 **공식 입구**(주소·포트)를 통해서만 안으로 들어갈 수 있습니다.

<div class="svg-figure">
<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="STEP 1 비유 — 고객이 본사 공식 앱 아이콘을 눌러 앱에 진입">
  <defs>
    <marker id="m1-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">고객이 본사 공식 앱 아이콘을 누른다</text>
  <g transform="translate(80, 90)">
    <circle cx="40" cy="0" r="20" fill="#fff" stroke="#475569" stroke-width="1.8"/>
    <path d="M 10 28 Q 10 60 40 60 Q 70 60 70 28 L 70 95 L 10 95 Z" fill="#fff" stroke="#475569" stroke-width="1.8"/>
  </g>
  <text x="120" y="210" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">고객</text>
  <line x1="180" y1="135" x2="290" y2="135" stroke="#ff7849" stroke-width="2.6" marker-end="url(#m1-a)"/>
  <text x="235" y="124" text-anchor="middle" font-size="11" font-style="italic" fill="#7b341e">앱 아이콘 누름</text>
  <g transform="translate(300, 60)">
    <rect x="0" y="0" width="160" height="160" rx="18" fill="#fff" stroke="#475569" stroke-width="2"/>
    <rect x="10" y="14" width="140" height="124" rx="3" fill="#fff4ed" stroke="#fbbf24" stroke-width="1.4"/>
    <circle cx="80" cy="55" r="22" fill="#ff7849"/>
    <text x="80" y="61" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">앱</text>
    <text x="80" y="100" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">본사 공식 앱</text>
    <text x="80" y="118" text-anchor="middle" font-size="9" fill="#7b341e">공식 주소·포트</text>
    <circle cx="80" cy="148" r="7" fill="none" stroke="#475569" stroke-width="1.4"/>
  </g>
  <line x1="476" y1="135" x2="556" y2="135" stroke="#ff7849" stroke-width="2.6" marker-end="url(#m1-a)"/>
  <text x="516" y="124" text-anchor="middle" font-size="11" font-style="italic" fill="#7b341e">앱 진입</text>
  <rect x="560" y="80" width="160" height="120" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="640" y="120" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">앱 메인 화면</text>
  <text x="640" y="140" text-anchor="middle" font-size="10" fill="#7b341e">(요청이 본사 안에</text>
  <text x="640" y="155" text-anchor="middle" font-size="10" fill="#7b341e">도착함)</text>
  <text x="640" y="180" text-anchor="middle" font-size="9" font-style="italic" fill="#7b341e">↓ 다음: 안내 직원에게 배달</text>
</svg>
</div>

이 비유를 IT로 옮기면 두 가지가 짝지어집니다.

| 비유 | IT 용어 | 한 줄 설명 |
|:---:|:---|:---|
| 고객 | **외부 호스트** | 클러스터 바깥에서 요청을 보내는 사용자입니다 |
| 공식 앱 입구 (주소·포트) | **NodePort** | 외부 요청이 클러스터로 진입하는 공개 포트입니다 |

브라우저에서 `http://localhost/order` 같은 주소로 요청을 보내면, 노드에 뚫린 NodePort(또는 클라우드의 LoadBalancer)를 통해 클러스터 안으로 들어옵니다. 5.2.3에서 띄워 둔 `minikube tunnel` 이 바로 이 입구를 호스트와 이어 주는 통로입니다. 아직 HTTP 본문은 들여다보지 않은 상태입니다.

<div class="svg-figure">
<svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="STEP 1 — 외부 요청이 NodePort 입구로 클러스터에 진입">
  <defs>
    <marker id="fl1-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#cbd5e1"/></marker>
    <marker id="fl1-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <rect x="20" y="14" width="142" height="34" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="91" y="28" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">STEP 1</text>
  <text x="91" y="42" text-anchor="middle" font-size="10" fill="#7b341e">진입 (NodePort)</text>
  <line x1="166" y1="31" x2="178" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl1-d)"/>
  <rect x="180" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="251" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 2</text>
  <text x="251" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">배달 (kube-proxy)</text>
  <line x1="326" y1="31" x2="338" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl1-d)"/>
  <rect x="340" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="411" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 3</text>
  <text x="411" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">라우팅 (Ingress + DNS)</text>
  <line x1="486" y1="31" x2="498" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl1-d)"/>
  <rect x="500" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="571" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 4</text>
  <text x="571" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">NAT (kube-proxy 2차)</text>
  <line x1="646" y1="31" x2="658" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl1-d)"/>
  <rect x="660" y="14" width="120" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="720" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 5</text>
  <text x="720" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">도달 (Pod)</text>
  <text x="40" y="100" font-size="11" font-weight="600" fill="#475569">로컬호스트</text>
  <rect x="40" y="112" width="140" height="84" rx="6" fill="#fff" stroke="#475569" stroke-width="1.6"/>
  <text x="110" y="160" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">Host</text>
  <line x1="180" y1="154" x2="278" y2="154" stroke="#ff7849" stroke-width="2.6" marker-end="url(#fl1-a)"/>
  <text x="229" y="142" text-anchor="middle" font-size="12" font-family="monospace" font-weight="700" fill="#7b341e">localhost:9000</text>
  <rect x="288" y="80" width="220" height="170" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="1.8"/>
  <text x="398" y="102" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">클러스터 입구</text>
  <rect x="316" y="116" width="164" height="100" rx="8" fill="#fff" stroke="#ff7849" stroke-width="2.6"/>
  <text x="398" y="152" text-anchor="middle" font-size="18" font-weight="700" fill="#7b341e">NodePort</text>
  <text x="398" y="178" text-anchor="middle" font-size="15" font-family="monospace" fill="#7b341e">:9000</text>
  <text x="398" y="237" text-anchor="middle" font-size="11" fill="#7b341e">NodePort Service</text>
  <line x1="510" y1="170" x2="568" y2="170" stroke="#cbd5e1" stroke-width="1.4" marker-end="url(#fl1-d)"/>
  <rect x="568" y="135" width="200" height="80" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4" stroke-dasharray="4,3"/>
  <text x="668" y="160" text-anchor="middle" font-size="11" font-style="italic" fill="#94a3b8">다음 단계 (STEP 2)</text>
  <text x="668" y="182" text-anchor="middle" font-size="13" font-weight="700" fill="#94a3b8">Kube Proxy 가</text>
  <text x="668" y="200" text-anchor="middle" font-size="12" fill="#94a3b8">Ingress로 배달</text>
</svg>
</div>

*그림 5-32. 외부 요청이 NodePort(또는 LoadBalancer)로 진입. 실습에선 `minikube tunnel` 이 이 입구 역할*

**2단계 — 앱 내부 라우터가 안내 직원에게 배달**

앱에 들어온 요청은 곧장 매장으로 가지 않습니다. 먼저 앱 내부의 **라우터**가 요청을 받아 **메인 화면 안내 직원**에게 넘겨줍니다. 이 라우터는 주소·포트만 보고 옮기는 단순한 배달부 역할입니다.

<div class="svg-figure">
<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="STEP 2 비유 — 앱 입구에서 내부 라우터를 거쳐 메인 화면 안내 직원에게 배달">
  <defs>
    <marker id="m2-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">앱 입구 → 내부 라우터 → 메인 화면 안내 직원</text>
  <rect x="40" y="80" width="160" height="80" rx="10" fill="#fff" stroke="#cbd5e1" stroke-width="1.6"/>
  <text x="120" y="118" text-anchor="middle" font-size="13" font-weight="600" fill="#94a3b8">앱 입구</text>
  <text x="120" y="140" text-anchor="middle" font-size="10" fill="#94a3b8">(이전 단계)</text>
  <line x1="200" y1="120" x2="280" y2="120" stroke="#ff7849" stroke-width="2.6" marker-end="url(#m2-a)"/>
  <text x="240" y="110" text-anchor="middle" font-size="11" font-style="italic" fill="#7b341e">전달</text>
  <rect x="280" y="80" width="180" height="80" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="370" y="115" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">내부 라우터</text>
  <text x="370" y="135" text-anchor="middle" font-size="10" fill="#7b341e">(주소만 보고 배달)</text>
  <line x1="460" y1="120" x2="540" y2="120" stroke="#ff7849" stroke-width="2.6" marker-end="url(#m2-a)"/>
  <text x="500" y="110" text-anchor="middle" font-size="11" font-style="italic" fill="#7b341e">배달</text>
  <rect x="540" y="60" width="180" height="120" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="630" y="100" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">메인 화면</text>
  <text x="630" y="120" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">안내 직원</text>
  <text x="630" y="148" text-anchor="middle" font-size="9" font-style="italic" fill="#7b341e">↓ 다음: 주문서 읽기</text>
</svg>
</div>

이 비유를 IT로 옮기면 두 가지가 짝지어집니다.

| 비유 | IT 용어 | 한 줄 설명 |
|:---:|:---|:---|
| 내부 라우터 | **kube-proxy(1차)** | iptables 항목으로 패킷의 도착지를 옮기는 배달부입니다 |
| 메인 화면 안내 직원 | **Ingress Controller Pod** | 다음 단계에서 URL을 읽고 백엔드를 정하는 컨트롤러 Pod입니다 |

들어온 요청은 kube-proxy가 미리 등록해 둔 iptables 항목을 타고 인그레스 컨트롤러 Pod로 배달됩니다. 패킷의 도착지 IP·Port만 보고 옮길 뿐, HTTP 본문은 아직 들여다보지 않습니다.

<div class="svg-figure">
<svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="STEP 2 — kube-proxy(1차)가 NodePort로 들어온 요청을 Ingress Controller Pod로 전달">
  <defs>
    <marker id="fl2-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#cbd5e1"/></marker>
    <marker id="fl2-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <rect x="20" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="91" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 1</text>
  <text x="91" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">진입 (NodePort)</text>
  <line x1="166" y1="31" x2="178" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl2-d)"/>
  <rect x="180" y="14" width="142" height="34" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="251" y="28" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">STEP 2</text>
  <text x="251" y="42" text-anchor="middle" font-size="10" fill="#7b341e">배달 (kube-proxy)</text>
  <line x1="326" y1="31" x2="338" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl2-d)"/>
  <rect x="340" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="411" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 3</text>
  <text x="411" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">라우팅 (Ingress + DNS)</text>
  <line x1="486" y1="31" x2="498" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl2-d)"/>
  <rect x="500" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="571" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 4</text>
  <text x="571" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">NAT (kube-proxy 2차)</text>
  <line x1="646" y1="31" x2="658" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl2-d)"/>
  <rect x="660" y="14" width="120" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="720" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 5</text>
  <text x="720" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">도달 (Pod)</text>
  <rect x="20" y="135" width="120" height="80" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="80" y="170" text-anchor="middle" font-size="13" font-weight="700" fill="#94a3b8">NodePort</text>
  <text x="80" y="190" text-anchor="middle" font-size="11" font-family="monospace" fill="#94a3b8">:9000</text>
  <line x1="142" y1="175" x2="200" y2="175" stroke="#ff7849" stroke-width="2.6" marker-end="url(#fl2-a)"/>
  <text x="171" y="165" text-anchor="middle" font-size="10" font-style="italic" fill="#7b341e">전달</text>
  <rect x="200" y="135" width="170" height="80" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="285" y="172" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">Kube Proxy</text>
  <text x="285" y="192" text-anchor="middle" font-size="10" fill="#7b341e">(iptables 규칙)</text>
  <line x1="370" y1="175" x2="430" y2="175" stroke="#ff7849" stroke-width="2.6" marker-end="url(#fl2-a)"/>
  <text x="400" y="165" text-anchor="middle" font-size="10" font-style="italic" fill="#7b341e">배달</text>
  <rect x="430" y="135" width="200" height="80" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="530" y="167" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">Ingress Controller</text>
  <text x="530" y="186" text-anchor="middle" font-size="11" font-weight="700" fill="#7b341e">Pod</text>
  <text x="530" y="204" text-anchor="middle" font-size="10" fill="#7b341e">(L7 처리 시작)</text>
  <rect x="650" y="135" width="130" height="80" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4" stroke-dasharray="4,3"/>
  <text x="715" y="160" text-anchor="middle" font-size="10" font-style="italic" fill="#94a3b8">다음 단계</text>
  <text x="715" y="178" text-anchor="middle" font-size="11" font-weight="700" fill="#94a3b8">URL 읽고</text>
  <text x="715" y="195" text-anchor="middle" font-size="11" font-weight="700" fill="#94a3b8">Service 선택</text>
  <text x="715" y="210" text-anchor="middle" font-size="9" fill="#94a3b8">(STEP 3)</text>
</svg>
</div>

*그림 5-33. iptables 규칙을 따라 Ingress Controller Pod로 전달*

**3단계 — 안내 직원이 주문서 읽고 매장 명단으로 매장 결정**

안내 직원이 고객의 **주문서**(URL)를 펼쳐 읽습니다. "**짜장면 주문이네. 어느 매장으로 보낼까?**"라고 본사 **매장 명단**(이름 → 위치)을 조회합니다. 명단이 매장 이름을 매장 위치 번호로 풀어 주면, 직원은 그 위치 번호를 손에 쥐고 다음 단계로 넘깁니다.

<div class="svg-figure">
<svg viewBox="0 0 760 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="STEP 3 비유 — 안내 직원이 주문서를 읽고 매장 명단으로 매장 위치를 풀어 결정">
  <defs>
    <marker id="m3-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="m3-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">안내 직원이 주문서 읽고 매장 명단 조회 → 매장 결정</text>
  <rect x="40" y="80" width="180" height="80" rx="10" fill="#fff" stroke="#cbd5e1" stroke-width="1.6"/>
  <text x="130" y="115" text-anchor="middle" font-size="13" font-weight="600" fill="#94a3b8">메인 화면</text>
  <text x="130" y="133" text-anchor="middle" font-size="13" font-weight="600" fill="#94a3b8">안내 직원</text>
  <text x="130" y="152" text-anchor="middle" font-size="10" fill="#94a3b8">(주문서 펼침)</text>
  <line x1="220" y1="105" x2="280" y2="105" stroke="#475569" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#m3-s)"/>
  <text x="250" y="95" text-anchor="middle" font-size="10" font-style="italic" fill="#475569">"짜장면 매장?"</text>
  <line x1="280" y1="135" x2="220" y2="135" stroke="#ff7849" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#m3-a)"/>
  <text x="250" y="150" text-anchor="middle" font-size="10" font-style="italic" fill="#7b341e">"2층 5호점"</text>
  <rect x="280" y="80" width="180" height="80" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="370" y="110" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">매장 명단</text>
  <text x="370" y="128" text-anchor="middle" font-size="10" fill="#7b341e">이름 → 위치 번호</text>
  <text x="370" y="148" text-anchor="middle" font-size="9" fill="#7b341e">(자동 갱신)</text>
  <text x="130" y="195" text-anchor="middle" font-size="10" font-weight="600" fill="#7b341e">↓ 위치 번호로 분기</text>
  <line x1="130" y1="200" x2="540" y2="225" stroke="#ff7849" stroke-width="2.6" marker-end="url(#m3-a)"/>
  <line x1="130" y1="200" x2="660" y2="225" stroke="#ff7849" stroke-width="2.6" marker-end="url(#m3-a)"/>
  <rect x="500" y="225" width="120" height="32" rx="16" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="560" y="246" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">매장 A 위치</text>
  <rect x="640" y="225" width="100" height="32" rx="16" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="690" y="246" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">매장 B 위치</text>
</svg>
</div>

이 비유를 IT로 옮기면 세 가지가 짝지어집니다.

| 비유 | IT 용어 | 한 줄 설명 |
|:---:|:---|:---|
| 안내 직원 | **Ingress Controller** | URL 경로와 도메인 헤더로 어느 백엔드 Service에 보낼지 정합니다 |
| 매장 명단 (이름 → 위치) | **클러스터 DNS (CoreDNS)** | Service 이름을 ClusterIP로 풀어 줍니다 |
| 매장 위치 번호 | **ClusterIP** | Service의 가상 진입 IP입니다 |

Ingress Controller는 도착한 요청의 HTTP 본문을 읽습니다. URL 경로와 도메인 헤더를 등록된 Ingress 규칙과 대조해 "**이 요청은 `order-service` 로 보낸다**"고 정합니다. 이름이 정해진 직후, 이름만으로는 패킷을 보낼 수 없으니 클러스터 DNS가 곧바로 `order-service` 를 ClusterIP로 풀어 줍니다.

<div class="svg-figure">
<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="STEP 3 — Ingress Controller가 URL 읽고 Service 선택, DNS가 이름을 ClusterIP로 변환">
  <defs>
    <marker id="fl3-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#cbd5e1"/></marker>
    <marker id="fl3-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="fl3-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <rect x="20" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="91" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 1</text>
  <text x="91" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">진입 (NodePort)</text>
  <line x1="166" y1="31" x2="178" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl3-d)"/>
  <rect x="180" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="251" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 2</text>
  <text x="251" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">배달 (kube-proxy)</text>
  <line x1="326" y1="31" x2="338" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl3-d)"/>
  <rect x="340" y="14" width="142" height="34" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="411" y="28" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">STEP 3</text>
  <text x="411" y="42" text-anchor="middle" font-size="10" fill="#7b341e">라우팅 (Ingress + DNS)</text>
  <line x1="486" y1="31" x2="498" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl3-d)"/>
  <rect x="500" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="571" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 4</text>
  <text x="571" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">NAT (kube-proxy 2차)</text>
  <line x1="646" y1="31" x2="658" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl3-d)"/>
  <rect x="660" y="14" width="120" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="720" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 5</text>
  <text x="720" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">도달 (Pod)</text>
  <rect x="20" y="100" width="200" height="80" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="120" y="132" text-anchor="middle" font-size="13" font-weight="700" fill="#94a3b8">Ingress Controller</text>
  <text x="120" y="152" text-anchor="middle" font-size="11" fill="#94a3b8">Pod</text>
  <text x="120" y="170" text-anchor="middle" font-size="10" fill="#94a3b8">(URL 읽음)</text>
  <line x1="220" y1="125" x2="280" y2="125" stroke="#475569" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#fl3-s)"/>
  <text x="250" y="115" text-anchor="middle" font-size="10" font-style="italic" font-family="monospace" fill="#475569">"order-service?"</text>
  <line x1="280" y1="155" x2="220" y2="155" stroke="#ff7849" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#fl3-a)"/>
  <text x="250" y="170" text-anchor="middle" font-size="10" font-style="italic" font-family="monospace" fill="#7b341e">"10.96.0.20"</text>
  <rect x="280" y="100" width="180" height="80" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="370" y="130" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">클러스터 DNS</text>
  <text x="370" y="148" text-anchor="middle" font-size="11" fill="#7b341e">(CoreDNS)</text>
  <text x="370" y="168" text-anchor="middle" font-size="10" fill="#7b341e">이름 → ClusterIP</text>
  <text x="120" y="218" text-anchor="middle" font-size="10" font-weight="600" fill="#7b341e">↓ ClusterIP로 분기</text>
  <line x1="120" y1="225" x2="270" y2="240" stroke="#ff7849" stroke-width="2.6" marker-end="url(#fl3-a)"/>
  <line x1="120" y1="225" x2="510" y2="240" stroke="#ff7849" stroke-width="2.6" marker-end="url(#fl3-a)"/>
  <rect x="270" y="240" width="160" height="40" rx="20" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="350" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Service A</text>
  <rect x="510" y="240" width="160" height="40" rx="20" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="590" y="265" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Service B</text>
  <text x="400" y="305" text-anchor="middle" font-size="10" font-style="italic" fill="#94a3b8">다음 단계 (STEP 4): kube-proxy(2차)가 Pod IP로 변환</text>
</svg>
</div>

*그림 5-34. Ingress Controller가 URL을 읽고 Service를 선택, 그 직후 DNS가 이름을 ClusterIP로 변환*

**4단계 — 매장 분배 시스템이 매장 직원에게 전달**

매장 위치 번호가 손에 들렸지만 그 매장에는 직원이 여러 명 있을 수 있습니다. 위치 번호를 받은 **매장 분배 시스템**이 살아 있는 매장 직원 중 한 명을 골라 요청을 전달합니다. 분배 시스템은 본사 운영팀이 늘 갱신해 두는 **매장 직원 명단**을 보고 결정합니다.

<div class="svg-figure">
<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="STEP 4 비유 — 매장 위치 번호를 받은 분배 시스템이 살아 있는 매장 직원 중 하나를 선택">
  <defs>
    <marker id="m4-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">매장 위치 번호 → 분배 시스템 → 매장 직원 한 명</text>
  <rect x="40" y="90" width="160" height="60" rx="30" fill="#fff" stroke="#cbd5e1" stroke-width="1.6"/>
  <text x="120" y="118" text-anchor="middle" font-size="13" font-weight="600" fill="#94a3b8">매장 위치 번호</text>
  <text x="120" y="138" text-anchor="middle" font-size="10" fill="#94a3b8">(이전 단계)</text>
  <line x1="200" y1="120" x2="280" y2="120" stroke="#ff7849" stroke-width="2.6" marker-end="url(#m4-a)"/>
  <text x="240" y="110" text-anchor="middle" font-size="11" font-style="italic" fill="#7b341e">전달</text>
  <rect x="280" y="80" width="200" height="100" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="380" y="115" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">매장 분배 시스템</text>
  <text x="380" y="135" text-anchor="middle" font-size="10" fill="#7b341e">살아 있는 매장 직원</text>
  <text x="380" y="152" text-anchor="middle" font-size="10" fill="#7b341e">명단 확인</text>
  <text x="380" y="170" text-anchor="middle" font-size="9" fill="#7b341e">(부하 분산)</text>
  <line x1="480" y1="105" x2="560" y2="80" stroke="#ff7849" stroke-width="2.6" marker-end="url(#m4-a)"/>
  <line x1="480" y1="135" x2="560" y2="160" stroke="#ff7849" stroke-width="2.6" marker-end="url(#m4-a)"/>
  <rect x="560" y="60" width="160" height="40" rx="20" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="640" y="85" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">매장 직원 1</text>
  <rect x="560" y="140" width="160" height="40" rx="20" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="640" y="165" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">매장 직원 2</text>
</svg>
</div>

이 비유를 IT로 옮기면 두 가지가 짝지어집니다.

| 비유 | IT 용어 | 한 줄 설명 |
|:---:|:---|:---|
| 매장 분배 시스템 | **kube-proxy(2차)** | ClusterIP를 살아있는 Pod IP로 변환하는 L4 로드밸런서입니다 |
| 매장 직원 명단 | **Pod IP 목록** | Service에 묶인 살아있는 백엔드 Pod의 IP 목록입니다 |

ClusterIP로 향한 요청은 다시 같은 노드의 kube-proxy(2차)가 가로채, Pod IP 목록에서 살아있는 Pod 중 하나의 IP로 바꿔 보냅니다.

<div class="svg-figure">
<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="STEP 4 — kube-proxy(2차)가 ClusterIP를 Pod IP로 변환 (L4 로드밸런싱)">
  <defs>
    <marker id="fl4-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#cbd5e1"/></marker>
    <marker id="fl4-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
  </defs>
  <rect x="20" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="91" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 1</text>
  <text x="91" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">진입 (NodePort)</text>
  <line x1="166" y1="31" x2="178" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl4-d)"/>
  <rect x="180" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="251" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 2</text>
  <text x="251" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">배달 (kube-proxy)</text>
  <line x1="326" y1="31" x2="338" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl4-d)"/>
  <rect x="340" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="411" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 3</text>
  <text x="411" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">라우팅 (Ingress + DNS)</text>
  <line x1="486" y1="31" x2="498" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl4-d)"/>
  <rect x="500" y="14" width="142" height="34" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="571" y="28" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">STEP 4</text>
  <text x="571" y="42" text-anchor="middle" font-size="10" fill="#7b341e">NAT (kube-proxy 2차)</text>
  <line x1="646" y1="31" x2="658" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl4-d)"/>
  <rect x="660" y="14" width="120" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="720" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 5</text>
  <text x="720" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">도달 (Pod)</text>
  <rect x="100" y="100" width="160" height="40" rx="20" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="180" y="125" text-anchor="middle" font-size="13" font-weight="600" fill="#94a3b8">Service A (ClusterIP)</text>
  <rect x="540" y="100" width="160" height="40" rx="20" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="620" y="125" text-anchor="middle" font-size="13" font-weight="600" fill="#94a3b8">Service B (ClusterIP)</text>
  <line x1="180" y1="142" x2="180" y2="180" stroke="#ff7849" stroke-width="2.6" marker-end="url(#fl4-a)"/>
  <text x="200" y="166" font-size="10" font-style="italic" fill="#7b341e">DNAT</text>
  <line x1="620" y1="142" x2="620" y2="180" stroke="#ff7849" stroke-width="2.6" marker-end="url(#fl4-a)"/>
  <text x="640" y="166" font-size="10" font-style="italic" fill="#7b341e">DNAT</text>
  <rect x="60" y="180" width="240" height="100" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="80" y="200" font-size="11" font-weight="700" fill="#7b341e">Node 1</text>
  <text x="285" y="200" text-anchor="end" font-size="10" font-family="monospace" fill="#7b341e">port :9000</text>
  <rect x="100" y="215" width="160" height="40" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="180" y="240" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Kube Proxy</text>
  <text x="180" y="270" text-anchor="middle" font-size="10" fill="#7b341e">→ 살아있는 Pod IP 선택</text>
  <rect x="500" y="180" width="240" height="100" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="520" y="200" font-size="11" font-weight="700" fill="#7b341e">Node 2</text>
  <text x="725" y="200" text-anchor="end" font-size="10" font-family="monospace" fill="#7b341e">port :9000</text>
  <rect x="540" y="215" width="160" height="40" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="620" y="240" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Kube Proxy</text>
  <text x="620" y="270" text-anchor="middle" font-size="10" fill="#7b341e">→ 살아있는 Pod IP 선택</text>
  <text x="400" y="305" text-anchor="middle" font-size="10" font-style="italic" fill="#94a3b8">다음 단계 (STEP 5): 선택된 Pod에 도달</text>
</svg>
</div>

*그림 5-35. kube-proxy(2차)가 ClusterIP를 Pod IP로 변환 (L4 로드밸런싱)*

**5단계 — 매장 직원이 응답 + 본사 운영팀이 명단 갱신**

매장 직원이 주문을 받아 처리하고 응답을 돌려보냅니다. 그 사이 다섯 단계 내내 보이지 않게 일하는 사람이 있습니다. **본사 운영팀**입니다. 매장 직원이 새로 들어오거나 그만두면 곧바로 매장 직원 명단을 갱신해서, 4단계의 분배 시스템이 늘 살아 있는 직원만 배정하도록 받쳐 줍니다.

<div class="svg-figure">
<svg viewBox="0 0 760 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="STEP 5 비유 — 매장 직원이 응답하고, 본사 운영팀이 매장 직원 명단을 항상 갱신">
  <defs>
    <marker id="m5-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="m5-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <text x="380" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2937">매장 직원 응답 + 본사 운영팀이 직원 명단 갱신</text>
  <rect x="40" y="80" width="160" height="60" rx="30" fill="#fff" stroke="#cbd5e1" stroke-width="1.6"/>
  <text x="120" y="108" text-anchor="middle" font-size="13" font-weight="600" fill="#94a3b8">분배 시스템</text>
  <text x="120" y="128" text-anchor="middle" font-size="10" fill="#94a3b8">(이전 단계)</text>
  <line x1="200" y1="110" x2="280" y2="110" stroke="#ff7849" stroke-width="2.6" marker-end="url(#m5-a)"/>
  <text x="240" y="100" text-anchor="middle" font-size="11" font-style="italic" fill="#7b341e">배정</text>
  <rect x="280" y="70" width="280" height="100" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="420" y="95" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">매장 직원 그룹</text>
  <rect x="305" y="110" width="100" height="34" rx="17" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="355" y="132" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">직원 1</text>
  <rect x="435" y="110" width="100" height="34" rx="17" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="485" y="132" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">직원 2</text>
  <text x="420" y="162" text-anchor="middle" font-size="10" fill="#7b341e">주문 처리 → 응답</text>
  <rect x="40" y="200" width="220" height="60" rx="10" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="150" y="225" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">본사 운영팀</text>
  <text x="150" y="245" text-anchor="middle" font-size="10" fill="#7b341e">(매장 직원 명단 갱신)</text>
  <line x1="260" y1="220" x2="370" y2="155" stroke="#475569" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#m5-s)"/>
  <text x="310" y="200" text-anchor="middle" font-size="9" font-style="italic" fill="#475569">직원 감시 (입사·퇴사 추적)</text>
  <rect x="540" y="200" width="200" height="60" rx="10" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="640" y="222" text-anchor="middle" font-size="11" font-weight="700" fill="#94a3b8">분배 시스템</text>
  <text x="640" y="242" text-anchor="middle" font-size="10" fill="#94a3b8">최신 명단 참조 (4단계)</text>
  <line x1="260" y1="240" x2="540" y2="240" stroke="#475569" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#m5-s)"/>
  <text x="400" y="232" text-anchor="middle" font-size="9" font-style="italic" fill="#475569">갱신된 직원 명단 전달</text>
</svg>
</div>

이 비유를 IT로 옮기면 두 가지가 짝지어집니다.

| 비유 | IT 용어 | 한 줄 설명 |
|:---:|:---|:---|
| 매장 직원 | **Pod** | 비즈니스 로직을 실행하는 백엔드 인스턴스입니다 |
| 본사 운영팀 | **Endpoint Controller** | Pod 변동을 감시해 Service의 Pod IP 목록을 최신으로 유지합니다 |

요청이 백엔드 Pod에 닿습니다. 애플리케이션이 비즈니스 로직을 실행해 응답을 돌려보냅니다. 이 과정 내내 Endpoint Controller는 뒤에서 Pod IP 목록을 최신으로 유지합니다.

<div class="svg-figure">
<svg viewBox="0 0 800 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="STEP 5 — 요청이 Pod에 도달, Endpoint Controller는 백그라운드에서 Pod IP 목록 유지">
  <defs>
    <marker id="fl5-d" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#cbd5e1"/></marker>
    <marker id="fl5-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#ff7849"/></marker>
    <marker id="fl5-s" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#475569"/></marker>
  </defs>
  <rect x="20" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="91" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 1</text>
  <text x="91" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">진입 (NodePort)</text>
  <line x1="166" y1="31" x2="178" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl5-d)"/>
  <rect x="180" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="251" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 2</text>
  <text x="251" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">배달 (kube-proxy)</text>
  <line x1="326" y1="31" x2="338" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl5-d)"/>
  <rect x="340" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="411" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 3</text>
  <text x="411" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">라우팅 (Ingress + DNS)</text>
  <line x1="486" y1="31" x2="498" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl5-d)"/>
  <rect x="500" y="14" width="142" height="34" rx="6" fill="#fff" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="571" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">STEP 4</text>
  <text x="571" y="42" text-anchor="middle" font-size="10" fill="#94a3b8">NAT (kube-proxy 2차)</text>
  <line x1="646" y1="31" x2="658" y2="31" stroke="#cbd5e1" stroke-width="1.2" marker-end="url(#fl5-d)"/>
  <rect x="660" y="14" width="120" height="34" rx="6" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
  <text x="720" y="28" text-anchor="middle" font-size="10" font-weight="700" fill="#7b341e">STEP 5</text>
  <text x="720" y="42" text-anchor="middle" font-size="10" fill="#7b341e">도달 (Pod)</text>
  <rect x="20" y="100" width="160" height="80" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="100" y="132" text-anchor="middle" font-size="13" font-weight="600" fill="#94a3b8">Node Kube Proxy</text>
  <text x="100" y="155" text-anchor="middle" font-size="10" fill="#94a3b8">(STEP 4에서 선택한</text>
  <text x="100" y="170" text-anchor="middle" font-size="10" fill="#94a3b8">Pod IP로 전달)</text>
  <line x1="180" y1="140" x2="240" y2="140" stroke="#ff7849" stroke-width="2.6" marker-end="url(#fl5-a)"/>
  <text x="210" y="130" text-anchor="middle" font-size="10" font-style="italic" fill="#7b341e">전달</text>
  <rect x="240" y="100" width="280" height="100" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="380" y="125" text-anchor="middle" font-size="14" font-weight="700" fill="#7b341e">백엔드 Pod 그룹</text>
  <rect x="265" y="140" width="100" height="34" rx="17" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="315" y="162" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">Pod A</text>
  <rect x="395" y="140" width="100" height="34" rx="17" fill="#fff" stroke="#ff7849" stroke-width="2"/>
  <text x="445" y="162" text-anchor="middle" font-size="12" font-weight="700" fill="#7b341e">Pod B</text>
  <text x="380" y="192" text-anchor="middle" font-size="10" fill="#7b341e">애플리케이션 응답</text>
  <rect x="20" y="230" width="220" height="90" rx="8" fill="#fff4ed" stroke="#ff7849" stroke-width="2.6"/>
  <text x="130" y="255" text-anchor="middle" font-size="13" font-weight="700" fill="#7b341e">Endpoint Controller</text>
  <text x="130" y="275" text-anchor="middle" font-size="10" fill="#7b341e">(다섯 단계 내내</text>
  <text x="130" y="290" text-anchor="middle" font-size="10" fill="#7b341e">백그라운드 동작)</text>
  <text x="130" y="310" text-anchor="middle" font-size="10" fill="#7b341e">Pod IP 목록 갱신</text>
  <line x1="245" y1="255" x2="395" y2="180" stroke="#475569" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#fl5-s)"/>
  <text x="320" y="220" text-anchor="middle" font-size="10" font-style="italic" fill="#475569">Pod 감시 (살아있는 Pod 추적)</text>
  <rect x="540" y="230" width="240" height="90" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
  <text x="660" y="255" text-anchor="middle" font-size="11" font-weight="700" fill="#94a3b8">Kube Proxy</text>
  <text x="660" y="278" text-anchor="middle" font-size="10" fill="#94a3b8">Endpoint Controller가</text>
  <text x="660" y="293" text-anchor="middle" font-size="10" fill="#94a3b8">갱신한 Pod IP 목록을</text>
  <text x="660" y="308" text-anchor="middle" font-size="10" fill="#94a3b8">참조해 라우팅 (STEP 4)</text>
  <line x1="240" y1="265" x2="540" y2="265" stroke="#475569" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#fl5-s)"/>
  <text x="390" y="258" text-anchor="middle" font-size="10" font-style="italic" fill="#475569">Pod IP 목록 참조</text>
</svg>
</div>

*그림 5-36. Pod 도달. Endpoint Controller는 다섯 단계 내내 백그라운드에서 Pod IP 목록을 최신으로 유지*

다섯 단계를 한 표로 정리하면 다음과 같습니다.

| 단계 | 일하는 곳 | 진입점/프로그램 | 하는 일 | 의사결정 기준 |
|:-:|:--|:--|:--|:--|
| 1 | 외부 입구 | Service (NodePort/LoadBalancer) | 외부 요청을 클러스터 안으로 받는다 | 노드 IP, 포트 |
| 2 | 클러스터 안 | kube-proxy (1차) | Ingress Controller Pod로 요청을 보낸다 | Service ClusterIP, Pod IP 목록 |
| 3 | Ingress Controller + DNS | Ingress Controller, DNS | URL을 읽어 백엔드 Service를 정하고, 그 이름을 ClusterIP로 변환 | URL 경로, Host 헤더 → 이름 → ClusterIP |
| 4 | 백엔드 노드 | kube-proxy (2차) | ClusterIP를 살아있는 Pod IP로 바꾼다 | Service ClusterIP, Pod IP 목록 |
| 5 | 백엔드 Pod | 애플리케이션 | 비즈니스 로직 실행 | 요청 데이터 |

같은 다섯 단계지만 보는 정보의 깊이가 다릅니다. 프랜차이즈 비유 안에서는 둘 다 "**라우팅**"으로 묶이는데, 깊이 차이를 또렷이 보려고 잠깐 도로 메타포를 빌려옵니다. **톨게이트**는 차량 번호와 차종(IP·Port)만 확인하고 통과시킵니다. **안내데스크**는 차에 탄 사람의 용건(URL·Host)까지 듣고 적절한 길을 안내합니다. NodePort와 kube-proxy가 톨게이트 역할이라면, Ingress Controller가 안내데스크 역할입니다.

:::note
**L4와 L7**

네트워크에서는 IP·Port 같은 봉투 겉면 정보를 다루는 계층을 **L4(전송 계층)** , URL 경로·헤더 같은 봉투 안쪽 정보를 다루는 계층을 **L7(애플리케이션 계층)** 이라고 부릅니다. NodePort와 kube-proxy는 L4 정보로 일하고, 5.3.1에서 본 DNS·Endpoint Controller도 L4 영역에 머무릅니다. 다섯 단계 중 HTTP 본문(L7)까지 들여다보는 프로그램은 Ingress Controller 하나뿐입니다.
:::

따로 보면 복잡해 보이던 프로그램들이 한 줄로 늘어놓이니 그제야 머릿속에서 하나의 흐름으로 묶였습니다.

*'Service는 통로를 만들고 Ingress는 방향을 잡는다. 그 뒤에서 DNS, Endpoint Controller, kube-proxy가 받아 준다. 각자 맡은 일이 단순하니 관리하기도 편하겠다.'*

## 이것만은 기억하자

- **Service는 Pod의 변하지 않는 직통 전화번호입니다.** Pod는 소모품이라 IP가 수시로 바뀌지만, Service는 변하지 않는 주소를 제공합니다. 또한 하나의 Service에 여러 Pod를 연결해 요청을 골고루 나누는 로드밸런싱 기능도 수행합니다.
- **Service 뒤에서는 세 프로그램이 함께 동작합니다.** 클러스터 DNS는 Service 이름을 ClusterIP로 변환하고, Endpoint Controller는 Service에 연결된 살아있는 Pod IP 목록을 최신으로 유지하며, kube-proxy는 그 목록대로 각 노드 커널에 ClusterIP → Pod IP 규칙을 만듭니다. 이름이 Pod까지 닿기까지 두 단계 변환이 일어납니다.
- **Ingress는 프랜차이즈 공식 앱 역할을 합니다.** 숫자(IP/Port)만 보는 Service와 달리, Ingress는 도메인과 URL 경로를 읽고 적절한 Service로 연결하는 라우팅을 담당합니다. 메뉴 구성표 역할의 **리소스(YAML)** 와 앱을 실제로 구동하는 **컨트롤러(S/W)** 가 한 팀으로 움직이며, Minikube에서는 `minikube addons enable ingress`로 컨트롤러를 먼저 실행해 두어야 동작합니다.

네트워크 경로는 이제 완벽히 갖춰졌습니다. 하지만 프로젝트를 쿠버네티스에 실제로 올리려면 아직 해결해야 할 숙제가 남았습니다. DB 비밀번호를 이미지에 직접 포함할 수는 없으며, 컨테이너가 재시작될 때 소중한 데이터가 사라져서도 안 되기 때문입니다.

다음 챕터에서는 설정값(ConfigMap), 보안 비밀(Secret), 그리고 **데이터의 영속성(Volume)** 을 추가하여 챕터 3에서 만든 통합 구성을 쿠버네티스 위에 완벽하게 구현해 보겠습니다.
