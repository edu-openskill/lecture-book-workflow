// ══ API ══ Server communication (project info, connection status)

import { shared } from './state.js';

export async function fetchProject() {
  try {
    const resp = await fetch('/api/project');
    shared.projectInfo = await resp.json();
    document.getElementById('project-name').textContent = shared.projectInfo.name || '?';
    shared._serverConnected = true;
    hideServerBanner();
  } catch (e) {
    document.getElementById('project-name').textContent = '연결 실패';
    shared._serverConnected = false;
    showServerBanner();
  }
}

export function showServerBanner() {
  let banner = document.getElementById('server-offline-banner');
  if (!banner) {
    banner = document.createElement('div');
    banner.id = 'server-offline-banner';
    banner.style.cssText = 'padding:10px 16px;background:#fef3c7;border-bottom:1px solid #f59e0b;font-size:12px;color:#92400e;line-height:1.5;';
    banner.innerHTML = '<b>프리뷰 서버가 꺼져 있습니다.</b> 터미널에서 아래 명령으로 서버를 먼저 시작하세요.<br><code style="background:#fff7ed;padding:2px 6px;border-radius:3px;font-size:11px;">python3 .claude/skills/pub-studio/references/preview.py [프로젝트명]</code>';
    const sidebar = document.querySelector('.sidebar');
    sidebar.insertBefore(banner, sidebar.children[1]);
  }
  banner.style.display = 'block';
}

export function hideServerBanner() {
  const banner = document.getElementById('server-offline-banner');
  if (banner) banner.style.display = 'none';
}

// ── Custom Variants API ──

export async function fetchVariants() {
  try {
    const resp = await fetch('/api/variants');
    return await resp.json();
  } catch (e) {
    return { ok: false, variants: {} };
  }
}

export async function saveVariant(component, variantId, name, properties) {
  const resp = await fetch('/api/variants/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ component, variantId, name, properties }),
  });
  return resp.json();
}

export async function deleteVariant(component, variantId) {
  const resp = await fetch('/api/variants/delete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ component, variantId }),
  });
  return resp.json();
}
