<div class="svg-figure">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">1단계 — 주문 생성 이벤트 발행 → 오케스트레이터 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="12" fill="#3730a3">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="355" y="350" text-anchor="middle" font-size="9.5" font-weight="700" fill="#9a3412">주문 생성 이벤트</text><circle cx="392" cy="298" r="10" fill="#ff7849"/><text x="392" y="302" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="12" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="430" y1="134" x2="355" y2="248" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="414.5" y="192" text-anchor="start" font-size="13" font-weight="700" fill="#4f46e5">1. 주문 생성 이벤트 발행</text><line x1="355" y1="370" x2="355" y2="478" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="377" y="429" text-anchor="start" font-size="13" font-weight="700" fill="#3730a3">2. 오케스트레이터가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">1단계</text><text x="1146" y="132" font-size="20" font-weight="700" fill="#0f172a">1. 주문 생성 이벤트 발행</text><text x="1146" y="174" font-size="18" font-weight="400" fill="#475569">주문 서비스가 주문을</text><text x="1146" y="207" font-size="18" font-weight="400" fill="#475569">저장한 뒤 '주문 생성</text><text x="1146" y="240" font-size="18" font-weight="400" fill="#475569">이벤트'를 카프카에 발행합니다.</text><text x="1146" y="273" font-size="20" font-weight="700" fill="#0f172a">2. 오케스트레이터가 수신</text><text x="1146" y="315" font-size="18" font-weight="400" fill="#475569">오케스트레이터가 그 토픽을</text><text x="1146" y="348" font-size="18" font-weight="400" fill="#475569">구독하고 있다가 메시지를</text><text x="1146" y="381" font-size="18" font-weight="400" fill="#475569">받아 진행 상태를 기록합니다.</text>
 </svg>
</div>

*그림 4-5a. 1단계 — 주문 생성 이벤트 발행 → 오케스트레이터 수신*

<div class="svg-figure">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">2단계 — 재고 차감 명령 발행 → 상품 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="12" fill="#3730a3">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="355" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text><rect x="425" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="480" y="350" text-anchor="middle" font-size="9.5" font-weight="700" fill="#9a3412">재고 차감 명령</text><circle cx="517" cy="298" r="10" fill="#ff7849"/><text x="517" y="302" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="12" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="480" y1="478" x2="480" y2="372" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="502" y="429" text-anchor="start" font-size="13" font-weight="700" fill="#4f46e5">3. 재고 차감 명령 발행</text><line x1="480" y1="248" x2="660" y2="136" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="592" y="192" text-anchor="start" font-size="13" font-weight="700" fill="#3730a3">4. 상품 서비스가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">2단계</text><text x="1146" y="132" font-size="20" font-weight="700" fill="#0f172a">3. 재고 차감 명령 발행</text><text x="1146" y="174" font-size="18" font-weight="400" fill="#475569">오케스트레이터가 '재고 차감</text><text x="1146" y="207" font-size="18" font-weight="400" fill="#475569">명령'을 카프카에 발행합니다.</text><text x="1146" y="240" font-size="20" font-weight="700" fill="#0f172a">4. 상품 서비스가 수신</text><text x="1146" y="282" font-size="18" font-weight="400" fill="#475569">상품 서비스가 그 토픽을</text><text x="1146" y="315" font-size="18" font-weight="400" fill="#475569">구독하고 있다가 메시지를</text><text x="1146" y="348" font-size="18" font-weight="400" fill="#475569">받아 재고를 차감합니다.</text>
 </svg>
</div>

*그림 4-5b. 2단계 — 재고 차감 명령 발행 → 상품 수신*

<div class="svg-figure">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">3단계 — 재고 차감 이벤트 발행(상품) → 오케스트레이터 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="12" fill="#3730a3">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="355" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text><rect x="425" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="480" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">재고 차감 명령</text><rect x="550" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M550 290 L605 311 L660 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="605" y="350" text-anchor="middle" font-size="9.5" font-weight="700" fill="#9a3412">재고 차감 이벤트</text><circle cx="642" cy="298" r="10" fill="#ff7849"/><text x="642" y="302" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="12" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="660" y1="134" x2="605" y2="248" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="654.5" y="192" text-anchor="start" font-size="13" font-weight="700" fill="#4f46e5">5. 재고 차감 이벤트 발행</text><line x1="605" y1="370" x2="605" y2="478" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="627" y="429" text-anchor="start" font-size="13" font-weight="700" fill="#3730a3">6. 오케스트레이터가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">3단계</text><text x="1146" y="132" font-size="20" font-weight="700" fill="#0f172a">5. 재고 차감 이벤트 발행</text><text x="1146" y="174" font-size="18" font-weight="400" fill="#475569">상품 서비스가 재고를 줄인 뒤</text><text x="1146" y="207" font-size="18" font-weight="400" fill="#475569">성공 여부를 '재고 차감</text><text x="1146" y="240" font-size="18" font-weight="400" fill="#475569">이벤트'로 카프카에 발행합니다.</text><text x="1146" y="273" font-size="20" font-weight="700" fill="#0f172a">6. 오케스트레이터가 수신</text><text x="1146" y="315" font-size="18" font-weight="400" fill="#475569">오케스트레이터가 그 토픽을</text><text x="1146" y="348" font-size="18" font-weight="400" fill="#475569">구독하고 있다가 메시지를</text><text x="1146" y="381" font-size="18" font-weight="400" fill="#475569">받아 성공을 확인합니다.</text>
 </svg>
</div>

*그림 4-5c. 3단계 — 재고 차감 이벤트 발행(상품) → 오케스트레이터 수신*

<div class="svg-figure">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">4단계 — 배달 생성 명령 발행 → 배달 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="12" fill="#3730a3">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="355" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text><rect x="425" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="480" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">재고 차감 명령</text><rect x="550" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M550 290 L605 311 L660 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="605" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">재고 차감 이벤트</text><rect x="675" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M675 290 L730 311 L785 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="730" y="350" text-anchor="middle" font-size="9.5" font-weight="700" fill="#9a3412">배달 생성 명령</text><circle cx="767" cy="298" r="10" fill="#ff7849"/><text x="767" y="302" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="12" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="730" y1="478" x2="730" y2="372" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="752" y="429" text-anchor="start" font-size="13" font-weight="700" fill="#4f46e5">7. 배달 생성 명령 발행</text><line x1="730" y1="248" x2="890" y2="136" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="832" y="192" text-anchor="start" font-size="13" font-weight="700" fill="#3730a3">8. 배달 서비스가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">4단계</text><text x="1146" y="132" font-size="20" font-weight="700" fill="#0f172a">7. 배달 생성 명령 발행</text><text x="1146" y="174" font-size="18" font-weight="400" fill="#475569">오케스트레이터가 '배달 생성</text><text x="1146" y="207" font-size="18" font-weight="400" fill="#475569">명령'을 카프카에 발행합니다.</text><text x="1146" y="240" font-size="20" font-weight="700" fill="#0f172a">8. 배달 서비스가 수신</text><text x="1146" y="282" font-size="18" font-weight="400" fill="#475569">배달 서비스가 그 토픽을</text><text x="1146" y="315" font-size="18" font-weight="400" fill="#475569">구독하고 있다가 메시지를</text><text x="1146" y="348" font-size="18" font-weight="400" fill="#475569">받아 배달을 생성합니다.</text>
 </svg>
</div>

*그림 4-5d. 4단계 — 배달 생성 명령 발행 → 배달 수신*

<div class="svg-figure">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">5단계 — 배달 생성 이벤트 발행(배달) → 오케스트레이터 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="12" fill="#3730a3">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="355" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text><rect x="425" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="480" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">재고 차감 명령</text><rect x="550" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M550 290 L605 311 L660 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="605" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">재고 차감 이벤트</text><rect x="675" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M675 290 L730 311 L785 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="730" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">배달 생성 명령</text><rect x="800" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M800 290 L855 311 L910 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="855" y="350" text-anchor="middle" font-size="9.5" font-weight="700" fill="#9a3412">배달 생성 이벤트</text><circle cx="892" cy="298" r="10" fill="#ff7849"/><text x="892" y="302" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="12" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="890" y1="134" x2="855" y2="248" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="894.5" y="192" text-anchor="start" font-size="13" font-weight="700" fill="#4f46e5">9. 배달 생성 이벤트 발행</text><line x1="855" y1="370" x2="855" y2="478" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="877" y="429" text-anchor="start" font-size="13" font-weight="700" fill="#3730a3">10. 오케스트레이터가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">5단계</text><text x="1146" y="132" font-size="20" font-weight="700" fill="#0f172a">9. 배달 생성 이벤트 발행</text><text x="1146" y="174" font-size="18" font-weight="400" fill="#475569">배달 서비스가 배달을 만든 뒤</text><text x="1146" y="207" font-size="18" font-weight="400" fill="#475569">성공 여부를 '배달 생성</text><text x="1146" y="240" font-size="18" font-weight="400" fill="#475569">이벤트'로 카프카에 발행합니다.</text><text x="1146" y="273" font-size="20" font-weight="700" fill="#0f172a">10. 오케스트레이터가 수신</text><text x="1146" y="315" font-size="18" font-weight="400" fill="#475569">오케스트레이터가 그 토픽을</text><text x="1146" y="348" font-size="18" font-weight="400" fill="#475569">구독하고 있다가 메시지를</text><text x="1146" y="381" font-size="18" font-weight="400" fill="#475569">받아 성공을 확인합니다.</text>
 </svg>
</div>

*그림 4-5e. 5단계 — 배달 생성 이벤트 발행(배달) → 오케스트레이터 수신*

<div class="svg-figure">
<svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">6단계 — 주문 완료 명령 발행 → 주문 수신</text>
  <rect x="345" y="64" width="170" height="70" rx="8" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8"/>
 <text x="430" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#3730a3">Order</text>
 <text x="430" y="116" text-anchor="middle" font-size="12" fill="#3730a3">:8081 주문</text><rect x="575" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="660" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Product</text>
 <text x="660" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8082 상품</text><rect x="805" y="64" width="170" height="70" rx="8" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
 <text x="890" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="#94a3b8">Delivery</text>
 <text x="890" y="116" text-anchor="middle" font-size="12" fill="#cbd5e1">:8084 배달</text><rect x="280" y="250" width="780" height="120" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="250" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="265" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text><rect x="300" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M300 290 L355 311 L410 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="355" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">주문 생성 이벤트</text><rect x="425" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M425 290 L480 311 L535 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="480" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">재고 차감 명령</text><rect x="550" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M550 290 L605 311 L660 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="605" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">재고 차감 이벤트</text><rect x="675" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M675 290 L730 311 L785 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="730" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">배달 생성 명령</text><rect x="800" y="290" width="110" height="42" rx="3" fill="#fff" stroke="#ff7849" stroke-width="1"/>
   <path d="M800 290 L855 311 L910 290" fill="none" stroke="#ff7849" stroke-width="0.8"/>
   <text x="855" y="350" text-anchor="middle" font-size="9.5" font-weight="400" fill="#cbd5e1">배달 생성 이벤트</text><rect x="925" y="290" width="110" height="42" rx="3" fill="#ffedd5" stroke="#ff7849" stroke-width="1.8"/>
   <path d="M925 290 L980 311 L1035 290" fill="none" stroke="#ff7849" stroke-width="1.4"/>
   <text x="980" y="350" text-anchor="middle" font-size="9.5" font-weight="700" fill="#9a3412">주문 완료 명령</text><circle cx="1017" cy="298" r="10" fill="#ff7849"/><text x="1017" y="302" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">1</text><rect x="300" y="480" width="760" height="88" rx="10" fill="#c7d2fe" stroke="#4f46e5" stroke-width="2.4"/>
 <text x="680" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#312e81">Orchestrator</text>
 <text x="680" y="538" text-anchor="middle" font-size="12" fill="#312e81">흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행</text><line x1="980" y1="478" x2="980" y2="372" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/><text x="1002" y="429" text-anchor="start" font-size="13" font-weight="700" fill="#4f46e5">11. 주문 완료 명령 발행</text><line x1="980" y1="248" x2="430" y2="136" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/><text x="727" y="192" text-anchor="start" font-size="13" font-weight="700" fill="#3730a3">12. 주문 서비스가 수신</text><rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">6단계</text><text x="1146" y="132" font-size="20" font-weight="700" fill="#0f172a">11. 주문 완료 명령 발행</text><text x="1146" y="174" font-size="18" font-weight="400" fill="#475569">오케스트레이터가 '주문 완료</text><text x="1146" y="207" font-size="18" font-weight="400" fill="#475569">명령'을 카프카에 발행합니다.</text><text x="1146" y="240" font-size="20" font-weight="700" fill="#0f172a">12. 주문 서비스가 수신</text><text x="1146" y="282" font-size="18" font-weight="400" fill="#475569">주문 서비스가 그 토픽을</text><text x="1146" y="315" font-size="18" font-weight="400" fill="#475569">구독하고 있다가 메시지를</text><text x="1146" y="348" font-size="18" font-weight="400" fill="#475569">받아 주문을 COMPLETED로</text><text x="1146" y="381" font-size="18" font-weight="400" fill="#475569">바꿉니다.</text>
 </svg>
</div>

*그림 4-5f. 6단계 — 주문 완료 명령 발행 → 주문 수신*