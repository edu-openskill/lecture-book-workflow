// ══ Design ══ Presets, component toggles, save/load, sync UI

import { state, PRESETS, shared, BUILTIN_VARIANTS } from './state.js';
import { render } from './renderer.js';
import { showToast } from './ui.js';
import { scheduleDesignRebuild } from './builder.js';

// Lazy-loaded to avoid circular deps (variants.js imports builder.js)
let _variantsModule = null;
async function getVariants() {
  if (!_variantsModule) _variantsModule = await import('./variants.js');
  return _variantsModule;
}

export function applyPreset(id) {
  state.preset = id;
  document.querySelectorAll('.preset-btn').forEach(b => b.classList.toggle('active', b.dataset.preset === id));
  if (PRESETS[id]) {
    state.components = { ...PRESETS[id].components };
    state.componentStyles = {};
    syncToggleUI();
    getVariants().then(m => {
      m.applyAllGlobals();
      syncTypoSizesUI();
      m.renderAllPropertyEditors();
      render();
      scheduleDesignRebuild();
    });
  } else {
    render();
    scheduleDesignRebuild();
  }
}

export function syncTypoSizesUI() {
  for (const k of ['h1','h2','h3','code','quote','table','inline-code']) {
    const stateKey = k === 'inline-code' ? 'inlineCode' : k;
    const v = state.typoSizes[stateKey];
    const range = document.getElementById(k + '-size');
    const num = document.getElementById(k + '-size-num');
    if (range) range.value = v;
    if (num) num.value = v;
  }
}

export function setComponent(comp, design) {
  state.components[comp] = design;
  state.preset = 'custom';
  document.querySelectorAll('.preset-btn').forEach(b => b.classList.toggle('active', b.dataset.preset === 'custom'));
  render();
  scheduleDesignRebuild();
  // Refresh variant buttons + property editor + label
  getVariants().then(m => {
    m.renderVariantButtons(comp);
    m.renderPropertyEditor(comp);
    m.updateAllVariantLabels();
  });
}

export function syncToggleUI(singleComp) {
  // Dynamic variant buttons — delegate to renderVariantButtons
  getVariants().then(m => {
    const comps = singleComp ? [singleComp] : ['body','heading','code','inline_code','quote','table','toc'];
    comps.forEach(c => m.renderVariantButtons(c));
  });
}

export function updateFont(type) { state.fonts[type] = document.getElementById('font-' + type).value; render(); scheduleDesignRebuild(); }

export function updateTypo() {
  state.typo.size = parseFloat(document.getElementById('body-size').value);
  state.typo.tracking = parseFloat(document.getElementById('body-tracking').value);
  state.typo.leading = parseFloat(document.getElementById('body-leading').value);
  state.typo.paragraphGap = parseInt(document.getElementById('para-gap').value);
  render();
  scheduleDesignRebuild();
}

export function updateTypoSizes() {
  state.typoSizes.h1 = parseFloat(document.getElementById('h1-size').value);
  state.typoSizes.h2 = parseFloat(document.getElementById('h2-size').value);
  state.typoSizes.h3 = parseFloat(document.getElementById('h3-size').value);
  state.typoSizes.code = parseFloat(document.getElementById('code-size').value);
  state.typoSizes.quote = parseFloat(document.getElementById('quote-size').value);
  state.typoSizes.table = parseFloat(document.getElementById('table-size').value);
  state.typoSizes.inlineCode = parseFloat(document.getElementById('inline-code-size').value);
  for (const k of ['h1','h2','h3','code','quote','table','inline-code']) {
    const stateKey = k === 'inline-code' ? 'inlineCode' : k;
    const v = state.typoSizes[stateKey];
    const range = document.getElementById(k + '-size');
    const num = document.getElementById(k + '-size-num');
    if (range) range.value = v;
    if (num) num.value = v;
  }
  render();
  scheduleDesignRebuild();
}

export function updateTocDepth() {
  state.tocDepth = parseInt(document.getElementById('toc-depth').value);
  scheduleDesignRebuild();
}

export function updatePageFormat() {
  state.page.format = document.getElementById('page-format').value;
  render();
  scheduleDesignRebuild();
}

export function setOutputMode(mode) {
  state.page.outputMode = mode;
  document.querySelectorAll('#output-mode-row .toggle-btn').forEach(b => {
    b.classList.toggle('active', b.textContent.trim() === (mode === 'pod' ? 'POD' : '전자책'));
  });
  const labelLeft = document.getElementById('label-margin-left');
  const labelRight = document.getElementById('label-margin-right');
  if (mode === 'pod') {
    labelLeft.textContent = '안쪽(제본)';
    labelRight.textContent = '바깥쪽';
    state.margins.left = 22; state.margins.right = 17;
  } else {
    labelLeft.textContent = '좌측';
    labelRight.textContent = '우측';
    state.margins.left = 20; state.margins.right = 20;
  }
  updateMarginUI();
  render();
  scheduleDesignRebuild();
}

export function updateMarginUI() {
  document.getElementById('margin-top').value = state.margins.top;
  document.getElementById('margin-top-num').value = state.margins.top;
  document.getElementById('margin-bottom').value = state.margins.bottom;
  document.getElementById('margin-bottom-num').value = state.margins.bottom;
  document.getElementById('margin-left').value = state.margins.left;
  document.getElementById('margin-left-num').value = state.margins.left;
  document.getElementById('margin-right').value = state.margins.right;
  document.getElementById('margin-right-num').value = state.margins.right;
}

export function updateMargin() {
  state.margins.top = parseInt(document.getElementById('margin-top').value);
  state.margins.bottom = parseInt(document.getElementById('margin-bottom').value);
  state.margins.left = parseInt(document.getElementById('margin-left').value);
  state.margins.right = parseInt(document.getElementById('margin-right').value);
  render();
  scheduleDesignRebuild();
}

export function setImgPreset(type, preset) {
  state.images[type].preset = preset;
  document.querySelectorAll(`.border-preset-group[data-imgtype="${type}"] .border-preset-btn`).forEach(b => b.classList.toggle('active', b.dataset.border === preset));
  render();
  scheduleDesignRebuild();
}

export function updateImgWidth(type) { state.images[type].width = parseInt(document.getElementById('img-w-' + type).value); render(); scheduleDesignRebuild(); }

export function updateColor() {
  state.colors.primary = document.getElementById('color-primary').value;
  state.colors.text = document.getElementById('color-text').value;
  state.colors.codeText = document.getElementById('color-code').value;
  state.colors.quoteBg = document.getElementById('color-quote-bg').value;
  document.getElementById('color-primary-hex').textContent = state.colors.primary;
  document.getElementById('color-text-hex').textContent = state.colors.text;
  document.getElementById('color-code-hex').textContent = state.colors.codeText;
  document.getElementById('color-quote-bg-hex').textContent = state.colors.quoteBg;
  render();
  scheduleDesignRebuild();
}

export function exportConfig() {
  const compNames = ['body','heading','code','inline_code','quote','table','toc'];
  const allSame = compNames.every(c => state.components[c] === state.components.body);
  let designFlag;
  if (allSame) { designFlag = `--design ${state.components.body === 'd1' ? '1' : '2'}`; }
  else { const p = compNames.filter(c => state.components[c] === 'd2').map(c => `${c}=2`); designFlag = p.length ? `--design "${p.join(',')}"` : '--design 1'; }
  const config = {
    design_flag: designFlag,
    fonts: { body: state.fonts.body.split(',')[0].replace(/"/g,'').trim(), code: state.fonts.code.split(',')[0].replace(/"/g,'').trim() },
    typography: { body_size: state.typo.size+'pt', tracking: state.typo.tracking+'pt', leading: state.typo.leading+'em', paragraph_gap: state.typo.paragraphGap+'pt' },
    margins: { top: state.margins.top+'mm', bottom: state.margins.bottom+'mm', left: state.margins.left+'mm', right: state.margins.right+'mm' },
    images: state.images, colors: { ...state.colors },
    typoSizes: { ...state.typoSizes }, tocDepth: state.tocDepth
  };
  navigator.clipboard.writeText(designFlag + '\n\n' + JSON.stringify(config, null, 2)).then(() => showToast('설정이 클립보드에 복사되었습니다'));
}

export function resetAll() {
  Object.assign(state, {
    preset: '1',
    components: { body:'d1',heading:'d1',code:'d1',inline_code:'d1',quote:'d1',table:'d1',toc:'d1' },
    fonts: { body: '"RIDIBatang", serif', code: '"D2Coding", monospace' },
    typo: { size: 10, tracking: 0, leading: 1.5, paragraphGap: 8 },
    margins: { top: 20, bottom: 28, left: 20, right: 20 },
    images: { gemini: { preset:'bordered', width:70 }, terminal: { preset:'minimal', width:70 }, diagram: { preset:'minimal', width:60 } },
    colors: { primary: '#2563eb', text: '#1a1a1a', codeText: '#1e40af', quoteBg: '#f5f8ff' },
    typoSizes: { h1: 26, h2: 16, h3: 13, h4: 11, code: 8, quote: 9, table: 8.5, inlineCode: 8.5 },
    tocDepth: 2,
    imageOverrides: {},
    componentStyles: {},
  });
  document.querySelectorAll('.preset-btn').forEach(b => b.classList.toggle('active', b.dataset.preset === '1'));
  syncToggleUI();
  syncTypoSizesUI();
  document.getElementById('font-body').value = '"RIDIBatang", serif';
  document.getElementById('font-code').value = '"D2Coding", monospace';
  const vals = { 'body-size':10,'body-tracking':0,'body-leading':1.5,'para-gap':8,'margin-top':20,'margin-bottom':28,'margin-left':20,'margin-right':20,'img-w-gemini':70,'img-w-terminal':70,'img-w-diagram':60 };
  for (const [k,v] of Object.entries(vals)) { document.getElementById(k).value = v; const n = document.getElementById(k+'-num'); if(n) n.value = v; }
  document.getElementById('color-primary').value = '#2563eb';
  document.getElementById('color-text').value = '#1a1a1a';
  document.getElementById('color-code').value = '#1e40af';
  document.getElementById('color-quote-bg').value = '#f5f8ff';
  ['color-primary-hex','color-text-hex','color-code-hex','color-quote-bg-hex'].forEach((id,i) => {
    document.getElementById(id).textContent = ['#2563eb','#1a1a1a','#1e40af','#f5f8ff'][i];
  });
  for (const type of ['gemini','terminal','diagram']) {
    const def = state.images[type].preset;
    document.querySelectorAll(`.border-preset-group[data-imgtype="${type}"] .border-preset-btn`).forEach(b => b.classList.toggle('active', b.dataset.border === def));
  }
  render();
  getVariants().then(m => m.renderAllPropertyEditors());
  showToast('기본값으로 초기화되었습니다');
}

// ── Design Save/Load ──

export async function fetchDesigns() {
  try {
    const resp = await fetch('/api/designs?full=true');
    const data = await resp.json();
    shared._designCache = data.designs || {};
    renderDesignList();
  } catch (e) {
    shared._designCache = {};
    renderDesignList();
  }
}

export function renderDesignList() {
  const container = document.getElementById('saved-design-list');
  const names = Object.keys(shared._designCache);
  if (names.length === 0) {
    container.innerHTML = '<div style="font-size:11px;color:#9ca3af;padding:8px 0;text-align:center;">저장된 디자인이 없습니다</div>';
    return;
  }
  names.sort((a, b) => {
    const ta = (shared._designCache[a].updated_at || '');
    const tb = (shared._designCache[b].updated_at || '');
    return tb.localeCompare(ta);
  });
  container.innerHTML = names.map(name => {
    const entry = shared._designCache[name];
    const date = (entry.updated_at || '').slice(0, 10);
    const escaped = name.replace(/'/g, "\\'").replace(/"/g, '&quot;');
    return '<div class="saved-design-item" onclick="loadDesign(\'' + escaped + '\')">'
      + '<span class="dname" title="' + name.replace(/"/g, '&quot;') + '">' + name + '</span>'
      + '<span class="ddate">' + date + '</span>'
      + '<span class="ddel" onclick="event.stopPropagation();deleteDesign(\'' + escaped + '\')" title="삭제">x</span>'
      + '</div>';
  }).join('');
}

export async function saveDesign() {
  const input = document.getElementById('design-name-input');
  const name = input.value.trim();
  if (!name) { showToast('디자인 이름을 입력하세요'); return; }

  const resp = await fetch('/api/designs/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: name, state: state, overwrite: false }),
  });
  const data = await resp.json();

  if (data.error === 'duplicate') {
    if (confirm(data.message)) {
      const resp2 = await fetch('/api/designs/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, state: state, overwrite: true }),
      });
      const data2 = await resp2.json();
      if (data2.ok) { showToast('\'' + name + '\' 덮어쓰기 완료'); input.value = ''; fetchDesigns(); }
      else { showToast('저장 실패: ' + (data2.error || '')); }
    }
    return;
  }
  if (data.ok) { showToast('\'' + name + '\' 저장 완료'); input.value = ''; fetchDesigns(); }
  else { showToast('저장 실패: ' + (data.error || '')); }
}

export function loadDesign(name) {
  const entry = shared._designCache[name];
  if (!entry || !entry.state) { showToast('디자인 데이터를 찾을 수 없습니다'); return; }
  const s = entry.state;
  Object.assign(state, {
    preset: s.preset || 'custom',
    components: { ...s.components },
    fonts: { ...s.fonts },
    typo: { ...s.typo },
    margins: { ...s.margins },
    images: {
      gemini: { ...s.images.gemini },
      terminal: { ...s.images.terminal },
      diagram: { ...s.images.diagram },
    },
    colors: { ...s.colors },
    page: { ...s.page },
    typoSizes: { ...s.typoSizes },
    tocDepth: s.tocDepth || 2,
    imageOverrides: {},
    componentStyles: s.componentStyles ? JSON.parse(JSON.stringify(s.componentStyles)) : {},
  });
  syncAllUI();
  render();
  scheduleDesignRebuild();
  showToast('\'' + name + '\' 불러오기 완료');
}

export function syncAllUI() {
  document.querySelectorAll('.preset-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.preset === state.preset)
  );
  syncToggleUI();
  syncTypoSizesUI();
  const fb = document.getElementById('font-body'); if (fb) fb.value = state.fonts.body;
  const fc = document.getElementById('font-code'); if (fc) fc.value = state.fonts.code;
  const typoMap = { 'body-size': state.typo.size, 'body-tracking': state.typo.tracking,
    'body-leading': state.typo.leading, 'para-gap': state.typo.paragraphGap };
  for (const [k, v] of Object.entries(typoMap)) {
    const el = document.getElementById(k); if (el) el.value = v;
    const n = document.getElementById(k + '-num'); if (n) n.value = v;
  }
  const marginMap = { 'margin-top': state.margins.top, 'margin-bottom': state.margins.bottom,
    'margin-left': state.margins.left, 'margin-right': state.margins.right };
  for (const [k, v] of Object.entries(marginMap)) {
    const el = document.getElementById(k); if (el) el.value = v;
    const n = document.getElementById(k + '-num'); if (n) n.value = v;
  }
  const colorMap = { 'color-primary': state.colors.primary, 'color-text': state.colors.text,
    'color-code': state.colors.codeText, 'color-quote-bg': state.colors.quoteBg };
  for (const [id, v] of Object.entries(colorMap)) {
    const el = document.getElementById(id); if (el) el.value = v;
    const hex = document.getElementById(id + '-hex'); if (hex) hex.textContent = v;
  }
  for (const type of ['gemini', 'terminal', 'diagram']) {
    const w = state.images[type].width;
    const p = state.images[type].preset;
    const wEl = document.getElementById('img-w-' + type); if (wEl) wEl.value = w;
    const wN = document.getElementById('img-w-' + type + '-num'); if (wN) wN.value = w;
    document.querySelectorAll('.border-preset-group[data-imgtype="' + type + '"] .border-preset-btn')
      .forEach(b => b.classList.toggle('active', b.dataset.border === p));
  }
  const pf = document.getElementById('page-format'); if (pf) pf.value = state.page.format;
  document.querySelectorAll('#output-mode-row .toggle-btn').forEach(b => {
    const isPod = state.page.outputMode === 'pod';
    b.classList.toggle('active', (isPod && b.textContent.trim() === 'POD') || (!isPod && b.textContent.trim() !== 'POD'));
  });
  // 컴포넌트별 속성 편집기 갱신 (글로벌 타이포 값 포함)
  getVariants().then(m => m.renderAllPropertyEditors());
}

export async function deleteDesign(name) {
  if (!confirm('\'' + name + '\' 디자인을 삭제하시겠습니까?')) return;
  try {
    const resp = await fetch('/api/designs/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name }),
    });
    const data = await resp.json();
    if (data.ok) { showToast('\'' + name + '\' 삭제 완료'); fetchDesigns(); }
    else { showToast('삭제 실패: ' + (data.error || '')); }
  } catch (e) { showToast('서버 연결 오류'); }
}

// ── Preset CRUD (presets.json) ──

let _presetsCache = {};

export async function fetchPresets() {
  try {
    const resp = await fetch('/api/presets');
    const data = await resp.json();
    _presetsCache = data.presets || {};
    renderPresetList();
  } catch (e) {
    _presetsCache = {};
    renderPresetList();
  }
}

export function renderPresetList() {
  const container = document.getElementById('preset-list');
  if (!container) return;
  const ids = Object.keys(_presetsCache).sort((a, b) => parseInt(a) - parseInt(b));
  if (ids.length === 0) {
    container.innerHTML = '<div style="font-size:11px;color:#9ca3af;padding:8px 0;text-align:center;">프리셋이 없습니다</div>';
    return;
  }
  container.innerHTML = ids.map(id => {
    const p = _presetsCache[id];
    const name = p.name || '이름 없음';
    const desc = p.description || '';
    return '<div class="saved-design-item" onclick="applyPresetFromJSON(\'' + id + '\')" style="cursor:pointer;">'
      + '<span class="dname" title="' + desc + '"><b>' + id + '</b> ' + name + '</span>'
      + '<span class="preset-actions">'
      + '<span class="preset-act" onclick="event.stopPropagation();renamePreset(\'' + id + '\')" title="이름 수정">&#9998;</span>'
      + '<span class="preset-act" onclick="event.stopPropagation();updatePresetValues(\'' + id + '\')" title="현재 설정으로 덮어쓰기">&#8635;</span>'
      + '<span class="ddel" onclick="event.stopPropagation();deletePreset(\'' + id + '\')" title="삭제">x</span>'
      + '</span>'
      + '</div>';
  }).join('');
}

export async function saveAsPreset() {
  const name = prompt('프리셋 이름을 입력하세요:');
  if (!name) return;
  const description = prompt('설명 (선택):') || '';

  const resp = await fetch('/api/presets/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, description, components: { ...state.components } }),
  });
  const data = await resp.json();
  if (data.ok) {
    showToast('프리셋 ' + data.id + '번 \'' + name + '\' 저장 완료');
    fetchPresets();
  } else {
    showToast('저장 실패: ' + (data.error || ''));
  }
}

export function applyPresetFromJSON(id) {
  const p = _presetsCache[id];
  if (!p || !p.components) { showToast('프리셋 데이터를 찾을 수 없습니다'); return; }
  state.preset = 'custom';
  state.components = { ...p.components };
  state.componentStyles = {};
  const ov = p.overrides || {};
  syncToggleUI();
  import('./variants.js').then(m => {
    // 1. variant _globals 먼저 적용 (기본값)
    m.applyAllGlobals();
    // 2. preset overrides를 그 위에 적용 (우선순위 높음)
    if (ov.typo) Object.assign(state.typo, ov.typo);
    if (ov.typoSizes) Object.assign(state.typoSizes, ov.typoSizes);
    if (ov.margins) Object.assign(state.margins, ov.margins);
    if (ov.page) Object.assign(state.page, ov.page);
    if (ov.componentStyles) state.componentStyles = JSON.parse(JSON.stringify(ov.componentStyles));
    if (ov.tocDepth != null) state.tocDepth = ov.tocDepth;
    if (ov.tocSpacing != null) state.tocSpacing = ov.tocSpacing;
    if (ov.images) state.images = JSON.parse(JSON.stringify(ov.images));
    if (ov.colors) Object.assign(state.colors, ov.colors);
    syncTypoSizesUI();
    m.renderAllPropertyEditors();
    render();
    scheduleDesignRebuild();
  });
  showToast('프리셋 ' + id + '번 \'' + (p.name || '') + '\' 적용');
}

export async function renamePreset(id) {
  const p = _presetsCache[id];
  if (!p) return;
  const newName = prompt('새 이름:', p.name || '');
  if (!newName || newName === p.name) return;
  const newDesc = prompt('설명 (Enter로 유지):', p.description || '');
  try {
    const body = { id, name: newName };
    if (newDesc !== null) body.description = newDesc;
    const resp = await fetch('/api/presets/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await resp.json();
    if (data.ok) { showToast('프리셋 ' + id + '번 이름 변경 완료'); fetchPresets(); }
    else { showToast('수정 실패: ' + (data.error || '')); }
  } catch (e) { showToast('서버 연결 오류'); }
}

export async function updatePresetValues(id) {
  const p = _presetsCache[id];
  if (!p) return;
  if (!confirm('프리셋 ' + id + '번 \'' + (p.name || '') + '\'을 현재 설정으로 덮어쓰시겠습니까?')) return;
  try {
    const overrides = {
      page: { ...state.page },
      margins: { ...state.margins },
      typo: { ...state.typo },
      typoSizes: { ...state.typoSizes },
      tocDepth: state.tocDepth,
      tocSpacing: state.tocSpacing,
      images: JSON.parse(JSON.stringify(state.images)),
      colors: { ...state.colors },
    };
    if (Object.keys(state.componentStyles).length > 0) {
      overrides.componentStyles = JSON.parse(JSON.stringify(state.componentStyles));
    }
    const resp = await fetch('/api/presets/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, components: { ...state.components }, overrides }),
    });
    const data = await resp.json();
    if (data.ok) { showToast('프리셋 ' + id + '번 설정 업데이트 완료'); fetchPresets(); }
    else { showToast('업데이트 실패: ' + (data.error || '')); }
  } catch (e) { showToast('서버 연결 오류'); }
}

export async function deletePreset(id) {
  const p = _presetsCache[id];
  const name = p ? p.name : id;
  if (!confirm('프리셋 ' + id + '번 \'' + name + '\'을 삭제하시겠습니까?')) return;
  try {
    const resp = await fetch('/api/presets/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id }),
    });
    const data = await resp.json();
    if (data.ok) { showToast('프리셋 ' + id + '번 삭제 완료'); fetchPresets(); }
    else { showToast('삭제 실패: ' + (data.error || '')); }
  } catch (e) { showToast('서버 연결 오류'); }
}
