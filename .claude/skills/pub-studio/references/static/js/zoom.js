// ══ Zoom ══ Zoom controls

import { shared } from './state.js';

export function setZoom(level) {
  shared.zoomLevel = Math.max(30, Math.min(200, level));
  document.getElementById('zoom-level').textContent = shared.zoomLevel + '%';
  const viewer = document.getElementById('svg-viewer');
  const viewerW = viewer.clientWidth - 40;
  const pageW = Math.round(viewerW * shared.zoomLevel / 100);
  document.querySelectorAll('.svg-page').forEach(page => {
    page.style.width = pageW + 'px';
  });
}

export function zoomIn() { setZoom(shared.zoomLevel + 15); }
export function zoomOut() { setZoom(shared.zoomLevel - 15); }
export function zoomFit() {
  const viewer = document.getElementById('svg-viewer');
  const viewerW = viewer.clientWidth - 40;
  // 100% 기준으로 페이지 크기 측정 후 맞춤
  setZoom(100);
  const firstPage = viewer.querySelector('.svg-page');
  if (firstPage && firstPage.offsetWidth > 0) {
    setZoom(Math.min(100, Math.round(viewerW / firstPage.offsetWidth * 100)));
  }
}
