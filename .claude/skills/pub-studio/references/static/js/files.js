// ══ Files ══ File selector, file list, fetch files

import { shared } from './state.js';
import { showToast } from './ui.js';
import { scheduleDesignRebuild } from './builder.js';

export async function fetchFiles() {
  try {
    const resp = await fetch('/api/files');
    shared.fileList = await resp.json();
    renderFileSelector();
  } catch (e) {
    if (!shared._serverConnected) return;
    showToast('파일 목록 로드 실패');
  }
}

export function getSelectedFiles() {
  const files = { front: [], chapters: [], back: [] };
  document.querySelectorAll('.file-check:checked').forEach(cb => {
    const group = cb.dataset.group;
    if (files[group]) files[group].push(cb.dataset.path);
  });
  return files;
}

export function renderFileSelector() {
  const container = document.getElementById('file-selector');
  container.innerHTML = '';

  const groups = [
    { key: 'front', label: 'Front Matter', files: shared.fileList.front || [] },
    { key: 'chapters', label: 'Chapters', files: shared.fileList.chapters || [] },
    { key: 'back', label: 'Back Matter', files: shared.fileList.back || [] },
  ];

  groups.forEach(g => {
    if (!g.files.length) return;
    const checkedCount = g.files.filter(f => f.default_checked !== false).length;
    const allChecked = checkedCount === g.files.length;
    const div = document.createElement('div');
    div.className = 'file-group';
    div.innerHTML = `<div class="file-group-header">
      <input type="checkbox" ${allChecked ? 'checked' : ''} data-group="${g.key}" onchange="toggleFileGroup('${g.key}', this.checked)">
      <span>${g.label} (${checkedCount}/${g.files.length})</span>
    </div>`;

    g.files.forEach(f => {
      const isChecked = f.default_checked !== false;
      const isVersion = /\-v\d+\.md$/.test(f.name);
      const item = document.createElement('div');
      item.className = 'file-item';
      item.dataset.path = f.path;
      item.dataset.group = g.key;
      const sizeKB = f.size ? Math.round(f.size / 1024) : '';
      item.innerHTML = `<input type="checkbox" ${isChecked ? 'checked' : ''} class="file-check" data-path="${f.path}" data-group="${g.key}" onchange="onFileCheckChange()">
        <span class="fname${isVersion ? ' version-file' : ''}" onclick="openFileEditor('${f.path}')">${f.name.replace(/\.md$/, '')}</span>
        <span class="fedit" onclick="event.stopPropagation();openMdModal('${f.path}')" title="MD 편집">&#9998;</span>
        ${sizeKB ? '<span class="fsize">' + sizeKB + 'KB</span>' : ''}`;
      div.appendChild(item);
    });

    container.appendChild(div);
  });

  updateFileCount();
}

export function toggleFileSelectAll() {
  const checked = document.getElementById('file-select-all').checked;
  document.querySelectorAll('.file-check').forEach(cb => cb.checked = checked);
  document.querySelectorAll('.file-group-header input').forEach(cb => cb.checked = checked);
  updateFileCount();
  scheduleDesignRebuild(true);
}

export function toggleFileGroup(group, checked) {
  document.querySelectorAll(`.file-check[data-group="${group}"]`).forEach(cb => cb.checked = checked);
  updateFileCount();
  scheduleDesignRebuild(true);
}

export function onFileCheckChange() {
  updateFileCount();
  ['front', 'chapters', 'back'].forEach(g => {
    const checks = document.querySelectorAll(`.file-check[data-group="${g}"]`);
    const allChecked = Array.from(checks).every(c => c.checked);
    const header = document.querySelector(`.file-group-header input[data-group="${g}"]`);
    if (header) header.checked = allChecked;
  });
  const allChecks = document.querySelectorAll('.file-check');
  document.getElementById('file-select-all').checked = Array.from(allChecks).every(c => c.checked);
  scheduleDesignRebuild(true);
}

export function updateFileCount() {
  const total = document.querySelectorAll('.file-check').length;
  const selected = document.querySelectorAll('.file-check:checked').length;
  document.getElementById('file-count').textContent = `${selected}/${total}개 선택`;
}
