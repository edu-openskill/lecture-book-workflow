// ══ Images ══ Individual image control

import { state, shared } from './state.js';
import { showToast } from './ui.js';
import { scheduleDesignRebuild } from './builder.js';

export async function fetchImages() {
  try {
    const resp = await fetch('/api/images');
    const data = await resp.json();
    shared._imageList = data.images || [];
    renderImageList();
  } catch (e) { /* silent */ }
}

export function renderImageList() {
  const container = document.getElementById('img-individual-list');
  const badge = document.getElementById('img-count-badge');
  if (!shared._imageList.length) {
    container.innerHTML = '<div class="img-empty">빌드 후 이미지 목록이 표시됩니다</div>';
    badge.textContent = '';
    return;
  }
  badge.textContent = `(${shared._imageList.length})`;
  container.innerHTML = shared._imageList.map(img => {
    const hasOverride = img.override_width !== null || img.override_style !== null;
    const width = Math.round((img.override_width ?? img.default_width) * 100);
    const escapedPath = img.path.replace(/'/g, "\\'");
    return `<div class="img-individual-item${hasOverride ? ' overridden' : ''}">
      <div class="img-thumb" title="${img.category}"></div>
      <div class="img-info">
        <span class="img-name" title="${img.path}">${img.figure_label || img.rel_path.split('/').slice(-3).join('/')}</span>
        <span class="img-cat">${img.category} / ${img.default_style}</span>
      </div>
      <input type="range" class="img-width-slider" min="30" max="100" step="5" value="${width}"
        oninput="this.nextElementSibling.textContent=this.value+'%'"
        onchange="setImageOverride('${escapedPath}', parseInt(this.value))">
      <span class="img-width-val">${width}%</span>
      <button class="img-reset" title="초기화" onclick="resetImageOverride('${escapedPath}')">&times;</button>
    </div>`;
  }).join('');
}

export async function setImageOverride(path, widthPercent) {
  state.imageOverrides[path] = { width: widthPercent };
  try {
    await fetch('/api/image-override', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path, width: widthPercent })
    });
    scheduleDesignRebuild();
  } catch (e) {
    showToast('이미지 오버라이드 실패');
  }
}

export async function resetImageOverride(path) {
  delete state.imageOverrides[path];
  try {
    await fetch('/api/image-override', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path, reset: true })
    });
    scheduleDesignRebuild();
    fetchImages();
  } catch (e) {
    showToast('초기화 실패');
  }
}
