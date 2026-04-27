// ══ Tables ══ Per-table column width control

import { state } from './state.js';
import { scheduleDesignRebuild } from './builder.js';

let _tableList = [];

export function renderTableList(tables) {
  _tableList = tables || [];
  const container = document.getElementById('table-column-list');
  const badge = document.getElementById('table-count-badge');
  if (!container) return;

  if (!_tableList.length) {
    container.innerHTML = '<div class="img-empty">빌드 후 표 목록이 표시됩니다</div>';
    if (badge) badge.textContent = '';
    return;
  }
  if (badge) badge.textContent = `(${_tableList.length})`;

  container.innerHTML = _tableList.map(tbl => {
    const hasOverride = !!(state.tableOverrides && state.tableOverrides[tbl.idx]);
    const headerPreview = tbl.headers.join(' | ') || `${tbl.cols}열`;

    // current widths: override or auto-detected fr values → percentages
    let widths;
    if (hasOverride) {
      widths = state.tableOverrides[tbl.idx];
    } else {
      const total = tbl.widths.reduce((s, v) => s + v, 0);
      widths = tbl.widths.map(w => Math.round(w / total * 100));
    }

    const sliders = widths.map((w, ci) => {
      const label = tbl.headers[ci] || `열${ci + 1}`;
      return `<div class="tbl-col-row">
        <span class="tbl-col-label" title="${label}">${label}</span>
        <input type="range" class="tbl-col-slider" min="5" max="80" value="${w}"
          data-table="${tbl.idx}" data-col="${ci}"
          oninput="onTableSlider(${tbl.idx}, ${ci}, parseInt(this.value))"
          onchange="applyTableOverride(${tbl.idx})">
        <span class="tbl-col-val" id="tbl-val-${tbl.idx}-${ci}">${w}%</span>
      </div>`;
    }).join('');

    return `<div class="tbl-item${hasOverride ? ' overridden' : ''}" id="tbl-item-${tbl.idx}">
      <div class="tbl-header">
        <span class="tbl-idx">${tbl.label || '표 ' + tbl.idx}</span>
        <span class="tbl-preview">${tbl.est_page ? 'p.' + tbl.est_page + ' ' : ''}${headerPreview}</span>
        <button class="img-reset" title="자동으로 되돌리기" onclick="resetTableOverride(${tbl.idx})">&times;</button>
      </div>
      <div class="tbl-sliders">${sliders}</div>
    </div>`;
  }).join('');
}

// Slider drag: redistribute proportionally, keep sum ~100%
export function onTableSlider(tableIdx, colIdx, newVal) {
  const tbl = _tableList.find(t => t.idx === tableIdx);
  if (!tbl) return;

  const ncols = tbl.cols;
  const overrides = state.tableOverrides || {};
  let widths;
  if (overrides[tableIdx]) {
    widths = [...overrides[tableIdx]];
  } else {
    const total = tbl.widths.reduce((s, v) => s + v, 0);
    widths = tbl.widths.map(w => Math.round(w / total * 100));
  }

  const oldVal = widths[colIdx];
  const delta = newVal - oldVal;
  widths[colIdx] = newVal;

  // redistribute delta among other columns proportionally
  const otherIdxs = [];
  for (let i = 0; i < ncols; i++) {
    if (i !== colIdx && widths[i] > 5) otherIdxs.push(i);
  }
  if (otherIdxs.length > 0) {
    const otherTotal = otherIdxs.reduce((s, i) => s + widths[i], 0);
    let remaining = -delta;
    otherIdxs.forEach((i, idx) => {
      if (idx === otherIdxs.length - 1) {
        widths[i] = Math.max(5, widths[i] + remaining);
      } else {
        const share = Math.round(remaining * (widths[i] / otherTotal));
        widths[i] = Math.max(5, widths[i] + share);
        remaining -= share;
      }
    });
  }

  // normalize to 100%
  const sum = widths.reduce((s, v) => s + v, 0);
  if (sum !== 100) {
    const factor = 100 / sum;
    widths = widths.map(w => Math.round(w * factor));
    const diff = 100 - widths.reduce((s, v) => s + v, 0);
    widths[colIdx] += diff;
  }

  // update UI labels
  widths.forEach((w, i) => {
    const label = document.getElementById(`tbl-val-${tableIdx}-${i}`);
    if (label) label.textContent = `${w}%`;
    const slider = document.querySelector(`input[data-table="${tableIdx}"][data-col="${i}"]`);
    if (slider && i !== colIdx) slider.value = w;
  });

  // store temp (applied on change)
  if (!state.tableOverrides) state.tableOverrides = {};
  state.tableOverrides[tableIdx] = widths;
}

export function applyTableOverride(tableIdx) {
  if (!state.tableOverrides || !state.tableOverrides[tableIdx]) return;
  const item = document.getElementById(`tbl-item-${tableIdx}`);
  if (item) item.classList.add('overridden');
  scheduleDesignRebuild();
}

export function resetTableOverride(tableIdx) {
  if (!state.tableOverrides) return;
  delete state.tableOverrides[tableIdx];
  const item = document.getElementById(`tbl-item-${tableIdx}`);
  if (item) item.classList.remove('overridden');

  // restore auto-detected widths in UI
  const tbl = _tableList.find(t => t.idx === tableIdx);
  if (tbl) {
    const total = tbl.widths.reduce((s, v) => s + v, 0);
    const widths = tbl.widths.map(w => Math.round(w / total * 100));
    widths.forEach((w, i) => {
      const label = document.getElementById(`tbl-val-${tableIdx}-${i}`);
      if (label) label.textContent = `${w}%`;
      const slider = document.querySelector(`input[data-table="${tableIdx}"][data-col="${i}"]`);
      if (slider) slider.value = w;
    });
  }
  scheduleDesignRebuild();
}
