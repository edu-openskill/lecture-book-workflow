
const SX={Order:430, Product:660, Delivery:890};
const SVC_Y=64, SVC_H=70, SVC_BOT=134;
const KFK_Y=250, KFK_H=120, KFK_TOP=250, KFK_BOT=370;
const ORC_Y=480, ORC_H=88, ORC_TOP=480;
const TLAB=["주문 생성 이벤트","재고 차감 명령","재고 차감 이벤트","배달 생성 명령","배달 생성 이벤트","주문 완료 명령"];
const TX=[355,480,605,730,855,980]; // ex=300+i*125, 중심 ex+55
function svcBox(name,x,strong){
 const f=strong?"#eef2ff":"#fff", st=strong?"#4f46e5":"#cbd5e1", tc=strong?"#3730a3":"#94a3b8";
 const sub={Order:":8081 주문",Product:":8082 상품",Delivery:":8084 배달"}[name];
 return `<rect x="${x-85}" y="${SVC_Y}" width="170" height="${SVC_H}" rx="8" fill="${f}" stroke="${st}" stroke-width="${strong?1.8:1.4}"/>
 <text x="${x}" y="${SVC_Y+30}" text-anchor="middle" font-size="16" font-weight="700" fill="${tc}">${name}</text>
 <text x="${x}" y="${SVC_Y+52}" text-anchor="middle" font-size="12" fill="${strong?'#3730a3':'#cbd5e1'}">${sub}</text>`;
}
function kafka(msgIdx){
 let g=`<rect x="280" y="${KFK_Y}" width="780" height="${KFK_H}" rx="9" fill="#fff4ed" stroke="#ff7849" stroke-width="2"/>
 <rect x="280" y="${KFK_Y}" width="780" height="22" fill="#ff7849"/>
 <text x="670" y="${KFK_Y+15}" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Kafka — 토픽별로 메시지를 보관·전달</text>`;
 for(let i=0;i<=msgIdx;i++){
   const ex=300+i*125, on=i===msgIdx;
   g+=`<rect x="${ex}" y="${KFK_Y+40}" width="110" height="42" rx="3" fill="${on?'#ffedd5':'#fff'}" stroke="#ff7849" stroke-width="${on?1.8:1}"/>
   <path d="M${ex} ${KFK_Y+40} L${ex+55} ${KFK_Y+61} L${ex+110} ${KFK_Y+40}" fill="none" stroke="#ff7849" stroke-width="${on?1.4:0.8}"/>
   <text x="${ex+55}" y="${KFK_Y+100}" text-anchor="middle" font-size="9.5" font-weight="${on?700:400}" fill="${on?'#9a3412':'#cbd5e1'}">${TLAB[i]}</text>`;
   if(on) g+=`<circle cx="${ex+92}" cy="${KFK_Y+48}" r="10" fill="#ff7849"/><text x="${ex+92}" y="${KFK_Y+52}" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">1</text>`;
 }
 return g;
}
function orch(strong){
 const f=strong?"#c7d2fe":"#eef0f6", st=strong?"#4f46e5":"#cbd5e1", tc=strong?"#312e81":"#94a3b8";
 return `<rect x="300" y="${ORC_Y}" width="760" height="${ORC_H}" rx="10" fill="${f}" stroke="${st}" stroke-width="${strong?2.4:1.8}"/>
 <text x="680" y="${ORC_Y+34}" text-anchor="middle" font-size="20" font-weight="700" fill="${tc}">Orchestrator</text>
 <text x="680" y="${ORC_Y+58}" text-anchor="middle" font-size="12" fill="${strong?'#312e81':'#cbd5e1'}">${strong?'흐름을 결정하는 지휘자 — event를 받아 다음 command를 발행':'이 단계에 관여하지 않음'}</text>`;
}
function num(cx,cy,n,c){return `<circle cx="${cx}" cy="${cy}" r="14" fill="${c}"/><text x="${cx}" y="${cy+5}" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">${n}</text>`;}
// 발행 화살표: from(서비스 or 오케) → Kafka 토픽
function pub(fromKind, sx, ti, label, n){
 const tx=TX[ti];
 if(fromKind==="svc"){ // 서비스(위) → Kafka : 아래로
   return `<line x1="${sx}" y1="${SVC_BOT}" x2="${tx}" y2="${KFK_TOP-2}" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/>`     +`<text x="${(sx+tx)/2+22}" y="${(SVC_BOT+KFK_TOP)/2}" text-anchor="start" font-size="13" font-weight="700" fill="#4f46e5">${n}. ${label}</text>`;
 } else { // 오케(아래) → Kafka : 위로
   return `<line x1="${tx}" y1="${ORC_TOP-2}" x2="${tx}" y2="${KFK_BOT+2}" stroke="#4f46e5" stroke-width="2.6" marker-end="url(#mk)"/>`     +`<text x="${tx+22}" y="${(KFK_BOT+ORC_TOP)/2+4}" text-anchor="start" font-size="13" font-weight="700" fill="#4f46e5">${n}. ${label}</text>`;
 }
}
// 수신 화살표: Kafka 토픽 → to(서비스 or 오케)
function sub(toKind, tx2, ti, label, n){
 const tx=TX[ti];
 if(toKind==="orc"){ // Kafka → 오케(아래) : 아래로
   return `<line x1="${tx}" y1="${KFK_BOT}" x2="${tx}" y2="${ORC_TOP-2}" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/>`     +`<text x="${tx+22}" y="${(KFK_BOT+ORC_TOP)/2+4}" text-anchor="start" font-size="13" font-weight="700" fill="#3730a3">${n}. ${label}</text>`;
 } else { // Kafka → 서비스(위) : 위로
   return `<line x1="${tx}" y1="${KFK_TOP-2}" x2="${tx2}" y2="${SVC_BOT+2}" stroke="#3730a3" stroke-width="2.6" stroke-dasharray="5,3" marker-end="url(#mk2)"/>`     +`<text x="${(tx+tx2)/2+22}" y="${(SVC_BOT+KFK_TOP)/2}" text-anchor="start" font-size="13" font-weight="700" fill="#3730a3">${n}. ${label}</text>`;
 }
}
function memo(step,t,lines,base){
 let m=`<rect x="1090" y="40" width="460" height="510" rx="10" fill="#fffdf5" stroke="#e7d9a8" stroke-width="1.5"/>
  <line x1="1132" y1="40" x2="1132" y2="550" stroke="#f0e6c8" stroke-width="1.3"/>
  <text x="1146" y="84" font-size="22" font-weight="700" fill="#9a3412">${step}단계</text>`;
 let y=132, c=0;
 lines.forEach(L=>{
   const hd=L[0]==='■';
   const txt = hd ? `${base+(++c)}. ${L.replace('■','')}` : L;
   m+=`<text x="1146" y="${y}" font-size="${hd?20:18}" font-weight="${hd?700:400}" fill="${hd?'#0f172a':'#475569'}">${txt}</text>`;
   y+=hd?42:33;
 });
 return m;
}
function wrap(title,inner,cap){
 return `<div class="figure">
 <svg viewBox="260 30 1320 560" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="mk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4f46e5"/></marker>
   <marker id="mk2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3730a3"/></marker>
  </defs>
  <text x="680" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#0f172a">${title}</text>
  ${inner}
 </svg>
 <div class="figcap">${cap}</div></div>`;
}
// 6단계 정의: pubFrom(svc/orc, 서비스명), 토픽idx, subTo(orc/svc, 서비스명), 강조서비스
const STEPS=[
 {step:1, t:"주문 생성 이벤트 발행 → 오케스트레이터 수신",
  sv:{Order:1,Orchestrator:1}, pf:"svc", ps:"Order",  pi:0, pl:"주문 생성 이벤트 발행",
  sf:"orc", ss:null, si:0, sl:"오케스트레이터가 수신",
  m:["■주문 생성 이벤트 발행","주문 서비스가 주문을","저장한 뒤 '주문 생성","이벤트'를 카프카에 발행합니다.","■오케스트레이터가 수신","오케스트레이터가 그 토픽을","구독하고 있다가 메시지를","받아 진행 상태를 기록합니다."]},
 {step:2, t:"재고 차감 명령 발행 → 상품 수신",
  sv:{Orchestrator:1,Product:1}, pf:"orc", ps:null, pi:1, pl:"재고 차감 명령 발행",
  sf:"svc", ss:"Product", si:1, sl:"상품 서비스가 수신",
  m:["■재고 차감 명령 발행","오케스트레이터가 '재고 차감","명령'을 카프카에 발행합니다.","■상품 서비스가 수신","상품 서비스가 그 토픽을","구독하고 있다가 메시지를","받아 재고를 차감합니다."]},
 {step:3, t:"재고 차감 이벤트 발행(상품) → 오케스트레이터 수신",
  sv:{Product:1,Orchestrator:1}, pf:"svc", ps:"Product", pi:2, pl:"재고 차감 이벤트 발행",
  sf:"orc", ss:null, si:2, sl:"오케스트레이터가 수신",
  m:["■재고 차감 이벤트 발행","상품 서비스가 재고를 줄인 뒤","성공 여부를 '재고 차감","이벤트'로 카프카에 발행합니다.","■오케스트레이터가 수신","오케스트레이터가 그 토픽을","구독하고 있다가 메시지를","받아 성공을 확인합니다."]},
 {step:4, t:"배달 생성 명령 발행 → 배달 수신",
  sv:{Orchestrator:1,Delivery:1}, pf:"orc", ps:null, pi:3, pl:"배달 생성 명령 발행",
  sf:"svc", ss:"Delivery", si:3, sl:"배달 서비스가 수신",
  m:["■배달 생성 명령 발행","오케스트레이터가 '배달 생성","명령'을 카프카에 발행합니다.","■배달 서비스가 수신","배달 서비스가 그 토픽을","구독하고 있다가 메시지를","받아 배달을 생성합니다."]},
 {step:5, t:"배달 생성 이벤트 발행(배달) → 오케스트레이터 수신",
  sv:{Delivery:1,Orchestrator:1}, pf:"svc", ps:"Delivery", pi:4, pl:"배달 생성 이벤트 발행",
  sf:"orc", ss:null, si:4, sl:"오케스트레이터가 수신",
  m:["■배달 생성 이벤트 발행","배달 서비스가 배달을 만든 뒤","성공 여부를 '배달 생성","이벤트'로 카프카에 발행합니다.","■오케스트레이터가 수신","오케스트레이터가 그 토픽을","구독하고 있다가 메시지를","받아 성공을 확인합니다."]},
 {step:6, t:"주문 완료 명령 발행 → 주문 수신",
  sv:{Orchestrator:1,Order:1}, pf:"orc", ps:null, pi:5, pl:"주문 완료 명령 발행",
  sf:"svc", ss:"Order", si:5, sl:"주문 서비스가 수신",
  m:["■주문 완료 명령 발행","오케스트레이터가 '주문 완료","명령'을 카프카에 발행합니다.","■주문 서비스가 수신","주문 서비스가 그 토픽을","구독하고 있다가 메시지를","받아 주문을 COMPLETED로","바꿉니다."]},
];
function fig(S){
 let g="", b=(S.step-1)*2;
 ["Order","Product","Delivery"].forEach(n=> g+=svcBox(n,SX[n], !!S.sv[n]) );
 g+=kafka(S.pi)+orch(!!S.sv.Orchestrator);
 g+=pub(S.pf, S.ps?SX[S.ps]:0, S.pi, S.pl, b+1);
 g+=sub(S.sf, S.ss?SX[S.ss]:0, S.si, S.sl, b+2);
 g+=memo(S.step,S.t,S.m,b);
 return wrap(`${S.step}단계 — ${S.t}`, g, `그림 4-5${String.fromCharCode(96+S.step)}. ${S.step}단계 — ${S.t}`);
}
process.stdout.write(STEPS.map(fig).join(""));
