// ══ Renderer ══ DOM rendering, CSS variable injection, syntax highlighting

import { state, CODE_SAMPLE, BUILTIN_VARIANTS, VARIANT_SELECTORS, getAllVariants } from './state.js';

export function syncFromRange(rangeEl, numId) { document.getElementById(numId).value = rangeEl.value; }
export function syncFromNum(numEl, rangeId) { document.getElementById(rangeId).value = numEl.value; }

export function adjustColor(hex, amount) {
  const n = parseInt(hex.replace('#',''),16);
  let r = Math.min(255,Math.max(0,(n>>16)+amount)), g = Math.min(255,Math.max(0,((n>>8)&0xff)+amount)), b = Math.min(255,Math.max(0,(n&0xff)+amount));
  return '#'+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1);
}

export function highlightPython(code) {
  const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const lines = code.split('\n');
  return lines.map(line => {
    let out = '', i = 0;
    const raw = line;
    while (i < raw.length) {
      if (raw[i] === '#') { out += '<span class="syn-cmt">' + esc(raw.slice(i)) + '</span>'; break; }
      if (raw[i] === '"' || raw[i] === "'") {
        const q = raw[i]; let j = i + 1;
        while (j < raw.length && raw[j] !== q) { if (raw[j] === '\\') j++; j++; }
        out += '<span class="syn-str">' + esc(raw.slice(i, j + 1)) + '</span>'; i = j + 1; continue;
      }
      if (raw[i] === '@' && (i === 0 || /\s/.test(raw[i-1]))) {
        let j = i + 1; while (j < raw.length && /[\w.]/.test(raw[j])) j++;
        out += '<span class="syn-dec">' + esc(raw.slice(i, j)) + '</span>'; i = j; continue;
      }
      if (/[a-zA-Z_]/.test(raw[i])) {
        let j = i; while (j < raw.length && /[\w]/.test(raw[j])) j++;
        const word = raw.slice(i, j);
        const kws = ['from','import','def','async','await','return','class','if','elif','else','for','while','in','not','and','or','is','None','True','False','try','except','finally','with','as','pass','break','continue','yield','raise','lambda'];
        if (kws.includes(word)) { out += '<span class="syn-kw">' + word + '</span>'; }
        else if (j < raw.length && raw[j] === '(') { out += '<span class="syn-fn">' + word + '</span>'; }
        else { out += esc(word); }
        i = j; continue;
      }
      if (/[0-9]/.test(raw[i])) {
        let j = i; while (j < raw.length && /[0-9.]/.test(raw[j])) j++;
        out += '<span class="syn-num">' + raw.slice(i, j) + '</span>'; i = j; continue;
      }
      if ('=+-*/<>!:'.includes(raw[i])) {
        out += '<span class="syn-op">' + esc(raw[i]) + '</span>'; i++; continue;
      }
      out += esc(raw[i]); i++;
    }
    return out;
  }).join('\n');
}

export function applyCodeHighlight() {
  document.querySelectorAll('.book-code').forEach(el => {
    if (!el.dataset.raw) el.dataset.raw = CODE_SAMPLE;
    const lang = el.dataset.lang || '';
    if (lang === 'python' || lang === 'py' || !el.closest('#block-list')) {
      el.innerHTML = highlightPython(el.dataset.raw);
    } else {
      el.innerHTML = el.dataset.raw.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }
  });
}

// ── Dynamic Variant CSS ──

function camelToKebab(str) {
  return str.replace(/([A-Z])/g, '-$1').toLowerCase();
}

export function getEffectiveProperties(component, variantId) {
  const all = getAllVariants(component);
  const base = all[variantId] || {};
  const overrides = state.componentStyles[component] || {};
  return { ...base, ...overrides };
}

function generateComponentCSS(component, variantId, props) {
  const selectors = VARIANT_SELECTORS[component];
  if (!selectors) return '';

  const dAttr = `[data-design="${variantId}"]`;

  // Group properties by prefix
  const groups = {};
  for (const [key, value] of Object.entries(props)) {
    if (key === 'name' || key === '_globals') continue;
    const uIdx = key.indexOf('_');
    let prefix, prop;
    if (uIdx > 0 && selectors[key.substring(0, uIdx)] !== undefined) {
      prefix = key.substring(0, uIdx);
      prop = key.substring(uIdx + 1);
    } else if (selectors[''] !== undefined) {
      prefix = '';
      prop = key;
    } else {
      continue;
    }
    if (!groups[prefix]) groups[prefix] = {};
    groups[prefix][prop] = value;
  }

  let css = '';
  for (const [prefix, properties] of Object.entries(groups)) {
    const tmpl = selectors[prefix];
    if (!tmpl) continue;
    const selector = tmpl.replace('$D', dAttr);
    const decls = Object.entries(properties)
      .map(([p, v]) => `  ${camelToKebab(p)}: ${v};`)
      .join('\n');
    css += `${selector} {\n${decls}\n}\n`;
  }
  return css;
}

export function renderVariantCSS() {
  let css = '';
  for (const [comp, variantId] of Object.entries(state.components)) {
    if (comp === 'toc') continue; // toc has no CSS variants
    const props = getEffectiveProperties(comp, variantId);
    css += generateComponentCSS(comp, variantId, props);
  }
  const styleEl = document.getElementById('dynamic-variant-styles');
  if (styleEl) styleEl.textContent = css;
}

export function autoFitTableColumns() {
  document.querySelectorAll('.book-table').forEach((tbl, idx) => {
    const overrides = state.tableOverrides || {};
    if (overrides[idx]) {
      applyManualWidths(tbl, overrides[idx]);
      return;
    }
    autoFitByContent(tbl);
  });
}

function autoFitByContent(tbl) {
  const cols = tbl.querySelectorAll('thead th').length
    || tbl.querySelectorAll('tbody tr:first-child td').length;
  if (cols < 2) return;

  const maxLen = Array(cols).fill(1);
  tbl.querySelectorAll('tr').forEach(tr => {
    const cells = tr.querySelectorAll('th, td');
    cells.forEach((cell, i) => {
      if (i < cols) maxLen[i] = Math.max(maxLen[i], cell.textContent.trim().length);
    });
  });

  const total = maxLen.reduce((s, v) => s + v, 0);
  let cg = tbl.querySelector('colgroup');
  if (!cg) { cg = document.createElement('colgroup'); tbl.prepend(cg); }
  cg.innerHTML = maxLen.map(len =>
    `<col style="width:${(len / total * 100).toFixed(1)}%">`
  ).join('');
}

function applyManualWidths(tbl, widths) {
  let cg = tbl.querySelector('colgroup');
  if (!cg) { cg = document.createElement('colgroup'); tbl.prepend(cg); }
  cg.innerHTML = widths.map(w => `<col style="width:${w}%">`).join('');
}

export function render() {
  const r = document.documentElement.style;
  r.setProperty('--body-font', state.fonts.body);
  r.setProperty('--code-font', state.fonts.code);
  r.setProperty('--body-size', state.typo.size + 'pt');
  r.setProperty('--body-tracking', state.typo.tracking + 'pt');
  // CSS line-height = font-size + leading (Typst leading은 줄 사이 간격)
  r.setProperty('--body-leading', (state.typo.size + state.typo.leading) + 'pt');
  r.setProperty('--paragraph-gap', state.typo.paragraphGap + 'pt');
  r.setProperty('--page-margin-top', state.margins.top + 'mm');
  r.setProperty('--page-margin-bottom', state.margins.bottom + 'mm');
  r.setProperty('--page-margin-left', state.margins.left + 'mm');
  r.setProperty('--page-margin-right', state.margins.right + 'mm');
  r.setProperty('--color-primary', state.colors.primary);
  r.setProperty('--color-primary-dark', adjustColor(state.colors.primary, -30));
  r.setProperty('--color-primary-light', adjustColor(state.colors.primary, 80));
  r.setProperty('--color-text', state.colors.text);
  r.setProperty('--color-code-text', state.colors.codeText);
  r.setProperty('--color-quote-bg', state.colors.quoteBg);
  r.setProperty('--color-quote-border', adjustColor(state.colors.primary, 40));

  // typoSizes CSS 변수
  const szMap = { h1:'--h1-size', h2:'--h2-size', h3:'--h3-size', h4:'--h4-size', code:'--code-size', quote:'--quote-size', table:'--table-size', inlineCode:'--inline-code-size' };
  for (const [k,v] of Object.entries(szMap)) r.setProperty(v, (state.typoSizes[k]||10)+'pt');

  // 표 레이아웃 CSS 변수
  r.setProperty('--table-width', (state.tableWidth || 100) + '%');
  r.setProperty('--table-align', state.tableAlign || 'left');

  // 표 열 너비: 자동 맞춤 + 수동 오버라이드
  autoFitTableColumns();

  // 표에 인덱스 부여
  document.querySelectorAll('.book-table').forEach((tbl, i) => { tbl.dataset.tableIdx = i; });

  document.querySelectorAll('.book-body').forEach(el => el.dataset.design = state.components.body || 'd1');
  document.querySelectorAll('.book-h1,.book-h2,.book-h3,.book-h4').forEach(el => el.dataset.design = state.components.heading);
  document.querySelectorAll('.book-code').forEach(el => el.dataset.design = state.components.code);
  document.querySelectorAll('.book-inline-code').forEach(el => el.dataset.design = state.components.inline_code);
  document.querySelectorAll('.book-quote').forEach(el => el.dataset.design = state.components.quote);
  document.querySelectorAll('.book-table').forEach(el => el.dataset.design = state.components.table);

  for (const [type, cfg] of Object.entries(state.images)) {
    const el = document.getElementById('img-' + type);
    if (el) { el.className = 'image-placeholder style-' + cfg.preset; el.style.width = cfg.width + '%'; }
  }

  const d3 = document.getElementById('toc-depth3');
  if (d3) d3.style.display = state.components.toc === 'd2' ? 'block' : 'none';

  renderVariantCSS();
  updateMarginGuide();
  applyCodeHighlight();
}

export function updateMarginGuide() {
  const guide = document.getElementById('margin-guide');
  if (!guide) return;
  const frame = guide.parentElement;
  const w = frame.offsetWidth, scale = w / 188;
  guide.style.top = (state.margins.top * scale) + 'px';
  guide.style.bottom = (state.margins.bottom * scale) + 'px';
  guide.style.left = (state.margins.left * scale) + 'px';
  guide.style.right = (state.margins.right * scale) + 'px';
}
