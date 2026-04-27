// ══ Variants ══ Property editor UI, component style overrides, custom variant CRUD

import { state, BUILTIN_VARIANTS, COMPONENT_SCHEMAS, VARIANT_SELECTORS, customVariants, getAllVariants } from './state.js';
import { render, renderVariantCSS, getEffectiveProperties } from './renderer.js';
import { scheduleDesignRebuild } from './builder.js';
import { fetchVariants, saveVariant as apiSaveVariant, deleteVariant as apiDeleteVariant } from './api.js';
import { showToast } from './ui.js';

// ── State path helpers (for global properties) ──

function getStatePath(path) {
  const parts = path.split('.');
  let obj = state;
  for (const p of parts) obj = obj[p];
  return obj;
}

function setStatePath(path, value) {
  const parts = path.split('.');
  let obj = state;
  for (let i = 0; i < parts.length - 1; i++) obj = obj[parts[i]];
  obj[parts[parts.length - 1]] = value;
}

// ── Load custom variants from server ──

export async function loadCustomVariants() {
  const data = await fetchVariants();
  if (!data.ok) return;
  // Clear and repopulate
  for (const k of Object.keys(customVariants)) delete customVariants[k];
  for (const [comp, variants] of Object.entries(data.variants || {})) {
    customVariants[comp] = variants;
  }
}

// ── Next available variant ID for a component ──

function nextVariantId(component) {
  const all = getAllVariants(component);
  let n = 3;
  while (all['d' + n]) n++;
  return 'd' + n;
}

// ── Render variant toggle buttons for a component ──

export function renderVariantButtons(component) {
  const container = document.getElementById('variant-btns-' + component);
  if (!container) return;

  const all = getAllVariants(component);
  const current = state.components[component];

  let html = `<select class="variant-select" onchange="selectVariant('${component}', this.value)">`;
  for (const [vid, vdef] of Object.entries(all)) {
    const selected = vid === current ? ' selected' : '';
    html += `<option value="${vid}"${selected}>${vdef.name}</option>`;
  }
  html += `</select>`;
  html += `<button class="variant-btn variant-add-btn" onclick="showCreateVariantDialog('${component}')" title="새 변형 추가">+</button>`;
  container.innerHTML = html;
}

// ── Render all variant buttons ──

export function renderAllVariantButtons() {
  for (const comp of Object.keys(COMPONENT_SCHEMAS)) {
    renderVariantButtons(comp);
  }
}

// ── Apply _globals from a variant to state ──

function applyVariantGlobals(component, variantId) {
  const all = getAllVariants(component);
  const variant = all[variantId];
  if (!variant || !variant._globals) return;
  for (const [path, value] of Object.entries(variant._globals)) {
    setStatePath(path, value);
  }
}

// Apply _globals from all currently selected variants
export function applyAllGlobals() {
  for (const [comp, variantId] of Object.entries(state.components)) {
    applyVariantGlobals(comp, variantId);
  }
}

// ── Select a variant ──

export function selectVariant(component, variantId) {
  state.components[component] = variantId;
  applyVariantGlobals(component, variantId);
  renderVariantButtons(component);
  renderPropertyEditor(component);
  updateVariantLabel(component);
  render();
  scheduleDesignRebuild();
}

// ── Update single variant label ──

function updateVariantLabel(component) {
  const label = document.getElementById('variant-label-' + component);
  if (!label) return;
  const all = getAllVariants(component);
  const variant = all[state.components[component]];
  label.textContent = variant ? variant.name : state.components[component];
}

// ── Render property editor for a component ──

export function renderPropertyEditor(component) {
  const panel = document.getElementById('props-' + component);
  if (!panel) return;

  const schema = COMPONENT_SCHEMAS[component];
  if (!schema) { panel.innerHTML = ''; return; }

  const variantId = state.components[component];
  const effective = getEffectiveProperties(component, variantId);
  const overrides = state.componentStyles[component] || {};
  const all = getAllVariants(component);
  const isCustomVariant = !BUILTIN_VARIANTS[component]?.[variantId];

  let html = '';

  // Custom variant management buttons
  if (isCustomVariant && all[variantId]) {
    html += `<div class="variant-mgmt">`;
    html += `<span class="variant-custom-tag">커스텀</span>`;
    html += `<button class="variant-mgmt-btn" onclick="renameVariant('${component}','${variantId}')" title="이름 변경">이름</button>`;
    html += `<button class="variant-mgmt-btn variant-mgmt-del" onclick="removeVariant('${component}','${variantId}')" title="삭제">삭제</button>`;
    html += `<button class="variant-mgmt-btn" onclick="saveCurrentAsVariant('${component}','${variantId}')" title="현재 오버라이드를 이 변형에 저장">저장</button>`;
    html += `</div>`;
  }

  for (const [key, def] of Object.entries(schema)) {
    // Separator
    if (def.type === 'separator') {
      html += `<div class="prop-separator"><span>${def.label}</span></div>`;
      continue;
    }

    const isGlobal = !!def.global;
    let val, isOverridden;

    if (isGlobal) {
      val = getStatePath(def.global.path);
      isOverridden = false;
    } else {
      val = overrides[key] !== undefined ? overrides[key] : (effective[key] || '');
      isOverridden = overrides[key] !== undefined;
    }

    const cls = isOverridden ? ' overridden' : '';
    const escapedKey = key.replace(/'/g, "\\'");
    const escapedComp = component.replace(/'/g, "\\'");

    html += `<div class="prop-row${cls}">`;
    html += `<label class="prop-label">${def.label}</label>`;

    if (def.type === 'range') {
      const min = def.min ?? 0, max = def.max ?? 100, step = def.step ?? 1;
      const unit = def.unit || '';
      const numVal = parseFloat(val) || 0;
      html += `<input type="range" class="prop-range" min="${min}" max="${max}" step="${step}" value="${numVal}"
        oninput="this.nextElementSibling.value=this.value;updateComponentProp('${escapedComp}','${escapedKey}',this.value)">`;
      html += `<input type="number" class="prop-num" min="${min}" max="${max}" step="${step}" value="${numVal}"
        oninput="this.previousElementSibling.value=this.value;updateComponentProp('${escapedComp}','${escapedKey}',this.value)">`;
      if (unit) html += `<span class="prop-unit">${unit}</span>`;
    } else if (def.type === 'color') {
      html += `<input type="color" class="prop-color" value="${toHex(val)}"
        onchange="updateComponentProp('${escapedComp}','${escapedKey}',this.value)">`;
      html += `<span class="prop-color-label">${val}</span>`;
    } else if (def.type === 'select') {
      html += `<select class="prop-select" onchange="updateComponentProp('${escapedComp}','${escapedKey}',this.value)">`;
      for (const opt of (def.options || [])) {
        const optVal = typeof opt === 'object' ? opt.value : opt;
        const optLabel = typeof opt === 'object' ? opt.label : opt;
        html += `<option value="${optVal}"${String(optVal) === String(val) ? ' selected' : ''}>${optLabel}</option>`;
      }
      html += `</select>`;
    } else {
      html += `<input type="text" class="prop-text" value="${val}"
        onchange="updateComponentProp('${escapedComp}','${escapedKey}',this.value)">`;
    }

    if (isOverridden) {
      html += `<button class="prop-reset" title="기본값 복원" onclick="resetComponentProp('${escapedComp}','${escapedKey}')">&times;</button>`;
    }

    html += `</div>`;
  }

  panel.innerHTML = html;
}

// ── Render all component property editors ──

export function renderAllPropertyEditors() {
  for (const comp of Object.keys(COMPONENT_SCHEMAS)) {
    renderVariantButtons(comp);
    renderPropertyEditor(comp);
  }
  updateAllVariantLabels();
}

// ── Update variant name labels ──

export function updateAllVariantLabels() {
  for (const [comp, variantId] of Object.entries(state.components)) {
    updateVariantLabel(comp);
  }
}

// ── Update a single component property ──

export function updateComponentProp(component, key, value) {
  const def = (COMPONENT_SCHEMAS[component] || {})[key];

  // Global property → write to state path
  if (def && def.global) {
    const parsed = def.type === 'range' ? parseFloat(value) : (def.type === 'select' && /^\d+$/.test(value) ? parseInt(value) : value);
    setStatePath(def.global.path, parsed);
    render();
    scheduleDesignRebuild();
    return;
  }

  // Component style override
  if (!state.componentStyles[component]) {
    state.componentStyles[component] = {};
  }
  state.componentStyles[component][key] = value;
  renderVariantCSS();
  scheduleDesignRebuild();
}

// ── Reset a single property override ──

export function resetComponentProp(component, key) {
  if (state.componentStyles[component]) {
    delete state.componentStyles[component][key];
    if (Object.keys(state.componentStyles[component]).length === 0) {
      delete state.componentStyles[component];
    }
  }
  renderPropertyEditor(component);
  renderVariantCSS();
  scheduleDesignRebuild();
}

// ── Toggle component property panel ──

export function toggleCompProps(component) {
  const panel = document.getElementById('props-' + component);
  if (!panel) return;
  const isHidden = panel.style.display === 'none' || !panel.style.display;
  panel.style.display = isHidden ? 'block' : 'none';
  if (isHidden) renderPropertyEditor(component);
}

// ── Create variant dialog ──

export function showCreateVariantDialog(component) {
  const all = getAllVariants(component);
  const baseOptions = Object.entries(all).map(([vid, v]) =>
    `<option value="${vid}">${vid.toUpperCase()} - ${v.name}</option>`
  ).join('');

  const dialog = document.createElement('div');
  dialog.className = 'variant-dialog-overlay';
  dialog.innerHTML = `
    <div class="variant-dialog">
      <h4>새 변형 만들기 (${component})</h4>
      <label>이름</label>
      <input type="text" id="new-variant-name" placeholder="예: 네오 그린" autofocus>
      <label>기반 변형</label>
      <select id="new-variant-base">${baseOptions}</select>
      <div class="variant-dialog-actions">
        <button class="variant-dialog-cancel" onclick="this.closest('.variant-dialog-overlay').remove()">취소</button>
        <button class="variant-dialog-ok" onclick="createVariant('${component}')">생성</button>
      </div>
    </div>`;
  document.body.appendChild(dialog);
  dialog.querySelector('#new-variant-name').focus();
}

// ── Create variant from dialog ──

export async function createVariant(component) {
  const overlay = document.querySelector('.variant-dialog-overlay');
  const name = document.getElementById('new-variant-name').value.trim();
  const baseId = document.getElementById('new-variant-base').value;

  if (!name) { showToast('이름을 입력하세요', 'warn'); return; }

  const all = getAllVariants(component);
  const baseProps = { ...(all[baseId] || {}) };
  delete baseProps.name;

  const newId = nextVariantId(component);
  const result = await apiSaveVariant(component, newId, name, baseProps);

  if (result.error) { showToast(result.error, 'error'); return; }

  // Update local state
  if (!customVariants[component]) customVariants[component] = {};
  customVariants[component][newId] = { name, ...baseProps };

  overlay.remove();

  // Select the new variant
  selectVariant(component, newId);
  showToast(`${newId.toUpperCase()} "${name}" 생성됨`);
}

// ── Rename variant ──

export async function renameVariant(component, variantId) {
  const all = getAllVariants(component);
  const current = all[variantId];
  if (!current) return;

  const newName = prompt('변형 이름 변경', current.name);
  if (!newName || newName === current.name) return;

  const props = { ...current };
  delete props.name;
  const result = await apiSaveVariant(component, variantId, newName, props);
  if (result.error) { showToast(result.error, 'error'); return; }

  customVariants[component][variantId].name = newName;
  renderVariantButtons(component);
  updateVariantLabel(component);
  renderPropertyEditor(component);
  showToast(`이름 변경: "${newName}"`);
}

// ── Delete variant ──

export async function removeVariant(component, variantId) {
  if (!confirm(`${variantId.toUpperCase()} 변형을 삭제하시겠습니까?`)) return;

  const result = await apiDeleteVariant(component, variantId);
  if (result.error) { showToast(result.error, 'error'); return; }

  delete customVariants[component]?.[variantId];
  if (customVariants[component] && Object.keys(customVariants[component]).length === 0) {
    delete customVariants[component];
  }

  // Switch back to d1 if the deleted variant was active
  if (state.components[component] === variantId) {
    selectVariant(component, 'd1');
  } else {
    renderVariantButtons(component);
  }
  showToast(`${variantId.toUpperCase()} 삭제됨`);
}

// ── Save current overrides into custom variant ──

export async function saveCurrentAsVariant(component, variantId) {
  const all = getAllVariants(component);
  const base = all[variantId];
  if (!base) return;

  // Merge base properties with current overrides
  const overrides = state.componentStyles[component] || {};
  const merged = { ...base };
  delete merged.name;
  Object.assign(merged, overrides);

  const result = await apiSaveVariant(component, variantId, base.name, merged);
  if (result.error) { showToast(result.error, 'error'); return; }

  // Update local
  customVariants[component][variantId] = { name: base.name, ...merged };

  // Clear overrides since they're now baked into the variant
  if (state.componentStyles[component]) {
    delete state.componentStyles[component];
  }

  renderPropertyEditor(component);
  renderVariantCSS();
  showToast(`${variantId.toUpperCase()} 저장됨`);
}

// ── Helper: convert CSS color to hex ──

function toHex(color) {
  if (!color || color.startsWith('var(')) return '#888888';
  if (color.startsWith('#') && color.length === 7) return color;
  if (color.startsWith('#') && color.length === 4) {
    return '#' + color[1]+color[1] + color[2]+color[2] + color[3]+color[3];
  }
  return '#888888';
}
