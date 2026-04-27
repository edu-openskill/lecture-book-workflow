// ══ Layout ══ Layout issues, verified build, readability check

import { state, shared } from './state.js';
import { showToast } from './ui.js';
import { getSelectedFiles } from './files.js';
import { renderSvgPages, setBuildStatus } from './builder.js';
import { fetchImages } from './images.js';

// ── Verified Build + Polling ──

export async function buildVerified() {
  const btn = document.getElementById('verify-btn');
  btn.classList.add('running');
  btn.textContent = 'Verifying...';
  hideVerifyBanner();

  const reqBody = shared.currentMode === 'file'
    ? { mode: 'file', design_state: state }
    : { files: getSelectedFiles(), design_state: state };

  try {
    const resp = await fetch('/api/build-verified', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reqBody)
    });
    const data = await resp.json();
    if (data.ok) {
      pollVerification();
    } else {
      showVerifyBanner('error', data.error || '검증 시작 실패');
      btn.classList.remove('running');
      btn.textContent = 'Verified Build';
    }
  } catch (e) {
    showVerifyBanner('error', '서버 연결 오류');
    btn.classList.remove('running');
    btn.textContent = 'Verified Build';
  }
}

export function pollVerification() {
  if (shared._verifyPollTimer) clearTimeout(shared._verifyPollTimer);
  shared._verifyPollTimer = setTimeout(async () => {
    try {
      const resp = await fetch('/api/verification-status');
      const data = await resp.json();
      const btn = document.getElementById('verify-btn');

      if (data.running) {
        btn.textContent = `Verifying... (round ${data.round || '?'})`;
        pollVerification();
        return;
      }

      btn.classList.remove('running');
      btn.textContent = 'Verified Build';

      if (data.result) {
        const r = data.result;
        const autoCount = (r.auto_fixed || []).length;
        const manualCount = (r.manual_remaining || []).length;

        if (autoCount === 0 && manualCount === 0) {
          showVerifyBanner('success', `검증 완료 (${r.rounds}R) - 이슈 없음`);
        } else {
          const parts = [];
          if (autoCount) parts.push(`자동수정 ${autoCount}건`);
          if (manualCount) parts.push(`수동확인 ${manualCount}건`);
          showVerifyBanner('warning', `검증 완료 (${r.rounds}R) - ${parts.join(' + ')}`);
        }

        if (r.page_count) {
          renderSvgPages(r.page_count, r.svg_base || '/api/svg/');
          setBuildStatus(`${r.page_count}p / ${r.duration || '?'}s (verified)`);
        }

        fetchImages();
      }
    } catch (e) {
      const btn = document.getElementById('verify-btn');
      btn.classList.remove('running');
      btn.textContent = 'Verified Build';
    }
  }, 1000);
}

export function showVerifyBanner(type, message) {
  const banner = document.getElementById('verify-banner');
  banner.className = 'verify-banner ' + type;
  banner.innerHTML = `<button class="close-banner" onclick="hideVerifyBanner()">&times;</button>${message}`;
  banner.style.display = '';
}

export function hideVerifyBanner() {
  const banner = document.getElementById('verify-banner');
  banner.className = 'verify-banner';
  banner.style.display = 'none';
}

// ── Layout Issues ──

export async function fetchLayoutIssues() {
  try {
    const resp = await fetch('/api/layout-issues');
    shared._layoutData = await resp.json();
    renderLayoutIssues();
  } catch (e) {
    document.getElementById('layout-issues-panel').innerHTML =
      '<div class="layout-empty">레이아웃 데이터를 가져올 수 없습니다</div>';
  }
}

export function renderLayoutIssues() {
  const panel = document.getElementById('layout-issues-panel');
  const issues = shared._layoutData.issues || [];
  const usage = shared._layoutData.page_usage || [];

  if (!issues.length && !usage.length) {
    panel.innerHTML = '<div class="layout-empty">빌드 후 레이아웃 분석 결과가 표시됩니다.<br>Verified Build 버튼으로 검증을 시작하세요.</div>';
    return;
  }

  const autoCount = issues.filter(i => i.severity === 'auto_fixable').length;
  const manualCount = issues.filter(i => i.severity === 'manual').length;

  let html = '';

  html += `<div class="layout-summary">
    <div class="layout-stat ${issues.length === 0 ? 'good' : 'warn'}">
      <div class="stat-num">${issues.length}</div><div class="stat-label">총 이슈</div>
    </div>
    <div class="layout-stat ${autoCount === 0 ? 'good' : 'warn'}">
      <div class="stat-num">${autoCount}</div><div class="stat-label">자동수정</div>
    </div>
    <div class="layout-stat ${manualCount === 0 ? 'good' : 'warn'}">
      <div class="stat-num">${manualCount}</div><div class="stat-label">수동확인</div>
    </div>
  </div>`;

  if (usage.length) {
    html += '<div class="page-usage-chart">';
    usage.forEach(p => {
      const fillClass = p.usage >= 60 ? 'high' : p.usage >= 30 ? 'medium' : 'low';
      html += `<div class="page-usage-bar" onclick="goToPreviewPage(${p.page})">
        <span class="bar-label">p${p.page}</span>
        <div class="bar-track"><div class="bar-fill ${fillClass}" style="width:${p.usage}%"></div></div>
        <span class="bar-val">${p.usage}%${p.label ? ' ' + p.label : ''}</span>
      </div>`;
    });
    html += '</div>';
  }

  if (issues.length) {
    html += '<div class="issue-list">';
    issues.forEach(issue => {
      const badgeClass = issue.severity === 'auto_fixable' ? 'auto' : 'manual';
      const badgeText = issue.severity === 'auto_fixable' ? 'AUTO' : 'MANUAL';
      html += `<div class="issue-item" onclick="goToPreviewPage(${issue.page})">
        <span class="issue-badge ${badgeClass}">${badgeText}</span>
        <span class="issue-page">p${issue.page}</span>
        <div>
          <div class="issue-msg">${issue.message || issue.issue_type}</div>
          ${issue.suggestion ? '<div class="issue-suggestion">' + issue.suggestion + '</div>' : ''}
        </div>
      </div>`;
    });
    html += '</div>';
  }

  panel.innerHTML = html;
  updateIssueBadge();
}

export function updateIssueBadge() {
  const count = (shared._layoutData.issues || []).length;
  const badge = document.getElementById('issue-badge');
  if (!badge) return;
  badge.textContent = count;
  badge.style.display = count > 0 ? '' : 'none';
  if (count > 0) showToast(`레이아웃 이슈 ${count}건 발견`, 'warn');
}

// ── Readability Check ──

export function runReadabilityCheck() {
  const panel = document.getElementById('readability-panel');
  panel.innerHTML = '<div class="svg-loading">가독성 분석 중...</div>';

  const s = state;
  const checks = [];
  let score = 0;
  const maxScore = 10;

  const bodySize = parseFloat(s.typo.size);
  if (bodySize >= 9 && bodySize <= 12) { score++; checks.push({name: '본문 글자 크기', value: bodySize + 'pt', status: 'pass', note: '9~12pt 권장 범위 내'}); }
  else { checks.push({name: '본문 글자 크기', value: bodySize + 'pt', status: 'warn', note: bodySize < 9 ? '너무 작아 눈이 피로합니다' : '너무 커서 한 줄 글자 수가 줄어듭니다'}); }

  const leading = parseFloat(s.typo.leading);
  if (leading >= 1.4 && leading <= 1.8) { score++; checks.push({name: '행간', value: leading + 'em', status: 'pass', note: '1.4~1.8em 권장 범위 내'}); }
  else { checks.push({name: '행간', value: leading + 'em', status: 'warn', note: leading < 1.4 ? '줄이 빽빽해 가독성이 떨어집니다' : '줄 간격이 넓어 시선 이동이 불편합니다'}); }

  const tracking = parseFloat(s.typo.tracking);
  if (tracking >= -0.2 && tracking <= 0.5) { score++; checks.push({name: '자간', value: tracking + 'pt', status: 'pass', note: '-0.2~0.5pt 권장 범위 내'}); }
  else { checks.push({name: '자간', value: tracking + 'pt', status: 'warn', note: tracking < -0.2 ? '글자가 겹쳐 읽기 어렵습니다' : '글자 간격이 넓어 단어 인식이 어렵습니다'}); }

  const paraGap = parseFloat(s.typo.paragraphGap);
  if (paraGap >= 4 && paraGap <= 16) { score++; checks.push({name: '문단 간격', value: paraGap + 'pt', status: 'pass', note: '4~16pt 적정 범위'}); }
  else { checks.push({name: '문단 간격', value: paraGap + 'pt', status: 'warn', note: paraGap < 4 ? '문단 구분이 어렵습니다' : '문단 간격이 넓어 흐름이 끊깁니다'}); }

  const textColor = s.colors.text || '#1a1a1a';
  const textBrightness = parseInt(textColor.slice(1,3),16)*0.299 + parseInt(textColor.slice(3,5),16)*0.587 + parseInt(textColor.slice(5,7),16)*0.114;
  if (textBrightness < 80) { score++; checks.push({name: '텍스트 명도 대비', value: textColor, status: 'pass', note: '충분한 대비 (어두운 텍스트)'}); }
  else { checks.push({name: '텍스트 명도 대비', value: textColor, status: 'warn', note: '텍스트가 너무 밝아 읽기 어렵습니다'}); }

  const mL = parseInt(s.margins.left), mR = parseInt(s.margins.right);
  const mT = parseInt(s.margins.top), mB = parseInt(s.margins.bottom);
  if (mL >= 15 && mR >= 12 && mT >= 15 && mB >= 20) { score++; checks.push({name: '여백 충분성', value: `상${mT} 하${mB} 좌${mL} 우${mR}mm`, status: 'pass', note: '출판 기준 여백 충족'}); }
  else { checks.push({name: '여백 충분성', value: `상${mT} 하${mB} 좌${mL} 우${mR}mm`, status: 'warn', note: '제본/읽기 여백이 부족할 수 있습니다'}); }

  const codeSize = parseFloat(s.typoSizes.code);
  if (codeSize >= 7 && codeSize <= 10) { score++; checks.push({name: '코드 글자 크기', value: codeSize + 'pt', status: 'pass', note: '7~10pt 코드 가독 범위'}); }
  else { checks.push({name: '코드 글자 크기', value: codeSize + 'pt', status: 'warn', note: codeSize < 7 ? '코드가 너무 작아 읽기 어렵습니다' : '코드가 커서 줄 넘김이 많아집니다'}); }

  const h1 = parseFloat(s.typoSizes.h1), h2 = parseFloat(s.typoSizes.h2), h3 = parseFloat(s.typoSizes.h3);
  if (h1 > h2 && h2 > h3 && h3 > bodySize) { score++; checks.push({name: '제목 위계', value: `h1=${h1} > h2=${h2} > h3=${h3} > 본문=${bodySize}`, status: 'pass', note: '제목 크기 위계가 올바릅니다'}); }
  else { checks.push({name: '제목 위계', value: `h1=${h1}, h2=${h2}, h3=${h3}`, status: 'warn', note: '제목 크기 순서가 역전되어 있습니다'}); }

  const ratio = h1 / bodySize;
  if (ratio >= 1.8 && ratio <= 3.0) { score++; checks.push({name: 'h1/본문 비율', value: ratio.toFixed(1) + 'x', status: 'pass', note: '1.8~3.0x 권장 비율'}); }
  else { checks.push({name: 'h1/본문 비율', value: ratio.toFixed(1) + 'x', status: 'warn', note: ratio < 1.8 ? '제목이 본문과 구분되지 않습니다' : '제목이 지나치게 큽니다'}); }

  const format = s.page.format;
  if (format.includes('B5') || format.includes('크라운') || format.includes('신국')) { score++; checks.push({name: '판형 적합성', value: format, status: 'pass', note: '기술서적에 적합한 판형'}); }
  else { checks.push({name: '판형 적합성', value: format, status: 'warn', note: 'A4/A6은 기술서적 판형으로 비일반적'}); }

  const grade = score >= 9 ? 'A' : score >= 7 ? 'B' : score >= 5 ? 'C' : 'D';
  const gradeColor = score >= 9 ? '#10b981' : score >= 7 ? '#3b82f6' : score >= 5 ? '#f59e0b' : '#ef4444';

  let html = `<div style="text-align:center;padding:16px;">
    <div style="font-size:48px;font-weight:800;color:${gradeColor};">${grade}</div>
    <div style="font-size:14px;color:#6b7280;">가독성 점수 ${score}/${maxScore}</div>
  </div>`;

  html += '<div style="padding:0 12px;">';
  checks.forEach(c => {
    const icon = c.status === 'pass' ? '<span style="color:#10b981;">PASS</span>' : '<span style="color:#f59e0b;">WARN</span>';
    html += `<div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #f1f5f9;font-size:12px;">
      <span style="min-width:40px;font-weight:600;font-size:10px;">${icon}</span>
      <span style="min-width:100px;font-weight:600;">${c.name}</span>
      <span style="color:#6b7280;min-width:80px;">${c.value}</span>
      <span style="color:#94a3b8;flex:1;">${c.note}</span>
    </div>`;
  });
  html += '</div>';

  panel.innerHTML = html;
}
